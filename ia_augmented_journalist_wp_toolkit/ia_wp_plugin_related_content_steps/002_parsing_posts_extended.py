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
pip install mistralai python-dotenv datauri

python -m pip install mistralai python-dotenv datauri


# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_related_content_steps

# launch the file
python 002_parsing_posts_extended.py


"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Sequence


@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: str | None = None


def get_nested(mapping: Mapping[str, Any],
               path: Sequence[str],
               default: Any = None) -> Any:
    """
    Safely get a nested value from a dict using a list/tuple path.
    Example: get_nested(item, ["title", "rendered"])
    """
    current: Any = mapping
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return default
        current = current[key]
    return current


def parse_post(item: Mapping[str, Any]) -> ParsedPost:
    """
    Parse a single post object from the WP-like JSON structure.
    Extend this function when you need more fields.
    """
    return ParsedPost(
        id=int(item["id"]),
        title_rendered=str(get_nested(item, ["title", "rendered"], "")),
        content=str(get_nested(item, ["content", "rendered"], "")),
        slug=str(get_nested(item, ["slug"], "")),
    )


def parse_posts(items: Iterable[Mapping[str, Any]]) -> List[ParsedPost]:
    """
    Parse a sequence of post items into a list of ParsedPost objects.
    """
    return [parse_post(item) for item in items]


def load_json_file(path: str | Path) -> Any:
    """
    Load JSON from a file path.
    """
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    # Assumes the JSON file is in the same directory as this script.
    json_path = "sample_posts_2020_to_2025.json"

    raw = load_json_file(json_path)
    posts = parse_posts(raw)

    for post in posts:
        print(f"id={post.id}")
        print(f"slug={post.slug}")
        print(f"title_rendered={post.title_rendered}")
        print(f"content={post.content!r}")
        print("-" * 40)


if __name__ == "__main__":
    main()










