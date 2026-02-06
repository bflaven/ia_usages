# WordPress Tags API Extractor

A Python script to fetch all tags from a WordPress site via the REST API and save them to a timestamped JSON file.

## Features

✅ **Complete pagination handling** - Automatically fetches all tags across multiple pages  
✅ **Configurable** - Easy-to-modify configuration section  
✅ **Error handling** - Automatic retries with exponential backoff  
✅ **Logging** - Detailed progress tracking  
✅ **Field filtering** - Extract only the fields you need  
✅ **Best practices** - Type hints, DRY principles, modular functions  

## Requirements

- Python 3.7+
- requests library

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make the script executable (optional):
```bash
chmod +x wordpress_tags_extractor.py
```

## Usage

### Basic Usage

Simply run the script with default configuration:

```bash
python wordpress_tags_extractor.py
```

This will:
- Fetch all tags from `https://flaven.fr/wp-json/wp/v2/tags`
- Save to `sample_all_tags_YYYYMMDD_HHMMSS.json` in the current directory

### Configuration

Edit the `CONFIG` dictionary at the top of the script to customize:

```python
CONFIG = {
    # Your WordPress API endpoint
    "api_url": "https://flaven.fr/wp-json/wp/v2/tags",
    
    # Number of tags per page (max 100)
    "per_page": 100,
    
    # Output directory
    "output_dir": ".",
    
    # Output filename pattern
    "output_filename_pattern": "sample_all_tags_{datetime}.json",
    
    # Datetime format for filename
    "datetime_format": "%Y%m%d_%H%M%S",
    
    # Fields to extract (None = all fields)
    "fields_to_extract": None,
    
    # Request timeout in seconds
    "timeout": 30,
    
    # Maximum retries for failed requests
    "max_retries": 3,
    
    # Enable verbose logging
    "verbose": True,
}
```

### Examples

#### Example 1: Extract Only Specific Fields

If you only need `id`, `name`, `slug`, and `count`:

```python
"fields_to_extract": ["id", "name", "slug", "count"]
```

#### Example 2: Change Output Directory

To save files to a `data` folder:

```python
"output_dir": "./data"
```

#### Example 3: Different WordPress Site

To fetch tags from another WordPress site:

```python
"api_url": "https://yoursite.com/wp-json/wp/v2/tags"
```

#### Example 4: Custom Filename Pattern

For a different naming convention:

```python
"output_filename_pattern": "wp_tags_backup_{datetime}.json",
"datetime_format": "%Y-%m-%d"
```

Output: `wp_tags_backup_2026-01-25.json`

## Available Tag Fields

Common WordPress tag fields you can extract:

- `id` - Tag ID
- `name` - Tag name
- `slug` - URL-friendly version
- `description` - Tag description
- `count` - Number of posts with this tag
- `link` - URL to tag archive
- `taxonomy` - Taxonomy name (usually "post_tag")
- `meta` - Metadata array

**Tip:** Set `fields_to_extract: None` to see all available fields in your output.

## Output Format

The script generates a JSON file with this structure:

```json
[
  {
    "id": 123,
    "name": "Python",
    "slug": "python",
    "description": "Python programming language",
    "count": 42,
    "link": "https://flaven.fr/tag/python/",
    "taxonomy": "post_tag",
    "meta": []
  },
  {
    "id": 124,
    "name": "WordPress",
    "slug": "wordpress",
    ...
  }
]
```

## Extending the Script

### Adding New Endpoints

To fetch categories instead of tags, change the API URL:

```python
"api_url": "https://flaven.fr/wp-json/wp/v2/categories"
```

### Adding Custom Processing

Add your custom processing function:

```python
def custom_process_tags(tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add custom processing logic here."""
    for tag in tags:
        # Example: Add a custom field
        tag['custom_field'] = tag['name'].upper()
    return tags
```

Then call it in `main()`:

```python
filtered_tags = filter_fields(all_tags, CONFIG["fields_to_extract"])
filtered_tags = custom_process_tags(filtered_tags)  # Add this line
```

## Error Handling

The script includes robust error handling:

- **Network errors**: Automatic retry with 3 attempts
- **Timeout**: Configurable timeout (default 30s)
- **API errors**: Proper HTTP status code checking
- **Logging**: Detailed error messages

## Troubleshooting

### "Connection timeout"
- Increase `timeout` value in CONFIG
- Check your internet connection
- Verify the WordPress site is accessible

### "404 Not Found"
- Verify the API endpoint URL
- Check if the WordPress site has REST API enabled
- Try accessing the URL directly in a browser

### "Empty results"
- The site might not have any tags
- Check if authentication is required
- Verify pagination settings

## License

Free to use and modify for your needs.

## Author

Bruno - AI Coordinator & Product Owner
