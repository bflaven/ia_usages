# Breadcrumb Migration — WordPress Plugin

> Validate spaCy/Wikidata pipeline proposals and publish enriched taxonomy terms to WordPress.

---

## Overview

This plugin is the **validation and publication layer** of the breadcrumb migration pipeline. It reads enriched proposals written by the Python pipeline into custom MySQL tables and lets an admin:

1. **Simulate** the proposed breadcrumb path before committing
2. **Edit** the proposed name, slug, or description inline
3. **Validate** or **Reject** each proposal
4. **Publish** approved proposals to WordPress (updates the live WP term + creates a 301 redirect)

The plugin **never touches original WordPress tables** during the pipeline phase. Only the **Publish** action writes to `wp_terms` / `wp_term_taxonomy` — after explicit human approval.

---

## Plugin structure

```
wp-plugin-breadcrumb-migration/
├── breadcrumb-migration.php          ← Main entry point
├── uninstall.php                     ← Drops tables on plugin deletion
├── includes/
│   ├── db-tables.php                 ← Table creation via dbDelta (on activation)
│   ├── admin-page.php                ← Tab UI: Proposals / Delta / Import-Export / Settings / Danger Zone
│   ├── ajax-handler.php              ← AJAX endpoints (validate/simulate/edit/publish/empty/delta/wikidata-search)
│   ├── import-export.php             ← admin-post handlers: import file + export CSV
│   └── breadcrumb-simulator.php      ← Breadcrumb renderer + parent-chain walker
└── assets/
    ├── admin.css                     ← Responsive 2-column grid, tabs, danger zone styles
    └── admin.js                      ← jQuery AJAX for all actions + flash notices
```

---

## Requirements

| Requirement | Version |
|---|---|
| WordPress | 6.5+ |
| MySQL | 8.0 |
| PHP | 8.0+ |
| User capability | `manage_options` (Administrator) |

The Python pipeline must have populated `wp_breadcrumb_terms` and `wp_breadcrumb_proposals` before the plugin UI shows any data. For new tags added after the pipeline ran, use the **Delta — New Tags** tab to add them manually.

---

## Installation

### Deploy to Docker staging

The plugin source in `plugin/` maps to the WP plugins directory:

```bash
# Already deployed to Docker WP — plugin is at:
wp_docker/wordpress/wp-content/plugins/breadcrumb-migration/

# If you need to re-sync from plugin/ source:
cp -r plugin/. wp_docker/wordpress/wp-content/plugins/breadcrumb-migration/
```

### Activate

```
http://localhost:8080/wp-admin/plugins.php
→ Find "Breadcrumb Migration"
→ Click Activate
```

On activation, the plugin automatically creates the 3 custom tables via `dbDelta()`. No SQL file import needed.

---

## Database tables

Created on activation, dropped on deletion. Never modified by deactivation.

### `wp_breadcrumb_terms`
Snapshot of original WordPress terms — read from WP, never written back during pipeline.

| Column | Type | Description |
|---|---|---|
| `id` | BIGINT | Internal primary key |
| `wp_term_id` | BIGINT | Original WP `term_id` |
| `taxonomy` | VARCHAR(32) | `category` or `post_tag` |
| `original_name` | VARCHAR(200) | Original term name |
| `original_slug` | VARCHAR(200) | Original slug |
| `original_parent_id` | BIGINT | Parent term (categories) |
| `content_count` | INT | Posts attached |
| `status` | VARCHAR | `original` → `proposed` → `validated` → `published` |

### `wp_breadcrumb_proposals`
Enriched proposals from the pipeline. One row per term (upserted on re-run).

| Column | Type | Description |
|---|---|---|
| `term_id` | BIGINT | FK → `wp_breadcrumb_terms.id` |
| `proposed_name` | VARCHAR(200) | Proposed name |
| `proposed_slug` | VARCHAR(200) | Proposed slug |
| `proposed_description` | TEXT | Proposed description |
| `spacy_entity` | VARCHAR(32) | NER type: `PERSON`, `ORG`, `LOC`, `MISC` |
| `wikidata_id` | VARCHAR(50) | e.g. `Q11660` |
| `wikidata_label` | VARCHAR(200) | Wikidata label (fr → en fallback) |
| `wikidata_description` | TEXT | Wikidata description (fr → en fallback) |
| `proposed_parent_id` | BIGINT | WP `term_id` of parent category (post_tag only — replaces "Tag" in breadcrumb) |
| `proposed_breadcrumb` | TEXT | JSON array: `["Home","Tags","Term Name"]` or `["Home","webdoc","Term Name"]` |
| `validation_state` | VARCHAR | `pending` → `approved` or `rejected` |
| `validated_by` | BIGINT | WP user ID who validated |
| `validated_at` | DATETIME | Timestamp of validation |

### `wp_breadcrumb_redirects`
301/302 redirect map. Populated automatically when a term is published with a changed slug.

| Column | Type | Description |
|---|---|---|
| `original_url` | VARCHAR(500) | Old term URL |
| `new_url` | VARCHAR(500) | New term URL |
| `term_id` | BIGINT | FK → `wp_breadcrumb_terms.id` |
| `taxonomy` | VARCHAR(32) | `category` or `post_tag` |
| `redirect_type` | VARCHAR(3) | `301` or `302` |
| `is_active` | TINYINT | `1` = active |
| `hit_count` | INT | Usage counter |

---

## Admin interface

```
http://localhost:8080/wp-admin/admin.php?page=breadcrumb-migration
```

### Layout — two-column card per term

