## PROMPT_1
As a python and IA expert, let's start coding the `1. Decide what to vectorize per post`



## OUTPUT_1
You can treat this as defining a clean, testable “text builder” layer on top of your `ParsedPost` objects: one function to clean content, one to assemble the final text to vectorize.

Below is a concrete, copy‑pasteable implementation for STEP_1.1: “decide what to vectorize per post”, with simple HTML stripping and whitespace normalization, but still independent from any embedding model.

```python
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Optional


# This is the same structure you already parse from the JSON.
@dataclass
class ParsedPost:
    id: int
    title_rendered: str
    content: str
    slug: Optional[str] = None


# ---------- Low-level text helpers ----------

_HTML_TAG_RE = re.compile(r"<[^>]+>")  # simple HTML tag stripper


def strip_html_tags(text: str) -> str:
    """
    Remove HTML tags from a string.
    Good enough for WP content cleaning before embeddings.
    """
    # First unescape HTML entities (&amp;, &quot;, etc.)
    unescaped = html.unescape(text)
    # Then remove tags.
    return _HTML_TAG_RE.sub("", unescaped)


def normalize_whitespace(text: str) -> str:
    """
    Collapse multiple whitespace characters into single spaces and strip.
    """
    return re.sub(r"\s+", " ", text).strip()


# ---------- Post -> text to embed ----------

def build_post_text(
    post: ParsedPost,
    max_chars: int | None = None,
    include_slug: bool = False,
) -> str:
    """
    Build the final text representation for a post that will be vectorized.

    Strategy:
      - Always include the title.
      - Include cleaned content if present.
      - Optionally include slug (can help for SEO-like signals).
      - Optionally truncate to `max_chars` to keep embedding cost bounded.
    """
    title = normalize_whitespace(post.title_rendered)

    content_raw = post.content or ""
    content_clean = normalize_whitespace(strip_html_tags(content_raw))

    parts: list[str] = []

    # Title is always there
    if title:
        parts.append(f"TITLE: {title}")

    # Content if not empty
    if content_clean:
        parts.append(f"CONTENT: {content_clean}")

    # Optional slug
    if include_slug and post.slug:
        parts.append(f"SLUG: {post.slug}")

    full_text = "\n\n".join(parts)

    if max_chars is not None and len(full_text) > max_chars:
        full_text = full_text[:max_chars]

    return full_text
```

### How to use this in your pipeline

- After you parse the JSON into `ParsedPost` objects, call:

```python
text = build_post_text(post, max_chars=4000, include_slug=False)
```

- This `text` becomes the input for your embedding model in the next step.  
- You can later tweak:
  - Whether to include the slug.  
  - The `max_chars` value.  
  - The HTML cleaning strategy (switch to BeautifulSoup if your HTML becomes more complex). [stackoverflow](https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python)