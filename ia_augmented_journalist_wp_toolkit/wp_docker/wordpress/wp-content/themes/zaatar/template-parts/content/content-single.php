<?php
/**
 * Template part for displaying single posts.
 *
 * @package Zaatar
 */
?>

<div class="post-wrapper-hentry">
	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
		<div class="post-content-wrapper post-content-wrapper-single post-content-wrapper-single-post">

			<div class="entry-header-wrapper">
				<header class="entry-header">
					<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
				</header><!-- .entry-header -->

				<div class="entry-meta entry-meta-header-after">
					<?php
					allium_posted_by();
					allium_posted_on();
					allium_post_edit_link();
					?>
				</div><!-- .entry-meta -->

				<?php 
				// Display semantic breadcrumbs
				if ( function_exists( 'semaphore_breadcrumbs' ) ) { semaphore_breadcrumbs(); } ?>
				<!-- .semantic-breadcrumbs -->


				
			</div><!-- .entry-header-wrapper -->

			<div class="entry-content">
				<?php allium_post_thumbnail_single(); ?>
				<?php the_content(); ?>
				<?php
					wp_link_pages( array(
						'before'      => '<div class="page-links"><span class="page-links-title">' . esc_html__( 'Pages:', 'zaatar' ) . '</span>',
						'after'       => '</div>',
						'link_before' => '<span>',
						'link_after'  => '</span>',
					) );
				?>
			</div><!-- .entry-content -->

			<footer class="entry-meta entry-meta-footer">
				<?php allium_entry_footer(); ?>
			</footer><!-- .entry-meta -->

		</div><!-- .post-content-wrapper -->
	</article><!-- #post-## -->
</div><!-- .post-wrapper-hentry -->
