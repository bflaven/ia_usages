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

# Option A: conda-forge (usually easiest on macOS/Linux)
conda install -c conda-forge hdbscan

# If that fails, Option B: pip
pip install hdbscan

# Either via conda-forge:
conda install -c conda-forge spacy

# Or via pip:
pip install spacy
python -m spacy download en_core_web_sm

# # List installed spaCy models
python -m spacy validate


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_tags/

# launch the file
python 003_parsing_tags_similarity_sqlite_export_sqlite_csv_hdbscan_ner.py


"""


"""
POINT_TAGS - Graph-based clustering + NER + SQLite + CSV export for tag families.

File: 002_parsing_tags_similarity_sqlite_export_sqlite_csv.py

This script:

1. Loads tags from sample_light_tags_20260125_130601.json (WP /wp/v2/tags).
2. Builds multilingual embeddings for tag labels.
3. Computes cosine similarity matrix.
4. Builds an undirected graph where edges connect tags with similarity >= SIM_THRESHOLD.
5. Connected components of this graph = tag families.
6. Uses spaCy NER + usage_count to pick a canonical tag per family.
7. Stores families in SQLite and exports them to CSV.

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
import spacy  # type: ignore[import]


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
    # Input JSON (WP /wp/v2/tags)
    tags_json_path: Path = Path("sample_all_tags_20260125_130601.json")

    # Embeddings
    embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    batch_size: int = 64
    lowercase_labels: bool = True
    basic_cleaning: bool = True
    normalize_embeddings: bool = True

    # Similarity → graph edges
    # If cosine similarity between two tags >= sim_threshold_for_family, we link them.
    sim_threshold_for_family: float = 0.60

    # Minimum family size (components with fewer than this many tags are ignored).
    min_family_size: int = 2

    # NER model
    spacy_model_name: str = "en_core_web_sm"

    # SQLite DB
    sqlite_path: Path = Path("related_tags_embeddings_settings_csv.sqlite")

    # CSV export
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

        tags.append(
            ParsedTag(
                id=tag_id,
                label=label,
                usage_count=usage_count,
                language=None,
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
# NER (spaCy)
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
    doc = nlp(label)
    if doc.ents:
        return doc.ents[0].label_
    return "O"


def build_tag_entity_map(
    tags: Sequence[ParsedTag],
    config: TagClusteringConfig,
) -> Dict[int, str]:
    nlp = get_spacy_nlp(config.spacy_model_name)
    entity_map: Dict[int, str] = {}

    logger.info("Running NER on %d tags", len(tags))

    for t in tags:
        entity_label = detect_entity_label(t.label, nlp)
        entity_map[t.id] = entity_label

    return entity_map


# --------------------------------------------------------------------
# Graph-based clustering via similarity
# --------------------------------------------------------------------

def compute_cosine_similarity_matrix(embeddings: List[TagEmbedding]) -> Tuple[np.ndarray, List[int]]:
    """
    Return:
      sim_matrix: (N, N) cosine similarity matrix
      tag_ids:    order of tags in matrix
    """
    tag_ids = [tid for tid, _ in embeddings]
    mat = np.asarray([vec for _, vec in embeddings], dtype=float)

    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    mat_norm = mat / norms

    sim_matrix = mat_norm @ mat_norm.T
    return sim_matrix, tag_ids


def build_similarity_graph_components(
    embeddings: List[TagEmbedding],
    sim_threshold: float,
    min_family_size: int,
) -> List[List[int]]:
    """
    Build a graph where nodes = tags and edges connect tags
    with cosine similarity >= sim_threshold, then extract
    connected components.

    Returns:
        list of components, each a list of tag_ids.
    """
    if not embeddings:
        return []

    sim_matrix, tag_ids = compute_cosine_similarity_matrix(embeddings)
    n = sim_matrix.shape[0]

    # Build adjacency list
    neighbors: Dict[int, List[int]] = {i: [] for i in range(n)}

    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i, j] >= sim_threshold:
                neighbors[i].append(j)
                neighbors[j].append(i)

    visited = [False] * n
    components: List[List[int]] = []

    for i in range(n):
        if visited[i]:
            continue
        # BFS / DFS for connected component
        stack = [i]
        comp_indices = []

        while stack:
            idx = stack.pop()
            if visited[idx]:
                continue
            visited[idx] = True
            comp_indices.append(idx)
            for nb in neighbors[idx]:
                if not visited[nb]:
                    stack.append(nb)

        if len(comp_indices) >= min_family_size:
            # Map indices back to tag_ids
            comp_tag_ids = [tag_ids[k] for k in comp_indices]
            components.append(comp_tag_ids)

    logger.info(
        "Graph clustering produced %d families (min_family_size=%d, sim_threshold=%.2f)",
        len(components),
        min_family_size,
        sim_threshold,
    )
    return components


# --------------------------------------------------------------------
# Canonical selection per family
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
    components: List[List[int]],
    sim_matrix: np.ndarray,
    tag_ids_order: List[int],
    config: TagClusteringConfig,
) -> List[TagFamilyMember]:
    if not components:
        return []

    tag_id_to_tag = {t.id: t for t in tags}
    tag_id_to_index = {tid: i for i, tid in enumerate(tag_ids_order)}

    all_members: List[TagFamilyMember] = []
    family_counter = 0

    for comp_tag_ids in components:
        family_id = family_counter
        family_counter += 1

        cluster_items: List[TagWithMeta] = []
        for tid in comp_tag_ids:
            tag = tag_id_to_tag.get(tid)
            if tag is None:
                continue

            idx = tag_id_to_index[tid]
            emb = sim_matrix[idx] * 0.0  # dummy to satisfy typing, we will use sim_matrix directly
            # We don't actually need the embedding vector here because
            # we already have pairwise similarities in sim_matrix.
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

        # Choose canonical: highest usage_count, then shortest label, then lowest id.
        cluster_items_sorted = sorted(
            cluster_items,
            key=lambda x: (-x.usage_count, len(x.label), x.id),
        )
        canonical = cluster_items_sorted[0]
        canonical_idx = tag_id_to_index[canonical.id]

        # Build members with similarity to canonical.
        for item in cluster_items_sorted:
            item_idx = tag_id_to_index[item.id]
            sim = float(sim_matrix[canonical_idx, item_idx])

            all_members.append(
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

    logger.info("Built %d tag families with %d members", family_counter, len(all_members))
    return all_members


# --------------------------------------------------------------------
# SQLite storage
# --------------------------------------------------------------------

def init_sqlite_for_families(db_path: Path) -> sqlite3.Connection:
    logger.info("Initializing SQLite DB for families at %s", db_path)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_ner (
            tag_id INTEGER PRIMARY KEY,
            entity_label TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_families (
            family_id INTEGER PRIMARY KEY,
            canonical_tag_id INTEGER NOT NULL,
            canonical_label TEXT NOT NULL
        )
        """
    )

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

    # Families
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

    # Members
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

    # 3. NER
    entity_map = build_tag_entity_map(tags, config)

    # 4. Similarity matrix
    sim_matrix, tag_ids_order = compute_cosine_similarity_matrix(embeddings)

    # 5. Graph-based clustering
    components = build_similarity_graph_components(
        embeddings,
        sim_threshold=config.sim_threshold_for_family,
        min_family_size=config.min_family_size,
    )
    if not components:
        logger.warning("No tag families formed (no components above threshold); aborting.")
        return

    # 6. Build families + canonical selection
    family_members = build_tag_families(
        tags,
        embeddings,
        entity_map,
        components,
        sim_matrix,
        tag_ids_order,
        config,
    )
    if not family_members:
        logger.warning("No family members created; aborting.")
        return

    # 7. Store in SQLite
    conn = init_sqlite_for_families(config.sqlite_path)
    try:
        store_tag_ner(conn, entity_map)
        store_tag_families(conn, family_members)

        # 8. Export to CSV
        export_families_to_csv(conn, config.csv_output_path)
    finally:
        conn.close()

    logger.info("Done. Tag family CSV ready at %s", config.csv_output_path)


if __name__ == "__main__":
    main()












