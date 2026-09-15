# MODOP — Operational Method to Launch & Verify This POC

Step-by-step checklist to bring the project up from a clean checkout and
confirm every piece actually works, not just "looks right." Run steps in
order. Each step has an expected result — if it does not match, stop and
fix before moving on.

---

## Quick Start — the sequence to repeat every time (read this first)

This is the condensed loop for "I want to demo this again" or "something
looks broken, where do I even start." Three steps, in order. If a step
fails, the linked STEP below has the full detail and troubleshooting.

**Step 1 — sanity-check the MCP server alone, in a terminal, with no
client involved.** This is the fastest feedback loop: if this fails,
Claude Desktop will fail too, for the same reason, just with a much
vaguer error.

```bash
conda activate mcp_architecture_component
cd /absolute/path/to/this/repo
python -m src.client_demo
```

Expected: tool discovery listing `lookup_term`/`check_style_rule`, then 3
successful calls with real data printed. (This project uses conda + pip,
not `uv` — no separate install step needed beyond STEP 2 below if the env
already exists.) If this fails → full detail in STEP 5.

**Step 2 — open/reopen Claude Desktop, confirm the connector is healthy.**

- If Claude Desktop is already running: **quit it fully** (`Cmd+Q`, not
  just close the window) — a config change only takes effect on a fresh
  launch.
- Reopen it.
- Check its Settings → Developer (or Connectors) panel for
  `newsroom-style-guide`.
- Expected: status is healthy (running/connected), not a red "Failed" /
  "Server disconnected."
- If it still shows Failed → full detail in STEP 7, especially 7.2's two
  silent traps (bare `python`, unsupported `cwd`) and 7.6 (how to re-edit
  the config file yourself, with the comma/validation discipline).

**Step 3 — test it live, with the Ukrainian city-name example.** In a new
Claude Desktop chat:

> "Using newsroom-style-guide, check the house style for 'Kiev' and for
> 'Artemivsk'."

Expected: a visible tool-call step, then `"approved": "Kyiv"` and
`"approved": "Bakhmut"` with the house-style note for each. Full detail
and more example terms in STEP 7.5 and `docs/06_add_your_own_example.md`.

---

## STEP 0 — Prerequisites

- [ ] Conda installed (`conda --version`)
- [ ] Repo checked out locally, current directory = repo root
      (`_ia_mcp_architecture_component/`)

---

## STEP 1 — Environment

```bash
conda env list
```

Expected: `mcp_architecture_component` listed. If missing:

```bash
conda create -n mcp_architecture_component python=3.13
```

Activate:

```bash
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate mcp_architecture_component
```

Expected: prompt prefixed `(mcp_architecture_component)`.

```bash
python --version
```

Expected: `Python 3.13.x`.

---

## STEP 2 — Dependencies

```bash
pip install -r requirements.txt
```

Expected: no errors. Confirm the two SDK-critical packages landed:

```bash
python -c "import importlib.metadata as m; print(m.version('mcp'), m.version('fastapi'))"
```

Expected: `2.x.x 0.14x.x` (mcp major version **2**, not 1 — v1's `FastMCP`
import path is gone by design, see `CLAUDE.md`). Note: `mcp.__version__`
does not exist on this package — it raises `AttributeError`, not a version
string — always check via `importlib.metadata.version("mcp")` instead.

---

## STEP 3 — Unit / integration tests

```bash
python -m pytest tests/ -v
```

Expected: **6 passed**. If any fail, do not proceed to manual verification
below — fix the code first, tests are the fast signal.

---

## STEP 4 — "Before": legacy REST service

Terminal A:

```bash
conda activate mcp_architecture_component
uvicorn src.main:app --reload
```

Expected log: `Uvicorn running on http://127.0.0.1:8000`.

**Open `http://127.0.0.1:8000/` in a browser.** It redirects straight to
the interactive Swagger UI (`/docs`) — no bare 404, no need to know the
routes up front. This is the intended way to explore the API if you are
not going to read the source: click "Try it out" on `legacy-rest` and
`health`, right there in the browser.

Terminal B (new shell, no need to activate env — plain curl), for a
scripted check instead:

```bash
curl -i "http://127.0.0.1:8000/"
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/legacy/lookup-term?term=Sud-Liban&language_pair=fr-en"
```

