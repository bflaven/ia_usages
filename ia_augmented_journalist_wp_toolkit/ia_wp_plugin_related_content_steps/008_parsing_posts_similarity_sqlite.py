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
python 008_parsing_posts_similarity_sqlite.py


"""

"""
POINT_6 - Similarity + SQLite storage.

File: 008_parsing_posts_similarity_sqlite.py

This module:
- Loads WP posts and computes embeddings (reuses the POINT_5 config shape).
- Computes cosine similarity between all posts.
- For each post_id, selects top-K related posts (by similarity).
- Stores embeddings and relations in a temporary SQLite database.

Run:
    conda activate tags_treatment
    python 008_parsing_posts_similarity_sqlite.py

Env overrides (optional), same as POINT_5:
    export WP_JSON_PATH="sample_posts_2020_to_2025.json"
    export EMBEDDING_MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
    export EMBEDDING_BATCH_SIZE="32"
    export EMBEDDING_MAX_CHARS="4000"
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
# Config (same spirit as POINT_5)
# --------------------------------------------------------------------

@dataclass
class EmbeddingConfig:
    wp_json_path: Path = Path("sample_posts_2020_to_2025.json")
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32
    max_chars: int = 4000
    include_slug: bool = False
    normalize_embeddings: bool = True
    sqlite_path: Path = Path("related_posts_embeddings.sqlite")
    top_k: int = 5  # number of related posts per anchor

    @classmethod
    def from_env(cls) -> "EmbeddingConfig":
        wp_json_path = Path(os.getenv("WP_JSON_PATH", "sample_posts_2020_to_2025.json"))

        embedding_model_name = os.getenv(
            "EMBEDDING_MODEL_NAME",
            "sentence-transformers/all-MiniLM-L6-v2",
        )

        batch_size_str = os.getenv("EMBEDDING_BATCH_SIZE", "32")
        try:
            batch_size = int(batch_size_str)
        except ValueError:
            batch_size = 32

        max_chars_str = os.getenv("EMBEDDING_MAX_CHARS", "4000")
        try:
            max_chars = int(max_chars_str)
        except ValueError:
            max_chars = 4000

        include_slug_str = os.getenv("EMBEDDING_INCLUDE_SLUG", "false").lower()
        include_slug = include_slug_str in {"1", "true", "yes"}

        normalize_str = os.getenv("EMBEDDING_NORMALIZE", "true").lower()
        normalize_embeddings = normalize_str in {"1", "true", "yes"}

        # CAUTION : SQLITE_FLE e.g related_posts_embeddings_youtube_1
        sqlite_path = Path(os.getenv("EMBEDDING_SQLITE_PATH", "related_posts_embeddings_youtube_1.sqlite"))

        top_k_str = os.getenv("RELATED_TOP_K", "5")
        try:
            top_k = int(top_k_str)
        except ValueError:
            top_k = 5

        return cls(
            wp_json_path=wp_json_path,
            embedding_model_name=embedding_model_name,
            batch_size=batch_size,
            max_chars=max_chars,
            include_slug=include_slug,
            normalize_embeddings=normalize_embeddings,
            sqlite_path=sqlite_path,
            top_k=top_k,
        )


# --------------------------------------------------------------------
# ParsedPost & JSON loading (from POINT_5)
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
# Pre-processing and model (POINT_1 + POINT_2)
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
# Batching and embedding (POINT_4)
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
# Similarity computation (cosine via dot product on normalized embeddings)
# --------------------------------------------------------------------

def compute_similarity_top_k(
    embeddings: List[PostEmbedding],
    top_k: int,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    """
    Given:
        embeddings: list of (post_id, embedding_vector)
    Returns:
        list of (post_id, [(related_post_id, similarity), ...]) with up to top_k entries
    """
    if not embeddings:
        return []

    post_ids = [pid for pid, _ in embeddings]
    mat = np.asarray([vec for _, vec in embeddings], dtype=float)  # (N, D)

    # Normalize rows to unit length so dot product == cosine similarity. [web:121][web:122]
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    mat_norm = mat / norms

    # Cosine similarity matrix: (N, N)
    sim_matrix = mat_norm @ mat_norm.T  # [web:113][web:121]

    n = sim_matrix.shape[0]
    all_results: List[Tuple[int, List[Tuple[int, float]]]] = []

    for i in range(n):
        # Exclude self similarity by setting it to -inf
        sim_matrix[i, i] = -np.inf

        # Get indices of top_k highest similarities
        # argsort returns ascending; we take the last top_k and reverse. [web:115][web:126]
        idx = np.argsort(sim_matrix[i])[-top_k:][::-1]

        related: List[Tuple[int, float]] = []
        for j in idx:
            rel_post_id = post_ids[j]
            score = float(sim_matrix[i, j])
            # Optional: skip negative similarities
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
# Main runner
# --------------------------------------------------------------------

def main() -> None:
    config = EmbeddingConfig.from_env()
    logger.info("Effective configuration: %s", config)

    posts = load_posts_from_json(config.wp_json_path)
    embeddings = embed_posts_batched(posts, config)

    # Compute top-K similarities
    related_by_post = compute_similarity_top_k(embeddings, top_k=config.top_k)

    # Init SQLite and store
    conn = init_sqlite(config.sqlite_path)
    try:
        store_embeddings(conn, embeddings)
        store_related(conn, related_by_post)
    finally:
        conn.close()

    # Sanity check: print first 2 anchors and their related IDs
    for post_id, related in related_by_post[:2]:
        logger.info(
            "Post %s related -> %s",
            post_id,
            [(rid, f"{score:.3f}") for rid, score in related],
        )


if __name__ == "__main__":
    main()





