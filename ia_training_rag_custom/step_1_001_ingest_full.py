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
python step_1_001_ingest_full.py


"""

"""
step_1_001_ingest_full.py

Ingests all posts from a WordPress site via the REST API, 10 by 10,
using HTTP Basic Auth (e.g. protected by .htaccess).

Features:
- Paginates through /wp-json/wp/v2/posts until no more posts.
- Saves each page of results as a separate JSON file under ./source/.
- Consolidates all posts into one JSON file with a timestamped filename.
- Prints the total number of posts retrieved.
- Configurable pauses between HTTP calls and between each 10-page batch.

Update the CONFIG section only; the rest of the script should be reusable.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import requests
from requests.auth import HTTPBasicAuth


# =========================
# CONFIGURATION VARIABLES
# =========================

# Base URL of the WordPress site (no trailing slash)
BASE_URL: str = "https://flaven.fr"

# REST API endpoint for posts (relative to BASE_URL)
POSTS_ENDPOINT: str = "/wp-json/wp/v2/posts"

# HTTP Basic Auth credentials (for .htaccess protection)
# IMPORTANT: replace with your real credentials before running.
BASIC_AUTH_USERNAME: str = "your_username"
BASIC_AUTH_PASSWORD: str = "your_pasword"

# Pagination settings
PER_PAGE: int = 10        # number of posts per request
START_PAGE: int = 1       # usually 1
MAX_PAGES: Optional[int] = None  # safety limit; set to None for unlimited

# Output directories and filenames
SOURCE_DIR: Path = Path("source")  # directory to store raw page JSON files
CONSOLIDATED_PREFIX: str = "flaven_posts_full_"
CONSOLIDATED_SUFFIX: str = ".json"

# Network / request settings
REQUEST_TIMEOUT: int = 30  # seconds
VERIFY_SSL: bool = True    # set False only if you know what you're doing

# Throttling / pause settings (in seconds)
# Pause after each individual page fetch
PER_PAGE_PAUSE_SECONDS: float = 2.0
# Additional pause after each batch of N pages (e.g., every 10 pages)
BATCH_SIZE_FOR_PAUSE: int = 10
BATCH_PAUSE_SECONDS: float = 2.0


# =========================
# HELPER FUNCTIONS
# =========================

def ensure_directory(path: Path) -> None:
    """
    Ensure the given directory exists. Create it if missing.
    """
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def build_posts_url(base_url: str, endpoint: str) -> str:
    """
    Build the full URL for the posts endpoint.

    Args:
        base_url: Base URL of the site (no trailing slash ideally).
        endpoint: REST endpoint path, e.g. "/wp-json/wp/v2/posts".

    Returns:
        Full URL as a string.
    """
    return base_url.rstrip("/") + "/" + endpoint.lstrip("/")


def get_auth(username: str, password: str) -> HTTPBasicAuth:
    """
    Return a HTTPBasicAuth object for requests.
    """
    return HTTPBasicAuth(username, password)


def fetch_posts_page(
    session: requests.Session,
    url: str,
    page: int,
    per_page: int,
    auth: HTTPBasicAuth,
    timeout: int,
    verify_ssl: bool
) -> List[Dict[str, Any]]:
    """
    Fetch a single page of posts from the WordPress REST API.
    """
    params = {
        "page": page,
        "per_page": per_page,
    }

    response = session.get(
        url,
        params=params,
        auth=auth,
        timeout=timeout,
        verify=verify_ssl,
    )

    if response.status_code == 401:
        raise RuntimeError("Unauthorized (401): check your .htaccess username/password.")
    if response.status_code == 403:
        raise RuntimeError("Forbidden (403): check access rules on the server.")
    if response.status_code == 404:
        raise RuntimeError("Not found (404): check POSTS_ENDPOINT and BASE_URL.")
    if not response.ok:
        raise RuntimeError(
            f"HTTP error {response.status_code}: {response.text[:500]}"
        )

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to decode JSON for page {page}") from exc

    if not isinstance(data, list):
        raise RuntimeError(
            f"Unexpected JSON format for page {page}, expected list, got {type(data)}"
        )

    return data


