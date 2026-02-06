<?php
/**
 * Plugin Name: BF Related Posts via Embeddings (DB)
 * Description: Manage related posts with CSV import or manual selection + shortcode display
 * Author: IA with a bit of Bruno Flaven
 * Text Domain: bf-wp-related-embeddings-db
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}

/**
 * ACTIVATION: create table once
 */
function bf_re_emb_activate() {
    global $wpdb;

    $table_name      = bf_re_emb_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE `{$table_name}` (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        post_id BIGINT(20) UNSIGNED NOT NULL,
        related_post_id BIGINT(20) UNSIGNED NOT NULL,
        similarity DOUBLE NOT NULL DEFAULT 0,
        `rank` INT(11) NOT NULL,
        PRIMARY KEY  (id),
        UNIQUE KEY post_related (post_id, related_post_id),
        KEY post_id (post_id),
        KEY related_post_id (related_post_id)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );

    set_transient( 'bf_re_emb_activation_notice', true, 30 );
}
register_activation_hook( __FILE__, 'bf_re_emb_activate' );

function bf_re_emb_activation_notice() {
    if ( get_transient( 'bf_re_emb_activation_notice' ) ) {
        delete_transient( 'bf_re_emb_activation_notice' );
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p><strong>BF Related Posts:</strong> Plugin activated. Go to Settings → Related Embeddings to import CSV or manage posts.</p>';
        echo '</div>';
    }
}
add_action( 'admin_notices', 'bf_re_emb_activation_notice' );

/**
 * Get related posts
 */
function bf_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;
    $table_name = bf_re_emb_table_name();

    $sql = $wpdb->prepare(
        "SELECT related_post_id, similarity, `rank`
         FROM `{$table_name}`
         WHERE post_id = %d
         ORDER BY `rank` ASC
         LIMIT %d",
        $post_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );

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
 * Save related posts from meta box
 */
