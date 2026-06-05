# Breadcrumb Migration — Taxonomy Exporter

WordPress plugin. Exports `category` or `post_tag` taxonomies to JSON/CSV for use with the breadcrumb-migration pipeline (Step 1 — inventory).

**Version:** 1.4.0  
**Requires:** WordPress 6.0+, PHP 8.0+  
**Capability:** `manage_options` (admin only)  
**Companion to:** `breadcrumb-migration` main plugin

---

## Installation

1. Copy `breadcrumb-migration-taxonomy-exporter/` into `wp-content/plugins/`
2. Activate in **Plugins > Installed Plugins**
3. Navigate to **Settings > Tax Export**

No database tables created. No activation hook. No deactivation hook.

---

## Usage

### Admin page

**Settings > Tax Export** (`/wp-admin/options-general.php?page=tax-export-v4`)

| Field | Options | Default |
|-------|---------|---------|
| Taxonomy | `category`, `post_tag` | `category` |
| Format | `csv`, `json` | `csv` |
| Limit | 1–5000 terms | `100` |
| Dry Run | checkbox | unchecked |

**Dry run ON:** counts terms, shows result, writes no file.  
**Dry run OFF:** writes file to WordPress uploads dir, shows download link.

### Output files

Files land in the **current month's upload folder** (`wp-content/uploads/YYYY/MM/`).

**Filename convention:**
```
{taxonomy}_{YYYYMMDDTHHMMSS+TZ}_step_1_inventory.{format}
```

Examples:
```
category_20260513T142301+0200_step_1_inventory.json
post_tag_20260513T142301+0200_step_1_inventory.csv
```

The `step_1_inventory` suffix matches the pipeline glob pattern `*_step_1_inventory.*`.

### Recent exports panel

Bottom of the page lists the last 10 `*step_1_inventory.*` files in the current upload month, with download links, timestamps, and file sizes.

---

## Export formats

### JSON

```json
{
  "timestamp": "2026-05-13T14:23:01+02:00",
  "pipeline_step": "inventory",
  "taxonomy": "category",
  "total_processed": 42,
  "config": {
    "limit": 100,
    "dry_run": false,
    "taxonomy": "category"
  },
  "data": [
    {
      "id": 5,
      "name": "Technology",
      "slug": "technology",
      "taxonomy": "category",
      "post_count": 12,
      "parent_id": 0
    }
  ]
}
```

### CSV

```
taxonomy,id,name,slug,post_count,parent_id
category,5,"Technology",technology,12,0
```

Names with double-quotes are escaped (`"` → `""`).

---

## File reference

### `wp-taxonomy-exporter.php`

Single-file plugin. All logic inline.

| Function / Hook | Purpose |
|-----------------|---------|
| `admin_menu` action | Registers submenu under Settings |
| `TAX_EXPORT_V4_PAGE()` | Renders form, handles POST, writes export file |

**POST handling** (`$_SERVER['REQUEST_METHOD'] === 'POST'`):

1. Sanitizes `taxonomy` (whitelist: `category`, `post_tag`), `format`, `limit` (clamped 1–5000), `dry_run`
2. Calls `get_terms()` with `hide_empty => false`
3. Dry run → display count, stop
4. Real run → build data array, serialize to JSON or CSV, write via `file_put_contents()` to `wp_upload_dir()['path']`, return download URL

**No nonce verification** — intentional for internal dev/staging use. Do not expose on public production sites.

---

## Security notes

- Access gate: `current_user_can('manage_options')` — admin only
- Taxonomy input whitelisted to `['category', 'post_tag']`
- Limit clamped: `max(1, min(5000, intval(...)))`
- Download URLs escaped with `esc_url()`
- **No CSRF nonce** — plugin header documents this explicitly. Add nonce if deploying outside trusted environments

---

## Integration with breadcrumb-migration pipeline

This plugin produces the Step 1 input consumed by `002_step_2_spacy_ner.py` and subsequent pipeline scripts.

Typical workflow:

```
[WP Admin] Tax Export → category_TIMESTAMP_step_1_inventory.json
    ↓
[Python] 002_step_2_spacy_ner.py --input category_TIMESTAMP_step_1_inventory.json
    ↓
[Python] 003_step_3_wikidata_enrich.py
    ↓
[Python] 004_step_4_proposals.py
    ↓
[WP Plugin] breadcrumb-migration → Import & validate proposals
```

Download the export from the admin page, place it in `source/pipeline/exports/`, then run the pipeline.

---

## Changelog

### v1.4.0 — 2026-05-13
- Stable release. Single-file architecture. No activation/deactivation hooks.
- Dry-run mode, JSON + CSV dual export, recent-exports panel.
- Filename convention aligned with `step_1_inventory` pipeline standard.

### v1.0.0 — initial
- Basic taxonomy export to CSV only.
