
Let work on the look and feel for good.

## PROMPT_8
Can you rewrite the all plugin in that sense so I can only have to cut and paste, keep the rest as it is if it is not necessary to change.




## PROMPT_7

I know what the problem I am facing is. I have two issues that are confronting.
First, I want to preserve my old post tags visible on my post because that was my SEO effort. Second I want to introduce this new semantic clustering it comes may with tradeoff.
For instance, let’s pretend I have made a post with
A list of numerous post tags e.g agentic browsers, AI, AI agents, Anthropic, artificial intelligence, Atlas, Automate, Comet, dbt, digital autonomy, digital sovereignty, digital transformation, DuckDB, GDPR, GEO, Google Chrome, innovation theater, late-stage capitalism, natural search, OpenAI, organizational pathologies, Perplexity, personal data, privacy, Product Owner, semantic layer, SEO, surveillance, taxonomies 

A list of numerous family tags DuckDB (tag_family_1), Automate (tag_family_2) …. etc, 
For the moment, I need to remove all the post tags and keep only one family tag to have “Tag family data in DB for first tag: Yes” . That sucks.
I want the better of the two worlds for the ùoment the traditional SEO with keywords and the new seo with clustering semantics with family tags? 










## PROMPT_6

Yes but when I disable it I do not see the family table filter so maybe keep it as it is for the moment. It seems to work partially. 
But I have no more color when I select tags or tag families that are not a good UX too.
When i attach a tag to a family, I do not see the tag label in the table Family Members









## PROMPT_5
Changing semaphore-families-manager.js now I do not see anything on the semaphore-dashboard page and no actions is possible as tags an tags families have completely disappeared.






## PROMPT_4

On the front, everything is OK but on the backend that is the mess.
I want a change in the plugin, I have multiple and severe issues on the semaphore-dashboard page. 

- On the semaphore-dashboard page, it is impossible to select a tag or a family tag and then to unselect. JS issue ?


- On the semaphore-dashboard page, like you did for tags, you have added a search box that enables the search on tags. I want the same thing for tag families, enable a search box to search by ID, label on Tag Families. 

- On the semaphore-dashboard page, the button "Attach selected tag to current family" does not work when I have selected a tag on the left (post tag) and a family tag on the right. Both fields are in green. I got a js popup with network error.

- On the semaphore-dashboard page, I was unable to use the button "Detach selected member from current family".

Can you fix these multiple issue and make the semaphore-dashboard page working properly as expected



semaphore-families-manager.js


## PROMPT_3

I have reinstalled from scratch and reactivated one after the other feature and  none of the features of the plugin is available. See the mist below, can you fix this.

Debug mode : Enable debug blocks in semantic sidebar.
Semantic Sidebar: Enable semantic sidebar widget / shortcode.
Footer Related Content: Append related posts/tags after post content.
Breadcrumbs: Enable semantic breadcrumbs functions.
Schema.org JSON-LD: Output breadcrumb & tag archive schemas in <head>



The settings UI is there, but none of the switches do anything yet because the underlying feature code still checks the old option names and hooks; we need to finish that rename/wiring.

### 1. Fix the option names in feature checks

In your old plugin, all features used `bf_sem_seo_*` options (e.g. `bfsemseo_enable_sidebar`). Now the settings page saves `semaphore_enable_sidebar`, `semaphore_enable_footer`, etc., but the feature functions I left commented still use the old option keys or are not hooked. You must: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)

1. Ensure every feature function exists in `semaphore.php`.
2. Replace each `get_option( 'bfsemseo_enable_...' )` call with the new keys:
   - `bfsemseo_enable_sidebar` → `semaphore_enable_sidebar`
   - `bfsemseo_enable_footer` → `semaphore_enable_footer`
   - `bfsemseo_enable_breadcrumbs` → `semaphore_enable_breadcrumbs`
   - `bfsemseo_enable_schema` → `semaphore_enable_schema` [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)

For example, in the **sidebar** function you paste from the old plugin, change:

```php
if ( ! get_option( 'bfsemseo_enable_sidebar' ) ) {
    return;
}
```

to:

```php
if ( ! get_option( 'semaphore_enable_sidebar' ) ) {
    return;
}
```

Do the same for footer, breadcrumbs, and schema functions.

### 2. Re‑add and hook the SEO feature functions

From your old file (`CHUNK3` in paste.txt) you need to copy these functions into `semaphore.php`, below the “SEO FEATURES” comment I left:

- `bf_semantic_breadcrumbs` (rename to `semaphore_semantic_breadcrumbs` or keep old name but update options). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)
- `bf_breadcrumb_schema` (rename to `semaphore_breadcrumb_schema` – already present – just ensure the option name is `semaphore_enable_schema`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)
- `bf_tag_archive_schema` (already present as `semaphore_tag_archive_schema`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)
- `bf_semantic_sidebar` + `bf_semantic_sidebar_shortcode` + `BF_Semantic_Sidebar_Widget` + `bf_register_semantic_sidebar_widget`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)
- `bf_semseo_render_footer_related` hook on `wp_footer`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)

When you paste them, make these exact edits:

1. Sidebar:

```php
function semaphore_semantic_sidebar() {
    if ( ! is_single() ) {
        if ( get_option( 'semaphore_debug' ) ) {
            // debug block...
        }
        return;
    }

    if ( ! get_option( 'semaphore_enable_sidebar' ) ) {
        return;
    }

    // rest of bf_semantic_sidebar body unchanged
}
```

Then:

```php
function semaphore_semantic_sidebar_shortcode( $atts ) {
    if ( ! get_option( 'semaphore_enable_sidebar' ) ) {
        return '';
    }
    ob_start();
    semaphore_semantic_sidebar();
    return ob_get_clean();
}
add_shortcode( 'bf_sidebar', 'semaphore_semantic_sidebar_shortcode' );
```

And in the widget class, inside `widget()`:

```php
if ( ! get_option( 'semaphore_enable_sidebar' ) ) {
    return;
}
echo $args['before_widget'];
semaphore_semantic_sidebar();
echo $args['after_widget'];
```

2. Footer related content:

Paste `bf_semseo_render_footer_related` from CHUNK3 and rename + update option: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)

```php
function semaphore_render_footer_related() {
    if ( ! is_single() || ! is_main_query() ) {
        return;
    }
    // same WP-Admin / REST guards as original

    if ( ! get_option( 'semaphore_enable_footer' ) ) {
        return;
    }

    // body stays the same (uses bf_get_related_posts / bf_get_related_tags)
}
add_action( 'wp_footer', 'semaphore_render_footer_related', 20 );
```

3. Breadcrumbs:

You already have `semaphore_semantic_breadcrumbs()` and `semaphore_breadcrumb_schema()` in the new file, both using the new options, so just **call** them from your theme where needed:

```php
<?php if ( function_exists( 'semaphore_semantic_breadcrumbs' ) ) {
    semaphore_semantic_breadcrumbs();
} ?>
```

Schema functions are already hooked to `wp_head` with the new option. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)

### 3. Ensure the debug option is used

In the old semantic sidebar/widget you had debug blocks checking `bfsemseo_debug`. In the pasted code, change that to: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)

```php
if ( get_option( 'semaphore_debug' ) ) {
    // existing debug HTML
}
```

Use this in:

- `semaphore_semantic_sidebar()` debug box.
- `semaphore_render_footer_related()` debug messages when nothing is found. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7993663/a949a1a5-fe16-4188-bbb9-bee1905d50ca/paste.txt)

### 4. Quick checklist after edits

After you paste and adjust:

- Reactivate the plugin.
- In Settings → Semaphore:
  - Tick “Semantic Sidebar” and “Footer Related Content”.
  - Tick “Breadcrumbs” and “Schema.org JSON‑LD”.
- Visit a single post:
  - Sidebar: add `[bf_sidebar]` in a widget or post to see the semantic block.
  - Footer: related posts/tags block at bottom.
  - Breadcrumbs: call `semaphore_semantic_breadcrumbs()` in your theme.
  - JSON‑LD: view source, search for `BreadcrumbList` and `CollectionPage` scripts.

If you send me your current `semaphore.php` as it is now, I can give you an exact, ready‑to‑paste block with all these functions already renamed and wired.


## PROMPT_2
Can you perform one after the other so I just have to cut and paste the code after the STEP_1 and then do after STEP_2. Your proposal to treat chunks was useful as I can progress at the same time you and you do the job of coding.
STEP_1 : Move your existing “related posts” and “SEO features” blocks into this file, updating option names and menu slugs where noted.

STEP_2 : Create semaphore-families-manager.js to call the AJAX actions (semaphore_list_tags, semaphore_list_families, etc.) and render tables with pagination/search; you can wire it to something like DataTables or your own minimal UI.







## PROMPT_1
As a WordPress expert, rewrite the plugin code but changed do the following changes:
- The plugin name is Semaphore, use this name fo the pages for the plugin
- Remove the tag families management from the page tag edition and migrate into a page for the plugin as I want to manage the tag families. 
- On this  tag families management page, I should be able to have a list of all existing tags , think of an ergonomy that enables me to list 3000 tags for instance.
- On this  tag families management page, I should be able to have a list of all the family tags to convert post tags into tag families then attach post tags to this new tag family or canonical. I should also be able to send tag families as regular tags.
For each family tag I should be able to add or remove tags attached to these family tags.

In a sense, the main objective of this page it is to enable more accurate control on the tag family management with a page that works


