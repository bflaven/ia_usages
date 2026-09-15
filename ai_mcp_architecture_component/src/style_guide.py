"""Shared data access for the newsroom style guide.

Both the legacy REST endpoint (legacy_api.py) and the MCP server
(mcp_server.py) read from this single module, so they can never drift
apart in behavior — by construction, not by discipline. See
docs/03_kpis.md, "Quality / reliability".
"""

from __future__ import annotations

import difflib
import json
from dataclasses import dataclass
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "newsroom_style_guide.json"


@dataclass(frozen=True)
class StyleEntry:
    term: str
    language_pair: str
    approved: str
    note: str
    category: str


def _load_raw() -> dict:
    with DATA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def load_entries() -> list[StyleEntry]:
    raw = _load_raw()
    return [StyleEntry(**entry) for entry in raw["entries"]]


def guide_last_updated() -> str:
    return _load_raw()["updated"]


def lookup_term(term: str, language_pair: str | None = None) -> dict:
    """Look up a term in the style guide.

    Returns a structured result — never a guess. If nothing matches, the
    result explicitly says so and offers the closest known terms, per the
    "unknown term" acceptance criterion in docs/02_user_story.md.
    """
    entries = load_entries()
    term_lower = term.strip().lower()

    candidates = [
        e
        for e in entries
        if e.term.lower() == term_lower
        and (language_pair is None or e.language_pair == language_pair)
    ]

    if candidates:
        entry = candidates[0]
        return {
            "found": True,
            "term": entry.term,
            "language_pair": entry.language_pair,
            "approved": entry.approved,
            "note": entry.note,
            "category": entry.category,
            "guide_last_updated": guide_last_updated(),
        }

    all_terms = [e.term for e in entries]
    suggestions = difflib.get_close_matches(term, all_terms, n=3, cutoff=0.5)

    return {
        "found": False,
        "term": term,
        "suggestions": suggestions,
        "guide_last_updated": guide_last_updated(),
    }


def check_style_rule(text: str) -> dict:
    """Scan free text for any known style-guide terms it contains.

    Deliberately simple substring matching — this POC demonstrates the
    integration pattern (MCP vs. bespoke REST), not a production-grade
    NLP pipeline. A real deployment would reuse the NER/entity pipeline
    already documented on the author's blog (spaCy + Wikidata enrichment).
    """
    entries = load_entries()
    text_lower = text.lower()
    hits = [
        {
            "term": e.term,
            "approved": e.approved,
            "note": e.note,
            "category": e.category,
        }
        for e in entries
        if e.term.lower() in text_lower
    ]
    return {"hits": hits, "checked_terms": len(entries)}
