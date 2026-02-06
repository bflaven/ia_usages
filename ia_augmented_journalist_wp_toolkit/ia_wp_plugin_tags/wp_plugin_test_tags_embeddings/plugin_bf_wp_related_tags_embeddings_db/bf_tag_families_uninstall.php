<?php
/**
 * Uninstall handler for BF Tag Families via Embeddings (DB)
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;

$table_name = $wpdb->prefix . 'tag_families';

$wpdb->query( "DROP TABLE IF EXISTS `{$table_name}`" );

delete_option( 'bf_tf_table_created' );
delete_option( 'bf_tf_creation_method' );

// Delete all custom selection meta
$wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_selection'" );
$wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_mode_active'" );
$wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_order'" );