- bf-semantic-seo.php
```php
<?php
/**
 * Plugin Name: BF Semantic SEO Suite
 * Description: All-in-one semantic clustering plugin (related posts, tag families, sidebar, breadcrumbs & schemas).
 * Version: 1.0.0
 * Author: Bruno Flaven & IA
 * Text Domain: bf-semantic-seo
 */

/* ####################### // CHUNK_1 #######################  */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'BF_SEM_SEO_VERSION', '1.0.0' );

/**
 * ACTIVATION: create tables + defaults.
 */
function bf_sem_seo_activate() {
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

    // Tag families table.
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

    // Options defaults.
    add_option( 'bf_sem_seo_debug', 0 );
    add_option( 'bf_sem_seo_enable_sidebar', 1 );
    add_option( 'bf_sem_seo_enable_footer', 1 );
    add_option( 'bf_sem_seo_enable_breadcrumbs', 1 );
    add_option( 'bf_sem_seo_enable_schema', 1 );

    set_transient( 'bf_sem_seo_activation_notice', true, 30 );
}
register_activation_hook( __FILE__, 'bf_sem_seo_activate' );

/**
 * UNINSTALL: drop tables + options + term meta.
 */
function bf_sem_seo_uninstall() {
    global $wpdb;

    $wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}related_posts_embeddings`" );
    $wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}tag_families`" );

    delete_option( 'bf_sem_seo_debug' );
    delete_option( 'bf_sem_seo_enable_sidebar' );
    delete_option( 'bf_sem_seo_enable_footer' );
    delete_option( 'bf_sem_seo_enable_breadcrumbs' );
    delete_option( 'bf_sem_seo_enable_schema' );

    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_selection'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_mode_active'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_order'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = 'bf_is_family_tag'" );
}
register_uninstall_hook( __FILE__, 'bf_sem_seo_uninstall' );

/**
 * Activation notice.
 */
function bf_sem_seo_activation_notice() {
    if ( get_transient( 'bf_sem_seo_activation_notice' ) ) {
        delete_transient( 'bf_sem_seo_activation_notice' );
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p><strong>BF Semantic SEO Suite:</strong> Tables created. Go to Settings → BF Semantic SEO to import CSV and configure options.</p>';
        echo '</div>';
    }
}
add_action( 'admin_notices', 'bf_sem_seo_activation_notice' );

/* -------------------------------------------------------------------------
 * SETTINGS PAGE (global toggles)
 * ------------------------------------------------------------------------- */

function bf_sem_seo_register_settings() {
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_debug', array( 'type' => 'boolean', 'default' => 0 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_sidebar', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_footer', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_breadcrumbs', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_schema', array( 'type' => 'boolean', 'default' => 1 ) );
}
add_action( 'admin_init', 'bf_sem_seo_register_settings' );

function bf_sem_seo_admin_menu() {
    // Main settings + Help.
    add_options_page(
        'BF Semantic SEO',
        'BF Semantic SEO',
        'manage_options',
        'bf-sem-seo',
        'bf_sem_seo_render_settings_page'
    );

    // CSV pages re-used as subpages in Settings for familiarity.
    add_submenu_page(
        'options-general.php',
        'Related Embeddings',
        'Related Embeddings',
        'manage_options',
        'bf-sem-seo-related',
        'bf_re_emb_render_settings_page'
    );

    add_submenu_page(
        'options-general.php',
        'Tag Families',
        'Tag Families',
        'manage_options',
        'bf-sem-seo-families',
        'bf_tf_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_sem_seo_admin_menu' );

function bf_sem_seo_render_settings_page() {
    ?>
    <div class="wrap">
        <h1>BF Semantic SEO Suite</h1>

        <form method="post" action="options.php">
            <?php settings_fields( 'bf_sem_seo_settings' ); ?>

            <h2>Features</h2>
            <table class="form-table">
                <tr>
                    <th scope="row">Debug mode</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_debug" value="1" <?php checked( get_option( 'bf_sem_seo_debug' ), 1 ); ?>>
                            Enable debug blocks in semantic sidebar.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Semantic Sidebar</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_sidebar" value="1" <?php checked( get_option( 'bf_sem_seo_enable_sidebar' ), 1 ); ?>>
                            Enable semantic sidebar widget / shortcode.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Footer Related Content</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_footer" value="1" <?php checked( get_option( 'bf_sem_seo_enable_footer' ), 1 ); ?>>
                            Append related posts/tags after post content.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Breadcrumbs</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_breadcrumbs" value="1" <?php checked( get_option( 'bf_sem_seo_enable_breadcrumbs' ), 1 ); ?>>
                            Enable semantic breadcrumbs functions.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Schema.org JSON-LD</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_schema" value="1" <?php checked( get_option( 'bf_sem_seo_enable_schema' ), 1 ); ?>>
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
            <li>Import CSVs via Settings → Related Embeddings / Tag Families.</li>
            <li>Use shortcodes <code>[bf_related_posts]</code>, <code>[bf_related_tags]</code>, <code>[bf_sidebar]</code> where needed.</li>
        </ul>

        <h3>Uninstall</h3>
        <ul>
            <li>Delete the plugin from Plugins page.</li>
            <li>Tables <code>wp_related_posts_embeddings</code> and <code>wp_tag_families</code> are dropped.</li>
            <li>Options and custom term meta created by this plugin are removed.</li>
        </ul>

        <h3>Public APIs</h3>
        <ul>
            <li><code>bf_get_related_posts( $post_id, $limit )</code></li>
            <li><code>bf_get_related_tags( $tag_id, $limit )</code></li>
        </ul>
    </div>
    <?php
}

/* -------------------------------------------------------------------------
 * RELATED POSTS (CSV + meta box + shortcode)
 * ------------------------------------------------------------------------- */

function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}

/**
 * Get related posts, same logic as original DB plugin.
 */
function bf_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;
    $table_name = bf_re_emb_table_name();

    $custom_order = get_post_meta( $post_id, '_bf_custom_related_order', true );

    if ( ! empty( $custom_order ) && is_array( $custom_order ) ) {
        $out  = array();
        $rank = 1;

        foreach ( $custom_order as $related_id ) {
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
 * Save related posts from meta box.
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

    if ( isset( $_POST['bf_full_reset'] ) && $_POST['bf_full_reset'] === '1' ) {
        delete_post_meta( $post_id, '_bf_custom_related_selection' );
        delete_post_meta( $post_id, '_bf_custom_mode_active' );
        delete_post_meta( $post_id, '_bf_custom_related_order' );
        return;
    }

    $is_custom = isset( $_POST['bf_custom_selection'] ) && $_POST['bf_custom_selection'] === '1';

    if ( $is_custom ) {
        $selected_ids = isset( $_POST['bf_selected_ids'] ) ? json_decode( stripslashes( $_POST['bf_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );

        $ordered_ids = isset( $_POST['bf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $ordered_selected = array_values( array_intersect( $ordered_ids, $selected_ids ) );

        update_post_meta( $post_id, '_bf_custom_related_selection', $selected_ids );
        update_post_meta( $post_id, '_bf_custom_related_order', $ordered_selected );
        update_post_meta( $post_id, '_bf_custom_mode_active', '1' );
    } else {
        delete_post_meta( $post_id, '_bf_custom_related_selection' );
        delete_post_meta( $post_id, '_bf_custom_mode_active' );
        delete_post_meta( $post_id, '_bf_custom_related_order' );

        $ordered_ids = isset( $_POST['bf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $wpdb->delete( $table_name, array( 'post_id' => $post_id ), array( '%d' ) );

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
 * Meta box: manage related posts (unchanged UI).
 */
function bf_re_emb_render_meta_box( WP_Post $post ) {
    wp_nonce_field( 'bf_re_emb_save', 'bf_re_emb_nonce' );

    $post_id      = $post->ID;
    $related_rows = bf_re_emb_get_related_from_db( $post_id, 100 );

    $custom_selection  = get_post_meta( $post_id, '_bf_custom_related_selection', true );
    $custom_mode_active = get_post_meta( $post_id, '_bf_custom_mode_active', true );
    $is_custom         = ! empty( $custom_selection ) || $custom_mode_active === '1';
    $selected_ids      = ! empty( $custom_selection ) ? $custom_selection : array();
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
                <?php
                foreach ( $related_rows as $row ) :
                    $rel_post = get_post( $row['related_post_id'] );
                    if ( ! $rel_post ) {
                        continue;
                    }
                    $is_selected = in_array( $rel_post->ID, $selected_ids, true );
                    $bg_color    = $is_selected ? '#d4edda' : '#f0f0f0';
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

        updateOrderedIds();

        $('#bf-custom-selection').on('change', function() {
            isCustomMode = $(this).is(':checked');

            if (isCustomMode) {
                $('#bf-custom-mode-help').show();
                $('#bf-default-mode-help').hide();
            } else {
                $('#bf-custom-mode-help').hide();
                $('#bf-default-mode-help').show();
                $('.bf-related-item').removeClass('selected')
                    .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                    .find('.bf-check-icon').hide();
                $('#bf-selected-ids').val('[]');
            }
        });

        $(document).on('click', '#bf-reset-selection', function() {
            if (confirm('Reset to default? This will remove custom selection and show all posts from CSV/database.')) {
                $('<input>').attr({
                    type: 'hidden',
                    name: 'bf_full_reset',
                    value: '1'
                }).appendTo('#post');
                $('#publish, #save-post').click();
            }
        });

        $(document).on('click', '.bf-related-item', function(e) {
            if (!isCustomMode) return;
            if ($(e.target).hasClass('dashicons-menu')) return;

            var $item = $(this);
            var postId = $item.data('id');
            var selectedIds = JSON.parse($('#bf-selected-ids').val() || '[]');

            if ($item.hasClass('selected')) {
                $item.removeClass('selected')
                    .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                    .find('.bf-check-icon').hide();
                selectedIds = selectedIds.filter(function(id) { return id !== postId; });
            } else {
                $item.addClass('selected')
                    .css({'background': '#d4edda', 'border-left-color': '#28a745'})
                    .find('.bf-check-icon').show();
                selectedIds.push(postId);
            }

            $('#bf-selected-ids').val(JSON.stringify(selectedIds));
            updateOrderedIds();
        });

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
                        exclude: <?php echo (int) $post_id; ?>
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

        $(document).on('click', '.bf-search-result', function() {
            var postId = $(this).data('id');
            var postTitle = $(this).data('title');

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

            if (isCustomMode) {
                var selectedIds = JSON.parse($('#bf-selected-ids').val() || '[]');
                selectedIds.push(postId);
                $('#bf-selected-ids').val(JSON.stringify(selectedIds));
            }

            updateOrderedIds();
            $('#bf-post-search').val('');
            $('#bf-search-results').hide();
        });

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
 * AJAX search posts.
 */
function bf_re_emb_ajax_search_posts() {
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
 * CSV import.
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
    $handle   = fopen( $tmp_name, 'r' );

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
        $col                = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
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
 * Related posts CSV / usage page.
 */
function bf_re_emb_render_settings_page() {
    global $wpdb;

    if ( isset( $_POST['bf_re_emb_import_submit'] ) ) {
        bf_re_emb_handle_csv_import();
    }

    settings_errors( 'bf_re_emb_messages' );

    $table_name   = bf_re_emb_table_name();
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    $row_count    = 0;

    if ( $table_exists === $table_name ) {
        $row_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM `{$table_name}`" );
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
 * PUBLIC API: get related posts.
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
 * [bf_related_posts] shortcode.
 */
function bf_re_emb_shortcode( $atts ) {
    $atts = shortcode_atts(
        array(
            'post_id' => get_the_ID(),
            'limit'   => 5,
            'title'   => 'Related Posts',
        ),
        $atts
    );

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
 * Enqueue sortable script for meta box.
 */
function bf_re_emb_enqueue_scripts( $hook ) {
    if ( 'post.php' !== $hook && 'post-new.php' !== $hook ) {
        return;
    }

    wp_enqueue_script( 'jquery-ui-sortable' );
}
add_action( 'admin_enqueue_scripts', 'bf_re_emb_enqueue_scripts' );

/* ####################### // CHUNK_1 #######################  */

/* ####################### CHUNK_2 #######################  */

/* -------------------------------------------------------------------------
 * TAG FAMILIES (CSV + meta box + manual family tag + shortcode)
 * ------------------------------------------------------------------------- */

function bf_tf_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'tag_families';
}

/**
 * Get tag family members (same logic as original plugin).
 */
function bf_tf_get_family_members( $tag_id, $limit = 20 ) {
    global $wpdb;
    $table_name = bf_tf_table_name();

    // Check if custom selection is active
    $custom_order = get_term_meta( $tag_id, '_bf_custom_family_order', true );

    if ( ! empty( $custom_order ) && is_array( $custom_order ) ) {
        $out  = array();
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

/**
 * Save tag family members from meta box (custom selection only).
 */
function bf_tf_save_meta_box( $term_id ) {
    if ( ! isset( $_POST['bf_tf_nonce'] ) || ! wp_verify_nonce( $_POST['bf_tf_nonce'], 'bf_tf_save' ) ) {
        return;
    }

    if ( ! current_user_can( 'manage_categories' ) ) {
        return;
    }

    // Save "family tag" flag
    $is_family_tag = isset( $_POST['bf_is_family_tag'] ) ? 1 : 0;
    update_term_meta( $term_id, 'bf_is_family_tag', $is_family_tag );

    // Handle manual add tag by ID (insert row in DB)
    if ( $is_family_tag && ! empty( $_POST['bf_tf_add_tag_id'] ) ) {
        $add_tag_id = (int) $_POST['bf_tf_add_tag_id'];
        if ( $add_tag_id > 0 && $add_tag_id !== $term_id ) {
            $tag_to_add = get_term( $add_tag_id, 'post_tag' );
            $canonical  = get_term( $term_id, 'post_tag' );
            if ( $tag_to_add && ! is_wp_error( $tag_to_add ) && $canonical && ! is_wp_error( $canonical ) ) {
                global $wpdb;
                $table_name = bf_tf_table_name();

                // family_id = canonical term_id
                $wpdb->replace(
                    $table_name,
                    array(
                        'family_id'               => $term_id,
                        'canonical_tag_id'        => $term_id,
                        'canonical_label'         => $canonical->name,
                        'tag_id'                  => $tag_to_add->term_id,
                        'tag_label'               => $tag_to_add->name,
                        'similarity_to_canonical' => 1.0,
                        'usage_count'             => 0,
                        'entity_label'            => 'O',
                    ),
                    array( '%d', '%d', '%s', '%d', '%s', '%f', '%d', '%s' )
                );
            }
        }
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
        $selected_ids = isset( $_POST['bf_tf_selected_ids'] ) ? json_decode( stripslashes( $_POST['bf_tf_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );

        $ordered_ids = isset( $_POST['bf_tf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_tf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $ordered_selected = array_values( array_intersect( $ordered_ids, $selected_ids ) );

        update_term_meta( $term_id, '_bf_custom_family_selection', $selected_ids );
        update_term_meta( $term_id, '_bf_custom_family_order', $ordered_selected );
        update_term_meta( $term_id, '_bf_custom_mode_active', '1' );
    } else {
        delete_term_meta( $term_id, '_bf_custom_family_selection' );
        delete_term_meta( $term_id, '_bf_custom_mode_active' );
        delete_term_meta( $term_id, '_bf_custom_family_order' );
    }
}
add_action( 'edited_post_tag', 'bf_tf_save_meta_box', 10, 1 );
add_action( 'create_post_tag', 'bf_tf_save_meta_box', 10, 1 );

/**
 * Redirect back to term edit page after save (instead of term list).
 */
function bf_tf_redirect_after_save( $location, $term_id ) {
    if ( isset( $_POST['bf_tf_nonce'] ) && wp_verify_nonce( $_POST['bf_tf_nonce'], 'bf_tf_save' ) ) {
        $taxonomy = isset( $_POST['taxonomy'] ) ? $_POST['taxonomy'] : 'post_tag';

        $location = add_query_arg(
            array(
                'taxonomy'  => $taxonomy,
                'tag_ID'    => $term_id,
                'post_type' => 'post',
            ),
            admin_url( 'term.php' )
        );
    }

    return $location;
}
add_filter( 'edit_term_redirect', 'bf_tf_redirect_after_save', 10, 2 );

/**
 * Meta box: manage tag family, extended with:
 * - family tag checkbox
 * - add tag by ID field
 */
function bf_tf_render_meta_box( $term ) {
    wp_nonce_field( 'bf_tf_save', 'bf_tf_nonce' );

    $term_id       = $term->term_id;
    $family_members = bf_tf_get_family_members( $term_id, 100 );

    global $wpdb;
    $table_name = bf_tf_table_name();
    $canonical_info = $wpdb->get_row(
        $wpdb->prepare(
            "SELECT family_id, canonical_tag_id, canonical_label FROM `{$table_name}` WHERE tag_id = %d LIMIT 1",
            $term_id
        ),
        ARRAY_A
    );

    $custom_selection   = get_term_meta( $term_id, '_bf_custom_family_selection', true );
    $custom_mode_active = get_term_meta( $term_id, '_bf_custom_mode_active', true );
    $is_custom          = ! empty( $custom_selection ) || $custom_mode_active === '1';
    $selected_ids       = ! empty( $custom_selection ) ? $custom_selection : array();

    $is_family_tag = (int) get_term_meta( $term_id, 'bf_is_family_tag', true );
    ?>
    <tr class="form-field">
        <th scope="row"><label>Tag Family (Embeddings)</label></th>
        <td>
            <?php if ( $canonical_info ) : ?>
                <div style="background: #f0f6fc; padding: 10px; border-left: 3px solid #0073aa; margin-bottom: 15px;">
                    <strong>Canonical family:</strong><br>
                    Family ID: <?php echo (int) $canonical_info['family_id']; ?><br>
                    Canonical Tag ID: <?php echo (int) $canonical_info['canonical_tag_id']; ?><br>
                    Label: <?php echo esc_html( $canonical_info['canonical_label'] ); ?>
                </div>
            <?php else : ?>
                <div style="background: #fff3cd; padding: 10px; border-left: 3px solid #ffc107; margin-bottom: 15px;">
                    This tag has no family data yet. You can import CSV or mark it as a family tag and start adding members.
                </div>
            <?php endif; ?>

            <p>
                <label>
                    <input type="checkbox" name="bf_is_family_tag" value="1" <?php checked( $is_family_tag, 1 ); ?>>
                    This tag is a <strong>family tag</strong> (canonical).
                </label>
            </p>

            <div style="margin: 10px 0; padding: 10px; border: 1px solid #ddd;">
                <p style="margin-top:0;"><strong>Add member tag by ID</strong> (manual correction)</p>
                <p>
                    <input type="number" name="bf_tf_add_tag_id" value="" min="1" style="width:120px;" placeholder="Tag ID">
                    <br><span style="font-size:12px;color:#666;">On save, this tag will be added to this family table.</span>
                </p>
            </div>

            <p style="margin-top:15px;margin-bottom:8px;">
                <label>
                    <input type="checkbox" id="bf-tf-custom-selection" name="bf_tf_custom_selection" value="1" <?php checked( $is_custom ); ?>>
                    <strong>Custom selection</strong>
                </label>
                <?php if ( $is_custom ) : ?>
                    <button type="button" id="bf-tf-reset-selection" class="button button-small" style="margin-left:8px;">Reset</button>
                <?php endif; ?>
            </p>

            <div id="bf-tf-custom-mode-help" style="display: <?php echo $is_custom ? 'block' : 'none'; ?>; padding: 8px; background: #fff3cd; border-left: 3px solid #ffc107; margin-bottom: 10px; font-size: 12px;">
                Click to select/deselect. Drag to reorder. Selected tags = green.
            </div>

            <div id="bf-tf-default-mode-help" style="display: <?php echo $is_custom ? 'none' : 'block'; ?>; padding: 8px; background: #d1ecf1; border-left: 3px solid #0c5460; margin-bottom: 10px; font-size: 12px;">
                All family members shown. Drag to reorder.
            </div>

            <ul id="bf-tf-family-list" style="list-style:none;margin:0 0 10px 0;padding:0;">
                <?php if ( ! empty( $family_members ) ) : ?>
                    <?php foreach ( $family_members as $row ) : ?>
                        <?php
                        $member_tag = get_term( $row['tag_id'], 'post_tag' );
                        if ( ! $member_tag || is_wp_error( $member_tag ) ) {
                            continue;
                        }
                        $is_selected = in_array( $member_tag->term_id, $selected_ids, true );
                        $bg_color    = $is_selected ? '#d4edda' : '#f0f0f0';
                        $border_color = $is_selected ? '#28a745' : '#2271b1';
                        ?>
                        <li class="bf-tf-family-item <?php echo $is_selected ? 'selected' : ''; ?>"
                            data-id="<?php echo esc_attr( $member_tag->term_id ); ?>"
                            style="padding: 8px; margin: 3px 0; background: <?php echo $bg_color; ?>; cursor: move; border-left: 3px solid <?php echo $border_color; ?>; transition: all 0.2s;">
                            <span class="dashicons dashicons-menu" style="color:#999;margin-right:5px;"></span>
                            <strong>#<?php echo (int) $member_tag->term_id; ?></strong> — <?php echo esc_html( $member_tag->name ); ?>
                            <span class="bf-tf-check-icon" style="float:right;display:<?php echo $is_selected ? 'inline' : 'none'; ?>;">✓</span>
                        </li>
                    <?php endforeach; ?>
                <?php else : ?>
                    <li style="padding:8px;color:#666;font-style:italic;">No family members yet. Import CSV or add tags by ID.</li>
                <?php endif; ?>
            </ul>

            <input type="hidden" id="bf-tf-selected-ids" name="bf_tf_selected_ids" value="<?php echo esc_attr( json_encode( $selected_ids ) ); ?>">
            <input type="hidden" id="bf-tf-ordered-ids" name="bf_tf_ordered_ids" value="">

            <p style="font-size:11px;color:#777;margin-top:10px;">
                Custom selection only affects ordering/visibility in UI. Underlying CSV / DB data remains available.
            </p>
        </td>
    </tr>

    <script>
    jQuery(document).ready(function($) {
        var isCustomMode = $('#bf-tf-custom-selection').is(':checked');

        $('#bf-tf-family-list').sortable({
            placeholder: 'ui-state-highlight',
            handle: '.dashicons-menu',
            update: function() {
                updateOrderedIds();
            }
        });

        function updateOrderedIds() {
            var orderedIds = [];
            $('.bf-tf-family-item').each(function() {
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
                $('.bf-tf-family-item').removeClass('selected')
                    .css({'background':'#f0f0f0','border-left-color':'#2271b1'})
                    .find('.bf-tf-check-icon').hide();
                $('#bf-tf-selected-ids').val('[]');
            }
        });

        $(document).on('click', '#bf-tf-reset-selection', function() {
            if (confirm('Reset to default? This will remove custom selection and show all members from CSV/database.')) {
                $('<input>').attr({
                    type: 'hidden',
                    name: 'bf_tf_full_reset',
                    value: '1'
                }).appendTo('form#edittag');
                $('form#edittag').submit();
            }
        });

        $(document).on('click', '.bf-tf-family-item', function(e) {
            if (!isCustomMode) return;
            if ($(e.target).hasClass('dashicons-menu')) return;

            var $item = $(this);
            var tagId = $item.data('id');
            var selectedIds = JSON.parse($('#bf-tf-selected-ids').val() || '[]');

            if ($item.hasClass('selected')) {
                $item.removeClass('selected')
                    .css({'background':'#f0f0f0','border-left-color':'#2271b1'})
                    .find('.bf-tf-check-icon').hide();
                selectedIds = selectedIds.filter(function(id) { return id !== tagId; });
            } else {
                $item.addClass('selected')
                    .css({'background':'#d4edda','border-left-color':'#28a745'})
                    .find('.bf-tf-check-icon').show();
                selectedIds.push(tagId);
            }

            $('#bf-tf-selected-ids').val(JSON.stringify(selectedIds));
            updateOrderedIds();
        });
    });
    </script>
    <?php
}

/**
 * Hook meta box into tag edit form.
 */
function bf_tf_add_meta_box_fields( $term ) {
    bf_tf_render_meta_box( $term );
}
add_action( 'post_tag_edit_form_fields', 'bf_tf_add_meta_box_fields', 10, 1 );

/**
 * CSV import for tag families.
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
    $handle   = fopen( $tmp_name, 'r' );

    if ( ! $handle ) {
        add_settings_error( 'bf_tf_messages', 'bf_tf_file_open_error', 'Could not open file.', 'error' );
        return;
    }

    global $wpdb;
    $table_name = bf_tf_table_name();

    if ( isset( $_POST['bf_tf_truncate_table'] ) && $_POST['bf_tf_truncate_table'] === '1' ) {
        $wpdb->query( "TRUNCATE TABLE `{$table_name}`" );
    }

    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error( 'bf_tf_messages', 'bf_tf_bad_header', 'CSV has no header.', 'error' );
        return;
    }

    $normalized_header = array();
    foreach ( $header as $col ) {
        $col                = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
        $normalized_header[] = strtolower( trim( $col ) );
    }

    $idx_family_id               = array_search( 'family_id', $normalized_header, true );
    $idx_canonical_tag_id        = array_search( 'canonical_tag_id', $normalized_header, true );
    $idx_canonical_label         = array_search( 'canonical_label', $normalized_header, true );
    $idx_tag_id                  = array_search( 'tag_id', $normalized_header, true );
    $idx_tag_label               = array_search( 'tag_label', $normalized_header, true );
    $idx_similarity_to_canonical = array_search( 'similarity_to_canonical', $normalized_header, true );
    $idx_usage_count             = array_search( 'usage_count', $normalized_header, true );
    $idx_entity_label            = array_search( 'entity_label', $normalized_header, true );

    if ( $idx_family_id === false || $idx_canonical_tag_id === false || $idx_canonical_label === false ||
         $idx_tag_id === false || $idx_tag_label === false || $idx_similarity_to_canonical === false ||
         $idx_usage_count === false || $idx_entity_label === false ) {
        fclose( $handle );
        add_settings_error(
            'bf_tf_messages',
            'bf_tf_missing_columns',
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
            $table_name,
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
    if ( isset( $_POST['bf_tf_truncate_table'] ) && $_POST['bf_tf_truncate_table'] === '1' ) {
        $message .= ' (Table truncated first)';
    }

    add_settings_error( 'bf_tf_messages', 'bf_tf_import_success', $message, 'updated' );
}

/**
 * Tag families CSV / usage page.
 */
function bf_tf_render_settings_page() {
    global $wpdb;

    if ( isset( $_POST['bf_tf_import_submit'] ) ) {
        bf_tf_handle_csv_import();
    }

    settings_errors( 'bf_tf_messages' );

    $table_name   = bf_tf_table_name();
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    $row_count    = 0;

    if ( $table_exists === $table_name ) {
        $row_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM `{$table_name}`" );
    }
    ?>
    <div class="wrap">
        <h1>Tag Families Embeddings</h1>

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
        <p>CSV format: <code>family_id,canonical_tag_id,canonical_label,tag_id,tag_label,similarity_to_canonical,usage_count,entity_label</code></p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_tf_import_csv', 'bf_tf_import_nonce' ); ?>

            <table class="form-table">
                <tr>
                    <th><label for="bf_tf_csv">CSV File</label></th>
                    <td><input type="file" id="bf_tf_csv" name="bf_tf_csv" accept=".csv"></td>
                </tr>
                <tr>
                    <th><label for="bf_tf_truncate_table">Truncate table first?</label></th>
                    <td>
                        <label>
                            <input type="checkbox" id="bf_tf_truncate_table" name="bf_tf_truncate_table" value="1">
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

            <h3>Template Function</h3>
            <pre style="background: #f5f5f5; padding: 15px; border: 1px solid #ddd; overflow-x: auto; font-family: monospace; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">$related_tags = bf_get_related_tags( $tag_id, $limit );
foreach ( $related_tags as $tag ) {
    echo '&lt;a href="' . $tag['link'] . '"&gt;' . $tag['name'] . '&lt;/a&gt;';
}</pre>
        </div>
    </div>
    <?php
}

/**
 * PUBLIC API: get related tags for a tag_id.
 */
function bf_get_related_tags( $tag_id = 0, $limit = 5 ) {
    if ( ! $tag_id ) {
        $tag = get_queried_object();
        if ( $tag && ! is_wp_error( $tag ) && isset( $tag->term_id ) ) {
            $tag_id = $tag->term_id;
        }
    }

    if ( ! $tag_id ) {
        return array();
    }

    $rows = bf_tf_get_family_members( $tag_id, $limit );

    $out = array();
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

/**
 * [bf_related_tags] shortcode.
 */
function bf_tf_shortcode( $atts ) {
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

    $related = bf_get_related_tags( $tag_id, (int) $atts['limit'] );

    if ( empty( $related ) ) {
        return '';
    }

    $html = '<div class="bf-related-tags">';

    if ( ! empty( $atts['title'] ) ) {
        $html .= '<h3>' . esc_html( $atts['title'] ) . '</h3>';
    }

    $html .= '<ul>';
    foreach ( $related as $tag ) {
        $html .= '<li><a href="' . esc_url( $tag['link'] ) . '">' . esc_html( $tag['name'] ) . '</a></li>';
    }
    $html .= '</ul></div>';

    return $html;
}
add_shortcode( 'bf_related_tags', 'bf_tf_shortcode' );

/* ####################### // CHUNK_2 #######################  */

/* ####################### CHUNK_3 #######################  */

/* -------------------------------------------------------------------------
 * BF SEMANTIC SEO FEATURES (from functions_specific.php, adapted)
 * ------------------------------------------------------------------------- */

/**
 * Semantic breadcrumbs (HTML).
 * You can call bf_semantic_breadcrumbs() in your theme.
 */
function bf_semantic_breadcrumbs() {
    if ( ! get_option( 'bf_sem_seo_enable_breadcrumbs' ) ) {
        return;
    }

    if ( is_front_page() ) {
        return;
    }

    global $post;

    echo '<nav class="bf-breadcrumbs" aria-label="Breadcrumbs">';
    echo '<a href="' . esc_url( home_url( '/' ) ) . '">Home</a>';

    if ( is_single() && $post ) {
        // Add category
        $categories = get_the_category( $post->ID );
        if ( ! empty( $categories ) ) {
            $primary = $categories[0];
            echo ' &raquo; <a href="' . esc_url( get_category_link( $primary ) ) . '">' . esc_html( $primary->name ) . '</a>';
        }

        echo ' &raquo; <span>' . esc_html( get_the_title( $post ) ) . '</span>';
    } elseif ( is_tag() ) {
        $tag = get_queried_object();
        echo ' &raquo; <span>Tag: ' . esc_html( $tag->name ) . '</span>';
    } elseif ( is_category() ) {
        $cat = get_queried_object();
        echo ' &raquo; <span>Category: ' . esc_html( $cat->name ) . '</span>';
    } elseif ( is_search() ) {
        echo ' &raquo; <span>Search: ' . esc_html( get_search_query() ) . '</span>';
    } elseif ( is_page() && $post ) {
        $ancestors = array_reverse( get_post_ancestors( $post ) );
        foreach ( $ancestors as $ancestor_id ) {
            echo ' &raquo; <a href="' . esc_url( get_permalink( $ancestor_id ) ) . '">' . esc_html( get_the_title( $ancestor_id ) ) . '</a>';
        }
        echo ' &raquo; <span>' . esc_html( get_the_title( $post ) ) . '</span>';
    }

    echo '</nav>';
}

/**
 * Breadcrumb JSON-LD schema.
 */
function bf_breadcrumb_schema() {
    if ( ! get_option( 'bf_sem_seo_enable_schema' ) ) {
        return;
    }

    if ( is_front_page() ) {
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
            $primary = $categories[0];
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
add_action( 'wp_head', 'bf_breadcrumb_schema' );

/**
 * Tag archive JSON-LD schema (simple Topic / CollectionPage).
 */
function bf_tag_archive_schema() {
    if ( ! get_option( 'bf_sem_seo_enable_schema' ) ) {
        return;
    }

    if ( ! is_tag() ) {
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
add_action( 'wp_head', 'bf_tag_archive_schema', 20 );

/* -------------------------------------------------------------------------
 * SEMANTIC SIDEBAR (widget + shortcode)
 * ------------------------------------------------------------------------- */

/**
 * Main semantic sidebar renderer.
 * Relies on bf_get_related_posts() and bf_get_related_tags().
 */
function bf_semantic_sidebar() {
    if ( ! is_single() ) {
        if ( get_option( 'bf_sem_seo_debug' ) ) {
            echo '<div class="semantic-sidebar-widget" style="margin:15px 0;padding:10px;border:1px solid #ddd;background:#fffef5;">';
            echo '<p style="margin:0;font-size:12px;">Not a single post page, semantic sidebar is skipped.</p>';
            echo '</div>';
        }
        return;
    }

    if ( ! get_option( 'bf_sem_seo_enable_sidebar' ) ) {
        return;
    }

    global $post, $wpdb;

    ?>
    <div class="semantic-sidebar-widget" style="margin:15px 0;padding:10px;border:1px solid #ddd;background:#ffffff;">

        <?php if ( get_option( 'bf_sem_seo_debug' ) ) : ?>
        <!-- DEBUG INFO -->
        <div style="background:#fff3cd;padding:10px;margin-bottom:15px;border-left:4px solid #ffc107;font-size:12px;">
            <strong>🔍 Debug Info:</strong><br>
            Post ID: <?php echo (int) $post->ID; ?><br>
            bf_get_related_posts exists: <?php echo function_exists( 'bf_get_related_posts' ) ? '✅ Yes' : '❌ No'; ?><br>
            bf_get_related_tags exists: <?php echo function_exists( 'bf_get_related_tags' ) ? '✅ Yes' : '❌ No'; ?><br>
            <?php
            $tags = get_the_tags( $post->ID );
            echo 'Post has tags: ' . ( $tags ? '✅ Yes (' . count( $tags ) . ')' : '❌ No' ) . '<br>';

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
                $tag_db_count = $wpdb->get_var(
                    $wpdb->prepare(
                        "SELECT COUNT(*) FROM {$wpdb->prefix}tag_families WHERE tag_id = %d",
                        $tags[0]->term_id
                    )
                );
                echo 'Tag family data in DB for first tag: ' . ( $tag_db_count ? '✅ Yes' : '❌ No' ) . '<br>';
            }
            ?>
        </div>
        <?php endif; ?>

        <?php
        // Related posts via embeddings.
        $related_posts = function_exists( 'bf_get_related_posts' ) ? bf_get_related_posts( $post->ID, 5 ) : array();
        if ( ! empty( $related_posts ) ) :
        ?>
            <div class="bf-semantic-block bf-related-posts-block" style="margin-bottom:15px;">
                <h3 style="margin-top:0;">Related Posts IA sidebar</h3>
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
        <?php elseif ( get_option( 'bf_sem_seo_debug' ) ) : ?>
            <p style="font-size:12px;color:#777;"><em>No related posts found in DB for this post.</em></p>
        <?php endif; ?>

        <?php
        // Related tags based on first tag family.
        $tags = get_the_tags( $post->ID );
        if ( $tags ) {
            $first_tag = $tags[0];
            $related_tags = function_exists( 'bf_get_related_tags' ) ? bf_get_related_tags( $first_tag->term_id, 10 ) : array();

            if ( ! empty( $related_tags ) ) :
                ?>
                <div class="bf-semantic-block bf-related-tags-block">
                    <h3>Related Tags IA</h3>
                    <ul>
                        <?php foreach ( $related_tags as $rt ) : ?>
                            <li>
                                <a href="<?php echo esc_url( $rt['link'] ); ?>"><?php echo esc_html( $rt['name'] ); ?></a>
                            </li>
                        <?php endforeach; ?>
                    </ul>
                </div>
                <?php
            elseif ( get_option( 'bf_sem_seo_debug' ) ) :
                ?>
                <p style="font-size:12px;color:#777;"><em>No tag families found for first tag.</em></p>
                <?php
            endif;
        } elseif ( get_option( 'bf_sem_seo_debug' ) ) {
            echo '<p style="font-size:12px;color:#777;"><em>Post has no tags.</em></p>';
        }
        ?>

    </div>
    <?php
}

/**
 * Sidebar shortcode [bf_sidebar].
 */
function bf_semantic_sidebar_shortcode( $atts ) {
    if ( ! get_option( 'bf_sem_seo_enable_sidebar' ) ) {
        return '';
    }

    ob_start();
    bf_semantic_sidebar();
    return ob_get_clean();
}
add_shortcode( 'bf_sidebar', 'bf_semantic_sidebar_shortcode' );

/**
 * Sidebar widget wrapper.
 */
class BF_Semantic_Sidebar_Widget extends WP_Widget {
    public function __construct() {
        parent::__construct(
            'bf_semantic_sidebar_widget',
            'BF Semantic Sidebar',
            array(
                'description' => 'Shows related posts and tags using embeddings-based data.',
            )
        );
    }

    public function widget( $args, $instance ) {
        if ( ! get_option( 'bf_sem_seo_enable_sidebar' ) ) {
            return;
        }

        echo $args['before_widget'];
        bf_semantic_sidebar();
        echo $args['after_widget'];
    }

    public function form( $instance ) {
        echo '<p>This widget automatically shows semantic related content on single posts, based on embeddings DB tables.</p>';
    }
}

function bf_register_semantic_sidebar_widget() {
    register_widget( 'BF_Semantic_Sidebar_Widget' );
}
add_action( 'widgets_init', 'bf_register_semantic_sidebar_widget' );

/* -------------------------------------------------------------------------
 * AUTO FOOTER RELATED CONTENT
 * ------------------------------------------------------------------------- */

/**
 * Append related posts and tags blocks at the end of single post content.
 */

/**
 * Output related posts/tags at the very bottom of the page (footer),
 * instead of filtering the_content to avoid recursion with blocks.
 */
function bf_sem_seo_render_footer_related() {
    if ( ! is_single() || ! is_main_query() ) {
        return;
    }

    if ( is_admin() || doing_action( 'rest_api_init' ) || wp_is_json_request() ) {
        return;
    }

    if ( ! get_option( 'bf_sem_seo_enable_footer' ) ) {
        return;
    }

    global $post;
    if ( ! $post instanceof WP_Post ) {
        return;
    }

    // Avoid running multiple times.
    static $done = false;
    if ( $done ) {
        return;
    }
    $done = true;

    $html = '';

    // RELATED POSTS (small list).
    $related_posts = function_exists( 'bf_get_related_posts' ) ? bf_get_related_posts( $post->ID, 3 ) : array();
    if ( ! empty( $related_posts ) ) {
        $html .= '<div class="bf-related-footer bf-related-footer-posts" style="margin-top:30px;padding-top:15px;border-top:1px solid #ddd;">';
        $html .= '<h3>Related Posts IA</h3><ul>';
        foreach ( $related_posts as $rp ) {
            if ( empty( $rp['permalink'] ) || empty( $rp['title'] ) ) {
                continue;
            }
            $html .= '<li><a href="' . esc_url( $rp['permalink'] ) . '">' . esc_html( $rp['title'] ) . '</a></li>';
        }
        $html .= '</ul></div>';
    }

    // RELATED TAGS.
    $tags = get_the_tags( $post->ID );
    if ( $tags && ! empty( $tags[0]->term_id ) ) {
        $first_tag = $tags[0];
        $related_tags = function_exists( 'bf_get_related_tags' ) ? bf_get_related_tags( $first_tag->term_id, 6 ) : array();

        if ( ! empty( $related_tags ) && is_array( $related_tags ) ) {
            $html .= '<div class="bf-related-footer bf-related-footer-tags" style="margin-top:15px;">';
            $html .= '<h3>Explore Related Tags IA</h3><p>';

            $links = array();
            foreach ( $related_tags as $rt ) {
                if ( empty( $rt['link'] ) || empty( $rt['name'] ) ) {
                    continue;
                }
                $links[] = '<a href="' . esc_url( $rt['link'] ) . '">' . esc_html( $rt['name'] ) . '</a>';
            }

            $html .= implode( ', ', $links );
            $html .= '</p></div>';
        }
    }

    if ( $html === '' ) {
        return;
    }

    echo $html;
}
add_action( 'wp_footer', 'bf_sem_seo_render_footer_related', 20 );



/* ####################### // CHUNK_3 #######################  */

?>
```




