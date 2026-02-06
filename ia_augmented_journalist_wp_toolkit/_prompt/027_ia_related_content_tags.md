As Wordpress expert:

The main objective is I want an all-in-one plugin for my semantic clustreing strategy for SEO, easy to maintain and to update both with CSV or manually.

Note : use best practices to create WP plugin, uninstall procedure, DRY principles, keep comments for  all functions and helpers or make new comment for all functions and helpers if needed

1. Can you put the code from the file `functions_specific.php` inside a plugin.
2. Keep the debug function from the file `functions functions_specific.php`made but enable to turn on or to turn off the debug function from the plugin settings do I can debug easily.
3. Grab the logic and function from each plugin: `bf_wp_related_embeddings_db.php`, `bf_wp_tag_families_db.php` so I can still update with csv files and consolidate into a unique plugin, leverage on the tables, keep the comment and so on.
4. For `bf_wp_tag_families_db.php`, I want to be able to declare manually that this tag is a family tag then I will be able to manually add tags related to this family, use the id tag and create an add button. So, for the families tag that is used for semantic clustering, I will be able to correct
4. Add a help page so I have an operation mode to install, uninstall, link also with the functions in the two related plugins, it will help to keep track of the update, version and so on….


- bf_wp_related_embeddings_db.php
```php
<?php
/**
 * Plugin Name: BF Related Posts via Embeddings (DB)
 * Description: Manage related posts with CSV import or manual selection + shortcode display
 * Version: 1.0.0
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

    // Check if custom selection is active
    $custom_order = get_post_meta( $post_id, '_bf_custom_related_order', true );
    
    if ( ! empty( $custom_order ) && is_array( $custom_order ) ) {
        // Use custom selection order
        $out = array();
        $rank = 1;
        
        foreach ( $custom_order as $related_id ) {
            // Get similarity from database if exists
            $similarity_sql = $wpdb->prepare(
                "SELECT similarity FROM `{$table_name}` WHERE post_id = %d AND related_post_id = %d LIMIT 1",
                $post_id,
                $related_id
            );
            $similarity = $wpdb->get_var( $similarity_sql );
            
            $out[] = array(
                'related_post_id' => (int) $related_id,
                'similarity'      => $similarity ? (float) $similarity : 1.0,
                'rank'            => $rank++,
            );
            
            if ( $rank > $limit ) {
                break;
            }
        }
        
        return $out;
    }

    // Default: Get from database
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

    global $wpdb;
    $table_name = bf_re_emb_table_name();
    
    // Check if full reset was triggered
    if ( isset( $_POST['bf_full_reset'] ) && $_POST['bf_full_reset'] === '1' ) {
        // Delete custom selection meta only - database stays intact
        delete_post_meta( $post_id, '_bf_custom_related_selection' );
        delete_post_meta( $post_id, '_bf_custom_mode_active' );
        delete_post_meta( $post_id, '_bf_custom_related_order' );
        return;
    }
    
    // Check if custom selection mode
    $is_custom = isset( $_POST['bf_custom_selection'] ) && $_POST['bf_custom_selection'] === '1';
    
    if ( $is_custom ) {
        // Custom mode: Save selection in post meta, DON'T modify database
        $selected_ids = isset( $_POST['bf_selected_ids'] ) ? json_decode( stripslashes( $_POST['bf_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );
        
        // Get ordered IDs
        $ordered_ids = isset( $_POST['bf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );
        
        // Filter ordered_ids to only include selected ones
        $ordered_selected = array_values( array_intersect( $ordered_ids, $selected_ids ) );
        
        update_post_meta( $post_id, '_bf_custom_related_selection', $selected_ids );
        update_post_meta( $post_id, '_bf_custom_related_order', $ordered_selected );
        update_post_meta( $post_id, '_bf_custom_mode_active', '1' );
        
        // DON'T modify database - preserve original CSV data
        
    } else {
        // Default mode: Save order to database
        delete_post_meta( $post_id, '_bf_custom_related_selection' );
        delete_post_meta( $post_id, '_bf_custom_mode_active' );
        delete_post_meta( $post_id, '_bf_custom_related_order' );
        
        // Get ordered IDs
        $ordered_ids = isset( $_POST['bf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );
        
        // Delete existing
        $wpdb->delete( $table_name, array( 'post_id' => $post_id ), array( '%d' ) );
        
        // Add all in new order
        $rank = 1;
        foreach ( $ordered_ids as $related_id ) {
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
    $custom_mode_active = get_post_meta( $post_id, '_bf_custom_mode_active', true );
    $is_custom = ! empty( $custom_selection ) || $custom_mode_active === '1';
    $selected_ids = ! empty( $custom_selection ) ? $custom_selection : array();
    
    ?>
    <div id="bf-related-posts-wrap">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="margin: 0;">
                <input type="checkbox" id="bf-custom-selection" name="bf_custom_selection" value="1" <?php checked( $is_custom ); ?>>
                <strong>Custom selection</strong>
            </label>
            <?php if ( $is_custom ) : ?>
            <button type="button" id="bf-reset-selection" class="button button-small" style="padding: 2px 8px; height: auto;">Reset</button>
            <?php endif; ?>
        </div>
        
        <div id="bf-custom-mode-help" style="display: <?php echo $is_custom ? 'block' : 'none'; ?>; padding: 8px; background: #fff3cd; border-left: 3px solid #ffc107; margin-bottom: 10px; font-size: 12px;">
            Click to select/deselect. Drag to reorder. Selected posts = green.
        </div>
        
        <div id="bf-default-mode-help" style="display: <?php echo $is_custom ? 'none' : 'block'; ?>; padding: 8px; background: #d1ecf1; border-left: 3px solid #0c5460; margin-bottom: 10px; font-size: 12px;">
            All posts shown. Drag to reorder.
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
                    style="padding: 8px; margin: 3px 0; background: <?php echo $bg_color; ?>; cursor: move; border-left: 3px solid <?php echo $border_color; ?>; transition: all 0.2s;">
                    <span class="dashicons dashicons-menu" style="color: #999; margin-right: 5px;"></span>
                    <strong>#<?php echo $rel_post->ID; ?></strong> — <?php echo esc_html( get_the_title( $rel_post ) ); ?>
                    <span class="bf-check-icon" style="float: right; display: <?php echo $is_selected ? 'inline' : 'none'; ?>;">✓</span>
                </li>
                <?php endforeach; ?>
            <?php else : ?>
                <li style="padding: 8px; color: #666; font-style: italic;">No related posts. Import CSV or add below.</li>
            <?php endif; ?>
        </ul>
        
        <input type="hidden" id="bf-selected-ids" name="bf_selected_ids" value="<?php echo esc_attr( json_encode( $selected_ids ) ); ?>">
        <input type="hidden" id="bf-ordered-ids" name="bf_ordered_ids" value="">
        
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">
            <p style="margin-top: 0;"><strong>Add more posts:</strong></p>
            <input type="text" id="bf-post-search" placeholder="Search by ID or title..." style="width: 100%;">
            <div id="bf-search-results" style="max-height: 200px; overflow-y: auto; border: 1px solid #ddd; display: none; background: white; margin-top: 5px;"></div>
        </div>
    </div>
    
    <script>
    jQuery(document).ready(function($) {
        var isCustomMode = $('#bf-custom-selection').is(':checked');
        
        // Make list sortable
        $('#bf-related-posts-list').sortable({
            placeholder: 'ui-state-highlight',
            handle: '.dashicons-menu',
            update: function() {
                updateOrderedIds();
            }
        });
        
        function updateOrderedIds() {
            var orderedIds = [];
            $('.bf-related-item').each(function() {
                orderedIds.push($(this).data('id'));
            });
            $('#bf-ordered-ids').val(JSON.stringify(orderedIds));
        }
        
        // Initial order
        updateOrderedIds();
        
        // Toggle custom selection mode
        $('#bf-custom-selection').on('change', function() {
            isCustomMode = $(this).is(':checked');
            
            if (isCustomMode) {
                $('#bf-custom-mode-help').show();
                $('#bf-default-mode-help').hide();
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
        
        // Reset button
        $(document).on('click', '#bf-reset-selection', function() {
            if (confirm('Reset to default? This will remove custom selection and show all posts from CSV/database.')) {
                // Add hidden input to trigger full reset on save
                $('<input>').attr({
                    type: 'hidden',
                    name: 'bf_full_reset',
                    value: '1'
                }).appendTo('#post');
                
                // Save to trigger reset
                $('#publish, #save-post').click();
            }
        });
        
        // Click to select/deselect
        $(document).on('click', '.bf-related-item', function(e) {
            if (!isCustomMode) return;
            if ($(e.target).hasClass('dashicons-menu')) return; // Allow dragging
            
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
            updateOrderedIds();
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
            
            var html = '<li class="bf-related-item ' + (isSelected ? 'selected' : '') + '" data-id="' + postId + '" style="padding: 8px; margin: 3px 0; background: ' + bgColor + '; cursor: move; border-left: 3px solid ' + borderColor + '; transition: all 0.2s;">';
            html += '<span class="dashicons dashicons-menu" style="color: #999; margin-right: 5px;"></span>';
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
            
            updateOrderedIds();
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
            
            <h3>Shortcode</h3>
            <p><code>[bf_related_posts]</code></p>
            <p><strong>Parameters:</strong> <code>post_id</code>, <code>limit</code>, <code>title</code></p>
            <p><strong>Example:</strong></p>
            <pre style="background: #f5f5f5; padding: 10px; border: 1px solid #ddd; overflow-x: auto;">[bf_related_posts limit="3" title="You May Also Like"]</pre>
            
            <h3>Template Function</h3>
            <pre style="background: #f5f5f5; padding: 15px; border: 1px solid #ddd; overflow-x: auto; font-family: monospace; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">$related = bf_get_related_posts( $post_id, $limit );
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
    
    wp_enqueue_script( 'jquery-ui-sortable' );
}
add_action( 'admin_enqueue_scripts', 'bf_re_emb_enqueue_scripts' );

```
- bf_wp_tag_families_db.php
```php
<?php
/**
 * Plugin Name: BF Tag Families via Embeddings (DB)
 * Description: Manage semantic tag families with CSV import or manual selection + shortcode display
 * Version: 1.0.0
 * Author: Your Name
 * Text Domain: bf-wp-tag-families-db
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function bf_tf_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'tag_families';
}

/**
 * ACTIVATION: create table once
 */
function bf_tf_activate() {
    global $wpdb;

    $table_name      = bf_tf_table_name();
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE `{$table_name}` (
        id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        family_id INT(11) NOT NULL,
        canonical_tag_id BIGINT(20) UNSIGNED NOT NULL,
        canonical_label VARCHAR(255) NOT NULL,
        tag_id BIGINT(20) UNSIGNED NOT NULL,
        tag_label VARCHAR(255) NOT NULL,
        similarity_to_canonical DOUBLE NOT NULL,
        usage_count INT(11) NOT NULL,
        entity_label VARCHAR(50) NOT NULL,
        PRIMARY KEY  (id),
        UNIQUE KEY family_tag (family_id, tag_id),
        KEY tag_id (tag_id),
        KEY family_id (family_id),
        KEY canonical_tag_id (canonical_tag_id)
    ) {$charset_collate};";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );

    set_transient( 'bf_tf_activation_notice', true, 30 );
}
register_activation_hook( __FILE__, 'bf_tf_activate' );

/**
 * UNINSTALL: Clean up on plugin deletion
 */
function bf_tf_uninstall() {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'tag_families';
    
    // Drop the table
    $wpdb->query( "DROP TABLE IF EXISTS `{$table_name}`" );
    
    // Delete options
    delete_option( 'bf_tf_table_created' );
    delete_option( 'bf_tf_creation_method' );
    
    // Delete all custom selection term meta
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_selection'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_mode_active'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_order'" );
}
register_uninstall_hook( __FILE__, 'bf_tf_uninstall' );

function bf_tf_activation_notice() {
    if ( get_transient( 'bf_tf_activation_notice' ) ) {
        delete_transient( 'bf_tf_activation_notice' );
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p><strong>BF Tag Families:</strong> Plugin activated. Go to Settings → Tag Families to import CSV.</p>';
        echo '</div>';
    }
}
add_action( 'admin_notices', 'bf_tf_activation_notice' );

/**
 * Get tag family members
 */
function bf_tf_get_family_members( $tag_id, $limit = 20 ) {
    global $wpdb;
    $table_name = bf_tf_table_name();

    // Check if custom selection is active
    $custom_order = get_term_meta( $tag_id, '_bf_custom_family_order', true );
    
    if ( ! empty( $custom_order ) && is_array( $custom_order ) ) {
        // Use custom selection order
        $out = array();
        $rank = 1;
        
        foreach ( $custom_order as $related_tag_id ) {
            // Get data from database
            $sql = $wpdb->prepare(
                "SELECT tag_id, tag_label, canonical_tag_id, canonical_label, similarity_to_canonical, usage_count, entity_label, family_id
                 FROM `{$table_name}`
                 WHERE tag_id IN (SELECT tag_id FROM `{$table_name}` WHERE tag_id = %d)
                 AND tag_id = %d
                 LIMIT 1",
                $tag_id,
                $related_tag_id
            );
            $row = $wpdb->get_row( $sql, ARRAY_A );
            
            if ( $row ) {
                $out[] = array(
                    'tag_id'                  => (int) $row['tag_id'],
                    'tag_label'               => $row['tag_label'],
                    'canonical_tag_id'        => (int) $row['canonical_tag_id'],
                    'canonical_label'         => $row['canonical_label'],
                    'similarity_to_canonical' => (float) $row['similarity_to_canonical'],
                    'usage_count'             => (int) $row['usage_count'],
                    'entity_label'            => $row['entity_label'],
                    'family_id'               => (int) $row['family_id'],
                    'rank'                    => $rank++,
                );
            }
            
            if ( $rank > $limit ) {
                break;
            }
        }
        
        return $out;
    }

    // Default: Get all family members
    $sql = $wpdb->prepare(
        "SELECT tag_id, tag_label, canonical_tag_id, canonical_label, similarity_to_canonical, usage_count, entity_label, family_id
         FROM `{$table_name}`
         WHERE family_id = (SELECT family_id FROM `{$table_name}` WHERE tag_id = %d LIMIT 1)
         AND tag_id != %d
         ORDER BY similarity_to_canonical DESC
         LIMIT %d",
        $tag_id,
        $tag_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );

    $out = array();
    $rank = 1;
    if ( $rows ) {
        foreach ( $rows as $row ) {
            $out[] = array(
                'tag_id'                  => (int) $row['tag_id'],
                'tag_label'               => $row['tag_label'],
                'canonical_tag_id'        => (int) $row['canonical_tag_id'],
                'canonical_label'         => $row['canonical_label'],
                'similarity_to_canonical' => (float) $row['similarity_to_canonical'],
                'usage_count'             => (int) $row['usage_count'],
                'entity_label'            => $row['entity_label'],
                'family_id'               => (int) $row['family_id'],
                'rank'                    => $rank++,
            );
        }
    }

    return $out;
}

/**
 * Save tag family members from meta box
 */
function bf_tf_save_meta_box( $term_id ) {
    if ( ! isset( $_POST['bf_tf_nonce'] ) || ! wp_verify_nonce( $_POST['bf_tf_nonce'], 'bf_tf_save' ) ) {
        return;
    }

    if ( ! current_user_can( 'manage_categories' ) ) {
        return;
    }

    // Check if full reset was triggered
    if ( isset( $_POST['bf_tf_full_reset'] ) && $_POST['bf_tf_full_reset'] === '1' ) {
        delete_term_meta( $term_id, '_bf_custom_family_selection' );
        delete_term_meta( $term_id, '_bf_custom_mode_active' );
        delete_term_meta( $term_id, '_bf_custom_family_order' );
        return;
    }
    
    // Check if custom selection mode
    $is_custom = isset( $_POST['bf_tf_custom_selection'] ) && $_POST['bf_tf_custom_selection'] === '1';
    
    if ( $is_custom ) {
        // Custom mode: Save selection in term meta
        $selected_ids = isset( $_POST['bf_tf_selected_ids'] ) ? json_decode( stripslashes( $_POST['bf_tf_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );
        
        // Get ordered IDs
        $ordered_ids = isset( $_POST['bf_tf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_tf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );
        
        // Filter ordered_ids to only include selected ones
        $ordered_selected = array_values( array_intersect( $ordered_ids, $selected_ids ) );
        
        update_term_meta( $term_id, '_bf_custom_family_selection', $selected_ids );
        update_term_meta( $term_id, '_bf_custom_family_order', $ordered_selected );
        update_term_meta( $term_id, '_bf_custom_mode_active', '1' );
        
    } else {
        // Default mode
        delete_term_meta( $term_id, '_bf_custom_family_selection' );
        delete_term_meta( $term_id, '_bf_custom_mode_active' );
        delete_term_meta( $term_id, '_bf_custom_family_order' );
    }
}
add_action( 'edited_post_tag', 'bf_tf_save_meta_box', 10, 1 );
add_action( 'create_post_tag', 'bf_tf_save_meta_box', 10, 1 );

/**
 * Redirect back to term edit page after save (instead of term list)
 */
function bf_tf_redirect_after_save( $location, $term_id ) {
    if ( isset( $_POST['bf_tf_nonce'] ) && wp_verify_nonce( $_POST['bf_tf_nonce'], 'bf_tf_save' ) ) {
        $taxonomy = isset( $_POST['taxonomy'] ) ? $_POST['taxonomy'] : 'post_tag';
        
        // Redirect back to edit page to show updated state
        $location = add_query_arg( array(
            'taxonomy' => $taxonomy,
            'tag_ID' => $term_id,
            'post_type' => 'post',
        ), admin_url( 'term.php' ) );
    }
    
    return $location;
}
add_filter( 'edit_term_redirect', 'bf_tf_redirect_after_save', 10, 2 );

/**
 * Meta box: manage tag family
 */
function bf_tf_render_meta_box( $term ) {
    wp_nonce_field( 'bf_tf_save', 'bf_tf_nonce' );
    
    $term_id = $term->term_id;
    $family_members = bf_tf_get_family_members( $term_id, 100 );
    
    // Get canonical info
    global $wpdb;
    $table_name = bf_tf_table_name();
    $canonical_info = $wpdb->get_row( $wpdb->prepare(
        "SELECT family_id, canonical_tag_id, canonical_label FROM `{$table_name}` WHERE tag_id = %d LIMIT 1",
        $term_id
    ), ARRAY_A );
    
    // Get custom selection if exists
    $custom_selection = get_term_meta( $term_id, '_bf_custom_family_selection', true );
    $custom_mode_active = get_term_meta( $term_id, '_bf_custom_mode_active', true );
    $is_custom = ! empty( $custom_selection ) || $custom_mode_active === '1';
    $selected_ids = ! empty( $custom_selection ) ? $custom_selection : array();
    
    ?>
    <tr class="form-field">
        <th scope="row"><label>Tag Family (Embeddings)</label></th>
        <td>
            <?php if ( $canonical_info ) : ?>
                <div style="background: #f0f6fc; padding: 10px; border-left: 3px solid #0073aa; margin-bottom: 15px;">
                    <p style="margin: 0;"><strong>Family ID:</strong> <?php echo esc_html( $canonical_info['family_id'] ); ?></p>
                    <p style="margin: 5px 0 0 0;"><strong>Canonical Tag:</strong> 
                        <?php if ( $canonical_info['canonical_tag_id'] == $term_id ) : ?>
                            <span style="color: #0073aa; font-weight: bold;">★ This tag (canonical)</span>
                        <?php else : ?>
                            #<?php echo esc_html( $canonical_info['canonical_tag_id'] ); ?> — <?php echo esc_html( $canonical_info['canonical_label'] ); ?>
                        <?php endif; ?>
                    </p>
                </div>
            <?php endif; ?>
            
            <div id="bf-tf-wrap">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <label style="margin: 0;">
                        <input type="checkbox" id="bf-tf-custom-selection" name="bf_tf_custom_selection" value="1" <?php checked( $is_custom ); ?>>
                        <strong>Custom selection</strong>
                    </label>
                    <?php if ( $is_custom ) : ?>
                    <button type="button" id="bf-tf-reset-selection" class="button button-small">Reset</button>
                    <?php endif; ?>
                </div>
                
                <div id="bf-tf-custom-mode-help" style="display: <?php echo $is_custom ? 'block' : 'none'; ?>; padding: 8px; background: #fff3cd; border-left: 3px solid #ffc107; margin-bottom: 10px; font-size: 12px;">
                    Click to select/deselect. Drag to reorder. Selected = green.
                </div>
                
                <div id="bf-tf-default-mode-help" style="display: <?php echo $is_custom ? 'none' : 'block'; ?>; padding: 8px; background: #d1ecf1; border-left: 3px solid #0c5460; margin-bottom: 10px; font-size: 12px;">
                    All family members shown. Drag to reorder.
                </div>
                
                <ul id="bf-tf-list" style="list-style: none; padding: 0; margin: 0 0 10px 0;">
                    <?php if ( ! empty( $family_members ) ) : ?>
                        <?php foreach ( $family_members as $member ) : 
                            $is_selected = in_array( $member['tag_id'], $selected_ids );
                            $bg_color = $is_selected ? '#d4edda' : '#f0f0f0';
                            $border_color = $is_selected ? '#28a745' : '#2271b1';
                        ?>
                        <li class="bf-tf-item <?php echo $is_selected ? 'selected' : ''; ?>" 
                            data-id="<?php echo esc_attr( $member['tag_id'] ); ?>"
                            style="padding: 8px; margin: 3px 0; background: <?php echo $bg_color; ?>; cursor: move; border-left: 3px solid <?php echo $border_color; ?>; transition: all 0.2s;">
                            <span class="dashicons dashicons-menu" style="color: #999; margin-right: 5px;"></span>
                            <strong>#<?php echo $member['tag_id']; ?></strong> — <?php echo esc_html( $member['tag_label'] ); ?>
                            <span style="color: #666; font-size: 11px; margin-left: 10px;">
                                Sim: <?php echo number_format( $member['similarity_to_canonical'], 3 ); ?> | 
                                Uses: <?php echo $member['usage_count']; ?> | 
                                <?php echo esc_html( $member['entity_label'] ); ?>
                            </span>
                            <span class="bf-tf-check-icon" style="float: right; display: <?php echo $is_selected ? 'inline' : 'none'; ?>;">✓</span>
                        </li>
                        <?php endforeach; ?>
                    <?php else : ?>
                        <li style="padding: 8px; color: #666; font-style: italic;">No family members. Import CSV first.</li>
                    <?php endif; ?>
                </ul>
                
                <input type="hidden" id="bf-tf-selected-ids" name="bf_tf_selected_ids" value="<?php echo esc_attr( json_encode( $selected_ids ) ); ?>">
                <input type="hidden" id="bf-tf-ordered-ids" name="bf_tf_ordered_ids" value="">
            </div>
            
            <script>
            jQuery(document).ready(function($) {
                var isCustomMode = $('#bf-tf-custom-selection').is(':checked');
                
                $('#bf-tf-list').sortable({
                    placeholder: 'ui-state-highlight',
                    handle: '.dashicons-menu',
                    update: function() {
                        updateOrderedIds();
                    }
                });
                
                function updateOrderedIds() {
                    var orderedIds = [];
                    $('.bf-tf-item').each(function() {
                        orderedIds.push($(this).data('id'));
                    });
                    $('#bf-tf-ordered-ids').val(JSON.stringify(orderedIds));
                }
                
                updateOrderedIds();
                
                $('#bf-tf-custom-selection').on('change', function() {
                    isCustomMode = $(this).is(':checked');
                    
                    if (isCustomMode) {
                        $('#bf-tf-custom-mode-help').show();
                        $('#bf-tf-default-mode-help').hide();
                    } else {
                        $('#bf-tf-custom-mode-help').hide();
                        $('#bf-tf-default-mode-help').show();
                        $('.bf-tf-item').removeClass('selected')
                            .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                            .find('.bf-tf-check-icon').hide();
                        $('#bf-tf-selected-ids').val('[]');
                    }
                });
                
                $(document).on('click', '#bf-tf-reset-selection', function() {
                    if (confirm('Reset to default? This removes custom selection and shows all family members.')) {
                        var $form = $('#edittag');
                        if ($form.length === 0) {
                            $form = $('form#edittag, form[name="edittag"]').first();
                        }
                        if ($form.length === 0) {
                            $form = $(this).closest('form');
                        }
                        
                        $('<input>').attr({
                            type: 'hidden',
                            name: 'bf_tf_full_reset',
                            value: '1'
                        }).appendTo($form);
                        
                        $form.submit();
                    }
                });
                
                $(document).on('click', '.bf-tf-item', function(e) {
                    if (!isCustomMode) return;
                    if ($(e.target).hasClass('dashicons-menu')) return;
                    
                    var $item = $(this);
                    var tagId = $item.data('id');
                    var selectedIds = JSON.parse($('#bf-tf-selected-ids').val() || '[]');
                    
                    if ($item.hasClass('selected')) {
                        $item.removeClass('selected')
                            .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                            .find('.bf-tf-check-icon').hide();
                        selectedIds = selectedIds.filter(function(id) { return id !== tagId; });
                    } else {
                        $item.addClass('selected')
                            .css({'background': '#d4edda', 'border-left-color': '#28a745'})
                            .find('.bf-tf-check-icon').show();
                        selectedIds.push(tagId);
                    }
                    
                    $('#bf-tf-selected-ids').val(JSON.stringify(selectedIds));
                    updateOrderedIds();
                });
            });
            </script>
        </td>
    </tr>
    <?php
}

function bf_tf_add_meta_box( $taxonomy ) {
    if ( $taxonomy === 'post_tag' ) {
        add_action( 'post_tag_edit_form_fields', 'bf_tf_render_meta_box', 10, 1 );
    }
}
add_action( 'admin_init', function() { bf_tf_add_meta_box( 'post_tag' ); } );

/**
 * Admin menu
 */
function bf_tf_admin_menu() {
    add_options_page(
        'Tag Families',
        'Tag Families',
        'manage_options',
        'bf-wp-tag-families-db',
        'bf_tf_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_tf_admin_menu' );

/**
 * CSV import handler
 */
function bf_tf_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    if ( ! isset( $_POST['bf_tf_import_nonce'] ) || ! wp_verify_nonce( $_POST['bf_tf_import_nonce'], 'bf_tf_import_csv' ) ) {
        return;
    }

    if ( empty( $_FILES['bf_tf_csv']['tmp_name'] ) ) {
        add_settings_error( 'bf_tf_messages', 'bf_tf_no_file', 'No CSV file uploaded.', 'error' );
        return;
    }

    $tmp_name = $_FILES['bf_tf_csv']['tmp_name'];
    $handle = fopen( $tmp_name, 'r' );
    
    if ( ! $handle ) {
        add_settings_error( 'bf_tf_messages', 'bf_tf_file_open_error', 'Could not open file.', 'error' );
        return;
    }

    global $wpdb;
    $table_name = bf_tf_table_name();

    if ( isset( $_POST['bf_truncate_table'] ) && $_POST['bf_truncate_table'] === '1' ) {
        $wpdb->query( "TRUNCATE TABLE `{$table_name}`" );
    }

    // Read header
    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error( 'bf_tf_messages', 'bf_tf_bad_header', 'CSV has no header.', 'error' );
        return;
    }

    // Normalize header
    $normalized_header = array();
    foreach ( $header as $col ) {
        $col = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
        $normalized_header[] = strtolower( trim( $col ) );
    }

    $idx_family_id         = array_search( 'family_id', $normalized_header, true );
    $idx_canonical_tag_id  = array_search( 'canonical_tag_id', $normalized_header, true );
    $idx_canonical_label   = array_search( 'canonical_label', $normalized_header, true );
    $idx_tag_id            = array_search( 'tag_id', $normalized_header, true );
    $idx_tag_label         = array_search( 'tag_label', $normalized_header, true );
    $idx_similarity        = array_search( 'similarity_to_canonical', $normalized_header, true );
    $idx_usage_count       = array_search( 'usage_count', $normalized_header, true );
    $idx_entity_label      = array_search( 'entity_label', $normalized_header, true );

    if ( $idx_family_id === false || $idx_canonical_tag_id === false || $idx_tag_id === false ) {
        fclose( $handle );
        add_settings_error( 'bf_tf_messages', 'bf_tf_missing_columns', 'CSV must have: family_id, canonical_tag_id, canonical_label, tag_id, tag_label, similarity_to_canonical, usage_count, entity_label', 'error' );
        return;
    }

    $inserted = 0;

    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        if ( empty( array_filter( $row, 'strlen' ) ) ) {
            continue;
        }

        $family_id         = isset( $row[ $idx_family_id ] ) ? (int) $row[ $idx_family_id ] : 0;
        $canonical_tag_id  = isset( $row[ $idx_canonical_tag_id ] ) ? (int) $row[ $idx_canonical_tag_id ] : 0;
        $canonical_label   = isset( $row[ $idx_canonical_label ] ) ? $row[ $idx_canonical_label ] : '';
        $tag_id            = isset( $row[ $idx_tag_id ] ) ? (int) $row[ $idx_tag_id ] : 0;
        $tag_label         = isset( $row[ $idx_tag_label ] ) ? $row[ $idx_tag_label ] : '';
        $similarity_raw    = isset( $row[ $idx_similarity ] ) ? $row[ $idx_similarity ] : '0';
        $usage_count       = isset( $row[ $idx_usage_count ] ) ? (int) $row[ $idx_usage_count ] : 0;
        $entity_label      = isset( $row[ $idx_entity_label ] ) ? $row[ $idx_entity_label ] : 'O';

        $similarity = (float) str_replace( ',', '.', $similarity_raw );

        if ( $family_id < 0 || $canonical_tag_id <= 0 || $tag_id <= 0 ) {
            continue;
        }

        $result = $wpdb->replace(
            $table_name,
            array(
                'family_id'               => $family_id,
                'canonical_tag_id'        => $canonical_tag_id,
                'canonical_label'         => $canonical_label,
                'tag_id'                  => $tag_id,
                'tag_label'               => $tag_label,
                'similarity_to_canonical' => $similarity,
                'usage_count'             => $usage_count,
                'entity_label'            => $entity_label,
            ),
            array( '%d', '%d', '%s', '%d', '%s', '%f', '%d', '%s' )
        );

        if ( $result !== false ) {
            $inserted++;
        }
    }

    fclose( $handle );

    $message = sprintf( 'Imported %d tag family relationships.', $inserted );
    if ( isset( $_POST['bf_truncate_table'] ) && $_POST['bf_truncate_table'] === '1' ) {
        $message .= ' (Table truncated first)';
    }

    add_settings_error( 'bf_tf_messages', 'bf_tf_import_success', $message, 'updated' );
}

/**
 * Settings page
 */
function bf_tf_render_settings_page() {
    global $wpdb;
    
    if ( isset( $_POST['bf_tf_import_submit'] ) ) {
        bf_tf_handle_csv_import();
    }

    settings_errors( 'bf_tf_messages' );

    $table_name = bf_tf_table_name();
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    $row_count = 0;
    $family_count = 0;
    
    if ( $table_exists === $table_name ) {
        $row_count = $wpdb->get_var( "SELECT COUNT(*) FROM `{$table_name}`" );
        $family_count = $wpdb->get_var( "SELECT COUNT(DISTINCT family_id) FROM `{$table_name}`" );
    }

    ?>
    <div class="wrap">
        <h1>Tag Families via Embeddings</h1>

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
                    <td><strong>Tag Relationships:</strong></td>
                    <td><strong><?php echo number_format( $row_count ); ?></strong></td>
                </tr>
                <tr>
                    <td><strong>Tag Families:</strong></td>
                    <td><strong><?php echo number_format( $family_count ); ?></strong></td>
                </tr>
            </table>
        </div>

        <h2>CSV Import</h2>
        <p>CSV format: <code>family_id,canonical_tag_id,canonical_label,tag_id,tag_label,similarity_to_canonical,usage_count,entity_label</code></p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_tf_import_csv', 'bf_tf_import_nonce' ); ?>

            <table class="form-table">
                <tr>
                    <th><label for="bf_tf_csv">CSV File</label></th>
                    <td><input type="file" id="bf_tf_csv" name="bf_tf_csv" accept=".csv"></td>
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

            <?php submit_button( 'Import CSV', 'primary', 'bf_tf_import_submit' ); ?>
        </form>

        <div class="card">
            <h2>Usage</h2>
            
            <h3>Shortcode</h3>
            <p><code>[bf_related_tags]</code></p>
            <p><strong>Parameters:</strong> <code>tag_id</code>, <code>limit</code>, <code>title</code></p>
            <p><strong>Example:</strong></p>
            <pre style="background: #f5f5f5; padding: 10px; border: 1px solid #ddd; overflow-x: auto;">[bf_related_tags limit="5" title="Related Tags"]</pre>
            
            <h3>Template Function</h3>
            <pre style="background: #f5f5f5; padding: 15px; border: 1px solid #ddd; overflow-x: auto; font-family: monospace; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">$related = bf_get_related_tags( $tag_id, $limit );
foreach ( $related as $tag ) {
    echo '&lt;a href="' . $tag['url'] . '"&gt;' . $tag['name'] . '&lt;/a&gt;';
}</pre>
        </div>
    </div>
    <?php
}

/**
 * PUBLIC FUNCTION: Get related tags
 */
function bf_get_related_tags( $tag_id = 0, $limit = 5 ) {
    if ( ! $tag_id ) {
        $tags = get_the_tags();
        if ( $tags && ! is_wp_error( $tags ) ) {
            $tag_id = $tags[0]->term_id;
        }
    }
    
    if ( ! $tag_id ) {
        return array();
    }
    
    $family_members = bf_tf_get_family_members( $tag_id, $limit );
    
    $results = array();
    foreach ( $family_members as $member ) {
        $tag = get_tag( $member['tag_id'] );
        if ( $tag && ! is_wp_error( $tag ) ) {
            $results[] = array(
                'term_id'             => $tag->term_id,
                'name'                => $tag->name,
                'slug'                => $tag->slug,
                'url'                 => get_tag_link( $tag->term_id ),
                'count'               => $tag->count,
                'similarity'          => $member['similarity_to_canonical'],
                'usage_count'         => $member['usage_count'],
                'entity_label'        => $member['entity_label'],
                'canonical_tag_id'    => $member['canonical_tag_id'],
                'canonical_label'     => $member['canonical_label'],
            );
        }
    }
    
    return $results;
}

/**
 * SHORTCODE: [bf_related_tags]
 */
function bf_tf_shortcode( $atts ) {
    $atts = shortcode_atts( array(
        'tag_id' => 0,
        'limit'  => 5,
        'title'  => 'Related Tags',
    ), $atts );
    
    $related = bf_get_related_tags( $atts['tag_id'], $atts['limit'] );
    
    if ( empty( $related ) ) {
        return '';
    }
    
    $html = '<div class="bf-related-tags">';
    
    if ( ! empty( $atts['title'] ) ) {
        $html .= '<h3>' . esc_html( $atts['title'] ) . '</h3>';
    }
    
    $html .= '<ul>';
    
    foreach ( $related as $tag ) {
        $html .= '<li>';
        $html .= '<a href="' . esc_url( $tag['url'] ) . '">' . esc_html( $tag['name'] ) . '</a>';
        $html .= ' <span style="color: #666; font-size: 0.9em;">(' . $tag['count'] . ')</span>';
        $html .= '</li>';
    }
    
    $html .= '</ul>';
    $html .= '</div>';
    
    return $html;
}
add_shortcode( 'bf_related_tags', 'bf_tf_shortcode' );

/**
 * Enqueue scripts
 */
function bf_tf_enqueue_scripts( $hook ) {
    if ( strpos( $hook, 'term.php' ) !== false || strpos( $hook, 'edit-tags.php' ) !== false ) {
        wp_enqueue_script( 'jquery-ui-sortable' );
    }
}
add_action( 'admin_enqueue_scripts', 'bf_tf_enqueue_scripts' );

```

