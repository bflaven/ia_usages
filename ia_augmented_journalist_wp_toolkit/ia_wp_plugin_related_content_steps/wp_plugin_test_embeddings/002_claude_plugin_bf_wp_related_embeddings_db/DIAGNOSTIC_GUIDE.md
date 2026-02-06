# TABLE CREATION FAILED - DIAGNOSTIC GUIDE

Your plugin activated but the table wasn't created. Follow these steps to diagnose and fix:

## STEP 1: Install Diagnostic Version

1. **Deactivate the current plugin** in WordPress
2. **Replace the plugin file** with the diagnostic version:

```bash
# Backup current version
docker cp wordpress:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/bf_wp_related_embeddings_db.php ./backup_bf_wp_related_embeddings_db.php

# Copy diagnostic version
docker cp bf_wp_related_embeddings_db_diagnostic.php wordpress:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/bf_wp_related_embeddings_db.php

# Set permissions
docker exec wordpress chown www-data:www-data /var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/bf_wp_related_embeddings_db.php
```

## STEP 2: Activate and Watch Logs

1. **Open a terminal and watch logs in real-time:**
```bash
docker logs -f wordpress 2>&1 | grep bf_wp_related_embeddings_db
```

2. **In another terminal/window, activate the plugin:**
   - Go to WordPress Admin → Plugins
   - Activate "BF Related Posts via Embeddings (DB) - DIAGNOSTIC"

3. **Watch the log output** - it will show:
   - Database connection details
   - Database grants/permissions
   - Three different table creation methods being tried
   - Exact SQL errors (if any)

## STEP 3: Review Diagnostic Results

The logs will show one of these outcomes:

### ✓ SUCCESS (Method 1, 2, or 3):
```
✓ METHOD X SUCCESS: Table created via [method]
```
→ Great! Go to Step 5 below.

### ✗ ALL METHODS FAILED:
You'll see specific error messages. Common issues:

#### Issue A: Permission Denied
```
ERROR: Access denied; you need the CREATE privilege
```
**Fix:** Grant CREATE permission to your database user:
```sql
GRANT CREATE ON database_name.* TO 'wordpress_user'@'%';
FLUSH PRIVILEGES;
```

#### Issue B: Database doesn't exist
```
ERROR: Unknown database
```
**Fix:** Check your wp-config.php database name matches your MySQL database.

#### Issue C: Charset issues
```
ERROR: Unknown collation
```
**Fix:** Use the manual SQL method (Step 4).

## STEP 4: Manual Table Creation (If Needed)

If all automatic methods failed, create the table manually in phpMyAdmin:

```sql
-- Replace 'wp_' with your actual table prefix if different
CREATE TABLE wp_related_posts_embeddings (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    post_id BIGINT UNSIGNED NOT NULL,
    related_post_id BIGINT UNSIGNED NOT NULL,
    similarity DOUBLE NOT NULL,
    rank INT NOT NULL,
    PRIMARY KEY (id),
    INDEX (post_id),
    INDEX (related_post_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Verify it worked:
```sql
SHOW TABLES LIKE 'wp_related_posts_embeddings';
DESCRIBE wp_related_posts_embeddings;
```

## STEP 5: Check Diagnostic Page

Go to **Settings → Related Embeddings** in WordPress.

You'll see:
- Current database status
- Whether table exists (YES/NO)
- Which creation method worked

## STEP 6: Switch to Full Version (Once Working)

Once the table exists:

1. Deactivate diagnostic version
2. Restore the full version:
```bash
docker cp bf_wp_related_embeddings_db.php wordpress:/var/www/html/wp-content/plugins/bf_wp_related_embeddings_db/bf_wp_related_embeddings_db.php
```
3. Activate the full version
4. Import your CSV

## COMMON CAUSES & SOLUTIONS

### 1. Docker MySQL Container Permissions
If you're using separate MySQL container:
```bash
# Connect to MySQL container
docker exec -it mysql_container mysql -u root -p

# Grant permissions
GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress_user'@'%';
FLUSH PRIVILEGES;
```

### 2. wp-config.php Issues
Check your wp-config.php database settings:
```php
define('DB_NAME', 'wordpress');     // Database name
define('DB_USER', 'wordpress');     // Database user
define('DB_PASSWORD', 'password');  // Database password
define('DB_HOST', 'mysql:3306');    // Host (container name:port or localhost)
```

### 3. MySQL Version Too Old
dbDelta requires MySQL 5.0+. Check version:
```bash
docker exec wordpress mysql --version
```

### 4. Character Set Issues
Some Docker MySQL images have restrictive charset settings. The diagnostic version tries multiple approaches to work around this.

## NEED MORE HELP?

Send me the output from:
```bash
# Full diagnostic log
docker logs wordpress 2>&1 | grep bf_wp_related_embeddings_db

# MySQL grants
docker exec wordpress mysql -u wordpress_user -p wordpress -e "SHOW GRANTS FOR CURRENT_USER()"

# Existing tables
docker exec wordpress mysql -u wordpress_user -p wordpress -e "SHOW TABLES LIKE 'wp_%'"
```
