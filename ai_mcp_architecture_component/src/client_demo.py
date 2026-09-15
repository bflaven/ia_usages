"""Proof that a second, independent client reaches the same data with
ZERO new integration code — the actual acceptance criterion this whole
POC exists to satisfy (see docs/02_user_story.md, third scenario, and
docs/03_kpis.md, "Deployment speed").

This script is a plain MCP client. It does not import style_guide.py or
mcp_server.py directly, does not know how the data is stored, and does not
share any code with legacy_api.py. It only knows the standard MCP contract
(list tools, call a tool by name with arguments) — the same contract Claude
Desktop or Claude Code would use.

Run:
    python -m src.client_demo
"""

from __future__ import annotations

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["-m", "src.mcp_server"],
)


async def main() -> None:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools discovered with zero integration code:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()

            print("Calling lookup_term('Sud-Liban')...")
            result = await session.call_tool(
                "lookup_term", {"term": "Sud-Liban", "language_pair": "fr-en"}
            )
            _print_tool_result(result)

            print("Calling lookup_term('a term that does not exist')...")
            result = await session.call_tool(
                "lookup_term", {"term": "a term that does not exist"}
            )
            _print_tool_result(result)

            print("Calling check_style_rule on a draft sentence...")
            result = await session.call_tool(
                "check_style_rule",
                {
                    "text": (
                        "Our team at France Médias Monde covered the Sud-Liban "
                        "story using generative AI for the first draft."
                    )
                },
            )
            _print_tool_result(result)


def _print_tool_result(result) -> None:
    for block in result.content:
        text = getattr(block, "text", None)
        if text is not None:
            try:
                print(json.dumps(json.loads(text), ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print(text)
    print()


if __name__ == "__main__":
    asyncio.run(main())
