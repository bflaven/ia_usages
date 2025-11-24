<?php
/**
 * Template Name: Category Cloud Page
 * Description: Displays a category cloud with up to 100 most used categories.
 * The template for displaying archive pages.
 * Learn more: http://codex.wordpress.org/Template_Hierarchy
 *
 * @package Zaatar
 */

/**
 */

get_header(); ?>

<style>
.category-cloud a {
    display: inline-block;
    margin: 6px 8px 6px 0;
    padding: 6px 14px;
    background: #d6e3f3;
    color: #2a2a2a;
    border-radius: 6px;
    text-decoration: none;
    transition: background 0.2s, color 0.2s;
}
.category-cloud a:hover {
    background: #8bc6e6;
    color: #333;
}
</style>
    <div class="page-header-wrapper page-header-wrapper-archive">
        <div class="container">

            <div class="row">
                <div class="col">

                    <header class="page-header">
                        <?php
                        if ( have_posts() ) :
                            the_archive_title( '<h1 class="page-title">', '</h1>' );
                            the_archive_description( '<div class="taxonomy-description">', '</div>' );
                        else :
                            printf( '<h1 class="page-title"><span class="page-title-label">%1$s</span></h1>', esc_html__( 'Nothing Found', 'zaatar' ) );
                        endif;
                        ?>
                    </header><!-- .page-header -->

                </div><!-- .col -->
            </div><!-- .row -->

        </div><!-- .container -->
    </div><!-- .page-header-wrapper -->

    <div class="site-content-inside">
        <div class="container">
            <div class="row">
                <div id="primary" class="content-area <?php allium_layout_class( 'content' ); ?>">
                    <main id="main" class="site-main" role="main">

                    <div class="category-cloud">
        <?php
        // Get categories ordered by post count
        $categories = get_categories(array(
            'orderby' => 'count',
            'order' => 'DESC',
            'number' => 100,
            'hide_empty' => true,
        ));
        // Find min/max counts for font-size scaling
        $counts = wp_list_pluck($categories, 'count');
        $min = min($counts);
        $max = max($counts);
        $min_size = 12;  // px
        $max_size = 40;  // px

        foreach ($categories as $cat) {
            // Scale font size based on count
            $size = $min_size;
            if ($max > $min) {
                $size += ($cat->count - $min) * ($max_size - $min_size) / ($max - $min);
            }
            echo sprintf(
                '<a style="font-size:%.1fpx" href="%s">%s</a> ',
                $size,
                esc_url(get_category_link($cat->term_id)),
                esc_html($cat->name)
            );
        }
        ?>
    </div>

                    </main><!-- #main -->
                </div><!-- #primary -->

                <?php get_sidebar(); ?>

            </div><!-- .row -->
        </div><!-- .container -->
    </div><!-- .site-content-inside -->

<?php get_footer(); ?>
