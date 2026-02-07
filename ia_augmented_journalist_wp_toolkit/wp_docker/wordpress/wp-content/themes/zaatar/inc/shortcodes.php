<?php
	

	/* ==================================================
	
	Supreme Shortcodes
	
	================================================== */
	


	/* BOX SHORTCODE
	================================================= */

	    



/*
	function zaatarymelanzane_create_shortcode_books($atts, $content = null){
   		extract(shortcode_atts(array(
      		'posts' => 1,
   		), $atts));

   		query_posts(array(
   			'post_type' => 'books',
   			'publish_status' => 'published'
   		));
	
		   	$return_string = '<code>';		   	
		   	$return_string .= ''. do_shortcode($content) .'';		
   			$return_string .= '</code>';
   			return $return_string;
	}

	add_shortcode( 'box', 'zaatarymelanzane_create_shortcode_books' ); 
	
*/

	function zaatarymelanzane_create_shortcode_books($atts, $content = null){
   		
		$title = $pb_margin_bottom = $el_class = $width = $el_position = '';

   		extract(shortcode_atts(array(
   			'post_type' => 'books',
        	'title' => '',
        	'pb_margin_bottom'	=> '',
            'el_class' => '',
            'el_position' => '',
            'width' => '1'
        ), $atts));

        $output = '';

   		
	/*
		   	$output = '<code>'.$title.' '.$type.' '.$pb_margin_bottom.' '.$width.' '.$el_position.'';		   	
		   	$output .= ''. do_shortcode($content) .'';		
   			$output .= '</code>';
	*/


        $output .= "\n\t".'<div class="wpb_codesnippet_element '.$width.$el_class.'">';
        $output .= "\n\t\t".'<div class="wpb_wrapper">';
        $output .= ($title != '' ) ? "\n\t\t\t".'<div class="heading-wrap"><h3 class="wpb_heading wpb_codesnippet_heading"><span>'.$title.'</span></h3></div>' : '';
        $output .= "\n\t\t\t".'<code>'. do_shortcode($content) .'</code>';
        $output .= "\n\t\t".'</div>';
        $output .= "\n\t".'</div>';


   			return $output;
	}

	add_shortcode( 'box', 'zaatarymelanzane_create_shortcode_books' ); 

	


	/*
	title="Goethe" 
	type="whitestroke" 
	pb_margin_bottom="yes" 
	width="1/1" 
	el_position="first"

	 */
	/* TYPOGRAPHY SHORTCODES
	================================================= */

	// Highlight Text
	function highlighted($atts, $content = null) {
	   return '<span class="highlighted">'. do_shortcode($content) .'</span>';
	}
	add_shortcode("highlight", "highlighted");
	
	// Decorative Ampersand
	function decorative_ampersand($atts, $content = null) {
	   return '<span class="decorative-ampersand">&</span>';
	}
	add_shortcode("decorative_ampersand", "decorative_ampersand");

	// Dropcap type 1
	function dropcap1($atts, $content = null) {
		return '<span class="dropcap1">'. do_shortcode($content) .'</span>';
	}
	add_shortcode("dropcap1", "dropcap1");
	
	// Dropcap type 2
	function dropcap2($atts, $content = null) {
		return '<span class="dropcap2">'. do_shortcode($content) .'</span>';
	}
	add_shortcode("dropcap2", "dropcap2");
	
	// Dropcap type 3
	function dropcap3($atts, $content = null) {
		return '<span class="dropcap3">'. do_shortcode($content) .'</span>';
	}
	add_shortcode("dropcap3", "dropcap3");
	
	// Dropcap type 4
	function dropcap4($atts, $content = null) {
		return '<span class="dropcap4">'. do_shortcode($content) .'</span>';
	}
	add_shortcode("dropcap4", "dropcap4");
	
	// Blockquote type 1
	function blockquote1($atts, $content = null) {
		return '<blockquote class="blockquote1">'. do_shortcode($content) .'</blockquote>';
	}
	add_shortcode("blockquote1", "blockquote1");

	// Blockquote type 2
	function blockquote2($atts, $content = null) {
		return '<blockquote class="blockquote2">'. do_shortcode($content) .'</blockquote>';
	}
	add_shortcode("blockquote2", "blockquote2");
	
	// Blockquote type 3
	function blockquote3($atts, $content = null) {
		return '<blockquote class="blockquote3">'. do_shortcode($content) .'</blockquote>';
	}
	add_shortcode("blockquote3", "blockquote3");
	
	// Blockquote type 4
	function pullquote($atts, $content = null) {
		return '<blockquote class="pullquote">'. do_shortcode($content) .'</blockquote>';
	}
	add_shortcode("pullquote", "pullquote");


		/* LISTS SHORTCODES
	================================================= */
	
	function sf_list( $atts, $content = null ) {
		extract(shortcode_atts(array(
			"type" => ''
		), $atts));

		$output = '<ul class="sf-list list-'.$type.'">' . do_shortcode($content) .'</ul>';		
		return $output;		
	}
	add_shortcode('list', 'sf_list');
	
	function sf_list_item( $atts, $content = null ) {
		$output = '<li>' . do_shortcode($content) .'</li>';		
		return $output;		
	}
	add_shortcode('list_item', 'sf_list_item');
		

	/* DIVIDER SHORTCODE
	================================================= */

	function horizontal_break($atts, $content = null) {
	   return '<div class="horizontal-break"> </div>';
	}
	add_shortcode("hr", "horizontal_break");


	/* MAP SHORTCODE
	================================================= */

	function fn_googleMaps($atts, $content = null) {
	   extract(shortcode_atts(array(
	      "width" => '940',
	      "height" => '400',
	      "src" => ''
	   ), $atts));
	   return '<div class="map"><iframe width="'.$width.'" height="'.$height.'" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="'.$src.'&amp;output=embed&iwloc=near"></iframe></div>';
	}
	add_shortcode("map", "fn_googleMaps");


	/* SOCIAL SHORTCODE
	================================================= */

	function social_icons($atts, $content = null) {
		extract(shortcode_atts(array(
		   "type" => '',
		   "size" => 'standard',
		   "style" => 'colour'
		), $atts));
		
		$options = get_option('sf_supreme_options');

		$twitter = $options['twitter_username'];
		$facebook = $options['facebook_page_url'];
		$dribbble = $options['dribbble_username'];
		$vimeo = $options['vimeo_username'];
		$tumblr = $options['tumblr_username'];
		$spotify = $options['spotify_username'];
		$skype = $options['skype_username'];
		$linkedin = $options['linkedin_page_url'];
		$lastfm = $options['lastfm_username'];
		$googleplus = $options['googleplus_page_url'];
		$flickr = $options['flickr_page_url'];
		$youtube = $options['youtube_username'];
		$behance = $options['behance_username'];
		$pinterest = $options['pinterest_username'];
		$instagram = $options['instagram_username'];
		$yelp = $options['yelp_url'];
		
		$social_icons = '';
		
		if ($type == '') {
		
			if ($twitter) {
				$social_icons .= '<li class="twitter"><a href="http://www.twitter.com/'.$twitter.'" target="_blank">Twitter</a></li>';
			}
			if ($facebook) {
				$social_icons .= '<li class="facebook"><a href="'.$facebook.'" target="_blank">Facebook</a></li>';
			}
			if ($dribbble) {
				$social_icons .= '<li class="dribbble"><a href="http://www.dribbble.com/'.$dribbble.'" target="_blank">Dribbble</a></li>';
			}
			if ($vimeo) {
				$social_icons .= '<li class="vimeo"><a href="http://www.vimeo.com/'.$vimeo.'" target="_blank">Vimeo</a></li>';
			}
			if ($tumblr) {
				$social_icons .= '<li class="tumblr"><a href="http://'.$tumblr.'.tumblr.com/" target="_blank">Tumblr</a></li>';
			}
			if ($spotify) {
				$social_icons .= '<li class="spotify"><a href="http://open.spotify.com/user/'.$spotify.'" target="_blank">Spotify</a></li>';
			}
			if ($skype) {
				$social_icons .= '<li class="skype"><a href="skype:'.$skype.'" target="_blank">Skype</a></li>';
			}
			if ($linkedin) {
				$social_icons .= '<li class="linkedin"><a href="'.$linkedin.'" target="_blank">LinkedIn</a></li>';
			}
			if ($lastfm) {
				$social_icons .= '<li class="lastfm"><a href="http://www.last.fm/user/'.$lastfm.'" target="_blank">Last.fm</a></li>';
			}
			if ($googleplus) {
				$social_icons .= '<li class="googleplus"><a href="'.$googleplus.'" target="_blank">Google+</a></li>';
			}
			if ($flickr) {
				$social_icons .= '<li class="flickr"><a href="'.$flickr.'" target="_blank">Flickr</a></li>';
			}
			if ($youtube) {
				//V0
				// $social_icons .= '<li class="youtube"><a href="http://www.youtube.com/user/'.$youtube.'" target="_blank">YouTube</a></li>';
				//V1
				$social_icons .= '<li class="youtube"><a href="'.$youtube.'" target="_blank">YouTube</a></li>';
				
			}
			if ($behance) {
				$social_icons .= '<li class="behance"><a href="http://www.behance.net/'.$behance.'" target="_blank">Behance</a></li>';
			}
			if ($pinterest) {
				$social_icons .= '<li class="pinterest"><a href="http://www.pinterest.com/'.$pinterest.'/" target="_blank">Pinterest</a></li>';
			}
			if ($instagram) {
				$social_icons .= '<li class="instagram"><a href="http://instagram.com/'.$instagram.'" target="_blank">Instagram</a></li>';
			}
			if ($yelp) {
				$social_icons .= '<li class="yelp"><a href="'.$yelp.'/" target="_blank">Yelp</a></li>';
			}
		
		} else {
		
			$social_type = explode(',', $type);
			foreach ($social_type as $id) {
				if ($id == "twitter") {
					$social_icons .= '<li class="twitter"><a href="http://www.twitter.com/'.$twitter.'" target="_blank">Twitter</a></li>';
				}
				if ($id == "facebook") {
					$social_icons .= '<li class="facebook"><a href="'.$facebook.'" target="_blank">Facebook</a></li>';
				}
				if ($id == "dribbble") {
					$social_icons .= '<li class="dribbble"><a href="http://www.dribbble.com/'.$dribbble.'" target="_blank">Dribbble</a></li>';
				}
				if ($id == "vimeo") {
					$social_icons .= '<li class="vimeo"><a href="http://www.vimeo.com/'.$vimeo.'" target="_blank">Vimeo</a></li>';
				}
				if ($id == "tumblr") {
					$social_icons .= '<li class="tumblr"><a href="http://'.$tumblr.'.tumblr.com/" target="_blank">Tumblr</a></li>';
				}
				if ($id == "spotify") {
					$social_icons .= '<li class="spotify"><a href="http://open.spotify.com/user/'.$spotify.'" target="_blank">Spotify</a></li>';
				}
				if ($id == "skype") {
					$social_icons .= '<li class="skype"><a href="skype:'.$skype.'" target="_blank">Skype</a></li>';
				}
				if ($id == "linkedin") {
					$social_icons .= '<li class="linkedin"><a href="'.$linkedin.'" target="_blank">LinkedIn</a></li>';
				}
				if ($id == "lastfm") {
					$social_icons .= '<li class="lastfm"><a href="http://www.last.fm/user/'.$lastfm.'" target="_blank">Last.fm</a></li>';
				}
				if ($id == "googleplus") {
					$social_icons .= '<li class="googleplus"><a href="'.$googleplus.'" target="_blank">Google+</a></li>';
				}
				if ($id == "flickr") {
					$social_icons .= '<li class="flickr"><a href="'.$flickr.'" target="_blank">Flickr</a></li>';
				}
				if ($id == "youtube") {
					//V0
					// $social_icons .= '<li class="youtube"><a href="http://www.youtube.com/user/'.$youtube.'" target="_blank">YouTube</a></li>';
					 
					//V1
					$social_icons .= '<li class="youtube"><a href="'.$youtube.'" target="_blank">YouTube</a></li>';



				}
				if ($id == "behance") {
					$social_icons .= '<li class="behance"><a href="http://www.behance.net/'.$behance.'" target="_blank">Behance</a></li>';
				}
				if ($id == "pinterest") {
					$social_icons .= '<li class="pinterest"><a href="http://www.pinterest.com/'.$pinterest.'/" target="_blank">Pinterest</a></li>';
				}
				if ($id == "instagram") {
					$social_icons .= '<li class="instagram"><a href="http://instagram.com/'.$instagram.'" target="_blank">Instagram</a></li>';
				}
				if ($id == "yelp") {
					$social_icons .= '<li class="yelp"><a href="'.$yelp.'" target="_blank">Yelp</a></li>';
				}
			}
		}
		
		return '<ul class="social-icons '.$size.' '.$style.'">'. $social_icons .'</ul>';		
	}
	add_shortcode("social", "social_icons");
	
	
	/* SITEMAP SHORTCODE
	================================================= */
	
	function sf_sitemap($params = array()) {  
	    // default parameters  
	    extract(shortcode_atts(array(  
	        'title' => 'Site map',  
	        'id' => 'sitemap',  
	        'depth' => 2  
	    ), $params));  
	    // create sitemap
	    
	    $sitemap = '<div class="sitemap-wrap clearfix">';
	    
	        $sitemap .= '<div class="sitemap-col">';
	            
	            $sitemap .= '<h6>'.__("Pages", "swiftframework").'</h6>';
	              
	            $page_list = wp_list_pages("title_li=&depth=$depth&sort_column=menu_order&echo=0");  
	            if ($page_list != '') {  
	                $sitemap .= '<ul>'.$page_list.'</ul>';  
	            }
	        
	        $sitemap .= '</div>';
	        
	        $sitemap .= '<div class="sitemap-col">';
	        	
	        	$sitemap .= '<h6>'.__("Posts", "swiftframework").'</h6>';
	        	  
	        	$post_list = wp_get_archives('type=postbypost&limit=20&echo=0');
	        	if ($post_list != '') {  
	        	    $sitemap .= '<ul>'.$post_list.'</ul>';  
	        	}	  	
	        	
	        $sitemap .= '</div>';
	        	
	    	$sitemap .= '<div class="sitemap-col">';
	        	
	        	$sitemap .= '<h6>'.__("Categories", "swiftframework").'</h6>';
	        	  
	        	$category_list = wp_list_categories('sort_column=name&title_li=&depth=1&number=10&echo=0');
	        	if ($category_list != '') {  
	        	    $sitemap .= '<ul>'.$category_list.'</ul>';  
	        	}		
	        	
	        	$sitemap .= '<h6>'.__("Archives", "swiftframework").'</h6>';
	        	  
	        	$archive_list =  wp_get_archives('type=monthly&limit=12&echo=0');
	        	if ($archive_list != '') {  
	        	    $sitemap .= '<ul>'.$archive_list.'</ul>';  
	        	}
	        	
	    	$sitemap .= '</div>';
	    	
	    $sitemap .= '</div>';
	    
	    return $sitemap;  
	    
	}  
	add_shortcode('sf_sitemap', 'sf_sitemap');  
	
	
	/* LATEST TWEET SHORTCODE
	================================================= */

	function latest_tweet($atts) {
		extract(shortcode_atts(array(
			"username" => ''
		), $atts));
		$tweet_content = latestTweet(1, $username);
		return $tweet_content;
	}
	
	add_shortcode('latest-tweet', 'latest_tweet');
	

	/* YEAR SHORTCODE
	================================================= */

	function year_shortcode() {
		$year = date('Y');
		return $year;
	}

	add_shortcode('the-year', 'year_shortcode');


	/* WORDPRESS LINK SHORTCODE
	================================================= */

	function wordpress_link() {
		return '<a href="http://wordpress.org/" target="_blank">WordPress</a>';
	}

	add_shortcode('wp-link', 'wordpress_link');
	
?>