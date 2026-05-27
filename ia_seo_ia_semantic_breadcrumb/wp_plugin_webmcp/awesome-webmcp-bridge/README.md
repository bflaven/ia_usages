# WebMCP for WordPress

Exposes WordPress content as structured tools for AI agents via the [WebMCP proposed standard](https://webmcp.dev).

## What It Does

Injects a `<script type="application/mcp+json">` manifest in every page `<head>` and provides REST API endpoints that AI agents (Perplexity, Claude, ChatGPT Browse) can call directly to discover and query your content.

## File Structure

```
webmcp.php                         ← plugin entry point
uninstall.php                      ← cleans up wp_options on plugin delete
includes/
  class-webmcp-manifest.php        ← builds JSON manifest injected in <head>
  class-webmcp-tools.php           ← REST endpoints for each tool
  class-webmcp-admin.php           ← Settings > WebMCP admin page
assets/
  webmcp.js                        ← annotates DOM elements with data-mcp-* attributes
```

## REST API Endpoints

| Method | Endpoint | Tool |
|--------|----------|------|
| GET | `/wp-json/webmcp/v1/manifest` | Full manifest |
| GET | `/wp-json/webmcp/v1/search?query=X&category=Y&limit=10` | search_posts |
| GET | `/wp-json/webmcp/v1/posts?category=Y&count=10` | get_latest_posts |
| GET | `/wp-json/webmcp/v1/categories` | list_categories |
| GET | `/wp-json/webmcp/v1/post/{id}/toc` | get_post_toc |
| GET | `/wp-json/webmcp/v1/post/{id}/related?limit=5` | get_related_posts |

All endpoints are public (read-only). No authentication required.

## Admin

**Settings → WebMCP** — enable/disable plugin and individual tools. Live manifest preview included.

## Installation

1. Upload `wp_plugin_webmcp/` to `wp-content/plugins/webmcp/`
2. Activate via **Plugins** screen
3. Configure at **Settings → WebMCP**

## Requirements

- WordPress 6.0+
- PHP 7.4+

## Lifecycle

| Event | Behavior |
|-------|----------|
| Activate | Creates default options (`webmcp_enabled`, `webmcp_tools`, `webmcp_rate_limit`) |
| Deactivate | Keeps options (data preserved — plugin can be re-activated cleanly) |
| Delete | `uninstall.php` removes all 3 options from `wp_options` — full rollback |

## Changelog

### v1.0.3 — 2026-05-27
- Add: 3-tab admin UI (Settings | Manifest | Help & Verify)
- Add: Help tab — What Is WebMCP, how agents discover it, 4 verification methods with pre-filled live URLs, tool reference table, what plugin does NOT do, troubleshooting table

### v1.0.1 — 2026-05-27
- Fix: REST routes now registered on `rest_api_init` (was `init`) — resolves WP 5.1.0+ notice and headers-already-sent error
- Add: `uninstall.php` — deletes all plugin options on delete for clean rollback

### v1.0.0 — 2026-05-27
- Initial release
- 5 tools: search_posts, get_latest_posts, list_categories, get_post_toc, get_related_posts
- JSON manifest injected in `<head>`
- `data-mcp-*` DOM annotations via `webmcp.js`
- Admin settings page with live manifest preview