```
┌──────────────────────────────────────────────────────────────────┐
│ [Tag] [Pending]  Term Name                                        │
├────────────────────────────┬─────────────────────────────────────┤
│ ORIGINAL                   │ PROPOSED                            │
│ WP ID  : 1234              │ Name        : Term Name             │
│ Name   : term-name         │ Slug        : term-name             │
│ Slug   : term-name         │ spaCy       : ORG                   │
│ Parent : —                 │ Wikidata ID : Q11660                │
│ Posts  : 42                │ Label       : artificial intelli... │
│                            │ Description : field of computer...  │
│                            │ Breadcrumb  : Home › Tags › Term    │
├────────────────────────────┼─────────────────────────────────────┤
│ [Simulate] [Validate]      │ [Edit]  [Publish to WP]            │
│            [Reject]        │                                     │
└────────────────────────────┴─────────────────────────────────────┘
```

### Status badges

| Badge | Color | Meaning |
|---|---|---|
| `Pending` | Yellow | Pipeline wrote proposal, not reviewed yet |
| `Approved` | Green | Validated by admin, ready to publish |
| `Rejected` | Red | Discarded, WP term unchanged |
| `Published` | Purple | WP term updated + 301 redirect created |

### Actions

| Button | AJAX / handler | Effect |
|---|---|---|
| **Simulate** | `bm_simulate_breadcrumb` | Renders breadcrumb preview inline. No DB change. |
| **Validate** | `bm_validate_proposal` (approve) | Sets `validation_state = approved`. Unlocks Publish. |
| **Reject** | `bm_validate_proposal` (reject) | Sets `validation_state = rejected`. No WP change. |
| **Edit** | `bm_update_proposal` | Inline form: edit name, slug, description. For `post_tag`: pick a parent category to replace "Tag" in the breadcrumb. Always visible (including approved and published states). **If term is already published**, saving also calls `wp_update_term()` immediately — no second Publish click needed. |
| **↩ Reset to Pending** | `bm_validate_proposal` (reset) | Reverts `approved` proposal back to `pending`. Re-enables edit + validate/reject cycle. Available only on approved, not-yet-published proposals. |
| **Publish to WP** | `bm_publish_term` | Calls `wp_update_term()` + stores 301 in redirects table. Only available after Validate. |
| **Scan for new tags** | `bm_scan_delta` | Queries WP `post_tag` terms not yet in `wp_breadcrumb_terms`. Returns list with count. No DB write. |
| **Search Wikidata** | `bm_search_wikidata` | Proxies `wbsearchentities` to Wikidata API using the configured language. Returns up to 5 candidates (QID + label + description). |
| **Use** _(Wikidata result)_ | — | Client-side only. Fills `wikidata_id`, `wikidata_label`, `wikidata_description` fields from selected result and collapses the result list. |
| **Open on Wikidata ↗** | — | Static link opening `https://www.wikidata.org/w/index.php?search=…&language={lang}` in a new tab. URL updates live as the search input changes. |
| **Add to migration** | `bm_add_delta_term` | Inserts term into `wp_breadcrumb_terms` + proposal into `wp_breadcrumb_proposals` (state: pending) with manually entered spaCy and Wikidata fields. |
| **Save Settings** | `admin_post_bm_save_settings` | Validates and persists `bm_settings` to `wp_options`. Redirects back with success notice. |
| **Import** | `admin_post_bm_import` | Upload `.json` or `.csv` from pipeline Step 4 → upsert terms + proposals. |
| **Export Proposals / Terms / Redirects** | `admin_post_bm_export` | Download table as CSV (`bm_{table}_{date}.csv`). |
| **Empty all tables** | `bm_empty_tables` | DELETE proposals → redirects → terms (FK-safe). Requires typing `CONFIRM`. |
| **Fetch** _(Bulk Description)_ | `bm_fetch_wikidata_description` | Looks up a specific QID via `wbgetentities`, updates `wikidata_id` + `wikidata_description` + `wikidata_label` in DB, refreshes cell live. Respects configured language with English fallback. |
| **Save Description to WordPress** _(Bulk Description)_ | `bm_bulk_save_description` | For each selected approved proposal: copies `wikidata_description` → `proposed_description` in DB, calls `wp_update_term()` to push description to live WP tag. |

### Tabs

| Tab | URL | Content |
|---|---|---|
| **Proposals** | `?page=breadcrumb-migration` | Two-column card list with filters and pagination |
| **Delta — New Tags** | `?page=breadcrumb-migration&tab=delta` | Scan, Wikidata-search, and manually enrich tags added after pipeline ran |
| **Bulk Assign** | `?page=breadcrumb-migration&tab=bulk_assign` | Two-step workflow: check existing assignments (Step 1) then assign a parent category (Step 2) |
| **Bulk Description** | `?page=breadcrumb-migration&tab=bulk_description` | Review, fetch, and save Wikidata descriptions to WordPress for all approved tags |
| **Import & Export** | `?page=breadcrumb-migration&tab=import` | File upload form + 3 CSV/JSON download buttons |
| **Settings** | `?page=breadcrumb-migration&tab=settings` | Plugin options: Wikidata search language |
| **Danger Zone** | `?page=breadcrumb-migration&tab=danger` | Empty all tables action with row counts |

### Filters

- Taxonomy: All / Category / Tag
- State: All / Pending / Approved / Rejected
- Search: term name or slug
- Paginated: 20 terms per page

---

## Step-by-step usage

### Prerequisites

Before opening the plugin, the Python pipeline must have run through Step 4 and produced a `*_step_4_proposals.json` file in `source/pipeline/exports/`.

---

### Step 1 — Activate the plugin

```
WordPress Admin → Plugins → Breadcrumb Migration → Activate
```

Activation automatically creates the 3 custom tables (`wp_breadcrumb_terms`, `wp_breadcrumb_proposals`, `wp_breadcrumb_redirects`). No SQL file import is needed.

---

### Step 2 — Import pipeline data

1. Open the plugin admin page:
   ```
   http://localhost:8080/wp-admin/admin.php?page=breadcrumb-migration
   ```
