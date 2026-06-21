# wikidata_api_add_item

Python script to create a new Wikidata item via the MediaWiki API.
Item definition lives in `data/*.yaml` — edit that file to change what gets created, no Python required.
---

## TRY

### 002_wikidata_api_add_item.py (v2 — claims work in sandbox too)

```bash

# SANDBOX (safe, use this first)
# create the item (label + description + aliases only)
python 002_wikidata_api_add_item.py --item data/item_3WDOC.yaml --sandbox --no-claims

# create the item with the claims (attempts P279/P2283/P856 on test.wikidata.org)
python 002_wikidata_api_add_item.py --item data/item_Zeplin.yaml --sandbox


python 002_wikidata_api_add_item.py --item data/item_ben_fundis.yaml --sandbox

python 002_wikidata_api_add_item.py --item data/item_ben_hollis.yaml --sandbox

python 002_wikidata_api_add_item.py --item data/item_Youphil.yaml --sandbox

python 002_wikidata_api_add_item.py --item data/item_trevor_tweeten.yaml --sandbox

python 002_wikidata_api_add_item.py --item data/item_token_ai.yaml --sandbox


# PRODUCTION
# dry-run — print payload, no write
python 002_wikidata_api_add_item.py --item data/item_Zeplin.yaml --dry-run

# write to production
python 002_wikidata_api_add_item.py --item data/item_Zeplin.yaml


python 002_wikidata_api_add_item.py --item data/item_bankslave.yaml

python 002_wikidata_api_add_item.py --item data/item_ben_fundis.yaml

python 002_wikidata_api_add_item.py --item data/item_ben_hollis.yaml


python 002_wikidata_api_add_item.py --item data/item_Youphil.yaml

python 002_wikidata_api_add_item.py --item data/item_trevor_tweeten.yaml

python 002_wikidata_api_add_item.py --item data/item_token_ai.yaml

```

### 001_wikidata_api_add_item.py (v1 — claims always skipped in sandbox)

```bash
# SANDBOX (safe, use this first)
# create the item (no claims — sandbox auto-skips them)
python 001_wikidata_api_add_item.py --item data/item_3WDOC.yaml --sandbox --no-claims

python 001_wikidata_api_add_item.py --item data/item_Zeplin.yaml --sandbox

# PRODUCTION
# dry-run
python 001_wikidata_api_add_item.py --item data/item_3WDOC.yaml --dry-run

python 001_wikidata_api_add_item.py --item data/item_Zeplin.yaml --dry-run

# write to production
python 001_wikidata_api_add_item.py --item data/item_3WDOC.yaml

python 001_wikidata_api_add_item.py --item data/item_Zeplin.yaml
```





---

## Files

| File | Commit? | Description |
|------|---------|-------------|
| `002_wikidata_api_add_item.py` | yes | v2 — claims attempted in sandbox; `--no-claims` is explicit opt-out |
| `001_wikidata_api_add_item.py` | yes | v1 — sandbox always skips claims automatically |
| `data/item_ntlk.yaml` | yes | Example item (NLTK) |
| `data/item_template.yaml` | yes | Blank template — copy and fill in |
| `.env.example` | yes | Template showing required variables — safe to share |
| `.env` | **NO** | Your real credentials — never commit |
| `requirements.txt` | yes | Python dependencies |

---

## Quick start (in 5 steps)

```
1. pip install -r requirements.txt
2. cp .env.example .env   → fill in credentials
3. cp data/item_template.yaml data/item_myproject.yaml   → fill in item
4. python 001_wikidata_api_add_item.py --item data/item_myproject.yaml --sandbox --no-claims
5. python 001_wikidata_api_add_item.py --item data/item_myproject.yaml   (production, when autoconfirmed)



```

---

## Setup

### Step 1 — Install dependencies

```bash
conda create --name tags_treatment python=3.9.13
source activate tags_treatment
pip install -r requirements.txt
```

### Step 2 — Create your `.env` file

```bash
cp .env.example .env
```

Edit `.env` with your real values (see Authentication section below for how to get them):

```ini
WD_USERNAME="YourAccount@BotName"
WD_PASSWORD="your_bot_password"
WD_TEST_USERNAME="YourAccount@BotName"
WD_TEST_PASSWORD="your_test_bot_password"
WD_USER_AGENT="wikidata-item-creator/1.0 (https://your-project; your@email.com) python-requests"
```

### Step 3 — Create your item YAML

```bash
cp data/item_template.yaml data/item_myproject.yaml
```