Expected:
- `/` → `307` redirect to `/docs`
- `/health` → `{"status":"ok","style_guide_last_updated":"2026-09-15"}`
- `/legacy/lookup-term...` → `"found": true`, `"approved": "southern Lebanon"`

Stop Terminal A (`Ctrl+C`) when done.

---

## STEP 4bis — Zero-terminal walkthrough (for a non-engineer reader)

Skip this if you already did the curl checks above. This is the same
check, but every step is a click, and every result is a screenshot-style
description of exactly what you should see. No command line beyond the
one line that starts the server.

**Setup, once**: open a terminal, run these two lines, leave that window
open and alone for the rest of this section.

```bash
conda activate mcp_architecture_component
uvicorn src.main:app --reload
```

Expect this line to appear and then stop scrolling: `Uvicorn running on
http://127.0.0.1:8000`. If it stops there and does not show an error in
red, the server is up. Leave this terminal running in the background —
closing it turns the server off.

Now go to your browser for everything else.

### A. `http://127.0.0.1:8000/`

**Type this in the address bar and press Enter.**

- **What you expect**: a plain page, maybe an error, because you typed a
  bare address with nothing after it.
- **What you get instead**: the page instantly jumps to a different
  address ending in `/docs`, and you land on a title "Newsroom Style &
  Terminology Assistant — legacy REST demo" with three gray/blue boxes
  underneath labeled `doc`, `health`, `legacy-rest`. That jump is on
  purpose — it is the entire point of this URL.
- **Click nothing yet.** Just confirm the page title and the three boxes
  are there. If you see this, this check is done.

### B. `http://127.0.0.1:8000/health`

**Type this in the address bar and press Enter** — this one does NOT
redirect, it's a direct machine-readable check, so what you'll see is raw
text, not a nice page. That's expected here, not a bug.

- **What you expect**: something visual, a page.
- **What you get instead**: a small block of plain text, no styling:
  ```
  {"status":"ok","style_guide_last_updated":"2026-09-15"}
  ```
- **What to look for**: the word `"ok"` right after `"status":`. That
  single word is the entire answer to "is the service alive." Date after
  it will match whenever the style guide file was last edited — it does
  not need to be today's date.

### C. `http://127.0.0.1:8000/legacy/lookup-term` — the one with a form

This is the one you asked about — the GET box you can click and fill in.
Go back to `http://127.0.0.1:8000/docs` (or click `/` again, it redirects
there) for this one.

1. **Find the blue bar that says `GET` and `/legacy/lookup-term`.** It's
   under the `legacy-rest` heading. Click anywhere on that blue bar.
   - *Expect*: the bar expands downward and reveals a "Parameters" table
     and a white "Try it out" button in the top-right of the expanded box.
2. **Click the white "Try it out" button.**
   - *Expect*: the two gray input boxes underneath (`term`,
     `language_pair`) turn active/white and become editable. A blue
     "Execute" button appears below them, and a red "Cancel" button
     replaces "Try it out."
3. **Click inside the `term` box and type:** `Sud-Liban`
   - This is the exact spelling that exists in the demo style guide —
     capital S, capital L, one hyphen, no spaces.
4. **Click inside the `language_pair` box and type:** `fr-en`
5. **Click the big blue "Execute" button.**
   - *Expect*: the page does not navigate anywhere. Below the button, a
     "Responses" section appears (or updates) showing a `Curl` block, a
     `Request URL` line, and — the part that matters — a **"Server
     response"** section with `Code: 200` and a black "Response body" box
     containing:
     ```json
     {
       "found": true,
       "term": "Sud-Liban",
       "language_pair": "fr-en",
       "approved": "southern Lebanon",
       "note": "Lowercase 'southern' unless starting a headline; do not use 'South Lebanon' as a proper noun.",
       "category": "place_name",
       "suggestions": null,
       "guide_last_updated": "2026-09-15"
     }
     ```
   - **The one field that proves it worked**: `"found": true` and
     `"approved": "southern Lebanon"`. If `Code` shows anything other
     than `200`, or `"found"` is `false`, something is wrong — see
     Troubleshooting below.