2. Click the **Import & Export** tab.
3. Under **Import**, click **Choose file** and select the Step 4 JSON export:
   ```
   source/pipeline/exports/{taxonomy}_{timestamp}_step_4_proposals.json
   ```
4. Click **Import file**.

The plugin upserts all terms and proposals from the file. A success notice shows how many rows were inserted or updated.

---

### Step 3 — Review proposals

1. Click the **Proposals** tab.
2. Use the filter bar to narrow results:
   - **Taxonomy**: All / Category / Tag
   - **State**: All / Pending / Approved / Rejected
   - **Search**: free text on name or slug
3. For each term card, choose an action:

| Goal | Button | Effect |
|---|---|---|
| Preview the breadcrumb path | **Simulate** | Renders breadcrumb inline. No DB change. |
| Correct name / slug / description | **Edit** | Opens inline form. Save writes to proposal row only. |
| Accept the proposal | **Validate** | Sets state → `approved`. Unlocks Publish button. |
| Discard the proposal | **Reject** | Sets state → `rejected`. WP term unchanged. |

---

### Step 4 — Publish approved proposals

1. After validating, the **Publish to WP** button appears on the card.
2. Click **Publish to WP** and confirm the dialog.
3. The plugin calls `wp_update_term()` — the live WordPress term is updated.
4. If the slug changed, a 301 redirect is stored in `wp_breadcrumb_redirects`.
5. The card badge changes to **Published** (purple).

Only one term is published per click. Repeat for each approved proposal.

---

### Step 4b — Add new tags (Delta)

Use this when new `post_tag` terms were added to WordPress **after** the pipeline ran, and you want to enrich them manually without rerunning the full pipeline.

1. Open the **Delta — New Tags** tab.
2. The header shows: "N post_tag(s) in WordPress · M tracked in DB" — the difference is the delta.
3. Click **Scan for new tags**.
   - Returns all `post_tag` terms present in WordPress but not yet in `wp_breadcrumb_terms`.
   - Shows count and one card per missing tag.
4. For each tag, fill in manually what the pipeline would have computed:
   - **spaCy entity**: select from dropdown (PERSON / ORG / GPE / LOC / PRODUCT / EVENT / none)
   - **Wikidata ID**: e.g. `Q42`
   - **Wikidata label**: label in French (or English)
   - **Description**: short description from Wikidata (optional)
   - **Proposed name / slug**: pre-filled from original — edit if needed
5. Click **Add to migration**.
   - Inserts a row in `wp_breadcrumb_terms` (status: `original`)
   - Inserts a row in `wp_breadcrumb_proposals` (state: `pending`) with all entered fields
   - Default breadcrumb: `["Home","Tags","<tag name>"]`
   - Card fades out; tag disappears from scan results
6. Go to **Proposals** tab — the new tag appears with state `Pending`, ready for validate/publish.

> **Tip:** leave Wikidata fields empty if unknown. The proposal is still created as `pending` and can be edited later via the Proposals tab Edit button.

---

### Step 5 — Export data for audit

1. Open the **Import & Export** tab.
2. Under **Export**, click the table you want:
   - **Export Proposals** → `bm_proposals_{date}.csv`
   - **Export Terms** → `bm_terms_{date}.csv`
   - **Export Redirects** → `bm_redirects_{date}.csv`

Files download immediately.

---

### Step 6 — Reset (Danger Zone)

Use only if you need to re-import from scratch (e.g. pipeline re-run produced new data).

1. Open the **Danger Zone** tab.
2. Review the displayed row counts.
3. Click **Empty all tables**.
4. Type `CONFIRM` in the prompt and click OK.

All rows are deleted in FK-safe order (proposals → redirects → terms). WordPress terms are **not** affected — only the 3 custom tables are cleared.

---

## Theme breadcrumb function

The file `add_to_functions_bm_display_enriched_breadcrumb.php` (v1.3.0) is a standalone helper to paste into the active theme's `functions.php`. It is **not** part of the plugin itself.

### Functions

| Function | Purpose |
|---|---|
| `bm_display_enriched_breadcrumb()` | Entry point. Call in tag/category archive templates. |
| `bm_fetch_breadcrumb_crumbs( $wp_term_id, $taxonomy )` | Reads `proposed_breadcrumb` from DB (approved/published only). Returns `[]` if tables don't exist. |
| `bm_native_breadcrumb_crumbs( $term, $taxonomy )` | Fallback: walks WP parent chain for categories; returns `["Home","Tags","Name"]` for tags. |
| `bm_breadcrumb_output( $crumbs, $taxonomy )` | Renders the trail. Home → link. Last crumb → `<span>`. Middle crumbs → linked via two-step lookup: WP category name first, then WP page by slug. |

### Usage in template

```php
<?php bm_display_enriched_breadcrumb(); ?>
```

### Graceful degradation

If the plugin tables do not exist (plugin inactive or not installed), `bm_fetch_breadcrumb_crumbs()` returns `[]` silently via an `information_schema` check — no WordPress database error is printed to the page. The function falls back to the native WP breadcrumb chain.

### Tag parent-category breadcrumb

When a `post_tag` proposal has a parent category assigned via the plugin admin (Edit → "Parent category in breadcrumb"), `proposed_breadcrumb` is rebuilt as `["Home", "<category_name>", "<tag_name>"]`. The `bm_breadcrumb_output()` renderer resolves any intermediate crumb against WP categories (regardless of taxonomy), so the category name becomes a real clickable link:

```
Home > webdoc > 17 octobre 1961    ← "webdoc" links to /category/webdoc/
```

Without assignment the fallback produces:

```
Home > Tags > 17 octobre 1961      ← "Tags" links to /tags/ (WP page with slug "tags")
```

---

