"""
[env]
# Conda Environment
conda create --name tags_treatment python=3.9.13
conda info --envs
source activate tags_treatment
conda deactivate


# BURN AFTER READING
source activate tags_treatment



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n tags_treatment

# BURN AFTER READING
conda env remove -n tags_treatment


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install mistralai python-dotenv datauri

python -m pip install mistralai python-dotenv datauri


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_tags/

# launch the file
python 001_parsing_tags_similarity_sqlite_export_sqlite_csv.py


"""
"""
POINT_TAGS - Similarity + SQLite storage + CSV export for tags.

File: 001_parsing_tags_similarity_sqlite_export_sqlite_csv.py

This script:

1. Loads WordPress tags from a JSON export (WP REST /wp/v2/tags).
2. Builds multilingual embeddings for each tag label.
3. Computes cosine similarity between tags and keeps top-K
   similar tags per tag, above a similarity threshold.
4. Stores results in a SQLite database:
   - tag_embeddings (one row per tag)
   - tag_related (tag_id -> related_tag_id + similarity + rank)
5. Exports tag_related to a CSV file for later WordPress import.

Run:

    conda activate tags_treatment
    python 001_parsing_tags_similarity_sqlite_export_sqlite_csv.py
"""

import csv
import json
import logging
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import re

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore[import]


# --------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

@dataclass
class TagEmbeddingConfig:
    """
    Central configuration for the tag similarity pipeline.
    Edit these values as needed.
    """

    # Input JSON: direct export from WP REST /wp/v2/tags
    tags_json_path: Path = Path("sample_all_tags_20260125_130601.json")

    # Multilingual SentenceTransformer model
    embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    # Embedding batch size
    batch_size: int = 64

    # Label normalization
    lowercase_labels: bool = True
    basic_cleaning: bool = True

    # Normalize embeddings for cosine similarity
    normalize_embeddings: bool = True

    # SQLite DB
    sqlite_path: Path = Path("related_tags_embeddings_settings_csv.sqlite")

    # Similarity settings
    top_k_related: int = 10
    similarity_threshold: float = 0.40

    # CSV export path
    csv_output_path: Path = Path("related_tags_embeddings_settings_csv_1.csv")


# --------------------------------------------------------------------
# Data model & JSON loading
# --------------------------------------------------------------------

@dataclass
class ParsedTag:
    id: int
    label: str
    usage_count: Optional[int] = None
    language: Optional[str] = None  # not present in your JSON yet, kept for future use


def load_tags_from_json(path: Path) -> List[ParsedTag]:
    """
    Load tags from a WP /wp/v2/tags JSON export.

    Expected structure (your example):

    [
      {
        "id": 1570,
        "count": 1,
        "description": "",
        "link": "https://flaven.fr/tag/18daysinegypt/",
        "name": "#18DaysInEgypt",
        "slug": "18daysinegypt",
        "taxonomy": "post_tag",
        "meta": [],
        "_links": { ... }
      },
      ...
    ]

    We take:
      - id       -> tag_id
      - name     -> label
      - count    -> usage_count
    """

    logger.info("Loading tags from JSON: %s", path)

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, list):
        raise ValueError("Expected top-level JSON array for tags")

    tags: List[ParsedTag] = []

    for item in raw:
        if not isinstance(item, dict):
            continue

        # id is mandatory in WP tags
        if "id" not in item:
            continue

        tag_id = int(item["id"])

        # name is the human-readable label
        label = str(item.get("name", "")) or str(item.get("slug", tag_id))

        # usage_count from "count"
        usage_count = None
        if "count" in item:
            try:
                usage_count = int(item["count"])
            except (TypeError, ValueError):
                usage_count = None

        # language not present in this JSON; keep None for now
        language = None

        tags.append(
            ParsedTag(
                id=tag_id,
                label=label,
                usage_count=usage_count,
                language=language,
            )
        )

    logger.info("Loaded %d tags", len(tags))
    if tags:
        logger.info("First tag example: id=%s, label=%r, usage_count=%r", tags[0].id, tags[0].label, tags[0].usage_count)
    return tags