- `functions_specific.php`
```php
<?php

/* -----------  // For IA ----------- */


/* ===========================================================================
   BF SEMANTIC SEO FEATURES
   
   Dependencies:
   - bf_wp_related_embeddings_db plugin (provides bf_get_related_posts)
   - bf_wp_tag_families_db plugin (provides bf_get_related_tags)
   
   Features:
   - Level 1: Semantic breadcrumbs, related content footer, sidebar widget
   - Level 2: Schema.org structured data (Breadcrumbs, Article, CollectionPage)
   
   Usage:
   - Breadcrumbs: Call bf_semantic_breadcrumbs() in your template
   - Sidebar: Auto-added OR use widget OR shortcode [bf_sidebar]
   - Footer: Auto-added via 'the_content' filter
   - Schema: Auto-added via 'wp_head' action
   =========================================================================== */

/* ===========================================================================
   LEVEL 1: BASIC SEMANTIC SEO FEATURES
   =========================================================================== */

// ============================================================================
// 1. SEMANTIC BREADCRUMBS
// Shows: Home › Canonical Tag › Current Tag › Post Title
// ============================================================================

/**
 * Display semantic breadcrumbs with tag hierarchy
 * 
 * Shows hierarchical navigation using tag families:
 * - On single posts: Home > Parent Tag > Tag > Post Title
 * - On tag archives: Home > Parent Tag > Current Tag
 * 
 * @return void Echoes HTML directly
 * 
 * Usage: Add to single.php or content-single.php:
 * <?php bf_semantic_breadcrumbs(); ?>
 */
function bf_semantic_breadcrumbs() {
    // Don't show breadcrumbs on front page
    if ( is_front_page() ) {
        return;
    }
    
    // Only show on single posts and tag archives
    if ( ! is_single() && ! is_tag() ) {
        return;
    }
    
    global $wpdb;
    
    echo '<div class="entry-breadcrumb">';
    echo '<nav class="bf-breadcrumbs" aria-label="Breadcrumb">';
    echo '<span class="breadcrumb-icon">📍</span> ';
    echo '<a href="' . esc_url( home_url() ) . '">Home</a>';
    echo ' <span class="breadcrumb-separator">›</span> ';
    
    if ( is_single() ) {
        bf_breadcrumbs_single_post( $wpdb );
    } elseif ( is_tag() ) {
        bf_breadcrumbs_tag_archive( $wpdb );
    }
    
    echo '</nav>';
    echo '</div>';
}

/**
 * Helper: Generate breadcrumbs for single post
 * 
 * @param object $wpdb WordPress database object
 * @return void Echoes HTML directly
 */
function bf_breadcrumbs_single_post( $wpdb ) {
    $tags = get_the_tags();
    
    if ( $tags ) {
        $first_tag = $tags[0];
        
        // Show canonical (parent) tag if exists and is different from current tag
        $canonical_tag = bf_get_canonical_tag( $wpdb, $first_tag->term_id );
        if ( $canonical_tag && $canonical_tag->term_id != $first_tag->term_id ) {
            echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
            echo esc_html( $canonical_tag->name );
            echo '</a> <span class="breadcrumb-separator">›</span> ';
        }
        
        // Show current post's primary tag
        echo '<a href="' . esc_url( get_tag_link( $first_tag->term_id ) ) . '">';
        echo esc_html( $first_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show current post title (not linked)
    echo '<span class="breadcrumb-current">' . esc_html( get_the_title() ) . '</span>';
}

/**
 * Helper: Generate breadcrumbs for tag archive page
 * 
 * @param object $wpdb WordPress database object
 * @return void Echoes HTML directly
 */
function bf_breadcrumbs_tag_archive( $wpdb ) {
    $current_tag = get_queried_object();
    
    // Show canonical (parent) tag if exists
    $canonical_tag = bf_get_canonical_tag( $wpdb, $current_tag->term_id );
    if ( $canonical_tag && $canonical_tag->term_id != $current_tag->term_id ) {
        echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
        echo esc_html( $canonical_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show current tag (not linked)
    echo '<span class="breadcrumb-current">' . esc_html( $current_tag->name ) . '</span>';
}

/**
 * Helper: Get canonical (parent) tag for a given tag ID
 * 
 * Queries the tag_families table to find the canonical tag
 * that represents the parent topic cluster
 * 
 * @param object $wpdb WordPress database object
 * @param int $tag_id The tag ID to look up
 * @return object|null Tag object or null if not found
 */
function bf_get_canonical_tag( $wpdb, $tag_id ) {
    $canonical = $wpdb->get_row( $wpdb->prepare(
        "SELECT canonical_tag_id 
         FROM {$wpdb->prefix}tag_families 
         WHERE tag_id = %d 
         LIMIT 1",
        $tag_id
    ) );
    
    if ( $canonical && $canonical->canonical_tag_id ) {
        return get_tag( $canonical->canonical_tag_id );
    }
    
    return null;
}

// ============================================================================
// 2. SIDEBAR WIDGET (Related Posts + Tags)
// Shows both related articles and related topics in sidebar
// Multiple integration options: Widget, Shortcode, or Auto-inject
// ============================================================================

/**
 * Semantic Sidebar Widget - Core Function
 * 
 * Displays:
 * - Related posts (5 most similar articles)
 * - Related tags (5 semantically similar topics)
 * 
 * Styled with Zaatar theme colors (#4F1993)
 * 
 * @return void Echoes HTML directly
 */
/**
 * Semantic Sidebar Widget - SUPER DEBUG VERSION
 */
function bf_semantic_sidebar() {
    if ( ! is_single() ) {
        echo '<div class="semantic-sidebar-widget"><p>⚠️ Not a single post page</p></div>';
        return;
    }
    
    global $post, $wpdb;
    
    ?>
    <div class="semantic-sidebar-widget">
        
        <!-- DEBUG INFO -->
        <div style="background: #fff3cd; padding: 10px; margin-bottom: 15px; border-left: 4px solid #ffc107; font-size: 12px;">
            <strong>🔍 Debug Info:</strong><br>
            Post ID: <?php echo $post->ID; ?><br>
            bf_get_related_posts exists: <?php echo function_exists('bf_get_related_posts') ? '✅ Yes' : '❌ No'; ?><br>
            bf_get_related_tags exists: <?php echo function_exists('bf_get_related_tags') ? '✅ Yes' : '❌ No'; ?><br>
            <?php
            $tags = get_the_tags();
            echo 'Post has tags: ' . ($tags ? '✅ Yes (' . count($tags) . ')' : '❌ No') . '<br>';
            
            if ($tags) {
                echo 'First tag ID: ' . $tags[0]->term_id . ' (' . $tags[0]->name . ')<br>';
            }
            
            // Check database directly
            $db_count = $wpdb->get_var($wpdb->prepare(
                "SELECT COUNT(*) FROM {$wpdb->prefix}related_posts_embeddings WHERE post_id = %d",
                $post->ID
            ));
            echo 'Related posts in DB for this post: ' . ($db_count ? $db_count : '0') . '<br>';
            
            if ($tags) {
                $tag_db_count = $wpdb->get_var($wpdb->prepare(
                    "SELECT COUNT(*) FROM {$wpdb->prefix}tag_families WHERE tag_id = %d",
                    $tags[0]->term_id
                ));
                echo 'Tag family data in DB: ' . ($tag_db_count ? '✅ Yes' : '❌ No') . '<br>';
            }
            ?>
        </div>
        
        <!-- Related Posts Section -->
        <?php if ( function_exists( 'bf_get_related_posts' ) ) : ?>
            <?php
            $related_posts = bf_get_related_posts( $post->ID, 5 );
            
            // Debug output
            echo '<div style="background: #e7f3ff; padding: 10px; margin-bottom: 10px; font-size: 11px;">';
            echo '<strong>Related Posts Debug:</strong><br>';
            echo 'Function returned type: ' . gettype($related_posts) . '<br>';
            if (is_array($related_posts)) {
                echo 'Array count: ' . count($related_posts) . '<br>';
                if (count($related_posts) > 0) {
                    echo 'First item keys: ' . implode(', ', array_keys($related_posts[0])) . '<br>';
                }
            } else {
                echo 'Return value: ' . var_export($related_posts, true) . '<br>';
            }
            echo '</div>';
            
            if ( $related_posts && is_array($related_posts) && count($related_posts) > 0 ) :
            ?>
                <div class="related-posts-section">
                    <h3>Related Articles (<?php echo count($related_posts); ?>)</h3>
                    <ul>
                        <?php foreach ( $related_posts as $related ) : ?>
                            <li>
                                <a href="<?php echo esc_url( $related['permalink'] ); ?>">
                                    <?php echo esc_html( $related['title'] ); ?>
                                </a>
                                <small class="similarity-score">
                                    (<?php echo number_format( $related['similarity'], 2 ); ?>)
                                </small>
                            </li>
                        <?php endforeach; ?>
                    </ul>
                </div>
            <?php else: ?>
                <div style="background: #f8d7da; padding: 10px; margin-bottom: 15px; border-left: 4px solid #dc3545;">
                    ⚠️ No related posts returned from bf_get_related_posts()<br>
                    <small>Check if post ID <?php echo $post->ID; ?> exists in wp_related_posts_embeddings table</small>
                </div>
            <?php endif; ?>
        <?php endif; ?>
        
        <!-- Related Tags Section -->
        <?php if ( function_exists( 'bf_get_related_tags' ) ) : ?>
            <?php
            $tags = get_the_tags();
            
            if ( $tags && is_array($tags) && count($tags) > 0 ) {
                $first_tag_id = $tags[0]->term_id;
                $related_tags = bf_get_related_tags( $first_tag_id, 5 );
                
                // Debug output
                echo '<div style="background: #e7f3ff; padding: 10px; margin-bottom: 10px; font-size: 11px;">';
                echo '<strong>Related Tags Debug:</strong><br>';
                echo 'First tag ID: ' . $first_tag_id . ' (' . $tags[0]->name . ')<br>';
                echo 'Function returned type: ' . gettype($related_tags) . '<br>';
                if (is_array($related_tags)) {
                    echo 'Array count: ' . count($related_tags) . '<br>';
                    if (count($related_tags) > 0) {
                        echo 'First item keys: ' . implode(', ', array_keys($related_tags[0])) . '<br>';
                    }
                } else {
                    echo 'Return value: ' . var_export($related_tags, true) . '<br>';
                }
                echo '</div>';
                
                if ( $related_tags && is_array($related_tags) && count($related_tags) > 0 ) :
                ?>
                    <div class="related-tags-section">
                        <h3>Explore Topics (<?php echo count($related_tags); ?>)</h3>
                        <div class="tag-cloud">
                            <?php foreach ( $related_tags as $tag ) : ?>
                                <a href="<?php echo esc_url( $tag['url'] ); ?>" class="tag-badge">
                                    <?php echo esc_html( $tag['name'] ); ?>
                                    <small>(<?php echo intval( $tag['count'] ); ?>)</small>
                                </a>
                            <?php endforeach; ?>
                        </div>
                    </div>
                <?php else: ?>
                    <div style="background: #f8d7da; padding: 10px; margin-bottom: 15px; border-left: 4px solid #dc3545;">
                        ⚠️ No related tags returned from bf_get_related_tags()<br>
                        <small>Check if tag ID <?php echo $first_tag_id; ?> exists in wp_tag_families table</small>
                    </div>
                <?php endif;
            }
            ?>
        <?php endif; ?>
        
    </div>
    
    <!-- Styles -->
    <style>
    .semantic-sidebar-widget {
        background: linear-gradient(135deg, #f8f5fc 0%, #ffffff 100%);
        padding: 25px;
        border-left: 5px solid #4F1993;
        margin-bottom: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(79, 25, 147, 0.08);
    }
    .semantic-sidebar-widget h3 {
        margin-top: 0;
        font-size: 19px;
        color: #4F1993;
        font-weight: 700;
        border-bottom: 3px solid #4F1993;
        padding-bottom: 12px;
        margin-bottom: 18px;
    }
    .semantic-sidebar-widget ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .semantic-sidebar-widget ul li {
        padding: 10px 0;
        border-bottom: 1px solid rgba(79, 25, 147, 0.1);
    }
    .semantic-sidebar-widget ul li a {
        color: #4F1993;
        text-decoration: none;
        font-weight: 500;
        font-size: 15px;
    }
    .semantic-sidebar-widget ul li a:hover {
        color: #6d2cc4;
        text-decoration: underline;
    }
    .semantic-sidebar-widget .similarity-score {
        color: #999;
        font-size: 11px;
    }
    .tag-badge {
        display: inline-block;
        padding: 7px 14px;
        margin: 4px;
        background: white;
        border: 2px solid #4F1993;
        border-radius: 20px;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        color: #4F1993;
        transition: all 0.3s ease;
    }
    .tag-badge:hover {
        background: #4F1993;
        color: white;
    }
    </style>
    <?php
}

/**
 * Register Shortcode for Sidebar Widget
 * 
 * Usage: Add [bf_sidebar] anywhere in content or use in widgets
 */
function bf_semantic_sidebar_shortcode( $atts ) {
    ob_start();
    bf_semantic_sidebar();
    return ob_start();
}
add_shortcode( 'bf_sidebar', 'bf_semantic_sidebar_shortcode' );

/**
 * Register as WordPress Widget
 * 
 * This allows adding the widget via Appearance > Widgets
 */
class BF_Semantic_Sidebar_Widget extends WP_Widget {
    
    /**
     * Constructor
     */
    public function __construct() {
        parent::__construct(
            'bf_semantic_sidebar_widget',
            'BF Semantic Sidebar',
            array( 
                'description' => 'Shows related posts and tags using semantic AI matching'
            )
        );
    }
    
    /**
     * Front-end display of widget
     */
    public function widget( $args, $instance ) {
        echo $args['before_widget'];
        bf_semantic_sidebar();
        echo $args['after_widget'];
    }
    
    /**
     * Back-end widget form (no options needed)
     */
    public function form( $instance ) {
        echo '<p>This widget automatically shows related content on single posts.</p>';
        echo '<p>No configuration needed.</p>';
    }
}

/**
 * Register the widget
 */
function bf_register_semantic_sidebar_widget() {
    register_widget( 'BF_Semantic_Sidebar_Widget' );
}
add_action( 'widgets_init', 'bf_register_semantic_sidebar_widget' );

/**
 * OPTIONAL: Auto-inject sidebar widget
 * 
 * Automatically adds the widget to the primary sidebar on single posts
 * Uncomment this if you want automatic injection without editing sidebar.php
 */
/*
function bf_auto_inject_sidebar_widget( $sidebars_widgets ) {
    if ( is_single() && ! is_admin() ) {
        // Get the primary sidebar (adjust 'sidebar-1' to match your theme)
        $sidebar_id = 'sidebar-1'; // Common IDs: sidebar-1, primary, main-sidebar
        
        if ( isset( $sidebars_widgets[ $sidebar_id ] ) ) {
            // Add our widget at the top of the sidebar
            array_unshift( $sidebars_widgets[ $sidebar_id ], 'bf_semantic_sidebar_widget' );
        }
    }
    return $sidebars_widgets;
}
add_filter( 'sidebars_widgets', 'bf_auto_inject_sidebar_widget' );
*/

// ============================================================================
// 3. AUTO-RELATED CONTENT IN POST FOOTER
// Automatically adds related posts and tags after post content
// ============================================================================

/**
 * Auto-add related content to single post footer
 * 
 * Appends to post content:
 * - 3 related posts with thumbnails
 * - 8 related tags in a tag cloud
 * 
 * @param string $content The post content
 * @return string Modified content with related items appended
 */
function bf_auto_related_content( $content ) {
    // Only on single posts in main query
    if ( ! is_single() || ! is_main_query() ) {
        return $content;
    }
    
    // Prevent infinite loop when rendering related post excerpts
    remove_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    global $post;
    $footer = '';
    
    // Render related posts section
    if ( function_exists( 'bf_get_related_posts' ) ) {
        $related_posts = bf_get_related_posts( $post->ID, 3 );
        if ( $related_posts ) {
            $footer .= bf_render_related_posts( $related_posts );
        }
    }
    
    // Render related tags section
    if ( function_exists( 'bf_get_related_tags' ) ) {
        $tags = get_the_tags();
        if ( $tags ) {
            $related_tags = bf_get_related_tags( $tags[0]->term_id, 8 );
            if ( $related_tags ) {
                $footer .= bf_render_related_tags( $related_tags );
            }
        }
    }
    
    // Restore filter for next post
    add_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    // Wrap footer content if we have any
    if ( $footer ) {
        $footer = '<div class="bf-post-footer" style="margin-top: 50px; padding-top: 30px; border-top: 2px solid #eee;">' 
                . $footer 
                . '</div>';
    }
    
    return $content . $footer;
}
add_filter( 'the_content', 'bf_auto_related_content', 999 );

/**
 * Helper: Render related posts HTML
 * 
 * Creates a responsive grid of related post cards with:
 * - Featured image (if available)
 * - Post title
 * - Excerpt (trimmed to 15 words)
 * 
 * @param array $related_posts Array of related post data from plugin
 * @return string HTML markup for related posts grid
 */
function bf_render_related_posts( $related_posts ) {
    $html = '<h3 style="font-size: 24px; margin-bottom: 20px; color: #333;">Continue Reading</h3>';
    $html .= '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">';
    
    foreach ( $related_posts as $related ) {
        $html .= '<div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; transition: transform 0.2s;">';
        
        // Featured image (if exists)
        if ( ! empty( $related['thumbnail'] ) ) {
            $html .= '<a href="' . esc_url( $related['permalink'] ) . '">';
            $html .= '<img src="' . esc_url( $related['thumbnail'] ) . '" ';
            $html .= 'style="width: 100%; height: 180px; object-fit: cover;" ';
            $html .= 'alt="' . esc_attr( $related['title'] ) . '">';
            $html .= '</a>';
        }
        
        // Post title and excerpt
        $html .= '<div style="padding: 20px;">';
        $html .= '<h4 style="font-size: 18px; margin: 0 0 10px 0; line-height: 1.4;">';
        $html .= '<a href="' . esc_url( $related['permalink'] ) . '" style="text-decoration: none; color: #333;">';
        $html .= esc_html( $related['title'] );
        $html .= '</a></h4>';
        $html .= '<p style="font-size: 14px; color: #666; margin: 0;">';
        $html .= esc_html( wp_trim_words( $related['excerpt'], 15 ) );
        $html .= '</p>';
        $html .= '</div>';
        
        $html .= '</div>';
    }
    
    $html .= '</div>';
    return $html;
}

/**
 * Helper: Render related tags HTML
 * 
 * Creates a tag cloud of semantically related topics
 * Shows tag name and post count for each tag
 * 
 * @param array $related_tags Array of related tag data from plugin
 * @return string HTML markup for related tags section
 */
function bf_render_related_tags( $related_tags ) {
    $html = '<div style="background: #f9f9f9; padding: 20px; border-radius: 8px;">';
    $html .= '<h4 style="font-size: 16px; color: #666; margin: 0 0 15px 0;">Explore Related Topics</h4>';
    
    foreach ( $related_tags as $tag ) {
        $html .= '<a href="' . esc_url( $tag['url'] ) . '" ';
        $html .= 'style="display: inline-block; padding: 8px 15px; margin: 5px 5px 5px 0; ';
        $html .= 'background: white; border: 1px solid #ddd; border-radius: 4px; ';
        $html .= 'text-decoration: none; font-size: 14px; color: #0073aa; transition: all 0.2s;">';
        $html .= esc_html( $tag['name'] );
        $html .= ' <small style="color: #999;">(' . intval( $tag['count'] ) . ')</small>';
        $html .= '</a>';
    }
    
    $html .= '</div>';
    return $html;
}

/* ===========================================================================
   LEVEL 2: STRUCTURED DATA (Schema.org JSON-LD)
   Adds rich snippets for better Google search appearance
   =========================================================================== */

// ============================================================================
// 4. BREADCRUMB SCHEMA (Rich Snippets in Google)
// Makes breadcrumbs appear in search results
// ============================================================================

/**
 * Schema.org BreadcrumbList for Google Rich Snippets
 * 
 * Adds JSON-LD structured data to show breadcrumb trail in Google search results.
 * Uses semantic tag families to build hierarchical navigation.
 * 
 * @return void Echoes JSON-LD script tag in <head>
 */
function bf_breadcrumb_schema() {
    // Only add schema on single posts and tag archives
    if ( ! is_single() && ! is_tag() ) {
        return;
    }
    
    $items = array();
    $position = 1;
    
    // Always start with Home
    $items[] = array(
        '@type' => 'ListItem',
        'position' => $position++,
        'name' => 'Home',
        'item' => home_url()
    );
    
    if ( is_single() ) {
        global $post, $wpdb;
        
        $tags = get_the_tags();
        if ( $tags ) {
            $first_tag = $tags[0];
            
            // Get canonical (parent) tag from tag families table
            $canonical = $wpdb->get_row( $wpdb->prepare(
                "SELECT canonical_tag_id, canonical_label 
                 FROM {$wpdb->prefix}tag_families 
                 WHERE tag_id = %d 
                 LIMIT 1",
                $first_tag->term_id
            ) );
            
            // Add canonical tag to breadcrumb if it's different from current tag
            if ( $canonical && $canonical->canonical_tag_id != $first_tag->term_id ) {
                $canonical_tag = get_tag( $canonical->canonical_tag_id );
                if ( $canonical_tag ) {
                    $items[] = array(
                        '@type' => 'ListItem',
                        'position' => $position++,
                        'name' => $canonical_tag->name,
                        'item' => get_tag_link( $canonical_tag->term_id )
                    );
                }
            }
            
            // Add current post's primary tag
            $items[] = array(
                '@type' => 'ListItem',
                'position' => $position++,
                'name' => $first_tag->name,
                'item' => get_tag_link( $first_tag->term_id )
            );
        }
        
        // Add current post (last item has no 'item' property per schema.org spec)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => get_the_title()
        );
        
    } elseif ( is_tag() ) {
        global $wpdb;
        $current_tag = get_queried_object();
        
        // Get canonical (parent) tag
        $canonical = $wpdb->get_row( $wpdb->prepare(
            "SELECT canonical_tag_id, canonical_label 
             FROM {$wpdb->prefix}tag_families 
             WHERE tag_id = %d 
             LIMIT 1",
            $current_tag->term_id
        ) );
        
        // Add canonical tag if this is a child tag
        if ( $canonical && $canonical->canonical_tag_id != $current_tag->term_id ) {
            $canonical_tag = get_tag( $canonical->canonical_tag_id );
            if ( $canonical_tag ) {
                $items[] = array(
                    '@type' => 'ListItem',
                    'position' => $position++,
                    'name' => $canonical_tag->name,
                    'item' => get_tag_link( $canonical_tag->term_id )
                );
            }
        }
        
        // Add current tag (last item has no 'item' property)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => $current_tag->name
        );
    }
    
    // Build complete schema
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'BreadcrumbList',
        'itemListElement' => $items
    );
    
    // Output JSON-LD script in <head>
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_breadcrumb_schema' );

// ============================================================================
// 5. TAG ARCHIVE SCHEMA (CollectionPage for Topic Clusters)
// Helps Google understand topic cluster pages
// ============================================================================

/**
 * CollectionPage Schema for Tag Archives
 * 
 * Adds structured data to tag archive pages showing:
 * - Parent topic relationship
 * - Related tag pages
 * 
 * This helps Google understand your topic cluster structure.
 * 
 * @return void Echoes JSON-LD script tag in <head>
 */
function bf_tag_archive_schema() {
    // Only add on tag archive pages
    if ( ! is_tag() ) {
        return;
    }
    
    $current_tag = get_queried_object();
    global $wpdb;
    
    // Get tag family information
    $canonical = $wpdb->get_row( $wpdb->prepare(
        "SELECT canonical_tag_id, canonical_label 
         FROM {$wpdb->prefix}tag_families 
         WHERE tag_id = %d 
         LIMIT 1",
        $current_tag->term_id
    ) );
    
    // Get semantically related tags (limit to 8 for performance)
    $related_tags = array();
    if ( function_exists( 'bf_get_related_tags' ) ) {
        $related_tags_data = bf_get_related_tags( $current_tag->term_id, 8 );
        if ( $related_tags_data ) {
            foreach ( $related_tags_data as $tag ) {
                $related_tags[] = $tag['url'];
            }
        }
    }
    
    // Build base schema
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'CollectionPage',
        'name' => $current_tag->name . ' - ' . get_bloginfo( 'name' ),
        'description' => $current_tag->description ?: 'Articles about ' . $current_tag->name,
        'url' => get_tag_link( $current_tag->term_id )
    );
    
    // Add parent topic if this is a subtopic (not the canonical tag itself)
    if ( $canonical && $canonical->canonical_tag_id != $current_tag->term_id ) {
        $canonical_tag = get_tag( $canonical->canonical_tag_id );
        if ( $canonical_tag ) {
            $schema['isPartOf'] = array(
                '@type' => 'CollectionPage',
                'name' => $canonical_tag->name,
                'url' => get_tag_link( $canonical_tag->term_id )
            );
        }
    }
    
    // Add related tag pages
    if ( ! empty( $related_tags ) ) {
        $schema['relatedLink'] = $related_tags;
    }
    
    // Output JSON-LD script in <head>
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_tag_archive_schema', 20 );

/* ===========================================================================
   END BF SEMANTIC SEO FEATURES
   =========================================================================== */

   
/* -----------  // For IA ----------- */

?>
```
