<?php
/**
 * Uninstall — runs when admin deletes the plugin from WP Admin > Plugins.
 * Drops the 3 custom tables. Does NOT touch original WordPress tables.
 *
 * Deactivation (disable only) does NOT trigger this file — data is preserved.
 * Only plugin DELETION triggers cleanup.
 */

// WordPress sets this constant before calling uninstall.php.
// Bail if called directly.
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}

global $wpdb;

$tables = [
	$wpdb->prefix . 'breadcrumb_proposals', // drop child first (FK)
	$wpdb->prefix . 'breadcrumb_redirects',
	$wpdb->prefix . 'breadcrumb_terms',
];

foreach ( $tables as $table ) {
	$wpdb->query( "DROP TABLE IF EXISTS `{$table}`" ); // phpcs:ignore WordPress.DB.PreparedSQL.InterpolatedNotPrepared
}
