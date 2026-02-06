<?php
/**
 * Uninstall handler for BF Test Table.
 *
 * Called automatically by WordPress when you click "Delete" on the plugin.
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;

$table_name = $wpdb->prefix . 'bf_test_table';

error_log( '[bf_test_table] uninstall.php dropping table: ' . $table_name );

$wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