## Security

- All AJAX handlers verify `wp_nonce` (`bm_nonce`)
- All AJAX handlers check `manage_options` capability
- Settings form uses `wp_nonce_field` + `check_admin_referer('bm_save_settings_nonce')`
- Wikidata language input validated to `[a-z-]` only before storing in `wp_options`
- Wikidata search proxied server-side via `wp_remote_get` — no direct API calls from browser
- All DB queries use `$wpdb->prepare()` — no raw interpolation
- All output escaped with `esc_html()`, `esc_attr()`, `esc_url()`
- `uninstall.php` checks `WP_UNINSTALL_PLUGIN` constant before executing

---

## Plugin lifecycle

| Action | Tables | Data |
|---|---|---|
| **Activate** | Created via `dbDelta()` — safe to re-run | Empty until pipeline runs |
| **Deactivate** | Untouched | Preserved |
| **Re-activate** | `IF NOT EXISTS` — no-op | Preserved |
| **Delete (uninstall)** | Dropped in order: proposals → redirects → terms | Permanently deleted |

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Admin page shows "No terms found" | Pipeline Step 4 not run yet | Run `004_step_4_breadcrumb_proposal.py --no-dry-run` |
| "Proposal not found or not approved" on publish | Trying to publish without validating | Click **Validate** first |
| Tables missing after activation | dbDelta failed silently | Check `wp-content/debug.log`; re-deactivate + reactivate |
| AJAX returns 403 | Nonce expired (page open >12h) | Refresh the admin page |
| 301 redirect not in table | Slug didn't change after publish | Expected — redirect only created when old URL ≠ new URL |
| Delta scan shows 0 new tags | All WP `post_tag` terms already tracked | Expected — no action needed |
| Delta "Add to migration" fails with "Term already tracked" | Concurrent double-click or race condition | Reload page and re-scan |
| Wikidata search returns no results | Term too specific or language mismatch | Try English label, or change language in **Settings** tab |
| Wikidata search fails with "unreachable" | WordPress server cannot reach `wikidata.org` | Check outbound HTTP from server; `wp_remote_get` must reach external URLs |
| Edit → Save shows "Saved. WP sync failed: …" | `wp_update_term()` returned WP_Error | Check WP debug log; term may have a slug conflict |
| Edit → Save on published term shows "Proposal updated." (no sync) | Term `status` is not `published` in `wp_breadcrumb_terms` | Republish the term once to mark it published, then future edits will sync |
| DB error in theme: "Table doesn't exist" | Plugin deactivated but `bm_display_enriched_breadcrumb()` still in `functions.php` | Upgrade to v1.3.0 of the theme helper — it guards with `information_schema` check and falls back silently |
| Tag breadcrumb shows "Tag" (not clickable) | No parent category assigned | Open plugin → Proposals tab → filter by Tag → Edit → select "Parent category in breadcrumb" → Save |

---

## Changelog

### v1.18.0 — 2026-06-11
- **UX**: **Proposals — "Overview" stats panel** — `bm_render_stats()` output now wrapped in `<section class="bm-panel bm-panel--overview">`; titled "Overview" with `<h3 class="bm-panel__title">`; blue left border (`#2271b1`) matches WP admin card conventions
- **UX**: **Proposals — filter sections use WP panel style** — both "Filter" and "Search" sections now carry `bm-panel bm-filter-section` classes (white background, `#c3c4c7` border, `border-radius: 4px`), consistent with Bulk Description panels; old gray `#f9f9f9` card style removed
- **UX**: **"Basic Filters" renamed to "Filter"** — shorter, imperative label; section titles use `bm-panel__title` (14 px, 600 weight, bottom rule) matching every other panel in the plugin
- **UX**: **Filter + Reset buttons right-aligned** — `bm-filter-actions` uses `justify-content: flex-end`; button order: Reset (`.button`) on the left, Filter (`.button-primary`) on the right — standard WP list-table convention
- `admin-page.php`: `bm_render_stats()` rewritten to template style, wrapped in panel section; `bm_render_filters()` section classes + titles updated, button order and primary class applied
- `breadcrumb-migration.php`: version bumped to `1.18.0`
- `admin.css`: `.bm-filter-section` reduced to layout-only (`flex:1`, `min-width:260px`, `margin:0`); visual styling delegated to `.bm-panel`; `.bm-filter-actions` gets `justify-content:flex-end` + `margin-top:12px`; `.bm-panel--overview` added (blue left border); `.bm-panel--overview .bm-stats` resets margin; `.bm-stats` standalone margin removed

### v1.17.0 — 2026-06-11
- **UX**: **Proposals — filter form restructured into two `<section>` panels** to avoid overloading a single filter bar
  - **Section "Basic Filters"**: taxonomy dropdown (All / Category / Tag) + validation-state dropdown (All / Pending / Approved / Rejected)
  - **Section "Search"**: name/slug text search + new Wikidata ID input + new spaCy entity dropdown
- **Feature**: **Wikidata ID filter** — new `bm_wikidata_id` GET param; partial `LIKE` match against `p.wikidata_id`; placeholder `Q41773`; searches across any term whose wikidata_id contains the typed value
- **Feature**: **spaCy entity filter** — new `bm_spacy` GET param; `<select>` dropdown listing all 18 NER types (`PERSON`, `NORP`, `FAC`, `ORG`, `GPE`, `LOC`, `PRODUCT`, `EVENT`, `WORK_OF_ART`, `LAW`, `LANGUAGE`, `DATE`, `TIME`, `PERCENT`, `MONEY`, `QUANTITY`, `ORDINAL`, `CARDINAL`); exact match against `p.spacy_entity`
- Both new filters survive pagination (params carried in pagination URLs)
- Empty-state "run pipeline" hint only shown when no filters are active (including the two new params)
- `admin-page.php`: `bm_render_tab_proposals()` reads `bm_wikidata_id` + `bm_spacy`, extends WHERE accordingly; `bm_render_filters()` new signature + section layout; `bm_render_pagination()` carries new params in URL args
- `breadcrumb-migration.php`: version bumped to `1.17.0`
- `admin.css`: `.bm-filters` changed to `display:block`; new `.bm-filter-sections` (flex row of section cards), `.bm-filter-section`, `.bm-filter-section__title`, `.bm-filter-section__controls`, `.bm-filter-actions`, `.bm-filter-wikidata-id` styles

