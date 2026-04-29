#!/usr/bin/env python3
"""
bridge_export.py — Export CMS posts to the RAG bridge exchange file.

Reads:  config/bridge_wp.yaml → bridge.local_source  (overridable with --source)
Writes: config/bridge_wp.yaml → bridge.exchange_file  (overridable with --out)

When wordpress.enabled is false (default), reads from the local JSON file.
When wordpress.enabled is true, fetches from the WP REST API (stub — not yet implemented).

Exchange format: data/bridge/rag_bridge_schema.json
Schema:         data/bridge/rag_schema.sql

Usage:
    python bridge_export.py
    python bridge_export.py --source data/corpora/editorial/CMS_EXPORT_2026_2/my_posts.json
    python bridge_export.py --source data/corpora/editorial/CMS_EXPORT_2026_2/my_posts.json --out data/bridge/rag_bridge.json
    python bridge_export.py --config path/to/bridge_wp.yaml
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

try:
    from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
    import warnings
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
    _BS4 = True
except ImportError:
    _BS4 = False


# ── helpers ───────────────────────────────────────────────────────────────────

def _strip_html(html: str) -> str:
    """Remove HTML tags and decode entities. BeautifulSoup preferred, regex fallback."""
    if not html:
        return ""
    if _BS4:
        return BeautifulSoup(html, "html.parser").get_text(separator=" ").strip()
    import re
    text = re.sub(r"<[^>]+>", " ", html)
    for entity, char in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                          ("&nbsp;", " "), ("&#8217;", "'"), ("&#8220;", '"'),
                          ("&#8221;", '"')]:
        text = text.replace(entity, char)
    return re.sub(r"\s+", " ", text).strip()


def _rendered(field) -> str:
    """Extract .rendered from a WP REST API field object, or return value as-is."""
    if isinstance(field, dict):
        return field.get("rendered", "")
    return str(field) if field else ""


def _truncate_date(dt_str: str) -> str:
    """Truncate an ISO datetime string to YYYY-MM-DD."""
    return dt_str[:10] if dt_str else ""


# ── config ────────────────────────────────────────────────────────────────────

def load_config(config_path: str = "config/bridge_wp.yaml") -> dict:
    path = Path(config_path)
    if not path.exists():
        print(f"[ERROR] Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── normalization ─────────────────────────────────────────────────────────────

def normalize_post(post: dict) -> dict:
    """Convert one WP REST API post object to the exchange format (Option B)."""
    return {
        "id":      post["id"],
        "title":   _strip_html(_rendered(post.get("title", ""))),
        "url":     post.get("link", ""),
        "date":    _truncate_date(post.get("date", "")),
        "slug":    post.get("slug", ""),
        "excerpt": _strip_html(_rendered(post.get("excerpt", ""))),
        "text":    _strip_html(_rendered(post.get("content", ""))),
    }


# ── sources ───────────────────────────────────────────────────────────────────

def export_from_local(source_path: str) -> list[dict]:
    """Read posts from the local JSON file and normalize to exchange format."""
    path = Path(source_path)
    if not path.exists():
        print(f"[ERROR] Local source not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        posts = json.load(f)

    if not isinstance(posts, list):
        print("[ERROR] Expected a JSON array at the top level.", file=sys.stderr)
        sys.exit(1)

    records, skipped = [], 0
    for post in posts:
        if post.get("status") != "publish":
            skipped += 1
            continue
        records.append(normalize_post(post))

    print(f"[export] {len(records)} posts normalized  |  {skipped} skipped (non-publish)")
    return records


def export_from_api(_cfg: dict) -> list[dict]:
    """Fetch posts from the WP REST API.
    Requires wordpress.enabled = true in bridge_wp.yaml.
    Not yet implemented — flip enabled to false to use the local source.
    """
    raise NotImplementedError(
        "WP REST API fetch is not yet implemented. "
        "Set wordpress.enabled: false in config/bridge_wp.yaml "
        "and use the local source file."
    )


# ── output ────────────────────────────────────────────────────────────────────

def write_exchange_file(records: list[dict], output_path: str) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    size_kb = out.stat().st_size // 1024
    print(f"[export] Written → {out}  ({len(records)} records, {size_kb} KB)")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Export CMS posts to RAG bridge exchange file.")
    parser.add_argument("--config", default="config/bridge_wp.yaml",
                        help="Path to bridge_wp.yaml (default: config/bridge_wp.yaml)")
    parser.add_argument("--source", default=None,
                        help="Path to the source JSON file. Overrides bridge.local_source in the config.")
    parser.add_argument("--out", default=None,
                        help="Path for the output rag_bridge.json. Overrides bridge.exchange_file in the config.")
    args = parser.parse_args()

    cfg = load_config(args.config)

    wp_enabled   = cfg.get("wordpress", {}).get("enabled", False)
    local_source = args.source or cfg.get("bridge", {}).get("local_source", "")
    exchange_out = args.out    or cfg.get("bridge", {}).get("exchange_file", "data/bridge/rag_bridge.json")

    print(f"[export] wordpress.enabled = {wp_enabled}")

    if wp_enabled:
        api_url = cfg.get("wordpress", {}).get("api_url", "")
        print(f"[export] Source: WP REST API  →  {api_url}")
        records = export_from_api(cfg)
    else:
        print(f"[export] Source: local file   →  {local_source}")
        records = export_from_local(local_source)

    write_exchange_file(records, exchange_out)
    print(f"[export] Done  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