function bf_re_emb_save_meta_box( $post_id ) {
    if ( ! isset( $_POST['bf_re_emb_nonce'] ) || ! wp_verify_nonce( $_POST['bf_re_emb_nonce'], 'bf_re_emb_save' ) ) {
        return;
    }

    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }

    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }

    // Check if custom selection mode
    $is_custom = isset( $_POST['bf_custom_selection'] ) && $_POST['bf_custom_selection'] === '1';
    
    if ( $is_custom ) {
        // Save custom selection
        $selected_ids = isset( $_POST['bf_selected_ids'] ) ? json_decode( stripslashes( $_POST['bf_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );
        
        update_post_meta( $post_id, '_bf_custom_related_selection', $selected_ids );
        
        // Update database with custom selection
        global $wpdb;
        $table_name = bf_re_emb_table_name();
        
        // Delete existing
        $wpdb->delete( $table_name, array( 'post_id' => $post_id ), array( '%d' ) );
        
        // Add selected only
        $rank = 1;
        foreach ( $selected_ids as $related_id ) {
            if ( $related_id > 0 && $related_id !== $post_id ) {
                $wpdb->insert(
                    $table_name,
                    array(
                        'post_id'         => $post_id,
                        'related_post_id' => $related_id,
                        'similarity'      => 1.0,
                        'rank'            => $rank++,
                    ),
                    array( '%d', '%d', '%f', '%d' )
                );
            }
        }
    } else {
        // Remove custom selection - use all from CSV/database
        delete_post_meta( $post_id, '_bf_custom_related_selection' );
    }
}
add_action( 'save_post', 'bf_re_emb_save_meta_box' );

/**
 * Meta box: manage related posts
 */
function bf_re_emb_render_meta_box( WP_Post $post ) {
    wp_nonce_field( 'bf_re_emb_save', 'bf_re_emb_nonce' );
    
    $post_id = $post->ID;
    $related_rows = bf_re_emb_get_related_from_db( $post_id, 100 );
    
    // Get custom selection if exists
    $custom_selection = get_post_meta( $post_id, '_bf_custom_related_selection', true );
    $is_custom = ! empty( $custom_selection );
    $selected_ids = $is_custom ? $custom_selection : array();
    
    ?>
    <div id="bf-related-posts-wrap">
        <label style="display: block; margin-bottom: 10px;">
            <input type="checkbox" id="bf-custom-selection" name="bf_custom_selection" value="1" <?php checked( $is_custom ); ?>>
            <strong>Custom selection</strong>
        </label>
        
        <div id="bf-custom-mode-help" style="display: <?php echo $is_custom ? 'block' : 'none'; ?>; padding: 8px; background: #fff3cd; border-left: 3px solid #ffc107; margin-bottom: 10px; font-size: 12px;">
            Click posts below to select/deselect. Selected posts appear green.
        </div>
        
        <div id="bf-default-mode-help" style="display: <?php echo $is_custom ? 'none' : 'block'; ?>; padding: 8px; background: #d1ecf1; border-left: 3px solid #0c5460; margin-bottom: 10px; font-size: 12px;">
            All posts from CSV/database will be shown.
        </div>
        
        <ul id="bf-related-posts-list" style="list-style: none; padding: 0; margin: 0 0 10px 0;">
            <?php if ( ! empty( $related_rows ) ) : ?>
                <?php foreach ( $related_rows as $row ) : 
                    $rel_post = get_post( $row['related_post_id'] );
                    if ( ! $rel_post ) continue;
                    
                    $is_selected = in_array( $rel_post->ID, $selected_ids );
                    $bg_color = $is_selected ? '#d4edda' : '#f0f0f0';
                    $border_color = $is_selected ? '#28a745' : '#2271b1';
                ?>
                <li class="bf-related-item <?php echo $is_selected ? 'selected' : ''; ?>" 
                    data-id="<?php echo esc_attr( $rel_post->ID ); ?>"
                    style="padding: 8px; margin: 3px 0; background: <?php echo $bg_color; ?>; cursor: pointer; border-left: 3px solid <?php echo $border_color; ?>; transition: all 0.2s;">
                    <strong>#<?php echo $rel_post->ID; ?></strong> — <?php echo esc_html( get_the_title( $rel_post ) ); ?>
                    <span class="bf-check-icon" style="float: right; display: <?php echo $is_selected ? 'inline' : 'none'; ?>;">✓</span>
                </li>
                <?php endforeach; ?>
            <?php else : ?>
                <li style="padding: 8px; color: #666; font-style: italic;">No related posts found. Import CSV or add posts manually below.</li>
            <?php endif; ?>
        </ul>
        
        <input type="hidden" id="bf-selected-ids" name="bf_selected_ids" value="<?php echo esc_attr( json_encode( $selected_ids ) ); ?>">
        
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">
            <p style="margin-top: 0;"><strong>Add more posts:</strong></p>
            <input type="text" id="bf-post-search" placeholder="Search by ID or title..." style="width: 100%;">
            <div id="bf-search-results" style="max-height: 200px; overflow-y: auto; border: 1px solid #ddd; display: none; background: white; margin-top: 5px;"></div>
        </div>
    </div>
    
    <script>
    jQuery(document).ready(function($) {
        var isCustomMode = $('#bf-custom-selection').is(':checked');
        
        // Toggle custom selection mode
        $('#bf-custom-selection').on('change', function() {
            isCustomMode = $(this).is(':checked');
            
            if (isCustomMode) {
                $('#bf-custom-mode-help').show();
                $('#bf-default-mode-help').hide();
                // Enable clicking
                $('.bf-related-item').css('cursor', 'pointer');
            } else {
                $('#bf-custom-mode-help').hide();
                $('#bf-default-mode-help').show();
                // Reset all selections
                $('.bf-related-item').removeClass('selected')
                    .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                    .find('.bf-check-icon').hide();
                $('#bf-selected-ids').val('[]');
            }
        });
        
        // Click to select/deselect
        $(document).on('click', '.bf-related-item', function() {
            if (!isCustomMode) return;
            
            var $item = $(this);
            var postId = $item.data('id');
            var selectedIds = JSON.parse($('#bf-selected-ids').val() || '[]');
            
            if ($item.hasClass('selected')) {
                // Deselect
                $item.removeClass('selected')
                    .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                    .find('.bf-check-icon').hide();
                selectedIds = selectedIds.filter(function(id) { return id !== postId; });
            } else {
                // Select
                $item.addClass('selected')
                    .css({'background': '#d4edda', 'border-left-color': '#28a745'})
                    .find('.bf-check-icon').show();
                selectedIds.push(postId);
            }
            
            $('#bf-selected-ids').val(JSON.stringify(selectedIds));
        });
        
        // Search posts
        var searchTimeout;
        $('#bf-post-search').on('keyup', function() {
            var query = $(this).val();
            if (query.length < 2) {
                $('#bf-search-results').hide();
                return;
            }
            
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                $.ajax({
                    url: ajaxurl,
                    data: {
                        action: 'bf_search_posts',
                        query: query,
                        exclude: <?php echo $post_id; ?>
                    },
                    success: function(response) {
                        if (response.success) {
                            var html = '';
                            $.each(response.data, function(i, post) {
                                html += '<div class="bf-search-result" data-id="' + post.ID + '" data-title="' + post.post_title + '" style="padding: 5px; cursor: pointer; border-bottom: 1px solid #eee;">';
                                html += '<strong>#' + post.ID + '</strong> — ' + post.post_title;
                                html += '</div>';
                            });
                            $('#bf-search-results').html(html).show();
                        }
                    }
                });
            }, 300);
        });
        
        // Add from search results
        $(document).on('click', '.bf-search-result', function() {
            var postId = $(this).data('id');
            var postTitle = $(this).data('title');
            
            // Check if already exists
            if ($('.bf-related-item[data-id="' + postId + '"]').length) {
                alert('Already in list');
                return;
            }
            
            var isSelected = isCustomMode;
            var bgColor = isSelected ? '#d4edda' : '#f0f0f0';
            var borderColor = isSelected ? '#28a745' : '#2271b1';
            var checkDisplay = isSelected ? 'inline' : 'none';
            
            var html = '<li class="bf-related-item ' + (isSelected ? 'selected' : '') + '" data-id="' + postId + '" style="padding: 8px; margin: 3px 0; background: ' + bgColor + '; cursor: pointer; border-left: 3px solid ' + borderColor + '; transition: all 0.2s;">';
            html += '<strong>#' + postId + '</strong> — ' + postTitle;
            html += '<span class="bf-check-icon" style="float: right; display: ' + checkDisplay + ';">✓</span>';
            html += '</li>';
            
            $('#bf-related-posts-list').append(html);
            
            // If custom mode, add to selected
            if (isCustomMode) {
                var selectedIds = JSON.parse($('#bf-selected-ids').val() || '[]');
                selectedIds.push(postId);
                $('#bf-selected-ids').val(JSON.stringify(selectedIds));
            }
            
            $('#bf-post-search').val('');
            $('#bf-search-results').hide();
        });
        
        // Hide results on outside click
        $(document).on('click', function(e) {
            if (!$(e.target).closest('#bf-post-search, #bf-search-results').length) {
                $('#bf-search-results').hide();
            }
        });
    });
    </script>
    <?php
}

