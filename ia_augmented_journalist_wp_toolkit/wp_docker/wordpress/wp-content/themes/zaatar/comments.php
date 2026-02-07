<?php
/**
 * The template for displaying Comments.
 *
 * The area of the page that contains both current comments
 * and the comment form. The actual display of comments is
 * handled by a callback to allium_comment() which is
 * located in the inc/template-tags.php file.
 *
 * @package Zaatar
 */

/*
 * If the current post is protected by a password and
 * the visitor has not yet entered the password we will
 * return early without loading the comments.
 */
if ( post_password_required() ) {
	return;
}
?>

<div id="comments" class="comments-area">

	<?php // You can start editing here -- including this comment! ?>

	<?php if ( have_comments() ) : ?>
	<div class="comments-area-wrapper">

		<h2 class="comments-title">
			<?php
				$allium_comments_number = get_comments_number();
                if ( '1' === $allium_comments_number ) {
					printf(
						esc_html(
							/* translators: %s: post title */
							_x(
						        'One Reply to &ldquo;%s&rdquo;',
                                'comments title',
                                'zaatar'
                            )
                        ),
						esc_html( get_the_title() )
					);
				} else {
					printf(
						esc_html(
							/* translators: 1: number of comments, 2: comments title */
							_nx(
                                '%1$s Reply to &ldquo;%2$s&rdquo;',
                                '%1$s Replies to &ldquo;%2$s&rdquo;',
                                $allium_comments_number,
                                'comments title',
                                'zaatar'
						    )
                        ),
						esc_html( number_format_i18n( $allium_comments_number ) ),
						esc_html( get_the_title() )
					);
				}
			?>
		</h2>

		<?php if ( get_comment_pages_count() > 1 && get_option( 'page_comments' ) ) : ?>
		<nav id="comment-nav-above" class="navigation comment-navigation comment-navigation-above" role="navigation">
			<h1 class="screen-reader-text"><?php esc_html_e( 'Comment navigation', 'zaatar' ); ?></h1>
			<div class="nav-links">
				<div class="nav-previous"><?php previous_comments_link( esc_html__( 'Older Comments', 'zaatar' ) ); ?></div>
				<div class="nav-next"><?php next_comments_link( esc_html__( 'Newer Comments', 'zaatar' ) ); ?></div>
			</div><!-- .nav-links -->
		</nav><!-- #comment-nav-above -->
		<?php endif; // check for comment navigation ?>

		<ol class="comment-list">
			<?php
				wp_list_comments( array(
					'style'       => 'ol',
					'short_ping'  => true,
					'avatar_size' => 68,
				) );
			?>
		</ol><!-- .comment-list -->

		<?php if ( get_comment_pages_count() > 1 && get_option( 'page_comments' ) ) : // are there comments to navigate through ?>
		<nav id="comment-nav-below" class="navigation comment-navigation comment-navigation-below" role="navigation">
			<h1 class="screen-reader-text"><?php esc_html_e( 'Comment navigation', 'zaatar' ); ?></h1>
			<div class="nav-links">
				<div class="nav-previous"><?php previous_comments_link( esc_html__( 'Older Comments', 'zaatar' ) ); ?></div>
				<div class="nav-next"><?php next_comments_link( esc_html__( 'Newer Comments', 'zaatar' ) ); ?></div>
			</div><!-- .nav-links -->
		</nav><!-- #comment-nav-above -->
		<?php endif; // check for comment navigation ?>

	</div><!-- .comments-area-wrapper -->
	<?php endif; // have_comments() ?>

	<?php
	// If comments are closed and there are comments, let's leave a little note, shall we?
	if ( ! comments_open() && '0' != get_comments_number() && post_type_supports( get_post_type(), 'comments' ) ) :
	?>
	<div class="no-comments-wrapper">
		<p class="no-comments"><?php esc_html_e( 'Comments are closed.', 'zaatar' ); ?></p>
	</div><!-- .comments-area-wrapper -->
	<?php endif; ?>

	<?php comment_form(); ?>

</div><!-- #comments -->
