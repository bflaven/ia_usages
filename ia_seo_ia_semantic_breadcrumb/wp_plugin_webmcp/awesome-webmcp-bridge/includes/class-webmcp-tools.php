<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WebMCP_Tools {

    public static function register_rest_routes() {
        $namespace = 'webmcp/v1';

        register_rest_route( $namespace, '/manifest', [
            'methods'             => 'GET',
            'callback'            => [ __CLASS__, 'get_manifest' ],
            'permission_callback' => '__return_true',
        ] );

        register_rest_route( $namespace, '/search', [
            'methods'             => 'GET',
            'callback'            => [ __CLASS__, 'tool_search_posts' ],
            'permission_callback' => '__return_true',
            'args'                => [
                'query'    => [ 'required' => true, 'sanitize_callback' => 'sanitize_text_field' ],
                'category' => [ 'required' => false, 'sanitize_callback' => 'sanitize_text_field' ],
                'limit'    => [ 'required' => false, 'default' => 10, 'sanitize_callback' => 'absint' ],
            ],
        ] );

        register_rest_route( $namespace, '/posts', [
            'methods'             => 'GET',
            'callback'            => [ __CLASS__, 'tool_get_latest' ],
            'permission_callback' => '__return_true',
            'args'                => [
                'category' => [ 'required' => false, 'sanitize_callback' => 'sanitize_text_field' ],
                'count'    => [ 'required' => false, 'default' => 10, 'sanitize_callback' => 'absint' ],
            ],
        ] );

        register_rest_route( $namespace, '/categories', [
            'methods'             => 'GET',
            'callback'            => [ __CLASS__, 'tool_list_categories' ],
            'permission_callback' => '__return_true',
        ] );

        register_rest_route( $namespace, '/post/(?P<id>\d+)/toc', [
            'methods'             => 'GET',
            'callback'            => [ __CLASS__, 'tool_get_toc' ],
            'permission_callback' => '__return_true',
            'args'                => [
                'id' => [ 'required' => true, 'sanitize_callback' => 'absint' ],
            ],
        ] );

        register_rest_route( $namespace, '/post/(?P<id>\d+)/related', [
            'methods'             => 'GET',
            'callback'            => [ __CLASS__, 'tool_get_related' ],
            'permission_callback' => '__return_true',
            'args'                => [
                'id'    => [ 'required' => true, 'sanitize_callback' => 'absint' ],
                'limit' => [ 'required' => false, 'default' => 5, 'sanitize_callback' => 'absint' ],
            ],
        ] );
    }

    public static function get_manifest( WP_REST_Request $request ) {
        return rest_ensure_response( WebMCP_Manifest::build() );
    }

    public static function tool_search_posts( WP_REST_Request $request ) {
        $enabled = get_option( 'webmcp_tools', [] );
        if ( empty( $enabled['search_posts'] ) ) {
            return new WP_Error( 'tool_disabled', 'Tool disabled', [ 'status' => 403 ] );
        }

        $limit = min( (int) $request->get_param( 'limit' ), 20 );
        $args  = [
            's'              => $request->get_param( 'query' ),
            'posts_per_page' => $limit,
            'post_status'    => 'publish',
        ];

        $cat_slug = $request->get_param( 'category' );
        if ( $cat_slug ) {
            $args['category_name'] = $cat_slug;
        }

        $query = new WP_Query( $args );
        return rest_ensure_response( self::format_posts( $query->posts ) );
    }

    public static function tool_get_latest( WP_REST_Request $request ) {
        $enabled = get_option( 'webmcp_tools', [] );
        if ( empty( $enabled['get_latest'] ) ) {
            return new WP_Error( 'tool_disabled', 'Tool disabled', [ 'status' => 403 ] );
        }

        $count = min( (int) $request->get_param( 'count' ), 20 );
        $args  = [
            'posts_per_page' => $count,
            'post_status'    => 'publish',
            'orderby'        => 'date',
            'order'          => 'DESC',
        ];

        $cat_slug = $request->get_param( 'category' );
        if ( $cat_slug ) {
            $args['category_name'] = $cat_slug;
        }

        $query = new WP_Query( $args );
        return rest_ensure_response( self::format_posts( $query->posts ) );
    }

    public static function tool_list_categories( WP_REST_Request $request ) {
        $enabled = get_option( 'webmcp_tools', [] );
        if ( empty( $enabled['list_categories'] ) ) {
            return new WP_Error( 'tool_disabled', 'Tool disabled', [ 'status' => 403 ] );
        }

        $cats = get_categories( [ 'hide_empty' => true ] );
        $out  = [];
        foreach ( $cats as $cat ) {
            $out[] = [
                'id'          => $cat->term_id,
                'name'        => $cat->name,
                'slug'        => $cat->slug,
                'description' => $cat->description,
                'count'       => $cat->count,
                'url'         => get_category_link( $cat->term_id ),
            ];
        }
        return rest_ensure_response( $out );
    }

    public static function tool_get_toc( WP_REST_Request $request ) {
        $enabled = get_option( 'webmcp_tools', [] );
        if ( empty( $enabled['get_toc'] ) ) {
            return new WP_Error( 'tool_disabled', 'Tool disabled', [ 'status' => 403 ] );
        }

        $post = get_post( (int) $request->get_param( 'id' ) );
        if ( ! $post || $post->post_status !== 'publish' ) {
            return new WP_Error( 'not_found', 'Post not found', [ 'status' => 404 ] );
        }

        preg_match_all( '/<h([2-4])[^>]*>(.*?)<\/h\1>/i', $post->post_content, $matches );
        $toc = [];
        foreach ( $matches[2] as $i => $heading ) {
            $toc[] = [
                'level'   => (int) $matches[1][ $i ],
                'heading' => wp_strip_all_tags( $heading ),
            ];
        }

        return rest_ensure_response( [
            'post_id'    => $post->ID,
            'post_title' => $post->post_title,
            'url'        => get_permalink( $post->ID ),
            'toc'        => $toc,
        ] );
    }

    public static function tool_get_related( WP_REST_Request $request ) {
        $enabled = get_option( 'webmcp_tools', [] );
        if ( empty( $enabled['get_related'] ) ) {
            return new WP_Error( 'tool_disabled', 'Tool disabled', [ 'status' => 403 ] );
        }

        $post_id = (int) $request->get_param( 'id' );
        $limit   = min( (int) $request->get_param( 'limit' ), 10 );
        $post    = get_post( $post_id );

        if ( ! $post || $post->post_status !== 'publish' ) {
            return new WP_Error( 'not_found', 'Post not found', [ 'status' => 404 ] );
        }

        $cats  = wp_get_post_categories( $post_id );
        $query = new WP_Query( [
            'posts_per_page'      => $limit,
            'post_status'         => 'publish',
            'post__not_in'        => [ $post_id ],
            'category__in'        => $cats,
            'ignore_sticky_posts' => 1,
        ] );

        return rest_ensure_response( self::format_posts( $query->posts ) );
    }

    private static function format_posts( array $posts ) {
        $out = [];
        foreach ( $posts as $post ) {
            $cats = wp_get_post_categories( $post->ID, [ 'fields' => 'names' ] );
            $out[] = [
                'id'      => $post->ID,
                'title'   => $post->post_title,
                'slug'    => $post->post_name,
                'url'     => get_permalink( $post->ID ),
                'date'    => $post->post_date,
                'excerpt' => wp_trim_words( $post->post_excerpt ?: $post->post_content, 30 ),
                'cats'    => $cats,
            ];
        }
        return $out;
    }
}
