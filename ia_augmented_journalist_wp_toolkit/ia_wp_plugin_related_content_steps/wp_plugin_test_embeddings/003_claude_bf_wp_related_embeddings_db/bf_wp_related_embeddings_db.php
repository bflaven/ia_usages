<?php
/**
 * Plugin Name: BF Related Posts via Embeddings (DB)
 * Description: Custom table for related posts (embeddings) + CSV import + meta box.
 * Version: 0.5.0
 * Author: IA with a bit of Bruno Flaven
 * Text Domain: bf-wp-related-embeddings-db
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'BF_RE_EMB_DEFAULT_CSV_FILENAME', 'related_posts_embeddings_settings_csv.csv' );
define( 'BF_RE_EMB_DEBUG', true ); // Set to false in production

/**
 * Debug logging helper
 */
function bf_re_emb_log( $message ) {
    if ( defined( 'BF_RE_EMB_DEBUG' ) && BF_RE_EMB_DEBUG ) {
        error_log( '[bf_wp_related_embeddings_db] ' . $message );
    }
}

/**
 * Table name helper: wp_related_posts_embeddings (with prefix).
 */
function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}

/**
 * ACTIVATION: create table.
 */
function bf_re_emb_activate() {
    global $wpdb;

    bf_re_emb_log( 'Starting plugin activation...' );

    $table_name      = bf_re_emb_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    bf_re_emb_log( "Creating table: {$table_name}" );
    bf_re_emb_log( "Charset/Collate: {$charset_collate}" );

    $sql = "CREATE TABLE {$table_name} (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        post_id BIGINT(20) UNSIGNED NOT NULL,
        related_post_id BIGINT(20) UNSIGNED NOT NULL,
        similarity DOUBLE NOT NULL,
        `rank` INT(11) NOT NULL,
        PRIMARY KEY  (id),
        KEY post_id (post_id),
        KEY related_post_id (related_post_id)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';

    // Execute dbDelta
    $result = dbDelta( $sql );
    
    bf_re_emb_log( 'dbDelta result: ' . print_r( $result, true ) );

    // Verify table was created
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    
    if ( $table_exists === $table_name ) {
        bf_re_emb_log( "✓ Table {$table_name} created successfully!" );
        update_option( 'bf_re_emb_table_created', true );
    } else {
        bf_re_emb_log( "✗ ERROR: Table {$table_name} was NOT created!" );
        update_option( 'bf_re_emb_table_created', false );
    }

    // Show activation notice
    set_transient( 'bf_re_emb_activation_notice', true, 30 );
}
register_activation_hook( __FILE__, 'bf_re_emb_activate' );

/**
 * Show admin notice after activation
 */
function bf_re_emb_activation_notice() {
    if ( get_transient( 'bf_re_emb_activation_notice' ) ) {
        delete_transient( 'bf_re_emb_activation_notice' );
        
        $table_created = get_option( 'bf_re_emb_table_created', false );
        $table_name = bf_re_emb_table_name();
        
        if ( $table_created ) {
            echo '<div class="notice notice-success is-dismissible">';
            echo '<p><strong>BF Related Posts Embeddings:</strong> Plugin activated successfully! Table <code>' . esc_html( $table_name ) . '</code> was created.</p>';
            echo '<p>Next step: Go to <a href="' . admin_url( 'options-general.php?page=bf-wp-related-embeddings-db' ) . '">Settings → Related Embeddings</a> to import your CSV.</p>';
            echo '</div>';
        } else {
            echo '<div class="notice notice-error is-dismissible">';
            echo '<p><strong>BF Related Posts Embeddings:</strong> Plugin activated but table creation failed! Check your error logs.</p>';
            echo '</div>';
        }
    }
}
add_action( 'admin_notices', 'bf_re_emb_activation_notice' );

/**
 * Fetch related posts for a given post_id.
 */
function bf_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;

    $table_name = bf_re_emb_table_name();

    $sql = $wpdb->prepare(
        "SELECT related_post_id, similarity, `rank`
         FROM {$table_name}
         WHERE post_id = %d
         ORDER BY `rank` ASC
         LIMIT %d",
        $post_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );

    if ( $wpdb->last_error ) {
        bf_re_emb_log( 'Database error in get_related_from_db: ' . $wpdb->last_error );
    }

    $out = array();
    if ( $rows ) {
        foreach ( $rows as $row ) {
            $out[] = array(
                'related_post_id' => (int) $row['related_post_id'],
                'similarity'      => (float) $row['similarity'],
                'rank'            => (int) $row['rank'],
            );
        }
    }

    return $out;
}