## PROMPT_1
En tant qu'expert Wordpress, analyse le code de bf-semantic-seo.php et réfléchit aux évolutions suivantes ci-dessous. Pour chaque évolution tâche de donner avant de coder quoi que que ce soit, des arguments pour et contre avec le plugin actuel : 
- J’ai un problème, je ne peux facilement transformer des tags en family tag.
- J’ai un problème, je ne peux pas ajouter des tags de post à des family tags, je ne peux pas les ordonner.
- Faut-il gérer les familles (families) indépendamment des tags sinon je ne peux pas maintenir la taxonomie des tags (post tags) et le rapprochement des tags des posts via les familles de tags  (families) ? si oui il faudrait donc faire évoluer le plugin en faisant en sorte que je puisse ajouter/retirer des tags des posts dans un tag de famille dans une page à part et dans une taxonomie à part e.g. bf_tag_families
- Si on crée une nouvelle taxonomie attachée aux post e.g bf_tag_families comment conserver une base à jour des tags id qui sont représentatifs de la taxonomie des tags de post et comment continuer de mettre à jour la table de base de données avec un cvs.
- Que se passe-t-il si je corrige manuellement l'attachement d'un tag id à une famille ou si je supprime un tag de post et qu'il continue d'être dans un famille
- Comment assurer un mirroring correct entre ces deux bases de post tags qui viennent nourrir la table des familles id. C'est le même problème que dans une gestion de catégories.
- Le problème vient du fait que la jointure se fait sur un seul tag or le post peut appartenir à plusieurs familles si je décide de faire cette jointure.
- Quelle est la meilleure marche à suivre pour faire coexister les deux systèmes ?


