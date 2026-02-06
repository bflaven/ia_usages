## PROMPT_1


As a python expert, can you write a script in python that will:

1. parse the json object and grab for each items the value in `title > rendered` into a value name `title_rendered` and grab also the value in content into `content`.

2. Keep in mind that I want to have best practices, cut and paste the script for direct use, use function and DRY principles, make the update easy if I want to add some fields to be parsed.





```json
[
  {
    "id": 13091,
    "date": "2025-11-24T08:34:25",
    "date_gmt": "2025-11-24T07:34:25",
    "guid": {
      "rendered": "https://flaven.fr/?p=13091"
    },
    "modified": "2025-11-29T10:05:06",
    "modified_gmt": "2025-11-29T09:05:06",
    "slug": "ai-agentic-browsers-and-the-end-of-digital-autonomy",
    "status": "publish",
    "type": "post",
    "link": "https://flaven.fr/2025/11/ai-agentic-browsers-and-the-end-of-digital-autonomy/",
    "title": {
      "rendered": "AI, Agentic Browsers and the End of Digital Autonomy"
    },
    "content": {
      "rendered": "",
      "protected": false
    },
    "excerpt": {
      "rendered": "",
      "protected": false
    },
    "author": 1
  },
  {
    "id": 13070,
    "date": "2025-10-04T07:59:32",
    "date_gmt": "2025-10-04T05:59:32",
    "guid": {
      "rendered": "https://flaven.fr/?p=13070"
    },
    "modified": "2025-10-16T06:05:00",
    "modified_gmt": "2025-10-16T04:05:00",
    "slug": "rescuing-failed-ai-implementations-practical-explorations-with-n8n-ollama-geo",
    "status": "publish",
    "type": "post",
    "link": "https://flaven.fr/2025/10/rescuing-failed-ai-implementations-practical-explorations-with-n8n-ollama-geo/",
    "title": {
      "rendered": "Rescuing Failed AI Implementations + Practical Explorations with n8n, Ollama &#038; GEO"
    },
    "content": {
      "rendered": "",
      "protected": false
    },
    "excerpt": {
      "rendered": "",
      "protected": false
    },
    "author": 1
  }
]
```


## OUTPUT_1

Here is the same script, rewritten to include the `slug` field in a DRY, easily-extendable way.

```python
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
```

To add more fields later, extend `ParsedPost` with new attributes and use `get_nested` inside `parse_post` to map them from the JSON structure, keeping the rest of the script unchanged. [stackoverflow](https://stackoverflow.com/questions/70809438/python-dataclasses-with-optional-attributes)


