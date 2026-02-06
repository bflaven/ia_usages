# BF Related Posts via Embeddings (DB)

WordPress plugin for managing related posts using embeddings or manual selection.

## Installation

```bash
docker cp bf_wp_related_embeddings_db.php wordpress:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
docker cp uninstall.php wordpress:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
docker exec wordpress chown -R www-data:www-data /var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
```

Activate in WordPress Admin → Plugins.

## Features

### 1. CSV Import
Go to Settings → Related Embeddings:
- Upload CSV file (format: `post_id,related_post_id,similarity,rank`)
- Check "Truncate table first?" to delete existing data before import
- Click "Import CSV"

### 2. Manual Selection
Edit any post → sidebar → "Related Posts (Embeddings)":
- **Default mode (checkbox unchecked):** All posts from CSV/database shown automatically
- **Custom selection (checkbox checked):** Click posts to select/deselect (green = selected)
- Search and add more posts by ID or title

### 3. Display Related Posts

**Shortcode:**
```
[bf_related_posts]
[bf_related_posts limit="3" title="You May Also Like"]
```

**Template function:**
```php
$related = bf_get_related_posts( $post_id, $limit );
foreach ( $related as $post ) {
    echo '<a href="' . $post['permalink'] . '">' . $post['title'] . '</a>';
}
```

## Uninstall

Delete plugin → table and all data removed.

## MySQL 8 Compatibility

Includes backticks for `rank` column (MySQL 8 reserved word).