Open `data/item_myproject.yaml` in any text editor. Replace every `FILL_ME_IN` value.
Do NOT rename any key (`label_en`, `label`, etc.) — only change the values.

**You do not need to know QIDs.** Write only the English label — the script searches Wikidata automatically:

```yaml
subclass_of:
  - label: "software library"      # script finds Q188860 automatically
  - label: "free software"

uses:
  - label: "Python"                # script finds Q28865 automatically
```

The script prints what it resolved so you can verify before writing to production:
```
→ Resolving QIDs from labels (production wikidata.org)...
  ✓ 'software library' → Q188860 (searched)
  ✓ 'Python' → Q28865 (searched)
  ⚠ 'something unknown' → not found on Wikidata, skipping
```

If a resolved QID is wrong, override it directly in the YAML:
```yaml
subclass_of:
  - label: "software library"
    qid: "Q188860"    # add this line to bypass search and use exact QID
```

---

## Authentication — bot passwords

Regular account passwords are **rejected** by the Wikidata API. You must use a **bot password**.

### Production bot (wikidata.org)

1. Log in at https://www.wikidata.org with your account
2. Go to https://www.wikidata.org/wiki/Special:BotPasswords
3. Click **Create a new bot password**
4. Give it a name (any name, e.g. `MyScript`)
5. Check these grants:
   - **Edit existing pages** ← required
   - **Create, edit, and move pages** ← required
   - **High-volume editing** ← recommended
6. Click **Create** — note the generated password
7. Your username for the `.env` is: `YourWikidataAccount@MyScript`

> **Important**: new items on production require an **autoconfirmed** account.
> Your account must be **≥ 4 days old AND have ≥ 50 edits** on wikidata.org.
> Until then, use the sandbox to test.

### Sandbox bot (test.wikidata.org)

1. Go to https://test.wikidata.org — your global Wikimedia account works, just log in
2. Go to https://test.wikidata.org/wiki/Special:BotPasswords
3. Same steps as above — same grants required
4. Bot passwords are **site-specific**, so you need a separate one for sandbox

> **Sandbox limitation (v1)**: `test.wikidata.org` has a separate database.
> In `001_wikidata_api_add_item.py`, claims are **always skipped** in sandbox mode — `--no-claims` is implied.
> Full item with claims only works reliably on production.
>
> **v2 behaviour**: `002_wikidata_api_add_item.py` attempts claims in sandbox too.
> Pass `--no-claims` explicitly if properties are missing on `test.wikidata.org`.

---

## Operation — step by step

### Mode A: Sandbox (safe, use this first)

The sandbox (`test.wikidata.org`) is a safe playground — nothing created there affects the real Wikidata.

**Two equivalent commands — both do the same thing:**

```bash
# Short form (recommended) — claims skipped automatically
python 001_wikidata_api_add_item.py --sandbox

# Long form — explicit flag, same result
python 001_wikidata_api_add_item.py --sandbox --no-claims
```

> `--no-claims` is now optional with `--sandbox`. The script skips claims automatically
> because `test.wikidata.org` has a separate database and does not have production
> properties (P279, P2283, P856). The item is created with label, description and
> aliases only — enough to confirm login and item creation work correctly.

Expected output:
```
⚠ SANDBOX MODE — writing to test.wikidata.org
→ Loading item from: item_myproject.yaml
ℹ Claims skipped automatically (test.wikidata.org lacks production properties)
✓ Logged in as YourAccount@BotName
✓ CSRF token obtained

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Item : NLTK
  URL  : https://test.wikidata.org/wiki/Q246769
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Copy the URL and open it in your browser to verify the item was created correctly.

---

### Mode B: Production (wikidata.org — only after autoconfirmed)

```bash
# Step 1 — preview payload + verify QID resolution (no network write)
python 001_wikidata_api_add_item.py --item data/item_myproject.yaml --dry-run
```

Expected output — check the resolved QIDs carefully:
```
→ Loading item from: item_myproject.yaml
→ Resolving QIDs from labels (production wikidata.org)...
  ✓ 'software library' → Q188860 (searched)
  ✓ 'Python' → Q28865 (searched)
  ⚠ 'bad label' → not found on Wikidata, skipping
=== DRY RUN — payload that would be sent to www.wikidata.org ===
...
```

If a QID is wrong → fix the label or add `qid:` override in YAML. Then:

```bash
# Step 2 — write to production
python 001_wikidata_api_add_item.py --item data/item_myproject.yaml

