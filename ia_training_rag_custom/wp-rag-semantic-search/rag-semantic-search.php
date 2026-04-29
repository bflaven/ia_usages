<?php
/**
 * Plugin Name:  RAG Semantic Search
 * Plugin URI:   https://github.com/bflaven
 * Description:  Imports RAG bridge data (rag_bridge.json) into WordPress and
 *               exposes semantic search results via a shortcode [rag_search].
 * Version:      1.0.10
 * Author:       Bruno Flaven
 * License:      GPL-2.0-or-later
 * Text Domain:  rag-semantic-search
 *
 * Table of contents:
 *   1. Constants
 *   2. Bootstrap (include class files)
 *   3. Activation hook   → create tables
 *   4. Deactivation hook → no-op (data preserved)
 *   5. Uninstall hook    → drop tables
 */

defined( 'ABSPATH' ) || exit;

// ── 1. Constants ─────────────────────────────────────────────────────────────

define( 'RSS_VERSION',    '1.0.10' );
define( 'RSS_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( 'RSS_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

/**
 * Table names — always use these constants, never hard-code.
 * $wpdb->prefix is prepended at runtime (e.g. "wp_rag_posts").
 */
function rss_table_posts(): string {
    global $wpdb;
    return $wpdb->prefix . 'rag_posts';
}

function rss_table_results(): string {
    global $wpdb;
    return $wpdb->prefix . 'rag_results';
}

// ── 2. Bootstrap ─────────────────────────────────────────────────────────────

require_once RSS_PLUGIN_DIR . 'includes/class-db.php';
require_once RSS_PLUGIN_DIR . 'includes/class-importer.php';
require_once RSS_PLUGIN_DIR . 'includes/class-search.php';
require_once RSS_PLUGIN_DIR . 'includes/class-widget.php';

// ── 3. Activation ─────────────────────────────────────────────────────────────

register_activation_hook( __FILE__, 'rss_activate' );

function rss_activate(): void {
    // Suppress any accidental output from dbDelta / upgrade.php so WordPress
    // does not report "unexpected output during activation".
    ob_start();
    RSS_DB::create_tables();
    ob_end_clean();
    update_option( 'rss_db_version', RSS_VERSION );
}

// ── 3b. Upgrade on plugins_loaded ─────────────────────────────────────────────
// Runs every request. Creates tables when files are copied directly (no
// activation hook) or when the stored version is behind RSS_VERSION.

add_action( 'plugins_loaded', 'rss_maybe_upgrade' );

function rss_maybe_upgrade(): void {
    global $wpdb;

    // Check table existence first — handles direct file copies where the
    // activation hook never fired, regardless of what version is stored.
    $missing  = ! $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', rss_table_results() ) );
    $outdated = version_compare( (string) get_option( 'rss_db_version', '0' ), RSS_VERSION, '<' );

    if ( $missing || $outdated ) {
        RSS_DB::create_tables();
        update_option( 'rss_db_version', RSS_VERSION );
    }
}

// ── 4. Deactivation ───────────────────────────────────────────────────────────

register_deactivation_hook( __FILE__, 'rss_deactivate' );

function rss_deactivate(): void {
    // Intentional no-op: data is preserved across deactivation.
    // Tables are only dropped on full uninstall (see uninstall.php).
}

// ── 5. Sidebar widget ─────────────────────────────────────────────────────────
// Force the classic widget screen (wp-admin/widgets.php) so that
// register_widget() produces a visible, draggable widget.
// Without this, WordPress 5.8+ loads the Gutenberg block widget editor
// and classic WP_Widget subclasses are hidden inside a "Legacy Widget" block.

add_action( 'after_setup_theme', 'rss_disable_block_widgets' );

function rss_disable_block_widgets(): void {
    remove_theme_support( 'widgets-block-editor' );
}

add_action( 'widgets_init', 'rss_register_widget' );

function rss_register_widget(): void {
    register_widget( 'RSS_Widget' );
}

// ── 7. Admin menu ─────────────────────────────────────────────────────────────

add_action( 'admin_menu', 'rss_admin_menu' );

function rss_admin_menu(): void {
    add_menu_page(
        __( 'RAG Semantic Search', 'rag-semantic-search' ),
        __( 'RAG Search',          'rag-semantic-search' ),
        'manage_options',
        'rag-semantic-search',
        'rss_admin_page_render',
        'dashicons-search',
        80
    );
}

function rss_admin_page_render(): void {
    require_once RSS_PLUGIN_DIR . 'admin/admin-page.php';
}

// ── 8. Enqueue admin styles ───────────────────────────────────────────────────

add_action( 'admin_enqueue_scripts', 'rss_admin_styles' );

function rss_admin_styles( string $hook ): void {
    if ( $hook !== 'toplevel_page_rag-semantic-search' ) {
        return;
    }
    wp_enqueue_style(
        'rss-admin',
        RSS_PLUGIN_URL . 'admin/admin.css',
        [],
        RSS_VERSION
    );
}

// ── 7. Front-end search CSS ───────────────────────────────────────────────────

add_action( 'wp_enqueue_scripts', 'rss_frontend_styles' );

function rss_frontend_styles(): void {
    wp_enqueue_style(
        'rss-search',
        RSS_PLUGIN_URL . 'public/search.css',
        [],
        RSS_VERSION
    );
}

// ── 8. Standard-search redirect ───────────────────────────────────────────────
// Runs before any output so wp_redirect() works cleanly.

add_action( 'template_redirect', 'rss_maybe_redirect_standard_search' );

function rss_maybe_redirect_standard_search(): void {
    $mode  = isset( $_GET['rss_mode'] ) ? sanitize_key( $_GET['rss_mode'] ) : '';
    $query = isset( $_GET['rss_q'] )    ? sanitize_text_field( wp_unslash( $_GET['rss_q'] ) ) : '';

    if ( $mode === 'standard' && $query !== '' ) {
        wp_safe_redirect( home_url( '/?s=' . urlencode( $query ) ) );
        exit;
    }
}

// ── 9. Shortcode [rag_search] ─────────────────────────────────────────────────

add_shortcode( 'rag_search', 'rss_shortcode' );

function rss_shortcode( array $atts ): string {
    $atts = shortcode_atts(
        [
            'limit' => 10,
            'query' => '',
        ],
        $atts,
        'rag_search'
    );

    // Resolve query: URL param takes precedence over shortcode attribute.
    $query            = isset( $_GET['rss_q'] )
        ? sanitize_text_field( wp_unslash( $_GET['rss_q'] ) )
        : sanitize_text_field( $atts['query'] );

    $semantic_enabled = (bool) get_option( 'rss_semantic_enabled', '1' );

    // When semantic search is disabled force standard mode so the redirect
    // hook sends the query to the native WP search (/?s=query).
    $mode  = $semantic_enabled
        ? ( isset( $_GET['rss_mode'] ) ? sanitize_key( $_GET['rss_mode'] ) : 'semantic' )
        : 'standard';
    $limit = max( 1, min( 50, (int) $atts['limit'] ) );

    // Run search only in semantic mode with a non-empty query.
    // Strategy: check rag_results cache first; fall back to a live FULLTEXT
    // search and persist the results so subsequent identical queries are free.
    $results = [];
    if ( $query !== '' && $mode === 'semantic' ) {
        RSS_DB::purge_expired_results();

        $cached = RSS_DB::get_cached_results( $query );
        if ( ! empty( $cached ) ) {
            // Cache hit — reconstruct result objects from stored rows.
            $results = RSS_Search::format_cached( $cached, $query );
        } else {
            // Cache miss — run live search, then persist for future requests.
            $results = RSS_Search::search( $query, $limit );
            if ( ! empty( $results ) ) {
                $ttl_days = (int) get_option( 'rss_cache_ttl_days', 7 );
                RSS_DB::save_results( $query, $results, $ttl_days );
            }
        }
    }

    // Render via template, capture output.
    ob_start();
    include RSS_PLUGIN_DIR . 'templates/semantic-search-results.php';
    return ob_get_clean();
}

// ── 10. Public theme function: rag_semantic_search() ──────────────────────────
// Call this from your theme's search.php (or any template) to display a
// promotional banner pointing visitors to the semantic search page.
//
// Usage:
//   if ( function_exists( 'rag_semantic_search' ) ) {
//       rag_semantic_search();
//   }

function rag_semantic_search(): void {
    $text = get_option( 'rss_promo_text', '' );
    if ( empty( trim( strip_tags( $text ) ) ) ) {
        return;
    }
    echo '<div class="rss-promo-banner">' . wp_kses_post( $text ) . '</div>';
}
