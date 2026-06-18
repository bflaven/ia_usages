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
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_seo_ia_semantic_breadcrumb_webmcp/wikidata_api_add_item/

# LAUNCH the file

002_wikidata_api_add_item.py  — v2.0.0
--------------------
Creates a new Wikidata item via the MediaWiki API.
Improved over v1: claims (subclass_of, uses, official_website) are now
attempted in sandbox mode too. Use --no-claims to skip them explicitly.

Item definition lives in data/*.yaml — pass --item to specify which file.
If data/ contains exactly one .yaml file, it is used automatically.

QID resolution:
    You do not need to know QIDs. Write only "label" in your YAML.
    The script searches Wikidata automatically and prints what it resolved.
    If you DO know the QID, add "qid: Q12345" and it is used directly.

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
    # SANDBOX (safe, use this first)
    # create item without claims
    python 002_wikidata_api_add_item.py --item data/item_3WDOC.yaml --sandbox --no-claims

    # create item with claims (test.wikidata.org must have the properties P279/P2283/P856)
    python 002_wikidata_api_add_item.py --item data/item_Zeplin.yaml --sandbox

    # PRODUCTION
    # dry-run — print payload, no write
    python 002_wikidata_api_add_item.py --item data/item_Zeplin.yaml --dry-run

    # write to production
    python 002_wikidata_api_add_item.py --item data/item_Zeplin.yaml

Note on sandbox claims:
    Unlike v1, this script does NOT auto-skip claims in sandbox mode.
    test.wikidata.org mirrors the production schema but may lack some properties.
    If claims fail in sandbox, rerun with --no-claims for a safe label-only test.
"""

import os
import re
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
USER_AGENT       = os.getenv("WD_USER_AGENT", "wikidata-item-creator/2.0 python-requests")

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
    """Return the YAML file to load."""
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
    user   = WD_TEST_USERNAME if sandbox else WD_USERNAME
    pwd    = WD_TEST_PASSWORD if sandbox else WD_PASSWORD
    prefix = "WD_TEST_" if sandbox else "WD_"
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


def resolve_label_to_qid(label: str, session: requests.Session) -> Optional[str]:
    """Search production Wikidata for a QID by English label. Returns first match or None."""
    r = session.get(PROD_API_URL, params={
        "action": "wbsearchentities",
        "search": label,
        "language": "en",
        "type": "item",
        "limit": 1,
        "format": "json",
    })
    r.raise_for_status()
    results = r.json().get("search", [])
    if not results:
        return None
    return results[0]["id"]


def resolve_claims(item: dict, session: requests.Session) -> None:
    """Fill missing QIDs in subclass_of and uses by searching production Wikidata.

    Modifies item in-place. Entries that cannot be resolved are removed.
    Always searches production wikidata.org regardless of --sandbox.
    """
    print("→ Resolving QIDs from labels (production wikidata.org)...")
    for field in ("subclass_of", "uses"):
        resolved = []
        for entry in item.get(field, []):
            label = entry.get("label", "")
            if not label or "FILL_ME_IN" in label:
                continue
            if entry.get("qid"):
                print(f"  ✓ {label!r} → {entry['qid']} (from YAML)")
                resolved.append(entry)
                continue
            qid = resolve_label_to_qid(label, session)
            if qid:
                print(f"  ✓ {label!r} → {qid} (searched)")
                entry["qid"] = qid
                resolved.append(entry)
            else:
                print(f"  ⚠ {label!r} → not found on Wikidata, skipping")
        item[field] = resolved


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

        # P279 — subclass of
        subclass_statements = [
            {"mainsnak": qid_snak("P279", e["qid"]), "type": "statement", "rank": "normal"}
            for e in item.get("subclass_of", []) if e.get("qid")
        ]
        if subclass_statements:
            statements["P279"] = subclass_statements

        # P2283 — uses
        uses_statements = [
            {"mainsnak": qid_snak("P2283", e["qid"]), "type": "statement", "rank": "normal"}
            for e in item.get("uses", []) if e.get("qid")
        ]
        if uses_statements:
            statements["P2283"] = uses_statements

        # P856 — official website
        website = item.get("official_website", "").strip()
        if website:
            statements["P856"] = [{
                "mainsnak": url_snak("P856", website),
                "type": "statement",
                "rank": "preferred",
            }]

        data["claims"] = statements

    return data


def _extract_qid_from_conflict(error: dict) -> Optional[str]:
    """Return existing QID from a label-with-description-conflict error, or None."""
    for msg in error.get("messages", []):
        if msg.get("name") == "wikibase-validator-label-with-description-conflict":
            params = msg.get("parameters", [])
            if len(params) >= 3:
                m = re.search(r"\[\[(\w+)\|", str(params[2]))
                if m:
                    return m.group(1)
    return None


def _is_missing_property_error(error: dict) -> bool:
    """Return True when the API rejects because a property (P-id) doesn't exist on this wiki."""
    for msg in error.get("messages", []):
        if msg.get("name") == "wikibase-validator-no-such-property":
            return True
    return False


def create_item(session: requests.Session, data: dict, csrf_token: str, label: str):
    """Create a new item. Returns (qid, already_existed: bool).

    If claims reference properties absent from this wiki (common in sandbox),
    the request is retried without claims so the base item is still created.
    """
    r = session.post(API_URL, data={
        "action": "wbeditentity",
        "new": "item",
        "data": json.dumps(data),
        "token": csrf_token,
        "format": "json",
        "summary": f"Creating item '{label}' via wikidata_add_item.py v2",
    })
    r.raise_for_status()
    result = r.json()
    if "error" in result:
        error = result["error"]

        existing_qid = _extract_qid_from_conflict(error)
        if existing_qid:
            print(f"⚠ Item already exists as {existing_qid} — will patch claims onto it.")
            return existing_qid, True

        if _is_missing_property_error(error):
            missing = [
                p.get("parameters", ["?"])[0]
                for p in error.get("messages", [])
                if p.get("name") == "wikibase-validator-no-such-property"
            ]
            print(f"⚠ Property not found on this wiki ({', '.join(missing)}) — retrying without claims.")
            data_no_claims = {k: v for k, v in data.items() if k != "claims"}
            return create_item(session, data_no_claims, csrf_token, label)

        raise RuntimeError(f"API error: {error}")
    return result["entity"]["id"], False


def patch_item_claims(session: requests.Session, qid: str, claims: dict,
                      csrf_token: str, label: str) -> None:
    """Merge claims into an existing item (wbeditentity with id, not new)."""
    r = session.post(API_URL, data={
        "action": "wbeditentity",
        "id": qid,
        "data": json.dumps({"claims": claims}),
        "token": csrf_token,
        "format": "json",
        "summary": f"Adding claims to '{label}' via wikidata_add_item.py v2",
    })
    r.raise_for_status()
    result = r.json()
    if "error" in result:
        error = result["error"]
        if _is_missing_property_error(error):
            missing = [
                p.get("parameters", ["?"])[0]
                for p in error.get("messages", [])
                if p.get("name") == "wikibase-validator-no-such-property"
            ]
            print(f"⚠ Cannot add claims — properties missing on this wiki: {', '.join(missing)}")
            return
        raise RuntimeError(f"API error patching claims: {error}")
    print(f"✓ Claims patched onto {qid}")


def print_claims_summary(item: dict) -> None:
    print("\nSubclass of (P279):")
    for e in item.get("subclass_of", []):
        print(f"  {e.get('qid', '???'):12}  {e.get('label', '')}")
    print("\nUses (P2283):")
    for e in item.get("uses", []):
        print(f"  {e.get('qid', '???'):12}  {e.get('label', '')}")
    website = item.get("official_website", "").strip()
    if website:
        print(f"\nOfficial website (P856): {website}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    global API_URL, USERNAME, PASSWORD

    parser = argparse.ArgumentParser(
        description="Create a new Wikidata item from a YAML file in data/. "
                    "v2: claims are attempted in sandbox mode too."
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
        help="Write to test.wikidata.org instead of production (uses WD_TEST_* credentials). "
             "Claims are included unless --no-claims is also passed."
    )
    parser.add_argument(
        "--no-claims", action="store_true",
        help="Skip statements/claims (label + description + aliases only). "
             "Useful when testing on sandbox if properties are not available there."
    )
    args = parser.parse_args()

    if args.sandbox:
        API_URL  = SANDBOX_API_URL
        USERNAME = WD_TEST_USERNAME
        PASSWORD = WD_TEST_PASSWORD
        wiki_base = "https://test.wikidata.org/wiki"
        print("⚠ SANDBOX MODE — writing to test.wikidata.org")
        if not args.no_claims:
            print("ℹ Claims will be attempted (use --no-claims to skip if properties are missing)")
    else:
        wiki_base = "https://www.wikidata.org/wiki"

    item_path = resolve_item_path(args.item)
    print(f"→ Loading item from: {item_path.name}")
    item = load_item(item_path)

    no_claims = args.no_claims

    if not no_claims:
        search_session = get_session()
        resolve_claims(item, search_session)

    item_data = build_item_data(item, no_claims=no_claims)

    if args.dry_run:
        target = "test.wikidata.org" if args.sandbox else "www.wikidata.org"
        suffix = " (no claims)" if no_claims else " (with claims)"
        print(f"=== DRY RUN — payload that would be sent to {target}{suffix} ===")
        print(json.dumps(item_data, indent=2, ensure_ascii=False))
        if not no_claims:
            print_claims_summary(item)
        return

    check_credentials(args.sandbox)
    session = get_session()
    login(session)
    csrf_token = get_csrf_token(session)
    print("✓ CSRF token obtained")

    new_qid, already_existed = create_item(session, item_data, csrf_token, item["label_en"])

    # If item existed, patch claims now (creation skipped claims to avoid conflict error)
    claims_patched = False
    if already_existed and not no_claims and item_data.get("claims"):
        patch_item_claims(session, new_qid, item_data["claims"], csrf_token, item["label_en"])
        claims_patched = True

    url = f"{wiki_base}/{new_qid}"
    bar = "━" * 40
    print(f"\n{bar}")
    print(f"  Item : {item['label_en']}")
    print(f"  QID  : {new_qid}")
    print(f"  URL  : {url}")
    if not no_claims:
        claimed = []
        if item.get("subclass_of"):
            claimed.append(f"P279 ×{len(item['subclass_of'])}")
        if item.get("uses"):
            claimed.append(f"P2283 ×{len(item['uses'])}")
        if item.get("official_website", "").strip():
            claimed.append("P856")
        if claimed:
            action = "patched" if claims_patched else "created"
            print(f"  Claims ({action}): {', '.join(claimed)}")
    print(bar)


if __name__ == "__main__":
    main()