# Step 3 — check the result at the printed URL
# e.g. https://www.wikidata.org/wiki/Q130591234
```

Expected output:
```
→ Loading item from: item_myproject.yaml
→ Resolving QIDs from labels (production wikidata.org)...
  ✓ 'software library' → Q188860 (searched)
  ✓ 'Python' → Q28865 (searched)
✓ Logged in as YourAccount@BotName
✓ CSRF token obtained

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Item : My Project
  URL  : https://www.wikidata.org/wiki/Q130591234
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Copy the URL and open it in your browser to verify the full item with all claims.

---

## All flags

| Flag | Description |
|------|-------------|
| `--item PATH` | Path to the item YAML file. Auto-detected if only one `.yaml` in `data/` |
| `--sandbox` | Write to `test.wikidata.org` (uses `WD_TEST_*` credentials) |
| `--no-claims` | Skip statements/claims — required for sandbox |
| `--dry-run` | Print payload without writing anything |

---

## Improvement ideas (roadmap)

- **Batch mode**: `--item-dir data/` creates all `.yaml` files in one run
- **Duplicate check**: ~~search Wikidata by label before POST — warn if item already exists~~ (done in v1.6.0)
- **`instance_of` support**: add P31 block to YAML (most items need it alongside P279)
- **Multilingual**: add `label_fr`, `description_fr` blocks in YAML — script picks them all up
- **Update mode**: `--qid Q123456` patches an existing item instead of creating new
- **Log to file**: `--log output.json` saves API response for audit trail

---

## Changelog

### v2.0.0 — `002_wikidata_api_add_item.py`
- **Claims in sandbox**: removed auto-skip of claims when `--sandbox` is passed; `--no-claims` is now the explicit opt-out instead of being implied
- Output line added: prints QID alongside URL in the success banner
- Success banner shows claimed properties summary (e.g. `P279 ×3, P2283 ×4, P856`)
- `build_item_data`: skips empty claim groups per-property (cleaner than end dict-comp)

### v1.6.0
- **Duplicate-item guard**: if the API returns `modification-failed` with a label+description conflict, the script now extracts the existing QID, prints a warning (`⚠ Item already exists as QXXXXX`), and exits cleanly instead of crashing with a `RuntimeError`
- Add `import re` (stdlib, no new dependency)

### v1.5.0
- **Auto QID resolution**: no more manual QID lookup — write `label:` only in YAML; script calls `wbsearchentities` on production wikidata.org and resolves each label to a QID automatically
- Resolved QIDs printed before submission so user can verify (`✓ 'Python' → Q28865`)
- Labels not found on Wikidata print a warning and are skipped (`⚠ not found, skipping`)
- `qid:` field remains optional override — if provided, used directly without searching (backward compatible)
- Fix `item_ntlk.yaml`: corrected broken YAML structure (duplicate keys, misaligned list syntax)
- New `item_template.yaml`: label-only format, no QIDs required, full inline instructions
- Remove stale `~~` backup files from `data/`

### v1.4.0
- Move item YAML files to `data/` directory — keeps scripts and data separate
- Add `--item PATH` flag to specify which YAML to load; auto-detects single file in `data/` if flag omitted; clear error if multiple files found
- Add `data/item_template.yaml` — blank template with `FILL_ME_IN` placeholders and inline instructions

### v1.3.0
- **Security**: personal info removed from code — `WD_USER_AGENT` now loaded from `.env`; no credentials or identifying data hardcoded
- **Externalize item**: item definition moved to `item.yaml` (YAML format, human-editable, no Python required); script validates required keys on load
- **`.env.example`**: added safe-to-commit template showing all required variables
- Add `pyyaml` dependency

### v1.2.0
- Add `--sandbox` flag to target `test.wikidata.org` (uses `WD_TEST_*` credentials)
- Add `--no-claims` flag to skip statements (test.wikidata.org lacks production properties)
- Dynamic `API_URL` and credentials set at runtime based on flags

### v1.1.0
- Add `python-dotenv` to load credentials from `.env` file
- Add `User-Agent` header to session (Wikimedia blocks requests without it — root cause of 403)
- Add `check_credentials()` with clear error messages for missing or malformed credentials
- Move credential check to live-run only so `--dry-run` works without valid credentials
- Create `requirements.txt`

### v1.0.0
- Initial script: two-step MediaWiki login, CSRF token, `wbeditentity` item creation
- `--dry-run` flag to preview payload without writing
