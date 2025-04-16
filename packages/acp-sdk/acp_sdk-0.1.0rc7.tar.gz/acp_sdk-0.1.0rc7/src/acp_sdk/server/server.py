import asyncio
import inspect
import os
from collections.abc import AsyncGenerator, Awaitable, Coroutine, Generator
from typing import Any, Callable

import uvicorn
import uvicorn.config

from acp_sdk.models import Message
from acp_sdk.server.agent import Agent
from acp_sdk.server.app import create_app
from acp_sdk.server.context import Context
from acp_sdk.server.logging import configure_logger as configure_logger_func
from acp_sdk.server.telemetry import configure_telemetry as configure_telemetry_func
from acp_sdk.server.types import RunYield, RunYieldResume


class Server:
    def __init__(self) -> None:
        self._agents: list[Agent] = []
        self._server: uvicorn.Server | None = None

    def agent(self, name: str | None = None, description: str | None = None) -> Callable:
        """Decorator to register an agent."""

        def decorator(fn: Callable) -> Callable:
            signature = inspect.signature(fn)
            parameters = list(signature.parameters.values())

            if len(parameters) == 0:
                raise TypeError("The agent function must have at least 'input' argument")
            if len(parameters) > 2:
                raise TypeError("The agent function must have only 'input' and 'context' arguments")
            if len(parameters) == 2 and parameters[1].name != "context":
                raise TypeError("The second argument of the agent function must be 'context'")

            has_context_param = len(parameters) == 2

            agent: Agent
            if inspect.isasyncgenfunction(fn):

                class DecoratedAgent(Agent):
                    @property
                    def name(self) -> str:
                        return name or fn.__name__

                    @property
                    def description(self) -> str:
                        return description or fn.__doc__ or ""

                    async def run(self, input: Message, context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
                        try:
                            gen: AsyncGenerator[RunYield, RunYieldResume] = (
                                fn(input, context) if has_context_param else fn(input)
                            )
                            value = None
                            while True:
                                value = yield await gen.asend(value)
                        except StopAsyncIteration:
                            pass

                agent = DecoratedAgent()
            elif inspect.iscoroutinefunction(fn):

                class DecoratedAgent(Agent):
                    @property
                    def name(self) -> str:
                        return name or fn.__name__

                    @property
                    def description(self) -> str:
                        return description or fn.__doc__ or ""

                    async def run(self, input: Message, context: Context) -> Coroutine[RunYield]:
                        return await (fn(input, context) if has_context_param else fn(input))

                agent = DecoratedAgent()
            elif inspect.isgeneratorfunction(fn):

                class DecoratedAgent(Agent):
                    @property
                    def name(self) -> str:
                        return name or fn.__name__

                    @property
                    def description(self) -> str:
                        return description or fn.__doc__ or ""

                    def run(self, input: Message, context: Context) -> Generator[RunYield, RunYieldResume]:
                        yield from (fn(input, context) if has_context_param else fn(input))

                agent = DecoratedAgent()
            else:

                class DecoratedAgent(Agent):
                    @property
                    def name(self) -> str:
                        return name or fn.__name__

                    @property
                    def description(self) -> str:
                        return description or fn.__doc__ or ""

                    def run(self, input: Message, context: Context) -> RunYield:
                        return fn(input, context) if has_context_param else fn(input)

                agent = DecoratedAgent()

            self.register(agent)
            return fn

        return decorator

    def register(self, *agents: Agent) -> None:
        self._agents.extend(agents)

    def run(
        self,
        configure_logger: bool = True,
        configure_telemetry: bool = False,
        host: str = "127.0.0.1",
        port: int = 8000,
        uds: str | None = None,
        fd: int | None = None,
        loop: uvicorn.config.LoopSetupType = "auto",
        http: type[asyncio.Protocol] | uvicorn.config.HTTPProtocolType = "auto",
        ws: type[asyncio.Protocol] | uvicorn.config.WSProtocolType = "auto",
        ws_max_size: int = 16 * 1024 * 1024,
        ws_max_queue: int = 32,
        ws_ping_interval: float | None = 20.0,
        ws_ping_timeout: float | None = 20.0,
        ws_per_message_deflate: bool = True,
        lifespan: uvicorn.config.LifespanType = "auto",
        env_file: str | os.PathLike[str] | None = None,
        log_config: dict[str, Any]
        | str
        | uvicorn.config.RawConfigParser
        | uvicorn.config.IO[Any]
        | None = uvicorn.config.LOGGING_CONFIG,
        log_level: str | int | None = None,
        access_log: bool = True,
        use_colors: bool | None = None,
        interface: uvicorn.config.InterfaceType = "auto",
        reload: bool = False,
        reload_dirs: list[str] | str | None = None,
        reload_delay: float = 0.25,
        reload_includes: list[str] | str | None = None,
        reload_excludes: list[str] | str | None = None,
        workers: int | None = None,
        proxy_headers: bool = True,
        server_header: bool = True,
        date_header: bool = True,
        forwarded_allow_ips: list[str] | str | None = None,
        root_path: str = "",
        limit_concurrency: int | None = None,
        limit_max_requests: int | None = None,
        backlog: int = 2048,
        timeout_keep_alive: int = 5,
        timeout_notify: int = 30,
        timeout_graceful_shutdown: int | None = None,
        callback_notify: Callable[..., Awaitable[None]] | None = None,
        ssl_keyfile: str | os.PathLike[str] | None = None,
        ssl_certfile: str | os.PathLike[str] | None = None,
        ssl_keyfile_password: str | None = None,
        ssl_version: int = uvicorn.config.SSL_PROTOCOL_VERSION,
        ssl_cert_reqs: int = uvicorn.config.ssl.CERT_NONE,
        ssl_ca_certs: str | None = None,
        ssl_ciphers: str = "TLSv1",
        headers: list[tuple[str, str]] | None = None,
        factory: bool = False,
        h11_max_incomplete_event_size: int | None = None,
    ) -> None:
        if self._server:
            raise RuntimeError("The server is already running")

        import uvicorn

        if configure_logger:
            configure_logger_func()
        if configure_telemetry:
            configure_telemetry_func()

        config = uvicorn.Config(
            create_app(*self._agents),
            host,
            port,
            uds,
            fd,
            loop,
            http,
            ws,
            ws_max_size,
            ws_max_queue,
            ws_ping_interval,
            ws_ping_timeout,
            ws_per_message_deflate,
            lifespan,
            env_file,
            log_config,
            log_level,
            access_log,
            use_colors,
            interface,
            reload,
            reload_dirs,
            reload_delay,
            reload_includes,
            reload_excludes,
            workers,
            proxy_headers,
            server_header,
            date_header,
            forwarded_allow_ips,
            root_path,
            limit_concurrency,
            limit_max_requests,
            backlog,
            timeout_keep_alive,
            timeout_notify,
            timeout_graceful_shutdown,
            callback_notify,
            ssl_keyfile,
            ssl_certfile,
            ssl_keyfile_password,
            ssl_version,
            ssl_cert_reqs,
            ssl_ca_certs,
            ssl_ciphers,
            headers,
            factory,
            h11_max_incomplete_event_size,
        )
        self._server = uvicorn.Server(config)
        self._server.run()

    @property
    def should_exit(self) -> bool:
        return self._server.should_exit if self._server else False

    @should_exit.setter
    def should_exit(self, value: bool) -> None:
        self._server.should_exit = value
