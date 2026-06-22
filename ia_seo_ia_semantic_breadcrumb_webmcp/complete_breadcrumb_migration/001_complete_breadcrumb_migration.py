"""
001_complete_breadcrumb_migration.py
Version: 1.0.0

Fill empty `actual_description` fields in breadcrumb migration JSON
using Azure OpenAI. Outputs full JSON with all items to destination/.

[env]
conda activate ia_achats

[path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_seo_ia_semantic_breadcrumb_webmcp/complete_breadcrumb_migration/
python 001_complete_breadcrumb_migration.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI


# ============================================================================
# CONFIG
# ============================================================================

class CONFIG:
    MODEL       = "gpt-4.1-mini"
    TEMPERATURE = 0.3
    STREAMING   = False
    TIMEOUT     = 30
    MAX_TOKENS  = None

    SOURCE_FILE = Path("source/breadcrumb_migration_bulk_description_20260622_145542.json")
    DEST_DIR    = Path("destination")
    DEST_BASE   = "breadcrumb_migration_bulk_description_20260622_145542.json"


# ============================================================================
# AZURE CLIENT
# ============================================================================

class AzureClient:

    @staticmethod
    def AzureEurModel(
        model: str,
        temperature: float = 0.7,
        streaming: bool = False,
        timeout: int = 30,
        max_tokens: int = None,
    ) -> AzureChatOpenAI:
        load_dotenv(Path(__file__).resolve().parent / ".env")

        azure_endpoint = os.getenv("ENDPOINT")
        api_key        = os.getenv("API_KEY")

        if not azure_endpoint or not api_key:
            raise RuntimeError("ENDPOINT or API_KEY missing in .env")

        kwargs = dict(
            azure_endpoint   = azure_endpoint,
            api_key          = api_key,
            api_version      = "2024-05-01-preview",
            azure_deployment = model,
            temperature      = temperature,
            streaming        = streaming,
            timeout          = timeout,
        )
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        return AzureChatOpenAI(**kwargs)


# ============================================================================
# PROMPT
# ============================================================================

SYSTEM_PROMPT = (
    "You are a concise encyclopedia writer. "
    "Write short, factual descriptions in the style of Wikidata or Wikipedia infoboxes. "
    "Return ONLY the description text — no quotes, no preamble, no punctuation at the end unless it ends a sentence."
)

def build_description_prompt(tag_name: str) -> str:
    return (
        f"Write a short English description for \"{tag_name}\" "
        f"suitable as a Wikidata entity description. "
        f"Maximum 2 sentences. Be factual and neutral. "
        f"Do not start with the tag name itself as the first word."
    )


# ============================================================================
# HELPERS
# ============================================================================

def load_source(path: Path) -> list:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_empty_items(data: list) -> list:
    return [item for item in data if item.get("actual_description", "") == ""]


def print_banner(empty_count: int, total: int) -> None:
    print("=" * 70)
    print("001_complete_breadcrumb_migration.py — fill empty descriptions")
    print(f"   Model      : {CONFIG.MODEL}")
    print(f"   Source     : {CONFIG.SOURCE_FILE}")
    print(f"   Total items: {total}")
    print(f"   Empty      : {empty_count}")
    print("=" * 70)


def generate_description(llm: AzureChatOpenAI, tag_name: str) -> str:
    messages = [
        ("system", SYSTEM_PROMPT),
        ("user",   build_description_prompt(tag_name)),
    ]
    response = llm.invoke(messages)
    return response.content.strip()


def dest_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    CONFIG.DEST_DIR.mkdir(exist_ok=True)
    return CONFIG.DEST_DIR / f"filed_{timestamp}_{CONFIG.DEST_BASE}"


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    data = load_source(CONFIG.SOURCE_FILE)
    empty_items = find_empty_items(data)

    print_banner(len(empty_items), len(data))

    print(f"\nItems with empty actual_description ({len(empty_items)}):")
    for item in empty_items:
        print(f"  - {item['tag_name']}")

    if not empty_items:
        print("\nNothing to fill. Exit.")
        return

    llm = AzureClient.AzureEurModel(
        model       = CONFIG.MODEL,
        temperature = CONFIG.TEMPERATURE,
        streaming   = CONFIG.STREAMING,
        timeout     = CONFIG.TIMEOUT,
        max_tokens  = CONFIG.MAX_TOKENS,
    )

    print("\nGenerating descriptions...")
    print("-" * 70)

    # Build index for in-place update
    data_index = {item["wp_term_id"]: item for item in data}

    for item in empty_items:
        tag = item["tag_name"]
        print(f"  [{tag}] ...", end=" ", flush=True)
        try:
            desc = generate_description(llm, tag)
            data_index[item["wp_term_id"]]["actual_description"] = desc
            print(f"OK -> {desc[:80]}{'...' if len(desc) > 80 else ''}")
        except Exception as e:
            print(f"ERROR: {e}")

    out_path = dest_path()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(list(data_index.values()), f, ensure_ascii=False, indent=2)

    print("-" * 70)
    print(f"\nOutput written -> {out_path}")
    print(f"Items filled   : {len(empty_items)}")
    print(f"Total items    : {len(data)}")


if __name__ == "__main__":
    main()