- bf-semantic-seo.php
```php
<?php
/**
 * Plugin Name: BF Semantic SEO Suite
 * Description: All-in-one semantic clustering plugin (related posts, tag families, sidebar, breadcrumbs & schemas).
 * Version: 1.0.0
 * Author: Bruno Flaven & IA
 * Text Domain: bf-semantic-seo
 */

/* ####################### // CHUNK_1 #######################  */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'BF_SEM_SEO_VERSION', '1.0.0' );

/**
 * ACTIVATION: create tables + defaults.
 */
function bf_sem_seo_activate() {
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

    // Tag families table.
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

    // Options defaults.
    add_option( 'bf_sem_seo_debug', 0 );
    add_option( 'bf_sem_seo_enable_sidebar', 1 );
    add_option( 'bf_sem_seo_enable_footer', 1 );
    add_option( 'bf_sem_seo_enable_breadcrumbs', 1 );
    add_option( 'bf_sem_seo_enable_schema', 1 );

    set_transient( 'bf_sem_seo_activation_notice', true, 30 );
}
register_activation_hook( __FILE__, 'bf_sem_seo_activate' );

/**
 * UNINSTALL: drop tables + options + term meta.
 */
function bf_sem_seo_uninstall() {
    global $wpdb;

    $wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}related_posts_embeddings`" );
    $wpdb->query( "DROP TABLE IF EXISTS `{$wpdb->prefix}tag_families`" );

    delete_option( 'bf_sem_seo_debug' );
    delete_option( 'bf_sem_seo_enable_sidebar' );
    delete_option( 'bf_sem_seo_enable_footer' );
    delete_option( 'bf_sem_seo_enable_breadcrumbs' );
    delete_option( 'bf_sem_seo_enable_schema' );

    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_selection'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_mode_active'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = '_bf_custom_family_order'" );
    $wpdb->query( "DELETE FROM {$wpdb->termmeta} WHERE meta_key = 'bf_is_family_tag'" );
}
register_uninstall_hook( __FILE__, 'bf_sem_seo_uninstall' );

