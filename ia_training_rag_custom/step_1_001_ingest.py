"""
[env]
# Conda Environment
conda create --name ia_achats python=3.9.13
conda info --envs
source activate ia_achats
conda deactivate


# BURN AFTER READING
source activate ia_achats



# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n ia_achats

# BURN AFTER READING
conda env remove -n ia_achats


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
pip install mistralai python-dotenv datauri

python -m pip install mistralai python-dotenv datauri


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_training_rag_custom

# launch the file
python step_1_001_ingest.py


"""

"""
step_1_001_ingest.py

Purpose:
Parse WordPress posts JSON file from source/flaven_posts_en_2.json,
extract id, title.rendered, content.rendered for each post,
and save as clean, normalized JSON.

Configuration at top for easy reuse.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

@dataclass
class Post:
    """Normalized post data."""
    id: int
    title_rendered: str
    content_rendered: str


def get_nested(mapping: Mapping[str, Any], path: list[str], default: str = "") -> str:
    """Safely extract nested value or return default."""
    value = mapping
    for key in path:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return str(value)


def parse_posts(data: list[Mapping[str, Any]]) -> list[Post]:
    """Parse posts from JSON list."""
    return [
        Post(
            id=int(item["id"]),
            title_rendered=get_nested(item, ["title", "rendered"]),
            content_rendered=get_nested(item, ["content", "rendered"])
        )
        for item in data
    ]


def main():
    # === CONFIG ===
    INPUT_FILE = Path("source/flaven_posts_en_2.json")
    OUTPUT_FILE = Path("output_step_1_001_ingested_posts.json")
    
    # Load JSON
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Input file not found: {INPUT_FILE}")
        return
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {INPUT_FILE}: {e}")
        return
    
    if not isinstance(data, list):
        print("[ERROR] JSON root must be a list of posts.")
        return
    
    # Parse
    posts = parse_posts(data)
    
    # Save normalized output
    output = [{"id": p.id, "title_rendered": p.title_rendered, "content_rendered": p.content_rendered} for p in posts]
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] Parsed {len(posts)} posts from {INPUT_FILE}.")
    print(f"[INFO] Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()