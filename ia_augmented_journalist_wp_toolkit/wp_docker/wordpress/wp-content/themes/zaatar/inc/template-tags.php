<?php
/**
 * Custom template tags for this theme.
 *
 * Eventually, some of the functionality here could be replaced by core features.
 *
 * @package Zaatar
 */

if ( ! function_exists( 'allium_the_posts_pagination' ) ) :
/**
 * Display navigation to next/previous set of posts when applicable.
 *
 * @return void
 */
function allium_the_posts_pagination() {

	// Previous/next posts navigation @since 4.1.0
	the_posts_pagination( array(
		'prev_text'          => '<span class="screen-reader-text">' . esc_html__( 'Previous Page', 'zaatar' ) . '</span>',
		'next_text'          => '<span class="screen-reader-text">' . esc_html__( 'Next Page', 'zaatar' ) . '</span>',
		'before_page_number' => '<span class="meta-nav screen-reader-text">' . esc_html__( 'Page', 'zaatar' ) . ' </span>',
	) );

}
endif;

if ( ! function_exists( 'allium_the_post_pagination' ) ) :
/**
 * Previous/next post navigation.
 *
 * @return void
 */
function allium_the_post_pagination() {

	// Previous/next post navigation @since 4.1.0.
	
	the_post_navigation( array(
		'next_text' => '<span class="meta-nav">' . esc_html__( 'Next', 'zaatar' ) . '</span> ' . '<span class="post-title">%title</span>',
		'prev_text' => '<span class="meta-nav">' . esc_html__( 'Prev', 'zaatar' ) . '</span> ' . '<span class="post-title">%title</span>',
	) );
	
}
endif;

if ( ! function_exists( 'allium_posted_on' ) ) :
/**
 * Prints HTML with meta information for the current post-date/time and author.
 */
function allium_posted_on( $before = '', $after = '' ) {

	// No need to display date for sticky posts
	if ( allium_has_sticky_post() ) {
		return;
	}

	// Time String
	$time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';
	if ( get_the_time( 'U' ) !== get_the_modified_time( 'U' ) ) {
		$time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
	}

	$time_string = sprintf( $time_string,
		esc_attr( get_the_date( 'c' ) ),
		esc_html( get_the_date() ),
		esc_attr( get_the_modified_date( 'c' ) ),
		esc_html( get_the_modified_date() )
	);

	// Posted On
	$posted_on = sprintf( '<span class="screen-reader-text">%1$s</span><a href="%2$s" rel="bookmark">%3$s</a>',
		esc_html_x( 'Posted on', 'post date', 'zaatar' ),
		esc_url( get_permalink() ),
		$time_string
	);

	// Posted On HTML
	$html = '<span class="posted-on entry-meta-icon">' . $posted_on . '</span>'; // // WPCS: XSS OK.

	// Posted On HTML Before After
	$html = $before . $html . $after; // WPCS: XSS OK.

	/**
	 * Filters the Posted On HTML.
	 *
	 * @param string $html Posted On HTML.
	 */
	$html = apply_filters( 'allium_posted_on_html', $html );

	echo $html; // WPCS: XSS OK.
}
endif;

if ( ! function_exists( 'allium_posted_by' ) ) :
/**
 * Prints author.
 */
function allium_posted_by( $before = '', $after = '' ) {

	// Global Post
	global $post;

	// We need to get author meta data from both inside/outside the loop.
	$post_author_id = get_post_field( 'post_author', $post->ID );

	// Post Author
	$post_author = sprintf( '<span class="author vcard"><a class="entry-author-link url fn n" href="%1$s" rel="author"><span class="entry-author-name">%2$s</span></a></span>',
		esc_url( get_author_posts_url( get_the_author_meta( 'ID', $post_author_id ) ) ),
		esc_html( get_the_author_meta( 'display_name', $post_author_id ) )
	);

	// Byline
	$byline = sprintf(
		/* translators: %s: post author */
		esc_html_x( 'by %s', 'post author', 'zaatar' ),
		$post_author
	);

	// Posted By HTML
	$html = '<span class="byline entry-meta-icon">' . $byline . '</span>'; // WPCS: XSS OK.

	// Posted By HTML Before After
	$html = $before . $html . $after; // WPCS: XSS OK.

	/**
	 * Filters the Posted By HTML.
	 *
	 * @param string $html Posted By HTML.
	 */
	$html = apply_filters( 'allium_posted_by_html', $html );

	echo $html; // WPCS: XSS OK.
}
endif;

