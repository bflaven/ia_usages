<?php
/**
 * Zaatar functions and definitions
 *
 * @package Zaatar
 */
/* ==================================================
	
	Swift Framework Main Functions
	
	================================================== */
	
	define('SF_TEMPLATE_PATH', get_template_directory());
	define('SF_INCLUDES_PATH', SF_TEMPLATE_PATH . '/inc');
	define('SF_LOCAL_PATH', get_template_directory_uri());
	
	/* Include page builder */
	// include(SF_INCLUDES_PATH . '/page-builder/swift-page-builder.php');


	/* Add shortcodes */
	include(SF_INCLUDES_PATH . '/shortcodes.php');

	/* THEME SUPPORT
	================================================== */  
	add_theme_support( 'post-formats', array('quote') );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'post-thumbnails' );
	

if ( ! function_exists( 'allium_setup' ) ) :
/**
 * Sets up theme defaults and registers support for various WordPress features.
 *
 * Note that this function is hooked into the after_setup_theme hook, which
 * runs before the init hook. The init hook is too late for some features, such
 * as indicating support for post thumbnails.
 */
function allium_setup() {

	/*
	 * Make theme available for translation.
	 * Translations can be filed in the /languages/ directory.
	 * If you're building a theme based on Zaatar, use a find and replace
	 * to change 'zaatar' to the name of your theme in all the template files
	 */
	load_theme_textdomain( 'zaatar', get_template_directory() . '/languages' );

	// Add default posts and comments RSS feed links to head.
	add_theme_support( 'automatic-feed-links' );

	/*
	 * Let WordPress manage the document title.
	 * By adding theme support, we declare that this theme does not use a
	 * hard-coded <title> tag in the document head, and expect WordPress to
	 * provide it for us.
	 */
	add_theme_support( 'title-tag' );

	/*
	 * Enable support for custom logo.
	 *
	 * @link https://codex.wordpress.org/Theme_Logo
	 */
	add_theme_support( 'custom-logo', array(
		'height'      => 400,
		'width'       => 580,
		'flex-height' => true,
		'flex-width'  => true,
		'header-text' => array( 'site-title', 'site-description' ),
	) );

	/*
	 * Enable support for Post Thumbnails on posts and pages.
	 *
	 * @link http://codex.wordpress.org/Function_Reference/add_theme_support#Post_Thumbnails
	 */
	add_theme_support( 'post-thumbnails' );

	// Theme Image Sizes
	add_image_size( 'allium-featured', 700, 525, true );
	add_image_size( 'allium-featured-single', 769, 0, true );

	// This theme uses wp_nav_menu() in four locations.
	register_nav_menus( array (
		'header-menu' => esc_html__( 'Header Menu', 'zaatar' ),
		'top-menu'    => esc_html__( 'Top Menu', 'zaatar' ),
	) );

	// This theme styles the visual editor to resemble the theme style.
	add_editor_style( array ( 'css/editor-style.css', allium_fonts_url() ) );

	/*
	* Switch default core markup for search form, comment form, and comments
	* to output valid HTML5.
	*/
	add_theme_support( 'html5',
		array(
			'comment-form',
			'comment-list',
			'gallery',
			'caption',
		)
	);

	// Setup the WordPress core custom background feature.
	add_theme_support( 'custom-background', apply_filters( 'allium_custom_background_args', array (
		'default-color' => 'f9f9f9',
		'default-image' => '',
	) ) );

	// Add theme support for selective refresh for widgets.
	add_theme_support( 'customize-selective-refresh-widgets' );

	/*
	 * Add support for full and wide align images.
	 * @see https://wordpress.org/gutenberg/handbook/extensibility/theme-support/#wide-alignment
	 */
	add_theme_support( 'align-wide' );

}
endif; // allium_setup
add_action( 'after_setup_theme', 'allium_setup' );

/**
 * Set the content width in pixels, based on the theme's design and stylesheet.
 *
 * Priority 0 to make it available to lower priority callbacks.
 *
 * @global int $content_width
 */
function allium_content_width() {
	// This variable is intended to be overruled from themes.
	// Open WPCS issue: {@link https://github.com/WordPress-Coding-Standards/WordPress-Coding-Standards/issues/1043}.
	// phpcs:ignore WordPress.NamingConventions.PrefixAllGlobals.NonPrefixedVariableFound
	$GLOBALS['content_width'] = apply_filters( 'allium_content_width', 769 );
}
add_action( 'after_setup_theme', 'allium_content_width', 0 );

/**
 * Register widget area.
 *
 * @link http://codex.wordpress.org/Function_Reference/register_sidebar
 */
function allium_widgets_init() {

	// Widget Areas
	register_sidebar( array(
		'name'          => esc_html__( 'Main Sidebar', 'zaatar' ),
		'id'            => 'sidebar-1',
		'description'   => esc_html__( 'Add widgets here to appear in your sidebar.', 'zaatar' ),
		'before_widget' => '<aside id="%1$s" class="widget %2$s">',
		'after_widget'  => '</aside>',
		'before_title'  => '<h2 class="widget-title">',
		'after_title'   => '</h2>',
	) );

}
add_action( 'widgets_init', 'allium_widgets_init' );

/**
 * Enqueue scripts and styles.
 */
function allium_scripts() {

	/**
	 * Enqueue JS files
	 */

	// Enquire
	wp_enqueue_script( 'enquire', get_template_directory_uri() . '/js/enquire.js', array( 'jquery' ), '2.1.6', true );

	// Fitvids
	wp_enqueue_script( 'fitvids', get_template_directory_uri() . '/js/fitvids.js', array( 'jquery' ), '1.1', true );

	// Superfish Menu
	wp_enqueue_script( 'hover-intent', get_template_directory_uri() . '/js/hover-intent.js', array( 'jquery' ), 'r7', true );
	wp_enqueue_script( 'superfish', get_template_directory_uri() . '/js/superfish.js', array( 'jquery' ), '1.7.10', true );

	// Comment Reply
	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}

	// Keyboard image navigation support
	if ( is_singular() && wp_attachment_is_image() ) {
		wp_enqueue_script( 'allium-keyboard-image-navigation', get_template_directory_uri() . '/js/keyboard-image-navigation.js', array( 'jquery' ), '20140127', true );
	}

	// Custom Script
	wp_enqueue_script( 'allium-custom', get_template_directory_uri() . '/js/custom.js', array( 'jquery' ), '1.0', true );

	/**
	 * Enqueue CSS files
	 */

	// Bootstrap Custom
	wp_enqueue_style( 'allium-bootstrap-custom', get_template_directory_uri() . '/css/bootstrap-custom.css' );

	// Font Awesome 5
	// For Reviewer and Developers: Unique Handle `font-awesome-5` is required to avoid the conflict with Font Awesome 4+ library.
	// Font Awesome 5+ library is completely rewritten and is different from Font Awesome 4+ library.
	wp_enqueue_style( 'font-awesome-5', get_template_directory_uri() . '/css/fontawesome-all.css' );

	// Fonts
	wp_enqueue_style( 'allium-fonts', allium_fonts_url(), array(), null );

	// Theme Stylesheet
	wp_enqueue_style( 'allium-style', get_stylesheet_uri() );

}
add_action( 'wp_enqueue_scripts', 'allium_scripts' );

/**
 * Enhance the theme by hooking into WordPress.
 */
require get_template_directory() . '/inc/template-functions.php';

/**
 * Custom template tags for this theme.
 */
