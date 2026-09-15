"""FastAPI entry point — the 'before' half of this POC.

Serves the legacy REST endpoint (legacy_api.py) on its own. The MCP server
(mcp_server.py) is a sibling service, not mounted into this process — see
README.md, "Why two processes, not one mega-app" for the reasoning (short
version: mounting an MCP server's own ASGI lifespan into an unrelated
parent app is a known Starlette footgun; two small, correct, independently
runnable services beat one fragile combined one).

Run:
    uvicorn src.main:app --reload
"""

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

from . import legacy_api, style_guide

title = "Newsroom Style & Terminology Assistant — legacy REST demo"
description = (
    "The 'before' half of the MCP architecture POC: a normal, bespoke "
    "REST endpoint over the newsroom style guide. Built to be visited in "
    "a browser, not just called from a terminal — open `/` and it takes "
    "you straight to the interactive Swagger UI. See "
    "docs/04_recommendation.md, option B, for why this alone doesn't scale "
    "past one client."
)
version = "0.1.0"

tags_metadata = [
    {
        "name": "doc",
        "description": "Root redirect to the Swagger UI — start here.",
    },
    {
        "name": "health",
        "description": "Liveness check: is the service up, and how fresh is the underlying style guide.",
    },
    {
        "name": "legacy-rest",
        "description": "The 'before': one bespoke REST endpoint, one client at a time.",
    },
]

app = FastAPI(
    title=title,
    description=description,
    version=version,
    openapi_tags=tags_metadata,
)

app.include_router(legacy_api.router)


@app.get("/", tags=["doc"], include_in_schema=False)
def root() -> RedirectResponse:
    """Land on the interactive docs instead of a bare 404."""
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """No icon to serve — 204 instead of a noisy 404 in the logs."""
    return Response(status_code=204)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {
        "status": "ok",
        "style_guide_last_updated": style_guide.guide_last_updated(),
    }