if ( ! function_exists( 'allium_sticky_post' ) ) :
/**
 * Prints HTML label for the sticky post.
 */
function allium_sticky_post( $before = '', $after = '' ) {

	// Sticky Post Validation
	if ( ! allium_has_sticky_post() ) {
		return;
	}

	// Sticky Post HTML
	$html = sprintf( '<span class="post-label post-label-sticky entry-meta-icon">%1$s</span>',
		esc_html_x( 'Featured', 'sticky post label', 'zaatar' )
	);

	// Sticky Post HTML Before After
	$html = $before . $html . $after; // WPCS: XSS OK.

	/**
	 * Filters the Sticky Post HTML.
	 *
	 * @param string $html Sticky Post HTML.
	 */
	$html = apply_filters( 'allium_sticky_post_html', $html );

	echo $html; // WPCS: XSS OK.
}
endif;

if ( ! function_exists( 'allium_post_edit_link' ) ) :
/**
 * Prints post edit link.
 *
 * @return void
*/
function allium_post_edit_link( $before = '', $after = '' ) {

	// Post edit link Validation
	if ( allium_has_post_edit_link() ) {

		// Post Edit Link
		$post_edit_link = sprintf( '<span class="screen-reader-text">%1$s</span><a class="post-edit-link" href="%2$s">%3$s</a>',
		esc_html( the_title_attribute( 'echo=0' ) ),
		esc_url( get_edit_post_link() ),
		esc_html_x( 'Edit', 'post edit link label', 'zaatar' )
		);

		// Post Edit Link HTML
		$html = '<span class="post-edit-link-meta entry-meta-icon">' . $post_edit_link . '</span>';

		// Post Edit Link HTML Before After
		$html = $before . $html . $after; // WPCS: XSS OK.

		/**
		 * Filters the Post Edit Link HTML.
		 *
		 * @param string $html Post Edit Link HTML.
		 */
		$html = apply_filters( 'allium_post_edit_link_html', $html );

		echo $html; // WPCS: XSS OK.
	}

}
endif;

if ( ! function_exists( 'allium_post_first_category' ) ) :
/**
 * Prints first category for the current post.
 *
 * @return void
*/
function allium_post_first_category( $before = '', $after = '' ) {

	// An array of categories to return for the post.
	$categories = get_the_category();
	if ( $categories[0] ) {

		// Post First Category HTML
		$html = sprintf( '<span class="post-first-category cat-links entry-meta-icon"><a href="%1$s" title="%2$s">%3$s</a></span>',
			esc_attr( esc_url( get_category_link( $categories[0]->term_id ) ) ),
			esc_attr( $categories[0]->cat_name ),
			esc_html( $categories[0]->cat_name )
		);

		// Post First Category HTML Before After
		$html = $before . $html . $after; // WPCS: XSS OK.

		/**
		 * Filters the Post First Category HTML.
		 *
		 * @param string $html Post First Category HTML.
		 * @param array $categories An array of categories to return for the post.
		 */
		$html = apply_filters( 'allium_post_first_category_html', $html, $categories );

		echo $html; // WPCS: XSS OK.
	}

}
endif;

