import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
        env=None,
    )

    async with AsyncExitStack() as stack:
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        read_stream, write_stream = stdio_transport

        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()

        tools_response = await session.list_tools()

        print("Connected successfully.")
        print("Available tools:")

        for tool in tools_response.tools:
            print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())