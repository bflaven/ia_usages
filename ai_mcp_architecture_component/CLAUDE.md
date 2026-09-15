# CLAUDE.md — MCP Architecture Component (POC)

Project context for AI-assisted work. Read before touching any file here.
**All content in this project — code, docs, comments, commit messages — is
in English.** This POC is meant to be published on GitHub and folded into a
broader blog article (dataviz + AI + public administration, see the sibling
`_ia_data_science/` project) — write accordingly: clear, self-contained,
no throwaway/internal-only phrasing.

---

## What this POC is, in one sentence

A real Model Context Protocol (MCP) server, sitting next to a FastAPI REST
service exposing the same underlying data, that proves — with working
code, not a slide — why exposing an internal data source as one MCP server
beats writing a custom REST integration for every AI client that needs it.

## Why it exists (do not lose this framing when editing)

This is not a tech demo for its own sake. It is a deliberate demonstration
of a full product methodology applied to a technical choice:

```
Discovery (stakeholder interview) → Use case capture (qualify → measure →
adjudicate → adopt) → User Story → KPIs (adoption, operational efficiency,
quality/reliability, deployment speed) → Build-vs-buy recommendation →
"we choose MCP" → implementation
```

Method: **Design Thinking → Lean → Scrum**. See `docs/` for each step. The
code exists *because* the recommendation in `docs/04_recommendation.md`
concluded it should — never restructure the repo to make it look like the
code came first. The whole point is: the technical choice is downstream of
product reasoning, not a solution looking for a problem.

---

## The use case (do not silently change it)

**"Newsroom Style & Terminology Assistant"** — a multilingual newsroom
editor needs any AI assistant they use (Claude Desktop today, other MCP
clients tomorrow) to check a term against the house style guide instantly,
instead of searching a shared spreadsheet or asking a colleague — and
without someone having to hand-build a new integration every time a new AI
tool shows up.

Full detail: `docs/01_discovery.md` (persona is an explicitly-labeled
composite, not a real named individual) and `docs/02_user_story.md`.

---

## Architecture

```
src/
├── data/
│   └── newsroom_style_guide.json   ← mock terminology/style dataset (source of truth)
├── style_guide.py                  ← shared data-access module (both services read from this, never diverge)
├── legacy_api.py                   ← "before": one bespoke REST endpoint — the N×M problem, made visible
├── main.py                         ← FastAPI app serving legacy_api.py alone, port 8000
├── mcp_server.py                   ← "after": the MCP server (tools + resource) — the N+M fix, port 8001 or stdio
├── client_demo.py                  ← minimal MCP client, calls the server over stdio, proves it end-to-end
└── demo_journalist_workflow.py     ← before/after: flawed draft corrected live via check_style_rule
tests/
└── test_mcp_server.py
docs/
├── 01_discovery.md
├── 02_user_story.md
├── 03_kpis.md
├── 04_recommendation.md
├── 05_modop.md
├── 06_add_your_own_example.md      ← no-code HOWTO: edit the JSON, simulate your own use case
└── 07_journalist_demo.md           ← worked example behind demo_journalist_workflow.py, with sourcing notes
```

### Why both `legacy_api.py` and `mcp_server.py` exist, as sibling services

This is the whole argument of the article, made executable: `legacy_api.py`
(served by `main.py`, FastAPI, port 8000) is deliberately a normal,
well-written REST endpoint — nothing wrong with it in isolation. The
problem only appears once you imagine a second, third, fourth AI client
needing the same data: each one needs its own client-side integration code
against this bespoke REST shape. `mcp_server.py` exposes the exact same
underlying data (via the shared `style_guide.py` module — never a second
copy of the logic) through the MCP protocol instead — any MCP-compatible
client (Claude Desktop, Claude Code, a future in-house agent) can call it
with zero new integration code. **Do not delete `legacy_api.py` to "clean
up" — it is the control group, not dead code.**

