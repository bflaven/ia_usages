<?php
/**
 * The Template for displaying all single posts.
 *
 * @package Zaatar
 */

get_header(); ?>

	<div class="site-content-inside">
		<div class="container">
			<div class="row">

				<div id="primary" class="content-area <?php allium_layout_class( 'content' ); ?>">
					<main id="main" class="site-main" role="main">

						<div id="post-wrapper" class="post-wrapper post-wrapper-single post-wrapper-single-post">
						<?php /* Start the Loop */ ?>

						<?php 

						while ( have_posts() ) : the_post();
							print('<!-- '.get_post_type().' -->');

							/*
							bf_quotes_manager
							clients
							product_for_sale
							post

							 */

							
					
					if ( in_array(get_post_type(), array('bf_quotes_manager'))) {

							get_template_part( 'template-parts/content/content', 'bf_quotes_manager'); 
							allium_the_post_pagination(); 
							
					
					} else if ( in_array(get_post_type(), array('bf_videos_manager'))) { 
							get_template_part( 'template-parts/content/content', 'bf_videos_manager'); 
							allium_the_post_pagination();
							

					} else if ( in_array(get_post_type(), array('product_for_sale'))) { 
							get_template_part( 'template-parts/content/content', 'product_for_sale'); 
							allium_the_post_pagination();
							

					} else if ( in_array(get_post_type(), array('clients'))) { 
							get_template_part( 'template-parts/content/content', 'clients'); 
							allium_the_post_pagination();
							

					} else {
						get_template_part( 'template-parts/content/content', 'single' );
						get_template_part( 'template-parts/post/author', 'bio' ); 
							get_template_part( 'template-parts/post/related', 'posts' );
							allium_the_post_pagination(); 
							

					 }

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
