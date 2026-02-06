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
pip install -U sentence-transformers
python -m pip install -U sentence-transformers



# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_related_content_steps

# launch the file
python 009_parsing_posts_similarity_sqlite_settings.py


"""

"""
POINT_6 - Similarity + SQLite storage with in-script settings.

File: 009_parsing_posts_similarity_sqlite_settings.py

- post_number_against: how many related posts (max) per anchor post.
- threshold_for_similarity: minimum cosine similarity (0–1) to keep a relation.

Edit these two values in the EmbeddingConfig dataclass below.
"""

import json
import logging
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import html
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
# Configuration (edit here)
# --------------------------------------------------------------------

@dataclass
class EmbeddingConfig:
    wp_json_path: Path = Path("sample_posts_2020_to_2025.json")

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32
    max_chars: int = 4000
    include_slug: bool = False
    normalize_embeddings: bool = True

    sqlite_path: Path = Path("related_posts_embeddings_settings.sqlite")

    # EDIT HERE: how many related posts per anchor (top-K)
    post_number_against: int = 10

    # EDIT HERE: minimum cosine similarity to keep a relation
    threshold_for_similarity: float = 0.40


# --------------------------------------------------------------------
# ParsedPost & JSON loading
# --------------------------------------------------------------------

@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


def load_posts_from_json(path: Path) -> List[ParsedPost]:
    logger.info("Loading posts from JSON: %s", path)

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    def get_nested(mapping, path_seq, default=None):
        current = mapping
        for key in path_seq:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current

    posts: List[ParsedPost] = []
    for item in raw:
        posts.append(
            ParsedPost(
                id=int(item["id"]),
                title_rendered=str(get_nested(item, ["title", "rendered"], "")),
                content=str(get_nested(item, ["content", "rendered"], "")),
                slug=str(get_nested(item, ["slug"], "")),
            )
        )

    logger.info("Loaded %d posts", len(posts))
    return posts


# --------------------------------------------------------------------
# Pre-processing + model
# --------------------------------------------------------------------

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def strip_html_tags(text: str) -> str:
    unescaped = html.unescape(text)
    return _HTML_TAG_RE.sub("", unescaped)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_post_text(
    post: ParsedPost,
    max_chars: Optional[int] = None,
    include_slug: bool = False,
) -> str:
    title = normalize_whitespace(post.title_rendered)
    content_raw = post.content or ""
    content_clean = normalize_whitespace(strip_html_tags(content_raw))

    parts: List[str] = []

    if title:
        parts.append(f"TITLE: {title}")

    if content_clean:
        parts.append(f"CONTENT: {content_clean}")

    if include_slug and post.slug:
        parts.append(f"SLUG: {post.slug}")

    full_text = "\n\n".join(parts)

    if max_chars is not None and len(full_text) > max_chars:
        full_text = full_text[:max_chars]

    return full_text


_model: Optional[SentenceTransformer] = None


def get_embedding_model(model_name: str) -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
    return _model


# --------------------------------------------------------------------
# Batching + embeddings
# --------------------------------------------------------------------

def iter_batches(items: Sequence[ParsedPost], batch_size: int):
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    n = len(items)
    for start in range(0, n, batch_size):
        end = start + batch_size
        yield items[start:end]


EmbeddingVector = List[float]
PostEmbedding = Tuple[int, EmbeddingVector]


def embed_posts_batched(
    posts: Sequence[ParsedPost],
    config: EmbeddingConfig,
) -> List[PostEmbedding]:
    if not posts:
        logger.warning("No posts to embed")
        return []

    model = get_embedding_model(config.embedding_model_name)
    results: List[PostEmbedding] = []

    logger.info(
        "Embedding %d posts with batch_size=%d, max_chars=%d, include_slug=%s, normalize=%s",
        len(posts),
        config.batch_size,
        config.max_chars,
        config.include_slug,
        config.normalize_embeddings,
    )

    for batch_posts in iter_batches(posts, config.batch_size):
        texts = [
            build_post_text(
                p,
                max_chars=config.max_chars,
                include_slug=config.include_slug,
            )
            for p in batch_posts
        ]

        embeddings = model.encode(
            texts,
            normalize_embeddings=config.normalize_embeddings,
        )
        emb_arr = np.asarray(embeddings)

        for post, vec in zip(batch_posts, emb_arr):
            results.append((post.id, vec.astype(float).tolist()))

    logger.info("Finished embedding %d posts", len(results))
    return results


# --------------------------------------------------------------------
# Similarity computation using both settings
# --------------------------------------------------------------------

def compute_similarity_top_k(
    embeddings: List[PostEmbedding],
    top_k: int,
    similarity_threshold: float,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    """
    - top_k: maximum number of candidates considered per anchor (post_number_against).
    - similarity_threshold: minimum cosine similarity to keep a relation.
    """
    if not embeddings:
        return []

    post_ids = [pid for pid, _ in embeddings]
    mat = np.asarray([vec for _, vec in embeddings], dtype=float)  # (N, D)

    # Normalize so dot product == cosine similarity. [web:122]
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    mat_norm = mat / norms

    sim_matrix = mat_norm @ mat_norm.T  # (N, N)

    n = sim_matrix.shape[0]
    all_results: List[Tuple[int, List[Tuple[int, float]]]] = []

    logger.info(
        "Computing similarities with top_k=%d, threshold_for_similarity=%.3f",
        top_k,
        similarity_threshold,
    )

    for i in range(n):
        sim_matrix[i, i] = -np.inf  # avoid self-match

        idx = np.argsort(sim_matrix[i])[-top_k:][::-1]

        related: List[Tuple[int, float]] = []
        for j in idx:
            score = float(sim_matrix[i, j])
            if score < similarity_threshold:
                continue
            rel_post_id = post_ids[j]
            related.append((rel_post_id, score))

        all_results.append((post_ids[i], related))

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
        CREATE TABLE IF NOT EXISTS post_embeddings (
            post_id INTEGER PRIMARY KEY,
            embedding_json TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS post_related (
            post_id INTEGER NOT NULL,
            related_post_id INTEGER NOT NULL,
            similarity REAL NOT NULL,
            rank INTEGER NOT NULL,
            PRIMARY KEY (post_id, related_post_id)
        )
        """
    )

    conn.commit()
    return conn