if ( ! function_exists( 'allium_read_more_link' ) ) :
	/**
	 * Prints Read More Link.
	 */
	function allium_read_more_link() {

		// Read More Label
		$read_more_label = allium_mod( 'allium_read_more_label' );

		// Read More Link
		$read_more_link = sprintf( '<a href="%1$s" class="more-link">%2$s</a>',
			esc_url( get_permalink() ),
			esc_html( $read_more_label )
		);

		// Read More HTML
		$html = '<div class="more-link-wrapper">' . $read_more_link . '</div>'; // // WPCS: XSS OK.

		/**
		 * Filters the Read More HTML.
		 *
		 * @param string $html Read More HTML.
		 */
		$html = apply_filters( 'allium_read_more_html', $html );

		echo $html; // WPCS: XSS OK.
	}
endif;

if ( ! function_exists( 'allium_entry_footer' ) ) :
/**
 * Prints HTML with meta information for the categories, tags and comments.
 */
function allium_entry_footer() {

	// Hide category and tag text for pages.
	if ( 'post' === get_post_type() ) {
		/* translators: used between list items, there is a space after the comma */
		$categories_list = get_the_category_list( _x(', ', 'Used between category, there is a space after the comma.', 'zaatar' ) );
		if ( $categories_list && allium_categorized_blog() ) {
			printf(
				/* translators: 1: posted in label. 2: list of categories. */
				'<span class="cat-links cat-links-single">%1$s %2$s</span>',
				esc_html__( 'Posted in:', 'zaatar' ),
				$categories_list
			); // WPCS: XSS OK.
		}

		/* translators: used between list items, there is a space after the comma */
		$tags_list = get_the_tag_list( '', _x(', ', 'Used between tag, there is a space after the comma.', 'zaatar' ) );
		if ( $tags_list ) {
			printf(
				/* translators: 1: posted in label. 2: list of tags. */
				'<span class="tags-links tags-links-single">%1$s %2$s</span>',
				esc_html__( 'Tags:', 'zaatar' ),
				$tags_list
			); // WPCS: XSS OK.
		}
	}

	// Edit post link.
	edit_post_link(
		sprintf(
			wp_kses(
				/* translators: %s: Name of current post. Only visible to screen readers. */
				__( 'Edit <span class="screen-reader-text">%s</span>', 'zaatar' ),
				array(
					'span' => array(
						'class' => array(),
					),
				)
			),
			get_the_title()
		),
		'<span class="edit-link">',
		'</span>'
	);

}
endif;

/**
 * Returns true if a blog has more than 1 category.
 *
 * @return bool
 */
function allium_categorized_blog() {
	if ( false === ( $all_the_cool_cats = get_transient( 'allium_categories' ) ) ) {
		// Create an array of all the categories that are attached to posts.
		$all_the_cool_cats = get_categories( array (
			'fields'     => 'ids',
			'hide_empty' => 1,

			// We only need to know if there is more than one category.
			'number'     => 2,
		) );

		// Count the number of categories that are attached to the posts.
		$all_the_cool_cats = count( $all_the_cool_cats );

		set_transient( 'allium_categories', $all_the_cool_cats );
	}

	if ( $all_the_cool_cats > 1 ) {
		// This blog has more than 1 category so allium_categorized_blog should return true.
		return true;
	} else {
		// This blog has only 1 category so allium_categorized_blog should return false.
		return false;
	}
}

/**
 * Flush out the transients used in allium_categorized_blog.
 */
function allium_category_transient_flusher() {
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	// Like, beat it. Dig?
	delete_transient( 'allium_categories' );
}
add_action( 'edit_category', 'allium_category_transient_flusher' );
add_action( 'save_post',     'allium_category_transient_flusher' );

