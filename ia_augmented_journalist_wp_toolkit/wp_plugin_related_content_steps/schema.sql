-- Database schema for WordPress related content system

-- Table to store post embeddings
CREATE TABLE IF NOT EXISTS wp_post_embeddings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id BIGINT(20) UNSIGNED NOT NULL,
    embedding BLOB NOT NULL,
    embedding_model VARCHAR(100) NOT NULL DEFAULT 'paraphrase-multilingual-mpnet-base-v2',
    language VARCHAR(10),
    content_hash VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_post (post_id),
    KEY idx_language (language),
    KEY idx_model (embedding_model),
    KEY idx_content_hash (content_hash),
    FOREIGN KEY (post_id) REFERENCES wp_posts(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to store pre-computed similarity scores (optional - for performance)
CREATE TABLE IF NOT EXISTS wp_post_similarities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_post_id BIGINT(20) UNSIGNED NOT NULL,
    related_post_id BIGINT(20) UNSIGNED NOT NULL,
    similarity_score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY idx_source (source_post_id, similarity_score DESC),
    KEY idx_related (related_post_id),
    UNIQUE KEY unique_pair (source_post_id, related_post_id),
    FOREIGN KEY (source_post_id) REFERENCES wp_posts(ID) ON DELETE CASCADE,
    FOREIGN KEY (related_post_id) REFERENCES wp_posts(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Index for faster similarity lookups
CREATE INDEX idx_similarity_lookup ON wp_post_similarities (source_post_id, similarity_score DESC);

-- View for easy querying of related posts with metadata
CREATE OR REPLACE VIEW vw_related_posts AS
SELECT 
    ps.source_post_id,
    ps.related_post_id,
    ps.similarity_score,
    p.post_title,
    p.post_date,
    p.post_type,
    p.post_status,
    pe.language
FROM wp_post_similarities ps
JOIN wp_posts p ON ps.related_post_id = p.ID
JOIN wp_post_embeddings pe ON ps.related_post_id = pe.post_id
WHERE p.post_status = 'publish'
ORDER BY ps.source_post_id, ps.similarity_score DESC;
