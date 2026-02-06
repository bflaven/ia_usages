<?php
/**
 * Functions which enhance the theme by hooking into WordPress
 *
 * @package Zaatar
 */

if ( ! function_exists( 'allium_fonts_url' ) ) :
/**
 * Register fonts for theme.
 *
 * @return string Fonts URL for the theme.
 */
function allium_fonts_url() {

    // Fonts and Other Variables
    $fonts_url = '';
	$fonts     = array();
	$subsets   = 'latin,latin-ext';

	/* Translators: If there are characters in your language that are not
    * supported by Nunito Sans, translate this to 'off'. Do not translate
    * into your own language.
    */
    if ( 'off' !== esc_html_x( 'on', 'Nunito Sans font: on or off', 'zaatar' ) ) {
		$fonts[] = 'Nunito Sans:400,400i,700,700i';
	}

    /* Translators: If there are characters in your language that are not
    * supported by Roboto, translate this to 'off'. Do not translate
    * into your own language.
    */
    if ( 'off' !== esc_html_x( 'on', 'Roboto font: on or off', 'zaatar' ) ) {
		$fonts[] = 'Roboto:400,400i,700,700i';
	}

	/* Translators: To add an additional character subset specific to your language,
	* translate this to 'greek', 'cyrillic', 'devanagari' or 'vietnamese'.
	* Do not translate into your own language.
	*/
	$subset = esc_html_x( 'no-subset', 'Add new subset (cyrillic, greek, devanagari, vietnamese)', 'zaatar' );

	if ( 'cyrillic' === $subset ) {
		$subsets .= ',cyrillic,cyrillic-ext';
	} elseif ( 'greek' === $subset ) {
		$subsets .= ',greek,greek-ext';
	} elseif ( 'devanagari' === $subset ) {
		$subsets .= ',devanagari';
	} elseif ( 'vietnamese' === $subset ) {
		$subsets .= ',vietnamese';
	}

	if ( $fonts ) {
		$fonts_url = add_query_arg( array(
			'family' => urlencode( implode( '|', $fonts ) ),
			'subset' => urlencode( $subsets ),
		), 'https://fonts.googleapis.com/css' );
	}

	/**
	 * Filters the Google Fonts URL.
	 *
	 * @param string $fonts_url Google Fonts URL.
	 */
	return apply_filters( 'allium_fonts_url', $fonts_url );

}
endif;

/**
 * Get our wp_nav_menu() fallback, wp_page_menu(), to show a home link.
 *
 * @param array $args Configuration arguments.
 * @return array
 */
function allium_page_menu_args( $args ) {
	$args['show_home'] = true;
	$args['menu_class'] = 'site-header-menu';
	return $args;
}
add_filter( 'wp_page_menu_args', 'allium_page_menu_args' );

/**
 * Add ID and CLASS attributes to the first <ul> occurence in wp_page_menu
 */
function allium_page_menu_class( $class ) {
  return preg_replace( '/<ul>/', '<ul class="header-menu sf-menu">', $class, 1 );
}
add_filter( 'wp_page_menu', 'allium_page_menu_class' );

/**
 * Filter 'excerpt_length'
 *
 * @param int $length
 * @return int
 */
function allium_excerpt_length( $length ) {
  if ( is_admin() ) {
		return $length;
	}

	// Custom Excerpt Length
	$length = allium_mod( 'allium_excerpt_length' );

	/**
	 * Filters the Excerpt length.
	 *
	 * @param int $length Excerpt Length.
	 */
	return apply_filters( 'allium_excerpt_length', $length );
}
add_filter( 'excerpt_length', 'allium_excerpt_length' );

/**
 * Filter 'excerpt_more'
 *
 * Remove [...] string
 * @param str $more
 * @return str
 */
function allium_excerpt_more( $more ) {
	if ( is_admin() ) {
		return $more;
	}

	// Custom Excerpt More
	$more = '&hellip;';

	// Custom Excerpt Length
	$length = allium_mod( 'allium_excerpt_length' );

	// No need to show more in case of empty or zero Custom Excerpt Length
	if ( empty( $length ) ) {
		$more = '';
	}

  /**
	 * Filters the Excerpt more string.
	 *
	 * @param string $excerpt_more Excerpt More.
	 */
	return apply_filters( 'allium_excerpt_more', $more );
}
add_filter( 'excerpt_more', 'allium_excerpt_more' );

