<?php
/**
 * Swift Page Builder Here includes useful files for plugin
 *
 * @package SwiftPageBuilder
 *
 */

$lib_dir = $composer_settings['COMPOSER_LIB'];
$shortcodes_dir = $composer_settings['SHORTCODES_LIB'];

require_once( $lib_dir . 'abstract.php' );
require_once( $lib_dir . 'helpers.php' );
require_once( $lib_dir . 'mapper.php' );
require_once( $lib_dir . 'shortcodes.php' );
require_once( $lib_dir . 'composer.php' );

/* Add shortcodes classes */
require_once( $shortcodes_dir . 'default.php' );
require_once( $shortcodes_dir . 'column.php' );
require_once( $shortcodes_dir . 'accordion.php' );
require_once( $shortcodes_dir . 'tabs.php' );
require_once( $shortcodes_dir . 'tour.php' );
require_once( $shortcodes_dir . 'buttons.php' );
require_once( $shortcodes_dir . 'images_galleries.php' );
require_once( $shortcodes_dir . 'media.php' );
require_once( $shortcodes_dir . 'raw_content.php' );
require_once( $shortcodes_dir . 'teaser_grid.php' );

require_once( $shortcodes_dir . 'portfolio.php' );
require_once( $shortcodes_dir . 'blog.php' );
require_once( $shortcodes_dir . 'clients.php' );
require_once( $shortcodes_dir . 'team.php' );
require_once( $shortcodes_dir . 'jobs.php' );
require_once( $shortcodes_dir . 'testimonial.php' );
require_once( $shortcodes_dir . 'testimonial-carousel.php' );
require_once( $shortcodes_dir . 'faqs.php' );
require_once( $shortcodes_dir . 'showcase.php' );
require_once( $shortcodes_dir . 'recent-posts.php' );
require_once( $shortcodes_dir . 'portfolio-carousel.php' );
require_once( $shortcodes_dir . 'posts-carousel.php' );
//require_once( $shortcodes_dir . 'posts-ticker.php' );
require_once( $shortcodes_dir . 'team-carousel.php' );
require_once( $shortcodes_dir . 'jobs-overview.php' );
require_once( $shortcodes_dir . 'latest-tweet-bar.php' );
require_once( $shortcodes_dir . 'code-snippet.php' );
require_once( $shortcodes_dir . 'googlechart.php' );
require_once( $shortcodes_dir . 'sitemap.php' );
require_once( $shortcodes_dir . 'search.php' );

require_once( $lib_dir . 'media_tab.php' );

require_once( $lib_dir . 'layouts.php' );