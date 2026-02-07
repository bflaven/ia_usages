<?php
/**
 * The template used for displaying page content in page.php
 *
 * @package Zaatar
 */
?>

<div class="post-wrapper-hentry">


	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
		<div class="post-content-wrapper post-content-wrapper-single post-content-wrapper-single-page">

			<div class="entry-header-wrapper">
				<header class="entry-header">
					<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
				</header><!-- .entry-header -->

	
				<?php if ( allium_has_post_edit_link() ) : ?>
				<div class="entry-meta entry-meta-header-after">
					<?php allium_post_edit_link(); ?>
				</div><!-- .entry-meta -->
				<?php endif; ?>
			</div><!-- .entry-header-wrapper -->

			<div class="entry-content">
				
				<?php echo do_shortcode( '[captain_achab_anchor_fr]' ); ?>
	

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

			<?php if ( allium_has_post_edit_link() ) : ?>
			<footer class="entry-meta entry-meta-footer">
				<?php allium_entry_footer(); ?>
			</footer><!-- .entry-meta -->
			<?php endif; ?>

		</div><!-- .post-content-wrapper -->
	</article><!-- #post-## -->
</div><!-- .post-wrapper-hentry -->
