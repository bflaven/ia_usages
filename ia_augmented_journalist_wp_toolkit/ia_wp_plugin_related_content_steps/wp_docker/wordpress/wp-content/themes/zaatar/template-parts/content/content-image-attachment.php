<?php
/**
 * The default template for displaying content
 *
 * @package Zaatar
 */
?>

<div class="post-wrapper-hentry">
	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
		<div class="post-content-wrapper post-content-wrapper-single post-content-wrapper-single-image-attachment">

			<?php
			// Retrieve attachment metadata.
			$allium_metadata = wp_get_attachment_metadata();
			?>

			<div class="entry-header-wrapper">
				<header class="entry-header">
					<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
				</header><!-- .entry-header -->

				<div class="entry-meta entry-meta-header-after">
					<?php allium_posted_on(); ?>
					<?php if ( $post->post_parent ) : ?>
					<span class="parent-post-link entry-meta-icon">
						<a href="<?php echo esc_url( get_permalink( $post->post_parent ) ); ?>" rel="gallery"><?php echo esc_html( get_the_title( $post->post_parent ) ); ?></a>
					</span>
					<?php endif; ?>
					<span class="full-size-link entry-meta-icon">
						<a href="<?php echo esc_url( wp_get_attachment_url() ); ?>" target="_blank"><?php echo esc_html( $allium_metadata['width'] ); ?> &times; <?php echo esc_html( $allium_metadata['height'] ); ?></a>
					</span>
					<?php allium_post_edit_link(); ?>
					</ul>
				</div><!-- .entry-meta -->
			</div><!-- .entry-header-wrapper -->

			<div class="entry-attachment">
				<div class="attachment">
					<?php allium_the_attached_image(); ?>
				</div><!-- .attachment -->

				<?php if ( has_excerpt() ) : ?>
				<div class="entry-caption">
					<?php the_excerpt(); ?>
				</div><!-- .entry-caption -->
				<?php endif; ?>
			</div><!-- .entry-attachment -->

			<div class="entry-content entry-content-attachment">
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
				<?php edit_post_link( esc_html__( 'Edit', 'zaatar' ), '<span class="edit-link">', '</span>' ); ?>
			</footer><!-- .entry-meta -->
			<?php endif; ?>

		</div><!-- .post-content-wrapper -->
	</article><!-- #post-## -->
</div><!-- .post-wrapper-hentry -->
