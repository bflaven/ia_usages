<?php
/**
 * Uninstall handler for BF Related Posts via Embeddings (DB)
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;

$table_name = $wpdb->prefix . 'related_posts_embeddings';

$wpdb->query( "DROP TABLE IF EXISTS `{$table_name}`" );

delete_option( 'bf_re_emb_table_created' );
delete_option( 'bf_re_emb_creation_method' );
