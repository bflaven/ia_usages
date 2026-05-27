# CLAUDE.md — WebMCP WordPress Plugin

## Project Goal

Build a WordPress plugin that exposes blog content as structured tools for AI agents using the WebMCP proposed standard. Plugin is read-only — no user interaction features (no comments, no e-commerce, no forms).

---

## Context

**Site profile**: tech blog, ~20 categories, read-only content consumption. No comment forms, no checkout, no membership. Primary value of WebMCP here is content discoverability by AI agents (Perplexity, Claude, ChatGPT Browse), not interactive actuation.

**WebMCP spec status**: proposed, not finalized (as of 2026-05-27). Implementation must stay pragmatic — no over-engineering against a spec that may change.

**WordPress target**: 6.0+, PHP 7.4+, MySQL 8.0.

---

## Plugin Directory

```
awesome-webmcp-bridge/
├── webmcp.php                      ← plugin entry point
├── uninstall.php                   ← cleans up wp_options on plugin delete
├── includes/
│   ├── class-webmcp-manifest.php   ← JSON manifest builder + <head> injection
│   ├── class-webmcp-tools.php      ← REST API endpoints (one per tool)
│   └── class-webmcp-admin.php      ← Settings > WebMCP admin page
├── assets/
│   └── webmcp.js                   ← data-mcp-* DOM annotations
└── README.md
```

Do NOT create translation files in v1.0.

---

## Tools to Expose (MVP)

These 5 tools cover all meaningful agent interactions for a read-only blog:

| Tool | Endpoint | Parameters |
|------|----------|------------|
| `search_posts` | `GET /wp-json/webmcp/v1/search` | `query` (required), `category` (optional), `limit` (default 10, max 20) |
| `get_latest_posts` | `GET /wp-json/webmcp/v1/posts` | `category` (optional), `count` (default 10, max 20) |
| `list_categories` | `GET /wp-json/webmcp/v1/categories` | none |
| `get_post_toc` | `GET /wp-json/webmcp/v1/post/{id}/toc` | `id` (required) |
| `get_related_posts` | `GET /wp-json/webmcp/v1/post/{id}/related` | `id` (required), `limit` (default 5, max 10) |

All endpoints: public, read-only, no authentication.

---

## Manifest Format

Inject in every page `<head>`:

```html
<script type="application/mcp+json">{...manifest JSON...}</script>
<link rel="mcp-manifest" href="https://site.com/wp-json/webmcp/v1/manifest">
```

Manifest JSON structure:

```json
{
  "schema_version": "0.1",
  "name": "Site name",
  "description": "Site tagline",
  "url": "https://site.com",
  "manifest_url": "https://site.com/wp-json/webmcp/v1/manifest",
  "tools": [ ... ]
}
```

Each tool entry:

```json
{
  "name": "search_posts",
  "description": "Human-readable description for the agent",
  "parameters": {
    "query": { "type": "string", "required": true, "description": "..." }
  },
  "action": {
    "type": "http",
    "method": "GET",
    "url": "https://site.com/wp-json/webmcp/v1/search"
  }
}
```

---

## REST Response Format

All tools return JSON arrays of post objects shaped as:

```json
[
  {
    "id": 123,
    "title": "Post title",
    "slug": "post-slug",
    "url": "https://site.com/post-slug/",
    "date": "2026-05-01 10:00:00",
    "excerpt": "First 30 words...",
    "cats": ["AI & Machine Learning", "Tutorials & How-to"]
  }
]
```

`get_post_toc` returns:

```json
{
  "post_id": 123,
  "post_title": "Post title",
  "url": "https://site.com/post-slug/",
  "toc": [
    { "level": 2, "heading": "Introduction" },
    { "level": 3, "heading": "Setup" }
  ]
}
```

`list_categories` returns:

```json
[
  { "id": 5, "name": "AI & Machine Learning", "slug": "ai-machine-learning", "description": "...", "count": 42, "url": "..." }
]
```

---

## Admin Settings Page

Location: **Settings → WebMCP** (`options-general.php?page=webmcp-settings`).

