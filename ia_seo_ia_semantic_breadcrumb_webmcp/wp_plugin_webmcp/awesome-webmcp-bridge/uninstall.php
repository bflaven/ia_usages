<?php
// Only runs when admin clicks "Delete" on the plugin — not on deactivation.
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

delete_option( 'webmcp_enabled' );
delete_option( 'webmcp_tools' );
delete_option( 'webmcp_rate_limit' );
