<?php
/**
 * Plugin Name: Breadcrumb Migration
 * Description: Validate spaCy/Wikidata pipeline proposals and publish enriched taxonomy terms.
 * Version:     1.27.0
 * Author:      Bruno Flaven + Claude Code
 * Text Domain: breadcrumb-migration
 * Domain Path: /languages
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'BM_VERSION',       '1.27.0' );
define( 'BM_PLUGIN_DIR',    plugin_dir_path( __FILE__ ) );
define( 'BM_PLUGIN_URL',    plugin_dir_url( __FILE__ ) );

// Table names (resolved after $wpdb is available)
function bm_tables(): array {
	global $wpdb;
	return [
		'terms'     => $wpdb->prefix . 'breadcrumb_terms',
		'proposals' => $wpdb->prefix . 'breadcrumb_proposals',
		'redirects' => $wpdb->prefix . 'breadcrumb_redirects',
	];
}

require_once BM_PLUGIN_DIR . 'includes/db-tables.php';
require_once BM_PLUGIN_DIR . 'includes/breadcrumb-simulator.php';
require_once BM_PLUGIN_DIR . 'includes/ajax-handler.php';
require_once BM_PLUGIN_DIR . 'includes/import-export.php';
require_once BM_PLUGIN_DIR . 'includes/admin-page.php';

register_activation_hook( __FILE__, 'bm_create_tables' );

add_action( 'admin_menu',             'bm_admin_menu' );
add_action( 'admin_enqueue_scripts',  'bm_enqueue_assets' );

// AJAX — authenticated users only
add_action( 'wp_ajax_bm_validate_proposal',   'bm_ajax_validate_proposal' );
add_action( 'wp_ajax_bm_simulate_breadcrumb', 'bm_ajax_simulate_breadcrumb' );
add_action( 'wp_ajax_bm_publish_term',        'bm_ajax_publish_term' );
add_action( 'wp_ajax_bm_update_proposal',     'bm_ajax_update_proposal' );
add_action( 'wp_ajax_bm_empty_tables',        'bm_ajax_empty_tables' );
add_action( 'wp_ajax_bm_scan_delta',         'bm_ajax_scan_delta' );
add_action( 'wp_ajax_bm_add_delta_term',          'bm_ajax_add_delta_term' );
add_action( 'wp_ajax_bm_bulk_add_delta_terms',    'bm_ajax_bulk_add_delta_terms' );
add_action( 'wp_ajax_bm_search_wikidata',    'bm_ajax_search_wikidata' );
add_action( 'wp_ajax_bm_bulk_assign',        'bm_ajax_bulk_assign' );
add_action( 'wp_ajax_bm_bulk_check',         'bm_ajax_bulk_check' );
add_action( 'wp_ajax_bm_bulk_publish',            'bm_ajax_bulk_publish' );
add_action( 'wp_ajax_bm_fetch_wikidata_description', 'bm_ajax_fetch_wikidata_description' );
add_action( 'wp_ajax_bm_bulk_save_description',      'bm_ajax_bulk_save_description' );
add_action( 'wp_ajax_bm_sync_descriptions',             'bm_ajax_sync_descriptions' );
add_action( 'wp_ajax_bm_refresh_single_description',   'bm_ajax_refresh_single_description' );
add_action( 'wp_ajax_bm_update_original_term',         'bm_ajax_update_original_term' );
add_action( 'wp_ajax_bm_update_breadcrumb',            'bm_ajax_update_breadcrumb' );

// admin-post — file import + CSV export + settings save
add_action( 'admin_post_bm_import',         'bm_handle_import' );
add_action( 'admin_post_bm_export',         'bm_handle_export' );
add_action( 'admin_post_bm_save_settings',  'bm_handle_save_settings' );

// ── Admin menu ────────────────────────────────────────────────────────────────

function bm_admin_menu(): void {
	add_menu_page(
		__( 'Breadcrumb Migration', 'breadcrumb-migration' ),
		__( 'Breadcrumb Migration', 'breadcrumb-migration' ),
		'manage_options',
		'breadcrumb-migration',
		'bm_render_admin_page',
		'dashicons-admin-links',
		30
	);
}

// ── Assets ────────────────────────────────────────────────────────────────────

function bm_enqueue_assets( string $hook ): void {
	if ( 'toplevel_page_breadcrumb-migration' !== $hook ) {
		return;
	}
	wp_enqueue_style(
		'bm-admin',
		BM_PLUGIN_URL . 'assets/admin.css',
		[],
		BM_VERSION
	);
	wp_enqueue_script(
		'bm-admin',
		BM_PLUGIN_URL . 'assets/admin.js',
		[ 'jquery' ],
		BM_VERSION,
		true
	);
	$bm_settings = get_option( 'bm_settings', [] );
	wp_localize_script( 'bm-admin', 'bmData', [
		'ajaxUrl'      => admin_url( 'admin-ajax.php' ),
		'nonce'        => wp_create_nonce( 'bm_nonce' ),
		'wikidataLang' => $bm_settings['wikidata_lang'] ?? 'en',
		'i18n'         => [
			'confirmPublish' => __( 'Publish this term to WordPress? This will update the live taxonomy.', 'breadcrumb-migration' ),
			'confirmReject'  => __( 'Reject this proposal?', 'breadcrumb-migration' ),
			'publishing'     => __( 'Publishing…', 'breadcrumb-migration' ),
			'published'      => __( 'Published', 'breadcrumb-migration' ),
			'error'          => __( 'Error — see console.', 'breadcrumb-migration' ),
			'savedSynced'    => __( 'Saved and synced to WordPress.', 'breadcrumb-migration' ),
		],
	] );
}