6. **Optional — try a typo on purpose.** Clear the `term` box, type
   `Sud Liban` (no hyphen this time), click "Execute" again.
   - *Expect*: `Code: 200` still, but now `"found": false` and
     `"suggestions": ["Sud-Liban"]` — the system politely says "not
     found, did you mean this?" instead of guessing. That refusal-to-guess
     behavior is a deliberate design point of this POC, not a bug — worth
     remembering if this ends up in the article.

**When you're done**, go back to the terminal running `uvicorn` and press
`Ctrl+C` to stop the server.

---

## STEP 5 — "After": MCP server over stdio, proven by an independent client

```bash
conda activate mcp_architecture_component
python -m src.client_demo
```

Expected: script prints, in order —
1. tool discovery listing `lookup_term` and `check_style_rule`
2. known-term call → `found: true`, `approved: southern Lebanon`
3. unknown-term call → `found: false`, non-empty `suggestions`
4. `check_style_rule` call → hit on `Sud-Liban`

This is the one that matters most: it is a **second, independent client**
that imports nothing from `legacy_api.py` or `mcp_server.py` internals —
this is the N+M claim made concrete, not asserted.

---

## STEP 6 — MCP server over HTTP (alternate transport)

Terminal A:

```bash
conda activate mcp_architecture_component
python -m src.mcp_server --http
```

Expected log: server listening on `127.0.0.1:8001`.

**If you open `http://127.0.0.1:8001/` in a browser** (natural thing to
try — do not skip this instinct, it used to 404): you'll get plain JSON,
not a page, because this server has no Swagger UI — it only speaks
JSON-RPC over `POST /mcp`. Expected body:

```json
{
  "service": "newsroom-style-guide (MCP server)",
  "note": "This is an MCP server, not a browsable REST API...",
  "mcp_endpoint": "/mcp",
  "health_check": "/healthz"
}
```

That is the correct, intended result — it is telling you where to go
instead of silently failing. `http://127.0.0.1:8001/healthz` similarly
returns `{"status":"ok",...}`, and `/favicon.ico` returns a quiet `204`
instead of a 404 in the log.

Terminal B — the actual protocol check, curl:

```bash
curl -s http://127.0.0.1:8001/
curl -s http://127.0.0.1:8001/healthz
curl -N -X POST http://127.0.0.1:8001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"modop-check","version":"0.1"}}}'
```

Expected: `/` and `/healthz` return the JSON above; the `POST /mcp` call
returns `200 OK`, JSON-RPC result with `serverInfo.name` =
`newsroom-style-guide`, and a new session line in Terminal A's log.

Stop Terminal A (`Ctrl+C`) when done. Expected: a clean `INFO: Shutting
down` / `Application shutdown complete` log, ending with
`newsroom-style-guide MCP server stopped.` — no red traceback. If you do
see a `Traceback` / `KeyboardInterrupt` wall of text, you're on an older
copy of `src/mcp_server.py` — pull the fix from 2026-09-15 (see
Troubleshooting below).

---

## STEP 7 — Claude Desktop wiring, made concrete

### 7.1 Find the config file

macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
Windows: `%APPDATA%\Claude\claude_desktop_config.json`

It may already exist with other MCP servers in it (e.g. `filesystem`,
`memory`) — **do not overwrite the file**, only add a new key inside the
existing `"mcpServers": { ... }` block.

**Back it up first, every time:**

```bash
cp "$HOME/Library/Application Support/Claude/claude_desktop_config.json" \
   "$HOME/Library/Application Support/Claude/claude_desktop_config.json.bak_$(date +%Y%m%d_%H%M%S)"
```

### 7.2 Add this server — and get `command` + `env` right

