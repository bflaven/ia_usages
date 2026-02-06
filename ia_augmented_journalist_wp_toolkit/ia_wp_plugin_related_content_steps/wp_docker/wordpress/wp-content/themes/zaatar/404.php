<?php
/**
 * The template for displaying 404 pages (not found).
 *
 * @package Zaatar
 */

get_header(); ?>

	<div class="page-header-wrapper page-header-wrapper-404">
		<div class="container">

			<div class="row">
				<div class="col">

					<header class="page-header">
						<?php printf( '<h1 class="page-title"><span class="page-title-label">%1$s</span></h1>', esc_html__( 'Oops! That page can&rsquo;t be found.', 'zaatar' ) ); ?>
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

						<div class="post-wrapper post-wrapper-single post-wrapper-single-404">
							<?php get_template_part( 'template-parts/content/content', '404' ); ?>
						</div><!-- .post-wrapper -->

					</main><!-- #main -->
				</div><!-- #primary -->

				<?php get_sidebar(); ?>

			</div><!-- .row -->
		</div><!-- .container -->
	</div><!-- .site-content-inside -->

<?php get_footer(); ?>