/**
 * Activation notice.
 */
function bf_sem_seo_activation_notice() {
    if ( get_transient( 'bf_sem_seo_activation_notice' ) ) {
        delete_transient( 'bf_sem_seo_activation_notice' );
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p><strong>BF Semantic SEO Suite:</strong> Tables created. Go to Settings → BF Semantic SEO to import CSV and configure options.</p>';
        echo '</div>';
    }
}
add_action( 'admin_notices', 'bf_sem_seo_activation_notice' );

/* -------------------------------------------------------------------------
 * SETTINGS PAGE (global toggles)
 * ------------------------------------------------------------------------- */

function bf_sem_seo_register_settings() {
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_debug', array( 'type' => 'boolean', 'default' => 0 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_sidebar', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_footer', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_breadcrumbs', array( 'type' => 'boolean', 'default' => 1 ) );
    register_setting( 'bf_sem_seo_settings', 'bf_sem_seo_enable_schema', array( 'type' => 'boolean', 'default' => 1 ) );
}
add_action( 'admin_init', 'bf_sem_seo_register_settings' );

function bf_sem_seo_admin_menu() {
    // Main settings + Help.
    add_options_page(
        'BF Semantic SEO',
        'BF Semantic SEO',
        'manage_options',
        'bf-sem-seo',
        'bf_sem_seo_render_settings_page'
    );

    // CSV pages re-used as subpages in Settings for familiarity.
    add_submenu_page(
        'options-general.php',
        'Related Embeddings',
        'Related Embeddings',
        'manage_options',
        'bf-sem-seo-related',
        'bf_re_emb_render_settings_page'
    );

    add_submenu_page(
        'options-general.php',
        'Tag Families',
        'Tag Families',
        'manage_options',
        'bf-sem-seo-families',
        'bf_tf_render_settings_page'
    );
}
add_action( 'admin_menu', 'bf_sem_seo_admin_menu' );

function bf_sem_seo_render_settings_page() {
    ?>
    <div class="wrap">
        <h1>BF Semantic SEO Suite</h1>

        <form method="post" action="options.php">
            <?php settings_fields( 'bf_sem_seo_settings' ); ?>

            <h2>Features</h2>
            <table class="form-table">
                <tr>
                    <th scope="row">Debug mode</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_debug" value="1" <?php checked( get_option( 'bf_sem_seo_debug' ), 1 ); ?>>
                            Enable debug blocks in semantic sidebar.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Semantic Sidebar</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_sidebar" value="1" <?php checked( get_option( 'bf_sem_seo_enable_sidebar' ), 1 ); ?>>
                            Enable semantic sidebar widget / shortcode.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Footer Related Content</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_footer" value="1" <?php checked( get_option( 'bf_sem_seo_enable_footer' ), 1 ); ?>>
                            Append related posts/tags after post content.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Breadcrumbs</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_breadcrumbs" value="1" <?php checked( get_option( 'bf_sem_seo_enable_breadcrumbs' ), 1 ); ?>>
                            Enable semantic breadcrumbs functions.
                        </label>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Schema.org JSON-LD</th>
                    <td>
                        <label>
                            <input type="checkbox" name="bf_sem_seo_enable_schema" value="1" <?php checked( get_option( 'bf_sem_seo_enable_schema' ), 1 ); ?>>
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
            <li>Import CSVs via Settings → Related Embeddings / Tag Families.</li>
            <li>Use shortcodes <code>[bf_related_posts]</code>, <code>[bf_related_tags]</code>, <code>[bf_sidebar]</code> where needed.</li>
        </ul>

        <h3>Uninstall</h3>
        <ul>
            <li>Delete the plugin from Plugins page.</li>
            <li>Tables <code>wp_related_posts_embeddings</code> and <code>wp_tag_families</code> are dropped.</li>
            <li>Options and custom term meta created by this plugin are removed.</li>
        </ul>

        <h3>Public APIs</h3>
        <ul>
            <li><code>bf_get_related_posts( $post_id, $limit )</code></li>
            <li><code>bf_get_related_tags( $tag_id, $limit )</code></li>
        </ul>
    </div>
    <?php
}

/* -------------------------------------------------------------------------
 * RELATED POSTS (CSV + meta box + shortcode)
 * ------------------------------------------------------------------------- */

function bf_re_emb_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'related_posts_embeddings';
}

/**
 * Get related posts, same logic as original DB plugin.
 */
