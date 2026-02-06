<?php
/**
 * Plugin Name: BF Test Table
 * Description: Minimal plugin to test table creation and inserts via dbDelta.
 * Version: 0.1.0
 * Author: BF
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Helper: full table name.
 */
function bf_test_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'bf_test_table';
}

/**
 * ACTIVATION: create table and insert a few rows.
 */
function bf_test_table_activate() {
    global $wpdb;

    $table_name      = bf_test_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE {$table_name} (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        label VARCHAR(191) NOT NULL,
        value_int INT(11) NOT NULL,
        PRIMARY KEY  (id)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';

    // Debug: log the SQL and table name
    error_log( '[bf_test_table] Running dbDelta for table: ' . $table_name );
    error_log( '[bf_test_table] SQL: ' . $sql );

    dbDelta( $sql );

    // Insert a couple of test rows if table is empty.
    $count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$table_name}" );

    if ( $count === 0 ) {
        error_log( '[bf_test_table] Inserting sample rows into ' . $table_name );
        $wpdb->insert(
            $table_name,
            array( 'label' => 'first_row', 'value_int' => 1 ),
            array( '%s', '%d' )
        );
        $wpdb->insert(
            $table_name,
            array( 'label' => 'second_row', 'value_int' => 2 ),
            array( '%s', '%d' )
        );
    } else {
        error_log( '[bf_test_table] Table not empty, skipping sample inserts.' );
    }
}
register_activation_hook( __FILE__, 'bf_test_table_activate' );

/**
 * UNINSTALL: drop the table.
 */
function bf_test_table_uninstall() {
    global $wpdb;

    $table_name = bf_test_table_name();
    error_log( '[bf_test_table] Dropping table: ' . $table_name );
    $wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
}
register_uninstall_hook( __FILE__, 'bf_test_table_uninstall' );

/**
 * Simple admin page to show table contents.
 */
function bf_test_table_admin_menu() {
    add_options_page(
        'BF Test Table',
        'BF Test Table',
        'manage_options',
        'bf-test-table',
        'bf_test_table_render_admin_page'
    );
}
add_action( 'admin_menu', 'bf_test_table_admin_menu' );

function bf_test_table_render_admin_page() {
    global $wpdb;

    $table_name = bf_test_table_name();

    // Try to fetch rows, but catch errors.
    $rows = array();
    $error = '';

    try {
        $rows = $wpdb->get_results( "SELECT * FROM {$table_name} ORDER BY id ASC", ARRAY_A );
    } catch ( Exception $e ) {
        $error = $e->getMessage();
    }

    echo '<div class="wrap">';
    echo '<h1>BF Test Table</h1>';

    echo '<p>Table name: <code>' . esc_html( $table_name ) . '</code></p>';

    if ( $error ) {
        echo '<p><strong>Error querying table:</strong> ' . esc_html( $error ) . '</p>';
    } elseif ( empty( $rows ) ) {
        echo '<p>No rows found (table may not exist or is empty).</p>';
    } else {
        echo '<table class="widefat fixed striped">';
        echo '<thead><tr><th>ID</th><th>Label</th><th>Value</th></tr></thead><tbody>';
        foreach ( $rows as $row ) {
            echo '<tr>';
            echo '<td>' . esc_html( $row['id'] ) . '</td>';
            echo '<td>' . esc_html( $row['label'] ) . '</td>';
            echo '<td>' . esc_html( $row['value_int'] ) . '</td>';
            echo '</tr>';
        }
        echo '</tbody></table>';
    }

    echo '</div>';
}
