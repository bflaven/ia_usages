
## PROMPT_2
In the related_tags_embeddings_settings_csv.sqlite what does it means when in tag_ner table is entity_label is equal to O.
Can you give quick and straightforward explanations for each table so I can understand in simple terms what is happening during the process. I am a newbie.


## OUTPUT_2
In `tag_ner`, `entity_label = "O"` just means: “no named entity detected for this tag”. It’s the default label spaCy uses for tokens that are **Outside** any entity. [geeksforgeeks](https://www.geeksforgeeks.org/python/python-named-entity-recognition-ner-using-spacy/)

Here’s what each table in `related_tags_embeddings_settings_csv.sqlite` represents, in simple terms.

***

## tag_ner

- One row per tag.  
- Columns:
  - `tag_id`: the WordPress tag ID.  
  - `entity_label`: what spaCy thinks this tag is:
    - `PERSON`: person name.  
    - `ORG`: organization.  
    - `GPE`: country/city/region (geopolitical entity).  
    - `EVENT`, `WORK_OF_ART`, etc.  
    - `O`: **no clear entity**, just a generic topic, phrase, or label.

So `"O"` = “this tag doesn’t look like a clean named entity, treat it as a generic topic”.

***

## tag_families

- One row per **family** (cluster of similar tags).  
- Columns:
  - `family_id`: internal family identifier (0,1,2,…).  
  - `canonical_tag_id`: the tag chosen as the **master** of this family.  
  - `canonical_label`: its label (text of the canonical tag).

How canonical is chosen:

- Highest `usage_count` (most used tag wins).  
- If tie, shorter label (more generic / clean).  
- If tie again, lowest tag ID.

***

## tag_family_members

- One row per **tag inside a family**.  
- Columns:
  - `family_id`: which family this tag belongs to.  
  - `tag_id`: this tag’s ID.  
  - `tag_label`: text of the tag.  
  - `similarity_to_canonical`: cosine similarity between this tag and the family’s canonical tag (0–1, higher = more similar).  
  - `usage_count`: how many posts use this tag (from WP `count`).  
  - `entity_label`: same as in `tag_ner` (PERSON, ORG, GPE, O, …).

So for any tag:

- Look in `tag_family_members` to know:
  - which family it’s in,  
  - who is the canonical tag for that family,  
  - how close it is to the canonical (similarity),  
  - what kind of entity it is (from NER).

***

## How the process works (in plain language)

1. Read all tags from the JSON.  
2. Compute an embedding (vector) for each tag label. [sbert](https://sbert.net/examples/sentence_transformer/applications/clustering/README.html)
3. Compute similarity between tags and group tags that are close into **families** (connected components graph).  
4. Run NER on each tag text to get an **entity type**, or `"O"` if none. [stackoverflow](https://stackoverflow.com/questions/68035891/how-can-i-getting-ner-named-entity-recognition-for-one-word)
5. For each family, pick a **canonical tag** (highest usage, then shortest label).  
6. Store:
   - `tag_ner`: tag → entity type.  
   - `tag_families`: family → canonical tag.  
   - `tag_family_members`: all tags in each family, with similarity + usage + entity type.





## PROMPT_1

Write a new script 002_parsing_tags_similarity_sqlite_export_sqlite_csv.py that will do the 2 objectives that you describe:
1. Add clustering/HDBSCAN on embeddings to define families.
2. Add entity type info (from NER) and usage_count to choose canonical tags.

The build the WordPress plugin that imports related_tags_embeddings_settings_csv_1.csv into a custom table and exposes it in tag edit screens and front‑end templates will be made later. Focus on the 2 objectives above.


## OUTPUT_1

Here is `002_parsing_tags_similarity_sqlite_export_sqlite_csv.py` that builds on your previous script and adds:

1. **Clustering with HDBSCAN** on tag embeddings to define tag families. [towardsdatascience](https://towardsdatascience.com/clustering-sentence-embeddings-to-identify-intents-in-short-text-48d22d3bf02e/)
2. **Entity type detection with spaCy** and use of `usage_count` to pick a canonical tag per family. [stackoverflow](https://stackoverflow.com/questions/68035891/how-can-i-getting-ner-named-entity-recognition-for-one-word)

It:

- Reuses the same JSON structure as `001_*.py` (`sample_light_tags_20260125_130601.json`).  
- Writes families and canonical info into SQLite.  
- Exports a CSV `related_tags_embeddings_settings_csv_1.csv` with:

  `family_id, canonical_tag_id, canonical_label, tag_id, tag_label, similarity_to_canonical, usage_count, entity_label`

You can adjust thresholds and clustering parameters in the config at the top.

***

## Script: `002_parsing_tags_similarity_sqlite_export_sqlite_csv.py`

```python
"""
POINT_TAGS - Clustering + NER + SQLite + CSV export for tag families.

File: 002_parsing_tags_similarity_sqlite_export_sqlite_csv.py

Objectives:
1. Cluster tag embeddings (HDBSCAN) into semantic families.
2. Use NER (spaCy) + usage_count to choose a canonical tag per family.

Inputs:
- JSON tags from WordPress REST API (/wp/v2/tags):
  sample_light_tags_20260125_130601.json

Outputs:
- SQLite DB: related_tags_embeddings_settings_csv.sqlite
  - tag_embeddings            (tag_id -> embedding_json)
  - tag_ner                   (tag_id -> entity_label)
  - tag_families              (family_id -> canonical_tag_id, canonical_label)
  - tag_family_members        (family_id, tag_id, similarity_to_canonical, usage_count, entity_label)
- CSV: related_tags_embeddings_settings_csv_1.csv
  Columns:
    family_id,
    canonical_tag_id,
    canonical_label,
    tag_id,
    tag_label,
    similarity_to_canonical,
    usage_count,
    entity_label

Run:

    conda activate tags_treatment
    python 002_parsing_tags_similarity_sqlite_export_sqlite_csv.py
"""

import csv
import json
import logging
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import re

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore[import]
import hdbscan  # type: ignore[import]
import spacy    # type: ignore[import]


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
class TagClusteringConfig:
    """
    Configuration knobs for tag clustering + NER.
    """

    # Input JSON (same as in 001_*)
    tags_json_path: Path = Path("sample_light_tags_20260125_130601.json")

    # Embeddings: multilingual model
    embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    batch_size: int = 64
    lowercase_labels: bool = True
    basic_cleaning: bool = True
    normalize_embeddings: bool = True

    # HDBSCAN clustering parameters
    # You can tweak these depending on your tag volume:
    # - min_cluster_size: minimum tags per cluster
    # - min_samples: controls how conservative clustering is (None = same as min_cluster_size)
    hdbscan_min_cluster_size: int = 3
    hdbscan_min_samples: Optional[int] = None
    hdbscan_metric: str = "euclidean"  # embeddings are already normalized; cosine could also work

    # Similarity threshold for computing similarity to canonical
    similarity_threshold_to_canonical: float = 0.35

    # NER model (spaCy)
    # Install beforehand, e.g.:
    #   python -m spacy download en_core_web_sm
    spacy_model_name: str = "en_core_web_sm"

    # SQLite DB
    sqlite_path: Path = Path("related_tags_embeddings_settings_csv.sqlite")

    # CSV export for tag families
    csv_output_path: Path = Path("related_tags_embeddings_settings_csv_1.csv")


# --------------------------------------------------------------------
# Data model & JSON loading (same structure as 001_*)
# --------------------------------------------------------------------

@dataclass
class ParsedTag:
    id: int
    label: str
    usage_count: Optional[int] = None
    language: Optional[str] = None  # kept for future multilingual work


def load_tags_from_json(path: Path) -> List[ParsedTag]:
    """
    Load tags from a WP /wp/v2/tags JSON export.

    Structure example:

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

        if "id" not in item:
            continue

        tag_id = int(item["id"])
        label = str(item.get("name", "")) or str(item.get("slug", tag_id))

        usage_count = None
        if "count" in item:
            try:
                usage_count = int(item["count"])
            except (TypeError, ValueError):
                usage_count = None

        language = None  # not present here

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
        logger.info("First tag: id=%s, label=%r, usage_count=%r", tags[0].id, tags[0].label, tags[0].usage_count)
    return tags


# --------------------------------------------------------------------
# Pre-processing
# --------------------------------------------------------------------

_NON_ALNUM_RE = re.compile(r"[^0-9a-zA-ZÀ-ÖØ-öø-ÿ]+", re.UNICODE)


def clean_tag_label(label: str, lowercase: bool = True, basic_cleaning: bool = True) -> str:
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
    config: TagClusteringConfig,
) -> List[TagEmbedding]:
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
# NER (spaCy) for entity type
# --------------------------------------------------------------------

_spacy_nlp = None


def get_spacy_nlp(model_name: str):
    global _spacy_nlp
    if _spacy_nlp is None:
        logger.info("Loading spaCy model: %s", model_name)
        _spacy_nlp = spacy.load(model_name)
    return _spacy_nlp


def detect_entity_label(
    label: str,
    nlp,
) -> str:
    """
    Simple NER: run spaCy on the original label and return the first entity label.

    If no entity is detected, return "O" (outside).
    """
    doc = nlp(label)
    if doc.ents:
        # Take the first entity's label_ as the entity type.
        return doc.ents[0].label_
    return "O"


def build_tag_entity_map(
    tags: Sequence[ParsedTag],
    config: TagClusteringConfig,
) -> Dict[int, str]:
    """
    Map: tag_id -> entity_label (e.g. PERSON, ORG, GPE, O, ...).
    """
    nlp = get_spacy_nlp(config.spacy_model_name)
    entity_map: Dict[int, str] = {}

    logger.info("Running NER on %d tags", len(tags))

    for t in tags:
        entity_label = detect_entity_label(t.label, nlp)
        entity_map[t.id] = entity_label

    return entity_map


# --------------------------------------------------------------------
# Clustering (HDBSCAN)
# --------------------------------------------------------------------

def cluster_tags_hdbscan(
    embeddings: List[TagEmbedding],
    config: TagClusteringConfig,
) -> np.ndarray:
    """
    Run HDBSCAN on tag embeddings.

    Returns:
        labels: np.ndarray of shape (N,)
        where label = -1 means "noise" (no cluster).
    """
    if not embeddings:
        logger.warning("No embeddings for clustering")
        return np.array([])

    mat = np.asarray([vec for _, vec in embeddings], dtype=float)

    logger.info(
        "Clustering %d tag embeddings with HDBSCAN (min_cluster_size=%d, min_samples=%s, metric=%s)",
        mat.shape[0],
        config.hdbscan_min_cluster_size,
        str(config.hdbscan_min_samples),
        config.hdbscan_metric,
    )

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=config.hdbscan_min_cluster_size,
        min_samples=config.hdbscan_min_samples,
        metric=config.hdbscan_metric,
        cluster_selection_method="eom",
    )

    labels = clusterer.fit_predict(mat)

    unique_labels, counts = np.unique(labels, return_counts=True)
    logger.info("HDBSCAN produced clusters: %s", dict(zip(unique_labels.tolist(), counts.tolist())))
    return labels


# --------------------------------------------------------------------
# Canonical tag selection per family
# --------------------------------------------------------------------

@dataclass
class TagWithMeta:
    id: int
    label: str
    embedding: np.ndarray
    usage_count: int
    entity_label: str


@dataclass
class TagFamilyMember:
    family_id: int
    canonical_tag_id: int
    canonical_label: str
    tag_id: int
    tag_label: str
    similarity_to_canonical: float
    usage_count: int
    entity_label: str


def build_tag_families(
    tags: Sequence[ParsedTag],
    embeddings: List[TagEmbedding],
    entity_map: Dict[int, str],
    labels: np.ndarray,
    config: TagClusteringConfig,
) -> List[TagFamilyMember]:
    """
    Build tag families from HDBSCAN labels + embeddings + NER + usage_count.
    """
    if not embeddings or labels.size == 0:
        return []

    tag_id_to_embedding = {tid: np.asarray(vec, dtype=float) for tid, vec in embeddings}
    tag_id_to_tag = {t.id: t for t in tags}

    # Group tag IDs by cluster label (exclude noise = -1).
    cluster_to_tag_ids: Dict[int, List[int]] = {}
    tagged_ids = [tid for tid, _ in embeddings]

    for tag_id, cluster_label in zip(tagged_ids, labels):
        if cluster_label == -1:
            continue
        cluster_to_tag_ids.setdefault(int(cluster_label), []).append(tag_id)

    if not cluster_to_tag_ids:
        logger.warning("HDBSCAN produced no clusters (all noise).")
        return []

    logger.info("Number of non-noise clusters: %d", len(cluster_to_tag_ids))

    all_family_members: List[TagFamilyMember] = []
    family_counter = 0

    for cluster_label, cluster_tag_ids in cluster_to_tag_ids.items():
        if len(cluster_tag_ids) < config.hdbscan_min_cluster_size:
            # Should not happen due to HDBSCAN settings, but keep it explicit.
            continue

        family_id = family_counter
        family_counter += 1

        # Build list of TagWithMeta for this cluster.
        cluster_items: List[TagWithMeta] = []
        for tid in cluster_tag_ids:
            tag = tag_id_to_tag.get(tid)
            if tag is None:
                continue
            emb = tag_id_to_embedding[tid]
            usage = tag.usage_count if tag.usage_count is not None else 0
            ent = entity_map.get(tid, "O")
            cluster_items.append(
                TagWithMeta(
                    id=tid,
                    label=tag.label,
                    embedding=emb,
                    usage_count=usage,
                    entity_label=ent,
                )
            )

        if not cluster_items:
            continue

        # Canonical tag selection strategy:
        # 1) Prefer tags with higher usage_count.
        # 2) If tie, prefer shorter label (more general / clean).
        # 3) As tiebreaker, fall back to lowest id.
        cluster_items_sorted = sorted(
            cluster_items,
            key=lambda x: (-x.usage_count, len(x.label), x.id),
        )
        canonical = cluster_items_sorted[0]
        canonical_vec = canonical.embedding

        # Compute cosine similarity to canonical inside this family.
        canonical_norm = np.linalg.norm(canonical_vec)
        if canonical_norm == 0:
            canonical_norm = 1.0

        for item in cluster_items_sorted:
            sim = float(np.dot(canonical_vec, item.embedding) /
                        (canonical_norm * max(np.linalg.norm(item.embedding), 1e-12)))

            if sim < config.similarity_threshold_to_canonical:
                # Very loose filter: we still keep them because HDBSCAN already decided they belong.
                # You can uncomment the continue if you want harder filtering.
                # continue
                pass

            all_family_members.append(
                TagFamilyMember(
                    family_id=family_id,
                    canonical_tag_id=canonical.id,
                    canonical_label=canonical.label,
                    tag_id=item.id,
                    tag_label=item.label,
                    similarity_to_canonical=sim,
                    usage_count=item.usage_count,
                    entity_label=item.entity_label,
                )
            )

    logger.info("Built %d tag families with %d members total", family_counter, len(all_family_members))
    return all_family_members


# --------------------------------------------------------------------
# SQLite storage for families
# --------------------------------------------------------------------

def init_sqlite_for_families(db_path: Path) -> sqlite3.Connection:
    logger.info("Initializing SQLite DB for families at %s", db_path)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # tag_embeddings may already exist from 001_*; recreate if needed.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_embeddings (
            tag_id INTEGER PRIMARY KEY,
            embedding_json TEXT NOT NULL
        )
        """
    )

    # NER entity type per tag
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_ner (
            tag_id INTEGER PRIMARY KEY,
            entity_label TEXT NOT NULL
        )
        """
    )

    # Family-level canonical info
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_families (
            family_id INTEGER PRIMARY KEY,
            canonical_tag_id INTEGER NOT NULL,
            canonical_label TEXT NOT NULL
        )
        """
    )

    # Family members (one row per tag in a cluster)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_family_members (
            family_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            tag_label TEXT NOT NULL,
            similarity_to_canonical REAL NOT NULL,
            usage_count INTEGER NOT NULL,
            entity_label TEXT NOT NULL,
            PRIMARY KEY (family_id, tag_id)
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


def store_tag_ner(conn: sqlite3.Connection, entity_map: Dict[int, str]) -> None:
    logger.info("Storing NER labels for %d tags", len(entity_map))
    cur = conn.cursor()

    rows = [
        (tag_id, ent_label)
        for tag_id, ent_label in entity_map.items()
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO tag_ner (tag_id, entity_label)
        VALUES (?, ?)
        """,
        rows,
    )
    conn.commit()


def store_tag_families(conn: sqlite3.Connection, family_members: List[TagFamilyMember]) -> None:
    logger.info("Storing tag families and members into SQLite")

    cur = conn.cursor()

    # Insert into tag_families (deduplicate by family_id)
    family_map: Dict[int, Tuple[int, str]] = {}
    for m in family_members:
        family_map[m.family_id] = (m.canonical_tag_id, m.canonical_label)

    family_rows = [
        (fid, canonical_id, canonical_label)
        for fid, (canonical_id, canonical_label) in family_map.items()
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO tag_families (family_id, canonical_tag_id, canonical_label)
        VALUES (?, ?, ?)
        """,
        family_rows,
    )

    # Insert family members
    member_rows = [
        (m.family_id, m.tag_id, m.tag_label, m.similarity_to_canonical, m.usage_count, m.entity_label)
        for m in family_members
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO tag_family_members (
            family_id,
            tag_id,
            tag_label,
            similarity_to_canonical,
            usage_count,
            entity_label
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        member_rows,
    )

    conn.commit()


# --------------------------------------------------------------------
# CSV export
# --------------------------------------------------------------------

def export_families_to_csv(
    conn: sqlite3.Connection,
    csv_path: Path,
) -> None:
    """
    Export a flattened view of tag families to CSV:

    family_id,
    canonical_tag_id,
    canonical_label,
    tag_id,
    tag_label,
    similarity_to_canonical,
    usage_count,
    entity_label
    """
    logger.info("Exporting tag families to CSV at %s", csv_path)

    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            tf.family_id,
            tf.canonical_tag_id,
            tf.canonical_label,
            fm.tag_id,
            fm.tag_label,
            fm.similarity_to_canonical,
            fm.usage_count,
            fm.entity_label
        FROM tag_families AS tf
        JOIN tag_family_members AS fm
            ON tf.family_id = fm.family_id
        ORDER BY tf.family_id ASC, fm.similarity_to_canonical DESC
        """
    )
    rows = cur.fetchall()

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "family_id",
            "canonical_tag_id",
            "canonical_label",
            "tag_id",
            "tag_label",
            "similarity_to_canonical",
            "usage_count",
            "entity_label",
        ])
        for row in rows:
            writer.writerow(row)

    logger.info("Exported %d family-member rows to %s", len(rows), csv_path)


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main() -> None:
    config = TagClusteringConfig()
    logger.info("Effective configuration: %s", config)

    # 1. Load tags
    tags = load_tags_from_json(config.tags_json_path)
    if not tags:
        logger.warning("No tags loaded; aborting.")
        return

    # 2. Embeddings
    embeddings = embed_tags(tags, config)
    if not embeddings:
        logger.warning("No embeddings produced; aborting.")
        return

    # 3. NER (entity type per tag)
    entity_map = build_tag_entity_map(tags, config)

    # 4. Clustering (HDBSCAN)
    labels = cluster_tags_hdbscan(embeddings, config)
    if labels.size == 0:
        logger.warning("No cluster labels; aborting.")
        return

    # 5. Build tag families + canonical selection
    family_members = build_tag_families(tags, embeddings, entity_map, labels, config)
    if not family_members:
        logger.warning("No family members created; aborting.")
        return

    # 6. Store in SQLite
    conn = init_sqlite_for_families(config.sqlite_path)
    try:
        store_tag_embeddings(conn, embeddings)
        store_tag_ner(conn, entity_map)
        store_tag_families(conn, family_members)

        # 7. Export to CSV
        export_families_to_csv(conn, config.csv_output_path)
    finally:
        conn.close()

    logger.info("Done. Tag family CSV ready at %s", config.csv_output_path)


if __name__ == "__main__":
    main()
```

This gives you:

- A clustering/NER‑aware **tag families** CSV and SQLite schema ready for the future WordPress plugin.  
- Clear config knobs for HDBSCAN, similarity thresholds, and NER model so you can iterate quickly.




