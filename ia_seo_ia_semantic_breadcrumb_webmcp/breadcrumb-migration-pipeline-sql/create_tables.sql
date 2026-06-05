-- =============================================================
-- Breadcrumb Migration — Custom tables (never touch WP originals)
-- Target : wordpress2 / MySQL 8.0
-- Run    : source this file in phpMyAdmin or mysql CLI
-- =============================================================

USE wordpress2;

-- -------------------------------------------------------------
-- 1. Original terms snapshot (read-only copy from WP)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wp_breadcrumb_terms (
    id                  BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    wp_term_id          BIGINT(20) UNSIGNED NOT NULL,
    taxonomy            VARCHAR(32)  NOT NULL,
    original_name       VARCHAR(200) NOT NULL,
    original_slug       VARCHAR(200) NOT NULL,
    original_parent_id  BIGINT(20) UNSIGNED NULL DEFAULT NULL,
    content_count       INT UNSIGNED DEFAULT 0,
    language            VARCHAR(10)  DEFAULT 'fr',
    status              ENUM('original', 'proposed', 'validated', 'published') DEFAULT 'original',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_wp_term  (wp_term_id),
    INDEX idx_taxonomy (taxonomy),
    INDEX idx_status   (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -------------------------------------------------------------
-- 2. Enriched proposals (spaCy NER + Wikidata)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wp_breadcrumb_proposals (
    id                  BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    term_id             BIGINT(20) UNSIGNED NOT NULL,
    proposed_name       VARCHAR(200) NULL,
    proposed_slug       VARCHAR(200) NULL,
    proposed_description TEXT        NULL,
    proposed_parent_id  BIGINT(20) UNSIGNED NULL DEFAULT NULL,
    proposed_language   VARCHAR(10)  DEFAULT 'fr',
    spacy_entity        VARCHAR(32)  NULL COMMENT 'PERSON,ORG,GPE,LOC,PRODUCT,EVENT',
    wikidata_id          VARCHAR(50)  NULL COMMENT 'e.g. Q42',
    wikidata_label       VARCHAR(200) NULL,
    wikidata_description TEXT         NULL COMMENT 'Wikidata entity description (fr then en fallback)',
    proposed_breadcrumb  TEXT         NULL COMMENT 'JSON array of breadcrumb levels',
    validation_state    ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    validated_by        BIGINT(20) UNSIGNED NULL DEFAULT NULL,
    validated_at        TIMESTAMP NULL DEFAULT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (term_id) REFERENCES wp_breadcrumb_terms(id) ON DELETE CASCADE,
    INDEX idx_term       (term_id),
    INDEX idx_validation (validation_state),
    INDEX idx_wikidata   (wikidata_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -------------------------------------------------------------
-- 3. 301/302 redirect map
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wp_breadcrumb_redirects (
    id             BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    original_url   VARCHAR(500) NOT NULL,
    new_url        VARCHAR(500) NOT NULL,
    term_id        BIGINT(20) UNSIGNED NULL DEFAULT NULL,
    taxonomy       VARCHAR(32)  NULL,
    is_active      BOOLEAN      DEFAULT TRUE,
    redirect_type  ENUM('301', '302') DEFAULT '301',
    hit_count      INT          DEFAULT 0,
    created_at     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_original_url (original_url(191)),
    INDEX idx_term_id      (term_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -------------------------------------------------------------
-- Verify
-- -------------------------------------------------------------
SHOW TABLES LIKE 'wp_breadcrumb%';
