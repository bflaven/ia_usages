<?php
/**
 * Uninstall hook — runs when the plugin is deleted from WP admin.
 * Drops both RAG tables and removes the plugin option.
 *
 * This file is called directly by WordPress, not via require_once,
 * so we must guard it and bootstrap the plugin constants manually.
 */

defined( 'WP_UNINSTALL_PLUGIN' ) || exit;

// Bootstrap minimum constants (plugin file is not loaded during uninstall).
define( 'RSS_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );

require_once RSS_PLUGIN_DIR . 'includes/class-db.php';

RSS_DB::drop_tables();
delete_option( 'rss_db_version' );