def store_embeddings(conn: sqlite3.Connection, embeddings: List[PostEmbedding]) -> None:
    logger.info("Storing %d embeddings into SQLite", len(embeddings))
    cur = conn.cursor()

    rows = [
        (post_id, json.dumps(vec))
        for post_id, vec in embeddings
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO post_embeddings (post_id, embedding_json)
        VALUES (?, ?)
        """,
        rows,
    )
    conn.commit()


def store_related(
    conn: sqlite3.Connection,
    related_by_post: List[Tuple[int, List[Tuple[int, float]]]],
) -> None:
    logger.info("Storing related posts into SQLite")
    cur = conn.cursor()

    to_insert: List[Tuple[int, int, float, int]] = []

    for post_id, related_list in related_by_post:
        for rank, (rel_id, score) in enumerate(related_list, start=1):
            to_insert.append((post_id, rel_id, score, rank))

    cur.executemany(
        """
        INSERT OR REPLACE INTO post_related (post_id, related_post_id, similarity, rank)
        VALUES (?, ?, ?, ?)
        """,
        to_insert,
    )
    conn.commit()


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main() -> None:
    config = EmbeddingConfig()
    logger.info("Effective configuration: %s", config)

    posts = load_posts_from_json(config.wp_json_path)
    embeddings = embed_posts_batched(posts, config)

    related_by_post = compute_similarity_top_k(
        embeddings,
        top_k=config.post_number_against,
        similarity_threshold=config.threshold_for_similarity,
    )

    conn = init_sqlite(config.sqlite_path)
    try:
        store_embeddings(conn, embeddings)
        store_related(conn, related_by_post)
    finally:
        conn.close()

    # Debug: show first anchor and its related posts
    if related_by_post:
        anchor_id, rels = related_by_post[0]
        logger.info(
            "Anchor %s has %d related posts after filtering (top_k=%d, threshold=%.3f)",
            anchor_id,
            len(rels),
            config.post_number_against,
            config.threshold_for_similarity,
        )
        logger.info(
            "Anchor %s related -> %s",
            anchor_id,
            [(rid, f"{score:.3f}") for rid, score in rels],
        )


if __name__ == "__main__":
    main()