function bf_re_emb_add_meta_box() {
    add_meta_box(
        'bf_related_embeddings_meta_box',
        'Related Posts (Embeddings)',
        'bf_re_emb_render_meta_box',
        'post',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'bf_re_emb_add_meta_box' );

/**
 * AJAX search posts
 */
function bf_re_emb_ajax_search_posts() {
    $query = sanitize_text_field( $_GET['query'] );
    $exclude = isset( $_GET['exclude'] ) ? intval( $_GET['exclude'] ) : 0;
    
    $args = array(
        'post_type'      => 'post',
        'post_status'    => 'publish',
        'posts_per_page' => 20,
        'post__not_in'   => array( $exclude ),
        's'              => $query,
    );
    
    if ( is_numeric( $query ) ) {
        $args['post__in'] = array( intval( $query ) );
        unset( $args['s'] );
    }
    
    $posts = get_posts( $args );
    
    $results = array();
    foreach ( $posts as $p ) {
        $results[] = array(
            'ID'         => $p->ID,
            'post_title' => $p->post_title,
        );
    }
    
    wp_send_json_success( $results );
}
add_action( 'wp_ajax_bf_search_posts', 'bf_re_emb_ajax_search_posts' );

/**
 * Admin menu
 */
function bf_re_emb_admin_menu() {
    add_options_page(
        'Related Embeddings',
        'Related Embeddings',
        'manage_options',
        'bf-wp-related-embeddings-db',
        'bf_re_emb_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_re_emb_admin_menu' );

/**
 * CSV import
 */
function bf_re_emb_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! isset( $_POST['bf_re_emb_import_nonce'] ) || ! wp_verify_nonce( $_POST['bf_re_emb_import_nonce'], 'bf_re_emb_import_csv' ) ) {
        return;
    }

    if ( empty( $_FILES['bf_re_emb_csv']['tmp_name'] ) ) {
        add_settings_error( 'bf_re_emb_messages', 'bf_re_emb_no_file', 'No CSV file uploaded.', 'error' );
        return;
    }

    $tmp_name = $_FILES['bf_re_emb_csv']['tmp_name'];
    $handle = fopen( $tmp_name, 'r' );
    
    if ( ! $handle ) {
        add_settings_error( 'bf_re_emb_messages', 'bf_re_emb_file_open_error', 'Could not open file.', 'error' );
        return;
    }

    global $wpdb;
    $table_name = bf_re_emb_table_name();

    if ( isset( $_POST['bf_truncate_table'] ) && $_POST['bf_truncate_table'] === '1' ) {
        $wpdb->query( "TRUNCATE TABLE `{$table_name}`" );
    }

    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error( 'bf_re_emb_messages', 'bf_re_emb_bad_header', 'CSV has no header.', 'error' );
        return;
    }

    $normalized_header = array();
    foreach ( $header as $col ) {
        $col = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
        $normalized_header[] = strtolower( trim( $col ) );
    }

    $idx_post_id         = array_search( 'post_id', $normalized_header, true );
    $idx_related_post_id = array_search( 'related_post_id', $normalized_header, true );
    $idx_similarity      = array_search( 'similarity', $normalized_header, true );
    $idx_rank            = array_search( 'rank', $normalized_header, true );

    if ( $idx_post_id === false || $idx_related_post_id === false || $idx_similarity === false || $idx_rank === false ) {
        fclose( $handle );
        add_settings_error( 'bf_re_emb_messages', 'bf_re_emb_missing_columns', 'CSV must have: post_id, related_post_id, similarity, rank', 'error' );
        return;
    }

    $inserted = 0;

    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        if ( empty( array_filter( $row, 'strlen' ) ) ) {
            continue;
        }

        $post_id         = isset( $row[ $idx_post_id ] ) ? (int) $row[ $idx_post_id ] : 0;
        $related_post_id = isset( $row[ $idx_related_post_id ] ) ? (int) $row[ $idx_related_post_id ] : 0;
        $similarity_raw  = isset( $row[ $idx_similarity ] ) ? $row[ $idx_similarity ] : '0';
        $rank            = isset( $row[ $idx_rank ] ) ? (int) $row[ $idx_rank ] : 0;

        $similarity = (float) str_replace( ',', '.', $similarity_raw );

        if ( $post_id <= 0 || $related_post_id <= 0 || $rank <= 0 ) {
            continue;
        }

        $result = $wpdb->replace(
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
        }
    }

    fclose( $handle );

    $message = sprintf( 'Imported %d rows.', $inserted );
    if ( isset( $_POST['bf_truncate_table'] ) && $_POST['bf_truncate_table'] === '1' ) {
        $message .= ' (Table truncated first)';
    }

    add_settings_error( 'bf_re_emb_messages', 'bf_re_emb_import_success', $message, 'updated' );
}