/**
 * Filter 'get_the_archive_title'
 *
 * Possible formats for $title
 * 1. Category: Label
 * 2. Asides
 *
 * @see get_the_archive_title
 * @param string $title
 * @return $title
 */
function allium_the_archive_title( $title ) {
	// Explode on the basis of `:`
	$matches = explode( ':', $title, 2 );

	// Validation
	if ( count( $matches ) > 1 ) {
		$matches[0] = sprintf( '<span class="page-title-label">%1$s:</span>', trim( $matches[0] ) );
		$matches[1] = sprintf( '<span class="page-title-value">%1$s</span>',  trim( $matches[1] ) );
	} else {
		$matches[0] = sprintf( '<span class="page-title-label">%1$s</span>',  trim( $matches[0] ) );
	}

	// Implode
	$title = implode( ' ', $matches );

	return $title;
}
add_filter( 'get_the_archive_title', 'allium_the_archive_title' );

/**
 * Filter `body_class`
 * Adds custom classes to the array of body classes.
 *
 * @param array $classes Classes for the body element.
 * @return array
 */
function allium_body_classes( $classes ) {

	// Adds a class of group-blog to blogs with more than 1 published author.
	if ( is_multi_author() ) {
		$classes[] = 'group-blog';
	}

	if ( is_singular() ) {
		// Adds `singular` to singular pages.
		$classes[] = 'singular';
	} else {
		// Adds `hfeed` to non singular pages.
		$classes[] = 'hfeed';
	}

	// Site Title & Tagline Class
	if ( display_header_text() ) {
		$classes[] = 'has-site-branding';
	}

	// Custom Header
	if ( get_header_image() ) {
		$classes[] = 'has-custom-header';
	}

	// Custom Background Image
	if ( get_background_image() ) {
		$classes[] = 'has-custom-background-image';
	}

	// Theme Layout (wide|box)
	$classes[] = 'has-' . esc_attr( allium_mod( 'allium_theme_layout' ) ) . '-layout';

	// Sidebar Position
	if ( allium_has_sidebar() ) {
		$classes[] = 'has-' . esc_attr( allium_mod( 'allium_sidebar_position' ) ) . '-sidebar';
	} else {
		$classes[] = 'has-no-sidebar';
	}

	return $classes;
}
add_filter( 'body_class', 'allium_body_classes' );

/**
 * Add a pingback url auto-discovery header for single posts, pages, or attachments.
 */
function allium_pingback_header() {
	if ( is_singular() && pings_open() ) {
		printf( '<link rel="pingback" href="%s">', esc_url( get_bloginfo( 'pingback_url' ) ) );
	}
}
add_action( 'wp_head', 'allium_pingback_header' );

/**
 * Blog Credits.
 *
 * @return void
 */
function allium_credits_blog() {
	$html = '<div class="credits credits-blog">'. allium_mod( 'allium_copyright' ) .'</div>';

	/**
	 * Filters the Blog Credits HTML.
	 *
	 * @param string $html Blog Credits HTML.
	 */
	$html = apply_filters( 'allium_credits_blog_html', $html );

	echo convert_chars( convert_smilies( wptexturize( stripslashes( wp_filter_post_kses( addslashes( $html ) ) ) ) ) ); // WPCS: XSS OK.
}
add_action( 'allium_credits', 'allium_credits_blog' );

/**
 * Designer Credits.
 *
 * @return void
 */
