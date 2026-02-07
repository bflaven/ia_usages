<?php
/**
 * The Sidebar containing the main widget areas.
 *
 * @package Zaatar
 */

if ( ! allium_has_sidebar() ) {
	return;
}
?>
<div id="site-sidebar" class="sidebar-area <?php allium_layout_class( 'sidebar' ); ?>">

<?php 
// Safe: Check function exists before calling
if ( function_exists( 'semaphore_semantic_sidebar' ) && is_single() ) {
    semaphore_semantic_sidebar();
}
?>


<div id="secondary" class="sidebar widget-area sidebar-widget-area" role="complementary">
		<?php dynamic_sidebar( 'sidebar-1' ); ?>
	</div><!-- .sidebar -->
</div><!-- .col-* columns of main sidebar -->
