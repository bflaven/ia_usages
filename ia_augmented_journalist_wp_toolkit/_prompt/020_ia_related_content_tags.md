
## PROMPT_1

Let's code the solution 1 that you advise.
```text
Solution 1 – Python pipeline (technical)
```
1. Here are the filenames that I want to take into account with all the advice that I have already given for the posts similarity POC.
The source for tags, it is a local file: `sample_light_tags_20260125_130601.json`
The script python that will do the job: `001_parsing_tags_similarity_sqlite_export_sqlite_csv.py`
The database: `related_tags_embeddings_settings_csv.sqlite`
The output of the db in csv format: `related_tags_embeddings_settings_csv_1.csv`
Feel free to add explanation in the code like comments to simplify understanding and to add variables where I can easily update the configuration inside the script at the head of the script.
2. I will use the same anaconda environment `tags_treatment`
3. At the end, make a shortlist of the steps so I can follow your thinking.
4. The objective is to create a plugin in WP that will be installed and installed in a blog in production but that will be on the second time but bear it in mind.



## OUTPUT_1

Yes, you can implement Solution 1 with essentially the same structure as your posts POC, but at tag level and with clustering on tag labels.

Below is a complete `001_parsing_tags_similarity_sqlite_export_sqlite_csv.py` that:

- Reads tags from `sample_light_tags_20260125_130601.json`.  
- Embeds tag labels with a multilingual SentenceTransformer.  
- Computes pairwise similarity and (for now) keeps the **top‑K similar tags per tag** (same pattern as posts), storing them in SQLite.  
- Exports `tag_related` from SQLite to `related_tags_embeddings_settings_csv_1.csv` with columns: `tag_id, related_tag_id, similarity, rank`.

