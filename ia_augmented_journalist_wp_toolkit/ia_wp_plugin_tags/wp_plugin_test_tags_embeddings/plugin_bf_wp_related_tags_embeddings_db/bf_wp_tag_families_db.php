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
