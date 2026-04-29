"""
Chunker — Step 2 core logic.

Splits document text into overlapping chunks using spaCy sentence boundaries
(French) or a regex fallback (other languages). Applies business rules from
chunking_rules.yaml when enable_business_rules is true.
"""

import re
import logging
from pathlib import Path
from typing import Optional

import yaml

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# spaCy model registry — loaded once per process
# ---------------------------------------------------------------------------

_SPACY_MODELS: dict = {}

# Defaults — overridden at runtime by configure_spacy() from config.yaml
_LANG_TO_MODEL: dict[str, str] = {
    "en": "en_core_web_trf",
    "fr": "fr_dep_news_trf",
}
_FALLBACK_MODEL: str = "en_core_web_md"


def configure_spacy(spacy_cfg: dict) -> None:
    """
    Update the language→model map and fallback from the config.yaml `spacy` block.

    Called once by chunk_all_documents() before processing begins.
    Safe to call multiple times (idempotent — clears the model cache on change).
    """
    global _LANG_TO_MODEL, _FALLBACK_MODEL

    new_models = spacy_cfg.get("models", {})
    new_fallback = spacy_cfg.get("fallback", _FALLBACK_MODEL)

    if new_models != _LANG_TO_MODEL or new_fallback != _FALLBACK_MODEL:
        _LANG_TO_MODEL = {**new_models}
        _FALLBACK_MODEL = new_fallback
        _SPACY_MODELS.clear()   # discard any cached nlp objects for old models
        logger.info(
            "spaCy config updated — models: %s  fallback: %s",
            _LANG_TO_MODEL, _FALLBACK_MODEL,
        )


def _load_spacy(lang: str):
    """
    Return a loaded spaCy nlp object for the given language.
    Falls back to _FALLBACK_MODEL for unknown languages.
    Returns None only if the model cannot be loaded at all.
    """
    model_name = _LANG_TO_MODEL.get(lang, _FALLBACK_MODEL)
    if model_name in _SPACY_MODELS:
        return _SPACY_MODELS[model_name]
    try:
        import spacy
        nlp = spacy.load(model_name, disable=["ner", "parser"])
        nlp.enable_pipe("senter") if nlp.has_pipe("senter") else None
        if not nlp.has_pipe("sentencizer") and not nlp.has_pipe("senter"):
            nlp.add_pipe("sentencizer")
        _SPACY_MODELS[model_name] = nlp
        logger.info("Loaded spaCy model: %s (lang=%s)", model_name, lang)
        return nlp
    except Exception as exc:
        logger.warning("Could not load spaCy model %s: %s — using regex fallback", model_name, exc)
        return None


# ---------------------------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------------------------

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

# spaCy's hard limit is 1 000 000 chars. We stay comfortably below it.
_SPACY_MAX_CHARS = 900_000


def _split_text_for_spacy(text: str) -> list[str]:
    """
    Split a very long text into segments below _SPACY_MAX_CHARS.
    Splits on paragraph boundaries (\n\n) first, then on newlines, then hard-cuts.
    """
    if len(text) <= _SPACY_MAX_CHARS:
        return [text]

    segments: list[str] = []
    # Split on double-newline (paragraph boundary)
    paragraphs = text.split("\n\n")
    current = ""
    for para in paragraphs:
        # A single paragraph itself may be huge — hard-cut it
        if len(para) > _SPACY_MAX_CHARS:
            if current:
                segments.append(current)
                current = ""
            for i in range(0, len(para), _SPACY_MAX_CHARS):
                segments.append(para[i:i + _SPACY_MAX_CHARS])
        elif len(current) + len(para) + 2 > _SPACY_MAX_CHARS:
            if current:
                segments.append(current)
            current = para
        else:
            current = (current + "\n\n" + para) if current else para
    if current:
        segments.append(current)
    return segments