if ( ! function_exists( 'allium_post_thumbnail' ) ) :
/**
 * Display an optional post thumbnail.
 *
 * Wraps the post thumbnail in an anchor element on index views.
 *
 * @param array $args
 * @return void
*/
function allium_post_thumbnail( $args = array() ) {

	// Defaults
	$defaults = array (
 		'size'  => 'allium-featured',
 		'class' => 'entry-image-wrapper',
	);

	// Parse incoming $args into an array and merge it with $defaults
	$args = wp_parse_args( $args, $defaults );

	// Post Thumbnail HTML
	$html = '';

	// Post Thumbnail Validation
	if ( allium_has_post_thumbnail() ) {

		// Post Thumbnail HTML
		$html = sprintf( '<div class="%1$s"><figure class="post-thumbnail"><a href="%2$s">%3$s</a></figure></div>',
			esc_attr( $args['class'] ),
			esc_url( get_the_permalink() ),
			get_the_post_thumbnail( null, $args['size'], array( 'class' => 'img-featured img-responsive' ) )
		);

	}

	/**
	 * Filters the Post Thumbnail HTML.
	 *
	 * @param string $html Post Thumbnail HTML.
	 */
	$html = apply_filters( 'allium_post_thumbnail_html', $html );

	// Print HTML
	if ( ! empty ( $html ) ) {
		echo $html; // WPCS: XSS OK.
	}

}
endif;

if ( ! function_exists( 'allium_post_thumbnail_single' ) ) :
	/**
	 * Display an optional post thumbnail at single.
	 *
	 * Wraps the post thumbnail in a `p` tag
	 *
	 * @param array $args
	 * @return void
	*/
	function allium_post_thumbnail_single( $args = array() ) {

		// Post Thumbnail Display Check
		if ( false === allium_mod( 'allium_post_thumbnail_single' ) ) {
			return;
		}

		// Defaults
		$defaults = array (
			 'size'  => 'allium-featured-single',
			 'class' => 'post-thumbnail-single',
		);

		// Parse incoming $args into an array and merge it with $defaults
		$args = wp_parse_args( $args, $defaults );

		// Post Thumbnail HTML
		$html = '';

		// Post Thumbnail Validation
		if ( allium_has_post_thumbnail() ) {

			// Post Thumbnail HTML
			$html = sprintf( '<figure class="%1$s">%2$s</figure>',
				esc_attr( $args['class'] ),
				get_the_post_thumbnail( null, $args['size'], array( 'class' => 'img-featured-single img-responsive' ) )
			);

		}

		/**
		 * Filters the Post Thumbnail HTML.
		 *
		 * @param string $html Post Thumbnail HTML.
		 */
		$html = apply_filters( 'allium_post_thumbnail_single_html', $html );

		// Print HTML
		if ( ! empty ( $html ) ) {
			echo $html; // WPCS: XSS OK.
		}

	}
	endif;

/**
 * A helper conditional function.
 * Whether there is a post thumbnail and post is not password protected.
 *
 * @return bool
 */
function allium_has_post_thumbnail() {

	/**
	 * Post Thumbnail Filter
	 * @return bool
	 */
	return apply_filters( 'allium_has_post_thumbnail', (bool) ( ! post_password_required() && has_post_thumbnail() ) );

}

/**
 * A helper conditional function.
 * Post is Sticky or Not
 *
 * @return bool
 */
function allium_has_sticky_post() {

	/**
	 * Sticky Post Filter
	 * @return bool
	 */
	return apply_filters( 'allium_has_sticky_post', (bool) ( is_sticky() && is_home() && ! is_paged() ) );

}

/**
 * A helper conditional function.
 * Post has Edit link or Not
 *
 * @return bool
 */
function allium_has_post_edit_link() {

	/**
	 * Post Edit Link Filter
	 * @return bool
	 */
	$post_edit_link = get_edit_post_link();
	return apply_filters( 'allium_has_post_edit_link', (bool) ( ! empty( $post_edit_link ) ) );

}

/**
 * A helper conditional function.
 * Theme has Excerpt or Not
 *
 * @return bool
 */
