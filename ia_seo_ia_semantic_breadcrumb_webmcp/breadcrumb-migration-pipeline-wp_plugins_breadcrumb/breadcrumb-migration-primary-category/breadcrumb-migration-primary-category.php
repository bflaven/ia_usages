<?php
/*
Plugin Name: Breadcrumb Migration - Primary Category
Description: Related to the plugin Breadcrumb Migration. Allows selecting a primary category per post + bulk setting/clearing it.
Version: 1.1.0
Author: Bruno Flaven + Perplexity
*/

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class BF_Primary_Category {

    const META_KEY = '_primary_category_id';
    const OPTION_BULK_CAT = '_bf_primary_category_bulk_cat';

    public function __construct() {
        // Meta box
        add_action( 'add_meta_boxes', array( $this, 'add_meta_box' ) );
        add_action( 'save_post', array( $this, 'save_meta_box' ) );

        // Bulk actions
        add_filter( 'bulk_actions-edit-post', array( $this, 'register_bulk_actions' ) );
        add_filter( 'handle_bulk_actions-edit-post', array( $this, 'handle_bulk_actions' ), 10, 3 );

        // Capture selected bulk category BEFORE bulk handler runs
        add_action( 'load-edit.php', array( $this, 'capture_bulk_category_selection' ) );

        // Admin notice after bulk
        add_action( 'admin_notices', array( $this, 'admin_notices' ) );

        // Add bulk category dropdown to posts list
        add_action( 'restrict_manage_posts', array( $this, 'render_bulk_category_dropdown' ), 10, 2 );
    }

    /**
     * Add Primary Category meta box to post edit screen.
     */
    public function add_meta_box() {
        add_meta_box(
            'bf-primary-category',
            __( 'Primary Category', 'bf-primary-category' ),
            array( $this, 'render_meta_box' ),
            'post',
            'side',
            'default'
        );
    }

    /**
     * Render the meta box content.
     */
    public function render_meta_box( $post ) {
        wp_nonce_field( 'bf_primary_category_nonce', 'bf_primary_category_nonce' );

        $current_primary = (int) get_post_meta( $post->ID, self::META_KEY, true );
        $categories      = get_the_category( $post->ID );

        echo '<p>' . esc_html__( 'Choose one primary category among the categories assigned to this post.', 'bf-primary-category' ) . '</p>';

        // Radio: no primary category
        printf(
            '<p><label><input type="radio" name="bf_primary_category" value="0" %s /> %s</label></p>',
            checked( 0, $current_primary, false ),
            esc_html__( 'No primary category', 'bf-primary-category' )
        );

        if ( empty( $categories ) ) {
            echo '<p><em>' . esc_html__( 'This post has no categories yet.', 'bf-primary-category' ) . '</em></p>';
            return;
        }

        foreach ( $categories as $cat ) {
            printf(
                '<p><label><input type="radio" name="bf_primary_category" value="%1$d" %2$s /> %3$s</label></p>',
                (int) $cat->term_id,
                checked( (int) $cat->term_id, $current_primary, false ),
                esc_html( $cat->name )
            );
        }
    }

    /**
     * Save the selected primary category when the post is saved.
     */
    public function save_meta_box( $post_id ) {
        // Autosave / revisions / no nonce = bail
        if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
            return;
        }

        if ( ! isset( $_POST['bf_primary_category_nonce'] ) || ! wp_verify_nonce( $_POST['bf_primary_category_nonce'], 'bf_primary_category_nonce' ) ) {
            return;
        }

        if ( ! current_user_can( 'edit_post', $post_id ) ) {
            return;
        }

        if ( ! isset( $_POST['bf_primary_category'] ) ) {
            return;
        }

        $primary_id = (int) $_POST['bf_primary_category'];

        // 0 means: no primary category
        if ( $primary_id <= 0 ) {
            delete_post_meta( $post_id, self::META_KEY );
            return;
        }

        // Ensure that the primary category is actually assigned to this post
        $categories = get_the_category( $post_id );
        $cat_ids    = wp_list_pluck( (array) $categories, 'term_id' );

        if ( in_array( $primary_id, $cat_ids, true ) ) {
            update_post_meta( $post_id, self::META_KEY, $primary_id );
        } else {
            // If selected category is not attached anymore, remove the meta
            delete_post_meta( $post_id, self::META_KEY );
        }
    }

    /**
     * Add custom bulk actions.
     */
    public function register_bulk_actions( $bulk_actions ) {
        $bulk_actions['bf_set_primary_category']   = __( 'Set primary category…', 'bf-primary-category' );
        $bulk_actions['bf_clear_primary_category'] = __( 'Clear primary category', 'bf-primary-category' );
        return $bulk_actions;
    }

    /**
     * Capture selected bulk category from the dropdown before the bulk action handler.
     *
     * This runs on load-edit.php so we can store the chosen category in an option
     * that handle_bulk_actions-edit-post can read reliably.
     */
    public function capture_bulk_category_selection() {
        $screen = get_current_screen();
        if ( ! $screen || 'edit-post' !== $screen->id ) {
            return;
        }

        if ( isset( $_REQUEST['bf_primary_category_bulk'] ) ) {
            $cat_id = (int) $_REQUEST['bf_primary_category_bulk'];
            if ( $cat_id > 0 ) {
                update_option( self::OPTION_BULK_CAT, $cat_id );
            } else {
                delete_option( self::OPTION_BULK_CAT );
            }
        }
    }

    /**
     * Handle bulk actions for posts.
     */
    public function handle_bulk_actions( $redirect_url, $action, $post_ids ) {
        if ( $action === 'bf_set_primary_category' ) {

            $cat_id = (int) get_option( self::OPTION_BULK_CAT, 0 );

            if ( $cat_id > 0 ) {
                foreach ( $post_ids as $post_id ) {
                    // Optional: only set if the post has that category attached.
                    $categories = get_the_category( $post_id );
                    $cat_ids    = wp_list_pluck( (array) $categories, 'term_id' );

                    if ( in_array( $cat_id, $cat_ids, true ) ) {
                        update_post_meta( $post_id, self::META_KEY, $cat_id );
                    } else {
                        // If you prefer to force-assign anyway, you could call wp_set_post_categories() here.
                        // For now we skip posts that don't have that category.
                    }
                }

                $redirect_url = add_query_arg( 'bf_primary_category_bulk_set', count( $post_ids ), $redirect_url );
            }

        } elseif ( $action === 'bf_clear_primary_category' ) {

            foreach ( $post_ids as $post_id ) {
                delete_post_meta( $post_id, self::META_KEY );
            }

            $redirect_url = add_query_arg( 'bf_primary_category_bulk_cleared', count( $post_ids ), $redirect_url );
        }

        return $redirect_url;
    }

    /**
     * Show admin notices after bulk actions.
     */
    public function admin_notices() {
        if ( isset( $_GET['bf_primary_category_bulk_set'] ) ) {
            $count = (int) $_GET['bf_primary_category_bulk_set'];
            printf(
                '<div class="notice notice-success is-dismissible"><p>%s</p></div>',
                esc_html( sprintf( _n( 'Primary category set for %d post.', 'Primary category set for %d posts.', $count, 'bf-primary-category' ), $count ) )
            );
        }

        if ( isset( $_GET['bf_primary_category_bulk_cleared'] ) ) {
            $count = (int) $_GET['bf_primary_category_bulk_cleared'];
            printf(
                '<div class="notice notice-success is-dismissible"><p>%s</p></div>',
                esc_html( sprintf( _n( 'Primary category cleared for %d post.', 'Primary category cleared for %d posts.', $count, 'bf-primary-category' ), $count ) )
            );
        }
    }

    /**
     * Render the bulk category dropdown above the posts list.
     */
    public function render_bulk_category_dropdown( $post_type, $which ) {
        if ( 'post' !== $post_type ) {
            return;
        }

        // Only show on the top filter row to avoid duplication.
        if ( 'top' !== $which ) {
            return;
        }

        if ( ! current_user_can( 'edit_posts' ) ) {
            return;
        }

        $selected = isset( $_REQUEST['bf_primary_category_bulk'] ) ? (int) $_REQUEST['bf_primary_category_bulk'] : 0;

        wp_dropdown_categories( array(
            'show_option_none'  => __( '— Select primary category for bulk —', 'bf-primary-category' ),
            'option_none_value' => 0,
            'hide_empty'        => 0,
            'name'              => 'bf_primary_category_bulk',
            'id'                => 'bf_primary_category_bulk',
            'taxonomy'          => 'category',
            'selected'          => $selected,
        ) );
    }

}

/**
 * Helper: Get primary category term for a post.
 *
 * @param int|null $post_id
 * @return WP_Term|null
 */
function bf_get_primary_category( $post_id = null ) {
    if ( ! $post_id ) {
        $post_id = get_the_ID();
    }

    if ( ! $post_id ) {
        return null;
    }

    $primary_id = (int) get_post_meta( $post_id, BF_Primary_Category::META_KEY, true );
    if ( $primary_id <= 0 ) {
        return null;
    }

    $term = get_term( $primary_id, 'category' );
    if ( $term && ! is_wp_error( $term ) ) {
        return $term;
    }

    return null;
}

// Initialize plugin.
new BF_Primary_Category();