### v1.16.0 — 2026-06-11
- **UX**: **Bulk Assign — 2-step workflow** — tab split into two `<section class="bm-bulk-step">` blocks with numbered step badges
  - **Step 1 "Search Keywords — Check Existing Assignments"**: paste keywords → click "Check Current Assignments" → preview table shows each keyword, whether it exists in the migration DB, and its current parent category (if any); read-only, no DB writes; new AJAX handler `bm_ajax_bulk_check()`
  - **Step 2 "Assign Parent Category to Keywords"**: category dropdown + "Assign Category to Keywords" button — same bulk-assign logic as before, reuses keywords from Step 1 textarea
- **UX**: **Bulk Description — row color coding** — every row in the Tag Descriptions table is now color-coded by status:
  - **Light green** (`#f0fdf4`): `term_status = 'published'` — breadcrumb live on frontend, no action needed
  - **Light orange** (`#fff7ed`): at least one field missing (Wikidata ID, Wikidata description, or actual description) but not all three
  - **Light red** (`#fef2f2`): all three fields empty — needs full attention
  - Row color recalculates live via `bmUpdateRowStatus()` after fetch, copy, refresh, or sync operations
- **UX**: **Bulk Description — "Status Key" legend panel** — new `<section class="bm-panel bm-panel--legend">` between Requirements and Quick Find; shows three color swatches (green/orange/red) with label and description
- **UX**: **Bulk Description — filter counts** — count badge `(N)` added after each filter label showing how many rows match that criterion; `N / total` visible counter appears to the right of the "Show all" button and updates after every filter, search, or data change; pure DOM counting — zero extra DB queries
- **Feature**: **"Completed" filter checkbox** — new filter in the "Show only:" bar that shows only green (published) rows; complements existing "Wikidata ID empty", "Wikidata description empty", "Actual description empty", "Written (manual) only" filters
- `admin-page.php`: `bm_render_tab_bulk_assign()` restructured into two `<section>` elements with step badges and descriptions; `bm_render_tab_bulk_description()` SQL updated to fetch `t.status AS term_status`; row `foreach` computes `$is_published` and `$row_status`; TR gets `bm-desc-row--{status}` class + `data-row-status` + `data-term-published` attributes; Status Key legend added; filters section gets count spans + Completed checkbox + visible-count display
- `ajax-handler.php`: new `bm_ajax_bulk_check()` — read-only lookup of existing parent-category assignments for a list of keywords; returns `found`, `parent_id`, `parent_name` per keyword
- `breadcrumb-migration.php`: `wp_ajax_bm_bulk_check` hook registered; version bumped to `1.16.0`
- `admin.js`: new `bmUpdateRowStatus()` helper recomputes row color class from data attributes; new `bmUpdateFilterCounts()` updates all count badges + visible counter; bulk-check click handler added; `bmDescApplyFilters()` extended for Completed filter + calls `bmUpdateFilterCounts()`; filter reset updated; `bmSetActualBadge()` calls `bmUpdateRowStatus()` after updating data attributes; Wikidata fetch handler calls `bmUpdateRowStatus()`; filter counts initialised on page load via `bmUpdateFilterCounts()`; name search and tag filter apply/clear call `bmUpdateFilterCounts()`
- `admin.css`: `.bm-bulk-step`, `.bm-bulk-step--1/2`, `.bm-bulk-step__title`, `.bm-step-badge`, `.bm-bulk-step__actions`, `.bm-bulk-check-table` styles; `.bm-desc-row--green/orange/red` row status colors; `.bm-filter-count` badge; `.bm-filter-visible-count`; `.bm-panel--legend`, `.bm-legend-list`, `.bm-legend-item`, `.bm-legend-swatch` styles added

### v1.15.0 — 2026-06-11
- **UX**: **Bulk Description — 4 named sections** — tab now split into `<section class="bm-panel">` wrappers: **Requirements**, **Quick Find**, **Batch Filter**, **Tag Descriptions**; each has a visible `<h3>` title and bordered card layout
- **UX**: **Requirements section** replaces the old vague caution notice — explicit numbered checklist: (1) Proposal must be Approved (link → Proposals tab), (2) Parent category must be assigned (link → Bulk Assign tab); old `<p class="description">` paragraph removed
- **Feature**: **Manual description badge** — Actual Description cell now shows `✍ Written` (amber) when `proposed_description` is non-empty and differs from `wikidata_description` (user-authored); shows `Wikidata` (blue) when both match; no schema change — derived from existing fields at render time
- **Feature**: **`data-desc-source`** attribute (`manual` / `wikidata` / `empty`) added to every `<tr>` for client-side filtering
- **Feature**: **"Written (manual) only" filter checkbox** added to the "Show only:" filter bar — hides all non-manual rows
- **Feature**: **Per-row `↺` refresh button** in the Actual Description cell — reads current WP tag description for that specific row via new AJAX handler `bm_ajax_refresh_single_description()`, updates cell and badge in-place without page reload
- **Feature**: **Sync protection** — global "↺ Synchronize from WordPress" button now skips rows where `proposed_description` is non-empty and differs from `wikidata_description`; flash notice reports `N refreshed, N skipped (manually written)`
- `admin-page.php`: `bm_render_tab_bulk_description()` rewritten — 4 `<section>` panels, Requirements checklist with `add_query_arg()` tab links, `$desc_source` computation per row, badge HTML, refresh button, `data-desc-source` attribute, "Written (manual) only" checkbox
- `ajax-handler.php`: `bm_ajax_sync_descriptions()` rewritten — queries `proposed_description` + `wikidata_description`, skips manual rows, returns `{description, is_manual, skipped}` objects + `skipped` count; new `bm_ajax_refresh_single_description()` function
- `breadcrumb-migration.php`: `wp_ajax_bm_refresh_single_description` hook registered; version bumped to `1.15.0`
- `admin.js`: `bmSetActualBadge()` helper centralises badge + content DOM updates; sync handler updated for new response format; bulk-save and copy-to-actual handlers use `bmSetActualBadge`; per-row `↺` click handler added; `bmDescApplyFilters()` and reset handler wired to `#bm-filter-manual-only`
- `admin.css`: `.bm-panel`, `.bm-panel__title`, `.bm-panel--requirements`, `.bm-requirements-intro`, `.bm-requirements-list`, `.bm-desc-actual-badge`, `.bm-desc-actual-badge--manual` (amber `#fef3c7`/`#92400e`), `.bm-desc-actual-badge--wikidata` (blue `#dbeafe`/`#1e40af`), `.bm-btn-refresh-single-desc` styles added

