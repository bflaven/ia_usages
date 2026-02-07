/*
   On document ready jQuery will fire set of functions.
   If you want to override function behavior then copy it to your theme js file
   with the same name.
*/
jQuery(document).ready(function($) {
	vc_twitterBehaviour();
	vc_toggleBehaviour();
	vc_tabsBehaviour();
	vc_accordionBehaviour();
	vc_teaserGrid();
	vc_carouselBehaviour();
	vc_slidersBehaviour();
	vc_prettyPhoto();
	vc_googleplus();
	vc_pinterest();
	
}); // END jQuery(document).ready

/* Twitter 
---------------------------------------------------------- */
if ( typeof window['vc_twitterBehaviour'] !== 'function' ) {
	function vc_twitterBehaviour() {
		jQuery('.wpb_twitter_widget .tweets').each(function(index) {
			var this_element = jQuery(this),
				tw_name = this_element.attr('data-tw_name');
				tw_count = this_element.attr('data-tw_count');
			
			this_element.tweet({
				username: tw_name,
				join_text: "auto",
				avatar_size: 0,
				count: tw_count,
				template: "{avatar}{join}{text}{time}",
				auto_join_text_default: "",
				auto_join_text_ed: "",
				auto_join_text_ing: "",
				auto_join_text_reply: "",
				auto_join_text_url: "",
				loading_text: '<span class="loading_tweets">loading tweets...</span>'
	        });
		});
	}
}

/* Google plus
---------------------------------------------------------- */
if ( typeof window['vc_googleplus'] !== 'function' ) {
	function vc_googleplus() {
		if ( jQuery('.wpb_googleplus').length > 0 ) {
			(function() {
				var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
				po.src = 'https://apis.google.com/js/plusone.js';
				var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
			})();
		}
	}
}

if ( typeof window['vc_pinterest'] !== 'function' ) {
	function vc_pinterest() {
		if ( jQuery('.wpb_pinterest').length > 0 ) {
			(function() {
				var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
				po.src = 'http://assets.pinterest.com/js/pinit.js';
				var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
				//<script type="text/javascript" src="//assets.pinterest.com/js/pinit.js"></script>
			})();
		}
	}
}

/* Toggle
---------------------------------------------------------- */
if ( typeof window['vc_toggleBehaviour'] !== 'function' ) {
	function vc_toggleBehaviour() {
		jQuery(".wpb_toggle").click(function(e) {
			if ( jQuery(this).hasClass('wpb_toggle_title_active') ) {
				jQuery(this).removeClass('wpb_toggle_title_active').next().slideUp(500);
			} else {
				jQuery(this).addClass('wpb_toggle_title_active').next().slideDown(500);
			}
		});
		jQuery('.wpb_toggle_content').each(function(index) {
			if ( jQuery(this).next().is('h4.wpb_toggle') == false ) {
				jQuery('<div class="last_toggle_el_margin"></div>').insertAfter(this);
			}
		});
	}
}

/* Tabs + Tours
---------------------------------------------------------- */
if ( typeof window['vc_tabsBehaviour'] !== 'function' ) {
	function vc_tabsBehaviour() {
		jQuery('.wpb_tabs, .wpb_tour').each(function(index) {
			var $tabs,
				tabs_array = [];
			//
			$tabs = jQuery(this).find('.wpb_tour_tabs_wrapper').tabs();
			
			jQuery(this).find('.wpb_tab').each(function(){ tabs_array.push(this.id); });
			jQuery(this).find('.wpb_tab a[href^="#"]').click(function(e) {
				e.preventDefault();
				if ( jQuery.inArray( jQuery(this).attr('href'), tabs_array) ) {
					$tabs.tabs("select", jQuery(this).attr('href'));
					return false;
				}
			});
			
			jQuery(this).find('.wpb_prev_slide a, .wpb_next_slide a').click(function(e) {
				e.preventDefault();
				var index = $tabs.tabs('option', 'selected');
				
				if ( jQuery(this).parent().hasClass('wpb_next_slide') ) { 		index++; }
				else 													{	 	index--; }
				
				if ( index < 0 ) { 									index = $tabs.tabs("length") - 1; }
				else if ( index >= $tabs.tabs("length") ) {			index = 0; }
				
				$tabs.tabs("select", index);
			});
		});
	}
}

