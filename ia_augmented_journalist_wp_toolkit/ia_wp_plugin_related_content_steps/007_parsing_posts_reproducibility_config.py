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
python 007_parsing_posts_reproducibility_config.py


"""

"""
POINT_5 - Plan for reproducibility and configuration.

File: 007_parsing_posts_reproducibility_config.py

This module:
- Centralizes configuration (paths, model name, batch size, etc.).
- Loads overrides from environment variables when present.
- Provides a small "runner" that ties together:
    - loading posts from JSON
    - building texts
    - batching embeddings

Run:
    conda activate tags_treatment
    python 007_parsing_posts_reproducibility_config.py

Optionally configure via env vars, e.g.:
    export WP_JSON_PATH="sample_posts_2020_to_2025.json"
    export EMBEDDING_MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
    export EMBEDDING_BATCH_SIZE="32"
"""

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import html
import re

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore[import]


# --------------------------------------------------------------------
# Logging setup
# --------------------------------------------------------------------

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)


# --------------------------------------------------------------------
# Configuration dataclass (central config point)
# --------------------------------------------------------------------

@dataclass
class EmbeddingConfig:
    # Data
    wp_json_path: Path = Path("sample_posts_2020_to_2025.json")

    # Embedding model
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32
    max_chars: int = 4000
    include_slug: bool = False
    normalize_embeddings: bool = True

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

        return cls(
            wp_json_path=wp_json_path,
            embedding_model_name=embedding_model_name,
            batch_size=batch_size,
            max_chars=max_chars,
            include_slug=include_slug,
            normalize_embeddings=normalize_embeddings,
        )


# --------------------------------------------------------------------
# Core data structure (keep consistent with other scripts)
# --------------------------------------------------------------------

@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


# --------------------------------------------------------------------
# JSON loading
# --------------------------------------------------------------------

def load_posts_from_json(path: Path) -> List[ParsedPost]:
    """
    Load WP-like posts from a JSON file and convert to ParsedPost objects.
    """
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
# Pre-processing (POINT_1)
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
# Embedding model accessor (POINT_2)
# --------------------------------------------------------------------

_model: Optional[SentenceTransformer] = None


def get_embedding_model(model_name: str) -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
    return _model


# --------------------------------------------------------------------
# Batching (POINT_4)
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
    """
    Embed posts using SentenceTransformers in batches, honoring the config.
    """
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
# Main runner for this step
# --------------------------------------------------------------------

def main() -> None:
    config = EmbeddingConfig.from_env()
    logger.info("Effective configuration: %s", config)

    posts = load_posts_from_json(config.wp_json_path)
    post_embeddings = embed_posts_batched(posts, config)

    # Simple sanity check: print the first 2 embeddings metadata
    for post_id, vec in post_embeddings[:2]:
        logger.info("Post %s -> embedding length = %d", post_id, len(vec))


if __name__ == "__main__":
    main()