def split_sentences(text: str, lang: str = "en") -> list[str]:
    """
    Split text into sentences.
    Uses spaCy when available; falls back to regex.
    For texts exceeding spaCy's 1M-char limit, processes segments sequentially.
    """
    nlp = _load_spacy(lang)
    if nlp is not None:
        segments = _split_text_for_spacy(text)
        n_seg = len(segments)
        if n_seg > 1:
            logger.info(
                "Text too long for spaCy (%d chars) — split into %d segments",
                len(text), n_seg,
            )
        sentences: list[str] = []
        for seg_idx, seg in enumerate(segments, 1):
            if n_seg > 1:
                logger.info("  spaCy segment [%d/%d] — %d chars", seg_idx, n_seg, len(seg))
            doc = nlp(seg)
            sentences.extend(sent.text.strip() for sent in doc.sents if sent.text.strip())
        return sentences

    # Regex fallback
    sentences = _SENTENCE_SPLIT_RE.split(text)
    return [s.strip() for s in sentences if s.strip()]


# ---------------------------------------------------------------------------
# Token counting (word-based proxy — fast, no tokenizer required)
# ---------------------------------------------------------------------------

def count_tokens(text: str) -> int:
    return len(text.split())


# ---------------------------------------------------------------------------
# Business rules helpers
# ---------------------------------------------------------------------------

def _load_chunking_rules(rules_path: Path) -> dict:
    with open(rules_path) as f:
        return yaml.safe_load(f)


def _match_doc_type(source_file: str, doc_type: str, rule: dict) -> bool:
    """Return True if the document matches a rule's 'match' block."""
    match = rule.get("match", {})
    path_lower = source_file.lower()
    ext = Path(source_file).suffix.lstrip(".").lower()

    if "any_extension" in match:
        if ext not in [e.lower() for e in match["any_extension"]]:
            return False

    if "any_path_contains" in match:
        if not any(k.lower() in path_lower for k in match["any_path_contains"]):
            return False

    if "any_filename_contains" in match:
        fname = Path(source_file).name
        if not any(k in fname for k in match["any_filename_contains"]):
            return False

    return True


def _find_rule(source_file: str, doc_type: str, rules: dict) -> Optional[dict]:
    """Return the first matching document-type rule, or None."""
    for rule in rules.get("document_types", []):
        if _match_doc_type(source_file, doc_type, rule):
            return rule
    return None


def _compile_patterns(patterns: list[dict]) -> list[re.Pattern]:
    compiled = []
    for p in patterns or []:
        try:
            compiled.append(re.compile(p["regex"], re.MULTILINE))
        except re.error as exc:
            logger.warning("Invalid regex '%s': %s", p.get("regex"), exc)
    return compiled


def _should_drop(line: str, drop_patterns: list[re.Pattern]) -> bool:
    return any(p.search(line) for p in drop_patterns)


def _should_keep_with_next(line: str, keep_patterns: list[re.Pattern]) -> bool:
    return any(p.search(line) for p in keep_patterns)


# ---------------------------------------------------------------------------
# Core grouping logic
# ---------------------------------------------------------------------------

def _hard_split_sentence(sent: str, size: int) -> list[str]:
    """
    Hard-split a sentence that exceeds `size` words into word-based segments.
    Called when spaCy returns a paragraph or table block as one 'sentence'.
    """
    words = sent.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]