/**
 * Settings page
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
        $row_count = $wpdb->get_var( "SELECT COUNT(*) FROM `{$table_name}`" );
    }

    ?>
    <div class="wrap">
        <h1>Related Posts Embeddings</h1>

        <div class="card">
            <h2>Database Status</h2>
            <table class="widefat">
                <tr>
                    <td><strong>Table:</strong></td>
                    <td><code><?php echo esc_html( $table_name ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Status:</strong></td>
                    <td><?php echo $table_exists === $table_name ? '<span style="color: green;">✓ Exists</span>' : '<span style="color: red;">✗ Missing</span>'; ?></td>
                </tr>
                <tr>
                    <td><strong>Rows:</strong></td>
                    <td><strong><?php echo number_format( $row_count ); ?></strong></td>
                </tr>
            </table>
        </div>

        <h2>CSV Import</h2>
        <p>CSV format: <code>post_id,related_post_id,similarity,rank</code></p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_re_emb_import_csv', 'bf_re_emb_import_nonce' ); ?>

            <table class="form-table">
                <tr>
                    <th><label for="bf_re_emb_csv">CSV File</label></th>
                    <td><input type="file" id="bf_re_emb_csv" name="bf_re_emb_csv" accept=".csv"></td>
                </tr>
                <tr>
                    <th><label for="bf_truncate_table">Truncate table first?</label></th>
                    <td>
                        <label>
                            <input type="checkbox" id="bf_truncate_table" name="bf_truncate_table" value="1">
                            Delete all existing data before import
                        </label>
                    </td>
                </tr>
            </table>

            <?php submit_button( 'Import CSV', 'primary', 'bf_re_emb_import_submit' ); ?>
        </form>

        <div class="card">
            <h2>Usage</h2>
            <p><strong>Shortcode:</strong> <code>[bf_related_posts]</code></p>
            <p><strong>Parameters:</strong> <code>post_id</code>, <code>limit</code>, <code>title</code></p>
            <p><strong>Example:</strong> <code>[bf_related_posts limit="3" title="You May Also Like"]</code></p>
            <hr>
            <p><strong>Template function:</strong></p>
            <pre>$related = bf_get_related_posts( $post_id, $limit );
foreach ( $related as $post ) {
    echo '&lt;a href="' . $post['permalink'] . '"&gt;' . $post['title'] . '&lt;/a&gt;';
}</pre>
        </div>
    </div>
    <?php
}

/**
 * PUBLIC FUNCTION: Get related posts
 */
