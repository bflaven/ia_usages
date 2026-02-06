-- ============================================
-- MANUAL TABLE CREATION
-- BF Related Posts via Embeddings Plugin
-- ============================================
-- Use this if automatic table creation fails
-- Run in phpMyAdmin or MySQL command line
-- ============================================

-- IMPORTANT: Change 'wp_' prefix if your WordPress uses a different one
-- (Check wp-config.php for $table_prefix value)

-- Drop existing table if it exists (CAREFUL - deletes data!)
DROP TABLE IF EXISTS wp_related_posts_embeddings;

-- Create the table
CREATE TABLE wp_related_posts_embeddings (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    post_id BIGINT UNSIGNED NOT NULL,
    related_post_id BIGINT UNSIGNED NOT NULL,
    similarity DOUBLE NOT NULL,
    rank INT NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_post_id (post_id),
    INDEX idx_related_post_id (related_post_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Verify table was created
SHOW TABLES LIKE 'wp_related_posts_embeddings';

-- View table structure
DESCRIBE wp_related_posts_embeddings;

-- Expected output:
-- +------------------+---------------------+------+-----+---------+----------------+
-- | Field            | Type                | Null | Key | Default | Extra          |
-- +------------------+---------------------+------+-----+---------+----------------+
-- | id               | bigint unsigned     | NO   | PRI | NULL    | auto_increment |
-- | post_id          | bigint unsigned     | NO   | MUL | NULL    |                |
-- | related_post_id  | bigint unsigned     | NO   | MUL | NULL    |                |
-- | similarity       | double              | NO   |     | NULL    |                |
-- | rank             | int                 | NO   |     | NULL    |                |
-- +------------------+---------------------+------+-----+---------+----------------+

-- Insert test data (optional - to verify everything works)
INSERT INTO wp_related_posts_embeddings 
    (post_id, related_post_id, similarity, rank) 
VALUES 
    (1, 2, 0.95, 1),
    (1, 3, 0.89, 2),
    (1, 4, 0.82, 3);

-- Verify test data
SELECT * FROM wp_related_posts_embeddings;

-- If test data worked, clean it up:
-- DELETE FROM wp_related_posts_embeddings WHERE post_id = 1;

-- ============================================
-- TROUBLESHOOTING
-- ============================================

-- If you get "Access denied" error:
-- You need CREATE and INSERT privileges. Ask your database admin to run:
-- GRANT CREATE, INSERT, SELECT, UPDATE, DELETE ON your_database.* TO 'your_user'@'%';
-- FLUSH PRIVILEGES;

-- If you get "Unknown collation" error:
-- Try this simpler version without explicit charset:
/*
CREATE TABLE wp_related_posts_embeddings (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    post_id BIGINT UNSIGNED NOT NULL,
    related_post_id BIGINT UNSIGNED NOT NULL,
    similarity DOUBLE NOT NULL,
    rank INT NOT NULL,
    PRIMARY KEY (id),
    INDEX (post_id),
    INDEX (related_post_id)
) ENGINE=InnoDB;
*/

-- If you get "Table already exists" error:
-- Table exists but may be corrupted. Drop it first:
-- DROP TABLE wp_related_posts_embeddings;
-- Then run the CREATE TABLE statement again.
