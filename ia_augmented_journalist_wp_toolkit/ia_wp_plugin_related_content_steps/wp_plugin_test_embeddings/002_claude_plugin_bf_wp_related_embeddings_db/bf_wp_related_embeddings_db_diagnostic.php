<?php
/**
 * Plugin Name: BF Related Posts via Embeddings (DB) - DIAGNOSTIC
 * Description: Diagnostic version to troubleshoot table creation
 * Version: 0.5.1-diag
 * Author: IA with a bit of Bruno Flaven
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'BF_RE_EMB_DEBUG', true );

function bf_re_emb_log( $message ) {
    error_log( '[bf_wp_related_embeddings_db] ' . $message );
}

function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}

/**
 * ACTIVATION with detailed diagnostics
 */
function bf_re_emb_activate() {
    global $wpdb;

    bf_re_emb_log( '========================================' );
    bf_re_emb_log( 'DIAGNOSTIC ACTIVATION STARTING' );
    bf_re_emb_log( '========================================' );

    // 1. Check database connection
    bf_re_emb_log( 'Database name: ' . DB_NAME );
    bf_re_emb_log( 'Database user: ' . DB_USER );
    bf_re_emb_log( 'Database host: ' . DB_HOST );
    bf_re_emb_log( 'Table prefix: ' . $wpdb->prefix );

    $table_name      = bf_re_emb_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    bf_re_emb_log( "Target table name: {$table_name}" );
    bf_re_emb_log( "Charset/Collate: {$charset_collate}" );

    // 2. Check current database grants
    $grants = $wpdb->get_results( "SHOW GRANTS FOR CURRENT_USER()", ARRAY_A );
    bf_re_emb_log( 'Database grants: ' . print_r( $grants, true ) );

    // 3. Test basic database operations
    $test_query = $wpdb->get_var( "SELECT 1" );
    bf_re_emb_log( "Basic query test (SELECT 1): " . ( $test_query === '1' ? 'PASS' : 'FAIL' ) );

    // 4. Check if table already exists
    $existing = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    if ( $existing === $table_name ) {
        bf_re_emb_log( "WARNING: Table {$table_name} already exists! Dropping it..." );
        $drop_result = $wpdb->query( "DROP TABLE IF EXISTS {$table_name}" );
        bf_re_emb_log( "Drop result: " . ( $drop_result !== false ? 'SUCCESS' : 'FAILED - ' . $wpdb->last_error ) );
    }

    // 5. Try METHOD 1: Using dbDelta (WordPress standard)
    bf_re_emb_log( '----------------------------------------' );
    bf_re_emb_log( 'METHOD 1: Trying dbDelta...' );
    
    $sql = "CREATE TABLE {$table_name} (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        post_id BIGINT(20) UNSIGNED NOT NULL,
        related_post_id BIGINT(20) UNSIGNED NOT NULL,
        similarity DOUBLE NOT NULL,
        rank INT(11) NOT NULL,
        PRIMARY KEY  (id),
        KEY post_id (post_id),
        KEY related_post_id (related_post_id)
    ) {$charset_collate};";

    bf_re_emb_log( "SQL for dbDelta: " . $sql );

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    
    $dbdelta_result = dbDelta( $sql );
    bf_re_emb_log( 'dbDelta returned: ' . print_r( $dbdelta_result, true ) );
    
    if ( $wpdb->last_error ) {
        bf_re_emb_log( 'dbDelta ERROR: ' . $wpdb->last_error );
    }

    // Check if dbDelta worked
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    
    if ( $table_exists === $table_name ) {
        bf_re_emb_log( '✓ METHOD 1 SUCCESS: Table created via dbDelta' );
        update_option( 'bf_re_emb_table_created', true );
        update_option( 'bf_re_emb_creation_method', 'dbDelta' );
        bf_re_emb_log( '========================================' );
        return;
    }

    // 6. Try METHOD 2: Direct SQL query
    bf_re_emb_log( '----------------------------------------' );
    bf_re_emb_log( 'METHOD 1 FAILED - Trying METHOD 2: Direct SQL...' );
    
    $sql_direct = "CREATE TABLE IF NOT EXISTS {$table_name} (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        post_id BIGINT(20) UNSIGNED NOT NULL,
        related_post_id BIGINT(20) UNSIGNED NOT NULL,
        similarity DOUBLE NOT NULL,
        rank INT(11) NOT NULL,
        PRIMARY KEY (id),
        KEY post_id (post_id),
        KEY related_post_id (related_post_id)
    ) {$charset_collate}";

    bf_re_emb_log( "Direct SQL: " . $sql_direct );
    
    $direct_result = $wpdb->query( $sql_direct );
    
    if ( $wpdb->last_error ) {
        bf_re_emb_log( '✗ Direct SQL ERROR: ' . $wpdb->last_error );
    } else {
        bf_re_emb_log( "Direct query result: " . var_export( $direct_result, true ) );
    }

    // Check again
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    
    if ( $table_exists === $table_name ) {
        bf_re_emb_log( '✓ METHOD 2 SUCCESS: Table created via direct SQL' );
        update_option( 'bf_re_emb_table_created', true );
        update_option( 'bf_re_emb_creation_method', 'direct_sql' );
        bf_re_emb_log( '========================================' );
        return;
    }

    // 7. Try METHOD 3: Simplified table without charset
    bf_re_emb_log( '----------------------------------------' );
    bf_re_emb_log( 'METHOD 2 FAILED - Trying METHOD 3: Simplified SQL...' );
    
    $sql_simple = "CREATE TABLE IF NOT EXISTS {$table_name} (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        post_id BIGINT UNSIGNED NOT NULL,
        related_post_id BIGINT UNSIGNED NOT NULL,
        similarity DOUBLE NOT NULL,
        rank INT NOT NULL,
        PRIMARY KEY (id),
        INDEX (post_id),
        INDEX (related_post_id)
    )";

    bf_re_emb_log( "Simplified SQL: " . $sql_simple );
    
    $simple_result = $wpdb->query( $sql_simple );
    
    if ( $wpdb->last_error ) {
        bf_re_emb_log( '✗ Simplified SQL ERROR: ' . $wpdb->last_error );
    } else {
        bf_re_emb_log( "Simplified query result: " . var_export( $simple_result, true ) );
    }

    // Final check
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    
    if ( $table_exists === $table_name ) {
        bf_re_emb_log( '✓ METHOD 3 SUCCESS: Table created with simplified SQL' );
        update_option( 'bf_re_emb_table_created', true );
        update_option( 'bf_re_emb_creation_method', 'simplified_sql' );
    } else {
        bf_re_emb_log( '✗✗✗ ALL METHODS FAILED ✗✗✗' );
        bf_re_emb_log( 'This indicates a serious database permission or configuration issue' );
        update_option( 'bf_re_emb_table_created', false );
        update_option( 'bf_re_emb_creation_method', 'all_failed' );
    }

    bf_re_emb_log( '========================================' );
    bf_re_emb_log( 'DIAGNOSTIC ACTIVATION COMPLETE' );
    bf_re_emb_log( '========================================' );
}
register_activation_hook( __FILE__, 'bf_re_emb_activate' );

