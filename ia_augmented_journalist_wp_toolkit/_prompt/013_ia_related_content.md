## PROMPT_1


I have some questions: 

1. Where in the script it is set that there will be 5 posts tested against the main post selected and not 10 posts against the main post selected ? I have checked post_related table, you have the main post selected, the similarity, the rank. Where in the script, I have 5 posts testes against the main post and not 10 posts against the post selected 


2. Similarly can form 0 to 1, where in the script it is set that the similarity must >= to 0.45

In both question, indicate the line and specify where is set and may make it variables so I can easily uppdate the both values, the variable `post_number_against` and the variable threshold for similarity `threshold_for_similarity`


3. Below, here is  my interpretation of reading the database for a post. Am I right ? I have added the title so it is more straightforward.



```text
+ Main post 13091 AI, Agentic Browsers and the End of Digital Autonomy

--- 12927 Content Quality: How Sentence Embeddings Can Save AI-Generated Content and some other concerns on AI: Environmental Impact, Job Loss, 0.5533628113550911, 1
--- 12840 Exploring SEO, SMO, and ASO with AI: Developing Effective Prompts to Boost Digital Strategies, 0.5273974579326484, 2
--- 12947 Breadcrumbs of Innovation: A Snapshot of AI Explorations, 0.5141183899494592, 3
--- 12815 Unraveling the Cost of AI: The Hidden Expenses of API Keys and Pay-as-You-Go Pricing in AI-Based Products, 0.47802840827521753, 4
--- 11616 Web scraping, Beautifulsoup, Selenium &#8211; Various explorations in web scraping with Python and jumping timidly in surveillance capitalism, 0.4754158172759728, 5
```



## OUTPUT_1

1. Number of related posts (5 vs 10)

In `008_parsing_posts_similarity_sqlite.py`, the “how many related posts per main post” is controlled by `top_k` in the config and passed into the similarity function.

- In the config dataclass:

```python
@dataclass
class EmbeddingConfig:
    ...
    top_k: int = 5  # number of related posts per anchor
```

- In `main()`:

```python
related_by_post = compute_similarity_top_k(embeddings, top_k=config.top_k)
```

- In `compute_similarity_top_k`:

```python
def compute_similarity_top_k(
    embeddings: List[PostEmbedding],
    top_k: int,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    ...
    idx = np.argsort(sim_matrix[i])[-top_k:][::-1]
```

So the effective value is `EmbeddingConfig.top_k`, default 5, used when slicing the top similar indices. To make it easy to change, you already can:

- Edit the default in the dataclass:

```python
top_k: int = 10  # e.g. change to 10
```

or

- Override via env var:

```bash
export RELATED_TOP_K="10"
```

If you want a more explicit variable name, you can alias it:

```python
@dataclass
class EmbeddingConfig:
    ...
    post_number_against: int = 5  # more explicit name
    ...
    @classmethod
    def from_env(cls) -> "EmbeddingConfig":
        ...
        post_number_against_str = os.getenv("POST_NUMBER_AGAINST", "5")
        try:
            post_number_against = int(post_number_against_str)
        except ValueError:
            post_number_against = 5
        return cls(
            ...
            post_number_against=post_number_against,
        )
```

and in `main()`:

```python
related_by_post = compute_similarity_top_k(
    embeddings,
    top_k=config.post_number_against,
)
```

This way you control it via `config.post_number_against`. [stackoverflow](https://stackoverflow.com/questions/72328976/python-finding-cosine-similarity-between-two-groups-of-vectors-in-the-most-eff)

2. Similarity threshold (>= 0.45)

Right now there is **no similarity threshold** applied in the script: it always takes top‑K, even if some scores are low or negative. The only “filter” is “top K by similarity”.

To introduce a threshold `threshold_for_similarity` (e.g. 0.45), add it to the config and use it when building the related list.

a) Add to config:

```python
@dataclass
class EmbeddingConfig:
    ...
    threshold_for_similarity: float = 0.45
    ...
    @classmethod
    def from_env(cls) -> "EmbeddingConfig":
        ...
        threshold_str = os.getenv("RELATED_SIM_THRESHOLD", "0.45")
        try:
            threshold_for_similarity = float(threshold_str)
        except ValueError:
            threshold_for_similarity = 0.45

        return cls(
            ...
            threshold_for_similarity=threshold_for_similarity,
        )
```

b) Pass it where you compute similarities:

Change `compute_similarity_top_k` to accept the threshold:

```python
def compute_similarity_top_k(
    embeddings: List[PostEmbedding],
    top_k: int,
    similarity_threshold: float,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    ...
    for i in range(n):
        sim_matrix[i, i] = -np.inf
        idx = np.argsort(sim_matrix[i])[-top_k:][::-1]

        related: List[Tuple[int, float]] = []
        for j in idx:
            score = float(sim_matrix[i, j])
            if score < similarity_threshold:
                continue  # skip low-sim matches
            rel_post_id = post_ids[j]
            related.append((rel_post_id, score))

        all_results.append((post_ids[i], related))
```

And in `main()`:

```python
related_by_post = compute_similarity_top_k(
    embeddings,
    top_k=config.top_k,
    similarity_threshold=config.threshold_for_similarity,
)
```

or with your variable names:

```python
related_by_post = compute_similarity_top_k(
    embeddings,
    top_k=config.post_number_against,
    similarity_threshold=config.threshold_for_similarity,
)
```

This gives you both knobs:

- `post_number_against` → max number of candidates per post.  
- `threshold_for_similarity` → minimum cosine similarity in  for a pair to be kept. [dataquest](https://www.dataquest.io/blog/measuring-similarity-and-distance-between-embeddings/)

3. Your reading of the DB example

Your interpretation is correct.

For the example:

```text
+ Main post 13091 AI, Agentic Browsers and the End of Digital Autonomy

--- 12927 Content Quality: ... 0.5533628113550911, 1
--- 12840 Exploring SEO, SMO, and ASO with AI: ... 0.5273974579326484, 2
--- 12947 Breadcrumbs of Innovation: ... 0.5141183899494592, 3
--- 12815 Unraveling the Cost of AI: ... 0.47802840827521753, 4
--- 11616 Web scraping, Beautifulsoup, Selenium – ... 0.4754158172759728, 5
```

This matches what the script writes to `post_related`:

- `post_id` = 13091 (the main/anchor post).  
- For each row:
  - `related_post_id` = 12927, 12840, 12947, 12815, 11616.  
  - `similarity` = the cosine similarity between the embedding of 13091 and the embedding of the related post (0.55, 0.52, etc.).  
  - `rank` = 1–5, descending by similarity (1 is most similar, 5 is the fifth most similar).  

This is exactly the structure you need to later:

- Export `post_related` to MariaDB.  
- For a given `post_id` in your WP plugin, fetch `ORDER BY rank` (or `similarity DESC`) and display the 3–5 related posts by `related_post_id`. [apxml](https://apxml.com/courses/building-ml-recommendation-system/chapter-2-content-based-filtering/producing-content-based-recommendations)

## PROMPT_2
Can you rewrite the script based on `008_parsing_posts_similarity_sqlite.py` with the integrated with these 2 modifications with the proper comments named this new script `009_parsing_posts_similarity_sqlite_settings.py`


## OUTPUT_2

Here is `009_parsing_posts_similarity_sqlite_settings.py` with:

- `post_number_against` (how many related posts to keep per anchor).  
- `threshold_for_similarity` (minimum cosine similarity in ). [stackoverflow](https://stackoverflow.com/questions/70782902/best-way-to-navigate-a-nested-json-in-python)

Both are in the config and overridable via env vars.

```python
"""
POINT_6 - Similarity + SQLite storage with settings.

File: 009_parsing_posts_similarity_sqlite_settings.py

This module:
- Loads WP posts and computes embeddings (reuses POINT_1–5 logic).
- Computes cosine similarity between all posts.
- For each post_id, selects up to `post_number_against` related posts
  whose similarity >= `threshold_for_similarity`.
- Stores embeddings and relations in a temporary SQLite database.

Config is centralized in EmbeddingConfig and can be overridden by env vars.

Run:
    conda activate tags_treatment
    python 009_parsing_posts_similarity_sqlite_settings.py

Env overrides (optional):
    export WP_JSON_PATH="sample_posts_2020_to_2025.json"
    export EMBEDDING_MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
    export EMBEDDING_BATCH_SIZE="32"
    export EMBEDDING_MAX_CHARS="4000"
    export POST_NUMBER_AGAINST="5"
    export RELATED_SIM_THRESHOLD="0.45"
    export EMBEDDING_SQLITE_PATH="related_posts_embeddings.sqlite"
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
# Configuration with explicit knobs
# --------------------------------------------------------------------

@dataclass
class EmbeddingConfig:
    wp_json_path: Path = Path("sample_posts_2020_to_2025.json")

    # Embedding / preprocessing
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32
    max_chars: int = 4000
    include_slug: bool = False
    normalize_embeddings: bool = True

    # SQLite
    sqlite_path: Path = Path("related_posts_embeddings.sqlite")

    # Similarity settings
    # post_number_against = how many related posts we keep per anchor post
    post_number_against: int = 5
    # threshold_for_similarity = minimum cosine similarity to keep a relation
    threshold_for_similarity: float = 0.45

    @classmethod
    def from_env(cls) -> "EmbeddingConfig":
        """
        Build config from environment variables, with sane defaults.
        """
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

        sqlite_path = Path(os.getenv("EMBEDDING_SQLITE_PATH", "related_posts_embeddings.sqlite"))

        # Number of related posts to keep (top-K)
        post_number_against_str = os.getenv("POST_NUMBER_AGAINST", "5")
        try:
            post_number_against = int(post_number_against_str)
        except ValueError:
            post_number_against = 5

        # Cosine similarity threshold
        threshold_str = os.getenv("RELATED_SIM_THRESHOLD", "0.45")
        try:
            threshold_for_similarity = float(threshold_str)
        except ValueError:
            threshold_for_similarity = 0.45

        return cls(
            wp_json_path=wp_json_path,
            embedding_model_name=embedding_model_name,
            batch_size=batch_size,
            max_chars=max_chars,
            include_slug=include_slug,
            normalize_embeddings=normalize_embeddings,
            sqlite_path=sqlite_path,
            post_number_against=post_number_against,
            threshold_for_similarity=threshold_for_similarity,
        )


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
# Pre-processing and model accessor
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
# Batching and embedding
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
# Similarity computation with top-K and threshold
# --------------------------------------------------------------------

def compute_similarity_top_k(
    embeddings: List[PostEmbedding],
    top_k: int,
    similarity_threshold: float,
) -> List[Tuple[int, List[Tuple[int, float]]]]:
    """
    Given:
        embeddings: list of (post_id, embedding_vector)

    Returns:
        list of (post_id, [(related_post_id, similarity), ...])

    - For each anchor post, we:
      - compute cosine similarity to all others,
      - take top_k highest,
      - then filter out any below similarity_threshold.
    """
    if not embeddings:
        return []

    post_ids = [pid for pid, _ in embeddings]
    mat = np.asarray([vec for _, vec in embeddings], dtype=float)  # (N, D)

    # Normalize rows to unit norm so dot product == cosine similarity. [web:121][web:122]
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    mat_norm = mat / norms

    sim_matrix = mat_norm @ mat_norm.T  # (N, N), cosine similarities [web:113][web:122]

    n = sim_matrix.shape[0]
    all_results: List[Tuple[int, List[Tuple[int, float]]]] = []

    for i in range(n):
        # Exclude self similarity
        sim_matrix[i, i] = -np.inf

        # Get indices of top_k highest similarities
        idx = np.argsort(sim_matrix[i])[-top_k:][::-1]

        related: List[Tuple[int, float]] = []
        for j in idx:
            score = float(sim_matrix[i, j])
            if score < similarity_threshold:
                continue  # apply threshold_for_similarity
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
# Main runner
# --------------------------------------------------------------------

def main() -> None:
    config = EmbeddingConfig.from_env()
    logger.info("Effective configuration: %s", config)

    posts = load_posts_from_json(config.wp_json_path)
    embeddings = embed_posts_batched(posts, config)

    # Compute similarities with explicit settings
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

    # Quick sanity check: show first 2 anchors & related IDs
    for post_id, related in related_by_post[:2]:
        logger.info(
            "Post %s related -> %s",
            post_id,
            [(rid, f"{score:.3f}") for rid, score in related],
        )


if __name__ == "__main__":
    main()
```

Now you can:

- Change `post_number_against` (default 5) to 10 in the dataclass or via `POST_NUMBER_AGAINST`.  
- Change `threshold_for_similarity` (default 0.45) via `RELATED_SIM_THRESHOLD`.  

The SQLite schema and behavior stay the same; only how many rows per `post_id` and which similarity scores are kept will change. [stackoverflow](https://stackoverflow.com/questions/70032777/quickly-performing-cosine-similarity-with-list-of-embeddings)



## PROMPT_3
I have changed POST_NUMBER_AGAINST to 10 and RELATED_SIM_THRESHOLD to 0.40 but I see no chnages. Can you fix and make the csript work so I can play with these 2 values.

