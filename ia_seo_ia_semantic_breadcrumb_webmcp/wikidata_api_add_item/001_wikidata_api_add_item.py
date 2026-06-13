#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name tags_treatment python=3.9.13
conda info --envs
source activate tags_treatment
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n tags_treatment

# update conda
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


# [path]
cd /path/to/wikidata_api_add_item/

# LAUNCH the file
python 001_wikidata_api_add_item.py


001_wikidata_api_add_item.py  — v1.4.0
--------------------
Creates a new Wikidata item via the MediaWiki API.
Item definition lives in data/*.yaml — pass --item to specify which file.
If data/ contains exactly one .yaml file, it is used automatically.

Requirements:
    pip install requests python-dotenv pyyaml

Authentication:
    Wikidata requires bot passwords — regular account passwords are rejected.

    Production (wikidata.org) — requires autoconfirmed account (4 days + 50 edits):
      1. Log in to https://www.wikidata.org
      2. Go to https://www.wikidata.org/wiki/Special:BotPasswords
      3. Create bot — grants required:
           - Edit existing pages
           - Create, edit, and move pages
           - High-volume editing (recommended)
      4. Username format: "YourAccount@BotName"

    Sandbox (test.wikidata.org) — no restrictions, safe for testing:
      1. Log in to https://test.wikidata.org (global Wikimedia account works)
      2. Go to https://test.wikidata.org/wiki/Special:BotPasswords
      3. Create bot with same grants (bot passwords are site-specific)
      4. Use WD_TEST_USERNAME / WD_TEST_PASSWORD in .env

    Credentials go in .env (never commit — already in .gitignore).
    See .env.example for the required variables.

Usage:
    python 001_wikidata_api_add_item.py --item data/item_magma.yaml
    python 001_wikidata_api_add_item.py --item data/item_magma.yaml --sandbox --no-claims
    python 001_wikidata_api_add_item.py --item data/item_magma.yaml --dry-run

Note on --no-claims / sandbox:
    test.wikidata.org has a separate database — production properties (P279, P2283, P856)
    do not exist there. Use --no-claims when testing on sandbox; full claims only work
    on production once the account is autoconfirmed.
"""

import os
import sys
import json
import argparse
import pathlib
import requests
import yaml
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration — all sensitive values come from .env, never hardcoded
# ---------------------------------------------------------------------------
WD_USERNAME      = os.getenv("WD_USERNAME", "")
WD_PASSWORD      = os.getenv("WD_PASSWORD", "")
WD_TEST_USERNAME = os.getenv("WD_TEST_USERNAME", "")
WD_TEST_PASSWORD = os.getenv("WD_TEST_PASSWORD", "")
USER_AGENT       = os.getenv("WD_USER_AGENT", "wikidata-item-creator/1.0 python-requests")

PROD_API_URL    = "https://www.wikidata.org/w/api.php"
SANDBOX_API_URL = "https://test.wikidata.org/w/api.php"

# Set at runtime by main() based on --sandbox flag
API_URL  = PROD_API_URL
USERNAME = WD_USERNAME
PASSWORD = WD_PASSWORD

# ---------------------------------------------------------------------------
# Item loader
# ---------------------------------------------------------------------------
DATA_DIR = pathlib.Path(__file__).parent / "data"


def resolve_item_path(explicit: Optional[str]) -> pathlib.Path:
    """Return the YAML file to load.

    Priority:
      1. --item path provided by user
      2. Single .yaml file found in data/ (excluding item_template.yaml)
      3. Error with helpful message
    """
    if explicit:
        p = pathlib.Path(explicit)
        if not p.is_absolute():
            p = pathlib.Path(__file__).parent / p
        if not p.exists():
            sys.exit(f"ERROR: Item file not found: {p}")
        return p

    candidates = [
        f for f in DATA_DIR.glob("*.yaml")
        if f.name != "item_template.yaml"
    ]
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) == 0:
        sys.exit(
            f"ERROR: No item YAML files found in {DATA_DIR}/\n"
            "Copy data/item_template.yaml, fill it in, then pass:\n"
            "  --item data/your_item.yaml"
        )
    names = "\n  ".join(f.name for f in sorted(candidates))
    sys.exit(
        f"ERROR: Multiple item files found in {DATA_DIR}/:\n  {names}\n"
        "Specify which one to use:\n"
        "  --item data/your_item.yaml"
    )


def load_item(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    required = {"label_en", "description_en", "aliases_en",
                "subclass_of", "uses", "official_website"}
    missing = required - data.keys()
    if missing:
        sys.exit(f"ERROR: {path.name} is missing keys: {', '.join(sorted(missing))}")
    return data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def check_credentials(sandbox: bool) -> None:
    user = WD_TEST_USERNAME if sandbox else WD_USERNAME
    pwd  = WD_TEST_PASSWORD if sandbox else WD_PASSWORD
    prefix  = "WD_TEST_" if sandbox else "WD_"
    bot_url = (
        "https://test.wikidata.org/wiki/Special:BotPasswords"
        if sandbox else
        "https://www.wikidata.org/wiki/Special:BotPasswords"
    )
    if not user or not pwd:
        sys.exit(
            f"ERROR: {prefix}USERNAME or {prefix}PASSWORD not set.\n"
            f"Add to .env:\n"
            f"  {prefix}USERNAME=\"YourAccount@BotName\"\n"
            f"  {prefix}PASSWORD=\"your_bot_password\"\n"
            f"Bot passwords: {bot_url}"
        )
    if "@" not in user:
        sys.exit(
            f"ERROR: {prefix}USERNAME='{user}' looks wrong.\n"
            "Wikidata requires bot password format: 'YourAccount@BotName'\n"
            f"Create one at: {bot_url}"
        )


def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def login(session: requests.Session) -> None:
    r = session.get(API_URL, params={
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json",
    })
    r.raise_for_status()
    login_token = r.json()["query"]["tokens"]["logintoken"]

    r = session.post(API_URL, data={
        "action": "login",
        "lgname": USERNAME,
        "lgpassword": PASSWORD,
        "lgtoken": login_token,
        "format": "json",
    })
    r.raise_for_status()
    result = r.json()
    if result["login"]["result"] != "Success":
        raise RuntimeError(f"Login failed: {result['login']}")
    print(f"✓ Logged in as {USERNAME}")


def get_csrf_token(session: requests.Session) -> str:
    r = session.get(API_URL, params={
        "action": "query",
        "meta": "tokens",
        "format": "json",
    })
    r.raise_for_status()
    return r.json()["query"]["tokens"]["csrftoken"]


def build_item_data(item: dict, no_claims: bool = False) -> dict:
    """Assemble the Wikibase JSON structure for the new item."""

    def qid_snak(prop: str, qid: str) -> dict:
        return {
            "snaktype": "value",
            "property": prop,
            "datavalue": {
                "value": {"entity-type": "item", "id": qid},
                "type": "wikibase-entityid",
            },
        }

    def url_snak(prop: str, url: str) -> dict:
        return {
            "snaktype": "value",
            "property": prop,
            "datavalue": {"value": url, "type": "string"},
        }

    data = {
        "labels":       {"en": {"language": "en", "value": item["label_en"]}},
        "descriptions": {"en": {"language": "en", "value": item["description_en"]}},
        "aliases":      {"en": [{"language": "en", "value": a} for a in item["aliases_en"]]},
    }

    if not no_claims:
        statements = {}
        statements["P279"] = [
            {"mainsnak": qid_snak("P279", e["qid"]), "type": "statement", "rank": "normal"}
            for e in item["subclass_of"]
        ]
        statements["P2283"] = [
            {"mainsnak": qid_snak("P2283", e["qid"]), "type": "statement", "rank": "normal"}
            for e in item["uses"]
        ]
        statements["P856"] = [{
            "mainsnak": url_snak("P856", item["official_website"]),
            "type": "statement",
            "rank": "preferred",
        }]
        data["claims"] = statements

    return data


def create_item(session: requests.Session, data: dict, csrf_token: str, label: str) -> str:
    r = session.post(API_URL, data={
        "action": "wbeditentity",
        "new": "item",
        "data": json.dumps(data),
        "token": csrf_token,
        "format": "json",
        "summary": f"Creating item '{label}' via wikidata_add_item.py",
    })
    r.raise_for_status()
    result = r.json()
    if "error" in result:
        raise RuntimeError(f"API error: {result['error']}")
    return result["entity"]["id"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    global API_URL, USERNAME, PASSWORD

    parser = argparse.ArgumentParser(
        description="Create a new Wikidata item from a YAML file in data/."
    )
    parser.add_argument(
        "--item", metavar="PATH",
        help="Path to the item YAML file (default: auto-detect single file in data/)."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the payload without writing to Wikidata."
    )
    parser.add_argument(
        "--sandbox", action="store_true",
        help="Write to test.wikidata.org instead of production (uses WD_TEST_* credentials)."
    )
    parser.add_argument(
        "--no-claims", action="store_true",
        help="Skip statements/claims. Required for sandbox: test.wikidata.org lacks production properties."
    )
    args = parser.parse_args()

    if args.sandbox:
        API_URL  = SANDBOX_API_URL
        USERNAME = WD_TEST_USERNAME
        PASSWORD = WD_TEST_PASSWORD
        wiki_base = "https://test.wikidata.org/wiki"
        print("⚠ SANDBOX MODE — writing to test.wikidata.org")
    else:
        wiki_base = "https://www.wikidata.org/wiki"

    item_path = resolve_item_path(args.item)
    print(f"→ Loading item from: {item_path.name}")
    item = load_item(item_path)
    no_claims = args.no_claims
    item_data = build_item_data(item, no_claims=no_claims)

    if args.dry_run:
        target = "test.wikidata.org" if args.sandbox else "www.wikidata.org"
        suffix = " (no claims)" if no_claims else ""
        print(f"=== DRY RUN — payload that would be sent to {target}{suffix} ===")
        print(json.dumps(item_data, indent=2, ensure_ascii=False))
        if not no_claims:
            print("\nSubclass of (P279):")
            for e in item["subclass_of"]:
                print(f"  {e['qid']}  {e['label']}")
            print("\nUses (P2283):")
            for e in item["uses"]:
                print(f"  {e['qid']}  {e['label']}")
            print(f"\nOfficial website (P856): {item['official_website']}")
        return

    # Live run
    check_credentials(args.sandbox)
    session = get_session()
    login(session)
    csrf_token = get_csrf_token(session)
    print("✓ CSRF token obtained")

    new_qid = create_item(session, item_data, csrf_token, item["label_en"])
    print(f"✓ Item created successfully: {wiki_base}/{new_qid}")


if __name__ == "__main__":
    main()
