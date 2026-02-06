<?php
/**
 * The template part for displaying an Author Bio
 *
 * @package Zaatar
 */
?>

<div class="entry-author">
	<?php 
	// Display relate editorial
	if ( function_exists( 'semaphore_render_footer_related' ) ) { semaphore_render_footer_related(); 
	} ?>
</div><!-- .related-ediorial-ia -->



<div class="entry-author">
	<?php 
	// Display relate editorial
	if ( function_exists( 'totomo_related_posts' ) ) { totomo_related_posts(); 
	} ?>
	
</div><!-- .entry-author -->
