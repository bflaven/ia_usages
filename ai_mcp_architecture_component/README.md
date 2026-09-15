# Newsroom Style & Terminology Assistant — an MCP Architecture POC

A small, fully working proof of concept answering one question with code
instead of a slide deck: **why does exposing an internal data source as a
Model Context Protocol (MCP) server beat writing a custom REST integration
for every AI client that needs it?**

This repo does not start from the technology. It starts from a stakeholder
interview, a user story, and a KPI table — the same product method used
throughout this author's job-search materials (Design Thinking → Lean →
Scrum; use case capture as qualify → measure → adjudicate → adopt) — and
only reaches "we choose MCP" as the last step, once the numbers say so.
See `docs/` for the full trail.

---

## The 30-second version

- **Problem**: a multilingual newsroom editor needs any AI assistant to
  check a term against the house style guide. Every time a new AI tool is
  introduced, someone rebuilds a bespoke integration against the same data.
- **Before** (`src/legacy_api.py`, `src/main.py`): a clean, normal FastAPI
  REST endpoint. Works fine for exactly one client.
- **After** (`src/mcp_server.py`): the same underlying data
  (`src/style_guide.py`), exposed as an MCP server instead. Any
  MCP-compatible client — Claude Desktop, Claude Code, a future in-house
  agent — connects with zero new integration code.
- **Proof, not assertion** (`src/client_demo.py`): a second, independent
  client, written without importing a single line from the REST side,
  discovers the tools and calls them successfully. This is what actually
  separates option B from option C in `docs/04_recommendation.md` — not
  a claim, a passing script.

Full methodology trail: `docs/01_discovery.md` → `docs/02_user_story.md` →
`docs/03_kpis.md` → `docs/04_recommendation.md`. To actually stand this up
and verify it end-to-end yourself, follow `docs/05_modop.md`.

---

## Quickstart

```bash
conda create -n mcp_architecture_component python=3.13
conda activate mcp_architecture_component
pip install -r requirements.txt

# Run the tests
python -m pytest tests/ -v

# Terminal 1 — the "before": legacy REST demo
uvicorn src.main:app --reload
# then open http://127.0.0.1:8000/ in a browser — it redirects to the
# interactive Swagger UI, no need to memorize routes or use a terminal
curl "http://127.0.0.1:8000/legacy/lookup-term?term=Sud-Liban&language_pair=fr-en"

# Terminal 2 — the "after": prove a second, independent client works with
# zero integration code (spawns the MCP server itself over stdio)
python -m src.client_demo
```

To use it from Claude Desktop or Claude Code instead of the demo script,
point your MCP client config at (use the absolute path from
`which python` with the env activated — plain `"python"` won't have `mcp`
installed; use `env.PYTHONPATH`, not `cwd`, which Claude Desktop's schema
doesn't actually support and silently drops — see `docs/05_modop.md`
STEP 7.2 for why both traps are silent failures):

```json
{
  "mcpServers": {
    "newsroom-style-guide": {
      "command": "/absolute/path/to/conda/envs/mcp_architecture_component/bin/python",
      "args": ["-m", "src.mcp_server"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/this/repo"
      }
    }
  }
}
```

---

## Why this exists

Two reasons, on purpose, both real:

1. **A concrete answer to "have you worked with MCP?"** — not a
   PowerPoint slide of the protocol diagram, a repo that runs, with tests
   that pass, built on the same method (discovery → user story → KPIs →
   build-vs-buy recommendation) already used in this author's DENIA work
   at France Médias Monde.
2. **Material for a broader article** on how AI + data + automation is
   changing how information gets produced and shared — this POC is the
   concrete, technical half of that argument (see the sibling
   `_ia_data_science/` project for the rest).

---

## Repository layout

```
├── CLAUDE.md              ← AI-assistance context, architecture decisions
├── README.md              ← this file
├── requirements.txt
├── .env.example
├── src/
│   ├── data/newsroom_style_guide.json
│   ├── style_guide.py     ← shared logic, single source of truth
│   ├── legacy_api.py      ← the "before"
│   ├── main.py            ← FastAPI app serving legacy_api.py (port 8000)
│   ├── mcp_server.py      ← the "after" (stdio, or --http on port 8001)
│   ├── client_demo.py     ← proof: an independent client, zero shared code
│   └── demo_journalist_workflow.py  ← before/after: a flawed draft, corrected live via MCP
├── tests/
│   └── test_mcp_server.py
└── docs/
    ├── 01_discovery.md
    ├── 02_user_story.md
    ├── 03_kpis.md
    ├── 04_recommendation.md
    ├── 05_modop.md         ← step-by-step launch + verification checklist
    ├── 06_add_your_own_example.md  ← edit the JSON, simulate your own use case
    └── 07_journalist_demo.md       ← worked example: a flawed draft, corrected live via MCP
```

---

## Changelog

