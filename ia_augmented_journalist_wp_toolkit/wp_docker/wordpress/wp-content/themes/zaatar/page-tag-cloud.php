<?php
/**
 * Template Name: Tag Cloud Page
 * Description: Displays a tag cloud with up to 100 most used tags.
 * The template for displaying archive pages.
 * Learn more: http://codex.wordpress.org/Template_Hierarchy
 *
 * @package Zaatar
 */

/**
 */

get_header(); ?>

<style>
.tag-cloud a {
    display: inline-block;
    margin: 6px 8px 6px 0;
    padding: 6px 14px;
    background: #f3ecd6;
    color: #2a2a2a;
    border-radius: 6px;
    text-decoration: none;
    transition: background 0.2s, color 0.2s;
}
.tag-cloud a:hover {
    background: #e6c68b;
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

				<div class="tag-cloud">
        <?php
        wp_tag_cloud(array(
            'smallest' => 12,          // Minimum font size
            'largest'  => 40,          // Maximum font size
            'unit'     => 'px',
            'number'   => 100,         // Maximum number of tags
            'orderby'  => 'count',     // Order by usage count
            'order'    => 'DESC'
        ));
        ?>
    </div>

					</main><!-- #main -->
				</div><!-- #primary -->

				<?php get_sidebar(); ?>

			</div><!-- .row -->
		</div><!-- .container -->
	</div><!-- .site-content-inside -->

<?php get_footer(); ?>
