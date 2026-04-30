# Semaphore

**Version:** 1.2.4  
**Author:** Bruno Flaven & IA  
**Text Domain:** `semaphore`  
**Requires:** WordPress 5.8+, PHP 7.4+

Semantic clustering plugin for WordPress. Provides related posts (via embedding similarity), tag family grouping, a semantic sidebar widget, breadcrumbs, and Schema.org JSON-LD — all as a pure overlay that never modifies your actual post tags or content.

---

## How it works

Semaphore adds two custom database tables to store pre-computed semantic data:

| Table | Purpose |
|---|---|
| `{prefix}related_posts_embeddings` | Post-to-post similarity scores, computed externally (e.g. via Python + sentence-transformers) and imported via CSV |
| `{prefix}tag_families` | Tag grouping overlay: canonical tags, member tags, similarity scores, and usage counts |

You compute the data outside WordPress, import it via CSV, and Semaphore serves it on the front end through shortcodes and a sidebar widget.

---

## Admin screens

All screens live under the **Semaphore** top-level menu in the WordPress sidebar.

### Settings (`?page=semaphore`)

Feature toggles:

| Option | Default | Description |
|---|---|---|
| Debug mode | Off | Show debug blocks inside the semantic sidebar |
| Semantic Sidebar | On | Enable the sidebar widget / `[semaphore_sidebar]` shortcode |
| Footer Related Content | On | Append related posts/tags after post content |
| Breadcrumbs | On | Enable semantic breadcrumb functions |
| Schema.org JSON-LD | On | Output breadcrumb & tag archive structured data in `<head>` |

---

### Related Embeddings (`?page=semaphore-related`)

Manages the `{prefix}related_posts_embeddings` table.

**CSV Import**

Expected format (header row required):

```
post_id,related_post_id,similarity,rank
```

- `post_id` — base post ID (integer)
- `related_post_id` — related post ID (integer)
- `similarity` — score between 0 and 1 (decimal point or decimal comma accepted)
- `rank` — ordering position (integer, starting at 1)

Options:
- **Truncate table before import** — deletes all existing rows before inserting

**CSV Export** *(added in 1.2.3)*

Downloads the full current contents of `{prefix}related_posts_embeddings` as a CSV file named `related_posts_embeddings_YYYY-MM-DD.csv`. The file is UTF-8 with BOM (Excel-compatible). The export button is only shown when the table exists and contains at least one row.

---

### Tag Families CSV (`?page=semaphore-families-csv`)

Manages the `{prefix}tag_families` table.

**CSV Import**

Expected format (header row required):

```
family_id,canonical_tag_id,canonical_label,tag_id,tag_label,similarity_to_canonical,usage_count,entity_label
```

| Column | Type | Description |
|---|---|---|
| `family_id` | integer | Family group identifier |
| `canonical_tag_id` | integer | Term ID of the family's canonical (representative) tag |
| `canonical_label` | string | Name of the canonical tag |
| `tag_id` | integer | Term ID of the member tag |
| `tag_label` | string | Name of the member tag |
| `similarity_to_canonical` | float | Semantic similarity score (0–1) |
| `usage_count` | integer | Number of published posts using this tag |
| `entity_label` | string | NER entity type (e.g. `PER`, `LOC`, `O`) |

Options:
- **Truncate table before import** — deletes all existing rows before inserting

**CSV Export** *(added in 1.2.3)*

Downloads the full current contents of `{prefix}tag_families` as `tag_families_YYYY-MM-DD.csv`. Same UTF-8 BOM format, button only shown when data exists.

---

### Tag Families Manager (`?page=semaphore-dashboard`)

A JavaScript-driven UI for managing tag families directly in the admin without editing CSVs.

**Layout**

- **All Tags** (left) — paginated list of all `post_tag` terms, searchable by name or ID
- **Tag Families** (right, top) — list of all families with member count, searchable by label or family ID
- **Family Members** (right, bottom) — members of the currently selected family

**Actions**

| Button | Requires | Effect |
|---|---|---|
| Convert selected tag to family | A tag selected in All Tags | Creates a new family with that tag as its canonical member |
| Attach selected tag to current family | A tag + a family selected | Adds the tag as a member of the selected family |
| Detach selected member from current family | A family + a member selected | Removes that member from the family |

