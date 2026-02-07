<?php
/**
 * The template for displaying header site branding
 *
 * @package Zaatar
 */
?>

<div class="site-branding-wrapper">
	<?php if ( has_custom_logo() ) : ?>
		<div class="site-logo-wrapper site-logo"><?php the_custom_logo(); ?></div>
	<?php endif; ?>

	<div class="site-branding">
		<?php if ( is_front_page() && is_home() ) : ?>
		<h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" title="<?php echo esc_attr( get_bloginfo( 'name', 'display' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></h1>
		<?php else : ?>
			<p class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" title="<?php echo esc_attr( get_bloginfo( 'name', 'display' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></p>
		<?php endif; ?>

		<?php
		$allium_description = get_bloginfo( 'description', 'display' );
		if ( $allium_description || is_customize_preview() ) :
		?>
		<p class="site-description"><?php echo esc_html( $allium_description ); /* WPCS: xss ok. */ ?></p>
		<?php endif; ?>
	</div>
</div><!-- .site-branding-wrapper -->