Two traps here, both silent (no error dialog, the tool just doesn't work):

**Trap 1 — plain `"command": "python"`.** Claude Desktop launches the
server as its own subprocess, **without your shell's conda activation**,
so plain `python` resolves to whatever (or nothing) is on the app's own
PATH — not your `mcp_architecture_component` env, so `import mcp` fails
inside a process you can't see the error of. Fix: use the **full,
absolute path** to the conda env's python interpreter — find yours with:

```bash
conda activate mcp_architecture_component
which python
```

**Trap 2 — a `"cwd"` key.** It looks like the obvious way to tell the
server where the repo lives, and Claude Desktop accepts it in the file —
**but its schema doesn't actually support `cwd`**: the app silently drops
it the next time it rewrites its own config (e.g. on relaunch), and
`python -m src.mcp_server` then fails with `ModuleNotFoundError: No
module named 'src'` because nothing tells Python where to find the `src`
package. Fix: use `"env": {"PYTHONPATH": "..."}` instead — `env` *is*
part of the supported schema, and it survives the app's own rewrites.

Add this key inside the existing `"mcpServers": { ... }` object
(comma-separate it from whatever is already there):

```json
"newsroom-style-guide": {
  "command": "/opt/homebrew/Caskroom/miniconda/base/envs/mcp_architecture_component/bin/python",
  "args": ["-m", "src.mcp_server"],
  "env": {
    "PYTHONPATH": "/absolute/path/to/this/repo"
  }
}
```

Replace both absolute paths with your own (`which python` output, and
`pwd` run from the repo root).

### 7.3 Validate the JSON before restarting

A single missing comma here fails silently — Claude Desktop just won't
show the tool, with no error dialog.

```bash
python3 -c "import json; json.load(open('$HOME/Library/Application Support/Claude/claude_desktop_config.json')); print('valid JSON')"
```

Expected: `valid JSON`. If it errors, fix the syntax before continuing.

### 7.4 Restart Claude Desktop completely

Quit the app fully (not just close the window) and reopen it — a config
reload needs a full restart.

**Where to see it worked**: open a new chat, click the tools/connectors
icon (a small icon usually near the message box, or in the client's own
MCP/connector settings). Expected: `newsroom-style-guide` listed, with
`lookup_term` and `check_style_rule` as tools you can inspect.

### 7.5 Test it live — with a real, concrete example (Ukrainian place names)

This POC's style guide includes a small Ukrainian/Russian place-name
dataset (`ru-en` entries in `src/data/newsroom_style_guide.json`) —
exactly the kind of house-style rule a newsroom enforces: use the
Ukrainian transliteration (Kyiv, Kharkiv, Lviv...), not the Russian one
(Kiev, Kharkov, Lvov...). See `docs/06_add_your_own_example.md` for the
full worked example and why it fits this use case.

In a new Claude Desktop chat, type a prompt like:

``` text
Using the newsroom-style-guide tool, check the house style for the term 'Kiev' in the ru-en pair, and for 'Artemivsk'.
```
**Expected**: Claude Desktop shows it calling the `lookup_term` tool
(you'll see a tool-use step in the chat), then answers using the real
data — `"approved": "Kyiv"` for the first, `"approved": "Bakhmut"` for
the second, each with the house-style note explaining why. That tool call
happening at all — with zero code written for Claude Desktop specifically
— is the entire MCP argument, made concrete instead of theoretical.

### 7.6 Editing this file yourself, and adding more servers later

Do this with Claude Desktop **fully quit** (`Cmd+Q`) — editing while it's
running risks the app overwriting your edit on its own next save (this is
exactly how `"cwd"` got silently dropped, see 7.2).

1. Open `~/Library/Application Support/Claude/claude_desktop_config.json`
   in a real text/code editor — not TextEdit in rich-text mode, it can
   inject smart quotes and corrupt the file.
2. Back it up first:
   ```bash
   cp "$HOME/Library/Application Support/Claude/claude_desktop_config.json" \
      "$HOME/Library/Application Support/Claude/claude_desktop_config.json.bak_$(date +%Y%m%d_%H%M%S)"
   ```
3. `mcpServers` is a flat object — every server is a sibling key, none
   reference each other:
   ```json
   {
     "mcpServers": {
       "filesystem": { "...": "..." },
       "memory": { "...": "..." },
       "newsroom-style-guide": {
         "command": "/absolute/path/to/env/bin/python",
         "args": ["-m", "src.mcp_server"],
         "env": { "PYTHONPATH": "/absolute/path/to/this/repo" }
       }
     }
   }
   ```
   Add a new server as a new key inside that same object.
4. **Comma discipline** — the most common way this file breaks: every
   entry except the *last* one needs a trailing comma after its closing
   `}`. Adding a server after the current last one means adding a comma
   to that old last entry, and giving your new one none (unless you add
   another after it).
5. Validate before relaunching — paste into
   [jsonlint.com](https://jsonlint.com/), or locally:
   ```bash
   python3 -c "import json; json.load(open('$HOME/Library/Application Support/Claude/claude_desktop_config.json'))"
   ```
   No output / no error = valid.
6. Quit-and-reopen Claude Desktop fully, then check the tools/connectors
   icon in a new chat.

**Before adding a genuinely new server** (e.g. `newsroom-translation-guide`,
`newsroom-naming-guide`): decide whether it needs to be a **separate
process** at all, or is really just **another tool on the existing
server**. If it's the same underlying repo/data and the split is only
conceptual, add another `@mcp.tool()` function to the existing
`src/mcp_server.py` instead — one config entry, one process, no new moving
part to babysit. Reach for a new `mcpServers` entry only when it's an
actually separate service (different repo, different deploy). Matches
this project's own stance in `CLAUDE.md` against multiplying processes
for their own sake.

---

## Pass/fail summary — copy this checklist when verifying a release

- [ ] `conda env list` shows `mcp_architecture_component`
- [ ] `python --version` → 3.13.x
- [ ] `importlib.metadata.version("mcp")` → 2.x.x
- [ ] `pytest tests/ -v` → 6 passed
- [ ] `uvicorn src.main:app` + open `http://127.0.0.1:8000/` in browser → redirects to Swagger UI, no 404
- [ ] curl `/health` → ok
- [ ] curl `/legacy/lookup-term?term=Sud-Liban` → found, southern Lebanon
- [ ] `python -m src.client_demo` → all 3 tool calls succeed, correct data
- [ ] `python -m src.mcp_server --http` + open `http://127.0.0.1:8001/` in browser → explanatory JSON, no 404
- [ ] curl `initialize` on `POST /mcp` → 200, session created
- [ ] (optional) Claude Desktop config → `newsroom-style-guide` visible in tools, live "Kiev"→"Kyiv" lookup works

If every box is checked, the POC is verified end-to-end and safe to
publish / demo / push.

---

## Troubleshooting quick reference

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: mcp.server.fastmcp` | Following an old v1 tutorial | Use `MCPServer` from `mcp.server.mcpserver` — see `CLAUDE.md` SDK version note |
| `AttributeError: module 'mcp' has no attribute '__version__'` | `mcp` package does not expose `__version__` | Check version via `importlib.metadata.version("mcp")`, not the attribute |
| `client_demo.py` hangs / no output | Ran without `-m` | Always invoke as `python -m src.client_demo`, not `python src/client_demo.py` — relative imports need package context |
| `--http` mode: curl hangs or session never starts | MCP server accidentally mounted inside another app | Do not mount `mcp_server.py` into `main.py` — see lifespan-propagation note in `CLAUDE.md` |
| `--http` mode: `GET /` or `/favicon.ico` returns `404 Not Found` in the server log | Old behavior before `custom_route` handlers were added (fixed 2026-09-15) | Pull latest `src/mcp_server.py` — `/`, `/healthz`, `/favicon.ico` now answer directly; this is expected to be JSON, not a page, since there is no Swagger UI on this server |
| `--http` mode: pressing `Ctrl+C` prints a big red `Traceback` ending in `KeyboardInterrupt` | Old behavior — `anyio.run()` let the interrupt bubble up uncaught (fixed 2026-09-15) | Pull latest `src/mcp_server.py` — `Ctrl+C` is now caught and prints one clean line instead |
| REST and MCP give different answers for the same term | Logic duplicated instead of shared | Both must read only through `style_guide.py` — check no second copy of lookup logic was added |
| `pytest` fails on `TestClient` import | `httpx` missing/mismatched | Reinstall pinned versions: `pip install -r requirements.txt` |
| Claude Desktop doesn't list `newsroom-style-guide` at all, no error shown | Invalid JSON in `claude_desktop_config.json`, or app not fully restarted | Validate with the `python3 -c "import json..."` check in STEP 7.3; fully quit and reopen the app, not just close the window |
| Tool listed, but calling it errors / times out | `command` points to a `python` that doesn't have `mcp` installed (common when using bare `"python"` instead of the env's full path) | Use the absolute path from `which python` (env activated) — see STEP 7.2 |
| Tool listed, calling it fails with `ModuleNotFoundError: No module named 'src'` | Config uses `"cwd"`, which Claude Desktop's schema silently drops when it rewrites its own config file | Replace `"cwd"` with `"env": {"PYTHONPATH": "/absolute/path/to/this/repo"}` — see STEP 7.2, Trap 2 |