def save_json(data: Any, path: Path) -> None:
    """
    Save Python data as pretty-printed JSON to a file.
    """
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_timestamp() -> str:
    """
    Generate a filesystem-safe timestamp string.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def consolidate_posts(all_posts: List[Dict[str, Any]]) -> str:
    """
    Create a timestamped filename and return it.
    """
    timestamp = generate_timestamp()
    filename = f"{CONSOLIDATED_PREFIX}{timestamp}{CONSOLIDATED_SUFFIX}"
    return filename


# =========================
# MAIN LOGIC
# =========================

def ingest_all_posts() -> None:
    """
    Ingest all posts from the WordPress REST API, 10 by 10, and:
    - Save each page of posts as JSON into SOURCE_DIR.
    - Consolidate all posts into a single timestamped JSON file.
    - Print the total number of posts retrieved.
    - Apply configurable pauses per page and per batch.
    """
    ensure_directory(SOURCE_DIR)

    posts_url = build_posts_url(BASE_URL, POSTS_ENDPOINT)
    auth = get_auth(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)

    session = requests.Session()

    all_posts: List[Dict[str, Any]] = []
    page = START_PAGE
    page_count = 0

    print(f"Starting ingestion from: {posts_url}")
    print(f"Pagination: {PER_PAGE} posts per page")
    print(f"Per-page pause: {PER_PAGE_PAUSE_SECONDS}s, "
          f"batch pause every {BATCH_SIZE_FOR_PAUSE} pages: {BATCH_PAUSE_SECONDS}s")

    while True:
        if MAX_PAGES is not None and page > MAX_PAGES:
            print(f"Reached MAX_PAGES limit ({MAX_PAGES}). Stopping.")
            break

        print(f"Fetching page {page} ...")

        try:
            posts = fetch_posts_page(
                session=session,
                url=posts_url,
                page=page,
                per_page=PER_PAGE,
                auth=auth,
                timeout=REQUEST_TIMEOUT,
                verify_ssl=VERIFY_SSL,
            )
        except Exception as exc:
            print(f"Error while fetching page {page}: {exc}", file=sys.stderr)
            break

        if not posts:
            print(f"No posts returned on page {page}. Assuming end of dataset.")
            break

        # Save this page to a JSON file under SOURCE_DIR
        page_filename = SOURCE_DIR / f"posts_page_{page:04d}.json"
        save_json(posts, page_filename)
        print(f"Saved {len(posts)} posts to {page_filename}")

        # Accumulate posts
        all_posts.extend(posts)
        page_count += 1

        # Per-page pause
        if PER_PAGE_PAUSE_SECONDS and PER_PAGE_PAUSE_SECONDS > 0:
            print(f"Sleeping {PER_PAGE_PAUSE_SECONDS}s after page {page} ...")
            time.sleep(PER_PAGE_PAUSE_SECONDS)

        # Batch pause every BATCH_SIZE_FOR_PAUSE pages
        if (
            BATCH_SIZE_FOR_PAUSE
            and BATCH_SIZE_FOR_PAUSE > 0
            and page_count % BATCH_SIZE_FOR_PAUSE == 0
        ):
            print(
                f"Completed {page_count} pages. "
                f"Sleeping additional {BATCH_PAUSE_SECONDS}s for batch pause ..."
            )
            if BATCH_PAUSE_SECONDS and BATCH_PAUSE_SECONDS > 0:
                time.sleep(BATCH_PAUSE_SECONDS)

        # Next page
        page += 1

    # Consolidate all posts into a single JSON file
    consolidated_filename = consolidate_posts(all_posts)
    consolidated_path = Path(consolidated_filename)
    save_json(all_posts, consolidated_path)

    print(f"\nIngestion complete.")
    print(f"Pages fetched: {page_count}")
    print(f"Total posts retrieved: {len(all_posts)}")
    print(f"Consolidated file: {consolidated_path.resolve()}")
    print(f"Individual page files are in: {SOURCE_DIR.resolve()}")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    ingest_all_posts()