/**
 * Enhanced admin notice
 */
function bf_re_emb_activation_notice() {
    if ( ! get_transient( 'bf_re_emb_activation_notice' ) ) {
        return;
    }
    
    delete_transient( 'bf_re_emb_activation_notice' );
    
    $table_created = get_option( 'bf_re_emb_table_created', false );
    $creation_method = get_option( 'bf_re_emb_creation_method', 'unknown' );
    $table_name = bf_re_emb_table_name();
    
    if ( $table_created ) {
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p><strong>✓ BF Related Posts Embeddings:</strong> Table <code>' . esc_html( $table_name ) . '</code> created successfully!</p>';
        echo '<p>Creation method: <code>' . esc_html( $creation_method ) . '</code></p>';
        echo '<p><strong>CHECK YOUR DOCKER LOGS NOW</strong> to see the full diagnostic output:</p>';
        echo '<p><code>docker logs your-container 2>&1 | grep bf_wp_related_embeddings_db</code></p>';
        echo '</div>';
    } else {
        global $wpdb;
        echo '<div class="notice notice-error">';
        echo '<p><strong>✗ BF Related Posts Embeddings:</strong> Table creation failed!</p>';
        echo '<p><strong>URGENT: Check your Docker logs for detailed diagnostic information:</strong></p>';
        echo '<p><code>docker logs your-container 2>&1 | grep bf_wp_related_embeddings_db</code></p>';
        echo '<p>Database info:</p>';
        echo '<ul>';
        echo '<li>Database: <code>' . esc_html( DB_NAME ) . '</code></li>';
        echo '<li>User: <code>' . esc_html( DB_USER ) . '</code></li>';
        echo '<li>Prefix: <code>' . esc_html( $wpdb->prefix ) . '</code></li>';
        echo '<li>Target table: <code>' . esc_html( $table_name ) . '</code></li>';
        echo '</ul>';
        echo '</div>';
    }
}
add_action( 'admin_notices', 'bf_re_emb_activation_notice' );

