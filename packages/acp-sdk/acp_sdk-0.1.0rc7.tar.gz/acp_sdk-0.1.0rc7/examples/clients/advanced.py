import asyncio

import httpx
from acp_sdk.client.client import Client
from acp_sdk.models import Message, TextMessagePart


async def example() -> None:
    async with Client(
        client=httpx.AsyncClient(
            base_url="http://localhost:8000",
            auth=httpx.BasicAuth(username="username", password="password"),
            # Additional client configuration
        )
    ) as client:
        run = await client.run_sync(agent="echo", input=Message(TextMessagePart(content="Howdy!")))
        print(run.output)


if __name__ == "__main__":
    asyncio.run(example())
