<?php
/**
 * The header for our theme.
 *
 * Displays all of the <head> section and everything up till <div id="content">
 *
 * @package Zaatar
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="profile" href="http://gmpg.org/xfn/11">
<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php 
if ( function_exists( 'wp_body_open' ) ) {
    wp_body_open();
} else {
    do_action( 'wp_body_open' );
}
?>

<div id="page" class="site-wrapper site">

	<?php if ( has_nav_menu( 'top-menu' ) ) : ?>
	<div class="top-bar">
		<div class="container">
			<div class="row">
				<div class="col">
					<?php
					// Site Top Navigation
					get_template_part( 'template-parts/header/site-top-navigation' );
					?>
				</div><!-- .col -->
			</div><!-- .row -->
		</div><!-- .container -->
	</div><!-- .top-bar -->
	<?php endif; ?>

	<header id="masthead" class="site-header" role="banner">
		<div class="container">
			<div class="row">
				<div class="col">

					<div class="site-header-inside-wrapper">
						<?php
						// Site Branding
						get_template_part( 'template-parts/header/site-branding' );
						?>

						<?php
						// Site Navigation
						get_template_part( 'template-parts/header/site-navigation' );
						?>
					</div><!-- .site-header-inside-wrapper -->

				</div><!-- .col -->
			</div><!-- .row -->
		</div><!-- .container -->
	</header><!-- #masthead -->

	<div id="content" class="site-content">
