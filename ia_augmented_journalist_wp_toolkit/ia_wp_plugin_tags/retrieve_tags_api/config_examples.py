#!/usr/bin/env python3
"""
Example configurations for WordPress Tags Extractor
Copy these to the CONFIG dictionary in wordpress_tags_extractor.py
"""

# =============================================================================
# EXAMPLE 1: Minimal configuration (all fields, current directory)
# =============================================================================
CONFIG_MINIMAL = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": ".",
    "output_filename_pattern": "sample_all_tags_{datetime}.json",
    "datetime_format": "%Y%m%d_%H%M%S",
    "fields_to_extract": None,
    "timeout": 30,
    "max_retries": 3,
    "verbose": True,
}

# =============================================================================
# EXAMPLE 2: Minimal fields (ID, name, slug, count only)
# =============================================================================
CONFIG_MINIMAL_FIELDS = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": "./exports",
    "output_filename_pattern": "tags_minimal_{datetime}.json",
    "datetime_format": "%Y%m%d_%H%M%S",
    "fields_to_extract": ["id", "name", "slug", "count"],  # Only these fields
    "timeout": 30,
    "max_retries": 3,
    "verbose": True,
}

# =============================================================================
# EXAMPLE 3: Complete tag export with metadata
# =============================================================================
CONFIG_COMPLETE = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": "./backups",
    "output_filename_pattern": "full_tags_backup_{datetime}.json",
    "datetime_format": "%Y-%m-%d_%H-%M-%S",
    "fields_to_extract": [
        "id",
        "count",
        "description",
        "link",
        "name",
        "slug",
        "taxonomy",
        "meta"
    ],
    "timeout": 30,
    "max_retries": 3,
    "verbose": True,
}

# =============================================================================
# EXAMPLE 4: Production configuration (organized output, quiet mode)
# =============================================================================
CONFIG_PRODUCTION = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": "./data/wordpress/tags",
    "output_filename_pattern": "wp_tags_{datetime}.json",
    "datetime_format": "%Y%m%d",
    "fields_to_extract": None,
    "timeout": 60,
    "max_retries": 5,
    "verbose": False,  # Less verbose for production
}

# =============================================================================
# EXAMPLE 5: Multiple WordPress sites
# =============================================================================
CONFIG_SITE_1 = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": "./data/site1",
    "output_filename_pattern": "flaven_tags_{datetime}.json",
    "datetime_format": "%Y%m%d_%H%M%S",
    "fields_to_extract": None,
    "timeout": 30,
    "max_retries": 3,
    "verbose": True,
}

CONFIG_SITE_2 = {
    "api_url": "https://example.com/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": "./data/site2",
    "output_filename_pattern": "example_tags_{datetime}.json",
    "datetime_format": "%Y%m%d_%H%M%S",
    "fields_to_extract": None,
    "timeout": 30,
    "max_retries": 3,
    "verbose": True,
}

# =============================================================================
# EXAMPLE 6: Analytics/Statistics focused
# =============================================================================
CONFIG_ANALYTICS = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": "./analytics",
    "output_filename_pattern": "tag_stats_{datetime}.json",
    "datetime_format": "%Y%m%d",
    "fields_to_extract": ["id", "name", "count", "slug"],  # For usage analysis
    "timeout": 30,
    "max_retries": 3,
    "verbose": True,
}

# =============================================================================
# EXAMPLE 7: Categories instead of tags
# =============================================================================
CONFIG_CATEGORIES = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/categories",  # Categories endpoint
    "per_page": 100,
    "output_dir": ".",
    "output_filename_pattern": "sample_all_categories_{datetime}.json",
    "datetime_format": "%Y%m%d_%H%M%S",
    "fields_to_extract": None,
    "timeout": 30,
    "max_retries": 3,
    "verbose": True,
}

# =============================================================================
# EXAMPLE 8: Daily automated backup
# =============================================================================
CONFIG_DAILY_BACKUP = {
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    "per_page": 100,
    "output_dir": "./backups/daily",
    "output_filename_pattern": "tags_daily_{datetime}.json",
    "datetime_format": "%Y-%m-%d",  # Daily date format
    "fields_to_extract": None,
    "timeout": 60,
    "max_retries": 5,
    "verbose": False,
}
