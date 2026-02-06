<?php
/**
 * The template for displaying site top navigation
 *
 * @package Zaatar
 */
?>

<nav id="top-navigation" class="top-navigation" role="navigation">
	<?php
	// Top Menu
	wp_nav_menu( apply_filters( 'allium_top_menu_args', array(
		'container'       => 'div',
		'container_class' => 'site-top-menu',
		'fallback_cb'     => false,
		'theme_location'  => 'top-menu',
		'menu_class'      => 'top-menu',
		'menu_id'         => 'menu-2',
		'depth'           => 1,
	) ) );
	?>
</nav><!-- .top-navigation -->