function allium_has_excerpt() {

	// Post Excerpt
	$post_excerpt = get_the_excerpt();

	/**
	 * Excerpt Filter
	 * @return bool
	 */
	return apply_filters( 'allium_has_excerpt', (bool) ! empty ( $post_excerpt ) );

}

/**
 * A helper conditional function.
 * Theme has Sidebar or Not
 *
 * @return bool
 */
function allium_has_sidebar() {

	/**
	 * Sidebar Filter
	 * @return bool
	 */
	return apply_filters( 'allium_has_sidebar', (bool) is_active_sidebar( 'sidebar-1' ) );

}

/**
 * Display the layout classes.
 *
 * @param string $section - Name of the section to retrieve the classes
 * @return void
 */
function allium_layout_class( $section = 'content' ) {

	// Sidebar Position
	$sidebar_position = allium_mod( 'allium_sidebar_position' );
	if ( ! allium_has_sidebar() ) {
		$sidebar_position = 'no';
	}

	// Layout Skeleton
	$layout_skeleton = array(
		'content' => array(
			'content' => 'col',
		),

		'content-sidebar' => array(
			'content' => 'col-16 col-sm-16 col-md-16 col-lg-11 col-xl-11 col-xxl-11',
			'sidebar' => 'col-16 col-sm-16 col-md-16 col-lg-5 col-xl-5 col-xxl-5',
		),

		'sidebar-content' => array(
			'content' => 'col-16 col-sm-16 col-md-16 col-lg-11 col-xl-11 col-xxl-11 order-lg-2 order-xl-2 order-xxl-2',
			'sidebar' => 'col-16 col-sm-16 col-md-16 col-lg-5 col-xl-5 col-xxl-5 order-lg-1 order-xl-1 order-xxl-1',
		),
	);

	// Layout Classes
	switch( $sidebar_position ) {

		case 'no':
		$layout_classes = $layout_skeleton['content']['content'];
		break;

		case 'left':
		$layout_classes = ( 'sidebar' === $section )? $layout_skeleton['sidebar-content']['sidebar'] : $layout_skeleton['sidebar-content']['content'];
		break;

		case 'right':
		default:
		$layout_classes = ( 'sidebar' === $section )? $layout_skeleton['content-sidebar']['sidebar'] : $layout_skeleton['content-sidebar']['content'];

	}

	echo esc_attr( $layout_classes );

}

/**
 * Insert functions from Totomo
 * @package Totomo
 */

/**
 * Custom template tags for the theme.
 * @package Totomo
 */

/**
 * Prints HTML with meta information for the current post-date/time and author.
 */
function totomo_posted_on() {
	?>
	<ul class="post-meta clearfix">
		<li>
			<time class="date fa fa-clock-o" datetime="<?php the_time( 'c' ); ?>" pubdate><?php the_time( get_option( 'date_format' ) ); ?></time>
		</li>
		<li>
			<?php comments_popup_link( __( 'No Comments', 'totomo' ), __( '1 Comment', 'totomo' ), __( '% Comments', 'totomo' ), 'comments-link fa fa-comments' ); ?>
		</li>
		<li class="fa fa-tags">
			<?php the_category( ', ' ); ?>
		</li>
	</ul>
	<?php
}

/**
 * Display gallery slider.
 *
 * @param string $imagetotomoize Image size
 */
function totomo_gallerytotomolider( $imagetotomoize ) {
	$gallery = get_post_gallery( get_the_ID(), false );
	$images  = wp_parse_id_list( $gallery['ids'] );

	if ( empty( $images ) ) {
		return;
	}
	?>
	<div id="slider-<?php the_ID(); ?>" class="carousel slide" data-ride="carousel">
		<ol class="carousel-indicators">
			<?php
			foreach ( $images as $i => $image ) {
				printf( '<li data-target="#slider-%s" data-slide-to="%s"%s></li>', get_the_ID(), $i, 0 == $i ? ' class="active"' : '' );
			}
			?>
		</ol>
		<div class="carousel-inner">
			<?php
			foreach ( $images as $i => $image ) {
				printf( '<div class="item%s">%s</div>', 0 == $i ? ' active' : '', wp_get_attachment_image( $image, $imagetotomoize ) );
			}
			?>
		</div>
	</div>
	<?php
}

