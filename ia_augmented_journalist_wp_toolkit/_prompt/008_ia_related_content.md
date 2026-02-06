## PROMPT_1

I have decided to go with todo list, I have named each on how to proceed as `POINT_#NB` to make the distinction with `STEP_#NB`.

The `POINT_1` is done; let's proceed to `POINT_2`, give a name for the script file in python e.g 003_parsing_posts_[name_of_the_point].py. Keep the increment number in the filename.

I am using anaconda to manage environnement. The name of the env is `tags_treatment`.

```text
# POINT_1. Decide what to vectorize per post (DONE, 003_parsing_posts_vectorize_per_post.py)
# POINT_2. Choose and configure an embedding model (TODO)
# POINT_3. Design a small vectorization API (TODO)
# POINT_4. Implement pre‑processing + batching (TODO)
# POINT_5. Plan for reproducibility and configuration (TODO)
# POINT_6. Connect STEP_1 to later steps (high level) (TODO) 
```







## OUTPUT_1
The error means there is still something (likely a comment or blank line with non‑ASCII/BOM characters) before `from __future__ import annotations` in your actual file, even if it doesn’t look like it.

Simplest fix: remove the future import entirely; you don’t strictly need it here. Here is a version of `004_parsing_posts_choose_embedding_model.py` without `from __future__ import annotations`, so the error disappears:

```python
"""
POINT_2 - Choose and configure an embedding model.

File: 004_parsing_posts_choose_embedding_model.py

This module:
- Defines the embedding model name and basic config.
- Provides a singleton-style accessor `get_embedding_model`.
- Includes a small sanity-check `main()` to verify everything works.

Requires:
    conda activate tags_treatment
    conda install -c conda-forge sentence-transformers
    # or: pip install -U sentence-transformers
"""

from dataclasses import dataclass
from typing import Optional

from sentence_transformers import SentenceTransformer  # type: ignore[import]


# --------------------------------------------------------------------
# Data structure (same as POINT_1; keep in sync or import from there)
# --------------------------------------------------------------------

@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


# --------------------------------------------------------------------
# Embedding model configuration
# --------------------------------------------------------------------

# You can change this later if you want to try another model
# (e.g. 'sentence-transformers/all-mpnet-base-v2').
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Will be used later for batching in POINT_4, kept here for central config.
DEFAULT_BATCH_SIZE = 32


# --------------------------------------------------------------------
# Lazy-loaded global model instance
# --------------------------------------------------------------------

_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    """
    Return a singleton SentenceTransformer instance.

    The model is loaded only once per process. Other modules (POINT_3/4/…)
    should import and use this function instead of instantiating the model
    directly.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


# --------------------------------------------------------------------
# Sanity check / quick probe
# --------------------------------------------------------------------

def main() -> None:
    """
    Quick manual test:
    - Loads the embedding model.
    - Encodes two dummy sentences.
    - Prints basic information about the embeddings.
    """
    model = get_embedding_model()

    sentences = [
        "This is a sample WP post title.",
        "Another example content to check embeddings.",
    ]
    embeddings = model.encode(sentences)

    print(f"Model name: {EMBEDDING_MODEL_NAME}")
    print(f"Type of embeddings: {type(embeddings)}")

    # Try to inspect shape if numpy is available, but don't hard depend on it.
    try:
        import numpy as np  # type: ignore[import]
        arr = np.asarray(embeddings)
        print(f"Embeddings shape: {arr.shape}")  # expected: (2, 384) for all-MiniLM-L6-v2
    except Exception:
        # If numpy is not installed, just skip shape inspection.
        pass


if __name__ == "__main__":
    main()
```

This avoids the `from __future__ import annotations` constraint entirely and will run fine in your `tags_treatment` environment. [sbert](https://sbert.net/docs/quickstart.html)
