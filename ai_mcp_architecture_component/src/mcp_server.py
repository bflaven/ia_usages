"""The 'after' — one MCP server, any MCP-compatible client connects for free.

Exposes the exact same underlying data as legacy_api.py
(data/newsroom_style_guide.json, via style_guide.py) — but through the
Model Context Protocol instead of a bespoke REST shape. Any MCP client
(Claude Desktop, Claude Code, a future in-house agent) gets `lookup_term`
and `check_style_rule` as native tool calls, and the guide itself as a
readable resource, with zero client-specific integration code.

Targets `mcp` SDK v2.x: `MCPServer` (from mcp.server.mcpserver), not the
older v1 `FastMCP` (from mcp.server.fastmcp) — see CLAUDE.md, "MCP SDK
version note".

Run standalone over stdio (default — for Claude Desktop / Claude Code config):
    python -m src.mcp_server

Run standalone over HTTP instead (its own process, its own port — this is
the realistic deployment shape: the MCP server is a service in its own
right, not bolted onto an unrelated REST API's process/lifespan):
    python -m src.mcp_server --http

See README.md for why this runs as a sibling service to legacy_api.py
(main.py) rather than mounted into the same FastAPI app.
"""

from __future__ import annotations

import json
import sys

from mcp.server.mcpserver import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from . import style_guide

mcp = MCPServer(
    name="newsroom-style-guide",
    title="Newsroom Style & Terminology Assistant",
    description=(
        "Look up house-style terminology and check text against the "
        "newsroom style guide — the same data source used across every "
        "AI client, with no per-client integration code required."
    ),
    version="0.1.0",
)


@mcp.tool()
def lookup_term(term: str, language_pair: str | None = None) -> dict:
    """Look up a term in the newsroom house style guide.

    Args:
        term: The term or phrase to look up (e.g. "Sud-Liban").
        language_pair: Optional filter, e.g. "fr-en". If omitted, the first
            match across all language pairs is returned.

    Returns a structured result. If the term isn't found, `found` is False
    and up to three closest known terms are suggested instead of guessing.
    """
    return style_guide.lookup_term(term, language_pair)


@mcp.tool()
def check_style_rule(text: str) -> dict:
    """Scan a piece of text for any terms already covered by the style guide.

    Args:
        text: Free text (e.g. a draft paragraph) to check.

    Returns every style-guide entry whose term appears in the text, with
    the approved rendering and usage note for each hit.
    """
    return style_guide.check_style_rule(text)


@mcp.resource("styleguide://newsroom/full")
def full_style_guide() -> str:
    """The complete newsroom style guide, as a single readable resource."""
    entries = style_guide.load_entries()
    payload = {
        "updated": style_guide.guide_last_updated(),
        "entries": [entry.__dict__ for entry in entries],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


# --http mode only, plain HTTP routes bolted onto the MCP server's own
# Starlette app (via the SDK's own `custom_route`, not a mounted sub-app —
# no lifespan-propagation risk here, see CLAUDE.md). This server has no
# Swagger UI: there is nothing to browse-and-click, it only speaks
# JSON-RPC over POST /mcp. Visiting "/" in a browser is expected — give a
# real answer instead of a bare 404.
@mcp.custom_route("/", methods=["GET"])
async def root(request: Request) -> Response:
    return JSONResponse(
        {
            "service": "newsroom-style-guide (MCP server)",
            "note": (
                "This is an MCP server, not a browsable REST API — there "
                "is no Swagger UI here. It only understands JSON-RPC over "
                "POST /mcp (streamable-http transport). See "
                "docs/05_modop.md STEP 6 for a copy-pasteable curl check, "
                "or connect an MCP client (Claude Desktop/Code) instead."
            ),
            "mcp_endpoint": "/mcp",
            "health_check": "/healthz",
        }
    )


@mcp.custom_route("/healthz", methods=["GET"])
async def healthz(request: Request) -> Response:
    return JSONResponse(
        {"status": "ok", "style_guide_last_updated": style_guide.guide_last_updated()}
    )


@mcp.custom_route("/favicon.ico", methods=["GET"])
async def favicon(request: Request) -> Response:
    return Response(status_code=204)


if __name__ == "__main__":
    try:
        if "--http" in sys.argv:
            # Own process, own port (default 8001) — the legacy REST demo
            # (main.py) runs separately on 8000. Two sibling services, same
            # underlying data (style_guide.py), by design — see README.md.
            mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)
        else:
            mcp.run()  # stdio — for Claude Desktop / Claude Code config
    except KeyboardInterrupt:
        # Ctrl+C otherwise surfaces as a raw asyncio/anyio traceback
        # (CancelledError -> KeyboardInterrupt) up through anyio.run() —
        # harmless, but reads as a crash to a non-engineer. Swallow it and
        # exit quietly instead.
        print("\nnewsroom-style-guide MCP server stopped.")