/**
 * Callback function to show comment
 *
 * @param object $comment
 * @param array $args
 * @param int $depth
 *
 * @return void
 * @since 1.0
 */
function totomo_comment( $comment, $args, $depth ) {
	$GLOBALS['comment'] = $comment;
	$post               = get_post();

	$comment_type = get_comment_type( $comment->comment_ID );
	$templates    = array( "template-parts/comment-$comment_type.php" );
	// If the comment type is a 'pingback' or 'trackback', allow the use of 'comment-ping.php'.
	if ( 'pingback' == $comment_type || 'trackback' == $comment_type ) {
		$templates[] = 'template-parts/comment-ping.php';
	}
	// Add the fallback 'comment.php' template.
	$templates[] = 'template-parts/comment.php';

	require( locate_template( $templates ) );
}

/**
 * Show entry format images, video, gallery, audio, etc.
 *
 * @return void
 */
function totomo_post_formats() {
	$html  = '';
	$size  = 'totomo-thumb-blog-list';
	$thumb = get_the_post_thumbnail( get_the_ID(), $size );

	switch ( get_post_format() ) {
		case 'link':
			$link = get_the_content();
			if ( $link ) {
				$html = "<div class='link-wrapper'>$link</div>";
			}
			break;
		case 'quote':
			$html = get_the_content();

			if ( empty( $thumb ) ) {
				break;
			}

			$html .= '<a class="post-image" href="' . get_permalink() . '">';
			$html .= $thumb;
			$html .= '</a>';
			break;
		case 'gallery':

			// Show gallery
			totomo_gallerytotomolider( 'thumb-blog-list' );
			break;
		case 'audio':
			$content     = apply_filters( 'the_content', get_the_content( __( 'Read More', 'totomo' ) ) );
			$media       = get_media_embedded_in_content( $content, array( 'audio', 'object', 'embed', 'iframe' ) );
			$thumb_audio = '';
			if ( ! empty( $thumb ) ) {
				$html .= '<a class="post-image" href="' . get_permalink() . '">';
				$html .= $thumb;
				$html .= '</a>';
				$thumb_audio = 'thumb_audio';
			}

			if ( ! empty( $media ) ) : ?>
				<?php
				foreach ( $media as $embed_html ) {
					$html .= sprintf( '<div class="audio-wrapper %s">%s</div>', $thumb_audio, $embed_html );
				}
				?>
			<?php endif;

			break;
		case 'video':
			$content = apply_filters( 'the_content', get_the_content( __( 'Read More', 'totomo' ) ) );
			$media   = get_media_embedded_in_content( $content, array( 'video', 'object', 'embed', 'iframe' ) );
			if ( ! empty( $media ) ) : ?>
				<?php
				foreach ( $media as $embed_html ) {
					$html = sprintf( '%s', $embed_html );
				}
				?>
			<?php endif;
			break;
		default:
			if ( empty( $thumb ) ) {
				return;
			}

			$html .= '<a class="post-image" href="' . get_permalink() . '">';
			$html .= $thumb;
			$html .= '</a>';
	}

	if ( $html ) {
		echo "<div class='post-format-meta'>$html</div>";
	}

	$post_format = get_post_format( get_the_ID() );
	if ( 'link' == $post_format || 'quote' == $post_format ) {
		return;
	}
}

/**
 * Display related posts.
 */
