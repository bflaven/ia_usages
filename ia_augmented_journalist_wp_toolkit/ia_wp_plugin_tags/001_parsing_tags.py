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
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_augmented_journalist_wp_toolkit/ia_wp_plugin_tags

# launch the file
python 001_parsing_tags.py


"""

"""
WordPress Tags API Extractor
-----------------------------
Fetches all tags from a WordPress site via REST API and saves them to a JSON file.

Author: Bruno
Date: 2026-01-25
"""

import requests
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys


# ============================================================================
# CONFIGURATION SECTION - Edit these parameters as needed
# ============================================================================

CONFIG = {
    # WordPress API endpoint (without pagination parameters)
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    
    # Number of tags per page (WordPress default is 10, max is 100)
    "per_page": 100,
    
    # Output directory for JSON files
    "output_dir": ".",
    
    # Output filename pattern (datetime will be inserted)
    "output_filename_pattern": "sample_all_tags_{datetime}.json",
    
    # Datetime format for filename
    "datetime_format": "%Y%m%d_%H%M%S",
    
    # Fields to extract from each tag (set to None to get all fields)
    # Example: ["id", "name", "slug", "description", "count"]
    "fields_to_extract": None,  # None = all fields
    
    # Request timeout in seconds
    "timeout": 30,
    
    # Maximum number of retries for failed requests
    "max_retries": 3,
    
    # Enable detailed logging
    "verbose": True,
}


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging(verbose: bool = True) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


# ============================================================================
# API INTERACTION FUNCTIONS
# ============================================================================

def fetch_tags_page(
    url: str, 
    page: int, 
    per_page: int, 
    timeout: int,
    retries: int = 0,
    max_retries: int = 3
) -> tuple[List[Dict[str, Any]], Optional[int]]:
    """
    Fetch a single page of tags from the WordPress API.
    
    Args:
        url: Base API URL
        page: Page number to fetch
        per_page: Number of items per page
        timeout: Request timeout in seconds
        retries: Current retry count
        max_retries: Maximum number of retries
    
    Returns:
        Tuple of (list of tags, total number of pages)
    
    Raises:
        requests.RequestException: If request fails after all retries
    """
    params = {
        "page": page,
        "per_page": per_page,
    }
    
    try:
        logging.info(f"Fetching page {page} (per_page={per_page})...")
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        
        # Get total pages from headers
        total_pages = response.headers.get('X-WP-TotalPages')
        total_pages = int(total_pages) if total_pages else None
        
        logging.debug(f"Successfully fetched page {page}. Total pages: {total_pages}")
        
        return response.json(), total_pages
    
    except requests.RequestException as e:
        if retries < max_retries:
            logging.warning(f"Request failed (attempt {retries + 1}/{max_retries}): {e}")
            logging.info(f"Retrying in 2 seconds...")
            import time
            time.sleep(2)
            return fetch_tags_page(url, page, per_page, timeout, retries + 1, max_retries)
        else:
            logging.error(f"Failed to fetch page {page} after {max_retries} retries: {e}")
            raise


def fetch_all_tags(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetch all tags from the WordPress API with pagination handling.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        List of all tags
    """
    all_tags = []
    page = 1
    total_pages = None
    
    while True:
        tags, total_pages_from_response = fetch_tags_page(
            url=config["api_url"],
            page=page,
            per_page=config["per_page"],
            timeout=config["timeout"],
            max_retries=config["max_retries"]
        )
        
        if total_pages is None and total_pages_from_response:
            total_pages = total_pages_from_response
            logging.info(f"Total pages to fetch: {total_pages}")
        
        all_tags.extend(tags)
        logging.info(f"Collected {len(tags)} tags from page {page}. Total so far: {len(all_tags)}")
        
        # Check if we've reached the last page
        if not tags or (total_pages and page >= total_pages):
            break
        
        page += 1
    
    return all_tags


# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def filter_fields(tags: List[Dict[str, Any]], fields: Optional[List[str]]) -> List[Dict[str, Any]]:
    """
    Filter tags to include only specified fields.
    
    Args:
        tags: List of tag dictionaries
        fields: List of field names to keep, or None to keep all fields
    
    Returns:
        List of filtered tag dictionaries
    """
    if fields is None:
        return tags
    
    logging.info(f"Filtering tags to include only fields: {', '.join(fields)}")
    
    filtered_tags = []
    for tag in tags:
        filtered_tag = {field: tag.get(field) for field in fields if field in tag}
        filtered_tags.append(filtered_tag)
    
    return filtered_tags


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def save_to_json(data: List[Dict[str, Any]], config: Dict[str, Any]) -> Path:
    """
    Save data to a JSON file with timestamped filename.
    
    Args:
        data: Data to save
        config: Configuration dictionary
    
    Returns:
        Path to the saved file
    """
    # Generate filename with current datetime
    current_datetime = datetime.now().strftime(config["datetime_format"])
    filename = config["output_filename_pattern"].format(datetime=current_datetime)
    
    # Create output directory if it doesn't exist
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Full file path
    filepath = output_dir / filename
    
    # Save to JSON file
    logging.info(f"Saving {len(data)} tags to {filepath}...")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logging.info(f"Successfully saved to {filepath}")
    
    return filepath


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main() -> None:
    """Main execution function."""
    # Setup logging
    setup_logging(CONFIG["verbose"])
    
    logging.info("=" * 70)
    logging.info("WordPress Tags API Extractor")
    logging.info("=" * 70)
    logging.info(f"API URL: {CONFIG['api_url']}")
    logging.info(f"Per page: {CONFIG['per_page']}")
    logging.info("")
    
    try:
        # Fetch all tags
        logging.info("Starting tag extraction...")
        all_tags = fetch_all_tags(CONFIG)
        logging.info(f"Successfully fetched {len(all_tags)} tags in total")
        
        # Filter fields if specified
        filtered_tags = filter_fields(all_tags, CONFIG["fields_to_extract"])
        
        # Save to JSON file
        filepath = save_to_json(filtered_tags, CONFIG)
        
        # Summary
        logging.info("")
        logging.info("=" * 70)
        logging.info("SUMMARY")
        logging.info("=" * 70)
        logging.info(f"Total tags extracted: {len(filtered_tags)}")
        logging.info(f"Output file: {filepath}")
        logging.info(f"File size: {filepath.stat().st_size / 1024:.2f} KB")
        logging.info("=" * 70)
        logging.info("Extraction completed successfully! ✓")
        
    except requests.RequestException as e:
        logging.error(f"Network error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()










