<?php
/**
 * The default template for displaying content
 *
 * @package Zaatar
 */
?>

<div class="post-wrapper-hentry">
	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
		<div class="post-content-wrapper post-content-wrapper-archive">

			<?php allium_post_thumbnail(); ?>

			<div class="entry-data-wrapper">
				<div class="entry-header-wrapper">
					<?php if ( 'post' === get_post_type() ) : // For Posts ?>
						<div class="entry-meta entry-meta-header-before">
							<?php
							allium_post_first_category();
							allium_posted_on();
							allium_sticky_post();
							?>
						</div><!-- .entry-meta -->

						<?php
						// Show semantic breadcrumbs only on single posts, not in archives.
						if ( is_single() && function_exists( 'semaphore_breadcrumbs' ) ) {
							semaphore_breadcrumbs();
						}
						?>
						<!-- .semantic-breadcrumbs -->
					<?php endif; ?>

					<header class="entry-header">
						<?php the_title( sprintf( '<h1 class="entry-title"><a href="%1$s" rel="bookmark">', esc_url( get_permalink() ) ), '</a></h1>' ); ?>
					</header><!-- .entry-header -->
				</div><!-- .entry-header-wrapper -->

				<?php if ( allium_has_excerpt() ) : ?>
					<div class="entry-summary">
						<?php the_excerpt(); ?>
					</div><!-- .entry-summary -->
				<?php endif; ?>

				<?php allium_read_more_link(); ?>
			</div><!-- .entry-data-wrapper -->

		</div><!-- .post-content-wrapper -->
	</article><!-- #post-## -->
</div><!-- .post-wrapper-hentry -->