# --------------------------------------------------------------------
# Pre-processing
# --------------------------------------------------------------------

# Keep accented Latin letters
_NON_ALNUM_RE = re.compile(r"[^0-9a-zA-ZÀ-ÖØ-öø-ÿ]+", re.UNICODE)


def clean_tag_label(label: str, lowercase: bool = True, basic_cleaning: bool = True) -> str:
    """
    Basic normalization of tag labels:

    - Optional lowercasing
    - Optional removal of non-alphanumeric characters
    - Collapse whitespace
    """
    text = label.strip()

    if lowercase:
        text = text.lower()

    if basic_cleaning:
        text = _NON_ALNUM_RE.sub(" ", text)

    text = re.sub(r"\s+", " ", text).strip()
    return text or label.strip()


# --------------------------------------------------------------------
# Embeddings
# --------------------------------------------------------------------

_model: Optional[SentenceTransformer] = None


def get_embedding_model(model_name: str) -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
    return _model


TagEmbeddingVector = List[float]
TagEmbedding = Tuple[int, TagEmbeddingVector]


def iter_batches(items: Sequence[ParsedTag], batch_size: int):
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    n = len(items)
    for start in range(0, n, batch_size):
        end = start + batch_size
        yield items[start:end]


def embed_tags(
    tags: Sequence[ParsedTag],
    config: TagEmbeddingConfig,
) -> List[TagEmbedding]:
    """
    Build embeddings for tag labels.
    """
    if not tags:
        logger.warning("No tags to embed")
        return []

    model = get_embedding_model(config.embedding_model_name)
    results: List[TagEmbedding] = []

    logger.info(
        "Embedding %d tags with model=%s, batch_size=%d, lowercase=%s, basic_cleaning=%s, normalize=%s",
        len(tags),
        config.embedding_model_name,
        config.batch_size,
        config.lowercase_labels,
        config.basic_cleaning,
        config.normalize_embeddings,
    )

    for batch_tags in iter_batches(tags, config.batch_size):
        texts = [
            clean_tag_label(
                t.label,
                lowercase=config.lowercase_labels,
                basic_cleaning=config.basic_cleaning,
            )
            for t in batch_tags
        ]

        embeddings = model.encode(
            texts,
            normalize_embeddings=config.normalize_embeddings,
        )
        emb_arr = np.asarray(embeddings)

        for tag, vec in zip(batch_tags, emb_arr):
            results.append((tag.id, vec.astype(float).tolist()))

    logger.info("Finished embedding %d tags", len(results))
    return results


# --------------------------------------------------------------------
# Similarity computation
# --------------------------------------------------------------------

