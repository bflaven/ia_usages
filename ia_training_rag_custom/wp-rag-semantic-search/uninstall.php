<?php
/**
 * Uninstall hook — runs when the plugin is deleted from WP admin.
 *
 * WordPress does NOT load the main plugin file during uninstall, so this
 * file must be fully self-contained: no require_once of plugin classes,
 * no calls to helper functions defined elsewhere.
 *
 * On deletion this script:
 *   1. Drops wp_rag_results (first — FK dependency on wp_rag_posts).
 *   2. Drops wp_rag_posts.
 *   3. Removes every plugin option from wp_options.
 *
 * Deactivating the plugin does NOT trigger this file — data is preserved
 * until the admin explicitly deletes the plugin.
 */

defined( 'WP_UNINSTALL_PLUGIN' ) || exit;

global $wpdb;

// Drop both tables. Results first to respect the FK dependency.
$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'rag_results' ); // phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'rag_posts' );   // phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared

// Remove all plugin options stored in wp_options.
delete_option( 'rss_db_version' );
delete_option( 'rss_semantic_enabled' );
delete_option( 'rss_promo_text' );
delete_option( 'rss_lang_notice' );
delete_option( 'rss_cache_ttl_days' );
