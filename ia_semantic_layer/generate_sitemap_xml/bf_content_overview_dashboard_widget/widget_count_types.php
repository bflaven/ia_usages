<?php
/*
Plugin Name: Content Overview Dashboard Widget
Description: Displays counts of posts, pages, tags, categories, custom post types and taxonomies in the dashboard.
Version: 1.1
Author: Bruno Flaven
*/

add_action('wp_dashboard_setup', 'content_overview_add_dashboard_widget');

function content_overview_add_dashboard_widget() {
    wp_add_dashboard_widget('content_overview_widget', 'Content Overview', 'content_overview_widget_display');
}

function content_overview_widget_display() {
    // Built-in content types
    $total_posts = wp_count_posts('post')->publish;
    $total_pages = wp_count_posts('page')->publish;

    // Built-in taxonomies
    $total_categories = wp_count_terms('category');
    $total_tags = wp_count_terms('post_tag');

    // Custom Post Types
    $custom_post_types = array('bf_videos_manager', 'bf_quotes_manager', 'clients', 'product_for_sale');


    // Add more CPTs as needed
    echo "<ul>";
    echo "<li>Posts: {$total_posts}</li>";
    echo "<li>Pages: {$total_pages}</li>";
    echo "<li>Categories: {$total_categories}</li>";
    echo "<li>Tags: {$total_tags}</li>";

    foreach($custom_post_types as $cpt) {
        $count = wp_count_posts($cpt)->publish;
        echo "<li>" . ucfirst($cpt) . ": {$count}</li>";
    }


    // Custom Taxonomies
    $custom_taxonomies = array('bf_videos_manager_tag', 'bf_videos_manager_cat', 'bf_quotes_manager_author', 'bf_quotes_manager_flavor', 'product_for_sale_kw', 'product_for_sale_author');



    foreach($custom_taxonomies as $tax) {
        $tax_count = wp_count_terms($tax);
        echo "<li>" . ucfirst(str_replace('-', ' ', $tax)) . ": {$tax_count}</li>";
    }
    echo "</ul>";
}
?>
