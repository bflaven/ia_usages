
## PROMPT_1

As a Wordpress plugin expert, the plugin Semaphore is working fine but I want manually correct some stuff on the semaphore-dashboard


1. If I select a certain tag in "Tag Families" e.g Claude AI, I want to see below the "Family Members" e.g 4 members to this family "Isabelle Fougère", "Marie-Eve Maheu", "Michelle Alliot-Marie" then I want to be able to click on one of those keywords in Family Members and then click "Detach selected member from current family" for the moment it is not working.

## PROMPT_2

Can you rewrite the all plugin based on the code below both for PHP and JS so I just have to cut and paste. Increment the version both for php and javascript.

- semaphore.php
```php
<?php
/**
 * Plugin Name: Semaphore
 * Description: Semantic clustering plugin (related posts, tag families, sidebar, breadcrumbs & schemas).
 * Version: 1.2.0
 * Author: Bruno Flaven & IA
 * Text Domain: semaphore
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'SEMAPHORE_VERSION', '1.2.0' );

/* --------------------------------------------------------------------------
 * DB TABLES + OPTIONS
 * ----------------------------------------------------------------------- */

function semaphore_activate() {
    global $wpdb;

    $charset_collate = $wpdb->get_charset_collate();

    // Related posts embeddings table.
    $table_related = $wpdb->prefix . 'related_posts_embeddings';
    $sql_related   = "CREATE TABLE `{$table_related}` (
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

    // Tag families table (pure overlay on existing post_tag terms).
    $table_families = $wpdb->prefix . 'tag_families';
    $sql_families   = "CREATE TABLE `{$table_families}` (
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
    dbDelta( $sql_related );
    dbDelta( $sql_families );

    add_option( 'semaphore_debug', 0 );
    add_option( 'semaphore_enable_sidebar', 1 );
    add_option( 'semaphore_enable_footer', 1 );
    add_option( 'semaphore_enable_breadcrumbs', 1 );
    add_option( 'semaphore_enable_schema', 1 );

    set_transient( 'semaphore_activation_notice', true, 30 );
}
register_activation_hook( __FILE__, 'semaphore_activate' );

function semaphore_uninstall() {
    global $wpdb;

    $wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}related_posts_embeddings`" );
    $wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}tag_families`" );

    delete_option( 'semaphore_debug' );
    delete_option( 'semaphore_enable_sidebar' );
    delete_option( 'semaphore_enable_footer' );
    delete_option( 'semaphore_enable_breadcrumbs' );
    delete_option( 'semaphore_enable_schema' );
}
register_uninstall_hook( __FILE__, 'semaphore_uninstall' );

function semaphore_activation_notice() {
    if ( get_transient( 'semaphore_activation_notice' ) ) {
        delete_transient( 'semaphore_activation_notice' );
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p><strong>Semaphore:</strong> Tables created. Go to Settings → Semaphore to import CSV and configure options.</p>';
        echo '</div>';
    }
}
add_action( 'admin_notices', 'semaphore_activation_notice' );

/* --------------------------------------------------------------------------
 * FRONTEND ASSETS (CSS)
 * ----------------------------------------------------------------------- */

function semaphore_enqueue_front_assets() {
    if ( is_admin() ) {
        return;
    }

    // Zaatar purple look & feel.
    wp_enqueue_style(
        'semaphore-frontend',
        plugins_url( 'assets/css/bf-semantic-seo-styles.css', __FILE__ ),
        array(),
        '1.0.0'
    );
}
add_action( 'wp_enqueue_scripts', 'semaphore_enqueue_front_assets' );

/* --------------------------------------------------------------------------
 * SETTINGS PAGE + MENUS
 * ----------------------------------------------------------------------- */

function semaphore_register_settings() {
    register_setting( 'semaphore_settings', 'semaphore_debug', array( 'type' => 'boolean', 'default' => 0 ) );
    register_setting( 'semaphore_settings', 'semaphore_enable_sidebar', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'semaphore_settings', 'semaphore_enable_footer', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'semaphore_settings', 'semaphore_enable_breadcrumbs', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'semaphore_settings', 'semaphore_enable_schema', array( 'type' => 'boolean', 'default' => 1 ) );
}
add_action( 'admin_init', 'semaphore_register_settings' );

function semaphore_admin_menu() {
    // Main settings.
    add_options_page(
        'Semaphore',
        'Semaphore',
        'manage_options',
        'semaphore',
        'semaphore_render_settings_page'
    );

    // Related embeddings CSV.
    add_submenu_page(
        'options-general.php',
        'Semaphore – Related Embeddings',
        'Semaphore: Related Embeddings',
        'manage_options',
        'semaphore-related',
        'semaphore_re_render_csv_page'
    );

    // Families CSV (legacy import).
    add_submenu_page(
        'options-general.php',
        'Semaphore – Tag Families CSV',
        'Semaphore: Tag Families CSV',
        'manage_options',
        'semaphore-families-csv',
        'semaphore_tf_render_csv_page'
    );

    // Tag Families manager UI.
    add_submenu_page(
        'options-general.php',
        'Semaphore – Tag Families',
        'Semaphore: Tag Families',
        'manage_options',
        'semaphore-dashboard',
        'semaphore_render_dashboard_page'
    );
}
add_action( 'admin_menu', 'semaphore_admin_menu' );

function semaphore_render_settings_page() {
    ?>
    <div class="wrap">
        <h1>Semaphore</h1>

        <form method="post" action="options.php">
            <?php settings_fields( 'semaphore_settings' ); ?>

            <h2>Features</h2>
            <table class="form-table">
                <tr>
                    <th scope="row">Debug mode</th>
                    <td>
                        <label>
                            <input type="checkbox" name="semaphore_debug" value="1" <?php checked( get_option( 'semaphore_debug' ), 1 ); ?>>
                            Enable debug blocks in semantic sidebar.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Semantic Sidebar</th>
                    <td>
                        <label>
                            <input type="checkbox" name="semaphore_enable_sidebar" value="1" <?php checked( get_option( 'semaphore_enable_sidebar' ), 1 ); ?>>
                            Enable semantic sidebar widget / shortcode.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Footer Related Content</th>
                    <td>
                        <label>
                            <input type="checkbox" name="semaphore_enable_footer" value="1" <?php checked( get_option( 'semaphore_enable_footer' ), 1 ); ?>>
                            Append related posts/tags after post content.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Breadcrumbs</th>
                    <td>
                        <label>
                            <input type="checkbox" name="semaphore_enable_breadcrumbs" value="1" <?php checked( get_option( 'semaphore_enable_breadcrumbs' ), 1 ); ?>>
                            Enable semantic breadcrumbs functions.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Schema.org JSON-LD</th>
                    <td>
                        <label>
                            <input type="checkbox" name="semaphore_enable_schema" value="1" <?php checked( get_option( 'semaphore_enable_schema' ), 1 ); ?>>
                            Output breadcrumb & tag archive schemas in &lt;head&gt;.
                        </label>
                    </td>
                </tr>
            </table>

            <?php submit_button(); ?>
        </form>

        <hr>
        <h2>Help / Operation Mode</h2>
        <h3>Install</h3>
        <ul>
            <li>Activate this plugin; tables are created automatically.</li>
            <li>Import CSVs via Settings → Semaphore: Related Embeddings / Semaphore: Tag Families CSV.</li>
            <li>Use shortcodes <code>[semaphore_related_posts]</code>, <code>[semaphore_related_tags]</code>, <code>[semaphore_sidebar]</code> where needed.</li>
        </ul>

        <h3>Uninstall</h3>
        <ul>
            <li>Delete the plugin from Plugins page.</li>
            <li>Tables <code>wp_related_posts_embeddings</code> and <code>wp_tag_families</code> are dropped.</li>
            <li>Options created by this plugin are removed.</li>
        </ul>
    </div>
    <?php
}

/* --------------------------------------------------------------------------
 * RELATED POSTS (DB + CSV + META BOX + SHORTCODE)
 * ----------------------------------------------------------------------- */

function semaphore_re_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}

function semaphore_re_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;
    $table = semaphore_re_table_name();

    $custom_order = get_post_meta( $post_id, '_semaphore_custom_related_order', true );

    if ( ! empty( $custom_order ) && is_array( $custom_order ) ) {
        $out  = array();
        $rank = 1;

        foreach ( $custom_order as $related_id ) {
            $sql = $wpdb->prepare(
                "SELECT similarity FROM `{$table}` WHERE post_id = %d AND related_post_id = %d LIMIT 1",
                $post_id,
                $related_id
            );
            $similarity = $wpdb->get_var( $sql );

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

    $sql = $wpdb->prepare(
        "SELECT related_post_id, similarity, `rank`
         FROM `{$table}`
         WHERE post_id = %d
         ORDER BY `rank` ASC
         LIMIT %d",
        $post_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );
    $out  = array();

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

function semaphore_re_save_meta_box( $post_id ) {
    if ( ! isset( $_POST['semaphore_re_nonce'] ) || ! wp_verify_nonce( $_POST['semaphore_re_nonce'], 'semaphore_re_save' ) ) {
        return;
    }
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }

    global $wpdb;
    $table = semaphore_re_table_name();

    if ( isset( $_POST['semaphore_full_reset'] ) && $_POST['semaphore_full_reset'] === '1' ) {
        delete_post_meta( $post_id, '_semaphore_custom_related_selection' );
        delete_post_meta( $post_id, '_semaphore_custom_mode_active' );
        delete_post_meta( $post_id, '_semaphore_custom_related_order' );
        return;
    }

    $is_custom = isset( $_POST['semaphore_custom_selection'] ) && $_POST['semaphore_custom_selection'] === '1';

    if ( $is_custom ) {
        $selected_ids = isset( $_POST['semaphore_selected_ids'] ) ? json_decode( stripslashes( $_POST['semaphore_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );

        $ordered_ids = isset( $_POST['semaphore_ordered_ids'] ) ? json_decode( stripslashes( $_POST['semaphore_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $ordered_selected = array_values( array_intersect( $ordered_ids, $selected_ids ) );

        update_post_meta( $post_id, '_semaphore_custom_related_selection', $selected_ids );
        update_post_meta( $post_id, '_semaphore_custom_related_order', $ordered_selected );
        update_post_meta( $post_id, '_semaphore_custom_mode_active', '1' );
    } else {
        delete_post_meta( $post_id, '_semaphore_custom_related_selection' );
        delete_post_meta( $post_id, '_semaphore_custom_mode_active' );
        delete_post_meta( $post_id, '_semaphore_custom_related_order' );

        $ordered_ids = isset( $_POST['semaphore_ordered_ids'] ) ? json_decode( stripslashes( $_POST['semaphore_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $wpdb->delete( $table, array( 'post_id' => $post_id ), array( '%d' ) );

        $rank = 1;
        foreach ( $ordered_ids as $related_id ) {
            if ( $related_id > 0 && $related_id !== $post_id ) {
                $wpdb->insert(
                    $table,
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
add_action( 'save_post', 'semaphore_re_save_meta_box' );

function semaphore_re_render_meta_box( WP_Post $post ) {
    wp_nonce_field( 'semaphore_re_save', 'semaphore_re_nonce' );

    $post_id      = $post->ID;
    $related_rows = semaphore_re_get_related_from_db( $post_id, 100 );

    $custom_selection   = get_post_meta( $post_id, '_semaphore_custom_related_selection', true );
    $custom_mode_active = get_post_meta( $post_id, '_semaphore_custom_mode_active', true );
    $is_custom          = ! empty( $custom_selection ) || $custom_mode_active === '1';
    $selected_ids       = ! empty( $custom_selection ) ? $custom_selection : array();
    ?>
    <div id="semaphore-related-posts-wrap">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <label style="margin:0;">
                <input type="checkbox" id="semaphore-custom-selection" name="semaphore_custom_selection" value="1" <?php checked( $is_custom ); ?>>
                <strong>Custom selection</strong>
            </label>
            <?php if ( $is_custom ) : ?>
                <button type="button" id="semaphore-reset-selection" class="button button-small" style="padding:2px 8px;height:auto;">Reset</button>
            <?php endif; ?>
        </div>

        <div id="semaphore-custom-mode-help" style="display:<?php echo $is_custom ? 'block' : 'none'; ?>;padding:8px;background:#fff3cd;border-left:3px solid #ffc107;margin-bottom:10px;font-size:12px;">
            Click to select/deselect. Drag to reorder. Selected posts = green.
        </div>

        <div id="semaphore-default-mode-help" style="display:<?php echo $is_custom ? 'none' : 'block'; ?>;padding:8px;background:#d1ecf1;border-left:3px solid #0c5460;margin-bottom:10px;font-size:12px;">
            All posts shown. Drag to reorder.
        </div>

        <ul id="semaphore-related-posts-list" style="list-style:none;padding:0;margin:0 0 10px 0;">
            <?php if ( ! empty( $related_rows ) ) : ?>
                <?php foreach ( $related_rows as $row ) :
                    $rel_post = get_post( $row['related_post_id'] );
                    if ( ! $rel_post ) {
                        continue;
                    }
                    $is_selected  = in_array( $rel_post->ID, $selected_ids, true );
                    $bg_color     = $is_selected ? '#d4edda' : '#f0f0f0';
                    $border_color = $is_selected ? '#28a745' : '#2271b1';
                    ?>
                    <li class="semaphore-related-item <?php echo $is_selected ? 'selected' : ''; ?>"
                        data-id="<?php echo esc_attr( $rel_post->ID ); ?>"
                        style="padding:8px;margin:3px 0;background:<?php echo $bg_color; ?>;cursor:move;border-left:3px solid <?php echo $border_color; ?>;transition:all 0.2s;">
                        <span class="dashicons dashicons-menu" style="color:#999;margin-right:5px;"></span>
                        <strong>#<?php echo $rel_post->ID; ?></strong> — <?php echo esc_html( get_the_title( $rel_post ) ); ?>
                        <span class="semaphore-check-icon" style="float:right;display:<?php echo $is_selected ? 'inline' : 'none'; ?>;">✓</span>
                    </li>
                <?php endforeach; ?>
            <?php else : ?>
                <li style="padding:8px;color:#666;font-style:italic;">No related posts. Import CSV or add below.</li>
            <?php endif; ?>
        </ul>

        <input type="hidden" id="semaphore-selected-ids" name="semaphore_selected_ids" value="<?php echo esc_attr( json_encode( $selected_ids ) ); ?>">
        <input type="hidden" id="semaphore-ordered-ids" name="semaphore_ordered_ids" value="">

        <div style="margin-top:15px;padding-top:15px;border-top:1px solid #ddd;">
            <p style="margin-top:0;"><strong>Add more posts:</strong></p>
            <input type="text" id="semaphore-post-search" placeholder="Search by ID or title..." style="width:100%;">
            <div id="semaphore-search-results" style="max-height:200px;overflow-y:auto;border:1px solid #ddd;display:none;background:white;margin-top:5px;"></div>
        </div>
    </div>

    <script>
    jQuery(document).ready(function($){
        var isCustomMode = $('#semaphore-custom-selection').is(':checked');

        $('#semaphore-related-posts-list').sortable({
            placeholder: 'ui-state-highlight',
            handle: '.dashicons-menu',
            update: function(){ updateOrderedIds(); }
        });

        function updateOrderedIds(){
            var orderedIds = [];
            $('.semaphore-related-item').each(function(){
                orderedIds.push($(this).data('id'));
            });
            $('#semaphore-ordered-ids').val(JSON.stringify(orderedIds));
        }
        updateOrderedIds();

        $('#semaphore-custom-selection').on('change', function(){
            isCustomMode = $(this).is(':checked');
            if(isCustomMode){
                $('#semaphore-custom-mode-help').show();
                $('#semaphore-default-mode-help').hide();
            } else {
                $('#semaphore-custom-mode-help').hide();
                $('#semaphore-default-mode-help').show();
                $('.semaphore-related-item').removeClass('selected')
                    .css({'background':'#f0f0f0','border-left-color':'2271b1'})
                    .find('.semaphore-check-icon').hide();
                $('#semaphore-selected-ids').val('[]');
            }
        });

        $(document).on('click','#semaphore-reset-selection',function(){
            if(confirm('Reset to default? This will remove custom selection and show all posts from CSV/database.')){
                $('<input>').attr({
                    type:'hidden',
                    name:'semaphore_full_reset',
                    value:'1'
                }).appendTo('#post');
                $('#publish, #save-post').click();
            }
        });

        $(document).on('click','.semaphore-related-item',function(e){
            if(!isCustomMode) return;
            if($(e.target).hasClass('dashicons-menu')) return;

            var $item = $(this);
            var postId = $item.data('id');
            var selectedIds = JSON.parse($('#semaphore-selected-ids').val() || '[]');

            if($item.hasClass('selected')){
                $item.removeClass('selected')
                    .css({'background':'#f0f0f0','border-left-color':'2271b1'})
                    .find('.semaphore-check-icon').hide();
                selectedIds = selectedIds.filter(function(id){ return id !== postId; });
            } else {
                $item.addClass('selected')
                    .css({'background':'#d4edda','border-left-color':'28a745'})
                    .find('.semaphore-check-icon').show();
                selectedIds.push(postId);
            }

            $('#semaphore-selected-ids').val(JSON.stringify(selectedIds));
            updateOrderedIds();
        });

        var searchTimeout;
        $('#semaphore-post-search').on('keyup', function(){
            var query = $(this).val();
            if(query.length < 2){
                $('#semaphore-search-results').hide();
                return;
            }
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function(){
                $.ajax({
                    url: ajaxurl,
                    data: {
                        action: 'semaphore_search_posts',
                        query: query,
                        exclude: <?php echo (int) $post_id; ?>
                    },
                    success: function(response){
                        if(response.success){
                            var html = '';
                            $.each(response.data, function(i, post){
                                html += '<div class="semaphore-search-result" data-id="'+post.ID+'" data-title="'+post.post_title+'" style="padding:5px;cursor:pointer;border-bottom:1px solid #eee;">';
                                html += '<strong>#'+post.ID+'</strong> — '+post.post_title;
                                html += '</div>';
                            });
                            $('#semaphore-search-results').html(html).show();
                        }
                    }
                });
            },300);
        });

        $(document).on('click','.semaphore-search-result',function(){
            var postId = $(this).data('id');
            var postTitle = $(this).data('title');

            if($('.semaphore-related-item[data-id="'+postId+'"]').length){
                alert('Already in list');
                return;
            }

            var isSelected = isCustomMode;
            var bgColor = isSelected ? '#d4edda' : '#f0f0f0';
            var borderColor = isSelected ? '#28a745' : '#2271b1';
            var checkDisplay = isSelected ? 'inline' : 'none';

            var html = '<li class="semaphore-related-item '+(isSelected?'selected':'')+'" data-id="'+postId+'" style="padding:8px;margin:3px 0;background:'+bgColor+';cursor:move;border-left:3px solid '+borderColor+';transition:all 0.2s;">';
            html += '<span class="dashicons dashicons-menu" style="color:#999;margin-right:5px;"></span>';
            html += '<strong>#'+postId+'</strong> — '+postTitle;
            html += '<span class="semaphore-check-icon" style="float:right;display:'+checkDisplay+';">✓</span>';
            html += '</li>';

            $('#semaphore-related-posts-list').append(html);

            if(isCustomMode){
                var selectedIds = JSON.parse($('#semaphore-selected-ids').val() || '[]');
                selectedIds.push(postId);
                $('#semaphore-selected-ids').val(JSON.stringify(selectedIds));
            }

            updateOrderedIds();
            $('#semaphore-post-search').val('');
            $('#semaphore-search-results').hide();
        });

        $(document).on('click', function(e){
            if(!$(e.target).closest('#semaphore-post-search, #semaphore-search-results').length){
                $('#semaphore-search-results').hide();
            }
        });
    });
    </script>
    <?php
}

function semaphore_re_add_meta_box() {
    add_meta_box(
        'semaphore_related_embeddings_meta_box',
        'Semaphore – Related Posts',
        'semaphore_re_render_meta_box',
        'post',
        'side',
        'default'
    );
}
add_action( 'add_meta_boxes', 'semaphore_re_add_meta_box' );

function semaphore_re_ajax_search_posts() {
    $query   = isset( $_GET['query'] ) ? sanitize_text_field( $_GET['query'] ) : '';
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

    $posts   = get_posts( $args );
    $results = array();

    foreach ( $posts as $p ) {
        $results[] = array(
            'ID'         => $p->ID,
            'post_title' => $p->post_title,
        );
    }

    wp_send_json_success( $results );
}
add_action( 'wp_ajax_semaphore_search_posts', 'semaphore_re_ajax_search_posts' );

function semaphore_re_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    if ( ! isset( $_POST['semaphore_re_import_nonce'] ) || ! wp_verify_nonce( $_POST['semaphore_re_import_nonce'], 'semaphore_re_import_csv' ) ) {
        return;
    }
    if ( empty( $_FILES['semaphore_re_csv']['tmp_name'] ) ) {
        add_settings_error( 'semaphore_re_messages', 'semaphore_re_no_file', 'No CSV file uploaded.', 'error' );
        return;
    }

    $tmp_name = $_FILES['semaphore_re_csv']['tmp_name'];
    $handle   = fopen( $tmp_name, 'r' );
    if ( ! $handle ) {
        add_settings_error( 'semaphore_re_messages', 'semaphore_re_file_open_error', 'Could not open file.', 'error' );
        return;
    }

    global $wpdb;
    $table = semaphore_re_table_name();

    if ( isset( $_POST['semaphore_re_truncate_table'] ) && $_POST['semaphore_re_truncate_table'] === '1' ) {
        $wpdb->query( "TRUNCATE TABLE `{$table}`" );
    }

    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error( 'semaphore_re_messages', 'semaphore_re_bad_header', 'CSV has no header.', 'error' );
        return;
    }

    $normalized = array();
    foreach ( $header as $col ) {
        $col          = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
        $normalized[] = strtolower( trim( $col ) );
    }

    $idx_post_id         = array_search( 'post_id', $normalized, true );
    $idx_related_post_id = array_search( 'related_post_id', $normalized, true );
    $idx_similarity      = array_search( 'similarity', $normalized, true );
    $idx_rank            = array_search( 'rank', $normalized, true );

    if ( $idx_post_id === false || $idx_related_post_id === false || $idx_similarity === false || $idx_rank === false ) {
        fclose( $handle );
        add_settings_error( 'semaphore_re_messages', 'semaphore_re_missing_columns', 'CSV must have: post_id, related_post_id, similarity, rank', 'error' );
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
            $table,
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
    if ( isset( $_POST['semaphore_re_truncate_table'] ) && $_POST['semaphore_re_truncate_table'] === '1' ) {
        $message .= ' (Table truncated first)';
    }

    add_settings_error( 'semaphore_re_messages', 'semaphore_re_import_success', $message, 'updated' );
}

function semaphore_re_render_csv_page() {
    global $wpdb;

    if ( isset( $_POST['semaphore_re_import_submit'] ) ) {
        semaphore_re_handle_csv_import();
    }

    settings_errors( 'semaphore_re_messages' );

    $table       = semaphore_re_table_name();
    $table_exist = $wpdb->get_var( "SHOW TABLES LIKE '{$table}'" );
    $row_count   = 0;

    if ( $table_exist === $table ) {
        $row_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM `{$table}`" );
    }
    ?>
    <div class="wrap">
        <h1>Semaphore – Related Posts Embeddings</h1>

        <div class="card">
            <h2>Database Status</h2>
            <table class="widefat">
                <tr>
                    <td><strong>Table:</strong></td>
                    <td><code><?php echo esc_html( $table ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Status:</strong></td>
                    <td><?php echo $table_exist === $table ? '<span style="color:green;">✓ Exists</span>' : '<span style="color:red;">✗ Missing</span>'; ?></td>
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
            <?php wp_nonce_field( 'semaphore_re_import_csv', 'semaphore_re_import_nonce' ); ?>

            <table class="form-table">
                <tr>
                    <th><label for="semaphore_re_csv">CSV File</label></th>
                    <td><input type="file" id="semaphore_re_csv" name="semaphore_re_csv" accept=".csv"></td>
                </tr>
                <tr>
                    <th><label for="semaphore_re_truncate_table">Truncate table first?</label></th>
                    <td>
                        <label>
                            <input type="checkbox" id="semaphore_re_truncate_table" name="semaphore_re_truncate_table" value="1">
                            Delete all existing data before import
                        </label>
                    </td>
                </tr>
            </table>

            <?php submit_button( 'Import CSV', 'primary', 'semaphore_re_import_submit' ); ?>
        </form>
    </div>
    <?php
}

/* PUBLIC API + SHORTCODE FOR RELATED POSTS */

function semaphore_get_related_posts( $post_id = 0, $limit = 5 ) {
    if ( ! $post_id ) {
        $post_id = get_the_ID();
    }

    $related_rows = semaphore_re_get_related_from_db( $post_id, $limit );
    $results      = array();

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

function semaphore_re_shortcode( $atts ) {
    $atts = shortcode_atts(
        array(
            'post_id' => get_the_ID(),
            'limit'   => 5,
            'title'   => 'Related Posts',
        ),
        $atts
    );

    $related = semaphore_get_related_posts( $atts['post_id'], $atts['limit'] );

    if ( empty( $related ) ) {
        return '';
    }

    $html = '<div class="bf-post-footer">';
    if ( ! empty( $atts['title'] ) ) {
        $html .= '<h3>' . esc_html( $atts['title'] ) . '</h3>';
    }

    $html .= '<div class="related-posts-grid">';
    foreach ( $related as $post ) {
        $html .= '<article class="related-post-card">';
        if ( $post['thumbnail'] ) {
            $html .= '<img src="' . esc_url( $post['thumbnail'] ) . '" alt="' . esc_attr( $post['title'] ) . '">';
        }
        $html .= '<div class="card-content">';
        $html .= '<h4><a href="' . esc_url( $post['permalink'] ) . '">' . esc_html( $post['title'] ) . '</a></h4>';
        if ( $post['excerpt'] ) {
            $html .= '<p>' . esc_html( wp_trim_words( $post['excerpt'], 20 ) ) . '</p>';
        }
        $html .= '</div></article>';
    }
    $html .= '</div></div>';

    return $html;
}
add_shortcode( 'semaphore_related_posts', 'semaphore_re_shortcode' );

function semaphore_re_enqueue_admin_scripts( $hook ) {
    if ( in_array( $hook, array( 'post.php', 'post-new.php' ), true ) ) {
        wp_enqueue_script( 'jquery-ui-sortable' );
    }
}
add_action( 'admin_enqueue_scripts', 'semaphore_re_enqueue_admin_scripts' );

/* --------------------------------------------------------------------------
 * TAG FAMILIES – DB + CSV (overlay only, does NOT change post_tag terms)
 * ----------------------------------------------------------------------- */

function semaphore_tf_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'tag_families';
}

function semaphore_tf_get_family_members( $tag_id, $limit = 20 ) {
    global $wpdb;
    $table = semaphore_tf_table_name();

    $sql = $wpdb->prepare(
        "SELECT tag_id, tag_label, canonical_tag_id, canonical_label, similarity_to_canonical, usage_count, entity_label, family_id
         FROM `{$table}`
         WHERE family_id = (SELECT family_id FROM `{$table}` WHERE tag_id = %d LIMIT 1)
         AND tag_id != %d
         ORDER BY similarity_to_canonical DESC
         LIMIT %d",
        $tag_id,
        $tag_id,
        $limit
    );

    $rows = $wpdb->get_results( $sql, ARRAY_A );
    $out  = array();
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

/* CSV IMPORT PAGE */

function semaphore_tf_handle_csv_import() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    if ( ! isset( $_POST['semaphore_tf_import_nonce'] ) || ! wp_verify_nonce( $_POST['semaphore_tf_import_nonce'], 'semaphore_tf_import_csv' ) ) {
        return;
    }
    if ( empty( $_FILES['semaphore_tf_csv']['tmp_name'] ) ) {
        add_settings_error( 'semaphore_tf_messages', 'semaphore_tf_no_file', 'No CSV file uploaded.', 'error' );
        return;
    }

    $tmp_name = $_FILES['semaphore_tf_csv']['tmp_name'];
    $handle   = fopen( $tmp_name, 'r' );
    if ( ! $handle ) {
        add_settings_error( 'semaphore_tf_messages', 'semaphore_tf_file_open_error', 'Could not open file.', 'error' );
        return;
    }

    global $wpdb;
    $table = semaphore_tf_table_name();

    if ( isset( $_POST['semaphore_tf_truncate_table'] ) && $_POST['semaphore_tf_truncate_table'] === '1' ) {
        $wpdb->query( "TRUNCATE TABLE `{$table}`" );
    }

    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error( 'semaphore_tf_messages', 'semaphore_tf_bad_header', 'CSV has no header.', 'error' );
        return;
    }

    $normalized = array();
    foreach ( $header as $col ) {
        $col          = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
        $normalized[] = strtolower( trim( $col ) );
    }

    $idx_family_id               = array_search( 'family_id', $normalized, true );
    $idx_canonical_tag_id        = array_search( 'canonical_tag_id', $normalized, true );
    $idx_canonical_label         = array_search( 'canonical_label', $normalized, true );
    $idx_tag_id                  = array_search( 'tag_id', $normalized, true );
    $idx_tag_label               = array_search( 'tag_label', $normalized, true );
    $idx_similarity_to_canonical = array_search( 'similarity_to_canonical', $normalized, true );
    $idx_usage_count             = array_search( 'usage_count', $normalized, true );
    $idx_entity_label            = array_search( 'entity_label', $normalized, true );

    if (
        $idx_family_id === false || $idx_canonical_tag_id === false || $idx_canonical_label === false ||
        $idx_tag_id === false || $idx_tag_label === false || $idx_similarity_to_canonical === false ||
        $idx_usage_count === false || $idx_entity_label === false
    ) {
        fclose( $handle );
        add_settings_error(
            'semaphore_tf_messages',
            'semaphore_tf_missing_columns',
            'CSV must have: family_id, canonical_tag_id, canonical_label, tag_id, tag_label, similarity_to_canonical, usage_count, entity_label',
            'error'
        );
        return;
    }

    $inserted = 0;

    while ( ( $row = fgetcsv( $handle ) ) !== false ) {
        if ( empty( array_filter( $row, 'strlen' ) ) ) {
            continue;
        }

        $family_id        = isset( $row[ $idx_family_id ] ) ? (int) $row[ $idx_family_id ] : 0;
        $canonical_tag_id = isset( $row[ $idx_canonical_tag_id ] ) ? (int) $row[ $idx_canonical_tag_id ] : 0;
        $canonical_label  = isset( $row[ $idx_canonical_label ] ) ? $row[ $idx_canonical_label ] : '';
        $tag_id           = isset( $row[ $idx_tag_id ] ) ? (int) $row[ $idx_tag_id ] : 0;
        $tag_label        = isset( $row[ $idx_tag_label ] ) ? $row[ $idx_tag_label ] : '';
        $similarity_raw   = isset( $row[ $idx_similarity_to_canonical ] ) ? $row[ $idx_similarity_to_canonical ] : '0';
        $usage_count      = isset( $row[ $idx_usage_count ] ) ? (int) $row[ $idx_usage_count ] : 0;
        $entity_label     = isset( $row[ $idx_entity_label ] ) ? $row[ $idx_entity_label ] : '';

        $similarity_to_canonical = (float) str_replace( ',', '.', $similarity_raw );

        if ( $family_id <= 0 || $canonical_tag_id <= 0 || $tag_id <= 0 ) {
            continue;
        }

        $result = $wpdb->replace(
            $table,
            array(
                'family_id'               => $family_id,
                'canonical_tag_id'        => $canonical_tag_id,
                'canonical_label'         => $canonical_label,
                'tag_id'                  => $tag_id,
                'tag_label'               => $tag_label,
                'similarity_to_canonical' => $similarity_to_canonical,
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

    $message = sprintf( 'Imported %d rows.', $inserted );
    if ( isset( $_POST['semaphore_tf_truncate_table'] ) && $_POST['semaphore_tf_truncate_table'] === '1' ) {
        $message .= ' (Table truncated first)';
    }

    add_settings_error( 'semaphore_tf_messages', 'semaphore_tf_import_success', $message, 'updated' );
}

function semaphore_tf_render_csv_page() {
    global $wpdb;

    if ( isset( $_POST['semaphore_tf_import_submit'] ) ) {
        semaphore_tf_handle_csv_import();
    }

    settings_errors( 'semaphore_tf_messages' );

    $table       = semaphore_tf_table_name();
    $table_exist = $wpdb->get_var( "SHOW TABLES LIKE '{$table}'" );
    $row_count   = 0;

    if ( $table_exist === $table ) {
        $row_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM `{$table}`" );
    }
    ?>
    <div class="wrap">
        <h1>Semaphore – Tag Families CSV</h1>

        <div class="card">
            <h2>Database Status</h2>
            <table class="widefat">
                <tr>
                    <td><strong>Table:</strong></td>
                    <td><code><?php echo esc_html( $table ); ?></code></td>
                </tr>
                <tr>
                    <td><strong>Status:</strong></td>
                    <td><?php echo $table_exist === $table ? '<span style="color:green;">✓ Exists</span>' : '<span style="color:red;">✗ Missing</span>'; ?></td>
                </tr>
                <tr>
                    <td><strong>Rows:</strong></td>
                    <td><strong><?php echo number_format( $row_count ); ?></strong></td>
                </tr>
            </table>
        </div>

        <h2>CSV Import</h2>
        <p>CSV format: <code>family_id,canonical_tag_id,canonical_label,tag_id,tag_label,similarity_to_canonical,usage_count,entity_label</code></p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'semaphore_tf_import_csv', 'semaphore_tf_import_nonce' ); ?>

            <table class="form-table">
                <tr>
                    <th><label for="semaphore_tf_csv">CSV File</label></th>
                    <td><input type="file" id="semaphore_tf_csv" name="semaphore_tf_csv" accept=".csv"></td>
                </tr>
                <tr>
                    <th><label for="semaphore_tf_truncate_table">Truncate table first?</label></th>
                    <td>
                        <label>
                            <input type="checkbox" id="semaphore_tf_truncate_table" name="semaphore_tf_truncate_table" value="1">
                            Delete all existing data before import
                        </label>
                    </td>
                </tr>
            </table>

            <?php submit_button( 'Import CSV', 'primary', 'semaphore_tf_import_submit' ); ?>
        </form>
    </div>
    <?php
}

/* PUBLIC API + SHORTCODE FOR RELATED TAGS (OVERLAY ONLY) */

function semaphore_get_related_tags( $tag_id = 0, $limit = 5 ) {
    if ( ! $tag_id ) {
        $tag = get_queried_object();
        if ( $tag && ! is_wp_error( $tag ) && isset( $tag->term_id ) ) {
            $tag_id = $tag->term_id;
        }
    }
    if ( ! $tag_id ) {
        return array();
    }

    $rows = semaphore_tf_get_family_members( $tag_id, $limit );
    $out  = array();

    foreach ( $rows as $row ) {
        $term = get_term( $row['tag_id'], 'post_tag' );
        if ( $term && ! is_wp_error( $term ) ) {
            $out[] = array(
                'term_id'      => $term->term_id,
                'name'         => $term->name,
                'slug'         => $term->slug,
                'link'         => get_term_link( $term ),
                'similarity'   => $row['similarity_to_canonical'],
                'usage_count'  => $row['usage_count'],
                'entity_label' => $row['entity_label'],
                'family_id'    => $row['family_id'],
            );
        }
    }

    return $out;
}

function semaphore_tf_shortcode( $atts ) {
    $atts = shortcode_atts(
        array(
            'tag_id' => 0,
            'limit'  => 10,
            'title'  => 'Related Tags',
        ),
        $atts
    );

    $tag_id = (int) $atts['tag_id'];
    if ( ! $tag_id ) {
        $tag = get_queried_object();
        if ( $tag && ! is_wp_error( $tag ) && isset( $tag->term_id ) ) {
            $tag_id = $tag->term_id;
        }
    }
    if ( ! $tag_id ) {
        return '';
    }

    $related = semaphore_get_related_tags( $tag_id, (int) $atts['limit'] );
    if ( empty( $related ) ) {
        return '';
    }

    $html = '<div class="related-tags-section">';
    if ( ! empty( $atts['title'] ) ) {
        $html .= '<h4>' . esc_html( $atts['title'] ) . '</h4>';
    }
    $html .= '<div class="tag-cloud">';
    foreach ( $related as $tag ) {
        $html .= '<a class="tag-badge" href="' . esc_url( $tag['link'] ) . '">' . esc_html( $tag['name'] ) . '</a>';
    }
    $html .= '</div></div>';

    return $html;
}
add_shortcode( 'semaphore_related_tags', 'semaphore_tf_shortcode' );

/* --------------------------------------------------------------------------
 * TAG FAMILIES MANAGER DASHBOARD PAGE (FAMILIES OVERLAY ONLY)
 * ----------------------------------------------------------------------- */

function semaphore_tagfamilies_table() {
    return semaphore_tf_table_name();
}

function semaphore_admin_enqueue( $hook ) {
    if ( $hook !== 'settings_page_semaphore-dashboard' ) {
        return;
    }

    // Simple highlight style for active rows in the dashboard for tags and families
    wp_register_style( 'semaphore-admin-inline', false );
    wp_enqueue_style( 'semaphore-admin-inline' );
    wp_add_inline_style(
        'semaphore-admin-inline',
        '#semaphore-families-layout .active{background:#d4edda !important;border-left:3px solid #28a745 !important;}'
    );
/*
    wp_enqueue_script(
        'semaphore-families-manager',
        plugins_url( 'semaphore-families-manager.js', __FILE__ ),
        array( 'jquery' ),
        SEMAPHORE_VERSION,
        true
    );
*/

    wp_enqueue_script(
        'semaphore-families-manager',
        plugins_url( 'assets/js/semaphore-families-manager.js', __FILE__ ),
        array( 'jquery' ),
        SEMAPHORE_VERSION,
        true
    );

    wp_localize_script(
        'semaphore-families-manager',
        'semaphoreDashboard',
        array(
            'ajax_url' => admin_url( 'admin-ajax.php' ),
            'nonce'    => wp_create_nonce( 'semaphore_families_nonce' ),
        )
    );
}
add_action( 'admin_enqueue_scripts', 'semaphore_admin_enqueue' );

/**
 * Render the Tag Families Manager dashboard page.
 *
 * Layout:
 * - Left main card with workspace header + collapsible help.
 * - Right sidebar with context cards ("How this fits" and an example workflow).
 * - Below: 2-column grid (All Tags on the left, Tag Families + Family Members on the right).
 */
function semaphore_render_dashboard_page() {
    ?>
    <div class="wrap semaphore-dashboard-wrap">

        <h1>Semaphore – Tag Families Manager</h1>
        <p>
            Manage tag families as a clustering layer on top of your existing <code>post_tag</code> terms.
            Existing tags on posts are never modified; this screen only manages the overlay families table.
        </p>

        <div class="semaphore-dashboard-shell">

            <!-- Main workspace card -->
            <div class="semaphore-dashboard-main">
                <div class="semaphore-card semaphore-card--primary">

                    <!-- Card header with title and help toggle -->
                    <div class="semaphore-card-header">
                        <div class="semaphore-card-header-main">
                            <h2 class="semaphore-card-title">Tag Families Workspace</h2>
                            <p class="semaphore-card-description">
                                Use this workspace to explore all tags, promote canonical tags to families,
                                and attach/detach related tags into semantic clusters.
                            </p>
                        </div>

                        <div class="semaphore-card-header-side">
                            <button
                                type="button"
                                class="button button-secondary semaphore-help-toggle"
                                aria-expanded="false"
                                aria-controls="semaphore-help-panel"
                            >
                                Show help
                            </button>
                        </div>
                    </div>

                    <!-- Collapsible help panel -->
                    <div id="semaphore-help-panel" class="semaphore-help-panel" hidden>
                        <div class="semaphore-help-inner">
                            <h3>How to use this manager</h3>

                            <h4>User stories</h4>
                            <ul>
                                <li>
                                    <strong>As an editor</strong>, I want to pick any existing tag and convert it into a
                                    “family” so that I can group similar tags around this canonical tag without
                                    touching the original post tags.
                                </li>
                                <li>
                                    <strong>As an editor</strong>, I want to attach or detach tags from a family so that
                                    my semantic clusters stay aligned with how the newsroom uses tags.
                                </li>
                                <li>
                                    <strong>As an SEO user</strong>, I want to reuse these families to drive
                                    “Related Tags IA” and “Related Posts IA” blocks fed by
                                    <em>Semaphore: Related Embeddings</em> and
                                    <em>Semaphore: Tag Families CSV</em>.
                                </li>
                            </ul>

                            <h4>All Tags (left column)</h4>
                            <ul>
                                <li>Lists all existing <code>post_tag</code> terms from WordPress.</li>
                                <li>Use the search box to filter tags by name or ID.</li>
                                <li>Click a row to select a tag (the row turns light green).</li>
                                <li>The selected tag is the candidate you will convert to a family or attach to a family.</li>
                            </ul>

                            <h4>Tag Families (top right)</h4>
                            <ul>
                                <li>Each row is a family: one canonical tag that acts as the entry of a cluster.</li>
                                <li>Use the search box to filter families by ID or label.</li>
                                <li>Click a row to set the “current family” (row turns light green).</li>
                            </ul>

                            <h4>Family Members (bottom right)</h4>
                            <ul>
                                <li>Shows all tags attached to the currently selected family.</li>
                                <li>Click a member row to select it (light green background).</li>
                                <li>“Detach selected member” removes this mapping from the family (the tag itself stays in WordPress).</li>
                            </ul>

                            <h4>Actions</h4>
                            <ul>
                                <li>
                                    <strong>Convert selected tag to family</strong> – with a tag selected in “All Tags”,
                                    create or update a family where this tag is canonical.
                                </li>
                                <li>
                                    <strong>Attach selected tag to current family</strong> – with a tag selected on the
                                    left and a family selected on the right, attach the tag as a member.
                                </li>
                                <li>
                                    <strong>Detach selected member from current family</strong> – with a family and a
                                    member selected, remove the member from that family.
                                </li>
                            </ul>

                            <p class="semaphore-help-note">
                                Light green rows indicate the current selection (tag, family, or member) that actions will apply to.
                            </p>
                        </div>
                    </div>
                    <!-- /#semaphore-help-panel -->

                </div><!-- .semaphore-card -->
            </div><!-- .semaphore-dashboard-main -->

            <!-- Sidebar with context cards -->
            <aside class="semaphore-dashboard-side">
                <div class="semaphore-side-card">
                    <h3 class="semaphore-side-title">How this fits</h3>
                    <p class="semaphore-side-text">
                        Families defined here are consumed by:
                    </p>
                    <ul class="semaphore-side-links">
                        <li>
                            <strong>Semaphore: Related Embeddings</strong> – uses post/post similarities
                            to build “Related Posts IA”.
                        </li>
                        <li>
                            <strong>Semaphore: Tag Families CSV</strong> – imports/exports families to keep
                            semantic clusters in sync with your NLP pipeline.
                        </li>
                    </ul>
                </div>

                <div class="semaphore-side-card">
                    <h3 class="semaphore-side-title">Example workflow</h3>
                    <p class="semaphore-side-text">
                        As an SEO editor, I convert <em>“Ukraine”</em> into a family, then attach tags like
                        <em>“Kyiv”</em>, <em>“Zelensky”</em>, and <em>“Russia–Ukraine war”</em>. Frontend widgets
                        can now show smarter related tags and posts around this cluster.
                    </p>
                </div>
            </aside>

        </div><!-- .semaphore-dashboard-shell -->

        <!-- Help panel toggle logic (no dependency on external JS) -->
        <script>
        (function() {
            var toggle = document.querySelector('.semaphore-help-toggle');
            var panel  = document.getElementById('semaphore-help-panel');

            if (!toggle || !panel) {
                return;
            }

            toggle.addEventListener('click', function() {
                var expanded = this.getAttribute('aria-expanded') === 'true';
                expanded = !expanded;

                this.setAttribute('aria-expanded', expanded ? 'true' : 'false');
                this.textContent = expanded ? 'Hide help' : 'Show help';

                if (expanded) {
                    panel.removeAttribute('hidden');
                } else {
                    panel.setAttribute('hidden', 'hidden');
                }
            });
        })();
        </script>

        <!-- Main 2-column data layout: All Tags (left), Families + Members (right) -->
        <div id="semaphore-families-layout" style="display:flex;gap:20px;align-items:flex-start;">

            <!-- Left: All Tags table -->
            <div style="flex:1;min-width:320px;">
                <h2>All Tags</h2>
                <input
                    type="text"
                    id="semaphore-tag-search"
                    placeholder="Search tags by name or ID..."
                    style="width:100%;max-width:100%;margin-bottom:10px;"
                >
                <div
                    id="semaphore-all-tags-table"
                    style="border:1px solid #ddd;max-height:500px;overflow:auto;"
                ></div>
            </div>

            <!-- Right: Tag Families + Family Members stacked -->
            <div style="flex:1.5;min-width:420px;">
                <h2>Tag Families</h2>
                <input
                    type="text"
                    id="semaphore-family-search"
                    placeholder="Search families by ID or label..."
                    style="width:100%;max-width:100%;margin-bottom:10px;"
                >
                <div
                    id="semaphore-families-list"
                    style="border:1px solid #ddd;max-height:240px;overflow:auto;margin-bottom:15px;"
                ></div>

                <h2>Family Members</h2>
                <div
                    id="semaphore-family-members"
                    style="border:1px solid #ddd;max-height:260px;overflow:auto;margin-bottom:10px;"
                ></div>

                <div id="semaphore-family-actions">
                    <button
                        class="button button-primary"
                        id="semaphore-convert-to-family"
                        disabled
                    >
                        Convert selected tag to family
                    </button>
                    <button
                        class="button"
                        id="semaphore-attach-to-family"
                        disabled
                    >
                        Attach selected tag to current family
                    </button>
                    <button
                        class="button"
                        id="semaphore-detach-from-family"
                        disabled
                    >
                        Detach selected member from current family
                    </button>

                    <p style="font-size:12px;color:#555;margin-top:8px;">
                        All changes happen in the family table only. Post tags themselves remain unchanged.
                    </p>
                </div>
            </div>
        </div><!-- #semaphore-families-layout -->

    </div><!-- .wrap.semaphore-dashboard-wrap -->
    <?php
}


/* AJAX HANDLERS FOR DASHBOARD */

function semaphore_ajax_list_tags() {
    check_ajax_referer( 'semaphore_families_nonce', 'nonce' );
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( array( 'message' => 'Permission denied.' ) );
    }

    global $wpdb;

    $paged    = max( 1, intval( $_GET['paged'] ?? 1 ) );
    $per_page = max( 1, min( 200, intval( $_GET['per_page'] ?? 50 ) ) );
    $offset   = ( $paged - 1 ) * $per_page;
    $search   = isset( $_GET['search'] ) ? sanitize_text_field( wp_unslash( $_GET['search'] ) ) : '';

    $where  = "WHERE tt.taxonomy = 'post_tag'";
    $params = array();

    if ( $search !== '' ) {
        if ( is_numeric( $search ) ) {
            $where   .= ' AND tt.term_id = %d';
            $params[] = intval( $search );
        } else {
            $where   .= ' AND t.name LIKE %s';
            $params[] = '%' . $wpdb->esc_like( $search ) . '%';
        }
    }

    $sql_total = "
        SELECT COUNT(*)
        FROM {$wpdb->term_taxonomy} AS tt
        INNER JOIN {$wpdb->terms} AS t ON tt.term_id = t.term_id
        $where
    ";
    $total = (int) $wpdb->get_var( $wpdb->prepare( $sql_total, ...$params ) );

    $sql_rows = "
        SELECT t.term_id, t.name, tt.count
        FROM {$wpdb->term_taxonomy} AS tt
        INNER JOIN {$wpdb->terms} AS t ON tt.term_id = t.term_id
        $where
        ORDER BY t.term_id DESC
        LIMIT %d OFFSET %d
    ";
    $params_rows   = array_merge( $params, array( $per_page, $offset ) );
    $prepared_rows = $wpdb->prepare( $sql_rows, ...$params_rows );
    $rows          = $wpdb->get_results( $prepared_rows, ARRAY_A );

    wp_send_json_success(
        array(
            'rows'     => $rows,
            'total'    => $total,
            'per_page' => $per_page,
            'paged'    => $paged,
        )
    );
}
add_action( 'wp_ajax_semaphore_list_tags', 'semaphore_ajax_list_tags' );

function semaphore_ajax_list_families() {
    check_ajax_referer( 'semaphore_families_nonce', 'nonce' );
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( array( 'message' => 'Permission denied.' ) );
    }

    global $wpdb;
    $table = semaphore_tagfamilies_table();

    $sql = "
        SELECT 
            canonical_tag_id AS family_id,
            canonical_label  AS canonical_label,
            COUNT(*)         AS members
        FROM {$table}
        GROUP BY canonical_tag_id, canonical_label
        ORDER BY canonical_tag_id DESC
        LIMIT 500
    ";

    $rows = $wpdb->get_results( $sql, ARRAY_A );
    wp_send_json_success( array( 'families' => $rows ) );
}
add_action( 'wp_ajax_semaphore_list_families', 'semaphore_ajax_list_families' );

function semaphore_ajax_list_family_members() {
    check_ajax_referer( 'semaphore_families_nonce', 'nonce' );
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( array( 'message' => 'Permission denied.' ) );
    }

    global $wpdb;
    $table     = semaphore_tagfamilies_table();
    $family_id = intval( $_GET['family_id'] ?? 0 );

    if ( ! $family_id ) {
        wp_send_json_success( array( 'members' => array() ) );
    }

    $sql  = $wpdb->prepare(
        "SELECT tag_id AS tag_id,
                tag_label AS taglabel,
                usage_count AS usage_count
         FROM {$table}
         WHERE family_id = %d
         ORDER BY similarity_to_canonical DESC, usage_count DESC",
        $family_id
    );
    $rows = $wpdb->get_results( $sql, ARRAY_A );

    wp_send_json_success( array( 'members' => $rows ) );
}
add_action( 'wp_ajax_semaphore_list_family_members', 'semaphore_ajax_list_family_members' );

function semaphore_ajax_convert_to_family() {
    check_ajax_referer( 'semaphore_families_nonce', 'nonce' );
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( array( 'message' => 'Permission denied.' ) );
    }

    $tag_id = intval( $_POST['tag_id'] ?? 0 );
    if ( ! $tag_id ) {
        wp_send_json_error( array( 'message' => 'Invalid tag ID.' ) );
    }

    $tag = get_term( $tag_id, 'post_tag' );
    if ( ! $tag || is_wp_error( $tag ) ) {
        wp_send_json_error( array( 'message' => 'Tag not found.' ) );
    }

    global $wpdb;
    $table = semaphore_tagfamilies_table();

    $data = array(
        'family_id'               => $tag_id,
        'canonical_tag_id'        => $tag_id,
        'canonical_label'         => $tag->name,
        'tag_id'                  => $tag_id,
        'tag_label'               => $tag->name,
        'similarity_to_canonical' => 1.0,
        'usage_count'             => 0,
        'entity_label'            => 'O',
    );
    $formats = array( '%d', '%d', '%s', '%d', '%s', '%f', '%d', '%s' );

    $result = $wpdb->replace( $table, $data, $formats );
    if ( false === $result ) {
        wp_send_json_error( array( 'message' => 'Database error while creating family.' ) );
    }

    wp_send_json_success( array( 'message' => 'Tag converted to family (overlay only).' ) );
}
add_action( 'wp_ajax_semaphore_convert_to_family', 'semaphore_ajax_convert_to_family' );

function semaphore_ajax_attach_to_family() {
    check_ajax_referer( 'semaphore_families_nonce', 'nonce' );
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( array( 'message' => 'Permission denied.' ) );
    }

    $family_id = intval( $_POST['family_id'] ?? 0 );
    $tag_id    = intval( $_POST['tag_id'] ?? 0 );

    if ( ! $family_id || ! $tag_id ) {
        wp_send_json_error( array( 'message' => 'Missing IDs.' ) );
    }

    $family = get_term( $family_id, 'post_tag' );
    $tag    = get_term( $tag_id, 'post_tag' );

    if ( ! $family || is_wp_error( $family ) || ! $tag || is_wp_error( $tag ) ) {
        wp_send_json_error( array( 'message' => 'Family or tag not found.' ) );
    }

    global $wpdb;
    $table = semaphore_tagfamilies_table();

    $data = array(
        'family_id'               => $family_id,
        'canonical_tag_id'        => $family_id,
        'canonical_label'         => $family->name,
        'tag_id'                  => $tag_id,
        'tag_label'               => $tag->name,
        'similarity_to_canonical' => 1.0,
        'usage_count'             => 0,
        'entity_label'            => 'O',
    );
    $formats = array( '%d', '%d', '%s', '%d', '%s', '%f', '%d', '%s' );

    $result = $wpdb->replace( $table, $data, $formats );
    if ( false === $result ) {
        wp_send_json_error( array( 'message' => 'Database error while attaching tag to family.' ) );
    }

    wp_send_json_success( array( 'message' => 'Tag attached to family (overlay only).' ) );
}
add_action( 'wp_ajax_semaphore_attach_to_family', 'semaphore_ajax_attach_to_family' );

function semaphore_ajax_detach_from_family() {
    check_ajax_referer( 'semaphore_families_nonce', 'nonce' );
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( array( 'message' => 'Permission denied.' ) );
    }

    $family_id = intval( $_POST['family_id'] ?? 0 );
    $tag_id    = intval( $_POST['tag_id'] ?? 0 );

    if ( ! $family_id || ! $tag_id ) {
        wp_send_json_error( array( 'message' => 'Missing IDs.' ) );
    }

    global $wpdb;
    $table = semaphore_tagfamilies_table();

    $deleted = $wpdb->delete(
        $table,
        array(
            'family_id' => $family_id,
            'tag_id'    => $tag_id,
        ),
        array( '%d', '%d' )
    );

    if ( false === $deleted ) {
        wp_send_json_error( array( 'message' => 'Database error while detaching tag.' ) );
    }

    wp_send_json_success( array( 'message' => 'Tag detached from family (overlay only).' ) );
}
add_action( 'wp_ajax_semaphore_detach_from_family', 'semaphore_ajax_detach_from_family' );

/* --------------------------------------------------------------------------
 * BREADCRUMBS + SCHEMAS + SIDEBAR + FOOTER
 * ----------------------------------------------------------------------- */

function semaphore_breadcrumbs() {
    if ( ! get_option( 'semaphore_enable_breadcrumbs' ) || is_front_page() ) {
        return;
    }

    global $post;

    echo '<div class="entry-breadcrumb"><nav class="bf-breadcrumbs" aria-label="Breadcrumbs">';
    
/*
    echo '<span class="breadcrumb-icon" aria-hidden="true">🏠</span>';
    echo '<span class="breadcrumb-icon" aria-hidden="true">📍</span>';
    echo '<a href="' . esc_url( home_url( '/' ) ) . '">Home</a>';
*/

/*
    echo '<span class="breadcrumb-icon pinpoint" aria-hidden="true">📍</span>';
    echo '<a href="' . esc_url( home_url( '/' ) ) . '" class="breadcrumb-link">Home</a>';
*/

    /*
    echo '<span class="breadcrumb-icon pinpoint" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="#4F1993">
                <circle cx="10" cy="10" r="10" />
            </svg>
          </span>';
    echo '<a href="' . esc_url( home_url( '/' ) ) . '" class="breadcrumb-link">Home</a>';
    */

echo '<span class="breadcrumb-icon"><i class="fas fa-map-marker-alt" style="color: #4F1993;"></i></span>';
    echo '<a href="' . esc_url( home_url( '/' ) ) . '" class="breadcrumb-link">Home</a>';

    echo '<span class="breadcrumb-separator">›</span>';

    if ( is_single() && $post ) {
        $categories = get_the_category( $post->ID );
        if ( ! empty( $categories ) ) {
            $primary = $categories[0];
            echo '<a href="' . esc_url( get_category_link( $primary ) ) . '">' . esc_html( $primary->name ) . '</a>';
            echo '<span class="breadcrumb-separator">›</span>';
        }
        echo '<span class="breadcrumb-current">' . esc_html( get_the_title( $post ) ) . '</span>';
    } elseif ( is_tag() ) {
        $tag = get_queried_object();
        echo '<span class="breadcrumb-current">Tag: ' . esc_html( $tag->name ) . '</span>';
    } elseif ( is_category() ) {
        $cat = get_queried_object();
        echo '<span class="breadcrumb-current">Category: ' . esc_html( $cat->name ) . '</span>';
    } elseif ( is_search() ) {
        echo '<span class="breadcrumb-current">Search: ' . esc_html( get_search_query() ) . '</span>';
    } elseif ( is_page() && $post ) {
        $ancestors = array_reverse( get_post_ancestors( $post ) );
        foreach ( $ancestors as $ancestor_id ) {
            echo '<a href="' . esc_url( get_permalink( $ancestor_id ) ) . '">' . esc_html( get_the_title( $ancestor_id ) ) . '</a>';
            echo '<span class="breadcrumb-separator">›</span>';
        }
        echo '<span class="breadcrumb-current">' . esc_html( get_the_title( $post ) ) . '</span>';
    }

    echo '</nav></div>';
}

function semaphore_breadcrumb_schema() {
    if ( ! get_option( 'semaphore_enable_schema' ) || is_front_page() ) {
        return;
    }

    $item_list = array();
    $position  = 1;

    $item_list[] = array(
        '@type'    => 'ListItem',
        'position' => $position++,
        'name'     => 'Home',
        'item'     => home_url( '/' ),
    );

    if ( is_single() ) {
        global $post;
        if ( ! $post ) {
            return;
        }

        $categories = get_the_category( $post->ID );
        if ( ! empty( $categories ) ) {
            $primary      = $categories[0];
            $item_list[] = array(
                '@type'    => 'ListItem',
                'position' => $position++,
                'name'     => $primary->name,
                'item'     => get_category_link( $primary ),
            );
        }

        $item_list[] = array(
            '@type'    => 'ListItem',
            'position' => $position++,
            'name'     => get_the_title( $post ),
            'item'     => get_permalink( $post ),
        );
    } elseif ( is_tag() ) {
        $tag = get_queried_object();
        if ( ! $tag || is_wp_error( $tag ) ) {
            return;
        }
        $item_list[] = array(
            '@type'    => 'ListItem',
            'position' => $position++,
            'name'     => 'Tag',
            'item'     => get_term_link( $tag ),
        );
        $item_list[] = array(
            '@type'    => 'ListItem',
            'position' => $position++,
            'name'     => $tag->name,
            'item'     => get_term_link( $tag ),
        );
    } elseif ( is_category() ) {
        $cat = get_queried_object();
        if ( ! $cat || is_wp_error( $cat ) ) {
            return;
        }
        $item_list[] = array(
            '@type'    => 'ListItem',
            'position' => $position++,
            'name'     => $cat->name,
            'item'     => get_term_link( $cat ),
        );
    } elseif ( is_page() ) {
        global $post;
        if ( ! $post ) {
            return;
        }
        $ancestors = array_reverse( get_post_ancestors( $post ) );
        foreach ( $ancestors as $ancestor_id ) {
            $item_list[] = array(
                '@type'    => 'ListItem',
                'position' => $position++,
                'name'     => get_the_title( $ancestor_id ),
                'item'     => get_permalink( $ancestor_id ),
            );
        }
        $item_list[] = array(
            '@type'    => 'ListItem',
            'position' => $position++,
            'name'     => get_the_title( $post ),
            'item'     => get_permalink( $post ),
        );
    } else {
        return;
    }

    $data = array(
        '@context'        => 'https://schema.org',
        '@type'           => 'BreadcrumbList',
        'itemListElement' => $item_list,
    );

    echo '<script type="application/ld+json">' . wp_json_encode( $data ) . '</script>' . "\n";
}
add_action( 'wp_head', 'semaphore_breadcrumb_schema' );

function semaphore_tag_archive_schema() {
    if ( ! get_option( 'semaphore_enable_schema' ) || ! is_tag() ) {
        return;
    }

    $tag = get_queried_object();
    if ( ! $tag || is_wp_error( $tag ) ) {
        return;
    }

    $data = array(
        '@context' => 'https://schema.org',
        '@type'    => 'CollectionPage',
        'name'     => single_tag_title( '', false ),
        'url'      => get_term_link( $tag ),
        'about'    => array(
            '@type' => 'Thing',
            'name'  => $tag->name,
        ),
    );

    echo '<script type="application/ld+json">' . wp_json_encode( $data ) . '</script>' . "\n";
}
add_action( 'wp_head', 'semaphore_tag_archive_schema', 20 );

/* SIDEBAR: Zaatar look, first tag with family data, tags unchanged */

function semaphore_semantic_sidebar() {
    if ( ! is_single() || ! get_option( 'semaphore_enable_sidebar' ) ) {
        return;
    }

    global $post, $wpdb;
    ?>
    <div class="semantic-sidebar-widget">

        <?php if ( get_option( 'semaphore_debug' ) ) : ?>
            <div class="bf-debug-box">
                <strong>Debug Info:</strong>
                Post ID: <?php echo (int) $post->ID; ?><br>
                semaphore_get_related_posts exists: <?php echo function_exists( 'semaphore_get_related_posts' ) ? 'Yes' : 'No'; ?><br>
                semaphore_get_related_tags exists: <?php echo function_exists( 'semaphore_get_related_tags' ) ? 'Yes' : 'No'; ?><br>
                <?php
                $tags = get_the_tags( $post->ID );
                echo 'Post has tags: ' . ( $tags ? 'Yes (' . count( $tags ) . ')' : 'No' ) . '<br>';

                if ( $tags ) {
                    echo 'First tag ID: ' . (int) $tags[0]->term_id . ' (' . esc_html( $tags[0]->name ) . ')<br>';
                }

                $db_count = $wpdb->get_var(
                    $wpdb->prepare(
                        "SELECT COUNT(*) FROM {$wpdb->prefix}related_posts_embeddings WHERE post_id = %d",
                        $post->ID
                    )
                );
                echo 'Related posts in DB for this post: ' . ( $db_count ? (int) $db_count : 0 ) . '<br>';

                if ( $tags ) {
                    $any_has_family = false;
                    foreach ( $tags as $t ) {
                        $tag_db_count = $wpdb->get_var(
                            $wpdb->prepare(
                                "SELECT COUNT(*) FROM {$wpdb->prefix}tag_families WHERE tag_id = %d",
                                $t->term_id
                            )
                        );
                        if ( $tag_db_count ) {
                            $any_has_family = true;
                            break;
                        }
                    }
                    echo 'Any tag has family data: ' . ( $any_has_family ? 'Yes' : 'No' ) . '<br>';
                }
                ?>
            </div>
        <?php endif; ?>

        <?php
        $related_posts = function_exists( 'semaphore_get_related_posts' ) ? semaphore_get_related_posts( $post->ID, 5 ) : array();
        if ( ! empty( $related_posts ) ) :
        ?>
            <div class="related-posts-section">
                <!-- SIDEBAR Related Posts made with IA  -->
                <h3>Related Posts</h3>
                <ul>
                    <?php foreach ( $related_posts as $rp ) : ?>
                        <li>
                            <a href="<?php echo esc_url( $rp['permalink'] ); ?>">
                                <?php echo esc_html( $rp['title'] ); ?>
                            </a>
                        </li>
                    <?php endforeach; ?>
                </ul>
            </div>
        <?php elseif ( get_option( 'semaphore_debug' ) ) : ?>
            <div class="bf-info-box">
                <strong>Related Posts</strong>
                No related posts found in DB for this post.
            </div>
        <?php endif; ?>

        <?php
        $tags = get_the_tags( $post->ID );
        if ( $tags ) {
            // Find first tag that has overlay family data.
            $family_entry_tag = null;
            foreach ( $tags as $t ) {
                $has_family_data = $wpdb->get_var(
                    $wpdb->prepare(
                        "SELECT COUNT(*) FROM {$wpdb->prefix}tag_families WHERE tag_id = %d",
                        $t->term_id
                    )
                );
                if ( $has_family_data ) {
                    $family_entry_tag = $t;
                    break;
                }
            }

            if ( $family_entry_tag ) {
                $related_tags = function_exists( 'semaphore_get_related_tags' )
                    ? semaphore_get_related_tags( $family_entry_tag->term_id, 12 )
                    : array();

                if ( ! empty( $related_tags ) ) :
                    ?>
                    <div class="related-tags-section">
                        <!-- SIDEBAR Related Tags made with IA -->
                        <h4>Related Tags</h4>
                        <div class="tag-cloud">
                            <?php foreach ( $related_tags as $rt ) : ?>
                                <a class="tag-badge" href="<?php echo esc_url( $rt['link'] ); ?>">
                                    <?php echo esc_html( $rt['name'] ); ?>
                                </a>
                            <?php endforeach; ?>
                        </div>
                    </div>
                    <?php
                elseif ( get_option( 'semaphore_debug' ) ) :
                    ?>
                    <div class="bf-info-box">
                        <strong>Related Tags</strong>
                        No tag family members found for overlay cluster.
                    </div>
                    <?php
                endif;
            } elseif ( get_option( 'semaphore_debug' ) ) {
                ?>
                <div class="bf-info-box">
                    <strong>Related Tags</strong>
                    No tag families found for any tag on this post.
                </div>
                <?php
            }
        } elseif ( get_option( 'semaphore_debug' ) ) {
            ?>
            <div class="bf-info-box">
                <strong>Tags</strong>
                Post has no tags.
            </div>
            <?php
        }
        ?>
    </div>
    <?php
}

function semaphore_sidebar_shortcode() {
    if ( ! get_option( 'semaphore_enable_sidebar' ) ) {
        return '';
    }
    ob_start();
    semaphore_semantic_sidebar();
    return ob_get_clean();
}
add_shortcode( 'semaphore_sidebar', 'semaphore_sidebar_shortcode' );

class Semaphore_Semantic_Sidebar_Widget extends WP_Widget {
    public function __construct() {
        parent::__construct(
            'semaphore_semantic_sidebar_widget',
            'Semaphore Sidebar',
            array( 'description' => 'Shows related posts and tags using embeddings-based data (tags overlayed by families but not changed).' )
        );
    }

    public function widget( $args, $instance ) {
        if ( ! get_option( 'semaphore_enable_sidebar' ) ) {
            return;
        }
        echo $args['before_widget'];
        semaphore_semantic_sidebar();
        echo $args['after_widget'];
    }

    public function form( $instance ) {
        echo '<p>This widget automatically shows semantic related content on single posts. It does not modify post tags.</p>';
    }
}

function semaphore_register_sidebar_widget() {
    register_widget( 'Semaphore_Semantic_Sidebar_Widget' );
}
add_action( 'widgets_init', 'semaphore_register_sidebar_widget' );

/* FOOTER RELATED CONTENT: use grid + inline tags, tags unchanged */

function semaphore_render_footer_related() {
    if ( ! is_single() || ! is_main_query() ) {
        return;
    }
    if ( is_admin() || doing_action( 'rest_api_init' ) || wp_is_json_request() ) {
        return;
    }
    if ( ! get_option( 'semaphore_enable_footer' ) ) {
        return;
    }

    global $post, $wpdb;
    if ( ! $post instanceof WP_Post ) {
        return;
    }

    static $done = false;
    if ( $done ) {
        return;
    }
    $done = true;

    $html = '';

    $related_posts = function_exists( 'semaphore_get_related_posts' ) ? 

    // Set the number of related post
    // semaphore_get_related_posts( $post->ID, 3 ) : array();
    // semaphore_get_related_posts( $post->ID, 2 ) : array();
    semaphore_get_related_posts( $post->ID, 4 ) : array();

    if ( ! empty( $related_posts ) ) {
        $html .= '<!-- SUBFOOTER Explore Related Posts made with IA -->';
        $html .= '<h3>Explore Related Posts</h3>';
        $html .= '<div class="related-posts-grid">';
        foreach ( $related_posts as $rp ) {
            if ( empty( $rp['permalink'] ) || empty( $rp['title'] ) ) {
                continue;
            }
            $html .= '<article class="related-post-card">';
            if ( ! empty( $rp['thumbnail'] ) ) {
                $html .= '<img src="' . esc_url( $rp['thumbnail'] ) . '" alt="' . esc_attr( $rp['title'] ) . '">';
            }
            $html .= '<div class="card-content">';
            $html .= '<h4><a href="' . esc_url( $rp['permalink'] ) . '">' . esc_html( $rp['title'] ) . '</a></h4>';
            if ( ! empty( $rp['excerpt'] ) ) {
                $html .= '<p>' . esc_html( wp_trim_words( $rp['excerpt'], 20 ) ) . '</p>';
            }
            $html .= '</div></article>';
        }
        $html .= '</div>';
    }

    $tags = get_the_tags( $post->ID );
    if ( $tags ) {
        // Find first tag that has overlay family data.
        $family_entry_tag = null;
        foreach ( $tags as $t ) {
            $has_family_data = $wpdb->get_var(
                $wpdb->prepare(
                    "SELECT COUNT(*) FROM {$wpdb->prefix}tag_families WHERE tag_id = %d",
                    $t->term_id
                )
            );
            if ( $has_family_data ) {
                $family_entry_tag = $t;
                break;
            }
        }

        if ( $family_entry_tag ) {
            $related_tags = function_exists( 'semaphore_get_related_tags' )
                ? semaphore_get_related_tags( $family_entry_tag->term_id, 12 )
                : array();

            if ( ! empty( $related_tags ) && is_array( $related_tags ) ) {
                $html .= '<div class="related-tags-section">';
                $html .= '<!-- SUBFOOTER Explore Related Tags made by IA -->';
                $html .= '<h4>Explore Related Tags</h4>';
                $html .= '<div class="tag-cloud">';
                foreach ( $related_tags as $rt ) {
                    if ( empty( $rt['link'] ) || empty( $rt['name'] ) ) {
                        continue;
                    }
                    $html .= '<a class="inline-tag" href="' . esc_url( $rt['link'] ) . '">' . esc_html( $rt['name'] ) . '</a>';
                }
                $html .= '</div>';
                // $html .= '<p class="bf-text-small bf-text-muted bf-mt-10">Cluster entry tag: <span class="bf-text-bold">'. esc_html( $family_entry_tag->name ) . '</span> (overlay only).</p>';
                $html .= '</div>';
            }
        }
    }

    if ( $html ) {
        echo '<div class="bf-post-footer">' . $html . '</div>';
    }
}
/* 
Disable injection in footer, use related-posts.php to inject the module in theme
*/
// add_action( 'wp_footer', 'semaphore_render_footer_related', 20 );

```

