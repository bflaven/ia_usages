<?php
/**
 * Template part for displaying single posts.
 *
 * @package Zaatar
 */
?>
<?php
/*
define ('_PAGE_TYPE_', 'content-product_for_sale.php');
echo ('<!-- PAGE '._PAGE_TYPE_.' -->');
*/
?>

<div class="post-wrapper-hentry">
	<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
		<div class="post-content-wrapper post-content-wrapper-single post-content-wrapper-single-post">

			<div class="entry-header-wrapper">
				<header class="entry-header">
					<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
				</header><!-- .entry-header -->

				<div class="entry-meta entry-meta-header-after">
					<?php
					allium_posted_by();
					allium_posted_on();
					allium_post_edit_link();
					?>
				</div><!-- .entry-meta -->
			</div><!-- .entry-header-wrapper -->

			<div class="entry-content">
				<?php allium_post_thumbnail_single(); ?>
				<?php the_content(); ?>
				
				<?php
								/* print_r($post); */

						$amazon_item_AmazonAsin = get_post_meta($post->ID,'amazon_item_AmazonAsin', true);
						$amazon_item_AmazonTitle = get_post_meta($post->ID,'amazon_item_AmazonTitle', true);
						$amazon_item_AmazonDetailPageURL = get_post_meta($post->ID,'amazon_item_AmazonDetailPageURL', true);
						$amazon_item_AmazonMediumImageURL = get_post_meta($post->ID,'amazon_item_AmazonMediumImageURL', true);
						$amazon_item_AmazonMediumImageHeight = get_post_meta($post->ID,'amazon_item_AmazonMediumImageHeight', true);
						$amazon_item_AmazonMediumImageWidth = get_post_meta($post->ID,'amazon_item_AmazonMediumImageWidth', true);
						$amazon_item_AmazonAuthor = get_post_meta($post->ID,'amazon_item_AmazonAuthor', true);
						$amazon_item_AmazonManufacturer = get_post_meta($post->ID,'amazon_item_AmazonManufacturer', true);
						$amazon_item_AmazonStudio = get_post_meta($post->ID,'amazon_item_AmazonStudio', true);
						$amazon_item_AmazonSource = get_post_meta($post->ID,'amazon_item_AmazonSource', true);
						$amazon_item_AmazonEditorialReviewContent = get_post_meta($post->ID,'amazon_item_AmazonEditorialReviewContent', true);
						
						/* IN REPLACEMENT OF amazon_item_AmazonDetailPageURL */
						$permalink = get_permalink($post->ID);

							?>
											
											<!-- <?php echo (''.$amazon_item_AmazonAsin.''); ?> -->
										<div class="textwidget-unique text">

										        <div class="textwidget-photo">
										                <a href="<?php echo $amazon_item_AmazonDetailPageURL;?>" class="photo" title="<?php echo $amazon_item_AmazonTitle;?>"><img alt="<?php echo $amazon_item_AmazonTitle;?>" src="<?php echo $amazon_item_AmazonMediumImageURL;?>" width="<?php echo $amazon_item_AmazonMediumImageWidth;?>" height="<?php echo $amazon_item_AmazonMediumImageHeight;?>"></a>
										            </div>
											<div class="info half">
												<h2 class="product-title"><a class="head" href="<?php echo $amazon_item_AmazonDetailPageURL;?>" title="<?php echo $amazon_item_AmazonTitle;?>"><?php echo $amazon_item_AmazonTitle;?></a></h2>
												
												

										        <p class="product-excerpt"><?php 

										echo (''.$post->post_excerpt.'');

										?></p>

										<footer class="entry-meta entry-meta-footer">
							
										<?php 

													/* tags-links tags-links-single */

							$product_for_sale_genre = get_the_term_list($post->ID, 'product_for_sale_genre', 'Type(s) : ', ', ', '' );
							$product_for_sale_author = get_the_term_list($post->ID, 'product_for_sale_author', 'Author(s) : ', ', ', '' );
							$product_for_sale_kw = get_the_term_list($post->ID, 'product_for_sale_kw', 'Publisher(s) : ', ', ', '' );



													
													/* GENRES */
													if ( !empty( $product_for_sale_genre)) {
															print('<span class="tags-links tags-links-single">');
															echo (''.$product_for_sale_genre.'');
															print('</span><br>');
													} 

													/* AUTHORS */
													if ( !empty( $product_for_sale_author)) {
														print('<span class="tags-links tags-links-single">');
															echo (''.$product_for_sale_author.'');
															print('</span><br>');
													}

													/* KWS */
													if ( !empty( $product_for_sale_kw)) {
															print('<span class="tags-links tags-links-single">');
															echo (''.$product_for_sale_kw.'');
															print('</span><br>');
													}
													


												  ?>
										</footer>
										<br/>
										<div class="but-wrap"><a href="<?php echo $amazon_item_AmazonDetailPageURL;?>" class="button"><span><i class="more"></i>+ d'infos</span></a></div>
											</div>
											<!-- separator -->
											<div class="clear-div"></div>


				<?php
				/*
					wp_link_pages( array(
						'before'      => '<div class="page-links"><span class="page-links-title">' . esc_html__( 'Pages:', 'zaatar' ) . '</span>',
						'after'       => '</div>',
						'link_before' => '<span>',
						'link_after'  => '</span>',
					) );
				*/
				?>
			</div><!-- .entry-content -->

			<footer class="entry-meta entry-meta-footer">
				<?php allium_entry_footer(); ?>
			</footer><!-- .entry-meta -->

		</div><!-- .post-content-wrapper -->
	</article><!-- #post-## -->
</div><!-- .post-wrapper-hentry -->