**Why two separate processes, not one app with MCP mounted inside
FastAPI**: it was tried. `MCPServer.streamable_http_app()` returns a
Starlette app whose session manager is wired into *that app's own*
lifespan (`lifespan=lambda app: session_manager.run()`). Mounting it into
a parent FastAPI app via `.mount()` does not reliably propagate that
lifespan — the ASGI server only sends lifespan events to the root app, so
the MCP session manager's background task can end up never started. Rather
than paper over that with private-attribute access, this POC ships two
small, independently correct, independently runnable services instead —
also a more realistic deployment shape (an MCP server is a service, not a
sub-route bolted onto an unrelated API). Both are proven working end to
end (`python -m src.client_demo` for MCP over stdio, live `curl` against
`--http` mode, and against `uvicorn src.main:app` for the REST side) —
see README.md changelog for the verification record.

### `src/main.py` is meant to be opened in a browser, not just curled

This project doubles as interview/article material for a non-engineer
audience — the FastAPI app (`main.py`) is deliberately configured so a
first-time visitor lands somewhere useful:

- `title` / `description` / `version` / `openapi_tags` are set on the
  `FastAPI(...)` constructor so `/docs` (Swagger UI) reads like a labeled
  product, not an unnamed script.
- `GET /` redirects (307) to `/docs` — no bare 404 on the root URL.
- `GET /favicon.ico` returns `204` instead of logging a 404 on every visit.
- `GET /health` is tagged `health`, `legacy_api.router` is tagged
  `legacy-rest` — both group and get a description in Swagger UI.

Do not remove this in the name of minimalism — it is intentional UX, not
scope creep.

### `mcp_server.py` `--http` mode also answers `/` — but with JSON, not a page

Unlike `main.py`, this server has no Swagger UI to redirect to — it only
speaks JSON-RPC over `POST /mcp`. A visitor hitting `/` in a browser is a
sure thing to happen (it happened during manual testing), so `/`,
`/healthz`, and `/favicon.ico` are registered via the SDK's own
`@mcp.custom_route(...)` decorator (`mcp.server.mcpserver.MCPServer`
exposes this; it appends a Starlette `Route` to the same app returned by
`streamable_http_app()` — **not** a mounted sub-app, so none of the
lifespan-propagation risk described above applies). `/` and `/healthz`
return a small `JSONResponse` explaining what this service is and where
`/mcp` is; `/favicon.ico` returns an empty `204`. Keep these three routes
if this file is edited — they exist because the raw 404 was genuinely
confusing to a non-engineer reader, not as a nicety.

### `mcp_server.py` `--http` mode: `Ctrl+C` must exit clean, not crash

`mcp.run(transport="streamable-http", ...)` drives the server through
`anyio.run(...)`. A plain `Ctrl+C` cancels that task, and the cancellation
surfaces as `asyncio.exceptions.CancelledError` immediately followed by
`KeyboardInterrupt`, printed as a full traceback if left uncaught — reads
as a crash to a non-engineer, even though the shutdown itself is fine. The
`if __name__ == "__main__":` block wraps both `mcp.run(...)` calls in
`try/except KeyboardInterrupt`, printing one clean line instead. Verified
live via `kill -INT` on the running process: exit code `0`, no traceback,
uvicorn's own "Shutting down" / "Application shutdown complete" log lines
still appear as normal.

### MCP SDK version note

