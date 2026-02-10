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
python 010_parsing_posts_similarity_sqlite_export_sqlite_csv.py


"""

"""
POINT_6 helper - Recompute similarity, store in SQLite, export to CSV.

File: 010_parsing_posts_similarity_sqlite_export_sqlite_csv.py

This script:
1. Loads WP posts from JSON.
2. Builds embeddings with sentence-transformers.
3. Computes cosine similarity between posts, keeps top-K per post
   with a similarity threshold.
4. Stores results in a SQLite database (post_embeddings + post_related).
5. Exports post_related to a CSV: post_id, related_post_id, similarity, rank.

This CSV can then be imported into the WP plugin's MySQL table.
"""

import csv
import json
import logging
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
# CONFIGURATION - edit as needed
# --------------------------------------------------------------------

@dataclass
class EmbeddingConfig:
    # Input WP JSON (same file you used for previous scripts)
    wp_json_path: Path = Path("sample_posts_2020_to_2025.json")

    # Embedding
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32
    max_chars: int = 4000
    include_slug: bool = False
    normalize_embeddings: bool = True

    # SQLite DB for intermediate storage
    # CAUTION : SQLITE_FLE e.g related_posts_embeddings_settings_csv_youtube_1
    sqlite_path: Path = Path("related_posts_embeddings_settings_csv.sqlite")


    # Similarity settings
    post_number_against: int = 10    # top-K per post
    threshold_for_similarity: float = 0.40  # minimum cosine similarity

    # CSV output
    # CAUTION : SQLITE_FLE e.g related_posts_embeddings_settings_csv_youtube_1
    csv_output_path: Path = Path("related_posts_embeddings_settings_csv_youtube_1.csv")


# --------------------------------------------------------------------
# Data model & JSON loading
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
# Pre-processing
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


# --------------------------------------------------------------------
# Embeddings with batching
# --------------------------------------------------------------------

_model: Optional[SentenceTransformer] = None


def get_embedding_model(model_name: str) -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
    return _model


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
# Similarity computation
# --------------------------------------------------------------------

def compute_similarity_top_k(
    embeddings: List[PostEmbedding],
    top_k: int,
    similarity_threshold: float,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    """
    Returns:
        list of (post_id, [(related_post_id, similarity), ...])
    """
    if not embeddings:
        return []

    post_ids = [pid for pid, _ in embeddings]
    mat = np.asarray([vec for _, vec in embeddings], dtype=float)  # (N, D)

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
        sim_matrix[i, i] = -np.inf

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
# SQLite storage for post_embeddings + post_related
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
# CSV export from SQLite
# --------------------------------------------------------------------

def export_post_related_to_csv(
    conn: sqlite3.Connection,
    csv_path: Path,
) -> None:
    logger.info("Exporting post_related to CSV at %s", csv_path)

    cur = conn.cursor()
    cur.execute(
        """
        SELECT post_id, related_post_id, similarity, rank
        FROM post_related
        ORDER BY post_id ASC, rank ASC
        """
    )
    rows = cur.fetchall()

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["post_id", "related_post_id", "similarity", "rank"])
        for row in rows:
            writer.writerow(row)

    logger.info("Exported %d rows to %s", len(rows), csv_path)


# --------------------------------------------------------------------
# Main pipeline
# --------------------------------------------------------------------

def main() -> None:
    config = EmbeddingConfig()
    logger.info("Effective configuration: %s", config)

    # 1. Load posts
    posts = load_posts_from_json(config.wp_json_path)

    # 2. Embed posts
    embeddings = embed_posts_batched(posts, config)

    # 3. Compute similarity
    related_by_post = compute_similarity_top_k(
        embeddings,
        top_k=config.post_number_against,
        similarity_threshold=config.threshold_for_similarity,
    )

    # 4. Store in SQLite
    conn = init_sqlite(config.sqlite_path)
    try:
        store_embeddings(conn, embeddings)
        store_related(conn, related_by_post)

        # 5. Export post_related to CSV
        export_post_related_to_csv(conn, config.csv_output_path)
    finally:
        conn.close()

    logger.info("Done. CSV ready at %s", config.csv_output_path)


if __name__ == "__main__":
    main()




