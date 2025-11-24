<?php
/*
Plugin Name: API Enable All Custom Types
Description: Enables REST API access for all specified custom post types and taxonomies.
Version: 1.0
Author: Bruno Flaven
*/

// Force REST API support for existing custom post types
add_filter( 'register_post_type_args', function( $args, $post_type ) {
    $enabled_post_types = [
        'bf_videos_manager'     => 'bf_videos_manager',
        'bf_quotes_manager'     => 'bf_quotes_manager',
        'clients'               => 'clients',
        'product_for_sale'      => 'product_for_sale',
    ];
    if ( isset( $enabled_post_types[ $post_type ] ) ) {
        $args['show_in_rest'] = true;
        $args['rest_base'] = $enabled_post_types[ $post_type ];
    }
    return $args;
}, 10, 2 );

// Force REST API support for custom taxonomies
add_filter( 'register_taxonomy_args', function( $args, $taxonomy ) {
    $enabled_taxonomies = [
        'bf_videos_manager_tag'    => 'bf_videos_manager_tag',
        'bf_videos_manager_cat'    => 'bf_videos_manager_cat',
        'bf_quotes_manager_author' => 'bf_quotes_manager_author',
        'bf_quotes_manager_flavor' => 'bf_quotes_manager_flavor',
        'product_for_sale_kw'      => 'product_for_sale_kw',
        'product_for_sale_author'  => 'product_for_sale_author'
    ];
    if ( isset( $enabled_taxonomies[ $taxonomy ] ) ) {
        $args['show_in_rest'] = true;
        $args['rest_base'] = $enabled_taxonomies[ $taxonomy ];
    }
    return $args;
}, 10, 2 );

// Optional: Register post types and taxonomies if not present (for demo/testing)
add_action('init', function() {
    // Register dummy CPTs if needed (remove if CPTs already exist)
    // register_post_type( ... ); // Your code here for registering new CPTs or taxonomies
});


/*
/wp-json/wp/v2/bf_videos_manager
/wp-json/wp/v2/bf_videos_manager_tag
/wp-json/wp/v2/product_for_sale_author
 
bf_videos_manager
bf_quotes_manager
clients
product_for_sale

https://flaven.fr/wp-json/wp/v2/bf_videos_manager?per_page=20&page=1&orderby=date&order=desc

https://flaven.fr/wp-json/wp/v2/bf_quotes_manager?per_page=20&page=1&orderby=date&order=desc

https://flaven.fr/wp-json/wp/v2/clients?per_page=20&page=1&orderby=date&order=desc

https://flaven.fr/wp-json/wp/v2/product_for_sale?per_page=20&page=1&orderby=date&order=desc

https://flaven.fr/wp-json/wp/v2/bf_videos_manager_tag
https://flaven.fr/wp-json/wp/v2/bf_videos_manager_cat
https://flaven.fr/wp-json/wp/v2/bf_quotes_manager_author
https://flaven.fr/wp-json/wp/v2/bf_quotes_manager_flavor
https://flaven.fr/wp-json/wp/v2/product_for_sale_kw
https://flaven.fr/wp-json/wp/v2/product_for_sale_author


*/