require get_template_directory() . '/inc/template-tags.php';

/**
 * Implement the Custom Header feature.
 */
require get_template_directory() . '/inc/custom-header.php';

/**
 * Customizer additions.
 */
require get_template_directory() . '/inc/customizer/customizer-core.php';
require get_template_directory() . '/inc/customizer/customizer.php';



              	/*
              		* INSERT SPECIFIC CONTENT FOR BRUNO FLAVEN WEBSITE
              		*
              		*
              		* 
              	/*/



				/*****************************************************************************************/
				      /// BEGIN - Settings for the filtering columns for product_for_sale
				/*****************************************************************************************/
				

						// ProductForSale: Add admin columns with correct image rendering
						add_filter('manage_edit-productforsale_columns', 'myeditproductforsalecolumns');
						add_action('manage_productforsale_posts_custom_column', 'mymanageproductforsalecolumns', 10, 2);

						function myeditproductforsalecolumns($columns) {
						    $columns = array(
						        'cb'           => '<input type="checkbox" />',
						        'cover'        => 'Cover',
						        'title'        => 'Title',
						        'productasin'  => 'Asin',
						        'author'       => 'Auteur',
						        'genres'       => 'Genres',
						        'auteurs'      => 'Auteurs',
						        'editions'     => 'Editions',
						        'amazonproductsingle' => 'posts966',
						        'shortcodesingle' => 'Shortcode',
						        'id'           => 'ID',
						        'views'        => 'Vues',
						        'date'         => 'Date',
						        'comments'     => 'Comments',
						        'attachments'  => 'Attachments'
						    );
						    return $columns;
						}

						function mymanageproductforsalecolumns($column, $post_id) {
						    switch ($column) {

						        case 'productasin':
						            $asin = get_post_meta($post_id, 'amazonitemAmazonAsin', true);
						            echo empty($asin) ? 'Unknown' : esc_html($asin);
						            break;

						        case 'genres':
						            $terms = get_the_terms($post_id, 'productforsalegenre');
						            if (!empty($terms)) {
						                $out = array();
						                foreach ($terms as $term) {
						                    $out[] = sprintf(
						                        '<a href="%s">%s</a>',
						                        esc_url(add_query_arg(array('post_type' => 'productforsale', 'productforsalegenre' => $term->slug), 'edit.php')),
						                        esc_html($term->name)
						                    );
						                }
						                echo join(', ', $out);
						            } else {
						                echo 'No Genres';
						            }
						            break;

						        case 'auteurs':
						            $terms = get_the_terms($post_id, 'productforsaleauthor');
						            if (!empty($terms)) {
						                $out = array();
						                foreach ($terms as $term) {
						                    $out[] = sprintf(
						                        '<a href="%s">%s</a>',
						                        esc_url(add_query_arg(array('post_type' => 'productforsale', 'productforsaleauthor' => $term->slug), 'edit.php')),
						                        esc_html($term->name)
						                    );
						                }
						                echo join(', ', $out);
						            } else {
						                echo 'No Authors';
						            }
						            break;

						        case 'editions':
						            $terms = get_the_terms($post_id, 'productforsalekw');
						            if (!empty($terms)) {
						                $out = array();
						                foreach ($terms as $term) {
						                    $out[] = sprintf(
						                        '<a href="%s">%s</a>',
						                        esc_url(add_query_arg(array('post_type' => 'productforsale', 'productforsalekw' => $term->slug), 'edit.php')),
						                        esc_html($term->name)
						                    );
						                }
						                echo join(', ', $out);
						            } else {
						                echo 'No Editions';
						            }
						            break;

						        case 'shortcodesingle':
						            // Display the ID in a hidden input and a textarea for shortcode use
						            $id = $post_id;
						            if (empty($id)) {
						                echo 'Unknown';
						            } else {
						                printf('<input value="amazonproductsingle_posts%s" />', esc_attr($id));
						                printf('<textarea rows="3" cols="15" wrap="hard">amazonproductsingle_posts%s</textarea>', esc_attr($id));
						            }
						            break;

						        case 'cover':
						            $cover_url = get_post_meta($post_id, 'amazonitemAmazonMediumImageURL', true);
						            $cover_title = get_post_meta($post_id, 'amazonitemAmazonTitle', true);
						            $cover_height = get_post_meta($post_id, 'amazonitemAmazonMediumImageHeight', true);
						            $cover_width = get_post_meta($post_id, 'amazonitemAmazonMediumImageWidth', true);

						            if (empty($cover_url)) {
						                echo 'Unknown';
						            } else {
						                printf(
						                    '<img alt="%s" src="%s" width="%d" height="%d" />',
						                    esc_attr($cover_title),
						                    esc_url($cover_url),
						                    intval($cover_width),
						                    intval($cover_height)
						                );
						            }
						            break;

						        // Add more custom columns as needed...

						        default:
						            // For other columns, use default behavior or break
						            break;
						    }
						}

						// Make columns sortable if needed
						add_filter('manage_edit-productforsale_sortable_columns', 'myproductforsalesortablecolumns');
						function myproductforsalesortablecolumns($columns) {
						    $columns['title'] = 'title';
						    $columns['productasin'] = 'productasin';
						    $columns['genres'] = 'genres';
						    $columns['auteurs'] = 'auteurs';
						    $columns['editions'] = 'editions';
						    $columns['views'] = 'views';
						    $columns['date'] = 'date';
						    $columns['id'] = 'id';
						    $columns['shortcodesingle'] = 'shortcodesingle';
						    $columns['cover'] = 'cover';
						    return $columns;
						}

				
				/*****************************************************************************************/
					      ///  END - Settings for the filtering columns for product_for_sale
				/*****************************************************************************************/




					/*****************************************************************************************/
					/*
						// BEGIN WIDGETS
					*/
					/*****************************************************************************************/

						/* NOTE: USING POST_TYPE */

								/* // amazon widget */
								function widget_amazon_init() {

									if ( !function_exists('register_sidebar_widget') )
										return;
										/* TO CONTROL TH WIDGET IN BACKEND */
										function widget_amazon_single_product_control () {

												// Get options
												$options = get_option('widget_amazon_single_product');
												// options exist? if not set defaults
												if ( !is_array($options) )
													$options = array('title'=>'Book', 'id' => '1021', 'excerpt'=>'0');

												// form posted?
												if ( $_POST['amazon-submit'] ) {

													// Remember to sanitize and format use input appropriately.
													$options['title'] = strip_tags(stripslashes($_POST['amazon-title']));
													$options['id'] = strip_tags(stripslashes($_POST['amazon-id']));
													$options['excerpt'] = strip_tags(stripslashes($_POST['amazon-excerpt']));

													/* caution */
													update_option('widget_amazon_single_product', $options);

												}

												// Get options for form fields to show
												$title = htmlspecialchars($options['title'], ENT_QUOTES);
												$id = htmlspecialchars($options['id'], ENT_QUOTES);
												$excerpt = htmlspecialchars($options['excerpt'], ENT_QUOTES);

												// The form fields
												echo '<p style="text-align:right;">
														<label for="amazon-title">' . __('Title:') . ' 
														<input style="width: 200px;" id="amazon-title" name="amazon-title" type="text" value="'.$title.'" />
														</label></p>';
														echo '<p style="text-align:right;">
																<label for="amazon-id">' . __('ID:') . ' 
																<input style="width: 200px;" id="amazon-id" name="amazon-id" type="text" value="'.$id.'" />
																</label></p>';
												echo '<p style="text-align:right;">
														<label for="amazon-excerpt">' . __('Show excerpt:') . ' 
														<input style="width: 200px;" id="amazon-excerpt" name="amazon-excerpt" type="text" value="'.$excerpt.'" />
														</label></p>';

												echo '<input type="hidden" id="amazon-submit" name="amazon-submit" value="1" />';


									}//EOF

									/* TO CONTROL THE WIDGET IN FRONTEND */
									function widget_amazon_single_product ($contents) {

												// "$args is an array of strings that help widgets to conform to
												// the active theme: before_widget, before_title, after_widget,
												// and after_title are the array keys." - These are set up by the theme
												extract($args);

												// These are our own options
												$options = get_option('widget_amazon_single_product');
												$title = $options['title'];  // Title in sidebar for widget
												$id = $options['id'];  // The total looks
												$excerpt = $options['excerpt'];  // Showing the excerpt or not

												/* VALUES */
												$post_type = 'product_for_sale';

											// Output
											// echo $before_widget . $before_title . $title . $after_title;

											$args = array(
												'post_type'=> $post_type,
												'post__in' => array($id),
											);

											$query = new WP_Query($args);
											$all_products = $query->posts;
											// print_r($all_products);

											ob_start();

											foreach ($all_products as $product_single) {

						$amazon_item_AmazonAsin = get_post_meta($product_single->ID,'amazon_item_AmazonAsin', true);
						$amazon_item_AmazonTitle = get_post_meta($product_single->ID,'amazon_item_AmazonTitle', true);
						$amazon_item_AmazonDetailPageURL = get_post_meta($product_single->ID,'amazon_item_AmazonDetailPageURL', true);
						$amazon_item_AmazonMediumImageURL = get_post_meta($product_single->ID,'amazon_item_AmazonMediumImageURL', true);
						$amazon_item_AmazonMediumImageHeight = get_post_meta($product_single->ID,'amazon_item_AmazonMediumImageHeight', true);
						$amazon_item_AmazonMediumImageWidth = get_post_meta($product_single->ID,'amazon_item_AmazonMediumImageWidth', true);
						$amazon_item_AmazonAuthor = get_post_meta($product_single->ID,'amazon_item_AmazonAuthor', true);
						$amazon_item_AmazonManufacturer = get_post_meta($product_single->ID,'amazon_item_AmazonManufacturer', true);
						$amazon_item_AmazonStudio = get_post_meta($product_single->ID,'amazon_item_AmazonStudio', true);
						$amazon_item_AmazonSource = get_post_meta($product_single->ID,'amazon_item_AmazonSource', true);
						$amazon_item_AmazonEditorialReviewContent = get_post_meta($product_single->ID,'amazon_item_AmazonEditorialReviewContent', true);

						/* IN REPLACEMENT OF amazon_item_AmazonDetailPageURL */
						$permalink = get_permalink($product_single->ID);

						// 

											$contents = '<!-- amazon_single_product -->';
											$contents .= "\n";
											$contents .= '<h3 class="widget-title">'.$title.'</h3>';	
											$contents .= "\n";
											$contents .= '<div class="widget-amazon">';
											$contents .= '<!-- '.$id.' -->';
											$contents .= "\n";		

											$contents .= "\n";
											/* img */
											$contents .= '<div class="widget-amazon-photo">';		
											$contents .= '<a href="'.$permalink.'" class="photo" title="'.$amazon_item_AmazonTitle.'">';
											$contents .= '<img alt="'.$amazon_item_AmazonTitle.'" src="'.$amazon_item_AmazonMediumImageURL.'" width="'.$amazon_item_AmazonMediumImageWidth.'" height="'.$amazon_item_AmazonMediumImageHeight.'" >';
											$contents .= '</a>';
											$contents .= '</div>';	
											/* // img */

											/* title */
											$contents .= '<div class="widget-amazon-title">';
											$contents .= '<a href="'.$permalink.'" class="title" title="'.$amazon_item_AmazonTitle.'">';
											$contents .= ''.$amazon_item_AmazonTitle.'';
											$contents .= '</a>';
											$contents .= '</div>';		
											/* // title */


											/* excerpt */
											$contents .= '<!-- '.$excerpt.' -->';
											 if (empty($excerpt)) {
											    $contents .= '<!-- no excerpt show  -->';	
											} else {
												$contents .= '<div class="widget-amazon-excerpt">';
												$contents .= ''.strip_tags($product_single->post_excerpt).'';
												$contents .= '</div>';	

											}
											/* // excerpt */

											$contents .= '</div>';
											$contents .= "\n";
											$contents .= '<!-- //amazon_single_product -->';

									}//EOL
											ob_end_clean();	


											//Return the output		
											echo $contents;

									}//EOF

									/*****************************************************************************************/
									// REGISTER THE WIDGETS
									/*****************************************************************************************/


									// Register widget for use
									register_sidebar_widget(array('Amazon Single Product', 'widgets'), 'widget_amazon_single_product');

									// Register settings for use, 300x100 pixel form
									register_widget_control(array('Amazon Single Product', 'widgets'), 'widget_amazon_single_product_control', 300, 200);
								}//EOF for widget_amazon_init

								// Run code and init
								add_action('widgets_init', 'widget_amazon_init');
								/* // homepage_3_people_and_all_peoples */


								/*****************************************************************************************/
								/*
								// BEGIN Change the admin columns for all the post_type and post
								
								*/
								/*****************************************************************************************/
		
								/* // -----------  for Posts -----------  */
																
								/*  ADD specific columns for the posts */
								add_filter( 'manage_edit-post_columns', 'he3_edit_posts_columns' );
								add_action( 'manage_posts_custom_column', 'he3_posts_columns', 10, 2 );

								/* For Posts */
								function he3_edit_posts_columns( $columns ) {

								// Insert 'id' as the first custom column after checkbox
								$new_columns = array();

								foreach ( $columns as $key => $value ) {
								if ( $key === 'cb' ) {
								    $new_columns['cb'] = $value;
								    $new_columns['id'] = __( 'ID' );
								} else {
								    $new_columns[$key] = $value;
								}
								}

								// Add columns if not set by theme/plugins
								$new_columns['thumb'] = __( 'Thumbnail' );
								$new_columns['attachments'] = __( 'Attachments' );
								$new_columns['views'] = __( 'Views' );

								return $new_columns;
								}
								// End of he3_edit_posts_columns

								function he3_posts_columns( $column, $post_id ) {
								switch( $column ) {

								// ID column
								case 'id':
								    echo $post_id;
								    break;

								// Thumbnail column
								case 'thumb':
								    $thumb = get_the_post_thumbnail( $post_id, array( 125, 80 ) );
								    $url = admin_url( 'media-upload.php?post_id=' . $post_id . '&type=image&TB_iframe=1&width=640&height=296' );

								    if ( empty( $thumb ) ) {
								        echo __( 'No Thumbnail' );
								    } else {
								        $html = '<div>';
								        $html .= $thumb . '<br>';
								        $html .= '<a href="' . $url . '" id="set-post-thumbnail" class="thickbox">Select thumbnail</a>';
								        $html .= '</div>';
								        echo $html;
								    }
								    break;

								// Attachments column
								case 'attachments':
								    $attachments = get_children( array( 'post_parent' => $post_id ) );
								    $count = count( $attachments );
								    $html = '<code>' . $count . __( ' Files' ) . '</code>';

								    foreach ( $attachments as $att ) {
								        $html .= '<div style="float:left; padding: 2px; margin: 0 2px 5px; border: 1px solid #DFDFDF;">';
								        $html .= '<a href="' . esc_url( $att->guid ) . '" title="' . esc_attr( $att->post_title ) . '" rel="attached" class="thickbox">';
								        $html .= wp_get_attachment_image( $att->ID, array( 30, 30 ), true, array( "class" => "pinkynail" ) );
								        $html .= '</a></div>';
								    }
								    $html .= '<br style="clear:both;" />';
								    echo $html;
								    break;

								default:
								    break;
								}
								}
								// End of he3_posts_columns

								/*
								Uncomment if you want sortable columns
								// add_filter( 'manage_edit-post_sortable_columns', 'he3_posts_sortable_columns' );
								function he3_posts_sortable_columns( $columns ) {
								$columns['id'] = 'id';
								$columns['thumb'] = 'thumb';
								$columns['title'] = 'title';
								$columns['categories'] = 'categories';
								$columns['tags'] = 'tags';
								$columns['comments'] = 'comments';
								$columns['date'] = 'date';
								$columns['author'] = 'author';
								$columns['views'] = 'views';
								$columns['attachments'] = 'attachments';

								return $columns;
								}
								*/

								// // -----------  for Posts -----------  
	
	
	/* -----------  For Pages ----------- */
	
	/*  ADD specific columns for the pages */								
	add_filter( 'manage_edit-page_columns', 'he3_edit_pages_columns' ) ;
	add_action( 'manage_pages_custom_column', 'he3_pages_columns', 10, 2 );
	
	function he3_edit_pages_columns( $columns ) {

		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'author' => __( 'Auteur' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF	
	
	
	function he3_pages_columns ( $column, $post_id ) {
		global $post;

		switch( $column ) {
				/* id */
					case 'id' :
						$postid = get_the_ID();
						if ( empty( $postid ) )
							echo __( 'Unknown' );
						else
							printf( __( '%s' ), $postid );
						break;
				/* // id */
				
			/* thumb */
				case 'thumb' :
					$postid = get_the_ID();
					$thumb = get_the_post_thumbnail($post_id, array(125, 80) );
					
					if ( empty( $postid ) )
						echo __( 'Unknown' );
					else
					printf( __( '%s' ), $thumb );
						
					break;
			/* // thumb */
			
			/* views */
			case 'views' :

		  // global $wp_locale, $wpdb, $post;
			global $wpdb;
			/* values */
			$post_id = get_the_ID();			
			$type = "page";
			if ( empty( $post_id ) )
				echo __( 'Unknown' );
			else
				/* // MOST VIEWED PAGE */			
				/* QUERY */
				
				/*
				$sql = " SELECT 
				".$wpdb->prefix."posts.ID, 
				".$wpdb->prefix."postview.view, 
				".$wpdb->prefix."posts.post_date
				FROM ".$wpdb->prefix."posts 
				INNER JOIN ".$wpdb->prefix."postview ON ".$wpdb->prefix."posts.ID = ".$wpdb->prefix."postview.post_id
				WHERE
				".$wpdb->prefix."posts.post_status='publish' AND 
				".$wpdb->prefix."posts.post_parent=0 AND 
				".$wpdb->prefix."posts.post_type='".$type."' AND 
				".$wpdb->prefix."posts.ID='".$post_id."'
				";
				*/
				
				$sql = " SELECT 
				".$wpdb->prefix."postview.post_id, 
				".$wpdb->prefix."postview.view, 
				".$wpdb->prefix."postview.post_id
				FROM ".$wpdb->prefix."postview 
				INNER JOIN ".$wpdb->prefix."posts ON ".$wpdb->prefix."posts.ID = ".$wpdb->prefix."postview.post_id
				WHERE
				".$wpdb->prefix."postview.post_id='".$post_id."'
				";
				
				$results = $wpdb->get_results($sql);
        // print_r($results);
        foreach ( $results as $result ) 
        {
        	echo $result->view;
        }        
			/* // MOST VIEWED PAGE */
			break;
			
			/* // views */
			
			/* attachments */
				case 'attachments' :
					$postid = get_the_ID();
					$attachments = get_children(array('post_parent'=>$postid));
					$count = count($attachments);
					
					if ( empty( $postid ) )
						echo __( 'Unknown' );
					else
						    //printf( __( '%s' ), $count );
							// add_thickbox();
							$html = '<code>';
							$html .= $count. __(' Files').'</code>';

							foreach ($attachments as $att) {
									$html .= '<div style="float:left; padding: 2px; margin: 0 2px 5px; border: 1px solid #DFDFDF;">';
									$html .= '<a href="'.$att->guid.' " title="'.$att->post_title.'" rel="attached" class="thickbox">';
									$html .= wp_get_attachment_image( $att->ID, array(30, 30), true, array("class"=>"pinkynail") );
									$html .= '</a></div>' ;
							}             
							$html .= '<br style="clear:both;" />';
							echo $html;
						
					break;
			/* // attachments */
			
		

			/* - CAUTION - */
			/* Just break out of the switch statement for everything else. */
			default :										
			break;
				
		}//EOS
		
		
	}//EOF
	
	/* -----------  // For pages ----------- */
	
	/* -----------  For post_type ----------- */
	
	/*
	portfolio
	showcase
	team
	clients
	testimonials
	jobs
	faqs
	*/
	
	/*  ADD specific columns for the post_type */

	// For portfolio
	add_filter( 'manage_edit-portfolio_columns', 'he3_edit_posts_type_portfolio_columns' ) ;
	add_action( 'manage_portfolio_custom_column', 'he3_posts_type_columns', 10, 2 );

	function he3_edit_posts_type_portfolio_columns ( $columns ) {

		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'portfolio-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF

	// For showcase
	add_filter( 'manage_edit-showcase_columns', 'he3_edit_posts_type_showcase_columns' ) ;
	add_action( 'manage_showcase_custom_column', 'he3_posts_type_columns', 10, 2 );
	
	function he3_edit_posts_type_showcase_columns ( $columns ) {

		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'showcase-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF
	
	// For team
	add_filter( 'manage_edit-team_columns', 'he3_edit_posts_type_team_columns' ) ;
	add_action( 'manage_team_custom_column', 'he3_posts_type_columns', 10, 2 );
	
	function he3_edit_posts_type_team_columns ( $columns ) {

		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'team-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF
	
	// For clients
	add_filter( 'manage_edit-clients_columns', 'he3_edit_posts_type_clients_columns' ) ;
	add_action( 'manage_clients_custom_column', 'he3_posts_type_columns', 10, 2 );
	
	function he3_edit_posts_type_clients_columns ( $columns ) {

		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'clients-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF
	
	// For testimonials
	add_filter( 'manage_edit-testimonials_columns', 'he3_edit_posts_type_testimonials_columns' ) ;
	add_action( 'manage_testimonials_custom_column', 'he3_posts_type_columns', 10, 2 );
	
	function he3_edit_posts_type_testimonials_columns ( $columns ) {

		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'testimonials-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF


	// For jobs
	add_filter( 'manage_edit-jobs_columns', 'he3_edit_posts_type_jobs_columns' ) ;
	add_action( 'manage_jobs_custom_column', 'he3_posts_type_columns', 10, 2 );
	
	function he3_edit_posts_type_jobs_columns ( $columns ) {

		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'jobs-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF

	

	// For faqs // NOPE
	add_filter( 'manage_edit-faqs_columns', 'he3_edit_posts_type_faqs_columns' ) ;
	add_action( 'manage_faqs_custom_column', 'he3_posts_type_columns', 10, 2 );
	
	function he3_edit_posts_type_faqs_columns ( $columns ) {
		/*
		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'jobs-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);
		*/
		
		$columns = array(
					'cb' => '<input type="checkbox" />',
					'id' => __( 'ID' ),
					'thumb' => __( 'Thumbnail' ),
					'title' => __( 'Title' ),
					'faqs-category' => __( 'Categories' ),
					'tags' => __( 'Tags' ),
					'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
					'date' => __( 'Date' ),
					'author' => __( 'Auteur' ),
					'views' => __( 'Vue(s)' ),
					'attachments' => __( 'Attachments' ),
		);

		return $columns;
	}//EOF
	
	/* -----------  // For post_type ----------- */
	
						
/*****************************************************************************************/
							/*
								// END Change the admin columns for all the post_type and post
							*//*****************************************************************************************/
							
							/*****************************************************************************************/
							/*
								// GET THE DATE IN FRENCH
							*/
							/*****************************************************************************************/
// Voir http://webmaster.multimania.fr/tips/989424764/, check header.php for usage
							function MyFrenchDate () {		
									$jour["Monday"] = "Lundi";
									$jour["Tuesday"] = "Mardi";
									$jour["Wednesday"] = "Mercredi";
									$jour["Thursday"] = "Jeudi";
									$jour["Friday"] = "Vendredi";
									$jour["Saturday"] = "Samedi";
									$jour["Sunday"] = "Dimanche";

									function getJour($day) {
									return $jour[$day];
									}

									$mois["January"] = "Janvier";
									$mois["Febrary"] = "Février";
									$mois["March"] = "Mars";
									$mois["April"] = "Avril";
									$mois["May"] = "Mai";
									$mois["June"] = "Juin";
									$mois["July"] = "Juillet";
									$mois["August"] = "Août";
									$mois["September"] = "Septembre";
									$mois["October"] = "Octobre";
									$mois["November"] = "Novembre";
									$mois["December"] = "Décembre";

									function getMois($month){
									return $mois[$month];
									}

									$month = date(F);
									$day = date(l);

									getJour($day);
									getMois($month);


									print "$jour[$day] ";
									print date(d)." ";
									print "$mois[$month] ";
									print date(Y);
								}//EOF
							/*****************************************************************************************/
							/*
								// GET THE DATE IN FRENCH
							*/
							/*****************************************************************************************/

							/*****************************************************************************************/
							/*
								// GET THE FILENAME
							*/
							/*****************************************************************************************/
									
									
									function flaven_get_filename () {
										
										echo ('<!-- GET THE TPL FILE => '._PAGE_TYPE_.' -->');
									}

							/*****************************************************************************************/
							/*
								// GET THE FILENAME
							*/
							/*****************************************************************************************/

              /*****************************************************************************************/
							/*
								// ENABLE Link Manager
							*/
							/*****************************************************************************************/
									
									 /*
                     * See http://core.trac.wordpress.org/ticket/21307
                     */
									
									add_filter( 'pre_option_link_manager_enabled', '__return_true' );

							/*****************************************************************************************/
							/*
							// ENABLE Link Manager
							*/
							/*****************************************************************************************/							
							
							/*****************************************************************************************/
							/*
								// DEFINE a default post thumbnail
							*/
							/*****************************************************************************************/
							
              // http://justintadlock.com/archives/2012/07/05/how-to-define-a-default-post-thumbnail
             
              add_filter( 'post_thumbnail_html', 'bf_my_post_thumbnail_html' );

              function bf_my_post_thumbnail_html( $html ) {

              	if ( empty( $html ) )
              		$html = '<img src="' . trailingslashit( get_template_directory_uri() ) . 'images/default-thumbnail.png' . '" alt="" />';

              	return $html;
              }
              
              /*****************************************************************************************/
							/*
								// // DEFINE a default post thumbnail
							*/
							/*****************************************************************************************/
							
							
							/*****************************************************************************************/
                    /// BEGIN - Settings for the filtering columns for bf_quotes_manager
              /*****************************************************************************************/

              /*  ADD specific columns to the post_type bf_quotes_manager */
              add_filter( 'manage_edit-bf_quotes_manager_columns', 'my_edit_bf_quotes_manager_columns' ) ;

              add_action( 'manage_bf_quotes_manager_posts_custom_column', 'my_manage_bf_quotes_manager_columns', 10, 2 );

              	function my_edit_bf_quotes_manager_columns( $columns ) {

              		$columns = array(
              					'cb' => '<input type="checkbox" />',
              					'thumb' => __( 'Thumbnail' ),
              					'title' => __( 'Title' ),
              					'authors' => __( 'Author(s)' ),
              					'flavors' => __( 'Flavors(s)' ),
              					'shortcode_single' => ('Shortcode'),
              					'views' => __( 'Vue(s)' ),
              		);

              		return $columns;
              	}



              	function my_manage_bf_quotes_manager_columns ( $column, $post_id ) {
              		global $post;

              		switch( $column ) {

              				/* - bf_quotes_manager_genre - */

              				/* If displaying the column. */
              						case 'authors' :

              							/* Get the types for the post. */
              							$terms = get_the_terms( $post_id, 'bf_quotes_manager_author' );

              							/* If terms were found. */
              							if ( !empty( $terms ) ) {

              								$out = array();

              								/* Loop through each term, linking to the 'edit posts' page for the specific term. */
              								foreach ( $terms as $term ) {
              									$out[] = sprintf( '<a href="%s">%s</a>',
              										esc_url( add_query_arg( array( 'post_type' => $post->post_type, 'bf_quotes_manager_genre' => $term->slug ), 'edit.php' ) ),
              										esc_html( sanitize_term_field( 'name', $term->name, $term->term_id, 'bf_quotes_manager_genre', 'display' ) )
              									);
              								}

              								/* Join the terms, separating them with a comma. */
              								echo join( ', ', $out );
              							}

              							/* If no terms were found, output a default message. */
              							else {
              								_e( 'No Genres' );
              							}

              							break;
              				/* //- bf_quotes_manager_genre - */

              				/* - bf_quotes_manager_author - */

              							/* If displaying the column. */
              									case 'flavors' :

              										/* Get the types for the post. */
              										$terms = get_the_terms( $post_id, 'bf_quotes_manager_flavor' );

              										/* If terms were found. */
              										if ( !empty( $terms ) ) {

              											$out = array();

              											/* Loop through each term, linking to the 'edit posts' page for the specific term. */
              											foreach ( $terms as $term ) {
              												$out[] = sprintf( '<a href="%s">%s</a>',
              													esc_url( add_query_arg( array( 'post_type' => $post->post_type, 'bf_quotes_manager_flavor' => $term->slug ), 'edit.php' ) ),
              													esc_html( sanitize_term_field( 'name', $term->name, $term->term_id, 'bf_quotes_manager_flavor', 'display' ) )
              												);
              											}

              											/* Join the terms, separating them with a comma. */
              											echo join( ', ', $out );
              										}

              										/* If no terms were found, output a default message. */
              										else {
              											_e( 'No Flavor(s)' );
              										}

              										break;
              										/* // - bf_quotes_manager_flavor - */

              										/* - shortcode_single - */
              											/* If displaying the 'id' column. */
              											case 'shortcode_single' :

              												/* Get the id. */
              												$postid = get_the_ID();

              												/* If no id is found, output a default message. */
              												if ( empty( $postid ) )
              													echo __( 'Unknown' );

              												/* If there is a id, append 'id' to the text string. */
              												else
              							// printf( __( '<input value="[amazon_product_single posts="%s"]">' ), $postid );
              							printf( __( '<textarea rows="3" cols="15" wrap="hard">[bf_quotes_manager_single posts="%s"]</textarea>' ), $postid );
              												break;


              												 /* shortcode_single */


              												



              			/* - CAUTION - */

              			/* Just break out of the switch statement for everything else. */
              			default :
              				break;
              		}
              	}

              	add_filter( 'manage_edit-bf_quotes_manager_sortable_columns', 'my_bf_quotes_manager_sortable_columns' );

              	function my_bf_quotes_manager_sortable_columns( $columns ) {
              		$columns['cover'] = 'cover';
              		$columns['title'] = 'title';
              		$columns['authors'] = 'authors';
              		$columns['flavors'] = 'flavors';
              		$columns['shortcode_single'] = 'shortcode_single';
              		$columns['views'] = 'views';
              		// $columns['date'] = 'date';
              		// $columns['id'] = 'id';

              		return $columns;
              	}
              	/*****************************************************************************************/
              	      ///  END - Settings for the filtreing columns for bf_quotes_manager
              	/*****************************************************************************************/








              	/*****************************************************/
              	      /* SiteSpeed analysis 
              	      	check in https://developers.google.com/speed/pagespeed/insights/

              	      */
              	     
              	    // If you want the Async method
					/*function to add async to all scripts*/
					function add_async_attribute($tag){
					 # Add async to all remaining scripts
					 return str_replace( ' src', ' async="async" src', $tag );
					}
					add_filter( 'script_loader_tag', 'add_async_attribute', 10, 2);


					// remove query strings
				function remove_query_strings() {
						   if(!is_admin()) {
						       add_filter('script_loader_src', 'remove_query_strings_split', 15);
						       add_filter('style_loader_src', 'remove_query_strings_split', 15);
						   }
						}

				function remove_query_strings_split($src){
						   $output = preg_split("/(&ver|\?ver)/", $src);
						   return $output[0];
						}

				add_action('init', 'remove_query_strings');

				/*****************************************************/


/* Remove post_type=feedback from WP 
* http://flaven.fr/wp-admin/edit.php?post_type=feedback 
* */
function delete_post_type(){
  unregister_post_type( 'feedback');
}
add_action('init','delete_post_type', 100);


/*
If you want your theme to be backward compatible with older versions of WordPress, you will need to add a snippet in your functions.php file.
 */

if ( ! function_exists( 'wp_body_open' ) ) {
    function wp_body_open() {
        do_action( 'wp_body_open' );
    }
}

/* -----------  // For IA ----------- */

/* ===========================================================================
   BF SEMANTIC SEO FEATURES
   
   Dependencies:
   - bf_wp_related_embeddings_db plugin (provides bf_get_related_posts)
   - bf_wp_tag_families_db plugin (provides bf_get_related_tags)
   
   Features:
   - Level 1: Semantic breadcrumbs, related content footer, sidebar widget
   - Level 2: Schema.org structured data (Breadcrumbs, Article, CollectionPage)
   
   Usage:
   - Breadcrumbs: Call bf_semantic_breadcrumbs() in your template
   - Sidebar: Call bf_semantic_sidebar() in sidebar.php
   - Footer: Auto-added via 'the_content' filter
   - Schema: Auto-added via 'wp_head' action
   =========================================================================== */

/* ===========================================================================
   LEVEL 1: BASIC SEMANTIC SEO FEATURES
   =========================================================================== */

// ============================================================================
// 1. SEMANTIC BREADCRUMBS
// Shows: Home › Canonical Tag › Current Tag › Post Title
// ============================================================================

/**
 * Display semantic breadcrumbs with tag hierarchy
 * 
 * Shows hierarchical navigation using tag families:
 * - On single posts: Home > Parent Tag > Tag > Post Title
 * - On tag archives: Home > Parent Tag > Current Tag
 * 
 * @return void Echoes HTML directly
 * 
 * Usage: Add to single.php or content-single.php:
 * <?php bf_semantic_breadcrumbs(); ?>
 */
function bf_semantic_breadcrumbs() {
    // Don't show breadcrumbs on front page
    if ( is_front_page() ) {
        return;
    }
    
    // Only show on single posts and tag archives
    if ( ! is_single() && ! is_tag() ) {
        return;
    }
    
    global $wpdb;
    
    echo '<div class="entry-breadcrumb">';
    echo '<nav class="bf-breadcrumbs" aria-label="Breadcrumb">';
    echo '<span class="breadcrumb-icon">📍</span> ';
    echo '<a href="' . esc_url( home_url() ) . '">Home</a>';
    echo ' <span class="breadcrumb-separator">›</span> ';
    
    if ( is_single() ) {
        bf_breadcrumbs_single_post( $wpdb );
    } elseif ( is_tag() ) {
        bf_breadcrumbs_tag_archive( $wpdb );
    }
    
    echo '</nav>';
    echo '</div>';
}

/**
 * Helper: Generate breadcrumbs for single post
 * 
 * @param object $wpdb WordPress database object
 * @return void Echoes HTML directly
 */
function bf_breadcrumbs_single_post( $wpdb ) {
    $tags = get_the_tags();
    
    if ( $tags ) {
        $first_tag = $tags[0];
        
        // Show canonical (parent) tag if exists and is different from current tag
        $canonical_tag = bf_get_canonical_tag( $wpdb, $first_tag->term_id );
        if ( $canonical_tag && $canonical_tag->term_id != $first_tag->term_id ) {
            echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
            echo esc_html( $canonical_tag->name );
            echo '</a> <span class="breadcrumb-separator">›</span> ';
        }
        
        // Show current post's primary tag
        echo '<a href="' . esc_url( get_tag_link( $first_tag->term_id ) ) . '">';
        echo esc_html( $first_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show current post title (not linked)
    echo '<span class="breadcrumb-current">' . esc_html( get_the_title() ) . '</span>';
}

/**
 * Helper: Generate breadcrumbs for tag archive page
 * 
 * @param object $wpdb WordPress database object
 * @return void Echoes HTML directly
 */
function bf_breadcrumbs_tag_archive( $wpdb ) {
    $current_tag = get_queried_object();
    
    // Show canonical (parent) tag if exists
    $canonical_tag = bf_get_canonical_tag( $wpdb, $current_tag->term_id );
    if ( $canonical_tag && $canonical_tag->term_id != $current_tag->term_id ) {
        echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
        echo esc_html( $canonical_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show current tag (not linked)
    echo '<span class="breadcrumb-current">' . esc_html( $current_tag->name ) . '</span>';
}

/**
 * Helper: Get canonical (parent) tag for a given tag ID
 * 
 * Queries the tag_families table to find the canonical tag
 * that represents the parent topic cluster
 * 
 * @param object $wpdb WordPress database object
 * @param int $tag_id The tag ID to look up
 * @return object|null Tag object or null if not found
 */
function bf_get_canonical_tag( $wpdb, $tag_id ) {
    $canonical = $wpdb->get_row( $wpdb->prepare(
        "SELECT canonical_tag_id 
         FROM {$wpdb->prefix}tag_families 
         WHERE tag_id = %d 
         LIMIT 1",
        $tag_id
    ) );
    
    if ( $canonical && $canonical->canonical_tag_id ) {
        return get_tag( $canonical->canonical_tag_id );
    }
    
    return null;
}

// ============================================================================
// 2. SIDEBAR WIDGET (Related Posts + Tags)
// Shows both related articles and related topics in sidebar
// ============================================================================

/**
 * Semantic Sidebar Widget
 * 
 * Displays:
 * - Related posts (5 most similar articles)
 * - Related tags (5 semantically similar topics)
 * 
 * @return void Echoes HTML directly
 * 
 * Usage: Add to sidebar.php:
 * <?php if ( is_single() ) { bf_semantic_sidebar(); } ?>
 */
function bf_semantic_sidebar() {
    // Only show on single post pages
    if ( ! is_single() ) {
        return;
    }
    
    global $post;
    
    ?>
    <div class="semantic-sidebar-widget">
        
        <!-- Related Posts Section -->
        <?php if ( function_exists( 'bf_get_related_posts' ) ) : ?>
            <?php
            $related_posts = bf_get_related_posts( $post->ID, 5 );
            if ( $related_posts ) :
            ?>
                <div class="related-posts-section">
                    <h3>Related Articles</h3>
                    <ul>
                        <?php foreach ( $related_posts as $related ) : ?>
                            <li>
                                <a href="<?php echo esc_url( $related['permalink'] ); ?>">
                                    <?php echo esc_html( $related['title'] ); ?>
                                </a>
                                <small class="similarity-score">
                                    (<?php echo number_format( $related['similarity'], 2 ); ?>)
                                </small>
                            </li>
                        <?php endforeach; ?>
                    </ul>
                </div>
            <?php endif; ?>
        <?php endif; ?>
        
        <!-- Related Tags Section -->
        <?php if ( function_exists( 'bf_get_related_tags' ) ) : ?>
            <?php
            $tags = get_the_tags();
            if ( $tags ) {
                $related_tags = bf_get_related_tags( $tags[0]->term_id, 5 );
                if ( $related_tags ) :
                ?>
                    <div class="related-tags-section">
                        <h3>Explore Topics</h3>
                        <div class="tag-cloud">
                            <?php foreach ( $related_tags as $tag ) : ?>
                                <a href="<?php echo esc_url( $tag['url'] ); ?>" class="tag-badge">
                                    <?php echo esc_html( $tag['name'] ); ?>
                                    <small>(<?php echo intval( $tag['count'] ); ?>)</small>
                                </a>
                            <?php endforeach; ?>
                        </div>
                    </div>
                <?php
                endif;
            }
            ?>
        <?php endif; ?>
        
    </div>
    
    <!-- Inline Styles for Sidebar Widget -->
    <style>
    .semantic-sidebar-widget {
        background: #f9f9f9;
        padding: 20px;
        border-left: 4px solid #0073aa;
        margin-bottom: 30px;
    }
    .semantic-sidebar-widget h3 {
        margin-top: 0;
        font-size: 18px;
        color: #333;
        border-bottom: 2px solid #0073aa;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .semantic-sidebar-widget .related-posts-section {
        margin-bottom: 30px;
    }
    .semantic-sidebar-widget ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .semantic-sidebar-widget ul li {
        padding: 8px 0;
        border-bottom: 1px solid #eee;
    }
    .semantic-sidebar-widget ul li:last-child {
        border-bottom: none;
    }
    .semantic-sidebar-widget ul li a {
        color: #0073aa;
        text-decoration: none;
        font-weight: 500;
    }
    .semantic-sidebar-widget ul li a:hover {
        text-decoration: underline;
    }
    .semantic-sidebar-widget .similarity-score {
        color: #999;
        font-size: 12px;
        margin-left: 5px;
    }
    .tag-badge {
        display: inline-block;
        padding: 6px 12px;
        margin: 3px;
        background: white;
        border: 1px solid #ddd;
        border-radius: 3px;
        text-decoration: none;
        font-size: 13px;
        color: #0073aa;
        transition: all 0.2s ease;
    }
    .tag-badge:hover {
        background: #0073aa;
        color: white;
        border-color: #0073aa;
    }
    .tag-badge small {
        color: #999;
        font-size: 11px;
    }
    .tag-badge:hover small {
        color: rgba(255, 255, 255, 0.8);
    }
    </style>
    <?php
}

// ============================================================================
// 3. AUTO-RELATED CONTENT IN POST FOOTER
// Automatically adds related posts and tags after post content
// ============================================================================

/**
 * Auto-add related content to single post footer
 * 
 * Appends to post content:
 * - 3 related posts with thumbnails
 * - 8 related tags in a tag cloud
 * 
 * @param string $content The post content
 * @return string Modified content with related items appended
 */
function bf_auto_related_content( $content ) {
    // Only on single posts in main query
    if ( ! is_single() || ! is_main_query() ) {
        return $content;
    }
    
    // Prevent infinite loop when rendering related post excerpts
    remove_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    global $post;
    $footer = '';
    
    // Render related posts section
    if ( function_exists( 'bf_get_related_posts' ) ) {
        $related_posts = bf_get_related_posts( $post->ID, 3 );
        if ( $related_posts ) {
            $footer .= bf_render_related_posts( $related_posts );
        }
    }
    
    // Render related tags section
    if ( function_exists( 'bf_get_related_tags' ) ) {
        $tags = get_the_tags();
        if ( $tags ) {
            $related_tags = bf_get_related_tags( $tags[0]->term_id, 8 );
            if ( $related_tags ) {
                $footer .= bf_render_related_tags( $related_tags );
            }
        }
    }
    
    // Restore filter for next post
    add_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    // Wrap footer content if we have any
    if ( $footer ) {
        $footer = '<div class="bf-post-footer" style="margin-top: 50px; padding-top: 30px; border-top: 2px solid #eee;">' 
                . $footer 
                . '</div>';
    }
    
    return $content . $footer;
}
add_filter( 'the_content', 'bf_auto_related_content', 999 );

/**
 * Helper: Render related posts HTML
 * 
 * Creates a responsive grid of related post cards with:
 * - Featured image (if available)
 * - Post title
 * - Excerpt (trimmed to 15 words)
 * 
 * @param array $related_posts Array of related post data from plugin
 * @return string HTML markup for related posts grid
 */
function bf_render_related_posts( $related_posts ) {
    $html = '<h3 style="font-size: 24px; margin-bottom: 20px; color: #333;">Continue Reading</h3>';
    $html .= '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">';
    
    foreach ( $related_posts as $related ) {
        $html .= '<div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; transition: transform 0.2s;">';
        
        // Featured image (if exists)
        if ( ! empty( $related['thumbnail'] ) ) {
            $html .= '<a href="' . esc_url( $related['permalink'] ) . '">';
            $html .= '<img src="' . esc_url( $related['thumbnail'] ) . '" ';
            $html .= 'style="width: 100%; height: 180px; object-fit: cover;" ';
            $html .= 'alt="' . esc_attr( $related['title'] ) . '">';
            $html .= '</a>';
        }
        
        // Post title and excerpt
        $html .= '<div style="padding: 20px;">';
        $html .= '<h4 style="font-size: 18px; margin: 0 0 10px 0; line-height: 1.4;">';
        $html .= '<a href="' . esc_url( $related['permalink'] ) . '" style="text-decoration: none; color: #333;">';
        $html .= esc_html( $related['title'] );
        $html .= '</a></h4>';
        $html .= '<p style="font-size: 14px; color: #666; margin: 0;">';
        $html .= esc_html( wp_trim_words( $related['excerpt'], 15 ) );
        $html .= '</p>';
        $html .= '</div>';
        
        $html .= '</div>';
    }
    
    $html .= '</div>';
    return $html;
}

/**
 * Helper: Render related tags HTML
 * 
 * Creates a tag cloud of semantically related topics
 * Shows tag name and post count for each tag
 * 
 * @param array $related_tags Array of related tag data from plugin
 * @return string HTML markup for related tags section
 */
function bf_render_related_tags( $related_tags ) {
    $html = '<div style="background: #f9f9f9; padding: 20px; border-radius: 8px;">';
    $html .= '<h4 style="font-size: 16px; color: #666; margin: 0 0 15px 0;">Explore Related Topics</h4>';
    
    foreach ( $related_tags as $tag ) {
        $html .= '<a href="' . esc_url( $tag['url'] ) . '" ';
        $html .= 'style="display: inline-block; padding: 8px 15px; margin: 5px 5px 5px 0; ';
        $html .= 'background: white; border: 1px solid #ddd; border-radius: 4px; ';
        $html .= 'text-decoration: none; font-size: 14px; color: #0073aa; transition: all 0.2s;">';
        $html .= esc_html( $tag['name'] );
        $html .= ' <small style="color: #999;">(' . intval( $tag['count'] ) . ')</small>';
        $html .= '</a>';
    }
    
    $html .= '</div>';
    return $html;
}

/* ===========================================================================
   LEVEL 2: STRUCTURED DATA (Schema.org JSON-LD)
   Adds rich snippets for better Google search appearance
   =========================================================================== */

// ============================================================================
// 4. BREADCRUMB SCHEMA (Rich Snippets in Google)
// Makes breadcrumbs appear in search results
// ============================================================================

/**
 * Schema.org BreadcrumbList for Google Rich Snippets
 * 
 * Adds JSON-LD structured data to show breadcrumb trail in Google search results.
 * Uses semantic tag families to build hierarchical navigation.
 * 
 * @return void Echoes JSON-LD script tag in <head>
 */
function bf_breadcrumb_schema() {
    // Only add schema on single posts and tag archives
    if ( ! is_single() && ! is_tag() ) {
        return;
    }
    
    $items = array();
    $position = 1;
    
    // Always start with Home
    $items[] = array(
        '@type' => 'ListItem',
        'position' => $position++,
        'name' => 'Home',
        'item' => home_url()
    );
    
    if ( is_single() ) {
        global $post, $wpdb;
        
        $tags = get_the_tags();
        if ( $tags ) {
            $first_tag = $tags[0];
            
            // Get canonical (parent) tag from tag families table
            $canonical = $wpdb->get_row( $wpdb->prepare(
                "SELECT canonical_tag_id, canonical_label 
                 FROM {$wpdb->prefix}tag_families 
                 WHERE tag_id = %d 
                 LIMIT 1",
                $first_tag->term_id
            ) );
            
            // Add canonical tag to breadcrumb if it's different from current tag
            if ( $canonical && $canonical->canonical_tag_id != $first_tag->term_id ) {
                $canonical_tag = get_tag( $canonical->canonical_tag_id );
                if ( $canonical_tag ) {
                    $items[] = array(
                        '@type' => 'ListItem',
                        'position' => $position++,
                        'name' => $canonical_tag->name,
                        'item' => get_tag_link( $canonical_tag->term_id )
                    );
                }
            }
            
            // Add current post's primary tag
            $items[] = array(
                '@type' => 'ListItem',
                'position' => $position++,
                'name' => $first_tag->name,
                'item' => get_tag_link( $first_tag->term_id )
            );
        }
        
        // Add current post (last item has no 'item' property per schema.org spec)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => get_the_title()
        );
        
    } elseif ( is_tag() ) {
        global $wpdb;
        $current_tag = get_queried_object();
        
        // Get canonical (parent) tag
        $canonical = $wpdb->get_row( $wpdb->prepare(
            "SELECT canonical_tag_id, canonical_label 
             FROM {$wpdb->prefix}tag_families 
             WHERE tag_id = %d 
             LIMIT 1",
            $current_tag->term_id
        ) );
        
        // Add canonical tag if this is a child tag
        if ( $canonical && $canonical->canonical_tag_id != $current_tag->term_id ) {
            $canonical_tag = get_tag( $canonical->canonical_tag_id );
            if ( $canonical_tag ) {
                $items[] = array(
                    '@type' => 'ListItem',
                    'position' => $position++,
                    'name' => $canonical_tag->name,
                    'item' => get_tag_link( $canonical_tag->term_id )
                );
            }
        }
        
        // Add current tag (last item has no 'item' property)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => $current_tag->name
        );
    }
    
    // Build complete schema
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'BreadcrumbList',
        'itemListElement' => $items
    );
    
    // Output JSON-LD script in <head>
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_breadcrumb_schema' );

// ============================================================================
// 5. TAG ARCHIVE SCHEMA (CollectionPage for Topic Clusters)
// Helps Google understand topic cluster pages
// ============================================================================

/**
 * CollectionPage Schema for Tag Archives
 * 
 * Adds structured data to tag archive pages showing:
 * - Parent topic relationship
 * - Related tag pages
 * 
 * This helps Google understand your topic cluster structure.
 * 
 * @return void Echoes JSON-LD script tag in <head>
 */
function bf_tag_archive_schema() {
    // Only add on tag archive pages
    if ( ! is_tag() ) {
        return;
    }
    
    $current_tag = get_queried_object();
    global $wpdb;
    
    // Get tag family information
    $canonical = $wpdb->get_row( $wpdb->prepare(
        "SELECT canonical_tag_id, canonical_label 
         FROM {$wpdb->prefix}tag_families 
         WHERE tag_id = %d 
         LIMIT 1",
        $current_tag->term_id
    ) );
    
    // Get semantically related tags (limit to 8 for performance)
    $related_tags = array();
    if ( function_exists( 'bf_get_related_tags' ) ) {
        $related_tags_data = bf_get_related_tags( $current_tag->term_id, 8 );
        if ( $related_tags_data ) {
            foreach ( $related_tags_data as $tag ) {
                $related_tags[] = $tag['url'];
            }
        }
    }
    
    // Build base schema
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'CollectionPage',
        'name' => $current_tag->name . ' - ' . get_bloginfo( 'name' ),
        'description' => $current_tag->description ?: 'Articles about ' . $current_tag->name,
        'url' => get_tag_link( $current_tag->term_id )
    );
    
    // Add parent topic if this is a subtopic (not the canonical tag itself)
    if ( $canonical && $canonical->canonical_tag_id != $current_tag->term_id ) {
        $canonical_tag = get_tag( $canonical->canonical_tag_id );
        if ( $canonical_tag ) {
            $schema['isPartOf'] = array(
                '@type' => 'CollectionPage',
                'name' => $canonical_tag->name,
                'url' => get_tag_link( $canonical_tag->term_id )
            );
        }
    }
    
    // Add related tag pages
    if ( ! empty( $related_tags ) ) {
        $schema['relatedLink'] = $related_tags;
    }
    
    // Output JSON-LD script in <head>
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_tag_archive_schema', 20 );

/* ===========================================================================
   END BF SEMANTIC SEO FEATURES
   =========================================================================== */

   
/* -----------  // For IA ----------- */