All actions are AJAX-based, nonce-verified, and require `manage_options` capability.

> **Note:** The `usage_count` field is kept in sync automatically. Whenever post tags are saved in the WordPress editor, a `set_object_terms` hook re-counts published posts per tag and updates `{prefix}tag_families.usage_count` accordingly.

---

## Shortcodes

| Shortcode | Attributes | Output |
|---|---|---|
| `[semaphore_related_posts]` | `post_id`, `limit`, `title` | Grid of related posts pulled from `{prefix}related_posts_embeddings` |
| `[semaphore_related_tags]` | `tag_id`, `limit`, `title` | Badge list of semantically related tags from `{prefix}tag_families` |
| `[semaphore_sidebar]` | — | Full semantic sidebar (related posts + related tags combined) |

Custom related post order can be set per-post via the **Semaphore – Related Posts** meta box on the post edit screen (drag to reorder, toggle custom selection mode, search to add posts).

---

## Frontend features

- **Semantic sidebar widget** — registers as a standard WordPress widget; also available via `[semaphore_sidebar]`
- **Breadcrumbs** — `semaphore_breadcrumbs()` template function; outputs semantic breadcrumbs for single posts, tag archives, category archives, and pages
- **Schema.org JSON-LD** — outputs `BreadcrumbList` and tag archive structured data in `<head>` when enabled

---

## Installation

1. Upload the `semaphore/` folder to `/wp-content/plugins/`.
2. Activate via **Plugins** in the WordPress admin.
3. On activation, both database tables are created automatically.
4. Go to **Semaphore → Related Embeddings** and import your embeddings CSV.
5. Go to **Semaphore → Tag Families CSV** and import your tag families CSV.
6. Use shortcodes or the sidebar widget in your theme.

---

## Uninstall

Delete the plugin from **Plugins → Installed Plugins → Delete**.

On deletion WordPress runs `uninstall.php`, which:
- Drops `{prefix}related_posts_embeddings`
- Drops `{prefix}tag_families`
- Deletes all five plugin options (`semaphore_debug`, `semaphore_enable_sidebar`, `semaphore_enable_footer`, `semaphore_enable_breadcrumbs`, `semaphore_enable_schema`)

Deactivating the plugin (without deleting) does **not** remove any data.

---

## File structure

```
semaphore/
├── semaphore.php                          # Main plugin file
├── uninstall.php                          # Runs on plugin deletion — drops tables & options
├── inc/
│   └── tag-families-usage-sync.php        # Auto-syncs usage_count on set_object_terms
└── assets/
    ├── css/
    │   ├── bf-semantic-seo-styles.css     # Frontend styles
    │   └── semaphore-admin.css            # Admin styles
    └── js/
        └── semaphore-families-manager.js  # Dashboard AJAX UI
```

---

## Changelog

### 1.2.4
- Added `uninstall.php` — the WordPress-recommended uninstall mechanism. Drops both tables and removes all plugin options when the plugin is deleted. Replaces the previous `register_uninstall_hook` approach, which depended on the plugin loading successfully at delete time.

### 1.2.3
- Moved all admin pages from **Settings** submenu to a dedicated **Semaphore** top-level sidebar menu (icon: chart-area). Submenus: Settings · Related Embeddings · Tag Families CSV · Tag Families Manager.
- Fixed Tag Families Manager dashboard (all AJAX features broken after 1.2.2): the admin script enqueue hook name was still `settings_page_semaphore-dashboard`; corrected to `semaphore_page_semaphore-dashboard` to match the new top-level menu parent.
- Added **CSV Export** to the Related Embeddings page — downloads `{prefix}related_posts_embeddings` as `related_posts_embeddings_YYYY-MM-DD.csv`.
- Added **CSV Export** to the Tag Families CSV page — downloads `{prefix}tag_families` as `tag_families_YYYY-MM-DD.csv`.
- Both exports are nonce-verified, capability-checked (`manage_options`), and UTF-8 BOM encoded for Excel compatibility.

### 1.2.2
- Initial reference version for this changelog.