function totomo_related_posts() {
	$args    = '';
	$args    = wp_parse_args( $args, array(
		'category__in'   => wp_get_post_categories( get_the_ID() ),
		'posts_per_page' => 4,
		'post__not_in'   => array( get_the_ID() ),
	) );
	$related = new WP_Query( $args );

	if ( ! $related->have_posts() ) {
		return;
	}
	?>
	<div class="related-article">
		<h2 class="box-title"><?php _e( 'Last Posts', 'totomo' ); ?></h2>
		<ul class="row">
			<?php
			while ( $related->have_posts() ) {
				$related->the_post();

				$post_thumbnail = get_the_post_thumbnail( get_the_ID(), 'thumbnail' );

				$class_format = '';
				if ( ! $post_thumbnail ) {
					$class_format = 'fa-format-' . get_post_format( get_the_ID() );
				}

				printf(
					'<li class="col-md-6">
						<a href="%s" class="post-thumbnail %s">%s</a>
						<div class="related-post-content">
							<a class="related-post-title" href="%s">
							<span class="date">%s</span></br>
							%s</a>
						</div>
					</li>',
					esc_url( get_permalink() ),
					$class_format,
					$post_thumbnail,
					esc_url( get_permalink() ),
					get_the_date(),
					get_the_title()
				);
				?>
				<?php
			}
			?>
		</ul>
	</div>
	<?php
	wp_reset_postdata();
}

/**
 * Display post author box
 *
 * @since  1.0
 * @return void
 */
function totomo_get_author_box() {
	?>
	<div id="post-author" class="post-author-area">
		<?php echo get_avatar( get_the_author_meta( 'ID' ), 96 ); ?>
		<div class="info">
			<h4 class="display-name"><?php the_author(); ?></h4>
			<p class="author-desc"><?php the_author_meta( 'description' ); ?></p>
		</div>
	</div>
	<?php
}

add_filter( 'excerpt_more', 'totomo_excerpt_more' );

/**
 * Replaces "[...]" (appended to automatically generated excerpts) with ... and a 'Continue reading' link.
 *
 * @return string 'Continue reading' link prepended with an ellipsis.
 */
function totomo_excerpt_more() {
	$text = wp_kses_post( sprintf( __( 'Continue reading &rarr; %s', 'totomo' ), '<span class="screen-reader-text">' . get_the_title() . '</span>' ) );
	$more = sprintf( '&hellip; <p class="text-center"><a href="%s" class="more-link">%s</a></p>', esc_url( get_permalink() ), $text );

	return $more;
}

add_filter( 'the_content_more_link', 'totomo_content_more' );

/**
 * Auto add more links.
 *
 * @return string 'Continue reading' link prepended with an ellipsis.
 */
function totomo_content_more() {
	$text = wp_kses_post( sprintf( __( 'Continue reading &rarr; %s', 'totomo' ), '<span class="screen-reader-text">' . get_the_title() . '</span>' ) );
	$more = sprintf( '<p class="text-center"><a href="%s#more-%d" class="more-link">%s</a></p>', esc_url( get_permalink() ), get_the_ID(), $text );

	return $more;
}

add_filter( 'excerpt_length', 'totomo_excerpt_length' );

/**
 * Change excerpt length.
 *
 * @return int
 */
function totomo_excerpt_length() {
	return 25;
}

/**
 * Prints HTML with meta information for the categories, tags and comments.
 */
function totomo_entry_footer() {
	// Hide tag text for pages.
	if ( 'post' === get_post_type() ) {
		/* translators: used between list items, there is a space after the comma */
		$tags_list = get_the_tag_list( '#', esc_html__( ' #', 'totomo' ) );
		if ( $tags_list ) {
			printf( '<div class="tags-links">%s</div>', $tags_list ); // WPCS: XSS OK.
		}
	}

	edit_post_link(
		sprintf(
			/* translators: %s: Name of current post */
			esc_html__( 'Edit %s', 'totomo' ),
			the_title( '<span class="screen-reader-text">"', '"</span>', false )
		),
		'<span class="edit-link">',
		'</span>'
	);
}
