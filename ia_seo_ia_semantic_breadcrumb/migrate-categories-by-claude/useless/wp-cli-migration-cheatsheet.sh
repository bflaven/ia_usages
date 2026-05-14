#!/usr/bin/env bash
# =============================================================================
# wp-cli-migration-cheatsheet.sh
# WP-CLI commands for the category migration workflow — flaven.fr / Bruno
#
# Run from WordPress root (where wp-config.php lives).
# =============================================================================


# -----------------------------------------------------------------------------
# STEP 0 — Sanity check: list all current categories with post counts
# -----------------------------------------------------------------------------
wp term list category --fields=name,slug,count --orderby=count --order=DESC


# -----------------------------------------------------------------------------
# STEP 1 — Dry-run: preview migration without writing anything
#           Edit migrate-categories.php: set DRY_RUN to true
# -----------------------------------------------------------------------------
wp eval-file migrate-categories.php


# -----------------------------------------------------------------------------
# STEP 2 — Full run: set DRY_RUN to false in the script, then:
# -----------------------------------------------------------------------------
wp eval-file migrate-categories.php


# -----------------------------------------------------------------------------
# STEP 3 — Verify new categories and their post counts after migration
# -----------------------------------------------------------------------------
wp term list category --fields=name,slug,count --orderby=count --order=DESC


# -----------------------------------------------------------------------------
# STEP 4 — (Optional) Manually delete any old category that was NOT
#           caught by the script (e.g. a slug that differs from expected)
#
#   wp term delete category <term_id>   # by ID
#   wp term delete category $(wp term list category --name="Divers" --field=term_id)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# STEP 5 — Flush rewrite rules (already done by script, but handy standalone)
# -----------------------------------------------------------------------------
wp rewrite flush --hard


# -----------------------------------------------------------------------------
# STEP 6 — Quick smoke-test: curl a few old URLs and check for 301 response
#           (do this AFTER adding htaccess-category-redirects.conf to .htaccess)
# -----------------------------------------------------------------------------
curl -sI https://flaven.fr/category/tutoriaux/       | grep -E "HTTP|Location"
curl -sI https://flaven.fr/category/developpement/   | grep -E "HTTP|Location"
curl -sI https://flaven.fr/category/reseaux-sociaux/ | grep -E "HTTP|Location"
curl -sI https://flaven.fr/category/divers/          | grep -E "HTTP|Location"
curl -sI https://flaven.fr/category/technologie/     | grep -E "HTTP|Location"


# -----------------------------------------------------------------------------
# STEP 7 — Regenerate sitemap if using Yoast / RankMath / XML Sitemaps plugin
#           (depends on plugin — usually triggered automatically on category change,
#            but you can force it via WP-CLI for Yoast:)
# -----------------------------------------------------------------------------
# wp yoast index --reindex
# wp cache flush


# -----------------------------------------------------------------------------
# STEP 8 — After verifying: submit updated sitemap in Google Search Console
#           URL: https://search.google.com/search-console/sitemaps
#           Sitemap URL: https://flaven.fr/sitemap.xml (or sitemap_index.xml)
# -----------------------------------------------------------------------------
