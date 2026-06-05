<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WebMCP_Manifest {

    public static function inject_manifest() {
        if ( ! get_option( 'webmcp_enabled', 1 ) ) {
            return;
        }
        $manifest = self::build();
        echo '<script type="application/mcp+json">' . wp_json_encode( $manifest ) . '</script>' . "\n";
        echo '<link rel="mcp-manifest" href="' . esc_url( rest_url( 'webmcp/v1/manifest' ) ) . '">' . "\n";
    }

    public static function build() {
        $enabled   = get_option( 'webmcp_tools', [] );
        $rest_base = rest_url( 'webmcp/v1' );
        $tools     = [];

        if ( ! empty( $enabled['search_posts'] ) ) {
            $tools[] = [
                'name'        => 'search_posts',
                'description' => 'Search published blog posts by keyword, with optional category filter.',
                'parameters'  => [
                    'query'    => [ 'type' => 'string',  'required' => true,  'description' => 'Search keyword(s)' ],
                    'category' => [ 'type' => 'string',  'required' => false, 'description' => 'Category slug filter' ],
                    'limit'    => [ 'type' => 'integer', 'required' => false, 'default' => 10, 'description' => 'Max results (capped at 20)' ],
                ],
                'action' => [
                    'type'   => 'http',
                    'method' => 'GET',
                    'url'    => $rest_base . '/search',
                ],
            ];
        }

        if ( ! empty( $enabled['get_latest'] ) ) {
            $tools[] = [
                'name'        => 'get_latest_posts',
                'description' => 'Retrieve the most recent published posts, optionally filtered by category.',
                'parameters'  => [
                    'category' => [ 'type' => 'string',  'required' => false, 'description' => 'Category slug' ],
                    'count'    => [ 'type' => 'integer', 'required' => false, 'default' => 10, 'description' => 'Number of posts (capped at 20)' ],
                ],
                'action' => [
                    'type'   => 'http',
                    'method' => 'GET',
                    'url'    => $rest_base . '/posts',
                ],
            ];
        }

        if ( ! empty( $enabled['list_categories'] ) ) {
            $tools[] = [
                'name'        => 'list_categories',
                'description' => 'List all non-empty categories with post counts and URLs.',
                'parameters'  => [],
                'action'      => [
                    'type'   => 'http',
                    'method' => 'GET',
                    'url'    => $rest_base . '/categories',
                ],
            ];
        }

        if ( ! empty( $enabled['get_toc'] ) ) {
            $tools[] = [
                'name'        => 'get_post_toc',
                'description' => 'Extract the table of contents (H2–H4 headings) from a post.',
                'parameters'  => [
                    'id' => [ 'type' => 'integer', 'required' => true, 'description' => 'WordPress post ID' ],
                ],
                'action' => [
                    'type'     => 'http',
                    'method'   => 'GET',
                    'url'      => $rest_base . '/post/{id}/toc',
                    'url_vars' => [ 'id' ],
                ],
            ];
        }

        if ( ! empty( $enabled['get_related'] ) ) {
            $tools[] = [
                'name'        => 'get_related_posts',
                'description' => 'Get posts related to a given post (same categories).',
                'parameters'  => [
                    'id'    => [ 'type' => 'integer', 'required' => true,  'description' => 'WordPress post ID' ],
                    'limit' => [ 'type' => 'integer', 'required' => false, 'default' => 5, 'description' => 'Max results (capped at 10)' ],
                ],
                'action' => [
                    'type'     => 'http',
                    'method'   => 'GET',
                    'url'      => $rest_base . '/post/{id}/related',
                    'url_vars' => [ 'id' ],
                ],
            ];
        }

        return [
            'schema_version' => '0.1',
            'name'           => get_bloginfo( 'name' ),
            'description'    => get_bloginfo( 'description' ),
            'url'            => get_site_url(),
            'manifest_url'   => rest_url( 'webmcp/v1/manifest' ),
            'tools'          => $tools,
        ];
    }
}
