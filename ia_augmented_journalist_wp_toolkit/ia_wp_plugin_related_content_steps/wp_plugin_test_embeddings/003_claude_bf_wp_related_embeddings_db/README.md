# BF Related Posts via Embeddings (DB)

WordPress plugin for managing related posts using embeddings stored in a custom database table.

## Installation

1. Copy files to `wp-content/plugins/bf_wp_related_embeddings_db/`:
   ```bash
   docker cp bf_wp_related_embeddings_db.php wordpress:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
   docker cp uninstall.php wordpress:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
   docker exec wordpress chown -R www-data:www-data /var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
   ```

2. Activate plugin in WordPress Admin → Plugins

3. Import CSV at Settings → Related Embeddings

## CSV Format

```csv
post_id,related_post_id,similarity,rank
11463,13091,0.923,1
11463,12345,0.891,2
```

## MySQL 8 Compatibility

This version includes backticks around `rank` column for MySQL 8.0+ compatibility.

## Uninstall

Deleting the plugin removes the `wp_related_posts_embeddings` table and all data.