def compute_tag_similarity_top_k(
    embeddings: List[TagEmbedding],
    top_k: int,
    similarity_threshold: float,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    """
    Compute cosine similarity between all tags and keep top_k related per tag.

    Returns:
        list of (tag_id, [(related_tag_id, similarity), ...])
    """
    if not embeddings:
        return []

    tag_ids = [tid for tid, _ in embeddings]
    mat = np.asarray([vec for _, vec in embeddings], dtype=float)  # (N, D)

    # Normalize so dot product == cosine similarity
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    mat_norm = mat / norms

    sim_matrix = mat_norm @ mat_norm.T  # (N, N)

    n = sim_matrix.shape[0]
    all_results: List[Tuple[int, List[Tuple[int, float]]]] = []

    logger.info(
        "Computing tag similarities with top_k=%d, similarity_threshold=%.3f",
        top_k,
        similarity_threshold,
    )

    for i in range(n):
        # Avoid self-match
        sim_matrix[i, i] = -np.inf

        # Indices of top_k highest similarities
        idx = np.argsort(sim_matrix[i])[-top_k:][::-1]

        related: List[Tuple[int, float]] = []
        for j in idx:
            score = float(sim_matrix[i, j])
            if score < similarity_threshold:
                continue
            rel_tag_id = tag_ids[j]
            related.append((rel_tag_id, score))

        all_results.append((tag_ids[i], related))

    return all_results


# --------------------------------------------------------------------
# SQLite storage
# --------------------------------------------------------------------

def init_sqlite(db_path: Path) -> sqlite3.Connection:
    logger.info("Initializing SQLite DB at %s", db_path)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_embeddings (
            tag_id INTEGER PRIMARY KEY,
            embedding_json TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_related (
            tag_id INTEGER NOT NULL,
            related_tag_id INTEGER NOT NULL,
            similarity REAL NOT NULL,
            rank INTEGER NOT NULL,
            PRIMARY KEY (tag_id, related_tag_id)
        )
        """
    )

    conn.commit()
    return conn


def store_tag_embeddings(conn: sqlite3.Connection, embeddings: List[TagEmbedding]) -> None:
    logger.info("Storing %d tag embeddings into SQLite", len(embeddings))
    cur = conn.cursor()

    rows = [
        (tag_id, json.dumps(vec))
        for tag_id, vec in embeddings
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO tag_embeddings (tag_id, embedding_json)
        VALUES (?, ?)
        """,
        rows,
    )
    conn.commit()


def store_tag_related(
    conn: sqlite3.Connection,
    related_by_tag: List[Tuple[int, List[Tuple[int, float]]]],
) -> None:
    logger.info("Storing tag_related into SQLite")
    cur = conn.cursor()

    to_insert: List[Tuple[int, int, float, int]] = []

    for tag_id, related_list in related_by_tag:
        for rank, (rel_id, score) in enumerate(related_list, start=1):
            to_insert.append((tag_id, rel_id, score, rank))

    cur.executemany(
        """
        INSERT OR REPLACE INTO tag_related (tag_id, related_tag_id, similarity, rank)
        VALUES (?, ?, ?, ?)
        """,
        to_insert,
    )
    conn.commit()


# --------------------------------------------------------------------
# CSV export from SQLite
# --------------------------------------------------------------------

def export_tag_related_to_csv(
    conn: sqlite3.Connection,
    csv_path: Path,
) -> None:
    logger.info("Exporting tag_related to CSV at %s", csv_path)

    cur = conn.cursor()
    cur.execute(
        """
        SELECT tag_id, related_tag_id, similarity, rank
        FROM tag_related
        ORDER BY tag_id ASC, rank ASC
        """
    )
    rows = cur.fetchall()

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tag_id", "related_tag_id", "similarity", "rank"])
        for row in rows:
            writer.writerow(row)

    logger.info("Exported %d rows to %s", len(rows), csv_path)


# --------------------------------------------------------------------
# Main pipeline
# --------------------------------------------------------------------

def main() -> None:
    config = TagEmbeddingConfig()
    logger.info("Effective configuration: %s", config)

    # 1. Load tags
    tags = load_tags_from_json(config.tags_json_path)
    if not tags:
        logger.warning("No tags loaded; aborting.")
        return

    # 2. Embed tags
    embeddings = embed_tags(tags, config)

    # 3. Compute similarity
    related_by_tag = compute_tag_similarity_top_k(
        embeddings,
        top_k=config.top_k_related,
        similarity_threshold=config.similarity_threshold,
    )

    # 4. Store in SQLite
    conn = init_sqlite(config.sqlite_path)
    try:
        store_tag_embeddings(conn, embeddings)
        store_tag_related(conn, related_by_tag)

        # 5. Export tag_related to CSV
        export_tag_related_to_csv(conn, config.csv_output_path)
    finally:
        conn.close()

    logger.info("Done. CSV ready at %s", config.csv_output_path)


if __name__ == "__main__":
    main()














