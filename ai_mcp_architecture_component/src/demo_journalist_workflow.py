"""A concrete, end-to-end journalist scenario: a rough draft with
intentional Russian-transliteration place-name errors, corrected live
through the MCP server's `check_style_rule` tool.

The draft text below is original, written for this demo — it is inspired
by, not copied from, France24's 2026-09-14 report on Zelensky's
de-escalation offer (see docs/07_journalist_demo.md for the source link
and what was and wasn't taken from it: no Ukrainian city was actually
named in that article in connection with strikes, so every place name
below is an illustrative addition, not a misquote).

This is the same MCP client pattern as client_demo.py (real stdio
handshake, zero shared code with mcp_server.py's internals) — the point
here is showing what an editor actually *does* with the tool's output,
not just that the call succeeds.

Run:
    python -m src.demo_journalist_workflow
"""

from __future__ import annotations

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(command="python", args=["-m", "src.mcp_server"])

DRAFT = (
    "President Volodymyr Zelensky said Ukraine is ready to halt strikes on "
    "Russian energy infrastructure if Moscow does the same, calling it a "
    "possible de-escalatory step. He added that Russia has so far shown no "
    "genuine will to end the war. Away from the frontline diplomacy, wire "
    "desks noted the toll on Ukraine's rail network: recent weeks have "
    "seen drone strikes near border crossings, with disruption felt as "
    "far as Kiev, Kharkov and Odessa. Editors compiling the daily brief "
    "also flagged fresh reporting out of Dnepropetrovsk and Lvov, where "
    "local officials described damage to power substations."
)


async def main() -> None:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("=" * 70)
            print("DRAFT (as filed, before house-style check)")
            print("=" * 70)
            print(DRAFT)
            print()

            result = await session.call_tool("check_style_rule", {"text": DRAFT})
            payload = json.loads(result.content[0].text)
            hits = payload["hits"]

            print("=" * 70)
            print(f"MCP tool call: check_style_rule — {len(hits)} house-style hit(s)")
            print("=" * 70)
            corrected = DRAFT
            for hit in hits:
                print(f"  '{hit['term']}' -> '{hit['approved']}'")
                print(f"    note: {hit['note']}")
                corrected = corrected.replace(hit["term"], hit["approved"])
            print()

            print("=" * 70)
            print("CORRECTED (ready to file)")
            print("=" * 70)
            print(corrected)
            print()

            print("=" * 70)
            print("What just happened")
            print("=" * 70)
            print(
                "The editor didn't retype anything by hand and didn't need to "
                "know the house style rules from memory — the same "
                "check_style_rule tool call above works from Claude Desktop, "
                "Claude Code, or any other MCP client, with zero code written "
                "for that specific client. That's the whole argument, not a "
                "slide about it."
            )


if __name__ == "__main__":
    asyncio.run(main())