### v1.14.0 — 2026-06-11
- **Feature**: **Bulk Description — live search** — text input above the table filters visible rows by tag name in real-time (case-insensitive substring match); clears on "Clear" button
- **Feature**: **Bulk Description — tag filter textarea** — paste a comma or newline-separated list of tag names (e.g. `Apidoc, Chai, cheerio, CRUD`); click "Apply Filter" to narrow rows to exact case-insensitive matches; "Clear" restores all rows and resets the search input
- **Feature**: **Bulk Description — Synchronize from WordPress** button — reads the current `description` from each live WP tag via `get_term()`, writes it back to `proposed_description` in the migration DB, and refreshes all "Actual Description" cells in-place without a page reload; new AJAX handler `bm_ajax_sync_descriptions()`
- **Feature**: **Bulk Description — per-row "→ Copy to Actual" button** — appears in the "Description from Wikidata" column whenever `wikidata_description` is filled; clicking copies it to `proposed_description` + pushes to the live WP tag (reuses `bm_bulk_save_description`); button is also added dynamically after a successful "Fetch"
- **Feature**: **Bulk Description — Tag column** (replaces bare "Slug" column) — shows `original_name` (bold) + `proposed_slug` (code) + `wp_term_id` as a readonly text input + **✏ Edit** link opening `wp-admin/term.php?taxonomy=post_tag&tag_ID={id}&post_type=post` in a new tab + **↗** frontend view link
- **Feature**: **Bulk Description — ✏ Edit in WP link** in the "Actual Description" cell — same edit-tag admin URL, allows jumping directly from any row to the WP tag edit screen
- `admin-page.php`: `bm_render_tab_bulk_description()` — added search bar, tag filter section, `data-tag-name` attribute on rows, Tag column, copy button in Wikidata desc cell, edit links; inner spans `.bm-desc-actual-content` and `.bm-desc-wikidata-content` added for targeted JS updates
- `ajax-handler.php`: new `bm_ajax_sync_descriptions()`
- `breadcrumb-migration.php`: `wp_ajax_bm_sync_descriptions` hook registered; version bumped to `1.14.0`
- `admin.js`: 4 new handlers (live search, filter apply/clear, sync, per-row copy); existing fetch-wikidata handler updated to use `.bm-desc-wikidata-content` span and dynamically insert/remove copy button; bulk-save handler targets `.bm-desc-actual-content` span
- `admin.css`: `.bm-desc-search-bar`, `.bm-desc-tag-filter`, `.bm-desc-td-tag`, `.bm-desc-tag-meta`, `.bm-desc-wp-id`, `.bm-desc-edit-link`, `.bm-desc-wd-copy-wrap`, `.bm-btn-copy-wd-desc`, `.bm-desc-actual-content`, `.bm-desc-actual-actions` styles

### v1.13.0 — 2026-06-10
- **Feature**: **Bulk Description** tab — new tab placed after "Bulk Assign"; lists all approved proposals and lets admin review, fetch, and save Wikidata descriptions to WordPress in bulk
- Table columns: checkbox (with Select All in header), editable Wikidata ID with Fetch button and ↗ Wikidata link, Slug with "View tag" link, Description from Wikidata, Actual Description (current `proposed_description`)
- **Wikidata ID edit + Fetch**: user can correct the Wikidata ID inline; clicking "Fetch" calls the new `bm_ajax_fetch_wikidata_description()` handler which queries `wbgetentities` for the specific QID, updates `wikidata_id`, `wikidata_description`, and `wikidata_label` in `wp_breadcrumb_proposals`, and refreshes the cell live — respects the configured `wikidata_lang` with English fallback
- **Save Description to WordPress**: select rows with checkboxes, click button → `bm_ajax_bulk_save_description()` copies `wikidata_description` → `proposed_description` in DB for each selected proposal, then calls `wp_update_term()` to push the description to the live WP tag — result is immediately visible in WP Admin → Edit Tag → Description field and on the frontend tag archive page
- Rows with empty `wikidata_description` are skipped with error status; saved rows turn green, skipped/error rows turn red
- `admin-page.php`: new `bulk_description` tab entry + `bm_render_tab_bulk_description()` function
- `ajax-handler.php`: `bm_ajax_fetch_wikidata_description()` and `bm_ajax_bulk_save_description()`
- `breadcrumb-migration.php`: two new `wp_ajax_*` hooks registered; version bumped to `1.13.0`
- `admin.js`: select-all, fetch, and bulk-save handlers for Bulk Description tab
- `admin.css`: `.bm-bulk-desc-*` styles

