# wikidata_api_add_item

Python script to create a new Wikidata item via the MediaWiki API.
Item definition lives in `data/*.yaml` — edit that file to change what gets created, no Python required.

---

## Files

| File | Commit? | Description |
|------|---------|-------------|
| `001_wikidata_api_add_item.py` | yes | Main script |
| `data/item_magma.yaml` | yes | Example item (Magma.com) |
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
Do NOT rename any key (`label_en`, `qid`, etc.) — only change the values.

To find a QID: search https://www.wikidata.org → open the item → QID is in the URL.
Example: `https://www.wikidata.org/wiki/Q1330336` → QID is `Q1330336`.

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

> **Sandbox limitation**: `test.wikidata.org` has a separate database.
> Production properties (P279, P2283, P856) do not exist there.
> Always use `--no-claims` with `--sandbox`. Full item with claims only works on production.

---

## Operation — step by step

### Mode A: Sandbox (safe, use this first)

```bash
# Step 1 — preview the payload, no network write
python 001_wikidata_api_add_item.py --item data/item_myproject.yaml --sandbox --no-claims --dry-run

# Step 2 — write to sandbox (test.wikidata.org), skip claims
python 001_wikidata_api_add_item.py --item data/item_myproject.yaml --sandbox --no-claims

# Step 3 — check the result at the printed URL
# e.g. https://test.wikidata.org/wiki/Q246762
```

Expected output:
```
⚠ SANDBOX MODE — writing to test.wikidata.org
→ Loading item from: item_myproject.yaml
✓ Logged in as YourAccount@BotName
✓ CSRF token obtained
✓ Item created successfully: https://test.wikidata.org/wiki/Q246762
```

---

### Mode B: Production (wikidata.org — only after autoconfirmed)

```bash
# Step 1 — preview the full payload including claims
python 001_wikidata_api_add_item.py --item data/item_myproject.yaml --dry-run

# Step 2 — write to production
python 001_wikidata_api_add_item.py --item data/item_myproject.yaml

# Step 3 — check the result at the printed URL
# e.g. https://www.wikidata.org/wiki/Q130591234
```

Expected output:
```
→ Loading item from: item_myproject.yaml
✓ Logged in as YourAccount@BotName
✓ CSRF token obtained
✓ Item created successfully: https://www.wikidata.org/wiki/Q130591234
```

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
- **Duplicate check**: search Wikidata by label before POST — warn if item already exists
- **`instance_of` support**: add P31 block to YAML (most items need it alongside P279)
- **Multilingual**: add `label_fr`, `description_fr` blocks in YAML — script picks them all up
- **QID validator**: `--validate-qids` hits Wikidata API to confirm all QIDs in YAML exist before submitting
- **Update mode**: `--qid Q123456` patches an existing item instead of creating new
- **Log to file**: `--log output.json` saves API response for audit trail

---

## Changelog

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