function allium_credits_designer() {
	$designer_string = sprintf(
		/* translators: %1$s is Theme / Designer Name ( Zaatar ), %2$s is WordPress */
		esc_html__( '%1$s &sdot; %2$s Powered by %3$s', 'zaatar' ),
		// wp_kses_post( 'Zaatar Theme by <a href="https://templatelens.com">TemplateLens</a>' ),
		wp_kses_post( 'Theme Zaatar.' ),
		wp_kses_post( '<!-- Inspired by Allium, Totomo and Supreme -->'),
		wp_kses_post( '<a href="https://wordpress.org" target="_blank">WordPress</a>' )

	);

	// Designer HTML
	// $html = '<div class="credits credits-designer">'. $designer_string .'</div>';
	$html = '<div class="credits credits-designer">'. $designer_string .'</div>';



	/**
	 * Filters the Designer HTML.
	 *
	 * @param string $html Designer HTML.
	 */
	$html = apply_filters( 'allium_credits_designer_html', $html );

	echo $html; // WPCS: XSS OK.
}
add_action( 'allium_credits', 'allium_credits_designer' );

/**
 * Enqueues front-end CSS to hide elements.
 *
 * @see wp_add_inline_style()
 */
function allium_hide_elements() {
	// Elements
	$elements = array();

	// Credit
	if ( false === allium_mod( 'allium_credit' ) ) {
		$elements[] = '.credits-designer';
	}

	// Bail if their are no elements to process
	if ( 0 === count( $elements ) ) {
		return;
	}

	// Build Elements
	$elements = implode( ',', $elements );

	// Build CSS
	$css = sprintf( '%1$s { clip: rect(1px, 1px, 1px, 1px); position: absolute; }', $elements );

	// Add Inline Style
	wp_add_inline_style( 'allium-style', $css );
}
add_action( 'wp_enqueue_scripts', 'allium_hide_elements', 11 );

/**
 * Filter in a link to a content ID attribute for the next/previous image links on image attachment pages
 */
function allium_attachment_link( $url, $id ) {
	if ( ! is_attachment() && ! wp_attachment_is_image( $id ) ) {
		return $url;
	}

	$image = get_post( $id );
	if ( ! empty( $image->post_parent ) && $image->post_parent != $id ) {
		$url .= '#main';
	}

	return $url;
}
add_filter( 'attachment_link', 'allium_attachment_link', 10, 2 );

if ( ! function_exists( 'allium_the_attached_image' ) ) :
/**
 * Print the attached image with a link to the next attached image.
 *
 * @return void
 */
function allium_the_attached_image() {
	$post                = get_post();
	/**
	 * Filter the default Zaatar attachment size.
	 *
	 * @param array $dimensions {
	 *     An array of height and width dimensions.
	 *
	 *     @type int $height Height of the image in pixels. Default 1140.
	 *     @type int $width  Width of the image in pixels. Default 1140.
	 * }
	 */
	$attachment_size     = apply_filters( 'allium_attachment_size', 'full' );
	$next_attachment_url = wp_get_attachment_url();

	if ( $post->post_parent ) { // Only look for attachments if this attachment has a parent object.

		/*
		 * Grab the IDs of all the image attachments in a gallery so we can get the URL
		 * of the next adjacent image in a gallery, or the first image (if we're
		 * looking at the last image in a gallery), or, in a gallery of one, just the
		 * link to that image file.
		 */
		$attachment_ids = get_posts( array(
			'post_parent'    => $post->post_parent,
			'fields'         => 'ids',
			'numberposts'    => 100,
			'post_status'    => 'inherit',
			'post_type'      => 'attachment',
			'post_mime_type' => 'image',
			'order'          => 'ASC',
			'orderby'        => 'menu_order ID',
		) );

		// If there is more than 1 attachment in a gallery...
		if ( count( $attachment_ids ) > 1 ) {

			foreach ( $attachment_ids as $key => $attachment_id ) {
				if ( $attachment_id === $post->ID ) {
					break;
				}
			}

			// For next attachment
			$key++;

			if ( isset( $attachment_ids[ $key ] ) ) {
				// get the URL of the next image attachment
				$next_attachment_url = get_attachment_link( $attachment_ids[$key] );
			} else {
				// or get the URL of the first image attachment
				$next_attachment_url = get_attachment_link( $attachment_ids[0] );
			}

		}

	} // end post->post_parent check

	printf( '<a href="%1$s" title="%2$s" rel="attachment">%3$s</a>',
		esc_url( $next_attachment_url ),
		esc_attr( get_the_title() ),
		wp_get_attachment_image( $post->ID, $attachment_size )
	);

}
endif;
