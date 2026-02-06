<?php
/**
 * Uninstall handler for BF Related Posts via Embeddings (DB).
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;

$table_name = $wpdb->prefix . 'related_posts_embeddings';

// Log the uninstall
if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
    error_log( '[bf_wp_related_embeddings_db] Uninstalling plugin, dropping table: ' . $table_name );
}

// Drop the table
$wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );

// Clean up options
delete_option( 'bf_re_emb_table_created' );

if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
    error_log( '[bf_wp_related_embeddings_db] Uninstall complete' );
}
