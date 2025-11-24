## PROMPT_1

As a php expert and a wordpress specialist, can you fix the code below, I can not see th ID in the first column within the code of the `functions.php`
- 1. Reindent the code correctly and fix th error
- 2. Generate all the code so I just have to cut and paste. 

- ERROR
```php
/*  ADD specific columns for the posts */
								add_filter( 'manage_edit-post_columns', 'he3_edit_posts_columns' ) ;
								add_action( 'manage_posts_custom_column', 'he3_posts_columns', 10, 2 );
								
								/* For Posts */
								function he3_edit_posts_columns( $columns ) {

									$columns = array(
												'cb' => '<input type="checkbox" />',
												'id' => __( 'ID' ),
												'thumb' => __( 'Thumbnail' ),
												'title' => __( 'Title' ),
												'categories' => __( 'Categories' ),
												'tags' => __( 'Tags' ),
												'comments' => __( '<span class="vers"><img src="'.get_admin_url().'/images/comment-grey-bubble.png" alt="Comments"></span>'),
												'date' => __( 'Date' ),
												'author' => __( 'Auteur' ),
												'views' => __( 'Vue(s)' ),
												'attachments' => __( 'Attachments' ),
									);

									return $columns;
								}//EOF
								
								function he3_posts_columns ( $column, $post_id ) {
									global $post;

									switch( $column ) {
									
										/* thumb */
											case 'thumb' :
												$postid = get_the_ID();
												$thumb = get_the_post_thumbnail($postid, array(125, 80) );
												$url = admin_url( 'media-upload.php?post_id='.$postid.'&amp;type=image&amp;TB_iframe=3&amp;width=640&amp;height=296', 'http' );

/* <a href="http://www.flaven.net/wp-admin/media-upload.php?post_id='.$postid.'&amp;type=image&amp;TB_iframe=1&amp;width=640&amp;height=296" id="set-post-thumbnail" class="thickbox">Select thumbnail</a> */

												if ( empty( $postid ) )
													echo __( 'Unknown' );
												else
													
													// printf( __( '%s' ), $thumb);
													
													$html = '<!-- link + thumb -->';
													$html .= ''.$thumb.'<br>';
													$html .= '<!-- '.$postid.' -->';
													$html .= '<a href="'.$url.'id="set-post-thumbnail" class="thickbox">Select thumbnail</a>';
													$html .= '<!-- // link + thumb -->';
													
													echo $html;
													
												break;
										/* // thumb */
										
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
								
									// 
									
									
									/*  add_filter( 'manage_edit-posts_sortable_columns', 'he3_posts_sortable_columns' );	 
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
									}//EOF
*/
// http://www.tcbarrett.com/2011/09/adding-custom-sortable-columns-to-your-wordpress-custom-post-type/

		/* // -----------  for Posts -----------  */
```