### v1.12.0 — 2026-06-10
- **Feature**: **Bulk Publish** step in the Bulk Assign tab — after assigning keywords to a category, the results table now shows a checkbox on the right of each successfully `updated` or `created` row; a **Select All** checkbox in the column header toggles all checkboxes at once
- A **"Publish Selected to WordPress"** button appears below the results table whenever there is at least one selectable row; clicking it sends all checked proposal IDs to the new `bm_bulk_publish` AJAX endpoint
- `bm_ajax_bulk_publish()` in `ajax-handler.php`: new endpoint that, for each proposal ID, sets `validation_state = 'approved'`, calls `wp_update_term()`, stores a 301 redirect if the slug changed, and marks `status = 'published'` in `wp_breadcrumb_terms` — making the breadcrumb available on the frontend in one step
- `bm_ajax_bulk_assign()` in `ajax-handler.php`: now includes `proposal_id` in each result item so the JS can wire up checkboxes
- `admin.js`: bulk-assign results handler updated — checkbox column with Select All logic; `bm-btn-bulk-publish` click handler collects checked IDs, confirms, posts to `bm_bulk_publish`, then updates each published row's status badge to "Published" inline without page reload
- `admin.css`: added `.bm-bulk-status--published`, `.bm-bulk-row--published`, `.bm-bulk-col-cb`, `.bm-bulk-publish-actions`, `.bm-bulk-publish-note` styles

### v1.10.0 — 2026-05-13
- **Feature**: **Full spaCy NER entity list** — extended from 6 to 18 types everywhere the select appears: Proposals edit form, Delta new-tag form, and the AJAX allowlist validator
- New entities added: `NORP`, `FAC`, `WORK_OF_ART`, `LAW`, `LANGUAGE`, `DATE`, `TIME`, `PERCENT`, `MONEY`, `QUANTITY`, `ORDINAL`, `CARDINAL`
- **Feature**: **Settings tab — spaCy reference table** — read-only table listing all 18 entity types with their descriptions (from official spaCy documentation); displayed below the Wikidata language setting
- `admin-page.php`: `$spacy_options` array in `bm_render_term_card()` updated to all 18 types; `bm_render_tab_settings()` gains `bm-spacy-ref-table` section
- `ajax-handler.php`: `$allowed_entities` allowlist updated to all 18 types
- `admin.js`: `entities` array in `renderDeltaRow()` updated to all 18 types

### v1.9.0 — 2026-05-13
- **Feature**: **Edit form — Label, spaCy, Wikidata ID now editable** in the Proposals tab proposed column
- `admin-page.php`: added 3 fields to the inline `.bm-edit-form`: `wikidata_label` (text input), `spacy_entity` (select: PERSON / ORG / GPE / LOC / PRODUCT / EVENT / none), `wikidata_id` (text input); all pre-filled with current DB values
- `ajax-handler.php`: `bm_ajax_update_proposal()` now saves `spacy_entity` (allowlist-validated), `wikidata_id`, `wikidata_label` to `wp_breadcrumb_proposals`; all three included in success JSON response
- `admin.js`: save-edit handler reads and sends the 3 new fields; after success, refreshes displayed spaCy entity badge, Wikidata ID link, and Label text in the card without page reload; changes persist whether the term is pending, approved, or published

### v1.8.0 — 2026-05-11
- **Feature**: **Settings** tab (`?tab=settings`) — stores plugin options in `wp_options('bm_settings')`; first setting: **Wikidata search language** (default `en`, BCP 47 code, validated to `[a-z-]`)
- `bm_handle_save_settings()` in `admin-page.php`: `admin_post_bm_save_settings` handler — validates input, calls `update_option`, redirects with "Settings saved." notice
- `bm_ajax_search_wikidata()`: reads language from `bm_settings['wikidata_lang']` instead of hardcoded `fr`; `language=` and `uselang=` both use configured value
- `bm_enqueue_assets()`: passes `wikidataLang` and new `savedSynced` i18n string to `bmData` via `wp_localize_script`
- `admin.js`: `renderDeltaRow()` and `input` handler both use `bmData.wikidataLang` for ext link URL — no hardcoded language
- **Feature**: **Edit → Save auto-syncs to live WP term when published** — `bm_ajax_update_proposal()` now calls `wp_update_term()` after saving to proposals table if `term_status = published`; response includes `wp_synced` flag and `sync_error` message
- `admin.js`: save-edit handler shows "Saved and synced to WordPress." on success, "Saved. WP sync failed: …" on error, "Proposal updated." for non-published terms

### v1.7.0 — 2026-05-11
- **Feature**: **Wikidata inline search** in Delta tab — each new-tag card has a search widget to look up Wikidata entities by label without leaving the admin
- New AJAX action `bm_search_wikidata` (`bm_ajax_search_wikidata()`): server-side proxy to Wikidata `wbsearchentities` API (8s timeout, proper user-agent); returns up to 5 results with QID, label, description
- `renderDeltaRow()` in `admin.js`: added Wikidata search block above fields — search input (pre-filled with tag name), **Search Wikidata** button, **Open on Wikidata ↗** link (`target="_blank"`, updates live as user types)
- Per-result row: QID badge, bold label, italic description, **↗** item link (`target="_blank"`), **Use** button — clicking Use fills `wikidata_id`, `wikidata_label`, `wikidata_description` fields with a green flash and collapses the results
- `admin.css`: `.bm-wikidata-search`, `.bm-wikidata-result`, `.bm-field-filled` styles

