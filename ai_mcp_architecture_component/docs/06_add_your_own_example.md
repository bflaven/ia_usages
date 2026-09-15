# 06 — Add Your Own Example (no code required)

The entire "database" for this POC is one JSON file:
`src/data/newsroom_style_guide.json`. There is no real database — see "No
database, on purpose" below. To simulate your own use case, edit that file
directly. No restart needed: every lookup re-reads the file from disk
(`style_guide.py`'s `_load_raw()`), so a saved edit is live on the very
next request.

---

## The shape of one entry

Every entry needs exactly these five fields, all plain strings:

| Field | What it means | Example |
|---|---|---|
| `term` | The exact word/phrase someone will type or say, as written in the source language | `"Sud-Liban"` |
| `language_pair` | Which language pair this rule applies to, `xx-yy` | `"fr-en"` |
| `approved` | The correct rendering to use | `"southern Lebanon"` |
| `note` | The one-line house-style rule that explains *why* | `"Lowercase 'southern' unless starting a headline..."` |
| `category` | A free-text tag to group similar entries | `"place_name"` |

That's it. No IDs, no nesting, no optional fields to worry about.

---

## Step by step: add one entry

1. Open `src/data/newsroom_style_guide.json` in any text editor.
2. Inside the `"entries": [ ... ]` array, copy one existing entry block
   (the `{ ... }` with its trailing comma) and paste it as a new one.
3. Fill in your five fields. Example — adding a made-up term:

```json
{
  "term": "intelligence artificielle frugale",
  "language_pair": "fr-en",
  "approved": "frugal AI",
  "note": "Use 'frugal AI', not 'lightweight AI' — house style term for low-compute models.",
  "category": "terminology"
}
```

4. Make sure every entry except the last one ends with a comma, and the
   last one doesn't (plain JSON syntax — a trailing comma will break the
   file).
5. Optional but recommended: bump the top-level `"updated"` date so
   `guide_last_updated` reflects your change:

```json
{
  "updated": "2026-09-20",
  "entries": [ ... ]
}
```

6. Save the file. Nothing else to run — no migration, no restart.

---

## Verify your new entry works (pick any one)

**Fastest — the test that doesn't need a server running:**

```bash
conda activate mcp_architecture_component
python -c "from src import style_guide; print(style_guide.lookup_term('intelligence artificielle frugale', 'fr-en'))"
```

Expected: `{'found': True, ... 'approved': 'frugal AI', ...}`.

**Or in the browser** (see `docs/05_modop.md` STEP 4bis for the full
click-by-click version):

```bash
uvicorn src.main:app --reload
```

Open `http://127.0.0.1:8000/`, expand `/legacy/lookup-term`, "Try it out",
type your new `term` and `language_pair`, "Execute" — same walkthrough,
your own data.

**Or through the MCP path** (the actual point of this POC):

```bash
python -m src.client_demo
```

Edit the three calls near the bottom of `src/client_demo.py` to use your
term instead of `"Sud-Liban"` if you want to see it end-to-end through the
MCP tool call rather than the REST endpoint.

---

## Worked example already in the repo: Ukrainian vs. Russian place names

A concrete, real-world extension of the use case, already added to
`src/data/newsroom_style_guide.json` as `ru-en` entries: a newsroom house
rule to use the Ukrainian transliteration of a city name, not the
Russian-derived one that was the international-press default before 2022
(Kyiv not Kiev, Kharkiv not Kharkov, Lviv not Lvov, Odesa not Odessa,
Mykolaiv not Nikolaev, Zaporizhzhia not Zaporozhye, Chernihiv not
Chernigov, plus two post-2016 decommunization renames: Dnipro
(ex-Dnepropetrovsk) and Bakhmut (ex-Artemivsk)).

**How this maps onto the persona / User Story pattern** (see
`docs/02_user_story.md`): an editor role — call them the house-style
enforcer — needs *any* AI assistant a reporter uses to catch the outdated
Russian form and surface the correct Ukrainian one automatically, instead
of relying on every reporter to remember the house rule by hand. Same
shape as Amira's story, same shape as the Tom/Maureen toy example: **As**
the style enforcer, **I want** any AI assistant a reporter uses to check
place names against house style, **so that** the newsroom never publishes
"Kiev" when the current rule says "Kyiv" — regardless of which AI tool
that reporter happens to be using that day. That "regardless of which
tool" clause is, again, exactly the MCP argument.

Try it (no server needed):

```bash
python -c "from src import style_guide; print(style_guide.lookup_term('Kiev', 'ru-en'))"
python -c "from src import style_guide; print(style_guide.lookup_term('Artemivsk', 'ru-en'))"
```

Or live, through an actual AI client with zero integration code — see
`docs/05_modop.md` STEP 7.5 for the Claude Desktop walkthrough.

---

## No database, on purpose

There is no SQLite, no Postgres, no ORM, nothing to install or migrate.
`src/data/newsroom_style_guide.json` **is** the entire data layer — a flat
file both `legacy_api.py` and `mcp_server.py` read through the shared
`style_guide.py` module. This is deliberate, not a shortcut waiting to be
"fixed":

- The whole point of this POC is the **integration pattern** (REST vs.
  MCP), not data engineering — a real database would add moving parts
  that have nothing to do with that argument.
- A flat file is something anyone, technical or not, can open, read, and
  edit directly — see the steps above.
- If this ever became a real production service, swapping
  `style_guide._load_raw()` for a real database call is a change confined
  to *one function*, because both services already read only through this
  one module. That's what "shared data-access module" bought you — see
  `docs/03_kpis.md`, "Quality/reliability."

Don't add one to make this "more real." Simple, editable, and correct
beats a cathedral of infrastructure nobody asked for.