| Date | Change |
|---|---|
| 2026-09-15 | POC created. Dedicated conda env `mcp_architecture_component` (Python 3.13). Full methodology trail written (`docs/01`–`04`): composite-persona stakeholder interview, Gherkin user story with a third acceptance criterion specifically about a second independent client, KPI table (adoption/usage, operational efficiency, quality/reliability, deployment speed), build-vs-buy-vs-protocol recommendation. |
| 2026-09-15 | Implemented `style_guide.py` (shared logic), `legacy_api.py` + `main.py` (FastAPI REST "before"), `mcp_server.py` (MCP "after", `mcp` SDK v2.x / `MCPServer`, not the older v1 `FastMCP`), `client_demo.py` (independent MCP client over stdio). |
| 2026-09-15 | Verified everything actually runs before publishing: `pytest` (6/6 passing), live `uvicorn` + `curl` against the REST endpoint, live `client_demo.py` run against the MCP server over stdio (real tool discovery + real tool calls, output captured), live MCP handshake against `--http` mode on port 8001. |
| 2026-09-15 | Deliberately did **not** mount the MCP server inside the FastAPI app — `MCPServer.streamable_http_app()`'s session-manager lifespan isn't reliably propagated when mounted into a parent app (checked in the SDK source before deciding). Two small, independently correct, independently runnable services instead — see CLAUDE.md for the full reasoning. |
| 2026-09-15 | Added `docs/05_modop.md`, a step-by-step launch/verify checklist (env → deps → tests → REST → MCP stdio → MCP HTTP → Claude Desktop wiring). |
| 2026-09-15 | Fixed the SDK version-check command in `docs/05_modop.md`: `mcp.__version__` does not exist (`AttributeError`) — use `importlib.metadata.version("mcp")` instead. |
| 2026-09-15 | REST demo (`src/main.py`) made browser-friendly: `/` now redirects to Swagger UI (`/docs`) instead of 404, `/favicon.ico` returns a quiet 204, endpoints grouped under OpenAPI tags (`doc`, `health`, `legacy-rest`) with a title/description/version so `/docs` reads like a real product, not a bare script. |
| 2026-09-15 | Added `docs/05_modop.md` STEP 4bis: a zero-terminal, click-by-click Swagger UI walkthrough for a non-engineer reader — what to click, what to type, what result to expect, screen by screen, for `/`, `/health`, and the `/legacy/lookup-term` form (including a deliberate typo example showing the "suggests, doesn't guess" behavior). |
| 2026-09-15 | Fixed `src/mcp_server.py` `--http` mode: `GET /` and `/favicon.ico` used to 404 (this server has no Swagger UI, only `POST /mcp`) — now `/` and new `/healthz` return explanatory JSON via the SDK's own `custom_route`, `/favicon.ico` returns a quiet 204. `docs/05_modop.md` STEP 6 updated to match; verified live (`/`, `/healthz`, `/favicon.ico`, `POST /mcp` all correct, tests still 6/6). |
| 2026-09-15 | Fixed `src/mcp_server.py`: `Ctrl+C` on `--http` mode used to print a full `Traceback`/`KeyboardInterrupt` wall of text — now caught, prints one clean "server stopped" line. Verified live via `kill -INT`: exit code 0, no traceback. |
| 2026-09-15 | Added a plain-language "what is a persona / User Story" primer to `docs/02_user_story.md` (toy Tom/Maureen example before the real Amira one), and `docs/06_add_your_own_example.md` — a no-code HOWTO for editing `src/data/newsroom_style_guide.json` to simulate your own use case, with a verified one-line command to check a new entry without starting any server. |
| 2026-09-15 | Added 9 real `ru-en` entries to `src/data/newsroom_style_guide.json` (Kyiv/Kiev, Kharkiv/Kharkov, Lviv/Lvov, Odesa/Odessa, Mykolaiv/Nikolaev, Zaporizhzhia/Zaporozhye, Chernihiv/Chernigov, Dnipro/Dnepropetrovsk, Bakhmut/Artemivsk) — a concrete worked example (use Ukrainian transliteration, not Russian, per house style) documented in `docs/06_add_your_own_example.md`. Verified: 15 total entries, lookups correct, 6/6 tests still pass. |
| 2026-09-15 | STEP 7 in `docs/05_modop.md` rewritten with the real Claude Desktop config path, a backup step, and two real traps hit and fixed live: bare `"python"` (missing the conda env) and `"cwd"` (Claude Desktop's schema doesn't support it — silently dropped on the app's own config rewrite, use `env.PYTHONPATH` instead). README's config snippet fixed to match. |
| 2026-09-15 | Added STEP 7.6 to `docs/05_modop.md`: how to edit `claude_desktop_config.json` yourself (quit-app-first, backup, comma discipline, jsonlint/local validation) and whether a new capability needs a new `mcpServers` entry or just another tool on the existing server. |
| 2026-09-15 | Added a "Quick Start" block at the top of `docs/05_modop.md` — the 3-step repeatable loop (sanity-check via `client_demo.py` → quit/reopen Claude Desktop → test live with the Ukraine example), so it's a fixed procedure instead of re-derived each session. Diagnosed a reported "Server disconnected" as stale (app wasn't running, config verified correct, exact subprocess launch re-simulated successfully). |
| 2026-09-15 | Added `src/demo_journalist_workflow.py` and `docs/07_journalist_demo.md` — a before/after worked example: an intentionally-flawed draft (5 Russian-transliteration place-name errors) corrected live through the real `check_style_rule` MCP tool call, not a lookup toy. Scenario is inspired by France24's 2026-09-14 Zelensky de-escalation report (paraphrased fact only); the Ukrainian city names are original additions for the demo, not reproduced from the article — documented explicitly to keep the sourcing honest. Verified live: all 5 errors caught and corrected, tests still 6/6. |
| 2026-09-15 | Removed `reponses_volet_mcp_denia.md` from the repo root — a private, French-language planning note (employer/job-application specifics) left over from before the POC's scope was set. Not referenced anywhere else, and its useful content was already genericized into `docs/01_discovery.md`–`04_recommendation.md`. This repo is published to GitHub; that file didn't belong in it. |
