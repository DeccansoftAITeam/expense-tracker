"""A small MCP client: launches server.py over stdio and calls it like Claude would.

Run with the backend running:  uv run stdio_client.py
"""

import json
import sys

import anyio
from mcp import Client, StdioServerParameters


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with Client(params) as client:
        tools = await client.list_tools()
        print("tools:", ", ".join(tool.name for tool in tools.tools))

        added = await client.call_tool("add_expense", {"description": "Client test", "amount_paise": 4999, "category": "food"})
        print("add_expense:", added.content[0].text)

        month = json.loads(added.content[0].text)["spent_on"][:7]
        summary = await client.read_resource(f"expenses://summary/{month}")
        print(summary.contents[0].text)

        bad = await client.call_tool("add_expense", {"description": "Too big", "amount_paise": 10_000_001})
        print("too big is_error =", bad.is_error, "-", bad.content[0].text)


if __name__ == "__main__":
    anyio.run(main)