### v1.6.0 — 2026-05-11
- **Feature**: **Delta — New Tags** tab — detects `post_tag` terms in WordPress not yet tracked in `wp_breadcrumb_terms` and lets admin enrich them manually (spaCy entity + Wikidata fields) without rerunning the Python pipeline
- New AJAX action `bm_scan_delta` (`bm_ajax_scan_delta()`): queries `wp_term_taxonomy LEFT JOIN wp_breadcrumb_terms`, returns untracked tags ordered by name
- New AJAX action `bm_add_delta_term` (`bm_ajax_add_delta_term()`): inserts into `wp_breadcrumb_terms` + `wp_breadcrumb_proposals` (state: `pending`) with manually supplied fields; builds default breadcrumb `["Home","Tags","<name>"]`
- `admin-page.php`: added `delta` tab between Proposals and Import & Export; `bm_render_tab_delta()` shows live WP vs tracked counts + scan button + results container
- `admin.js`: `renderDeltaRow()` renders per-tag form with spaCy select, Wikidata inputs, proposed name/slug; scan and add-to-migration handlers with fade-out on success
- `admin.css`: `.bm-delta-*` styles — responsive grid fields, blue left-border card, count badge

### v1.5.0 — 2026-05-10
- **Fix**: category crumb not clickable after tag-to-category assignment — `bm_breadcrumb_output()` (theme helper v1.3.0) now tries `get_term_by('slug', ...)` after `get_term_by('name', ...)` fails, covering accent/entity/case mismatches
- **Feature**: "↩ Reset to Pending" button added to `approved` proposal cards — allows re-editing and re-assigning parent category before re-approving; `bm_ajax_validate_proposal()` handles new `action_type=reset`
- **Fix**: Edit button now always visible when a proposal exists — including `approved` and `published` states — so parent category can be corrected on already-published tags without re-publishing the WP term
- `admin.js`: reset handler updates card badge, re-injects Validate+Reject buttons, removes Publish+Reset buttons
- `admin-page.php`: Edit button unconditional (no state/status guard); Reset button rendered for `approved` + not yet published

### v1.4.1 — 2026-05-10
- **Fix**: intermediate crumb in `bm_breadcrumb_output()` now falls back to WP page resolution by slug after category lookup fails — `"Tags"` links to `/tags/` (custom WP page) when no category named "Tags" exists

### v1.4.0 — 2026-05-10
- **Fix**: `bm_display_enriched_breadcrumb()` (theme helper v1.1.0) no longer triggers a WordPress database error when plugin tables don't exist — `information_schema` check returns `[]` and falls back silently to native WP breadcrumb
- **Feature**: `post_tag` proposals now support a parent-category picker in the Edit form — a `<select>` of all WP categories replaces "Tag" in the breadcrumb with a real clickable category link (e.g. `Home > webdoc > 17 octobre 1961`)
- `bm_ajax_update_proposal()` extended: accepts `tag_parent_category_id`, updates `proposed_parent_id`, rebuilds `proposed_breadcrumb` JSON as `["Home","<category>","<tag>"]`
- `bm_breadcrumb_output()` now resolves intermediate crumbs against WP categories for all taxonomies (previously `category` only) — enables clickable middle crumbs in tag archives
- `admin-page.php`: added `p.proposed_parent_id` to proposals SELECT; category `<select>` shown in edit form only for `post_tag` rows (pre-selected from saved value)
- `admin.js`: save handler sends `tag_parent_category_id`; breadcrumb preview row in card refreshed immediately on save

### v1.3.0 — 2026-05-10
- Export now supports both CSV and JSON formats — each table row in the Export section shows two buttons (CSV / JSON)
- `bm_handle_export()` reads new `bm_format=csv|json` GET param; JSON export streams `application/json` with envelope (`exported_at`, `table`, `total`, `data`)
- Admin-page export section replaced flat button row with a 3-row table (Proposals / Terms / Redirects × CSV / JSON)
- Added `.bm-export-table` CSS for the new table layout

### v1.2.0 — 2026-05-10
- Added **Import & Export** tab: file upload (JSON or CSV from Step 4) → upsert into DB
- Added **Danger Zone** tab: "Empty all tables" with `CONFIRM` prompt → DELETE in FK-safe order
- Added **Export** buttons: download `wp_breadcrumb_proposals`, `_terms`, `_redirects` as CSV
- New file `includes/import-export.php`: `bm_handle_import()` + `bm_handle_export()` via `admin_post`
- New AJAX action `bm_empty_tables` in `includes/ajax-handler.php`
- Admin page refactored to 3 tabs — `bm_render_tab_proposals()`, `bm_render_tab_import()`, `bm_render_tab_danger()`
- Renamed plugin directory: `plugin/` → `wp-plugin-breadcrumb-migration/` (no Docker auto-sync)
- Version bumped to `1.2.0`

### v1.1.0 — 2026-05-10
- Added `uninstall.php`: drops 3 custom tables on plugin deletion (proposals → redirects → terms order)
- Plugin is now fully autonomous: no external `.sql` file required
- Deactivation keeps data; only full deletion triggers table cleanup

### v1.0.0 — 2026-05-10
- Initial plugin creation
- `breadcrumb-migration.php`: entry point, hooks, admin menu, asset enqueue
- `includes/db-tables.php`: `bm_create_tables()` via `dbDelta` — 3 tables on activation
- `includes/admin-page.php`: two-column card UI, filter bar (taxonomy/state/search), pagination, stats bar
- `includes/ajax-handler.php`: validate/reject, simulate, inline edit, publish + 301 redirect storage
- `includes/breadcrumb-simulator.php`: `bm_render_breadcrumb()` from JSON + `bm_compute_breadcrumb()` parent-chain walker
- `assets/admin.css`: responsive 2-column grid, state color badges, colored action buttons
- `assets/admin.js`: jQuery AJAX for all 5 actions, inline edit toggle, flash notices