You can later evolve this into true clustering (DBSCAN/HDBSCAN) but this gives you a working, inspectable CSV very quickly. [github](https://github.com/suraj5424/Text-Clustering-with-Sentence-Transformers)

***

## 1. Script: `001_parsing_tags_similarity_sqlite_export_sqlite_csv.py`

```python
"""
POINT_TAGS - Similarity + SQLite storage + CSV export for tags.

File: 001_parsing_tags_similarity_sqlite_export_sqlite_csv.py

This script:

1. Loads tags from a JSON file.
2. Builds multilingual embeddings for each tag label.
3. Computes cosine similarity between tags and keeps top-K
   similar tags per tag, above a similarity threshold.
4. Stores results in a SQLite database:
   - tag_embeddings (one row per tag)
   - tag_related (tag_id -> related_tag_id + similarity + rank)
5. Exports tag_related to a CSV file suitable for import
   into a WordPress plugin.

You can run it in your existing conda env:

    conda activate tags_treatment
    python 001_parsing_tags_similarity_sqlite_export_sqlite_csv.py

Configuration knobs are grouped in the TagEmbeddingConfig dataclass
near the top of this file.
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
    Edit these values in-place as needed.
    """

    # Input JSON containing tags.
    # Expected basic structure: list of objects with at least:
    #   - id (int)
    #   - name or label (str)
    # Optionally:
    #   - usage_count (int)
    #   - language (str)
    tags_json_path: Path = Path("sample_light_tags_20260125_130601.json")

    # SentenceTransformer model (multilingual recommended).
    # Good default:
    #   paraphrase-multilingual-mpnet-base-v2
    # See: https://www.sbert.net/docs/pretrained_models.html
    embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    # Embedding batch size (adjust if you hit memory limits).
    batch_size: int = 64

    # Whether to lowercase labels before embedding.
    lowercase_labels: bool = True

    # Whether to strip non-alphanumeric characters (simple normalization).
    basic_cleaning: bool = True

    # Normalize embeddings so cosine similarity becomes dot product.
    normalize_embeddings: bool = True

    # SQLite DB for intermediate storage.
    sqlite_path: Path = Path("related_tags_embeddings_settings_csv.sqlite")

    # Similarity settings: top-K related tags, threshold.
    top_k_related: int = 10
    similarity_threshold: float = 0.40

    # CSV output for tag_related.
    csv_output_path: Path = Path("related_tags_embeddings_settings_csv_1.csv")


# --------------------------------------------------------------------
# Data model & JSON loading
# --------------------------------------------------------------------

@dataclass
class ParsedTag:
    id: int
    label: str
    usage_count: Optional[int] = None
    language: Optional[str] = None


def load_tags_from_json(path: Path) -> List[ParsedTag]:
    """
    Load tags from a JSON file.

    Expected JSON structure (flexible, minimal example):

    [
      {
        "id": 123,
        "name": "Olympics",
        "count": 42,
        "lang": "en"
      },
      ...
    ]

    This loader tries a few common field names and degrades gracefully.
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

        # id
        if "id" not in item:
            continue

        tag_id = int(item["id"])

        # label / name
        label = (
            item.get("label")
            or item.get("name")
            or item.get("slug")
            or str(tag_id)
        )
        label = str(label)

        # usage_count
        usage_count = None
        for key in ("usage_count", "count", "posts", "term_group"):
            if key in item:
                try:
                    usage_count = int(item[key])
                    break
                except (TypeError, ValueError):
                    usage_count = None

        # language
        language = None
        for key in ("language", "lang", "locale"):
            if key in item:
                language = str(item[key])
                break

        tags.append(
            ParsedTag(
                id=tag_id,
                label=label,
                usage_count=usage_count,
                language=language,
            )
        )

    logger.info("Loaded %d tags", len(tags))
    return tags


# --------------------------------------------------------------------
# Pre-processing
# --------------------------------------------------------------------

_NON_ALNUM_RE = re.compile(r"[^0-9a-zA-ZÀ-ÖØ-öø-ÿ]+", re.UNICODE)


def clean_tag_label(label: str, lowercase: bool = True, basic_cleaning: bool = True) -> str:
    """
    Basic tag label normalization.

    - Optional lowercasing.
    - Optional removal of non-alphanumeric characters
      (but keeps accented Latin characters).
    """
    text = label.strip()

    if lowercase:
        text = text.lower()

    if basic_cleaning:
        text = _NON_ALNUM_RE.sub(" ", text)

    # Collapse whitespace.
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
    Build embeddings for tag labels, with simple normalization.
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
```

***

## 2. How to run it in `tags_treatment`

From your project root:

```bash
conda activate tags_treatment
python 001_parsing_tags_similarity_sqlite_export_sqlite_csv.py
```

You should get:

- `related_tags_embeddings_settings_csv.sqlite` with tables:
  - `tag_embeddings`
  - `tag_related`  
- `related_tags_embeddings_settings_csv_1.csv` with columns:
  - `tag_id, related_tag_id, similarity, rank` [blog.pesky](https://blog.pesky.moe/posts/2024-08-05-sqlite-csv/)

***

## 3. Shortlist of steps (mental model)

1. **Input**  
   - Take `sample_light_tags_20260125_130601.json`.  
   - Parse into `ParsedTag(id, label, usage_count, language)`.

2. **Pre‑processing**  
   - Normalize label (lowercase, remove non‑alnum, collapse spaces).

3. **Embeddings**  
   - Load `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`. [dataloop](https://dataloop.ai/library/model/sentence-transformers_paraphrase-multilingual-mpnet-base-v2/)
   - Batch‑encode all labels into vectors, optionally normalized.

4. **Similarity**  
   - Build similarity matrix with cosine similarity. [milvus](https://milvus.io/ai-quick-reference/how-can-one-use-sentence-transformers-for-clustering-sentences-or-documents-by-topic-or-content-similarity)
   - For each tag:
     - exclude self,  
     - take top‑K neighbours,  
     - filter by `similarity_threshold`.

5. **Persist**  
   - Write embeddings and relations into SQLite.  
   - Export `tag_related` into a CSV with the canonical schema you need for the future WP plugin.

6. **Next phase (later)**  
   - Add clustering/HDBSCAN on embeddings to define families.  
   - Add entity type info (from NER) and usage_count to choose canonical tags.  
   - Build the WordPress plugin that imports `related_tags_embeddings_settings_csv_1.csv` into a custom table and exposes it in tag edit screens and front‑end templates.



## OUTPUT_1




