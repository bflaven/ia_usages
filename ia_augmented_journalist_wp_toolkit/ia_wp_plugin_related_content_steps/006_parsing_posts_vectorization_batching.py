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
python 006_parsing_posts_vectorization_batching.py


"""

"""
POINT_4 - Implement pre-processing + batching.

File: 006_parsing_posts_vectorization_batching.py

This module:
- Reuses ParsedPost and the text-building functions.
- Reuses the embedding model accessor.
- Adds a batched version of embed_posts() for scalability.

Run:
    conda activate tags_treatment
    python 006_parsing_posts_vectorization_batching.py
"""

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

import html
import re

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore[import]


# --------------------------------------------------------------------
# Shared data structure
# --------------------------------------------------------------------

@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


# --------------------------------------------------------------------
# Pre-processing (POINT_1, reused)
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
# Embedding model accessor (POINT_2, reused)
# --------------------------------------------------------------------

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_BATCH_SIZE = 32  # good starting point for CPU/GPU [web:93][web:94]

_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


# --------------------------------------------------------------------
# Batching utility
# --------------------------------------------------------------------

def iter_batches(items: Sequence[ParsedPost], batch_size: int) -> Iterable[Sequence[ParsedPost]]:
    """
    Yield items in batches of size `batch_size`.
    Last batch may be smaller.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    n = len(items)
    for start in range(0, n, batch_size):
        end = start + batch_size
        yield items[start:end]


# --------------------------------------------------------------------
# Vectorization API with batching (POINT_4)
# --------------------------------------------------------------------

EmbeddingVector = List[float]
PostEmbedding = Tuple[int, EmbeddingVector]


def embed_posts_batched(
    posts: Sequence[ParsedPost],
    *,
    max_chars: Optional[int] = 4000,
    include_slug: bool = False,
    normalize: bool = True,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> List[PostEmbedding]:
    """
    Embed posts using SentenceTransformers in batches.

    - Pre-processing is still done via build_post_text (POINT_1).
    - The model is obtained via get_embedding_model (POINT_2).
    - Batching improves throughput and memory usage for large N. [web:93][web:94][web:96]
    """
    if not posts:
        return []

    model = get_embedding_model()
    results: List[PostEmbedding] = []

    for batch_posts in iter_batches(posts, batch_size):
        # 1) Pre-process: build texts for this batch
        texts = [
            build_post_text(p, max_chars=max_chars, include_slug=include_slug)
            for p in batch_posts
        ]

        # 2) Encode in one go for this batch
        embeddings = model.encode(texts, normalize_embeddings=normalize)
        emb_arr = np.asarray(embeddings)  # shape: (len(batch_posts), dim)

        # 3) Attach embeddings back to post IDs
        for post, vec in zip(batch_posts, emb_arr):
            results.append((post.id, vec.astype(float).tolist()))

    return results


# --------------------------------------------------------------------
# Quick manual test
# --------------------------------------------------------------------

def main() -> None:
    demo_posts = [
        ParsedPost(
            id=1,
            title_rendered="AI, Agentic Browsers and the End of Digital Autonomy",
            content="Some example content for the first post.",
            slug="ai-agentic-browsers-and-the-end-of-digital-autonomy",
        ),
        ParsedPost(
            id=2,
            title_rendered="Rescuing Failed AI Implementations",
            content="Another bit of sample content to embed.",
            slug="rescuing-failed-ai-implementations",
        ),
        ParsedPost(
            id=3,
            title_rendered="Third post about vectorization and batching",
            content="Testing batching of embeddings.",
            slug="third-post-vectorization-batching",
        ),
    ]

    post_embeddings = embed_posts_batched(
        demo_posts,
        max_chars=4000,
        include_slug=False,
        normalize=True,
        batch_size=2,  # small batch to see it work
    )

    print(f"Number of posts embedded: {len(post_embeddings)}")
    for post_id, vec in post_embeddings:
        print(f"Post {post_id} -> embedding length = {len(vec)}")


if __name__ == "__main__":
    main()