/* Tabs + Tours
---------------------------------------------------------- */
if ( typeof window['vc_accordionBehaviour'] !== 'function' ) {
	function vc_accordionBehaviour() {
		jQuery('.wpb_accordion').each(function(index) {
			var $tabs;
			//
			$tabs = jQuery(this).find('.wpb_accordion_wrapper').accordion({
				header: "> div > h3",
				autoHeight: false
			})
		});
	}
}

/* Teaser grid: isotope
---------------------------------------------------------- */
if ( typeof window['vc_teaserGrid'] !== 'function' ) {
	function vc_teaserGrid() {
		var isotope = jQuery('.wpb_grid ul.thumbnails');
		if ( isotope.length > 0 ) {
			isotope.isotope({
				// options
				itemSelector : '.isotope-item',
				layoutMode : 'fitRows'
			});
			jQuery(window).load(function() {
				isotope.isotope("layout");
			});
		}
	}
}

if ( typeof window['vc_carouselBehaviour'] !== 'function' ) {
	function vc_carouselBehaviour() {
		jQuery(".wpb_carousel").each(function() {
			var carousel_width = jQuery(this).width(),
				visible_count = getColumnsCount(jQuery(this)),
				carousel_speed = 500
			if ( jQuery(this).hasClass('columns_count_1') ) {
				carousel_speed = 900;
			}
			jQuery(this).find('.wpb_wrapper:eq(0)').jCarouselLite({
		        btnNext: jQuery(this).find('.next'),
		        btnPrev: jQuery(this).find('.prev'),
		        visible: visible_count,
		        speed: carousel_speed
		    })
		    .width('100%');//carousel_width
		    
		    /*var ul = jQuery(this).find('ul.wpb_thumbnails-fluid'),
			    li = ul.find('li');
		    
		    var ll = li.width()/ul.width()*100,
			    pp = parseInt(li.css("margin-right"), 10)/ul.width()*100;
		    
		    li.width(ll+"%").css({"margin-right" : pp+"%"});
		    
		    var ww = ul.width()/jQuery(this).width()*100;
		    ul.width(ww+"%");
		    
		    var ul_left = parseInt(ul.css("left"), 10),
		    	ul_k = ul_left/ul.width();
		    //
		    jQuery(window).resize(function() {
		    	ul_left = ul.width()*ul_k;
		    	ul.css({ "left" : 0 });
		    });*/
		    jQuery(window).resize(function() {
		    	var before_resize = screen_size;
		    	screen_size = getSizeName();
		    	if ( before_resize != screen_size ) {
		    		window.setTimeout('location.reload()', 20);
		    	}
		    });
		});
	}
}