Required controls:
- Master on/off toggle (`webmcp_enabled`)
- Per-tool checkboxes (`webmcp_tools` option, array)
- Live manifest preview (formatted JSON, read-only `<pre>`)
- Link to live manifest REST endpoint

Options registered via `register_setting()` in `webmcp_group`. Use `sanitize_callback` on all inputs.

**Tab structure** (WP nav-tab-wrapper):
- `?tab=settings` — master toggle + per-tool checkboxes + Save button
- `?tab=manifest` — live manifest JSON preview + link to REST endpoint
- `?tab=help` — What Is WebMCP / agent discovery / pages that receive manifest / 4 verification methods with pre-filled live URLs / tool reference table / what plugin does NOT do / troubleshooting table

---

## DOM Annotations (webmcp.js)

Annotate existing page elements with `data-mcp-*` attributes so browser-based agents can locate entry points without parsing the manifest:

- Search form → `data-mcp-tool="search_posts"`, `data-mcp-action="{rest_url}search"`
- Search input → `data-mcp-param="query"`, `data-mcp-required="true"`
- Category links → `data-mcp-tool="get_latest_posts"`, `data-mcp-param-category="{slug}"`
- `<body>` → `data-mcp-manifest="{manifest_url}"`, `data-mcp-site="{site_name}"`

Pass REST base URL and site name via `wp_localize_script` as `webmcpConfig`.

---

## Plugin Lifecycle

| Event | Behavior |
|-------|----------|
| Activate | `register_activation_hook` — creates default options via `add_option()` |
| Deactivate | `register_deactivation_hook` — no-op, options preserved intentionally |
| Delete | `uninstall.php` — deletes `webmcp_enabled`, `webmcp_tools`, `webmcp_rate_limit` from `wp_options` |

**`uninstall.php` rules**:
- Must begin with `if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) { exit; }` — WP sets this constant before running the file; the guard prevents direct execution
- Only call `delete_option()` — no schema drops, no post deletions
- Runs only when admin clicks **Delete** in the Plugins screen, NOT on deactivate

---

## WordPress Coding Rules

- Register REST routes on `rest_api_init`, never on `init` — WP requires this since 5.1.0
- All user inputs: `sanitize_text_field()`, `absint()`, `esc_url_raw()` at boundaries
- All outputs in HTML: `esc_html()`, `esc_url()`, `esc_attr()`
- Never modify core WP tables
- No direct DB queries — use `WP_Query` and `get_terms`
- Cap all `limit`/`count` params server-side (max 20 posts, max 10 related)
- All REST callbacks: `permission_callback => '__return_true'` (public read-only)
- Check `post_status === 'publish'` before returning any post data

---

## What NOT to Build in v1.0

- Form annotation for comments, contact, newsletter (no forms active on site)
- Rate limiting middleware (WP REST API handles this at server level)
- Caching layer (WP object cache handles it)
- i18n/translation files
- Gutenberg block or widget
- Sync with llms.txt or robots.txt

---

## Acceptance Criteria

| Check | Passes when |
|-------|-------------|
| Manifest in `<head>` | `view-source:` shows `<script type="application/mcp+json">` on every page |
| Manifest endpoint | `GET /wp-json/webmcp/v1/manifest` returns valid JSON |
| search_posts | `?query=docker` returns array of matching posts |
| list_categories | Returns all 20 blog categories with counts |
| get_latest_posts | `?category=ai-machine-learning` returns recent posts in that category |
| get_post_toc | `post/{id}/toc` returns headings array for a published post |
| get_related_posts | Returns posts sharing at least one category with given post |
| Admin page | Settings → WebMCP visible, tools toggleable, manifest preview renders |
| Security | No private/draft posts leak through any endpoint |

---

## Versioning

```
v1.0.0 → initial release (5 tools, manifest injection, admin page)
v1.0.1 → fix rest_api_init hook; add uninstall.php for clean delete
v1.0.3 → 3-tab admin UI; Help & Verify tab with live URLs, tool reference, troubleshooting
v1.1.0 → add tool (e.g. get_post_full_content)
v2.0.0 → schema_version bump if WebMCP spec changes manifest format
```

Update `README.md` changelog after every version.
