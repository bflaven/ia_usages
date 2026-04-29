-- ============================================================
-- RAG Bridge — MySQL/MariaDB schema
-- File: data/bridge/rag_schema.sql
--
-- Two tables, prefixed to avoid collisions with core WP tables.
-- Table names match bridge_wp.yaml: posts_table / results_table.
--
-- Usage in WordPress:
--   The plugin prepends $wpdb->prefix at activation time,
--   so the actual table names become wp_rag_posts / wp_rag_results
--   (or whatever prefix your WP install uses).
--
-- Usage standalone (phpMyAdmin / MySQL CLI):
--   Run as-is against the WordPress database. No prefix applied.
-- ============================================================


-- ------------------------------------------------------------
-- Table: rag_posts
-- One row per article imported from the RAG exchange file.
-- Populated by the WP plugin admin import (T5).
-- Primary key is the WordPress post ID from the exchange file,
-- so re-importing the same file is idempotent (INSERT IGNORE).
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS `rag_posts` (
  `id`          INT            NOT NULL,           -- WP post ID (from exchange file, not auto-increment)
  `title`       VARCHAR(500)   NOT NULL,
  `url`         VARCHAR(1000)  NOT NULL,
  `date`        DATE           NOT NULL,
  `slug`        VARCHAR(500)   NOT NULL,
  `excerpt`     TEXT,                              -- may be empty
  `text`        LONGTEXT       NOT NULL,           -- full plain-text body, HTML stripped
  `imported_at` DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ------------------------------------------------------------
-- Table: rag_results
-- One row per (query, ranked result) pair.
-- Written when a semantic search is executed and results are
-- stored for display in WordPress.
-- Rows expire after results_ttl_days (default 7) via expires_at.
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS `rag_results` (
  `id`          INT            NOT NULL AUTO_INCREMENT,
  `query_hash`  CHAR(64)       NOT NULL,           -- SHA-256 of query_text (hex, for fast lookups)
  `query_text`  TEXT           NOT NULL,           -- original query string
  `post_id`     INT            NOT NULL,           -- FK → rag_posts.id
  `score`       FLOAT          NOT NULL,           -- relevance score from FAISS / re-ranker
  `rank`        TINYINT        NOT NULL,           -- 1-based position in the result set
  `created_at`  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expires_at`  DATETIME       NOT NULL,           -- = created_at + INTERVAL results_ttl_days DAY
  PRIMARY KEY (`id`),
  INDEX `idx_query_hash` (`query_hash`),           -- fast lookup by query
  INDEX `idx_expires_at` (`expires_at`),           -- fast TTL purge scan
  CONSTRAINT `fk_rag_results_post`
    FOREIGN KEY (`post_id`) REFERENCES `rag_posts` (`id`)
    ON DELETE CASCADE                              -- purge results when post is deleted
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- Utility queries (reference — not executed at install time)
-- ============================================================

-- Purge expired results (run on each search or on a schedule):
-- DELETE FROM `rag_results` WHERE `expires_at` < NOW();

-- Empty both tables without dropping them (WP plugin "empty tables" action):
-- DELETE FROM `rag_results`;
-- DELETE FROM `rag_posts`;

-- Drop both tables (WP plugin uninstall hook):
-- DROP TABLE IF EXISTS `rag_results`;   -- results first (FK dependency)
-- DROP TABLE IF EXISTS `rag_posts`;
