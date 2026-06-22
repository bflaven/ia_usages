# complete_breadcrumb_migration

Fill empty `actual_description` fields in breadcrumb migration JSON using Azure OpenAI. Outputs full JSON to `destination/`.

## Scripts

### `001_complete_breadcrumb_migration.py`

Reads source JSON, finds items with empty `actual_description`, generates English Wikidata-style descriptions via Azure OpenAI, writes full output JSON.

**Run:**
```bash
conda activate ia_achats
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_seo_ia_semantic_breadcrumb_webmcp/complete_breadcrumb_migration/
python 001_complete_breadcrumb_migration.py
```

**Input:** `source/breadcrumb_migration_bulk_description_20260622_145542.json`

**Output:** `destination/filed_[timestamp]_breadcrumb_migration_bulk_description_20260622_145542.json`

**Config (top of script):**
| Key | Default | Notes |
|-----|---------|-------|
| `MODEL` | `gpt-4.1-mini` | Azure deployment name |
| `TEMPERATURE` | `0.3` | Low for factual output |
| `TIMEOUT` | `30` | Seconds per API call |

## Environment

```
conda activate ia_achats   # Python 3.9.13
```

Requires `.env` in script directory:
```
API_KEY=...
ENDPOINT=https://...
```

## Directory structure

```
complete_breadcrumb_migration/
├── 001_complete_breadcrumb_migration.py
├── MODEL_007_poc_api_dtsi.py          # reference model
├── .env                               # Azure credentials (not committed)
├── source/
│   └── breadcrumb_migration_bulk_description_20260622_145542.json
└── destination/
    └── filed_[timestamp]_breadcrumb_migration_bulk_description_20260622_145542.json
```

## Changelog

### v1.0.0 — 2026-06-22

- Initial release
- Reads source JSON, detects items with empty `actual_description`
- Prints count + `tag_name` list for visual verification
- Generates English Wikidata-style descriptions via Azure OpenAI (`gpt-4.1-mini`)
- Writes full item array (filled + unchanged) to timestamped destination file
- Pattern based on `MODEL_007_poc_api_dtsi.py` (`AzureClient` factory, `CONFIG` class, `.env` loading)