- semaphore-families-manager.js
```javacript
/**
 * Plugin Name: Semaphore
 * Description: Semantic clustering plugin (related posts, tag families, sidebar, breadcrumbs & schemas).
 * Version: 1.2.0
 * Author: Bruno Flaven & IA
 * Text Domain: semaphore
 */

jQuery(function ($) {
    'use strict';

    if (typeof semaphoreDashboard === 'undefined') {
        console.error('semaphoreDashboard is not defined – check wp_localize_script.');
        return;
    }

    var state = {
        selectedTagId: null,
        selectedFamilyId: null,
        selectedMemberTagId: null,
        tagsPaged: 1,
        tagsPerPage: 50,
        tagsSearch: '',
        familiesSearch: '',
        families: []
    };

    var $tagsTable    = $('#semaphore-all-tags-table');
    var $familiesList = $('#semaphore-families-list');
    var $membersList  = $('#semaphore-family-members');

    var $btnConvert = $('#semaphore-convert-to-family');
    var $btnAttach  = $('#semaphore-attach-to-family');
    var $btnDetach  = $('#semaphore-detach-from-family');

    var $inputTagSearch    = $('#semaphore-tag-search');
    var $inputFamilySearch = $('#semaphore-family-search');

    function escapeHtml(str) {
        if (str == null) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function ajaxError(jqXHR, textStatus, errorThrown) {
        alert('Network error: ' + (errorThrown || textStatus));
        console.error('Semaphore dashboard error:', jqXHR, textStatus, errorThrown);
    }

    function updateButtons() {
        $btnConvert.prop('disabled', !state.selectedTagId);
        $btnAttach.prop('disabled', !(state.selectedTagId && state.selectedFamilyId));
        $btnDetach.prop('disabled', !(state.selectedFamilyId && state.selectedMemberTagId));
    }

    /* Tags list */

    function renderTags(data) {
        var rows    = data.rows || [];
        var total   = data.total || 0;
        var perPage = data.per_page || state.tagsPerPage;
        var paged   = data.paged || state.tagsPaged;
        var maxPage = Math.max(1, Math.ceil(total / perPage));

        var html = '<table class="widefat fixed striped"><thead><tr>' +
            '<th style="width:70px;">ID</th>' +
            '<th>Tag</th>' +
            '<th style="width:80px;">Posts</th>' +
            '</tr></thead><tbody>';

        if (!rows.length) {
            html += '<tr><td colspan="3"><em>No tags found.</em></td></tr>';
        } else {
            rows.forEach(function (r) {
                var active = (r.term_id === state.selectedTagId) ? ' active' : '';
                html += '<tr class="semaphore-tag-row' + active + '" data-id="' + r.term_id + '">' +
                    '<td>#' + r.term_id + '</td>' +
                    '<td>' + escapeHtml(r.name) + '</td>' +
                    '<td>' + (r.count || 0) + '</td>' +
                    '</tr>';
            });
        }

        html += '</tbody></table>';

        html += '<div class="tablenav"><div class="tablenav-pages">' +
            '<span class="displaying-num">' + total + ' items</span> ';

        if (maxPage > 1) {
            var prevDisabled = (paged <= 1) ? ' disabled' : '';
            var nextDisabled = (paged >= maxPage) ? ' disabled' : '';
            html += '<span class="pagination-links">' +
                '<a href="#" class="first-page' + prevDisabled + '" data-page="1">«</a>' +
                '<a href="#" class="prev-page' + prevDisabled + '" data-page="' + (paged - 1) + '">‹</a>' +
                '<span class="paging-input">' + paged + ' of <span class="total-pages">' + maxPage + '</span></span>' +
                '<a href="#" class="next-page' + nextDisabled + '" data-page="' + (paged + 1) + '">›</a>' +
                '<a href="#" class="last-page' + nextDisabled + '" data-page="' + maxPage + '">»</a>' +
                '</span>';
        }

        html += '</div></div>';
        $tagsTable.html(html);
    }

    function loadTags() {
        $.ajax({
            url: semaphoreDashboard.ajax_url,
            data: {
                action:   'semaphore_list_tags',
                nonce:    semaphoreDashboard.nonce,
                paged:    state.tagsPaged,
                per_page: state.tagsPerPage,
                search:   state.tagsSearch
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error loading tags.');
                return;
            }
            renderTags(res.data || {});
        }).fail(ajaxError);
    }

    /* Families */

    function renderFamilies() {
        var list = state.families || [];

        if (state.familiesSearch) {
            var q = state.familiesSearch.toLowerCase();
            list = list.filter(function (f) {
                var idMatch  = String(f.family_id).indexOf(q) !== -1;
                var lblMatch = (f.canonical_label || '').toLowerCase().indexOf(q) !== -1;
                return idMatch || lblMatch;
            });
        }

        var html = '<table class="widefat fixed striped"><thead><tr>' +
            '<th style="width:70px;">Family ID</th>' +
            '<th>Canonical label</th>' +
            '<th style="width:80px;">Members</th>' +
            '</tr></thead><tbody>';

        if (!list.length) {
            html += '<tr><td colspan="3"><em>No families found.</em></td></tr>';
        } else {
            list.forEach(function (f) {
                var active = (f.family_id === state.selectedFamilyId) ? ' active' : '';
                html += '<tr class="semaphore-family-row' + active + '" data-family-id="' + f.family_id + '">' +
                    '<td>#' + f.family_id + '</td>' +
                    '<td>' + escapeHtml(f.canonical_label || '') + '</td>' +
                    '<td>' + (f.members || 0) + '</td>' +
                    '</tr>';
            });
        }

        html += '</tbody></table>';
        $familiesList.html(html);
    }

    function loadFamilies(keepSelection) {
        $.ajax({
            url: semaphoreDashboard.ajax_url,
            data: {
                action: 'semaphore_list_families',
                nonce:  semaphoreDashboard.nonce
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error loading families.');
                return;
            }
            state.families = (res.data && res.data.families) || [];
            if (!keepSelection) {
                state.selectedFamilyId     = null;
                state.selectedMemberTagId  = null;
            }
            renderFamilies();
            if (state.selectedFamilyId) {
                loadMembers();
            } else {
                renderMembers([]);
            }
        }).fail(ajaxError);
    }

    /* Members */

    function renderMembers(list) {
        list = list || [];
        state.selectedMemberTagId = null;

        var html = '<table class="widefat fixed striped"><thead><tr>' +
            '<th style="width:70px;">Tag ID</th>' +
            '<th>Tag label</th>' +
            '<th style="width:80px;">Usage</th>' +
            '</tr></thead><tbody>';

        if (!list.length) {
            html += '<tr><td colspan="3"><em>No members in this family.</em></td></tr>';
        } else {
            list.forEach(function (m) {
                var active = (m.tag_id === state.selectedMemberTagId) ? ' active' : '';
                html += '<tr class="semaphore-member-row' + active + '" data-tag-id="' + m.tag_id + '">' +
                    '<td>#' + m.tag_id + '</td>' +
                    '<td>' + escapeHtml(m.taglabel || '') + '</td>' +
                    '<td>' + (m.usage_count || 0) + '</td>' +
                    '</tr>';
            });
        }

        html += '</tbody></table>';
        $membersList.html(html);
        updateButtons();
    }

    function loadMembers() {
        if (!state.selectedFamilyId) {
            renderMembers([]);
            return;
        }

        $.ajax({
            url: semaphoreDashboard.ajax_url,
            data: {
                action:    'semaphore_list_family_members',
                nonce:     semaphoreDashboard.nonce,
                family_id: state.selectedFamilyId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error loading members.');
                return;
            }
            renderMembers((res.data && res.data.members) || []);
        }).fail(ajaxError);
    }

    /* Selection handlers */

    $tagsTable.on('click', '.semaphore-tag-row', function () {
        var id = parseInt($(this).data('id'), 10) || 0;
        if (state.selectedTagId === id) {
            state.selectedTagId = null;
            $tagsTable.find('.semaphore-tag-row').removeClass('active');
        } else {
            state.selectedTagId = id;
            $tagsTable.find('.semaphore-tag-row').removeClass('active');
            $(this).addClass('active');
        }
        updateButtons();
    });

    $familiesList.on('click', '.semaphore-family-row', function () {
        var id = parseInt($(this).data('family-id'), 10) || 0;
        if (state.selectedFamilyId === id) {
            state.selectedFamilyId = null;
            $familiesList.find('.semaphore-family-row').removeClass('active');
            renderMembers([]);
        } else {
            state.selectedFamilyId = id;
            $familiesList.find('.semaphore-family-row').removeClass('active');
            $(this).addClass('active');
            loadMembers();
        }
        updateButtons();
    });

    $membersList.on('click', '.semaphore-member-row', function () {
        var id = parseInt($(this).data('tag-id'), 10) || 0;
        if (state.selectedMemberTagId === id) {
            state.selectedMemberTagId = null;
            $membersList.find('.semaphore-member-row').removeClass('active');
        } else {
            state.selectedMemberTagId = id;
            $membersList.find('.semaphore-member-row').removeClass('active');
            $(this).addClass('active');
        }
        updateButtons();
    });

    $tagsTable.on('click', '.tablenav-pages a', function (e) {
        e.preventDefault();
        var $a = $(this);
        if ($a.hasClass('disabled')) return;
        var page = parseInt($a.data('page'), 10) || 1;
        state.tagsPaged = page;
        loadTags();
    });

    /* Search fields */

    var tagTimer = null;
    $inputTagSearch.on('keyup', function () {
        state.tagsSearch = $(this).val();
        state.tagsPaged  = 1;
        if (tagTimer) clearTimeout(tagTimer);
        tagTimer = setTimeout(loadTags, 250);
    });

    var famTimer = null;
    $inputFamilySearch.on('keyup', function () {
        state.familiesSearch = $(this).val();
        if (famTimer) clearTimeout(famTimer);
        famTimer = setTimeout(renderFamilies, 150);
    });

    /* Actions */

    $btnConvert.on('click', function (e) {
        e.preventDefault();
        if (!state.selectedTagId) return;

        if (!window.confirm('Convert this tag into a family (canonical) in the overlay table?')) return;

        $.ajax({
            type: 'POST',
            url:  semaphoreDashboard.ajax_url,
            data: {
                action: 'semaphore_convert_to_family',
                nonce:  semaphoreDashboard.nonce,
                tag_id: state.selectedTagId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error converting tag to family.');
                return;
            }
            loadFamilies(true);
        }).fail(ajaxError);
    });

    $btnAttach.on('click', function (e) {
        e.preventDefault();
        if (!state.selectedTagId || !state.selectedFamilyId) return;

        $.ajax({
            type: 'POST',
            url:  semaphoreDashboard.ajax_url,
            data: {
                action:    'semaphore_attach_to_family',
                nonce:     semaphoreDashboard.nonce,
                family_id: state.selectedFamilyId,
                tag_id:    state.selectedTagId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error attaching tag to family.');
                return;
            }
            loadMembers();
            loadFamilies(true);
        }).fail(ajaxError);
    });

    $btnDetach.on('click', function (e) {
        e.preventDefault();
        if (!state.selectedFamilyId || !state.selectedMemberTagId) return;

        if (!window.confirm('Detach this tag from the current family in the overlay table?')) return;

        $.ajax({
            type: 'POST',
            url:  semaphoreDashboard.ajax_url,
            data: {
                action:    'semaphore_detach_from_family',
                nonce:     semaphoreDashboard.nonce,
                family_id: state.selectedFamilyId,
                tag_id:    state.selectedMemberTagId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error detaching tag from family.');
                return;
            }
            loadMembers();
            loadFamilies(true);
        }).fail(ajaxError);
    });

    /* Help panel toggle */
    var $helpToggle = jQuery('.semaphore-help-toggle');
    var $helpPanel  = jQuery('#semaphore-help-panel');

    $helpToggle.on('click', function () {
        var expanded = $helpToggle.attr('aria-expanded') === 'true';
        expanded = !expanded;
        $helpToggle.attr('aria-expanded', expanded ? 'true' : 'false');
        $helpToggle.text(expanded ? 'Hide help' : 'Show help');

        if (expanded) {
            $helpPanel.removeAttr('hidden');
        } else {
            $helpPanel.attr('hidden', 'hidden');
        }
    });


    /* Init */

    updateButtons();
    loadTags();
    loadFamilies(false);
});


```
