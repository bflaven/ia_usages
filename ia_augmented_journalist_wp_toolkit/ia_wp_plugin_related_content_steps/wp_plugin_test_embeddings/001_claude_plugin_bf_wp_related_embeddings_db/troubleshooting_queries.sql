-- ============================================
-- Troubleshooting SQL Queries
-- BF Related Posts via Embeddings Plugin
-- ============================================

-- 1. CHECK IF TABLE EXISTS
-- ------------------------------------------
SHOW TABLES LIKE 'wp_related_posts_embeddings';
-- Expected: One row with table name
-- If empty: Table doesn't exist, try reactivating plugin


-- 2. VIEW TABLE STRUCTURE
-- ------------------------------------------
DESCRIBE wp_related_posts_embeddings;
-- Expected columns:
-- id, post_id, related_post_id, similarity, rank


-- 3. COUNT TOTAL ROWS
-- ------------------------------------------
SELECT COUNT(*) AS total_rows 
FROM wp_related_posts_embeddings;
-- If 0: No data imported yet, upload CSV


-- 4. VIEW SAMPLE DATA
-- ------------------------------------------
SELECT * 
FROM wp_related_posts_embeddings 
ORDER BY post_id, rank 
LIMIT 20;


-- 5. CHECK DATA FOR SPECIFIC POST
-- ------------------------------------------
-- Replace 11463 with your post ID
SELECT 
    post_id,
    related_post_id,
    similarity,
    rank
FROM wp_related_posts_embeddings 
WHERE post_id = 11463
ORDER BY rank;


-- 6. COUNT POSTS WITH RELATED POSTS
-- ------------------------------------------
SELECT COUNT(DISTINCT post_id) AS posts_with_related 
FROM wp_related_posts_embeddings;


-- 7. TOP 10 POSTS BY NUMBER OF RELATED POSTS
-- ------------------------------------------
SELECT 
    post_id,
    COUNT(*) AS related_count
FROM wp_related_posts_embeddings 
GROUP BY post_id 
ORDER BY related_count DESC 
LIMIT 10;


-- 8. VERIFY DATA QUALITY
-- ------------------------------------------
-- Check for invalid similarity values
SELECT COUNT(*) AS invalid_similarity
FROM wp_related_posts_embeddings 
WHERE similarity < 0 OR similarity > 1;
-- Should be 0

-- Check for invalid ranks
SELECT COUNT(*) AS invalid_ranks
FROM wp_related_posts_embeddings 
WHERE rank <= 0;
-- Should be 0


-- 9. FIND POSTS THAT DON'T EXIST IN wp_posts
-- ------------------------------------------
SELECT DISTINCT rpe.post_id
FROM wp_related_posts_embeddings rpe
LEFT JOIN wp_posts p ON rpe.post_id = p.ID
WHERE p.ID IS NULL;
-- These post_ids exist in embeddings table but not in wp_posts

SELECT DISTINCT rpe.related_post_id
FROM wp_related_posts_embeddings rpe
LEFT JOIN wp_posts p ON rpe.related_post_id = p.ID
WHERE p.ID IS NULL;
-- These related_post_ids exist in embeddings table but not in wp_posts


-- 10. CHECK DUPLICATE RELATIONSHIPS
-- ------------------------------------------
SELECT 
    post_id,
    related_post_id,
    COUNT(*) AS duplicate_count
FROM wp_related_posts_embeddings 
GROUP BY post_id, related_post_id 
HAVING COUNT(*) > 1;
-- Should be empty (no duplicates)


-- 11. VIEW RELATED POSTS WITH ACTUAL POST TITLES
-- ------------------------------------------
-- Replace 11463 with your post ID
SELECT 
    rpe.rank,
    rpe.related_post_id,
    p.post_title,
    rpe.similarity,
    p.post_status,
    p.post_type
FROM wp_related_posts_embeddings rpe
LEFT JOIN wp_posts p ON rpe.related_post_id = p.ID
WHERE rpe.post_id = 11463
ORDER BY rpe.rank;


-- 12. STATISTICS OVERVIEW
-- ------------------------------------------
SELECT 
    COUNT(*) AS total_relationships,
    COUNT(DISTINCT post_id) AS unique_posts,
    COUNT(DISTINCT related_post_id) AS unique_related_posts,
    MIN(similarity) AS min_similarity,
    MAX(similarity) AS max_similarity,
    AVG(similarity) AS avg_similarity,
    MIN(rank) AS min_rank,
    MAX(rank) AS max_rank
FROM wp_related_posts_embeddings;


-- 13. CLEAN UP (CAREFUL - DELETES DATA!)
-- ------------------------------------------
-- Uncomment to use (removes all data)
-- TRUNCATE TABLE wp_related_posts_embeddings;

-- To completely remove table (will require reactivation)
-- DROP TABLE IF EXISTS wp_related_posts_embeddings;


-- 14. MANUALLY INSERT TEST DATA
-- ------------------------------------------
-- Use this if CSV import isn't working
INSERT INTO wp_related_posts_embeddings 
    (post_id, related_post_id, similarity, rank) 
VALUES 
    (11463, 13091, 0.923, 1),
    (11463, 12345, 0.891, 2),
    (11463, 11789, 0.876, 3);

-- Verify it worked
SELECT * FROM wp_related_posts_embeddings WHERE post_id = 11463;
