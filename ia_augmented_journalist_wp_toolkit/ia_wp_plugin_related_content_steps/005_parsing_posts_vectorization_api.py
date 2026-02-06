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
python 005_parsing_posts_vectorization_api.py


"""

"""
POINT_3 - Design a small vectorization API.

File: 005_parsing_posts_vectorization_api.py

This module:
- Defines ParsedPost (same structure as other scripts, can be deduplicated later).
- Reuses the text-building logic (POINT_1).
- Reuses the embedding model logic (POINT_2) inlined here.
- Exposes a small API:
    - embed_post(post) -> (post_id, embedding_vector)
    - embed_posts(posts) -> List[(post_id, embedding_vector)]

Run from your conda env:
    conda activate tags_treatment
    python 005_parsing_posts_vectorization_api.py
"""

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

import html
import re

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore[import]


# --------------------------------------------------------------------
# Data structure (keep consistent with other scripts)
# --------------------------------------------------------------------

@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


# --------------------------------------------------------------------
# POINT_1 logic: build text to embed
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
# POINT_2 logic: embedding model accessor
# (duplicated here for simplicity; you can import from 004_ later)
# --------------------------------------------------------------------

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


# --------------------------------------------------------------------
# POINT_3 - Vectorization API
# --------------------------------------------------------------------

EmbeddingVector = List[float]
PostEmbedding = Tuple[int, EmbeddingVector]


def embed_post(
    post: ParsedPost,
    *,
    max_chars: Optional[int] = 4000,
    include_slug: bool = False,
    normalize: bool = True,
) -> PostEmbedding:
    """
    Embed a single ParsedPost and return (post_id, embedding_vector).
    """
    model = get_embedding_model()
    text = build_post_text(post, max_chars=max_chars, include_slug=include_slug)

    emb = model.encode([text], normalize_embeddings=normalize)
    emb_arr = np.asarray(emb)[0]  # shape: (dim,)

    return post.id, emb_arr.astype(float).tolist()


def embed_posts(
    posts: Sequence[ParsedPost],
    *,
    max_chars: Optional[int] = 4000,
    include_slug: bool = False,
    normalize: bool = True,
) -> List[PostEmbedding]:
    """
    Embed a sequence of posts and return a list of (post_id, embedding_vector).

    POINT_4 will add explicit batching; here we encode all in one call.
    """
    if not posts:
        return []

    model = get_embedding_model()

    texts = [
        build_post_text(post, max_chars=max_chars, include_slug=include_slug)
        for post in posts
    ]

    embeddings = model.encode(texts, normalize_embeddings=normalize)
    emb_arr = np.asarray(embeddings)  # shape: (n_posts, dim)

    result: List[PostEmbedding] = []
    for post, vec in zip(posts, emb_arr):
        result.append((post.id, vec.astype(float).tolist()))

    return result


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
    ]

    post_embeddings = embed_posts(demo_posts)

    print(f"Number of posts embedded: {len(post_embeddings)}")
    for post_id, vec in post_embeddings:
        print(f"Post {post_id} -> embedding length = {len(vec)}")


if __name__ == "__main__":
    main()