function bf_re_emb_get_related_from_db( $post_id, $limit = 10 ) {
    global $wpdb;
    $table_name = bf_re_emb_table_name();

    $custom_order = get_post_meta( $post_id, '_bf_custom_related_order', true );

    if ( ! empty( $custom_order ) && is_array( $custom_order ) ) {
        $out  = array();
        $rank = 1;

        foreach ( $custom_order as $related_id ) {
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
 * Save related posts from meta box.
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

    if ( isset( $_POST['bf_full_reset'] ) && $_POST['bf_full_reset'] === '1' ) {
        delete_post_meta( $post_id, '_bf_custom_related_selection' );
        delete_post_meta( $post_id, '_bf_custom_mode_active' );
        delete_post_meta( $post_id, '_bf_custom_related_order' );
        return;
    }

    $is_custom = isset( $_POST['bf_custom_selection'] ) && $_POST['bf_custom_selection'] === '1';

    if ( $is_custom ) {
        $selected_ids = isset( $_POST['bf_selected_ids'] ) ? json_decode( stripslashes( $_POST['bf_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );

        $ordered_ids = isset( $_POST['bf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $ordered_selected = array_values( array_intersect( $ordered_ids, $selected_ids ) );

        update_post_meta( $post_id, '_bf_custom_related_selection', $selected_ids );
        update_post_meta( $post_id, '_bf_custom_related_order', $ordered_selected );
        update_post_meta( $post_id, '_bf_custom_mode_active', '1' );
    } else {
        delete_post_meta( $post_id, '_bf_custom_related_selection' );
        delete_post_meta( $post_id, '_bf_custom_mode_active' );
        delete_post_meta( $post_id, '_bf_custom_related_order' );

        $ordered_ids = isset( $_POST['bf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $wpdb->delete( $table_name, array( 'post_id' => $post_id ), array( '%d' ) );

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
 * Meta box: manage related posts (unchanged UI).
 */
function bf_re_emb_render_meta_box( WP_Post $post ) {
    wp_nonce_field( 'bf_re_emb_save', 'bf_re_emb_nonce' );

    $post_id      = $post->ID;
    $related_rows = bf_re_emb_get_related_from_db( $post_id, 100 );

    $custom_selection  = get_post_meta( $post_id, '_bf_custom_related_selection', true );
    $custom_mode_active = get_post_meta( $post_id, '_bf_custom_mode_active', true );
    $is_custom         = ! empty( $custom_selection ) || $custom_mode_active === '1';
    $selected_ids      = ! empty( $custom_selection ) ? $custom_selection : array();
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
                <?php
                foreach ( $related_rows as $row ) :
                    $rel_post = get_post( $row['related_post_id'] );
                    if ( ! $rel_post ) {
                        continue;
                    }
                    $is_selected = in_array( $rel_post->ID, $selected_ids, true );
                    $bg_color    = $is_selected ? '#d4edda' : '#f0f0f0';
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

        updateOrderedIds();

        $('#bf-custom-selection').on('change', function() {
            isCustomMode = $(this).is(':checked');

            if (isCustomMode) {
                $('#bf-custom-mode-help').show();
                $('#bf-default-mode-help').hide();
            } else {
                $('#bf-custom-mode-help').hide();
                $('#bf-default-mode-help').show();
                $('.bf-related-item').removeClass('selected')
                    .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                    .find('.bf-check-icon').hide();
                $('#bf-selected-ids').val('[]');
            }
        });

        $(document).on('click', '#bf-reset-selection', function() {
            if (confirm('Reset to default? This will remove custom selection and show all posts from CSV/database.')) {
                $('<input>').attr({
                    type: 'hidden',
                    name: 'bf_full_reset',
                    value: '1'
                }).appendTo('#post');
                $('#publish, #save-post').click();
            }
        });

        $(document).on('click', '.bf-related-item', function(e) {
            if (!isCustomMode) return;
            if ($(e.target).hasClass('dashicons-menu')) return;

            var $item = $(this);
            var postId = $item.data('id');
            var selectedIds = JSON.parse($('#bf-selected-ids').val() || '[]');

            if ($item.hasClass('selected')) {
                $item.removeClass('selected')
                    .css({'background': '#f0f0f0', 'border-left-color': '#2271b1'})
                    .find('.bf-check-icon').hide();
                selectedIds = selectedIds.filter(function(id) { return id !== postId; });
            } else {
                $item.addClass('selected')
                    .css({'background': '#d4edda', 'border-left-color': '#28a745'})
                    .find('.bf-check-icon').show();
                selectedIds.push(postId);
            }

            $('#bf-selected-ids').val(JSON.stringify(selectedIds));
            updateOrderedIds();
        });

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
                        exclude: <?php echo (int) $post_id; ?>
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

        $(document).on('click', '.bf-search-result', function() {
            var postId = $(this).data('id');
            var postTitle = $(this).data('title');

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

            if (isCustomMode) {
                var selectedIds = JSON.parse($('#bf-selected-ids').val() || '[]');
                selectedIds.push(postId);
                $('#bf-selected-ids').val(JSON.stringify(selectedIds));
            }

            updateOrderedIds();
            $('#bf-post-search').val('');
            $('#bf-search-results').hide();
        });

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
 * AJAX search posts.
 */
function bf_re_emb_ajax_search_posts() {
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
 * CSV import.
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
    $handle   = fopen( $tmp_name, 'r' );

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
        $col                = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
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
 * Related posts CSV / usage page.
 */
function bf_re_emb_render_settings_page() {
    global $wpdb;

    if ( isset( $_POST['bf_re_emb_import_submit'] ) ) {
        bf_re_emb_handle_csv_import();
    }

    settings_errors( 'bf_re_emb_messages' );

    $table_name   = bf_re_emb_table_name();
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    $row_count    = 0;

    if ( $table_exists === $table_name ) {
        $row_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM `{$table_name}`" );
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
 * PUBLIC API: get related posts.
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
 * [bf_related_posts] shortcode.
 */
function bf_re_emb_shortcode( $atts ) {
    $atts = shortcode_atts(
        array(
            'post_id' => get_the_ID(),
            'limit'   => 5,
            'title'   => 'Related Posts',
        ),
        $atts
    );

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
 * Enqueue sortable script for meta box.
 */
function bf_re_emb_enqueue_scripts( $hook ) {
    if ( 'post.php' !== $hook && 'post-new.php' !== $hook ) {
        return;
    }

    wp_enqueue_script( 'jquery-ui-sortable' );
}
add_action( 'admin_enqueue_scripts', 'bf_re_emb_enqueue_scripts' );

/* ####################### // CHUNK_1 #######################  */

/* ####################### CHUNK_2 #######################  */

/* -------------------------------------------------------------------------
 * TAG FAMILIES (CSV + meta box + manual family tag + shortcode)
 * ------------------------------------------------------------------------- */

function bf_tf_table_name() {
    global $wpdb;
    return $wpdb->prefix . 'tag_families';
}

/**
 * Get tag family members (same logic as original plugin).
 */
function bf_tf_get_family_members( $tag_id, $limit = 20 ) {
    global $wpdb;
    $table_name = bf_tf_table_name();

    // Check if custom selection is active
    $custom_order = get_term_meta( $tag_id, '_bf_custom_family_order', true );

    if ( ! empty( $custom_order ) && is_array( $custom_order ) ) {
        $out  = array();
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

/**
 * Save tag family members from meta box (custom selection only).
 */
function bf_tf_save_meta_box( $term_id ) {
    if ( ! isset( $_POST['bf_tf_nonce'] ) || ! wp_verify_nonce( $_POST['bf_tf_nonce'], 'bf_tf_save' ) ) {
        return;
    }

    if ( ! current_user_can( 'manage_categories' ) ) {
        return;
    }

    // Save "family tag" flag
    $is_family_tag = isset( $_POST['bf_is_family_tag'] ) ? 1 : 0;
    update_term_meta( $term_id, 'bf_is_family_tag', $is_family_tag );

    // Handle manual add tag by ID (insert row in DB)
    if ( $is_family_tag && ! empty( $_POST['bf_tf_add_tag_id'] ) ) {
        $add_tag_id = (int) $_POST['bf_tf_add_tag_id'];
        if ( $add_tag_id > 0 && $add_tag_id !== $term_id ) {
            $tag_to_add = get_term( $add_tag_id, 'post_tag' );
            $canonical  = get_term( $term_id, 'post_tag' );
            if ( $tag_to_add && ! is_wp_error( $tag_to_add ) && $canonical && ! is_wp_error( $canonical ) ) {
                global $wpdb;
                $table_name = bf_tf_table_name();

                // family_id = canonical term_id
                $wpdb->replace(
                    $table_name,
                    array(
                        'family_id'               => $term_id,
                        'canonical_tag_id'        => $term_id,
                        'canonical_label'         => $canonical->name,
                        'tag_id'                  => $tag_to_add->term_id,
                        'tag_label'               => $tag_to_add->name,
                        'similarity_to_canonical' => 1.0,
                        'usage_count'             => 0,
                        'entity_label'            => 'O',
                    ),
                    array( '%d', '%d', '%s', '%d', '%s', '%f', '%d', '%s' )
                );
            }
        }
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
        $selected_ids = isset( $_POST['bf_tf_selected_ids'] ) ? json_decode( stripslashes( $_POST['bf_tf_selected_ids'] ), true ) : array();
        $selected_ids = array_map( 'intval', $selected_ids );
        $selected_ids = array_filter( $selected_ids );

        $ordered_ids = isset( $_POST['bf_tf_ordered_ids'] ) ? json_decode( stripslashes( $_POST['bf_tf_ordered_ids'] ), true ) : array();
        $ordered_ids = array_map( 'intval', $ordered_ids );
        $ordered_ids = array_filter( $ordered_ids );

        $ordered_selected = array_values( array_intersect( $ordered_ids, $selected_ids ) );

        update_term_meta( $term_id, '_bf_custom_family_selection', $selected_ids );
        update_term_meta( $term_id, '_bf_custom_family_order', $ordered_selected );
        update_term_meta( $term_id, '_bf_custom_mode_active', '1' );
    } else {
        delete_term_meta( $term_id, '_bf_custom_family_selection' );
        delete_term_meta( $term_id, '_bf_custom_mode_active' );
        delete_term_meta( $term_id, '_bf_custom_family_order' );
    }
}
add_action( 'edited_post_tag', 'bf_tf_save_meta_box', 10, 1 );
add_action( 'create_post_tag', 'bf_tf_save_meta_box', 10, 1 );

/**
 * Redirect back to term edit page after save (instead of term list).
 */
function bf_tf_redirect_after_save( $location, $term_id ) {
    if ( isset( $_POST['bf_tf_nonce'] ) && wp_verify_nonce( $_POST['bf_tf_nonce'], 'bf_tf_save' ) ) {
        $taxonomy = isset( $_POST['taxonomy'] ) ? $_POST['taxonomy'] : 'post_tag';

        $location = add_query_arg(
            array(
                'taxonomy'  => $taxonomy,
                'tag_ID'    => $term_id,
                'post_type' => 'post',
            ),
            admin_url( 'term.php' )
        );
    }

    return $location;
}
add_filter( 'edit_term_redirect', 'bf_tf_redirect_after_save', 10, 2 );

/**
 * Meta box: manage tag family, extended with:
 * - family tag checkbox
 * - add tag by ID field
 */
function bf_tf_render_meta_box( $term ) {
    wp_nonce_field( 'bf_tf_save', 'bf_tf_nonce' );

    $term_id       = $term->term_id;
    $family_members = bf_tf_get_family_members( $term_id, 100 );

    global $wpdb;
    $table_name = bf_tf_table_name();
    $canonical_info = $wpdb->get_row(
        $wpdb->prepare(
            "SELECT family_id, canonical_tag_id, canonical_label FROM `{$table_name}` WHERE tag_id = %d LIMIT 1",
            $term_id
        ),
        ARRAY_A
    );

    $custom_selection   = get_term_meta( $term_id, '_bf_custom_family_selection', true );
    $custom_mode_active = get_term_meta( $term_id, '_bf_custom_mode_active', true );
    $is_custom          = ! empty( $custom_selection ) || $custom_mode_active === '1';
    $selected_ids       = ! empty( $custom_selection ) ? $custom_selection : array();

    $is_family_tag = (int) get_term_meta( $term_id, 'bf_is_family_tag', true );
    ?>
    <tr class="form-field">
        <th scope="row"><label>Tag Family (Embeddings)</label></th>
        <td>
            <?php if ( $canonical_info ) : ?>
                <div style="background: #f0f6fc; padding: 10px; border-left: 3px solid #0073aa; margin-bottom: 15px;">
                    <strong>Canonical family:</strong><br>
                    Family ID: <?php echo (int) $canonical_info['family_id']; ?><br>
                    Canonical Tag ID: <?php echo (int) $canonical_info['canonical_tag_id']; ?><br>
                    Label: <?php echo esc_html( $canonical_info['canonical_label'] ); ?>
                </div>
            <?php else : ?>
                <div style="background: #fff3cd; padding: 10px; border-left: 3px solid #ffc107; margin-bottom: 15px;">
                    This tag has no family data yet. You can import CSV or mark it as a family tag and start adding members.
                </div>
            <?php endif; ?>

            <p>
                <label>
                    <input type="checkbox" name="bf_is_family_tag" value="1" <?php checked( $is_family_tag, 1 ); ?>>
                    This tag is a <strong>family tag</strong> (canonical).
                </label>
            </p>

            <div style="margin: 10px 0; padding: 10px; border: 1px solid #ddd;">
                <p style="margin-top:0;"><strong>Add member tag by ID</strong> (manual correction)</p>
                <p>
                    <input type="number" name="bf_tf_add_tag_id" value="" min="1" style="width:120px;" placeholder="Tag ID">
                    <br><span style="font-size:12px;color:#666;">On save, this tag will be added to this family table.</span>
                </p>
            </div>

            <p style="margin-top:15px;margin-bottom:8px;">
                <label>
                    <input type="checkbox" id="bf-tf-custom-selection" name="bf_tf_custom_selection" value="1" <?php checked( $is_custom ); ?>>
                    <strong>Custom selection</strong>
                </label>
                <?php if ( $is_custom ) : ?>
                    <button type="button" id="bf-tf-reset-selection" class="button button-small" style="margin-left:8px;">Reset</button>
                <?php endif; ?>
            </p>

            <div id="bf-tf-custom-mode-help" style="display: <?php echo $is_custom ? 'block' : 'none'; ?>; padding: 8px; background: #fff3cd; border-left: 3px solid #ffc107; margin-bottom: 10px; font-size: 12px;">
                Click to select/deselect. Drag to reorder. Selected tags = green.
            </div>

            <div id="bf-tf-default-mode-help" style="display: <?php echo $is_custom ? 'none' : 'block'; ?>; padding: 8px; background: #d1ecf1; border-left: 3px solid #0c5460; margin-bottom: 10px; font-size: 12px;">
                All family members shown. Drag to reorder.
            </div>

            <ul id="bf-tf-family-list" style="list-style:none;margin:0 0 10px 0;padding:0;">
                <?php if ( ! empty( $family_members ) ) : ?>
                    <?php foreach ( $family_members as $row ) : ?>
                        <?php
                        $member_tag = get_term( $row['tag_id'], 'post_tag' );
                        if ( ! $member_tag || is_wp_error( $member_tag ) ) {
                            continue;
                        }
                        $is_selected = in_array( $member_tag->term_id, $selected_ids, true );
                        $bg_color    = $is_selected ? '#d4edda' : '#f0f0f0';
                        $border_color = $is_selected ? '#28a745' : '#2271b1';
                        ?>
                        <li class="bf-tf-family-item <?php echo $is_selected ? 'selected' : ''; ?>"
                            data-id="<?php echo esc_attr( $member_tag->term_id ); ?>"
                            style="padding: 8px; margin: 3px 0; background: <?php echo $bg_color; ?>; cursor: move; border-left: 3px solid <?php echo $border_color; ?>; transition: all 0.2s;">
                            <span class="dashicons dashicons-menu" style="color:#999;margin-right:5px;"></span>
                            <strong>#<?php echo (int) $member_tag->term_id; ?></strong> — <?php echo esc_html( $member_tag->name ); ?>
                            <span class="bf-tf-check-icon" style="float:right;display:<?php echo $is_selected ? 'inline' : 'none'; ?>;">✓</span>
                        </li>
                    <?php endforeach; ?>
                <?php else : ?>
                    <li style="padding:8px;color:#666;font-style:italic;">No family members yet. Import CSV or add tags by ID.</li>
                <?php endif; ?>
            </ul>

            <input type="hidden" id="bf-tf-selected-ids" name="bf_tf_selected_ids" value="<?php echo esc_attr( json_encode( $selected_ids ) ); ?>">
            <input type="hidden" id="bf-tf-ordered-ids" name="bf_tf_ordered_ids" value="">

            <p style="font-size:11px;color:#777;margin-top:10px;">
                Custom selection only affects ordering/visibility in UI. Underlying CSV / DB data remains available.
            </p>
        </td>
    </tr>

    <script>
    jQuery(document).ready(function($) {
        var isCustomMode = $('#bf-tf-custom-selection').is(':checked');

        $('#bf-tf-family-list').sortable({
            placeholder: 'ui-state-highlight',
            handle: '.dashicons-menu',
            update: function() {
                updateOrderedIds();
            }
        });

        function updateOrderedIds() {
            var orderedIds = [];
            $('.bf-tf-family-item').each(function() {
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
                $('.bf-tf-family-item').removeClass('selected')
                    .css({'background':'#f0f0f0','border-left-color':'#2271b1'})
                    .find('.bf-tf-check-icon').hide();
                $('#bf-tf-selected-ids').val('[]');
            }
        });

        $(document).on('click', '#bf-tf-reset-selection', function() {
            if (confirm('Reset to default? This will remove custom selection and show all members from CSV/database.')) {
                $('<input>').attr({
                    type: 'hidden',
                    name: 'bf_tf_full_reset',
                    value: '1'
                }).appendTo('form#edittag');
                $('form#edittag').submit();
            }
        });

        $(document).on('click', '.bf-tf-family-item', function(e) {
            if (!isCustomMode) return;
            if ($(e.target).hasClass('dashicons-menu')) return;

            var $item = $(this);
            var tagId = $item.data('id');
            var selectedIds = JSON.parse($('#bf-tf-selected-ids').val() || '[]');

            if ($item.hasClass('selected')) {
                $item.removeClass('selected')
                    .css({'background':'#f0f0f0','border-left-color':'#2271b1'})
                    .find('.bf-tf-check-icon').hide();
                selectedIds = selectedIds.filter(function(id) { return id !== tagId; });
            } else {
                $item.addClass('selected')
                    .css({'background':'#d4edda','border-left-color':'#28a745'})
                    .find('.bf-tf-check-icon').show();
                selectedIds.push(tagId);
            }

            $('#bf-tf-selected-ids').val(JSON.stringify(selectedIds));
            updateOrderedIds();
        });
    });
    </script>
    <?php
}

/**
 * Hook meta box into tag edit form.
 */
function bf_tf_add_meta_box_fields( $term ) {
    bf_tf_render_meta_box( $term );
}
add_action( 'post_tag_edit_form_fields', 'bf_tf_add_meta_box_fields', 10, 1 );

/**
 * CSV import for tag families.
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
    $handle   = fopen( $tmp_name, 'r' );

    if ( ! $handle ) {
        add_settings_error( 'bf_tf_messages', 'bf_tf_file_open_error', 'Could not open file.', 'error' );
        return;
    }

    global $wpdb;
    $table_name = bf_tf_table_name();

    if ( isset( $_POST['bf_tf_truncate_table'] ) && $_POST['bf_tf_truncate_table'] === '1' ) {
        $wpdb->query( "TRUNCATE TABLE `{$table_name}`" );
    }

    $header = fgetcsv( $handle );
    if ( ! $header ) {
        fclose( $handle );
        add_settings_error( 'bf_tf_messages', 'bf_tf_bad_header', 'CSV has no header.', 'error' );
        return;
    }

    $normalized_header = array();
    foreach ( $header as $col ) {
        $col                = preg_replace( '/^\xEF\xBB\xBF/', '', $col );
        $normalized_header[] = strtolower( trim( $col ) );
    }

    $idx_family_id               = array_search( 'family_id', $normalized_header, true );
    $idx_canonical_tag_id        = array_search( 'canonical_tag_id', $normalized_header, true );
    $idx_canonical_label         = array_search( 'canonical_label', $normalized_header, true );
    $idx_tag_id                  = array_search( 'tag_id', $normalized_header, true );
    $idx_tag_label               = array_search( 'tag_label', $normalized_header, true );
    $idx_similarity_to_canonical = array_search( 'similarity_to_canonical', $normalized_header, true );
    $idx_usage_count             = array_search( 'usage_count', $normalized_header, true );
    $idx_entity_label            = array_search( 'entity_label', $normalized_header, true );

    if ( $idx_family_id === false || $idx_canonical_tag_id === false || $idx_canonical_label === false ||
         $idx_tag_id === false || $idx_tag_label === false || $idx_similarity_to_canonical === false ||
         $idx_usage_count === false || $idx_entity_label === false ) {
        fclose( $handle );
        add_settings_error(
            'bf_tf_messages',
            'bf_tf_missing_columns',
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
            $table_name,
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
    if ( isset( $_POST['bf_tf_truncate_table'] ) && $_POST['bf_tf_truncate_table'] === '1' ) {
        $message .= ' (Table truncated first)';
    }

    add_settings_error( 'bf_tf_messages', 'bf_tf_import_success', $message, 'updated' );
}

/**
 * Tag families CSV / usage page.
 */
function bf_tf_render_settings_page() {
    global $wpdb;

    if ( isset( $_POST['bf_tf_import_submit'] ) ) {
        bf_tf_handle_csv_import();
    }

    settings_errors( 'bf_tf_messages' );

    $table_name   = bf_tf_table_name();
    $table_exists = $wpdb->get_var( "SHOW TABLES LIKE '{$table_name}'" );
    $row_count    = 0;

    if ( $table_exists === $table_name ) {
        $row_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM `{$table_name}`" );
    }
    ?>
    <div class="wrap">
        <h1>Tag Families Embeddings</h1>

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
        <p>CSV format: <code>family_id,canonical_tag_id,canonical_label,tag_id,tag_label,similarity_to_canonical,usage_count,entity_label</code></p>

        <form method="post" enctype="multipart/form-data">
            <?php wp_nonce_field( 'bf_tf_import_csv', 'bf_tf_import_nonce' ); ?>

            <table class="form-table">
                <tr>
                    <th><label for="bf_tf_csv">CSV File</label></th>
                    <td><input type="file" id="bf_tf_csv" name="bf_tf_csv" accept=".csv"></td>
                </tr>
                <tr>
                    <th><label for="bf_tf_truncate_table">Truncate table first?</label></th>
                    <td>
                        <label>
                            <input type="checkbox" id="bf_tf_truncate_table" name="bf_tf_truncate_table" value="1">
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

            <h3>Template Function</h3>
            <pre style="background: #f5f5f5; padding: 15px; border: 1px solid #ddd; overflow-x: auto; font-family: monospace; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">$related_tags = bf_get_related_tags( $tag_id, $limit );
foreach ( $related_tags as $tag ) {
    echo '&lt;a href="' . $tag['link'] . '"&gt;' . $tag['name'] . '&lt;/a&gt;';
}</pre>
        </div>
    </div>
    <?php
}

/**
 * PUBLIC API: get related tags for a tag_id.
 */
function bf_get_related_tags( $tag_id = 0, $limit = 5 ) {
    if ( ! $tag_id ) {
        $tag = get_queried_object();
        if ( $tag && ! is_wp_error( $tag ) && isset( $tag->term_id ) ) {
            $tag_id = $tag->term_id;
        }
    }

    if ( ! $tag_id ) {
        return array();
    }

    $rows = bf_tf_get_family_members( $tag_id, $limit );

    $out = array();
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

/**
 * [bf_related_tags] shortcode.
 */
function bf_tf_shortcode( $atts ) {
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

    $related = bf_get_related_tags( $tag_id, (int) $atts['limit'] );

    if ( empty( $related ) ) {
        return '';
    }

    $html = '<div class="bf-related-tags">';

    if ( ! empty( $atts['title'] ) ) {
        $html .= '<h3>' . esc_html( $atts['title'] ) . '</h3>';
    }

    $html .= '<ul>';
    foreach ( $related as $tag ) {
        $html .= '<li><a href="' . esc_url( $tag['link'] ) . '">' . esc_html( $tag['name'] ) . '</a></li>';
    }
    $html .= '</ul></div>';

    return $html;
}
add_shortcode( 'bf_related_tags', 'bf_tf_shortcode' );

/* ####################### // CHUNK_2 #######################  */

/* ####################### CHUNK_3 #######################  */

/* -------------------------------------------------------------------------
 * BF SEMANTIC SEO FEATURES (from functions_specific.php, adapted)
 * ------------------------------------------------------------------------- */

/**
 * Semantic breadcrumbs (HTML).
 * You can call bf_semantic_breadcrumbs() in your theme.
 */
function bf_semantic_breadcrumbs() {
    if ( ! get_option( 'bf_sem_seo_enable_breadcrumbs' ) ) {
        return;
    }

    if ( is_front_page() ) {
        return;
    }

    global $post;

    echo '<nav class="bf-breadcrumbs" aria-label="Breadcrumbs">';
    echo '<a href="' . esc_url( home_url( '/' ) ) . '">Home</a>';

    if ( is_single() && $post ) {
        // Add category
        $categories = get_the_category( $post->ID );
        if ( ! empty( $categories ) ) {
            $primary = $categories[0];
            echo ' &raquo; <a href="' . esc_url( get_category_link( $primary ) ) . '">' . esc_html( $primary->name ) . '</a>';
        }

        echo ' &raquo; <span>' . esc_html( get_the_title( $post ) ) . '</span>';
    } elseif ( is_tag() ) {
        $tag = get_queried_object();
        echo ' &raquo; <span>Tag: ' . esc_html( $tag->name ) . '</span>';
    } elseif ( is_category() ) {
        $cat = get_queried_object();
        echo ' &raquo; <span>Category: ' . esc_html( $cat->name ) . '</span>';
    } elseif ( is_search() ) {
        echo ' &raquo; <span>Search: ' . esc_html( get_search_query() ) . '</span>';
    } elseif ( is_page() && $post ) {
        $ancestors = array_reverse( get_post_ancestors( $post ) );
        foreach ( $ancestors as $ancestor_id ) {
            echo ' &raquo; <a href="' . esc_url( get_permalink( $ancestor_id ) ) . '">' . esc_html( get_the_title( $ancestor_id ) ) . '</a>';
        }
        echo ' &raquo; <span>' . esc_html( get_the_title( $post ) ) . '</span>';
    }

    echo '</nav>';
}

/**
 * Breadcrumb JSON-LD schema.
 */
function bf_breadcrumb_schema() {
    if ( ! get_option( 'bf_sem_seo_enable_schema' ) ) {
        return;
    }

    if ( is_front_page() ) {
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
            $primary = $categories[0];
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
add_action( 'wp_head', 'bf_breadcrumb_schema' );

/**
 * Tag archive JSON-LD schema (simple Topic / CollectionPage).
 */
function bf_tag_archive_schema() {
    if ( ! get_option( 'bf_sem_seo_enable_schema' ) ) {
        return;
    }

    if ( ! is_tag() ) {
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
add_action( 'wp_head', 'bf_tag_archive_schema', 20 );

/* -------------------------------------------------------------------------
 * SEMANTIC SIDEBAR (widget + shortcode)
 * ------------------------------------------------------------------------- */

/**
 * Main semantic sidebar renderer.
 * Relies on bf_get_related_posts() and bf_get_related_tags().
 */
function bf_semantic_sidebar() {
    if ( ! is_single() ) {
        if ( get_option( 'bf_sem_seo_debug' ) ) {
            echo '<div class="semantic-sidebar-widget" style="margin:15px 0;padding:10px;border:1px solid #ddd;background:#fffef5;">';
            echo '<p style="margin:0;font-size:12px;">Not a single post page, semantic sidebar is skipped.</p>';
            echo '</div>';
        }
        return;
    }

    if ( ! get_option( 'bf_sem_seo_enable_sidebar' ) ) {
        return;
    }

    global $post, $wpdb;

    ?>
    <div class="semantic-sidebar-widget" style="margin:15px 0;padding:10px;border:1px solid #ddd;background:#ffffff;">

        <?php if ( get_option( 'bf_sem_seo_debug' ) ) : ?>
        <!-- DEBUG INFO -->
        <div style="background:#fff3cd;padding:10px;margin-bottom:15px;border-left:4px solid #ffc107;font-size:12px;">
            <strong>🔍 Debug Info:</strong><br>
            Post ID: <?php echo (int) $post->ID; ?><br>
            bf_get_related_posts exists: <?php echo function_exists( 'bf_get_related_posts' ) ? '✅ Yes' : '❌ No'; ?><br>
            bf_get_related_tags exists: <?php echo function_exists( 'bf_get_related_tags' ) ? '✅ Yes' : '❌ No'; ?><br>
            <?php
            $tags = get_the_tags( $post->ID );
            echo 'Post has tags: ' . ( $tags ? '✅ Yes (' . count( $tags ) . ')' : '❌ No' ) . '<br>';

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
                $tag_db_count = $wpdb->get_var(
                    $wpdb->prepare(
                        "SELECT COUNT(*) FROM {$wpdb->prefix}tag_families WHERE tag_id = %d",
                        $tags[0]->term_id
                    )
                );
                echo 'Tag family data in DB for first tag: ' . ( $tag_db_count ? '✅ Yes' : '❌ No' ) . '<br>';
            }
            ?>
        </div>
        <?php endif; ?>

        <?php
        // Related posts via embeddings.
        $related_posts = function_exists( 'bf_get_related_posts' ) ? bf_get_related_posts( $post->ID, 5 ) : array();
        if ( ! empty( $related_posts ) ) :
        ?>
            <div class="bf-semantic-block bf-related-posts-block" style="margin-bottom:15px;">
                <h3 style="margin-top:0;">Related Posts IA sidebar</h3>
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
        <?php elseif ( get_option( 'bf_sem_seo_debug' ) ) : ?>
            <p style="font-size:12px;color:#777;"><em>No related posts found in DB for this post.</em></p>
        <?php endif; ?>

        <?php
        // Related tags based on first tag family.
        $tags = get_the_tags( $post->ID );
        if ( $tags ) {
            $first_tag = $tags[0];
            $related_tags = function_exists( 'bf_get_related_tags' ) ? bf_get_related_tags( $first_tag->term_id, 10 ) : array();

            if ( ! empty( $related_tags ) ) :
                ?>
                <div class="bf-semantic-block bf-related-tags-block">
                    <h3>Related Tags IA</h3>
                    <ul>
                        <?php foreach ( $related_tags as $rt ) : ?>
                            <li>
                                <a href="<?php echo esc_url( $rt['link'] ); ?>"><?php echo esc_html( $rt['name'] ); ?></a>
                            </li>
                        <?php endforeach; ?>
                    </ul>
                </div>
                <?php
            elseif ( get_option( 'bf_sem_seo_debug' ) ) :
                ?>
                <p style="font-size:12px;color:#777;"><em>No tag families found for first tag.</em></p>
                <?php
            endif;
        } elseif ( get_option( 'bf_sem_seo_debug' ) ) {
            echo '<p style="font-size:12px;color:#777;"><em>Post has no tags.</em></p>';
        }
        ?>

    </div>
    <?php
}

/**
 * Sidebar shortcode [bf_sidebar].
 */
function bf_semantic_sidebar_shortcode( $atts ) {
    if ( ! get_option( 'bf_sem_seo_enable_sidebar' ) ) {
        return '';
    }

    ob_start();
    bf_semantic_sidebar();
    return ob_get_clean();
}
add_shortcode( 'bf_sidebar', 'bf_semantic_sidebar_shortcode' );

/**
 * Sidebar widget wrapper.
 */
class BF_Semantic_Sidebar_Widget extends WP_Widget {
    public function __construct() {
        parent::__construct(
            'bf_semantic_sidebar_widget',
            'BF Semantic Sidebar',
            array(
                'description' => 'Shows related posts and tags using embeddings-based data.',
            )
        );
    }

    public function widget( $args, $instance ) {
        if ( ! get_option( 'bf_sem_seo_enable_sidebar' ) ) {
            return;
        }

        echo $args['before_widget'];
        bf_semantic_sidebar();
        echo $args['after_widget'];
    }

    public function form( $instance ) {
        echo '<p>This widget automatically shows semantic related content on single posts, based on embeddings DB tables.</p>';
    }
}

function bf_register_semantic_sidebar_widget() {
    register_widget( 'BF_Semantic_Sidebar_Widget' );
}
add_action( 'widgets_init', 'bf_register_semantic_sidebar_widget' );

/* -------------------------------------------------------------------------
 * AUTO FOOTER RELATED CONTENT
 * ------------------------------------------------------------------------- */

/**
 * Append related posts and tags blocks at the end of single post content.
 */

/**
 * Output related posts/tags at the very bottom of the page (footer),
 * instead of filtering the_content to avoid recursion with blocks.
 */
function bf_sem_seo_render_footer_related() {
    if ( ! is_single() || ! is_main_query() ) {
        return;
    }

    if ( is_admin() || doing_action( 'rest_api_init' ) || wp_is_json_request() ) {
        return;
    }

    if ( ! get_option( 'bf_sem_seo_enable_footer' ) ) {
        return;
    }

    global $post;
    if ( ! $post instanceof WP_Post ) {
        return;
    }

    // Avoid running multiple times.
    static $done = false;
    if ( $done ) {
        return;
    }
    $done = true;

    $html = '';

    // RELATED POSTS (small list).
    $related_posts = function_exists( 'bf_get_related_posts' ) ? bf_get_related_posts( $post->ID, 3 ) : array();
    if ( ! empty( $related_posts ) ) {
        $html .= '<div class="bf-related-footer bf-related-footer-posts" style="margin-top:30px;padding-top:15px;border-top:1px solid #ddd;">';
        $html .= '<h3>Related Posts IA</h3><ul>';
        foreach ( $related_posts as $rp ) {
            if ( empty( $rp['permalink'] ) || empty( $rp['title'] ) ) {
                continue;
            }
            $html .= '<li><a href="' . esc_url( $rp['permalink'] ) . '">' . esc_html( $rp['title'] ) . '</a></li>';
        }
        $html .= '</ul></div>';
    }

    // RELATED TAGS.
    $tags = get_the_tags( $post->ID );
    if ( $tags && ! empty( $tags[0]->term_id ) ) {
        $first_tag = $tags[0];
        $related_tags = function_exists( 'bf_get_related_tags' ) ? bf_get_related_tags( $first_tag->term_id, 6 ) : array();

        if ( ! empty( $related_tags ) && is_array( $related_tags ) ) {
            $html .= '<div class="bf-related-footer bf-related-footer-tags" style="margin-top:15px;">';
            $html .= '<h3>Explore Related Tags IA</h3><p>';

            $links = array();
            foreach ( $related_tags as $rt ) {
                if ( empty( $rt['link'] ) || empty( $rt['name'] ) ) {
                    continue;
                }
                $links[] = '<a href="' . esc_url( $rt['link'] ) . '">' . esc_html( $rt['name'] ) . '</a>';
            }

            $html .= implode( ', ', $links );
            $html .= '</p></div>';
        }
    }

    if ( $html === '' ) {
        return;
    }

    echo $html;
}
add_action( 'wp_footer', 'bf_sem_seo_render_footer_related', 20 );



/* ####################### // CHUNK_3 #######################  */

?>
```
