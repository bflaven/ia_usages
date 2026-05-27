<?php
/**
 * Plugin Name: WebMCP for WordPress (awesome-webmcp-bridge)
 * Plugin URI:  https://github.com/brunoflaven/wp-webmcp
 * Description: Exposes WordPress content as structured tools for AI agents via the WebMCP proposed standard.
 * Version:     1.0.3
 * Author:      Bruno Flaven + Claude Code
 * License:     GPL-2.0-or-later
 * Text Domain: webmcp
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'WEBMCP_VERSION', '1.0.3' );
define( 'WEBMCP_DIR', plugin_dir_path( __FILE__ ) );
define( 'WEBMCP_URL', plugin_dir_url( __FILE__ ) );

require_once WEBMCP_DIR . 'includes/class-webmcp-tools.php';
require_once WEBMCP_DIR . 'includes/class-webmcp-manifest.php';
require_once WEBMCP_DIR . 'includes/class-webmcp-admin.php';

add_action( 'rest_api_init', [ 'WebMCP_Tools', 'register_rest_routes' ] );
add_action( 'wp_head', [ 'WebMCP_Manifest', 'inject_manifest' ] );
add_action( 'wp_enqueue_scripts', 'webmcp_enqueue_scripts' );
add_action( 'admin_menu', [ 'WebMCP_Admin', 'register_menu' ] );
add_action( 'admin_init', [ 'WebMCP_Admin', 'register_settings' ] );

function webmcp_enqueue_scripts() {
    if ( ! get_option( 'webmcp_enabled', 1 ) ) {
        return;
    }
    wp_enqueue_script(
        'webmcp',
        WEBMCP_URL . 'assets/webmcp.js',
        [],
        WEBMCP_VERSION,
        true
    );
    wp_localize_script( 'webmcp', 'webmcpConfig', [
        'restUrl'  => esc_url_raw( rest_url( 'webmcp/v1/' ) ),
        'nonce'    => wp_create_nonce( 'wp_rest' ),
        'siteUrl'  => get_site_url(),
        'siteName' => get_bloginfo( 'name' ),
    ] );
}

register_activation_hook( __FILE__, 'webmcp_activate' );
function webmcp_activate() {
    add_option( 'webmcp_enabled', 1 );
    add_option( 'webmcp_rate_limit', 60 );
    add_option( 'webmcp_tools', [
        'search_posts'    => 1,
        'list_categories' => 1,
        'get_latest'      => 1,
        'get_toc'         => 1,
        'get_related'     => 1,
    ] );
}

register_deactivation_hook( __FILE__, 'webmcp_deactivate' );
function webmcp_deactivate() {
    // intentionally keeps options — user data preserved on deactivate
}
