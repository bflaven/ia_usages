<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Create the 3 custom tables on plugin activation.
 * Safe to re-run (CREATE TABLE IF NOT EXISTS).
 */
function bm_create_tables(): void {
	global $wpdb;
	$charset = $wpdb->get_charset_collate();
	$t       = bm_tables();

	require_once ABSPATH . 'wp-admin/includes/upgrade.php';

	// ── 1. Terms snapshot ────────────────────────────────────────────────────
	dbDelta( "CREATE TABLE {$t['terms']} (
		id                 BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
		wp_term_id         BIGINT(20) UNSIGNED NOT NULL,
		taxonomy           VARCHAR(32)  NOT NULL,
		original_name      VARCHAR(200) NOT NULL,
		original_slug      VARCHAR(200) NOT NULL,
		original_parent_id BIGINT(20) UNSIGNED NULL DEFAULT NULL,
		content_count      INT UNSIGNED DEFAULT 0,
		language           VARCHAR(10) DEFAULT 'fr',
		status             VARCHAR(20) DEFAULT 'original',
		created_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
		updated_at         DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		PRIMARY KEY (id),
		KEY idx_wp_term  (wp_term_id),
		KEY idx_taxonomy (taxonomy),
		KEY idx_status   (status)
	) $charset;" );

	// ── 2. Enriched proposals ─────────────────────────────────────────────────
	dbDelta( "CREATE TABLE {$t['proposals']} (
		id                   BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
		term_id              BIGINT(20) UNSIGNED NOT NULL,
		proposed_name        VARCHAR(200) NULL,
		proposed_slug        VARCHAR(200) NULL,
		proposed_description TEXT NULL,
		proposed_parent_id   BIGINT(20) UNSIGNED NULL DEFAULT NULL,
		proposed_language    VARCHAR(10) DEFAULT 'fr',
		spacy_entity         VARCHAR(32) NULL,
		wikidata_id          VARCHAR(50) NULL,
		wikidata_label       VARCHAR(200) NULL,
		wikidata_description TEXT NULL,
		proposed_breadcrumb  TEXT NULL,
		validation_state     VARCHAR(20) DEFAULT 'pending',
		validated_by         BIGINT(20) UNSIGNED NULL DEFAULT NULL,
		validated_at         DATETIME NULL DEFAULT NULL,
		created_at           DATETIME DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (id),
		KEY idx_term       (term_id),
		KEY idx_validation (validation_state),
		KEY idx_wikidata   (wikidata_id)
	) $charset;" );

	// ── 3. Redirect map ───────────────────────────────────────────────────────
	dbDelta( "CREATE TABLE {$t['redirects']} (
		id            BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
		original_url  VARCHAR(500) NOT NULL,
		new_url       VARCHAR(500) NOT NULL,
		term_id       BIGINT(20) UNSIGNED NULL DEFAULT NULL,
		taxonomy      VARCHAR(32) NULL,
		is_active     TINYINT(1) DEFAULT 1,
		redirect_type VARCHAR(3) DEFAULT '301',
		hit_count     INT DEFAULT 0,
		created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (id),
		KEY idx_original_url (original_url(191)),
		KEY idx_term_id      (term_id)
	) $charset;" );
}