function bf_get_related_posts( $post_id = 0, $limit = 5 ) {
    if ( ! $post_id ) {
        $post_id = get_the_ID();
    }
    
    $related_rows = bf_re_emb_get_related_from_db( $post_id, $limit );
    
    $results = array();
    foreach ( $related_rows as $row ) {
        $post = get_post( $row['related_post_id'] );
        if ( $post ) {
            $results[] = array(
                'ID'         => $post->ID,
                'title'      => get_the_title( $post ),
                'permalink'  => get_permalink( $post ),
                'excerpt'    => get_the_excerpt( $post ),
                'thumbnail'  => get_the_post_thumbnail_url( $post, 'medium' ),
                'similarity' => $row['similarity'],
                'rank'       => $row['rank'],
            );
        }
    }
    
    return $results;
}

/**
 * SHORTCODE: [bf_related_posts]
 */
function bf_re_emb_shortcode( $atts ) {
    $atts = shortcode_atts( array(
        'post_id' => get_the_ID(),
        'limit'   => 5,
        'title'   => 'Related Posts',
    ), $atts );
    
    $related = bf_get_related_posts( $atts['post_id'], $atts['limit'] );
    
    if ( empty( $related ) ) {
        return '';
    }
    
    $html = '<div class="bf-related-posts">';
    
    if ( ! empty( $atts['title'] ) ) {
        $html .= '<h3>' . esc_html( $atts['title'] ) . '</h3>';
    }
    
    $html .= '<ul>';
    
    foreach ( $related as $post ) {
        $html .= '<li>';
        if ( $post['thumbnail'] ) {
            $html .= '<img src="' . esc_url( $post['thumbnail'] ) . '" alt="' . esc_attr( $post['title'] ) . '" style="max-width: 100px; height: auto; float: left; margin-right: 10px;">';
        }
        $html .= '<a href="' . esc_url( $post['permalink'] ) . '">' . esc_html( $post['title'] ) . '</a>';
        if ( $post['excerpt'] ) {
            $html .= '<p>' . esc_html( wp_trim_words( $post['excerpt'], 20 ) ) . '</p>';
        }
        $html .= '</li>';
    }
    
    $html .= '</ul>';
    $html .= '</div>';
    
    return $html;
}
add_shortcode( 'bf_related_posts', 'bf_re_emb_shortcode' );

/**
 * Enqueue scripts
 */
function bf_re_emb_enqueue_scripts( $hook ) {
    if ( 'post.php' !== $hook && 'post-new.php' !== $hook ) {
        return;
    }
    
    wp_enqueue_script( 'jquery' );
}
add_action( 'admin_enqueue_scripts', 'bf_re_emb_enqueue_scripts' );
