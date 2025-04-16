import asyncio
from collections.abc import AsyncGenerator
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from acp_sdk.models import (
    Agent as AgentModel,
)
from acp_sdk.models import (
    AgentName,
    AgentReadResponse,
    AgentsListResponse,
    Run,
    RunCancelResponse,
    RunCreateRequest,
    RunCreateResponse,
    RunId,
    RunMode,
    RunReadResponse,
    RunResumeRequest,
    RunResumeResponse,
    RunStatus,
)
from acp_sdk.models.errors import ACPError
from acp_sdk.server.agent import Agent
from acp_sdk.server.bundle import RunBundle
from acp_sdk.server.errors import (
    RequestValidationError,
    StarletteHTTPException,
    acp_error_handler,
    catch_all_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from acp_sdk.server.utils import stream_sse


class Headers(str, Enum):
    RUN_ID = "Run-ID"


def create_app(*agents: Agent) -> FastAPI:
    executor: ThreadPoolExecutor

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        nonlocal executor
        with ThreadPoolExecutor(max_workers=5) as exec:
            executor = exec
            yield

    app = FastAPI(lifespan=lifespan)

    FastAPIInstrumentor.instrument_app(app)

    agents: dict[AgentName, Agent] = {agent.name: agent for agent in agents}
    runs: dict[RunId, RunBundle] = {}

    app.exception_handler(ACPError)(acp_error_handler)
    app.exception_handler(StarletteHTTPException)(http_exception_handler)
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(Exception)(catch_all_exception_handler)

    def find_run_bundle(run_id: RunId) -> RunBundle:
        bundle = runs.get(run_id)
        if not bundle:
            raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
        return bundle

    def find_agent(agent_name: AgentName) -> Agent:
        agent = agents.get(agent_name, None)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        return agent

    @app.get("/agents")
    async def list_agents() -> AgentsListResponse:
        return AgentsListResponse(
            agents=[
                AgentModel(name=agent.name, description=agent.description, metadata=agent.metadata)
                for agent in agents.values()
            ]
        )

    @app.get("/agents/{name}")
    async def read_agent(name: AgentName) -> AgentReadResponse:
        agent = find_agent(name)
        return AgentModel(name=agent.name, description=agent.description, metadata=agent.metadata)

    @app.post("/runs")
    async def create_run(request: RunCreateRequest) -> RunCreateResponse:
        agent = find_agent(request.agent_name)
        bundle = RunBundle(
            agent=agent,
            run=Run(
                agent_name=agent.name,
                session_id=request.session_id,
            ),
        )

        nonlocal executor
        bundle.task = asyncio.create_task(bundle.execute(request.input, executor=executor))
        runs[bundle.run.run_id] = bundle

        headers = {Headers.RUN_ID: str(bundle.run.run_id)}

        match request.mode:
            case RunMode.STREAM:
                return StreamingResponse(
                    stream_sse(bundle),
                    headers=headers,
                    media_type="text/event-stream",
                )
            case RunMode.SYNC:
                await bundle.join()
                return JSONResponse(
                    headers=headers,
                    content=jsonable_encoder(bundle.run),
                )
            case RunMode.ASYNC:
                return JSONResponse(
                    status_code=status.HTTP_202_ACCEPTED,
                    headers=headers,
                    content=jsonable_encoder(bundle.run),
                )
            case _:
                raise NotImplementedError()

    @app.get("/runs/{run_id}")
    async def read_run(run_id: RunId) -> RunReadResponse:
        bundle = find_run_bundle(run_id)
        return bundle.run

    @app.post("/runs/{run_id}")
    async def resume_run(run_id: RunId, request: RunResumeRequest) -> RunResumeResponse:
        bundle = find_run_bundle(run_id)
        bundle.stream_queue = asyncio.Queue()  # TODO improve
        await bundle.await_queue.put(request.await_)
        match request.mode:
            case RunMode.STREAM:
                return StreamingResponse(
                    stream_sse(bundle),
                    media_type="text/event-stream",
                )
            case RunMode.SYNC:
                await bundle.join()
                return bundle.run
            case RunMode.ASYNC:
                return JSONResponse(
                    status_code=status.HTTP_202_ACCEPTED,
                    content=jsonable_encoder(bundle.run),
                )
            case _:
                raise NotImplementedError()

    @app.post("/runs/{run_id}/cancel")
    async def cancel_run(run_id: RunId) -> RunCancelResponse:
        bundle = find_run_bundle(run_id)
        if bundle.run.status.is_terminal:
            raise HTTPException(
                status_code=403,
                detail=f"Run with terminal status {bundle.run.status} can't be cancelled",
            )
        bundle.task.cancel()
        bundle.run.status = RunStatus.CANCELLING
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=jsonable_encoder(bundle.run))

    return app
