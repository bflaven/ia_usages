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
python 004_parsing_posts_choose_embedding_model.py


"""

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