This project targets **`mcp` v2.x** (`MCPServer`, from
`mcp.server.mcpserver import MCPServer`), not the older v1 `FastMCP` class
under `mcp.server.fastmcp` — that import path raises
`ModuleNotFoundError` on v2 by design (see the SDK's own migration message).
If you see `FastMCP` in older tutorials online, translate it to `MCPServer`
— same decorator ergonomics (`@mcp.tool()`, `@mcp.resource()`), renamed
class.

To check the installed version, do **not** use `mcp.__version__` — the
package does not define it and raises `AttributeError`. Use:
`python -c "import importlib.metadata as m; print(m.version('mcp'))"`.

---

## Environment

- Conda env: **`mcp_architecture_component`** (Python 3.13, created
  2026-09-15 — none of the pre-existing envs in this machine (`ia_achats`,
  `midterms`, `editorial_treatment`, `tags_treatment`) were a semantic fit
  for a standalone public POC, so a dedicated one was created rather than
  reused).
- Install: `pip install -r requirements.txt`
- Run the legacy REST demo: `uvicorn src.main:app --reload` (port 8000)
- Run the MCP server over stdio (for Claude Desktop/Code config):
  `python -m src.mcp_server`
- Run the MCP server over HTTP instead (its own port, 8001):
  `python -m src.mcp_server --http`
- Prove it end-to-end without any external AI client (spawns the stdio
  server itself, no separate terminal needed):
  `python -m src.client_demo`
- Run the tests: `python -m pytest tests/ -v`

All commands above use `-m` (module) invocation, not direct file paths —
`src/` is a package and the relative imports inside it (`from . import
style_guide`) require running it that way.

---

## What NOT to do

- Do not write anything in French in this project — see language rule above.
- Do not remove `legacy_api.py` — it is intentional, it is the argument.
- Do not fabricate a real named stakeholder in `docs/01_discovery.md` — the
  persona must stay an explicitly-labeled composite.
- Do not silently change the KPI framework in `docs/03_kpis.md` — it must
  stay the four blocks (adoption/usage, operational efficiency,
  quality/reliability, deployment speed) as used elsewhere in this user's
  job-search materials, for consistency across everything he publishes.
- Do not `git init` / commit / push from here — the user publishes this
  himself.
- Do not add a real database (SQLite, Postgres, ORM, etc). The single
  flat file `src/data/newsroom_style_guide.json`, read through
  `style_guide.py`, is the entire data layer, on purpose — see
  `docs/06_add_your_own_example.md`, "No database, on purpose." The POC's
  whole point is the integration pattern (REST vs MCP), not data
  engineering; adding one would be exactly the "technic for technic's
  sake" this project exists to avoid.

---

## Changelog (architecture decisions)

| Date | Decision | Rationale |
|---|---|---|
| 2026-09-15 | New conda env `mcp_architecture_component`, Python 3.13 | No existing env was a clean semantic fit; this POC is meant to be public and self-contained |
| 2026-09-15 | Targeted `mcp` v2.x (`MCPServer`), not v1 `FastMCP` | v1 raised `ModuleNotFoundError` on install; v2 is current or future readers hitting this repo in 2026+ should see current API |
| 2026-09-15 | Kept `legacy_api.py` alongside `mcp_server.py` deliberately | The N×M vs N+M argument needs a visible "before", not just an "after" |
| 2026-09-15 | `mcp_server.py` runs as its own sibling service (stdio or `--http` on port 8001), not mounted inside `main.py`'s FastAPI app | Mounting `MCPServer.streamable_http_app()` into a parent app doesn't reliably get its lifespan run (ASGI servers only send lifespan events to the root app) — verified by inspecting the SDK source before deciding, not guessed. Two small correct services beat one app that only works by accident. |
| 2026-09-15 | Extracted `style_guide.py` as a shared data-access module | Guarantees `legacy_api.py` and `mcp_server.py` can never return different answers for the same data — enforced by construction, not by discipline (see docs/03_kpis.md, "Quality/reliability") |
| 2026-09-15 | Full working smoke test before calling it done: pytest (6/6 pass), live `uvicorn` + `curl` against the REST app, live `client_demo.py` against the MCP server over stdio, live MCP handshake over `--http` | This POC is meant to be published and to carry real credibility — it had to actually run, not just look plausible |
| 2026-09-15 | Added `docs/05_modop.md`, step-by-step launch/verify checklist | Repeatable operational method for anyone (including the author, months later) to stand this up and confirm it still works |
| 2026-09-15 | `docs/05_modop.md` version-check command fixed: `importlib.metadata.version("mcp")` instead of `mcp.__version__` | `mcp` package raises `AttributeError` on `__version__` — caught via a real run, not assumed |
| 2026-09-15 | `src/main.py` given a title/description/tags_metadata, `/` redirect to `/docs`, `/favicon.ico` returns 204 | POC audience includes non-engineers; a raw uvicorn process with a bare-404 root and noisy favicon logs reads as unfinished — verified live: `/`→307→`/docs`, `/favicon.ico`→204, tests still 6/6 |
| 2026-09-15 | Added `docs/05_modop.md` STEP 4bis, a click-by-click Swagger UI walkthrough with no terminal commands | Author is a communicator/educator, not an engineer, and wants a MODOP any reader of the future article can follow without knowing curl — verified live via browser automation against a running server, exact button labels and response body captured, not guessed |
| 2026-09-15 | `mcp_server.py` `--http` mode: added `/`, `/healthz`, `/favicon.ico` via `@mcp.custom_route(...)` | User hit real `404 Not Found` on `GET /` and `/favicon.ico` when instinctively opening the MCP server's URL in a browser — same instinct STEP 4bis is built around, just on the wrong server; fixed instead of just documenting the 404 as expected, verified live: `/`→JSON, `/healthz`→ok, `/favicon.ico`→204, `POST /mcp`→200, tests still 6/6 |
| 2026-09-15 | `mcp_server.py` `--http`/stdio: `Ctrl+C` wrapped in `try/except KeyboardInterrupt` | User hit a full red `Traceback`/`KeyboardInterrupt` on stop — technically harmless but reads as a crash to a non-engineer; verified live via `kill -INT`: exit code 0, no traceback |
| 2026-09-15 | Added plain-language persona/User Story primer (`docs/02_user_story.md`) and `docs/06_add_your_own_example.md` | User (a communicator/educator, not an engineer) found "persona" opaque and wanted a concrete way to add his own data without code; verified the doc's one-line lookup command actually runs |
| 2026-09-15 | Added 9 `ru-en` Ukrainian/Russian place-name entries to `src/data/newsroom_style_guide.json` | User wanted a concrete, non-abstract extension of the use case (house style: Ukrainian transliteration, not Russian) to test end-to-end in Claude Desktop, not "airy-fairy" theory — verified live, 15/15 entries load, tests still 6/6 |
| 2026-09-15 | Fixed Claude Desktop wiring instructions (STEP 7, `docs/05_modop.md`): dropped `"cwd"` (unsupported by Claude Desktop's schema, silently stripped on the app's own config rewrite — caught live when the app rewrote the user's real config file and the key vanished), use `"env": {"PYTHONPATH": ...}` instead | A `cwd`-based config would have failed with `ModuleNotFoundError: No module named 'src'` the moment the app next rewrote its config — caught before it bit the user, not after |
| 2026-09-15 | Added a "Quick Start" 3-step block at the top of `docs/05_modop.md` | User reported a "Server disconnected" error and asked for one fixed, repeatable sequence instead of re-deriving the procedure each time; diagnosed the report as stale (app not running, config verified correct via a re-simulated exact subprocess launch) and packaged the loop (client_demo sanity check → quit/reopen Desktop → live Ukraine-example test) as a standing procedure |
| 2026-09-15 | Added `src/demo_journalist_workflow.py` + `docs/07_journalist_demo.md` | User wanted a concrete journalist scenario, not another isolated lookup: a flawed draft with intentional Russian-place-name errors, corrected live via the real `check_style_rule` MCP tool call. Draft text is original (inspired by, not copied from, a cited France24 article — that article names no Ukrainian cities in connection with strikes, so the errors are a deliberate addition, documented as such to keep sourcing honest). Verified live: 5/5 errors caught and corrected, tests still 6/6 |
| 2026-09-15 | Removed `reponses_volet_mcp_denia.md` (moved to the author's private job-search records, outside this repo) | Private, French-language job-application planning note — not referenced by any doc, content already genericized into `docs/01`–`04`, and this repo is meant to be pushed to GitHub publicly; violated both the English-only rule and basic privacy hygiene |