def _group_sentences_into_chunks(
    sentences: list[str],
    size: int,
    overlap: float,
    min_tokens: int,
    drop_patterns: list[re.Pattern],
    keep_patterns: list[re.Pattern],
) -> list[str]:
    """
    Group sentences into chunks of up to `size` tokens with `overlap` ratio.
    Applies drop/keep-together patterns.
    Oversized sentences (longer than `size` words) are hard-split first.
    """
    overlap_tokens = max(1, int(size * overlap))
    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0

    # Pre-expand any sentence longer than size into word-based sub-segments.
    # This prevents a single table cell or dense paragraph from becoming a
    # chunk that exceeds the embedding model's context window.
    expanded: list[str] = []
    for s in sentences:
        if count_tokens(s) > size:
            logger.debug("Long sentence (%d words) hard-split into %d segments", count_tokens(s), -(-count_tokens(s) // size))
            expanded.extend(_hard_split_sentence(s, size))
        else:
            expanded.append(s)
    sentences = expanded

    for sent in sentences:
        if _should_drop(sent, drop_patterns):
            continue

        sent_tokens = count_tokens(sent)

        if current_tokens + sent_tokens > size and current:
            chunk_text = " ".join(current).strip()
            if count_tokens(chunk_text) >= min_tokens:
                chunks.append(chunk_text)

            # Carry-over: keep last overlap_tokens worth of sentences
            carry: list[str] = []
            carry_tokens = 0
            for s in reversed(current):
                t = count_tokens(s)
                if carry_tokens + t > overlap_tokens:
                    break
                carry.insert(0, s)
                carry_tokens += t
            current = carry
            current_tokens = carry_tokens

        current.append(sent)
        current_tokens += sent_tokens

    # Flush remainder
    if current:
        chunk_text = " ".join(current).strip()
        if count_tokens(chunk_text) >= min_tokens:
            chunks.append(chunk_text)

    return chunks


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def chunk_document(
    doc: dict,
    chunk_size: int,
    chunk_overlap: float,
    min_tokens: int,
    drop_patterns: list[re.Pattern],
    keep_patterns: list[re.Pattern],
) -> list[dict]:
    """
    Chunk a single document dict and return a list of chunk dicts.
    Each chunk inherits the document's metadata plus chunk_index and tokens.
    """
    lang = doc["metadata"].get("language", "en")
    sentences = split_sentences(doc["text"], lang)

    chunk_texts = _group_sentences_into_chunks(
        sentences,
        size=chunk_size,
        overlap=chunk_overlap,
        min_tokens=min_tokens,
        drop_patterns=drop_patterns,
        keep_patterns=keep_patterns,
    )

    chunks = []
    for i, text in enumerate(chunk_texts):
        chunk = {
            "chunk_id": f"{doc['source']}#chunk_{i}",
            "text": text,
            "source": doc["source"],
            "metadata": {
                **doc["metadata"],
                "chunk_index": i,
                "tokens": count_tokens(text),
            },
        }
        chunks.append(chunk)

    return chunks


def chunk_all_documents(
    documents: list[dict],
    config: dict,
    rules_path: Optional[Path] = None,
) -> list[dict]:
    """
    Chunk all documents according to config and optional business rules.

    Args:
        documents:   output of step 1
        config:      loaded config.yaml dict
        rules_path:  path to chunking_rules.yaml (required if enable_business_rules)

    Returns:
        flat list of chunk dicts
    """
    # Apply spaCy model config from config.yaml if present
    if "spacy" in config:
        configure_spacy(config["spacy"])

    chunking_cfg = config.get("chunking", {})
    default_size = chunking_cfg.get("size", 512)
    default_overlap = chunking_cfg.get("overlap", 0.1)
    default_min = chunking_cfg.get("min_tokens", 50)
    use_rules = chunking_cfg.get("enable_business_rules", False)

    rules = None
    if use_rules and rules_path and rules_path.exists():
        rules = _load_chunking_rules(rules_path)
        logger.info("Business rules loaded from %s", rules_path)
    elif use_rules:
        logger.warning("enable_business_rules=true but rules file not found at %s", rules_path)

    all_chunks: list[dict] = []
    total = len(documents)

    for doc_idx, doc in enumerate(documents, 1):
        source_file = doc["metadata"].get("source_file", doc["source"])
        doc_type = doc["metadata"].get("doc_type", "")
        logger.info(
            "[%d/%d] Chunking: %s (%d chars)",
            doc_idx, total,
            doc["source"][:80],
            len(doc["text"]),
        )

        size = default_size
        overlap = default_overlap
        min_tokens = default_min
        drop_patterns: list[re.Pattern] = []
        keep_patterns: list[re.Pattern] = []

        if rules:
            rule = _find_rule(source_file, doc_type, rules)
            if rule:
                rule_chunking = rule.get("chunking", {})
                size = rule_chunking.get("size", default_size)
                overlap = rule_chunking.get("overlap", default_overlap)
                min_tokens = rules.get("defaults", {}).get("min_tokens", default_min)
                drop_patterns = _compile_patterns(rule.get("drop_patterns", []))
                keep_patterns = _compile_patterns(rule.get("keep_together_patterns", []))
                logger.debug("Applying rule '%s' to %s", rule["id"], source_file)

        chunks = chunk_document(doc, size, overlap, min_tokens, drop_patterns, keep_patterns)
        all_chunks.extend(chunks)

    return all_chunks