/**
 * Meta box: display related posts on post edit screen.
 */
function bf_re_emb_render_meta_box( WP_Post $post ) {
    global $wpdb;
    
    $post_id      = $post->ID;
    $table_name   = bf_re_emb_table_name();
    
    // Check if table exists
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    
    if ( $table_exists !== $table_name ) {
        echo '<div class="notice notice-error inline"><p>';
        echo '<strong>Error:</strong> Table <code>' . esc_html( $table_name ) . '</code> does not exist. ';
        echo 'Try deactivating and reactivating the plugin.';
        echo '</p></div>';
        return;
    }
    
    $max_related  = 10;
    $related_rows = bf_re_emb_get_related_from_db( $post_id, $max_related );

    echo '<p>';
    esc_html_e(
        'These related posts are computed offline from embeddings and stored in a custom table.',
        'bf-wp-related-embeddings-db'
    );
    echo '</p>';

    if ( empty( $related_rows ) ) {
        // Check if table has any data
        $total_count = $wpdb->get_var( "SELECT COUNT(*) FROM {$table_name}" );
        
        echo '<p><em>' . esc_html__(
            'No related posts found for this post.',
            'bf-wp-related-embeddings-db'
        ) . '</em></p>';
        
        if ( $total_count == 0 ) {
            echo '<p class="description">';
            echo 'The table is empty. Go to <a href="' . admin_url( 'options-general.php?page=bf-wp-related-embeddings-db' ) . '">Settings → Related Embeddings</a> to import your CSV.';
            echo '</p>';
        }
        
        return;
    }

    echo '<table class="widefat fixed striped">';
    echo '<thead><tr>';
    echo '<th>' . esc_html__( 'Rank', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Related Post', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '<th>' . esc_html__( 'Similarity', 'bf-wp-related-embeddings-db' ) . '</th>';
    echo '</tr></thead>';
    echo '<tbody>';

    foreach ( $related_rows as $row ) {
        $rel_id   = $row['related_post_id'];
        $rank     = $row['rank'];
        $sim      = $row['similarity'];
        $rel_post = get_post( $rel_id );

        echo '<tr>';

        echo '<td>' . esc_html( $rank ) . '</td>';

        echo '<td>';
        if ( $rel_post instanceof WP_Post ) {
            $title = get_the_title( $rel_post );
            $url   = get_edit_post_link( $rel_post );
            echo '<a href="' . esc_url( $url ) . '">';
            echo esc_html( sprintf( '%d — %s', $rel_id, $title ) );
            echo '</a>';
        } else {
            echo esc_html( sprintf( 'Post ID %d (not found)', $rel_id ) );
        }
        echo '</td>';

        echo '<td>' . esc_html( number_format( $sim, 3 ) ) . '</td>';

        echo '</tr>';
    }

    echo '</tbody>';
    echo '</table>';
}

/**
 * Register meta box.
 */
function bf_re_emb_add_meta_box() {
    add_meta_box(
        'bf_related_embeddings_meta_box',
        __( 'Related Posts (Embeddings)', 'bf-wp-related-embeddings-db' ),
        'bf_re_emb_render_meta_box',
        'post',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'bf_re_emb_add_meta_box' );

/**
 * Admin menu: CSV import page.
 */
function bf_re_emb_admin_menu() {
    add_options_page(
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        __( 'Related Embeddings', 'bf-wp-related-embeddings-db' ),
        'manage_options',
        'bf-wp-related-embeddings-db',
        'bf_re_emb_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_re_emb_admin_menu' );

/**
 * CSV import handler.
 */
function bf_re_emb_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        bf_re_emb_log( 'CSV import attempted without proper permissions' );
        return;
    }

    if ( ! isset( $_POST['bf_re_emb_import_nonce'] ) || ! wp_verify_nonce( $_POST['bf_re_emb_import_nonce'], 'bf_re_emb_import_csv' ) ) {
        bf_re_emb_log( 'CSV import nonce verification failed' );
        return;
    }

    if ( empty( $_FILES['bf_re_emb_csv']['tmp_name'] ) ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_no_file',
            __( 'No CSV file uploaded.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        bf_re_emb_log( 'No CSV file in upload' );
        return;
    }

    $tmp_name = $_FILES['bf_re_emb_csv']['tmp_name'];
    $file_size = $_FILES['bf_re_emb_csv']['size'];
    $file_name = $_FILES['bf_re_emb_csv']['name'];

    bf_re_emb_log( "Uploaded CSV: {$file_name}, size: {$file_size} bytes" );

    $handle = fopen( $tmp_name, 'r' );
    if ( ! $handle ) {
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_file_open_error',
            __( 'Could not open uploaded file.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        bf_re_emb_log( 'Could not open uploaded file' );
        return;
    }

    global $wpdb;
    $table_name = bf_re_emb_table_name();

    // Ensure table exists (if activation somehow didn't run).
    bf_re_emb_log( 'Ensuring table exists...' );
    bf_re_emb_activate();

    // Truncate current data.
    bf_re_emb_log( "Truncating table {$table_name}..." );
    $wpdb->query( "TRUNCATE TABLE {$table_name}" );

    // Read header row.
    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_bad_header',
            __( 'CSV file is empty or has no header.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        bf_re_emb_log( 'CSV has no header row' );
        return;
    }

    bf_re_emb_log( 'CSV header: ' . implode( ', ', $header ) );

    // Normalize header.
    $normalized_header = array();
    foreach ( $header as $col ) {
        $col = preg_replace( '/^\xEF\xBB\xBF/', '', $col ); // strip BOM
        $normalized_header[] = strtolower( trim( $col ) );
    }

    bf_re_emb_log( 'Normalized header: ' . implode( ', ', $normalized_header ) );

    $idx_post_id         = array_search( 'post_id', $normalized_header, true );
    $idx_related_post_id = array_search( 'related_post_id', $normalized_header, true );
    $idx_similarity      = array_search( 'similarity', $normalized_header, true );
    $idx_rank            = array_search( 'rank', $normalized_header, true );

    if ( $idx_post_id === false || $idx_related_post_id === false || $idx_similarity === false || $idx_rank === false ) {
        fclose( $handle );
        add_settings_error(
            'bf_re_emb_messages',
            'bf_re_emb_missing_columns',
            __( 'CSV must contain columns: post_id, related_post_id, similarity, rank.', 'bf-wp-related-embeddings-db' ),
            'error'
        );
        bf_re_emb_log( 'CSV missing required columns. Found: ' . implode( ', ', $normalized_header ) );
        return;
    }

    bf_re_emb_log( "Column indices - post_id: {$idx_post_id}, related_post_id: {$idx_related_post_id}, similarity: {$idx_similarity}, rank: {$idx_rank}" );

    $inserted = 0;
    $row_num = 1;
    $errors = array();

    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        $row_num++;
        
        if ( empty( array_filter( $row, 'strlen' ) ) ) {
            continue;
        }

        $post_id         = isset( $row[ $idx_post_id ] ) ? (int) $row[ $idx_post_id ] : 0;
        $related_post_id = isset( $row[ $idx_related_post_id ] ) ? (int) $row[ $idx_related_post_id ] : 0;
        $similarity_raw  = isset( $row[ $idx_similarity ] ) ? $row[ $idx_similarity ] : '0';
        $rank            = isset( $row[ $idx_rank ] ) ? (int) $row[ $idx_rank ] : 0;

        $similarity = (float) str_replace( ',', '.', $similarity_raw );

        if ( $inserted === 0 ) {
            bf_re_emb_log( "First CSV data row parsed - post_id: {$post_id}, related_post_id: {$related_post_id}, similarity: {$similarity}, rank: {$rank}" );
        }

        if ( $post_id <= 0 || $related_post_id <= 0 || $rank <= 0 ) {
            if ( count( $errors ) < 5 ) {
                $errors[] = "Row {$row_num}: Invalid data (post_id={$post_id}, related_post_id={$related_post_id}, rank={$rank})";
            }
            continue;
        }

        $result = $wpdb->insert(
            $table_name,
            array(
                'post_id'         => $post_id,
                'related_post_id' => $related_post_id,
                'similarity'      => $similarity,
                'rank'            => $rank,
            ),
            array( '%d', '%d', '%f', '%d' )
        );

        if ( $result !== false ) {
            $inserted++;
        } else {
            if ( count( $errors ) < 5 ) {
                $errors[] = "Row {$row_num}: Database insert failed - " . $wpdb->last_error;
            }
        }
    }

    fclose( $handle );

    bf_re_emb_log( "Import completed. Inserted: {$inserted} rows" );
    
    if ( ! empty( $errors ) ) {
        bf_re_emb_log( 'Errors during import: ' . implode( '; ', $errors ) );
    }

    $message = sprintf(
        __( 'Imported %d related rows (table truncated before import).', 'bf-wp-related-embeddings-db' ),
        $inserted
    );
    
    if ( ! empty( $errors ) ) {
        $message .= ' ' . sprintf( __( '%d errors occurred (check error log).', 'bf-wp-related-embeddings-db' ), count( $errors ) );
    }

    add_settings_error(
        'bf_re_emb_messages',
        'bf_re_emb_import_success',
        $message,
        $inserted > 0 ? 'updated' : 'error'
    );
}

/**
 * Settings page.
 */
function bf_re_emb_render_settings_page() {
    global $wpdb;
    
    if ( isset( $_POST['bf_re_emb_import_submit'] ) ) {
        bf_re_emb_handle_csv_import();
    }

    settings_errors( 'bf_re_emb_messages' );

    $table_name = bf_re_emb_table_name();
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    $row_count = 0;
    
    if ( $table_exists === $table_name ) {
        $row_count = $wpdb->get_var( "SELECT COUNT(*) FROM {$table_name}" );
    }

    ?>
    <div class="wrap">
        <h1><?php esc_html_e( 'Related Posts Embeddings Import', 'bf-wp-related-embeddings-db' ); ?></h1>

        <div class="card">
            <h2><?php esc_html_e( 'Database Status', 'bf-wp-related-embeddings-db' ); ?></h2>
            <table class="widefat">
                <tr>
                    <td><strong><?php esc_html_e( 'Table Name:', 'bf-wp-related-embeddings-db' ); ?></strong></td>
                    <td><code><?php echo esc_html( $table_name ); ?></code></td>
                </tr>
                <tr>
                    <td><strong><?php esc_html_e( 'Table Exists:', 'bf-wp-related-embeddings-db' ); ?></strong></td>
                    <td>
                        <?php if ( $table_exists === $table_name ) : ?>
                            <span style="color: green;">✓ <?php esc_html_e( 'Yes', 'bf-wp-related-embeddings-db' ); ?></span>
                        <?php else : ?>
                            <span style="color: red;">✗ <?php esc_html_e( 'No - Try deactivating and reactivating the plugin', 'bf-wp-related-embeddings-db' ); ?></span>
                        <?php endif; ?>
                    </td>
                </tr>
                <tr>
                    <td><strong><?php esc_html_e( 'Current Row Count:', 'bf-wp-related-embeddings-db' ); ?></strong></td>
                    <td><strong><?php echo esc_html( number_format( $row_count ) ); ?></strong></td>
                </tr>
            </table>
        </div>

        <h2><?php esc_html_e( 'CSV Import', 'bf-wp-related-embeddings-db' ); ?></h2>

        <p>
            <?php esc_html_e(
                'Upload a CSV file with columns: post_id, related_post_id, similarity, rank. The plugin will TRUNCATE the custom table and load the new data.',
                'bf-wp-related-embeddings-db'
            ); ?>
        </p>

        <p class="description">
            <?php esc_html_e( 'CSV Format Example:', 'bf-wp-related-embeddings-db' ); ?><br>
            <code>post_id,related_post_id,similarity,rank<br>
            11463,13091,0.923,1<br>
            11463,12345,0.891,2</code>
        </p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_re_emb_import_csv', 'bf_re_emb_import_nonce' ); ?>

            <table class="form-table" role="presentation">
                <tr>
                    <th scope="row">
                        <label for="bf_re_emb_csv"><?php esc_html_e( 'CSV File', 'bf-wp-related-embeddings-db' ); ?></label>
                    </th>
                    <td>
                        <input type="file" id="bf_re_emb_csv" name="bf_re_emb_csv" accept=".csv,text/csv" />
                    </td>
                </tr>
            </table>

            <?php submit_button(
                __( 'Import CSV (truncate & reload)', 'bf-wp-related-embeddings-db' ),
                'primary',
                'bf_re_emb_import_submit'
            ); ?>
        </form>

        <div class="card">
            <h2><?php esc_html_e( 'Troubleshooting', 'bf-wp-related-embeddings-db' ); ?></h2>
            <ul>
                <li><?php esc_html_e( 'Check Docker container logs for debugging output (look for [bf_wp_related_embeddings_db] prefix)', 'bf-wp-related-embeddings-db' ); ?></li>
                <li><?php esc_html_e( 'Enable WP_DEBUG in wp-config.php to see detailed error messages', 'bf-wp-related-embeddings-db' ); ?></li>
                <li><?php esc_html_e( 'Verify CSV file encoding is UTF-8', 'bf-wp-related-embeddings-db' ); ?></li>
                <li><?php esc_html_e( 'Check phpMyAdmin to verify table structure and data', 'bf-wp-related-embeddings-db' ); ?></li>
            </ul>
        </div>
    </div>
    <?php
}
