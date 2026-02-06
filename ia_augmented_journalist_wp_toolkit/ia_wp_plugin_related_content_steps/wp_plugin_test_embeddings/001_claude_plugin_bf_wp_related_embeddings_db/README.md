# BF Related Posts via Embeddings (DB)

WordPress plugin for managing related posts using embeddings stored in a custom database table.

## Installation & Setup

### Step 1: Install the Plugin

1. **In your Docker WordPress container**, copy the plugin files to:
   ```
   wp-content/plugins/bf_wp_related_embeddings_db/
   ```

2. File structure should be:
   ```
   wp-content/plugins/bf_wp_related_embeddings_db/
   ├── bf_wp_related_embeddings_db.php  (main plugin file)
   └── uninstall.php                     (cleanup on uninstall)
   ```

3. **Using Docker CLI:**
   ```bash
   # Copy files to your container
   docker cp bf_wp_related_embeddings_db.php your-container:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
   docker cp uninstall.php your-container:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
   
   # Set proper permissions
   docker exec your-container chown -R www-data:www-data /var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/
   ```

### Step 2: Activate the Plugin

1. Go to WordPress Admin → Plugins
2. Find "BF Related Posts via Embeddings (DB)"
3. Click "Activate"
4. You should see a success notice confirming the table was created

### Step 3: Verify Database Table

**In phpMyAdmin or MySQL client:**

```sql
-- Check if table exists
SHOW TABLES LIKE 'wp_related_posts_embeddings';

-- View table structure
DESCRIBE wp_related_posts_embeddings;

-- Should show:
-- id (BIGINT, PRIMARY KEY)
-- post_id (BIGINT, INDEX)
-- related_post_id (BIGINT, INDEX)
-- similarity (DOUBLE)
-- rank (INT)
```

### Step 4: Check Plugin Status

Go to: **Settings → Related Embeddings**

This page shows:
- Database table status (exists or not)
- Current row count
- CSV import form

### Step 5: Import CSV Data

1. Prepare your CSV file with these columns (in any order):
   ```csv
   post_id,related_post_id,similarity,rank
   11463,13091,0.923,1
   11463,12345,0.891,2
   11464,13092,0.856,1
   ```

2. Go to **Settings → Related Embeddings**
3. Upload your CSV file
4. Click "Import CSV (truncate & reload)"
5. Check the success message showing number of rows imported

### Step 6: Verify Import

**In phpMyAdmin:**

```sql
-- Count rows
SELECT COUNT(*) FROM wp_related_posts_embeddings;

-- View sample data
SELECT * FROM wp_related_posts_embeddings 
ORDER BY post_id, rank 
LIMIT 10;
```

**In WordPress:**
- Edit any post that has related posts
- Look for "Related Posts (Embeddings)" meta box in the sidebar
- Should show related posts with similarity scores

## Debugging

### Enable Debug Mode

The plugin includes extensive logging. To view logs:

1. **Check Docker container logs:**
   ```bash
   docker logs -f your-container 2>&1 | grep bf_wp_related_embeddings_db
   ```

2. **Enable WordPress debug logging** in `wp-config.php`:
   ```php
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   define('WP_DEBUG_DISPLAY', false);
   ```

3. **View debug.log:**
   ```bash
   docker exec your-container tail -f /var/www/html/wp-content/debug.log
   ```

### Common Issues & Solutions

#### Issue: Table not created
**Solution:** 
- Check error logs for database errors
- Verify database user has CREATE TABLE permissions
- Try deactivating and reactivating the plugin

#### Issue: CSV import shows 0 rows imported
**Check:**
- CSV file has correct column headers: `post_id`, `related_post_id`, `similarity`, `rank`
- CSV is UTF-8 encoded
- Column headers don't have extra spaces or special characters
- Data rows have valid integers for post_id, related_post_id, rank
- Look for error messages in the import success notice

#### Issue: Meta box shows "No related posts"
**Check:**
- Table has data: `SELECT COUNT(*) FROM wp_related_posts_embeddings;`
- The current post ID exists in the table: 
  ```sql
  SELECT * FROM wp_related_posts_embeddings WHERE post_id = YOUR_POST_ID;
  ```

## Features

- ✅ Custom database table for fast lookups
- ✅ CSV import with validation and error reporting
- ✅ Admin interface showing database status
- ✅ Meta box on post edit screen
- ✅ Extensive debug logging
- ✅ Proper activation/deactivation/uninstall hooks

## CSV Format Details

### Required Columns (case-insensitive, any order):
- `post_id` - WordPress post ID (integer > 0)
- `related_post_id` - Related WordPress post ID (integer > 0)
- `similarity` - Similarity score (float, can use comma or period as decimal)
- `rank` - Ranking (integer > 0, lower = more relevant)

### Example:
```csv
post_id,related_post_id,similarity,rank
11463,13091,0.923,1
11463,12345,0.891,2
11463,11789,0.876,3
11464,13092,0.856,1
11464,11463,0.834,2
```

## Support

If you encounter issues:
1. Check the database status page: Settings → Related Embeddings
2. Review Docker container logs
3. Enable WordPress debug logging
4. Verify CSV format matches requirements
5. Check phpMyAdmin for table structure and data