// Set activation notice flag
function bf_re_emb_set_activation_notice() {
    set_transient( 'bf_re_emb_activation_notice', true, 30 );
}
register_activation_hook( __FILE__, 'bf_re_emb_set_activation_notice' );

/**
 * Simple diagnostic page
 */
function bf_re_emb_admin_menu() {
    add_options_page(
        'Related Embeddings Diagnostic',
        'Related Embeddings',
        'manage_options',
        'bf-wp-related-embeddings-db',
        'bf_re_emb_render_diagnostic_page'
    );
}
add_action( 'admin_menu', 'bf_re_emb_admin_menu' );

function bf_re_emb_render_diagnostic_page() {
    global $wpdb;
    
    $table_name = bf_re_emb_table_name();
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    $creation_method = get_option( 'bf_re_emb_creation_method', 'not set' );
    
    ?>
    <div class="wrap">
        <h1>BF Related Embeddings - Diagnostic Mode</h1>
        
        <div class="card">
            <h2>Database Status</h2>
            <table class="widefat">
                <tr>
                    <td><strong>Database Name:</strong></td>
                    <td><code><?php echo esc_html( DB_NAME ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Database User:</strong></td>
                    <td><code><?php echo esc_html( DB_USER ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Database Host:</strong></td>
                    <td><code><?php echo esc_html( DB_HOST ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Table Prefix:</strong></td>
                    <td><code><?php echo esc_html( $wpdb->prefix ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Target Table:</strong></td>
                    <td><code><?php echo esc_html( $table_name ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Table Exists:</strong></td>
                    <td>
                        <?php if ( $table_exists === $table_name ) : ?>
                            <span style="color: green; font-weight: bold;">✓ YES</span>
                        <?php else : ?>
                            <span style="color: red; font-weight: bold;">✗ NO</span>
                        <?php endif; ?>
                    </td>
                </tr>
                <tr>
                    <td><strong>Creation Method:</strong></td>
                    <td><code><?php echo esc_html( $creation_method ); ?></code></td>
                </tr>
            </table>
        </div>

        <div class="card">
            <h2>Next Steps</h2>
            
            <?php if ( $table_exists === $table_name ) : ?>
                <p style="color: green;">✓ Table exists! You can now use the full version of the plugin.</p>
                <ol>
                    <li>Deactivate this diagnostic version</li>
                    <li>Activate the main plugin version</li>
                    <li>Import your CSV data</li>
                </ol>
            <?php else : ?>
                <p style="color: red;">✗ Table creation failed. Check the diagnostic output:</p>
                <ol>
                    <li><strong>View Docker logs:</strong><br>
                        <code>docker logs your-container 2>&1 | grep bf_wp_related_embeddings_db</code>
                    </li>
                    <li><strong>Check the diagnostic output above</strong> - it will show:
                        <ul>
                            <li>Which creation method(s) were tried</li>
                            <li>Any SQL errors</li>
                            <li>Database permissions</li>
                        </ul>
                    </li>
                    <li><strong>Try manual table creation</strong> in phpMyAdmin using the SQL below</li>
                </ol>
                
                <h3>Manual Table Creation SQL</h3>
                <p>Copy this and run it in phpMyAdmin:</p>
                <textarea readonly style="width: 100%; height: 200px; font-family: monospace;">CREATE TABLE <?php echo esc_html( $table_name ); ?> (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    post_id BIGINT UNSIGNED NOT NULL,
    related_post_id BIGINT UNSIGNED NOT NULL,
    similarity DOUBLE NOT NULL,
    rank INT NOT NULL,
    PRIMARY KEY (id),
    INDEX (post_id),
    INDEX (related_post_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;</textarea>
            <?php endif; ?>
        </div>
    </div>
    <?php
}
