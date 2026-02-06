<?php
/**
 * Template part for displaying single posts.
 *
 * @package Zaatar
 */
?>
<!-- content-bf_videos_manager.php -->

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


/* 
// YOUTUBE
bf_videos_manager_video_link
bf_videos_manager_video_id
bf_videos_manager_video_link_to_content

// AMAZON
bf_videos_manager_video_link_to_amazon
bf_videos_manager_video_title_link_to_amazon

// GITHUB
bf_videos_manager_video_link_to_github
bf_videos_manager_video_title_link_to_github

// YOUTUBE CHANNEL
bf_videos_manager_video_link_to_youtube_channel
bf_videos_manager_video_title_link_to_youtube_channel


*/

	// YOUTUBE
	$bf_video_link = get_post_meta($post->ID,'bf_videos_manager_video_link', true);
	$bf_video_id = get_post_meta($post->ID,'bf_videos_manager_video_id', true);

	// print YT embed
	echo ('<p>');
	echo('<!-- '.$bf_video_id.' :: '.$bf_video_link.' -->');
	echo('<iframe width="560" height="315" src="https://www.youtube.com/embed/'.$bf_video_id.'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>');
	echo ('</p>');

?>

<?php 

	// Check the related things
	
	// YOUTUBE
	$bf_video_content_linked = get_post_meta($post->ID,'bf_videos_manager_video_link_to_content', true);


	// AMAZON
	$bf_video_book_linked = get_post_meta($post->ID,'bf_videos_manager_video_link_to_amazon', true);
	$bf_video_book_linked_title = get_post_meta($post->ID,'bf_videos_manager_video_title_link_to_amazon', true);


	// GITHUB
	$bf_video_repo_github_linked = get_post_meta($post->ID,'bf_videos_manager_video_link_to_github', true);
	$bf_video_repo_github_linked_title = get_post_meta($post->ID,'bf_videos_manager_video_title_link_to_github', true);
	
	// YOUTUBE
	$bf_video_yt_channel_linked = get_post_meta($post->ID,'bf_videos_manager_video_link_to_youtube_channel', true);
	$bf_video_yt_channel_linked_title = get_post_meta($post->ID,'bf_videos_manager_video_title_link_to_youtube_channel', true);


	// needed if you want to grab elements from a post or a page
	$related_post = get_post($bf_video_content_linked);


	?>

				<?php 
				/* LINKED CONTENT */
				if (!$bf_video_content_linked ) { 
					// No article or page linked
					
				} else {

						print ('<div class="related-article">');
						print ('<h2 class="box-title">Related Content</h2>');
						

						$related_post_thumbnail = get_the_post_thumbnail( $related_post->ID, 'thumbnail' );

						$related_post_class_format = '';
						if ( ! $related_post_thumbnail ) {
						$related_post_class_format = 'fa-format-' . get_post_format( $related_post->ID );
						}

						printf(
						'
							<a href="%s" class="post-thumbnail %s">%s</a>
							<div class="related-post-content">
								<span class="date">%s</span>
								<p><a href="%s" class="related-video-article-link">%s</a></p>
							</div>

						',
						esc_url( get_permalink($related_post->ID) ),
						$related_post_class_format,
						$related_post_thumbnail,
						get_the_date( 'dS M Y', $post->ID ),
						esc_url( get_permalink($related_post->ID) ),
						get_the_title($related_post->ID)
						);

						wp_reset_postdata();
						print ('</div>');
					}

		/* // LINKED CONTENT */
		?>




		<?php  
		/* MORE RESSOURCES*/

		
	/*
-- ID for icons_for_promotion_amazon_585x330.png :: 11811
-- ID for icons_for_promotion_github_585x330.png :: 11812
-- ID for icons_for_promotion_youtube_585x330.png :: 11810

	 */
	
	define ('_ICON_PROMOTION_FORMAT_', 'thumbnail');

	// AMAZON
	// define ('_ICON_PROMOTION_AMAZON_ID_', '11811');
	// define ('_ICON_PROMOTION_AMAZON_ID_', '11815');
	define ('_ICON_PROMOTION_AMAZON_ID_', '11819');
	
	
	// GITHUB
	// define ('_ICON_PROMOTION_GITHUB_ID_', '11812');
	// define ('_ICON_PROMOTION_GITHUB_ID_', '11813');
	// define ('_ICON_PROMOTION_GITHUB_ID_', '11814');
	define ('_ICON_PROMOTION_GITHUB_ID_', '11818');
	

	// YOUTUBE
	// define ('_ICON_PROMOTION_YOUTUBE_ID_', '11810');
	// define ('_ICON_PROMOTION_YOUTUBE_ID_', '11816');
	define ('_ICON_PROMOTION_YOUTUBE_ID_', '11817');
	
	
	
	
	$icon_promotion_amazon = wp_get_attachment_image_src(_ICON_PROMOTION_AMAZON_ID_, _ICON_PROMOTION_FORMAT_);
	$icon_promotion_github = wp_get_attachment_image_src(_ICON_PROMOTION_GITHUB_ID_, _ICON_PROMOTION_FORMAT_);
	$icon_promotion_youtube = wp_get_attachment_image_src(_ICON_PROMOTION_YOUTUBE_ID_, _ICON_PROMOTION_FORMAT_);

		if ( ($bf_video_book_linked) || ($bf_video_repo_github_linked) || ($bf_video_yt_channel_linked) ) { 

				print('<br/>');
				print ('<div class="related-article">');
				print ('<h2 class="box-title">More ressources</h2>');
				print ('<ul class="row">');
				echo("\n");

		} 
	
		
		 if (!$bf_video_book_linked ) 
				{ 
						// No amazon book
					
					} else {

						if (!$bf_video_book_linked_title) 
						{ 
						// No amazon book title
						
								print('<li class="col-md-3">');
											print('<a href="'.trim($bf_video_book_linked).'" class="post-thumbnail-promotion" target="_blank" title="Amazon Book"><img width="'.trim($icon_promotion_amazon[1]).'" height="'.trim($icon_promotion_amazon[2]).'" src="'.trim($icon_promotion_amazon[0]).'" class="attachment-thumbnail size-thumbnail wp-post-image" alt="Amazon Book" loading="lazy"></a>');
								print('</li>');
								echo("\n");
						
						} else { 

							print('<li>');
											print('<a href="'.trim($bf_video_book_linked).'" class="post-thumbnail-promotion" target="_blank" title="'.trim($bf_video_book_linked_title).'"><img width="'.trim($icon_promotion_amazon[1]).'" height="'.trim($icon_promotion_amazon[2]).'" src="'.trim($icon_promotion_amazon[0]).'" class="attachment-thumbnail size-thumbnail wp-post-image" alt="'.trim($bf_video_book_linked_title).'" ');

								print(' loading="lazy"></a>');


								print('<a class="ressource-linked" href="'.trim($bf_video_book_linked).'"  target="_blank" title="'.trim($bf_video_book_linked_title).'">'.trim($bf_video_book_linked_title).'</a>');
								print('</li>');
								echo("\n");
						
						
								
					
						} 
					} 

				if (!$bf_video_repo_github_linked ) 
					{ 
						// No github repo
					
					} else {

						if (!$bf_video_repo_github_linked_title) 
						{ 
						// No github repo title
						
						print('<li class="col-md-3">');
								print('<a href="'.trim($bf_video_repo_github_linked).'" class="post-thumbnail-promotion" target="_blank"'); 
									print(' title="Github Repository">');
									print('<img width="'.trim($icon_promotion_github[1]).'" height="'.trim($icon_promotion_github[2]).'" src="'.trim($icon_promotion_github[0]).'" class="attachment-thumbnail size-thumbnail wp-post-image"');
									print(' alt="Github Repository" '); 
									print(' loading="lazy"></a>');
								print('</li>');
								echo("\n");

						} else { 

							print('<li>');
								print('<a href="'.trim($bf_video_repo_github_linked).'" class="post-thumbnail-promotion" target="_blank"'); 
									
									print(' title="'.trim($bf_video_repo_github_linked_title).' ');
									
									print('"><img width="'.trim($icon_promotion_github[1]).'" height="'.trim($icon_promotion_github[2]).'" src="'.trim($icon_promotion_github[0]).'" class="attachment-thumbnail size-thumbnail wp-post-image"');


									print(' alt="'.trim($bf_video_repo_github_linked_title).'" '); 

									print(' loading="lazy"></a>');

									print('<a class="ressource-linked" href="'.trim($bf_video_repo_github_linked).'"  target="_blank" title="'.trim($bf_video_repo_github_linked_title).'">'.trim($bf_video_repo_github_linked_title).'</a>');


								print('</li>');
								echo("\n");

						}

						

					} 
					
				if (!$bf_video_yt_channel_linked ) 
					{ 
						// No youtube channel
						
					} else {


						if (!$bf_video_yt_channel_linked_title) 

						{ 
							// No youtube channel title
							print('<li class="col-md-3">');
									print('<a href="'.trim($bf_video_yt_channel_linked).'" class="post-thumbnail-promotion" target="_blank" title="Youtube Video"><img width="'.trim($icon_promotion_youtube[1]).'" height="'.trim($icon_promotion_youtube[2]).'" src="'.trim($icon_promotion_youtube[0]).'" class="attachment-thumbnail size-thumbnail wp-post-image" alt="Youtube Video" loading="lazy"></a>');
								print('</li>');
								echo("\n");
						
								
						
						} else { 

							print('<li>');
											print('<a href="'.trim($bf_video_yt_channel_linked).'" class="post-thumbnail-promotion" target="_blank" title="'.trim($bf_video_yt_channel_linked_title).'"><img width="'.trim($icon_promotion_youtube[1]).'" height="'.trim($icon_promotion_youtube[2]).'" src="'.trim($icon_promotion_youtube[0]).'" class="attachment-thumbnail size-thumbnail wp-post-image" alt="'.trim($bf_video_yt_channel_linked_title).'" ');

								print(' loading="lazy"></a>');


								print('<a class="ressource-linked" href="'.trim($bf_video_yt_channel_linked).'"  target="_blank" title="'.trim($bf_video_yt_channel_linked_title).'">'.trim($bf_video_yt_channel_linked_title).'</a>');
								print('</li>');
								echo("\n");
						
						
								
					
						} 

					} 





		if ( ($bf_video_book_linked) || ($bf_video_repo_github_linked) || ($bf_video_yt_channel_linked) ) { 

				print ('</ul>');
				print ('</div>');

		}
			

	

		/* // MORE RESSOURCES*/ 
		?>

	<?php 
             // Print the taxonomies
			
			$bf_video_tag = get_the_term_list($post->ID, 'bf_videos_manager_tag', 'Tag(s) : ', ', ', '' );
			$bf_video_cat = get_the_term_list($post->ID, 'bf_videos_manager_cat', 'Categorie(s) : ', ', ', '' );


			print('<p>');
			if ( !empty( $bf_video_tag)) {
			echo (''.$bf_video_tag.'');
			echo ('<br>');
			}
			if ( !empty( $bf_video_cat)) {
			echo (''.$bf_video_cat.'');
			echo ('<br>');
			}
			print('</p>');

              					  


    ?>
				<?php
					wp_link_pages( array(
						'before'      => '<div class="page-links"><span class="page-links-title">' . esc_html__( 'Pages:', 'zaatar' ) . '</span>',
						'after'       => '</div>',
						'link_before' => '<span>',
						'link_after'  => '</span>',
					) );
				?>


			</div><!-- .entry-content -->

			<footer class="entry-meta entry-meta-footer">
				<?php allium_entry_footer(); ?>
			</footer><!-- .entry-meta -->

		</div><!-- .post-content-wrapper -->
	</article><!-- #post-## -->
</div><!-- .post-wrapper-hentry -->