if ( typeof window['vc_slidersBehaviour'] !== 'function' ) {
	function vc_slidersBehaviour() {
		//var sliders_count = 0;
		jQuery('.wpb_gallery .wpb_gallery_slides').each(function(index) {
			var this_element = jQuery(this);
			var ss_count = 0;
			
			/*if ( this_element.hasClass('wpb_slider_fading') ) {
				var sliderSpeed = 500, sliderTimeout = this_element.attr('data-interval')*1000, slider_fx = 'fade';
				var current_ss;
				
				function slideshowOnBefore(currSlideElement, nextSlideElement, options) {
					jQuery(nextSlideElement).css({"position" : "absolute" });
					jQuery(nextSlideElement).find("div.description").animate({"opacity": 0}, 0);
				}
				
				function slideshowOnAfter(currSlideElement, nextSlideElement, options) {
					jQuery(nextSlideElement).find("div.description").animate({"opacity": 1}, 2000);
					
					jQuery(nextSlideElement).css({"position" : "static" });
					var new_h = jQuery(nextSlideElement).find('img').height();
					if ( jQuery.isNumeric(new_h) ) {
						//this_element.animate({ "height" : new_h }, sliderSpeed );
					}
				}
				
				this_element.find('ul')
				.before('<div class="ss_nav ss_nav_'+ss_count+'"></div><div class="wpb_fading_nav"><a id="next_'+ss_count+'" href="#next"></a> <a id="prev_'+ss_count+'" href="#prev"></a></div>')
				.cycle({
					fx: slider_fx, // choose your transition type, ex: fade, scrollUp, shuffle, etc...
					pause: 1,
					speed: sliderSpeed,
					timeout: sliderTimeout,
					delay: -ss_count * 1000,
					before: slideshowOnBefore,
					after:slideshowOnAfter,
					pager:  '.ss_nav_'+ss_count
				});
				//.find('.description').width(jQuery(this).width() - 20);
				ss_count++;
			}
			else*/
			if ( this_element.hasClass('wpb_slider_nivo') ) {
				var sliderSpeed = 800,
					sliderTimeout = this_element.attr('data-interval')*1000;
				
				if ( sliderTimeout == 0 ) sliderTimeout = 9999999999;
				
				this_element.nivoSlider({
					effect: 'boxRainGrow,boxRain,boxRainReverse,boxRainGrowReverse', // Specify sets like: 'fold,fade,sliceDown'
					slices: 15, // For slice animations
					boxCols: 8, // For box animations
					boxRows: 4, // For box animations
					animSpeed: sliderSpeed, // Slide transition speed
					pauseTime: sliderTimeout, // How long each slide will show
					startSlide: 0, // Set starting Slide (0 index)
					directionNav: true, // Next & Prev navigation
					directionNavHide: true, // Only show on hover
					controlNav: true, // 1,2,3... navigation
					keyboardNav: false, // Use left & right arrows
					pauseOnHover: true, // Stop animation while hovering
					manualAdvance: false, // Force manual transitions
					prevText: 'Prev', // Prev directionNav text
					nextText: 'Next' // Next directionNav text
				});
			}
			else if ( this_element.hasClass('wpb_flexslider') ) {
				var sliderSpeed = 800,
					sliderTimeout = this_element.attr('data-interval')*1000,
					sliderFx = this_element.attr('data-flex_fx'),
					slideshow = true;
				if ( sliderTimeout == 0 ) slideshow = false;
				
				this_element.flexslider({
					animation: sliderFx,
					slideshow: slideshow,
					slideshowSpeed: sliderTimeout,
					sliderSpeed: sliderSpeed
				});
			}
			else if ( this_element.hasClass('wpb_image_grid') ) {
				var isotope = this_element.find('.wpb_image_grid_ul');
				isotope.isotope({
					// options
					itemSelector : '.isotope-item',
					layoutMode : 'fitRows'
				});
				jQuery(window).load(function() {
					isotope.isotope("layout");
				});
			}
		});
	}
}

if ( typeof window['vc_prettyPhoto'] !== 'function' ) {
	function vc_prettyPhoto() {
		try {
			// just in case. maybe prettyphoto isnt loaded on this site
			jQuery('a.prettyphoto').prettyPhoto({
				animationSpeed: 'normal', /* fast/slow/normal */
				padding: 15, /* padding for each side of the picture */
				opacity: 0.7, /* Value betwee 0 and 1 */
				showTitle: true, /* true/false */
				allowresize: true, /* true/false */
				counter_separator_label: '/', /* The separator for the gallery counter 1 "of" 2 */
				//theme: 'light_square', /* light_rounded / dark_rounded / light_square / dark_square */
				hideflash: false, /* Hides all the flash object on a page, set to TRUE if flash appears over prettyPhoto */
				modal: false, /* If set to true, only the close button will close the window */
				callback: function() {
					var url = location.href;
					var hashtag = (url.indexOf('#!prettyPhoto')) ? true : false;
					if (hashtag) location.hash = "!";
				} /* Called when prettyPhoto is closed */,
				social_tools : ''
			});
		} catch (err) { }
	}
}

/* Helper
---------------------------------------------------------- */
function getColumnsCount(el) {
	var find = false,
		i = 1;
		
	while ( find == false ) {
		if ( el.hasClass('columns_count_'+i) ) {
			find = true;
			return i;
		}
		i++;
	}
}

var screen_size = getSizeName();
function getSizeName() {
	var screen_size = '',
		screen_w = jQuery(window).width();
	if ( screen_w > 959 ) {
		screen_size = "big";
	}
	else if ( screen_w > 768 && screen_w < 959 ) {
		screen_size = "tablet";
	}
	else if ( screen_w > 300 && screen_w < 767 ) {
		screen_size = "mobile";
	}
	return screen_size;
}