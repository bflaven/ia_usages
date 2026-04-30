<?php
/**
 * Semaphore – Uninstall
 *
 * Runs when the plugin is deleted from the WordPress Plugins screen.
 * Drops all plugin-owned tables and removes all plugin options.
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;

// Drop plugin tables.
$wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}related_posts_embeddings`" );
$wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}tag_families`" );

// Remove plugin options.
delete_option( 'semaphore_debug' );
delete_option( 'semaphore_enable_sidebar' );
delete_option( 'semaphore_enable_footer' );
delete_option( 'semaphore_enable_breadcrumbs' );
delete_option( 'semaphore_enable_schema' );
