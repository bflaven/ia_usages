<?php
/**
 * The template for displaying image attachments
 *
 * @package Zaatar
 */

get_header(); ?>

	<div class="site-content-inside">
		<div class="container">
			<div class="row">

				<div id="primary" class="content-area <?php allium_layout_class( 'content' ); ?>">
					<main id="main" class="site-main" role="main">

						<div id="post-wrapper" class="post-wrapper post-wrapper-single post-wrapper-single-image-attachment">
						<?php while ( have_posts() ) : the_post(); ?>

							<?php get_template_part( 'template-parts/content/content', 'image-attachment' ); ?>

							<nav id="image-navigation" class="navigation image-navigation">
								<div class="nav-links">
									<div class="previous-image nav-previous"><?php previous_image_link( false, esc_html__( 'Previous Image', 'zaatar' ) ); ?></div>
									<div class="next-image nav-next"><?php next_image_link( false, esc_html__( 'Next Image', 'zaatar' ) ); ?></div>
								</div><!-- .nav-links -->
							</nav><!-- #image-navigation -->

							<?php
								// If comments are open or we have at least one comment, load up the comment template
								if ( comments_open() || '0' != get_comments_number() ) :
									comments_template();
								endif;
							?>

						<?php endwhile; // end of the loop. ?>
						</div><!-- .post-wrapper -->

					</main><!-- #main -->
				</div><!-- #primary -->

				<?php get_sidebar(); ?>

			</div><!-- .row -->
		</div><!-- .container -->
	</div><!-- .site-content-inside -->

<?php get_footer(); ?>
