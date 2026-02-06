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
python 003_parsing_posts_vectorize_per_post.py


"""
from __future__ import annotations

import json
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional, Sequence


# ---------- Parsing JSON into ParsedPost ----------

@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


def get_nested(mapping: Mapping[str, Any],
               path: Sequence[str],
               default: Any = None) -> Any:
    current: Any = mapping
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return default
        current = current[key]
    return current


def parse_post(item: Mapping[str, Any]) -> ParsedPost:
    return ParsedPost(
        id=int(item["id"]),
        title_rendered=str(get_nested(item, ["title", "rendered"], "")),
        content=str(get_nested(item, ["content", "rendered"], "")),
        slug=str(get_nested(item, ["slug"], "")),
    )


def parse_posts(items: Iterable[Mapping[str, Any]]) -> List[ParsedPost]:
    return [parse_post(item) for item in items]


def load_json_file(path: str | Path) -> Any:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Text building for vectorization ----------

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def strip_html_tags(text: str) -> str:
    unescaped = html.unescape(text)
    return _HTML_TAG_RE.sub("", unescaped)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def build_post_text(
    post: ParsedPost,
    max_chars: int | None = None,
    include_slug: bool = False,
) -> str:
    title = normalize_whitespace(post.title_rendered)
    content_raw = post.content or ""
    content_clean = normalize_whitespace(strip_html_tags(content_raw))

    parts: list[str] = []

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


# ---------- Example usage (where `post` is defined) ----------

def main() -> None:
    json_path = "sample_posts_2020_to_2025.json"

    raw = load_json_file(json_path)
    posts = parse_posts(raw)

    for post in posts:
        text = build_post_text(post, max_chars=4000, include_slug=False)
        print(f"Post id={post.id}")
        print(text[:300], "...\n")  # preview


if __name__ == "__main__":
    main()











