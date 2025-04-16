import asyncio
import logging
from collections.abc import AsyncGenerator
from concurrent.futures import ThreadPoolExecutor

from opentelemetry import trace
from pydantic import ValidationError

from acp_sdk.models import (
    AnyModel,
    Await,
    AwaitEvent,
    AwaitResume,
    CancelledEvent,
    CompletedEvent,
    CreatedEvent,
    Error,
    FailedEvent,
    GenericEvent,
    InProgressEvent,
    Message,
    MessageEvent,
    Run,
    RunEvent,
    RunStatus,
)
from acp_sdk.models.errors import ErrorCode
from acp_sdk.server.agent import Agent
from acp_sdk.server.logging import logger


class RunBundle:
    def __init__(self, *, agent: Agent, run: Run, task: asyncio.Task | None = None) -> None:
        self.agent = agent
        self.run = run
        self.task = task

        self.stream_queue: asyncio.Queue[RunEvent] = asyncio.Queue()
        self.composed_message = Message()

        self.await_queue: asyncio.Queue[AwaitResume] = asyncio.Queue(maxsize=1)
        self.await_or_terminate_event = asyncio.Event()

    async def stream(self) -> AsyncGenerator[RunEvent]:
        while True:
            event = await self.stream_queue.get()
            if event is None:
                break
            yield event
            self.stream_queue.task_done()

    async def emit(self, event: RunEvent) -> None:
        await self.stream_queue.put(event)

    async def await_(self) -> AwaitResume:
        await self.stream_queue.put(None)
        self.await_queue.empty()
        self.await_or_terminate_event.set()
        self.await_or_terminate_event.clear()
        resume = await self.await_queue.get()
        self.await_queue.task_done()
        return resume

    async def resume(self, resume: AwaitResume) -> None:
        self.stream_queue = asyncio.Queue()
        await self.await_queue.put(resume)

    async def join(self) -> None:
        await self.await_or_terminate_event.wait()

    async def execute(self, input: Message, *, executor: ThreadPoolExecutor) -> None:
        with trace.get_tracer(__name__).start_as_current_span("execute"):
            run_logger = logging.LoggerAdapter(logger, {"run_id": str(self.run.run_id)})

            await self.emit(CreatedEvent(run=self.run))
            try:
                self.run.session_id = await self.agent.session(self.run.session_id)
                run_logger.info("Session loaded")

                generator = self.agent.execute(input=input, session_id=self.run.session_id, executor=executor)
                run_logger.info("Run started")

                self.run.status = RunStatus.IN_PROGRESS
                await self.emit(InProgressEvent(run=self.run))

                await_resume = None
                while True:
                    next = await generator.asend(await_resume)
                    if isinstance(next, Message):
                        self.composed_message += next
                        await self.emit(MessageEvent(message=next))
                    elif isinstance(next, Await):
                        self.run.await_ = next
                        self.run.status = RunStatus.AWAITING
                        await self.emit(
                            AwaitEvent.model_validate(
                                {
                                    "run_id": self.run.run_id,
                                    "type": "await",
                                    "await": next,
                                }
                            )
                        )
                        run_logger.info("Run awaited")
                        await_resume = await self.await_()
                        self.run.status = RunStatus.IN_PROGRESS
                        await self.emit(InProgressEvent(run=self.run))
                        run_logger.info("Run resumed")
                    else:
                        try:
                            generic = AnyModel.model_validate(next)
                            await self.emit(GenericEvent(generic=generic))
                        except ValidationError:
                            raise TypeError("Invalid yield")
            except StopAsyncIteration:
                self.run.output = self.composed_message
                self.run.status = RunStatus.COMPLETED
                await self.emit(CompletedEvent(run=self.run))
                run_logger.info("Run completed")
            except asyncio.CancelledError:
                self.run.status = RunStatus.CANCELLED
                await self.emit(CancelledEvent(run=self.run))
                run_logger.info("Run cancelled")
            except Exception as e:
                self.run.error = Error(code=ErrorCode.SERVER_ERROR, message=str(e))
                self.run.status = RunStatus.FAILED
                await self.emit(FailedEvent(run=self.run))
                run_logger.exception("Run failed")
            finally:
                self.await_or_terminate_event.set()
                await self.stream_queue.put(None)
