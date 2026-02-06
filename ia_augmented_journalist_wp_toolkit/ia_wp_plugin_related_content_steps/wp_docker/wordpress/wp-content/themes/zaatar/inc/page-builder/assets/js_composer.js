(function($) {
    $.log = function(text) {
        if(typeof(window['console'])!='undefined') console.log(text);
    };

    $.wpb_composer = {
        isMainContainerEmpty: function() {
            if(!jQuery('.wpb_main_sortable > div').length) {
                $('.metabox-composer-content').addClass('empty-composer');
            } else {
                $('.metabox-composer-content').removeClass('empty-composer');
            }
        },
        cloneSelectedImagesFromMediaTab: function(html, $ids) {
            var $button = $('.wpb_current_active_media_button').removeClass('.wpb_current_active_media_button');

            var attached_img_div = $button.next(),
                site_img_div	 = $button.next().next();

            var hidden_ids = attached_img_div.prev().prev(),
                img_ul = attached_img_div.find('.gallery_widget_attached_images_list');

            img_ul.html(html);

            var hidden_ids_value = '';
            img_ul.find('li').each(function() {
                hidden_ids_value += (hidden_ids_value.length>0 ? ',' : '') + $(this).attr('media_id');
            });

            hidden_ids.val(hidden_ids_value);

            attachedImgSortable(img_ul);

            tb_remove();

        },
        galleryImagesControls: function() {
            $('.gallery_widget_add_images').live("click", function(e) {
                $(this).addClass('wpb_current_active_media_button');
                e.preventDefault();
                var selected_ids = $(this).parent().find('.gallery_widget_attached_images_ids').val();
                tb_show('Add/remove picture', 'media-upload.php?type=image&post_id=' +  $('#post_ID').val() +'&tab=composer_images&single_image=' + ($(this).attr('use-single')=='true' ? 'true' : 'false') + '&selected_ids=' + encodeURIComponent(selected_ids) + '&TB_iframe=true&height=343&width=800');
				
                return false;

                var attached_img_div = $(this).next(),
                    site_img_div	 = $(this).next().next();

                if ( attached_img_div.css('display') == 'block' ) {
                    $(this).addClass('button-primary').text('Finish Adding Images');
                    //
                    attached_img_div.hide();
                    site_img_div.show();

                    hideEditFormSaveButton();
                }
                else {
                    $(this).removeClass('button-primary').text($(this).attr('use-single')=='true' ? 'Add Image' : 'Add images');
                    //
                    attached_img_div.show();        // $this->addAction('admin_head', 'header');.show();
                    site_img_div.hide();

                    cloneSelectedImages(site_img_div, attached_img_div);

                    showEditFormSaveButton();
                }
            });

            $('.gallery_widget_img_select li').live("click", function(e) {
                $(this).toggleClass('added');

                var hidden_ids = $(this).parent().parent().prev().prev().prev(),
                    ids_array = (hidden_ids.val().length > 0) ? hidden_ids.val().split(",") : new Array(),
                    img_rel = $(this).find("img").attr("rel"),
                    id_pos = $.inArray(img_rel, ids_array);

                /* if not found */
                if ( id_pos == -1 ) {
                    ids_array.push(img_rel);
                }
                else {
                    ids_array.splice(id_pos, 1);
                }

                hidden_ids.val(ids_array.join(","));

            });
        },
        initializeFormEditing: function(element) {
            //
            $('#visual_composer_edit_form .wp-editor-wrap .textarea_html').each(function(index) {
                initTinyMce($(this));
            });

            $('#visual_composer_edit_form .gallery_widget_attached_images_list').each(function(index) {
                attachedImgSortable($(this));
            });


            // Get callback function name
            var cb = element.children(".wpb_vc_edit_callback");
            //
            if ( cb.length == 1 ) {
                var fn = window[cb.attr("value")];
                if ( typeof fn === 'function' ) {
                    var tmp_output = fn(element);
                }
            }

            $('.wpb_save_edit_form').unbind('click').click(function(e) {
                e.preventDefault();
                saveFormEditing(element);//(element);

            });

            $('#cancel-background-options').unbind('click').click(function(e){
                e.preventDefault();
                $('.wpb_main_sortable, #wpb_visual_composer-elements, .wpb_switch-to-composer').show();
                $('#visual_composer_edit_form').html('').hide();
                $('.visual_composer_tinymce').each(function () {
                    if (tinyMCE.majorVersion >= 4) {
                    	tinyMCE.execCommand("mceRemoveEditor", true, $(this).attr('id'));
                    } else {
                    	tinyMCE.execCommand("mceRemoveControl", true, $(this).attr('id'));
                    }
                });
                $('body, html').scrollTop(current_scroll_pos);
                $("#publish").show();
            });
        },
        onDragPlaceholder: function() {
            return $('<div id="drag_placeholder"></div>');
        },
        addLastClass: function(dom_tree) {
            var total_width, width, next_width;
            total_width = 0;
            width = 0;
            next_width = 0;
            $dom_tree = $(dom_tree);

            $dom_tree.children(".wpb_sortable").removeClass("wpb_first wpb_last");
            if ($dom_tree.hasClass("wpb_main_sortable")) {
                $dom_tree.find(".wpb_sortable .wpb_sortable").removeClass("sortable_1st_level");
                $dom_tree.children(".wpb_sortable").addClass("sortable_1st_level");
                $dom_tree.children(".wpb_sortable:eq(0)").addClass("wpb_first");
                $dom_tree.children(".wpb_sortable:last").addClass("wpb_last");
            }

            if ($dom_tree.hasClass("wpb_column_container")) {
                $dom_tree.children(".wpb_sortable:eq(0)").addClass("wpb_first");
                $dom_tree.children(".wpb_sortable:last").addClass("wpb_last");
            }

            $dom_tree.children(".wpb_sortable").each(function (index) {

                var cur_el = $(this);

                // Width of current element
                if (cur_el.hasClass("span12")
                    || cur_el.hasClass("wpb_widget")) {
                    width = 12;
                }
                else if (cur_el.hasClass("span10")) {
                    width = 10;
                }
                else if (cur_el.hasClass("span9")) {
                    width = 9;
                }
                else if (cur_el.hasClass("span8")) {
                    width = 8;
                }
                else if (cur_el.hasClass("span6")) {
                    width = 6;
                }
                else if (cur_el.hasClass("span4")) {
                    width = 4;
                }
                else if (cur_el.hasClass("span3")) {
                    width = 3;
                }
                else if (cur_el.hasClass("span2")) {
                    width = 2;
                }
                total_width += width;// + next_width;

                //console.log(next_width+" "+total_width);

                if (total_width > 10 && total_width <= 12) {
                    cur_el.addClass("wpb_last");
                    cur_el.next('.wpb_sortable').addClass("wpb_first");
                    total_width = 0;
                }
                if (total_width > 12) {
                    cur_el.addClass('wpb_first');
                    cur_el.prev('.wpb_sortable').addClass("wpb_last");
                    total_width = width;
                }

                if (cur_el.hasClass('wpb_vc_column') || cur_el.hasClass('wpb_vc_tabs') || cur_el.hasClass('wpb_vc_tour') || cur_el.hasClass('wpb_vc_accordion')) {

                    if (cur_el.find('.wpb_element_wrapper .wpb_column_container').length > 0) {
                        cur_el.removeClass('empty_column');
                        cur_el.addClass('not_empty_column');
                        //addLastClass(cur_el.find('.wpb_element_wrapper .wpb_column_container'));
                        cur_el.find('.wpb_element_wrapper .wpb_column_container').each(function (index) {
                            $.wpb_composer.addLastClass($(this)); // Seems it does nothing

                            if($(this).find('div:not(.container-helper)').length==0) {
                                $(this).addClass('empty_column');
                                $(this).html($('#container-helper-block').html());
                            } else {
                                $(this).removeClass('empty_column');
                            }
                        });
                    }
                    else if (cur_el.find('.wpb_element_wrapper .wpb_column_container').length == 0) {
                        cur_el.removeClass('not_empty_column');
                        cur_el.addClass('empty_column');
                    }
                    else {
                        cur_el.removeClass('empty_column not_empty_column');
                    }
                }

                //if ( total_width == 0 ) {
                //	cur_el.next('.wpb_sortable').addClass("wpb_first");
                //}

                //total_width += width;

                /*
                 // If total_width > 0.95 and <= 1 then add 'last' class name to the column
                 if (total_width >= 0.95 && total_width <= 1) {
                 cur_el.addClass("last");
                 cur_el.next('.column').addClass("first");
                 total_width = 0;
                 }
                 // If total_width > 1 then add 'first' class name to the current column and
                 // 'last' to the previous. 'first' class name is needed to clear floats
                 if (total_width > 1) {
                 cur_el.addClass("first");
                 cur_el.prev(".column").addClass("last");
                 total_width = width;
                 }

                 // If current column have column elements inside, then go throw them too
                 //if (cur_el.children(".column").length > 1) {
                 if (cur_el.hasClass('wpb_vc_column')) {
                 if (cur_el.children(".column").length > 0) {
                 cur_el.removeClass('empty_column');
                 cur_el.addClass('not_empty_column');
                 jQuery.wpb_composer.addLastClass(cur_el);
                 }
                 else if (cur_el.children(".column").length == 0) {
                 cur_el.removeClass('not_empty_column');
                 cur_el.addClass('empty_column');
                 }
                 else {
                 cur_el.removeClass('empty_column not_empty_column');
                 }
                 }
                 */
            });
            //$(dom_tree).children(".column:first").addClass("first");
            //$(dom_tree).children(".column:last").addClass("last");
        }, // endjQuery.wpb_composer.addLastClass()
        save_composer_html: function() {
            this.addLastClass($(".wpb_main_sortable"));

            var shortcodes = generateShortcodesFromHtml($(".wpb_main_sortable"));
            //console.log(shortcodes);

            //console.log(tinyMCE.ed.isHidden());

            //if ( tinyMCE.activeEditor == null ) {

            //setActive(wpb_def_wp_editor.editorId);

            if ( isTinyMceActive() != true ) {
                //TODO: WPML and qTranslate
                //tinyMCE.activeEditor.setContent(shortcodes, {format : 'html'});
                $('#content').val(shortcodes);
            } else {
                tinyMCE.activeEditor.setContent(shortcodes, {format : 'html'});
            }



            /*var val = $.trim($(".wpb_main_sortable").html());
             $("#visual_composer_html_code_holder").val(val);

             var shortcodes = generateShortcodesFromHtml($(".wpb_main_sortable"));
             $("#visual_composer_code_holder").val(shortcodes);

             var tiny_val = switchEditors.wpautop(shortcodes);

             //[REVISE] Should determine what mode is currently on Visual/HTML
             tinyMCE.get('content').setContent(tiny_val, {format : 'raw'});

             /*try {
             tinyMCE.get('content').setContent(tiny_val, {format : 'raw'});
             }
             catch (err) {
             switchEditors.go('content', 'html');
             $('#content').val(shortcodes);
             }*/
        }
    }
})(jQuery);

jQuery(document).ready(function($) {
	/* On load initialize sortable and dragable elements
	---------------------------------------------------------- */
    /*
	$('.wpb_main_sortable').sortable({
		forcePlaceholderSize: true,
		placeholder: "widgets-placeholder",
		// cursorAt: { left: 10, top : 20 },
		cursor: "move",
		items: "div.sortable_1st_level",//wpb_sortable
		update: function() {$.wpb_composer.save_composer_html(); }
	});
    */
    $( "#wpb_visual_composer .dropable_el, #wpb_visual_composer .dropable_column" ).draggable({
        helper: function() { return $('<div id="drag_placeholder"></div>').appendTo('body')},
        zIndex: 99999,
        // cursorAt: { left: 10, top : 20 },
        cursor: "move",
        // appendTo: "body",
        revert: "invalid",
        start: function(event, ui) { renderCorrectPlaceholder(event, ui);}
    });
    initDroppable();
    
    
   
	 /* Make menu elements dropable */

	$('.dropdown-toggle').dropdown();
	/*$('.dropdown-toggle').hover(
		function () { $(this).trigger("click"); },
		function () { }
	);
	$('.dropdown-menu').hover(
		function () { }, //$(this).trigger("click"); },
		function () { $(this).parent().find('.dropdown-toggle').trigger("click"); }
	);

	$('#wpb_visual_composer-elements .nav').children('li').find('a').hover( function() { $('.dropdown-menu').hide(); } );
	*/

	/* Add action for menu buttons with 'clickable_action' class name */
	$("#wpb_visual_composer-elements .clickable_action").click(function(e) {
		e.preventDefault();
		getElementMarkup($('.main_wrapper'), $(this), "initDroppable");
	});

	$("#wpb_visual_composer-elements .clickable_layout_action").click(function(e) {
		e.preventDefault();
		getElementMarkup($('.main_wrapper'), $(this), "initDroppable");
	});

	columnControls(); /* Set action for column sizes and delete buttons */


	if ( $("#wpb_visual_composer").length == 1 ) {
		$('div#titlediv').after('<p class="composer-switch"><a class="wpb_switch-to-composer button-primary" href="#">Swift Page Builder</a></p>');

		var postdivrich = $('#postdivrich'),
			visualcomposer = $('#wpb_visual_composer');

		$('.wpb_switch-to-composer').click(function(e){
			e.preventDefault();
			if ( postdivrich.is(":visible") ) {

				if (!isTinyMceActive()) {
                    if(switchEditors!=undefined) switchEditors.switchto($('#content-tmce').get(0));
                }
					postdivrich.hide();
					visualcomposer.show();
					$('#wpb_vc_js_status').val("true");
					$(this).html('Classic editor');

					wpb_shortcodesToVisualEditor();
					wpb_navOnScroll();
				// } else {
				//	alert("Please switch default WordPress editor to 'Visual' mode first.");
				// }
			}
			else {
				postdivrich.show();
				visualcomposer.hide();
				$('#wpb_vc_js_status').val("false");
				$(this).html('Swift Page Builder');
			}
		});

		/* Decide what editor to show on load
		---------------------------------------------------------- */
		if ( $('#wpb_vc_js_status').val() == 'true' && jQuery('#wp-content-wrap').hasClass('tmce-active') ) {
			//if ( isTinyMceActive() == true ) {
				postdivrich.hide();
				visualcomposer.show();
				$('.wpb_switch-to-composer').html('Classic editor');
			//} else {
			//	alert("Please switch default WordPress editor to 'Visual' mode first.");
			//}

			//wpb_shortcodesToVisualEditor();
		} else {
			postdivrich.show();
			visualcomposer.hide();
			$('.wpb_switch-to-composer').html('Swift Page Builder');
		}
	}
	jQuery(window).load(function() {
		if ( $('#wpb_vc_js_status').val() == 'true' && jQuery('#wp-content-wrap').hasClass('tmce-active') ) {
			//wpb_shortcodesToVisualEditor();
			window.setTimeout('wpb_shortcodesToVisualEditor()', 900);
			wpb_navOnScroll();
		}
	});

	/*** Toggle click (FAQ) ***/
	jQuery(".toggle_title").live("click", function(e) {
		if ( jQuery(this).hasClass('toggle_title_active') ) {
			jQuery(this).removeClass('toggle_title_active').next().hide();
		} else {
			jQuery(this).addClass('toggle_title_active').next().show();
		}
	});

	/*** Gallery Controls / Site attached images ***/
    $.wpb_composer.galleryImagesControls(); /* Actions for gallery images handling */
	/*jQuery('.gallery_widget_attached_images_list').each(function(index) {
		attachedImgSortable(jQuery(this));
	});*/

	/*** Template System ***/
	wpb_templateSystem();

    $('#wpb_visual_composer').on('click', '.add-text-block-to-content', function(e) {
        e.preventDefault();
        if($(this).attr('parent-container')) {
        	if ($(this).parent().parent().hasClass('ui-accordion-content') || $(this).parent().parent().hasClass('ui-tabs-panel')) {
        		getElementMarkup($(this).parent().parent(), $('#vc_column_text'));
        	} else if ($(this).parent().parent().parent().hasClass('ui-accordion-content') || $(this).parent().parent().parent().hasClass('ui-tabs-panel')) {
        		getElementMarkup($(this).parent().parent(), $('#vc_column_text'));
        	} else {
           		getElementMarkup($($(this).attr('parent-container')), $('#vc_column_text'));
           	}
        } else {
            getElementMarkup($(this).parent().parent().parent(), $('#vc_column_text'));
        }
    });
    
    function sortElementsDropdown() {
   		
   		var mylist = $('.wpb_content_elements').parent().find('ul');
   		var listitems = mylist.children('li').get();
   		listitems.sort(function(a, b) {
   		   var compA = $(a).text().toUpperCase();
   		   var compB = $(b).text().toUpperCase();
   		   return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
   		})
   		$.each(listitems, function(idx, itm) { mylist.append(itm); });
    	
    } sortElementsDropdown();
    
    
    $('.alt_background').live('change',function(){
        $('.altbg-preview').attr('class', 'altbg-preview');
        $('.altbg-preview').addClass(jQuery(this).val());
    });
    
}); // end jQuery(document).ready

function open_elements_dropdown() {
    jQuery('.wpb_content_elements:first').trigger('click');
}

function open_layouts_dropdown() {
    jQuery('.wpb_popular_layouts:first').trigger('click');
}

/**
 * WPBakery Composer class
 */

function wpb_templateSystem() {
	jQuery('#wpb_save_template').live("click", function(e) {
		e.preventDefault();

		var template_name = prompt("Please enter templates name", '');
		if ( template_name != null && template_name != "" ) {
			var template = generateShortcodesFromHtml(jQuery(".wpb_main_sortable"));
			var data = {
				action: 'wpb_save_template',
				template: template,
				template_name: template_name
			};

			jQuery.post(ajaxurl, data, function(response) {
				jQuery('.wpb_templates_ul').html(response);
			});
		} else {
			alert("Error. Please try again.");
		}
	});
	
	jQuery('.sf_prebuilt_template a').live("click", function(e) {
		e.preventDefault();
		
		var data = {
			action: 'sf_load_template',
			template_id: jQuery(this).attr('data-template_id')
		};

		jQuery.post(ajaxurl, data, function(response) {	
			jQuery('.wpb_main_sortable').append(response).find(".wpb_vc_init_callback").each(function(index) {
				var fn = window[jQuery(this).attr("value")];
				if ( typeof fn === 'function' ) {
				    fn(jQuery(this).closest('.wpb_content_element'));
				}
			});
			//
			initDroppable();
			save_composer_html();
		});
	});

	jQuery('.wpb_template_li a').live("click", function(e) {
		e.preventDefault();
		var data = {
			action: 'wpb_load_template',
			template_id: jQuery(this).attr('data-template_id')
		};

		jQuery.post(ajaxurl, data, function(response) {
			jQuery('.wpb_main_sortable').append(response).find(".wpb_vc_init_callback").each(function(index) {
				var fn = window[jQuery(this).attr("value")];
				if ( typeof fn === 'function' ) {
				    fn(jQuery(this).closest('.wpb_content_element'));
				}
			});
			//
			initDroppable();
			save_composer_html();
		});
	});

	jQuery('.wpb_remove_template').live("click", function(e) {
		e.preventDefault();
		var template_name = jQuery(this).closest('.wpb_template_li').find('a').text();
		var answer = confirm ("Confirm deleting '"+template_name+"' template, press Cancel to leave. This action cannot be undone.");
		if (answer) {
			//alert("delete");
			var data = {
				action: 'wpb_delete_template',
				template_id: jQuery(this).closest('.wpb_template_li').find('a').attr('data-template_id')
			};

			jQuery.post(ajaxurl, data, function(response) {
				jQuery('.wpb_templates_ul').html(response);
			});
		}
	});
}

// fix sub nav on scroll
var $win, $nav,	navTop,	isFixed = 0;
function wpb_navOnScroll() {
	$win = jQuery(window);
	$nav = jQuery('#wpb_visual_composer-elements');
	navTop = jQuery('#wpb_visual_composer-elements').length && jQuery('#wpb_visual_composer-elements').offset().top - 28;
	isFixed = 0;

	wpb_processScroll();
	$win.on('scroll', wpb_processScroll);
}
function wpb_processScroll() {
	var i,
		scrollTop = $win.scrollTop();

	if ( scrollTop >= navTop && !isFixed ) {
		isFixed = 1;
		$nav.addClass('subnav-fixed')
	} else if (scrollTop <= navTop && isFixed) {
		isFixed = 0;
		$nav.removeClass('subnav-fixed');
	}
}





function hideEditFormSaveButton() {
	jQuery('#visual_composer_edit_form .edit_form_actions').hide();
}
function showEditFormSaveButton() {
	jQuery('#visual_composer_edit_form .edit_form_actions').show();
}

/* Updates ids order in hidden input field, on drag-n-drop reorder */
function updateSelectedImagesOrderIds(img_ul) {
	var img_ids = new Array();

	jQuery(img_ul).find('.added img').each(function() {
		img_ids.push(jQuery(this).attr("rel"));
	});

	jQuery(img_ul).parent().prev().prev().val(img_ids.join(','));
}

/* Takes ids from hidden field and clone li's */
function cloneSelectedImages(site_img_div, attached_img_div) {
	var hidden_ids = jQuery(attached_img_div).prev().prev(),
		ids_array = (hidden_ids.val().length > 0) ? hidden_ids.val().split(",") : new Array(),
		img_ul = attached_img_div.find('.gallery_widget_attached_images_list');

	img_ul.html('');

	jQuery.each(ids_array, function(index, value) {
		jQuery(site_img_div).find('img[rel='+value+']').parent().clone().appendTo(img_ul);
	});
	attachedImgSortable(img_ul);
}

function attachedImgSortable(img_ul) {
	jQuery(img_ul).sortable({
		forcePlaceholderSize: true,
		placeholder: "widgets-placeholder",
		cursor: "move",
		items: "li",
		update: function() { updateSelectedImagesOrderIds(img_ul); }
	});
}



/* Get content from tinyMCE editor and convert it to Visual
   Composer
---------------------------------------------------------- */
function wpb_shortcodesToVisualEditor() {
	var content = wpb_getContentFromTinyMCE();

	jQuery('.wpb_main_sortable').html(jQuery('#wpb_vc_loading').val());
		
	var data = {
		action: 'wpb_shortcodes_to_visualComposer',
		content: content
	};

	jQuery.post(ajaxurl, data, function(response) {
		jQuery('.wpb_main_sortable').html(response);
        jQuery.wpb_composer.isMainContainerEmpty();
		//
		//console.log(response);
		jQuery.wpb_composer.addLastClass(jQuery(".wpb_main_sortable"));
		initDroppable();

		//Fire INIT callback if it is defined
		jQuery('.wpb_main_sortable').find(".wpb_vc_init_callback").each(function(index) {
			var fn = window[jQuery(this).attr("value")];
			if ( typeof fn === 'function' ) {
			    fn(jQuery(this).closest('.wpb_sortable'));
			}
		});
	});
}

/* get content from tinyMCE editor
---------------------------------------------------------- */
function wpb_getContentFromTinyMCE() {
	var content = '';

	//if ( tinyMCE.activeEditor ) {
	if ( isTinyMceActive() ) {
		var wpb_ed = tinyMCE.activeEditor; // get editor instance
        content = wpb_ed.save();
        if ( content == undefined ) {
            content = jQuery('#content').val();
        }
	} else {
		content = jQuery('#content').val();
	}
	return content;
}


/* This makes layout elements droppable, so user can drag
   them from on column to another and sort them (re-order)
   within the current column
---------------------------------------------------------- */
function initDroppable() {
    jQuery('.wpb_sortable_container').sortable({
        forcePlaceholderSize: true,
        connectWith: ".wpb_sortable_container",
        placeholder: "widgets-placeholder",
        // cursorAt: { left: 10, top : 20 },
        cursor: "move",
        items: "div.wpb_sortable",//wpb_sortablee
        distance: 0.5,
        start: function() {
            jQuery('#visual_composer_content').addClass('sorting-started');
        },
        stop: function(event, ui) {
            jQuery('#visual_composer_content').removeClass('sorting-started');
        },
        update: function() {jQuery.wpb_composer.save_composer_html(); },
        over: function(event, ui) {
            ui.placeholder.css({maxWidth: ui.placeholder.parent().width()});
            ui.placeholder.removeClass('hidden-placeholder');
            if( ui.item.hasClass('not-column-inherit') && ui.placeholder.parent().hasClass('not-column-inherit')) {
                ui.placeholder.addClass('hidden-placeholder');
            }

        },
        beforeStop: function(event, ui) {
            if( ui.item.hasClass('not-column-inherit') && ui.placeholder.parent().hasClass('not-column-inherit')) {
                return false;
            }
        }
    });


/*
    jQuery('.wpb_column_container').sortable({
        connectWith: ".wpb_column_container, .wpb_main_sortable",
        //connectWith: ".sortable_1st_level.wpb_vc_column",
        forcePlaceholderSize: true,
        placeholder: "widgets-placeholder",
        // cursorAt: { left: 10, top : 20 },
        cursor: "move",
        items: "div.wpb_sortable:not(.wpb_vc_column)",
        update: function() { jQuery.wpb_composer.save_composer_html(); },
    });
*/
    jQuery('.wpb_main_sortable').droppable({
        greedy: true,
        accept: ".dropable_el, .dropable_column",
        hoverClass: "wpb_ui-state-active",
        drop: function( event, ui ) {
            //console.log(jQuery(this));
            getElementMarkup(jQuery(this), ui.draggable, "addLastClass");
        }
    });

    jQuery('.wpb_column_container').droppable({
        greedy: true,
        accept: function(dropable_el) {
            if ( dropable_el.hasClass('dropable_el') && jQuery(this).hasClass('ui-droppable') && dropable_el.hasClass('not_dropable_in_third_level_nav') ) {
                return false;
            } else if ( dropable_el.hasClass('dropable_el') == true ) {
                return true;
            }

            //".dropable_el",
        },
        hoverClass: "wpb_ui-state-active",
        over: function( event, ui ) {
            jQuery(this).parent().addClass("wpb_ui-state-active");
        },
        out: function( event, ui ) {
            jQuery(this).parent().removeClass("wpb_ui-state-active");
        },
        drop: function( event, ui ) {
            //console.log(jQuery(this));
            jQuery(this).parent().removeClass("wpb_ui-state-active");
            getElementMarkup(jQuery(this), ui.draggable, "addLastClass");
        }
    });



}




function initDroppable2() {

    jQuery('.wpb_main_sortable').sortable({
        forcePlaceholderSize: true,
        connectWith: ".wpb_column_container",
        placeholder: "widgets-placeholder",
        // cursorAt: { left: 10, top : 20 },
        cursor: "move",
        items: "div.sortable_1st_level",//wpb_sortable
        update: function() {jQuery.wpb_composer.save_composer_html(); }
    });

	jQuery('.wpb_column_container').sortable({
		connectWith: ".wpb_column_container, .wpb_main_sortable",
		//connectWith: ".sortable_1st_level.wpb_vc_column",
		forcePlaceholderSize: false,
		placeholder: "widgets-placeholder",
		// cursorAt: { left: 10, top : 20 },
		cursor: "move",
		items: "div.wpb_sortable:not(.wpb_vc_column)",
		update: function() { jQuery.wpb_composer.save_composer_html(); }
	});

	jQuery('.wpb_main_sortable').droppable({
		greedy: true,
		accept: ".dropable_el, .dropable_column",
		hoverClass: "wpb_ui-state-active",
		drop: function( event, ui ) {
			//console.log(jQuery(this));
			getElementMarkup(jQuery(this), ui.draggable, "addLastClass");
		}
	});
	jQuery('.wpb_column_container').droppable({
		greedy: true,
		accept: function(dropable_el) {
			if ( dropable_el.hasClass('dropable_el') && jQuery(this).hasClass('ui-droppable') && dropable_el.hasClass('not_dropable_in_third_level_nav') ) {
				return false;
			} else if ( dropable_el.hasClass('dropable_el') == true ) {
				return true;
			}

			//".dropable_el",
		},
		hoverClass: "wpb_ui-state-active",
		over: function( event, ui ) {
			jQuery(this).parent().addClass("wpb_ui-state-active");
		},
		out: function( event, ui ) {
			jQuery(this).parent().removeClass("wpb_ui-state-active");
		},
		drop: function( event, ui ) {
			//console.log(jQuery(this));
			jQuery(this).parent().removeClass("wpb_ui-state-active");
			getElementMarkup(jQuery(this), ui.draggable, "addLastClass");
		}
	});



} // end initDroppable()


/* Get initial html markup for content element. This function
   use AJAX to run do_shortcode and then place output code into
   main content holder
---------------------------------------------------------- */
function getElementMarkup (target, element, action) {

	var data = {
		action: 'wpb_get_element_backend_html',
		//column_index: jQuery(".wpb_main_sortable .wpb_sortable").length + 1,
		element: element.attr('id'),
		data_element: element.attr('data-element'),
		data_width: element.attr('data-width')
	};

	// since 2.8 ajaxurl is always defined in the admin header and points to admin-ajax.php
	jQuery.post(ajaxurl, data, function(response) {
		//alert('Got this from the server: ' + response);
		//jQuery(target).append(response);

		//Fire INIT callback if it is defined
		//jQuery(response).find(".wpb_vc_init_callback").each(function(index) {
        target.removeClass('empty_column');
		jQuery(target).append(response).find(".wpb_vc_init_callback").each(function(index) {
			var fn = window[jQuery(this).attr("value")];
			if ( typeof fn === 'function' ) {
			    fn(jQuery(this).closest('.wpb_content_element').removeClass('empty_column'));
			}
		});
        jQuery.wpb_composer.isMainContainerEmpty();
		////


		//initTabs();
		//if (action == 'initDroppable') { initDroppable(); }
		initDroppable();
		save_composer_html();
	});

} // end getElementMarkup()



/* Set action for column size and delete buttons
---------------------------------------------------------- */
function columnControls() {
	jQuery(".column_delete").live("click", function(e) {
		e.preventDefault();
		var answer = confirm ("Press OK to delete section, Cancel to leave");
		if (answer) {
            $parent = jQuery(this).closest(".wpb_sortable");
			jQuery(this).closest(".wpb_sortable").remove();
            $parent.addClass('empty_column');
			save_composer_html();
		}
	});
	jQuery(".column_clone").live("click", function(e) {
		e.preventDefault();
		var closest_el = jQuery(this).closest(".wpb_sortable"),
			cloned = closest_el.clone();

		cloned.insertAfter(closest_el).hide().fadeIn();

		//Fire INIT callback if it is defined
		cloned.find('.wpb_initialized').removeClass('wpb_initialized');
		cloned.find(".wpb_vc_init_callback").each(function(index) {
			var fn = window[jQuery(this).attr("value")];
			if ( typeof fn === 'function' ) {
			    fn(cloned);
			}
		});

		//closest_el.clone().appendTo(jQuery(this).closest(".wpb_main_sortable, .wpb_column_container")).hide().fadeIn();
		save_composer_html();
	});

	jQuery(".wpb_sortable .wpb_sortable .column_popup").live("click", function(e) {
		e.preventDefault();
		var answer = confirm ("Press OK to pop (move) section to the top level, Cancel to leave");
		if (answer) {
			jQuery(this).closest(".wpb_sortable").appendTo('.wpb_main_sortable');//insertBefore('.wpb_main_sortable div.wpb_clear:last');
			initDroppable();
			save_composer_html();
		}
	});

	jQuery(".column_edit, .column_edit_trigger").live("click", function(e) {
		e.preventDefault();
		jQuery('body,html').animate({ scrollTop: 0});
		var element = jQuery(this).closest('.wpb_sortable');
		showEditForm(element);
	});



	jQuery(".column_increase").live("click", function(e) {
		e.preventDefault();
		var column = jQuery(this).closest(".wpb_sortable"),
			sizes = getColumnSize(column),
			assetTypeIsCarousel = column.hasClass('wpb_carousel');
		if (assetTypeIsCarousel) {
			sizes = getAltColumnSize(column);
			if (sizes[1]) {
				column.removeClass(sizes[0]).addClass(sizes[1]);
				/* get updated column size */
				sizes = getAltColumnSize(column);
				jQuery(column).find(".column_size:first").html(sizes[3]);
				save_composer_html();
			}
		} else {
			if (sizes[1]) {
				column.removeClass(sizes[0]).addClass(sizes[1]);
				/* get updated column size */
				sizes = getColumnSize(column);
				jQuery(column).find(".column_size:first").html(sizes[3]);
				save_composer_html();
			}
		}
	});
	
	jQuery(".column_decrease").live("click", function(e) {
		e.preventDefault();
		var column = jQuery(this).closest(".wpb_sortable"),
			sizes = getColumnSize(column),
			assetTypeIsCarousel = column.hasClass('wpb_carousel') || column.hasClass('wpb_team');
		if (assetTypeIsCarousel) {
			sizes = getAltColumnSize(column);
			if (sizes[2]) {
				column.removeClass(sizes[0]).addClass(sizes[2]);
				/* get updated column size */
				sizes = getAltColumnSize(column);
				jQuery(column).find(".column_size:first").html(sizes[3]);
				save_composer_html();
			}
		} else {
			if (sizes[2]) {
				column.removeClass(sizes[0]).addClass(sizes[2]);
				/* get updated column size */
				sizes = getColumnSize(column);
				jQuery(column).find(".column_size:first").html(sizes[3]);
				save_composer_html();
			}
		}
	});
} // end columnControls()


/* Show widget edit form
---------------------------------------------------------- */
var current_scroll_pos = 0;
function showEditForm(element) {
	current_scroll_pos = jQuery('body, html').scrollTop();
	//
	var element_shortcode = generateShortcodesFromHtml(element, true),
		element_type = element.attr("data-element_type");

	jQuery('#visual_composer_edit_form').html(jQuery('#wpb_vc_loading').val()).show().css({"padding-top" : 60});
	jQuery("#publish").hide(); // hide main publish button
	jQuery('.wpb_main_sortable, #wpb_visual_composer-elements, .wpb_switch-to-composer').hide();

	var data = {
		action: 'wpb_show_edit_form',
		element: element_type,
		shortcode: element_shortcode
	};

	// since 2.8 ajaxurl is always defined in the admin header and points to admin-ajax.php
	jQuery.post(ajaxurl, data, function(response) {
		jQuery('#visual_composer_edit_form').html(response).css({"padding-top" : 0});
        jQuery.wpb_composer.initializeFormEditing(element);
		// ALT BACKGROUND PREVIEW INIT
		var altBackgroundValue = jQuery('#visual_composer_edit_form').find('.alt_background').val();
		if (altBackgroundValue != "") {
			jQuery('#visual_composer_edit_form').find('.altbg-preview').addClass(altBackgroundValue);
		}
	});
}



function saveFormEditing(element) {
	jQuery("#publish").show(); // show main publish button
	jQuery('.wpb_main_sortable, #wpb_visual_composer-elements, .wpb_switch-to-composer').show();

	//save data
	jQuery("#visual_composer_edit_form .wpb_vc_param_value").each(function(index) {
		var element_to_update = jQuery(this).attr("name"),
			new_value = '';

		// Textfield - input
		if ( jQuery(this).hasClass("textfield") ) {
			new_value = jQuery(this).val();
		}
		// Dropdown - select
		else if ( jQuery(this).hasClass("dropdown") ) {
			new_value = jQuery(this).val(); // get selected element

			var all_classes_ar = new Array(),
				all_classes = '';
			jQuery(this).find('option').each(function() {
				var val = jQuery(this).attr('value');
				all_classes_ar.push(val); //populate all posible dropdown values
			});

			all_classes = all_classes_ar.join(" "); // convert array to string

			//element.removeClass(all_classes).addClass(new_value); // remove all possible class names and add only selected one
			element.find('.wpb_element_wrapper').removeClass(all_classes).addClass(new_value); // remove all possible class names and add only selected one
		}
		else if ( jQuery(this).hasClass("select-multiple") ) {
					
			var selected = jQuery(this).val();
					
			all_selected = selected.join(","); // convert array to string
						
			new_value = all_selected; // get selected element
						
			//element.removeClass(all_classes).addClass(new_value); // remove all possible class names and add only selected one
			//element.find('.wpb_element_wrapper').removeClass(all_classes).addClass(new_value); // remove all possible class names and add only selected one
		}
		// WYSIWYG field
		else if ( jQuery(this).hasClass("textarea_html") ) {
			new_value = getTinyMceHtml(jQuery(this));
		}
		// Check boxes
		else if ( jQuery(this).hasClass("wpb-checkboxes") ) {
			var posstypes_arr = new Array();
			jQuery(this).closest('.edit_form_line').find('input').each(function(index) {
				var self = jQuery(this);
				element_to_update = self.attr("name");
				if ( self.is(':checked') ) {
					posstypes_arr.push(self.attr("id"));
				}
			});
			if ( posstypes_arr.length > 0 ) {
				new_value = posstypes_arr.join(',');
			}
		}
		// Exploded textarea
		else if ( jQuery(this).hasClass("exploded_textarea") ) {
			new_value = jQuery(this).val().replace(/\n/g, ",");
		}
		// Regular textarea
		else if ( jQuery(this).hasClass("textarea") ) {
			new_value = jQuery(this).val();
		}
        else if ( jQuery(this).hasClass("textarea_raw_html") ) {
            new_value = jQuery(this).val();
            element.find('[name='+element_to_update+'_code]').val(btoa(new_value));
            new_value = jQuery("<div/>").text(new_value).html();
        }
		// Attach images
		else if ( jQuery(this).hasClass("attach_images") ) {
			new_value = jQuery(this).val();
		}
        else if ( jQuery(this).hasClass("attach_image") ) {
            new_value = jQuery(this).val();
            /* KLUDGE: to change image */
            var $thumbnail = element.find('[name='+element_to_update+']').next('.attachment-thumbnail');

            $thumbnail.attr('src', jQuery(this).parent().find('li.added img').attr('src'));
            $thumbnail.next().addClass('image-exists');
        }

		element_to_update = element_to_update.replace('wpb_tinymce_', '');
		if ( element.find('.'+element_to_update).is('div, h1,h2,h3,h4,h5,h6, span, i, b, strong, button') ) {

			//element.find('.'+element_to_update).html(new_value);
			element.find('[name='+element_to_update+']').html(new_value);
		} else {
			//element.find('.'+element_to_update).val(new_value);
			element.find('[name='+element_to_update+']').val(new_value);
		}
	});

	// Get callback function name
	var cb = element.children(".wpb_vc_save_callback");
	//
	if ( cb.length == 1 ) {
		var fn = window[cb.attr("value")];
		if ( typeof fn === 'function' ) {
		    var tmp_output = fn(element);
		}
	}

	save_composer_html();
	jQuery('#visual_composer_edit_form').html('').hide();

	jQuery('body, html').scrollTop(current_scroll_pos);
}

function getTinyMceHtml(obj) {

	var mce_id = obj.attr('id'),
		html_back;

	//html_back = tinyMCE.get(mce_id).getContent();

	//tinyMCE.execCommand('mceRemoveControl', false, mce_id);
	try {
		html_back = tinyMCE.get(mce_id).getContent();
		if (tinyMCE.majorVersion >= 4) {
			tinyMCE.execCommand("mceRemoveEditor", true, mce_id);
		} else {
			tinyMCE.execCommand("mceRemoveControl", true, mce_id);
		}
	}
	catch (err) {
		html_back = switchEditors.wpautop(obj.val());
	}

	return html_back;
}

function initTinyMce(element) {
//	wpb_def_wp_editor = tinyMCE.activeEditor;

	var textfield_id = element.attr("id");
	
	if (tinyMCE.majorVersion >= 4) {
		tinyMCE.execCommand("mceAddEditor", true, textfield_id);
	} else {
		tinyMCE.execCommand("mceAddControl", true, textfield_id);
	}

	element.closest('.edit_form_line').find('.wp-switch-editor').removeAttr("onclick");
	element.closest('.edit_form_line').find('.switch-tmce').click(function() {
		element.closest('.edit_form_line').find('.wp-editor-wrap').removeClass('html-active').addClass('tmce-active');

		var val = switchEditors.wpautop( jQuery(this).closest('.edit_form_line').find("textarea.visual_composer_tinymce").val() );
		jQuery("textarea.visual_composer_tinymce").val(val);
		// Add tinymce
		if (tinyMCE.majorVersion >= 4) {
			tinyMCE.execCommand("mceAddEditor", true, textfield_id);
		} else {
			tinyMCE.execCommand("mceAddControl", true, textfield_id);
		}
	});
	element.closest('.edit_form_line').find('.switch-html').click(function() {
		element.closest('.edit_form_line').find('.wp-editor-wrap').removeClass('tmce-active').addClass('html-active');
		if (tinyMCE.majorVersion >= 4) {
			tinyMCE.execCommand("mceRemoveEditor", true, textfield_id);
		} else {
			tinyMCE.execCommand("mceRemoveControl", true, textfield_id);
		}
	});
}

function isTinyMceActive() {
	var rich = (typeof tinyMCE != "undefined") && tinyMCE.activeEditor && !tinyMCE.activeEditor.isHidden();
	return rich;
}

/* This function helps when you need to determine current
   column size.

   Returns Array("current size", "larger size", "smaller size", "size string");
---------------------------------------------------------- */
function getColumnSize(column) {
	if (column.hasClass("span12")) //full-width
		return new Array("span12", "span12", "span9", "1/1");

	else if (column.hasClass("span9")) //three-fourth
		return new Array("span9", "span12", "span8", "3/4");

	else if (column.hasClass("span8")) //two-third
		return new Array("span8", "span9", "span6", "2/3");

	else if (column.hasClass("span6")) //one-half
		return new Array("span6", "span8", "span4", "1/2");

	else if (column.hasClass("span4")) // one-third
		return new Array("span4", "span6", "span3", "1/3");

	else if (column.hasClass("span3")) // one-fourth
		return new Array("span3", "span4", "span3", "1/4");
	else
		return false;
} // end getColumnSize()

function getAltColumnSize(column) {
	if (column.hasClass("span12")) //full-width
		return new Array("span12", "span12", "span9", "1/1");

	else if (column.hasClass("span9")) //three-fourth
		return new Array("span9", "span12", "span6", "3/4");

	else if (column.hasClass("span6")) //one-half
		return new Array("span6", "span9", "span3", "1/2");

	else if (column.hasClass("span3")) // one-fourth
		return new Array("span3", "span6", "span3", "1/4");
	else
		return false;
} // end getAltColumnSize()

/* This functions goes throw the dom tree and automatically
   adds 'last' class name to the columns elements.
---------------------------------------------------------- */
function addLastClass(dom_tree) {
    return jQuery.wpb_composer.addLastClass(dom_tree);
	//jQuery(dom_tree).children(".column:first").addClass("first");
	//jQuery(dom_tree).children(".column:last").addClass("last");
} // endjQuery.wpb_composer.addLastClass()

/* This functions copies html code into custom field and
   then on page reload/refresh it is used to build the
   initial layout.
---------------------------------------------------------- */
function save_composer_html() {
jQuery.wpb_composer.addLastClass(jQuery(".wpb_main_sortable"));

	var shortcodes = generateShortcodesFromHtml(jQuery(".wpb_main_sortable"));
	//console.log(shortcodes);

	//console.log(tinyMCE.ed.isHidden());

	//if ( tinyMCE.activeEditor == null ) {

	//setActive(wpb_def_wp_editor.editorId);

	if ( isTinyMceActive() != true ) {
		//TODO: WPML and qTranslate
		//tinyMCE.activeEditor.setContent(shortcodes, {format : 'html'});
		jQuery('#content').val(shortcodes);
	} else {
		tinyMCE.activeEditor.setContent(shortcodes, {format : 'html'});
	}

    jQuery.wpb_composer.isMainContainerEmpty();

	/*var val = jQuery.trim(jQuery(".wpb_main_sortable").html());
	jQuery("#visual_composer_html_code_holder").val(val);

	var shortcodes = generateShortcodesFromHtml(jQuery(".wpb_main_sortable"));
	jQuery("#visual_composer_code_holder").val(shortcodes);

	var tiny_val = switchEditors.wpautop(shortcodes);

	//[REVISE] Should determine what mode is currently on Visual/HTML
	tinyMCE.get('content').setContent(tiny_val, {format : 'raw'});

	/*try {
		tinyMCE.get('content').setContent(tiny_val, {format : 'raw'});
	}
	catch (err) {
		switchEditors.go('content', 'html');
		jQuery('#content').val(shortcodes);
	}*/
}

/* Generates shortcode values
---------------------------------------------------------- */
var current_top_level = null;
function generateShortcodesFromHtml(dom_tree, single_element) {
	var output = '';
	if ( single_element ) {
		// this is used to generate shortcode for a single content element
		selector_to_go_throw = jQuery(dom_tree);
	} else {
		selector_to_go_throw = jQuery(dom_tree).children(".wpb_sortable");
	}

	selector_to_go_throw.each(function(index) {
	//jQuery(dom_tree.selector+" > .wpb_sortable").each(function(index) {
		var element = jQuery(this),
			current_top_level = element,
			sc_base = element.find('.wpb_vc_sc_base').val(),
			column_el_width = getColumnSize(element),
			params = '',
			sc_ending = ']';

			element.children('.wpb_element_wrapper').children('.wpb_vc_param_value').each(function(index) {
				var param_name = jQuery(this).attr("name"),
					new_value = '';
				if ( jQuery(this).hasClass("textfield") ) {
					if (jQuery(this).is('div, h1,h2,h3,h4,h5,h6, span, i, b, strong')) {
						new_value = jQuery(this).html();
					} else if ( jQuery(this).is('button') ) {
						new_value = jQuery(this).text();
					} else {
						new_value = jQuery(this).val();
					}
				}
				else if ( jQuery(this).hasClass("dropdown") ) {
					new_value = jQuery(this).val();
				}
				else if ( jQuery(this).hasClass("select-multiple") ) {
					new_value = jQuery(this).val();
				}
				else if ( jQuery(this).hasClass("textarea_raw_html") && element.children('.wpb_sortable').length == 0 ) {
					content_value = jQuery(this).next('.' + param_name + '_code').val();
					sc_ending = '] '+ content_value +' [/'+sc_base+']';
				}
                else if ( jQuery(this).hasClass("textarea_html") && element.children('.wpb_sortable').length == 0 ) {
                    content_value = jQuery(this).html();
                    sc_ending = '] '+content_value+' [/'+sc_base+']';
                }
				else if ( jQuery(this).hasClass("posttypes") ) {
					new_value = jQuery(this).val();
				}
				else if ( jQuery(this).hasClass("exploded_textarea") ) {
					new_value = jQuery(this).val();
				}
				else if ( jQuery(this).hasClass("textarea") ) {
					if ( jQuery(this).is('div, h1,h2,h3,h4,h5,h6, span, i, b, strong') ) {
						new_value = jQuery(this).html();
					} else {
						new_value = jQuery(this).val();
					}
				}
				else if ( jQuery(this).hasClass("attach_images") ) {
                    new_value = jQuery(this).val();
                }
                else if ( jQuery(this).hasClass("attach_image") ) {
                    new_value = jQuery(this).val();
                }
				else if ( jQuery(this).hasClass("widgetised_sidebars") ) {
					new_value = jQuery(this).val();
				}

				new_value = jQuery.trim(new_value);
				if (new_value != '') { params += ' '+param_name+'="'+new_value+'"'; }
			});


			params += ' width="'+column_el_width[3]+'"'

			if ( element.hasClass("wpb_first") || element.hasClass("wpb_last")) {
				var wpb_first = (element.hasClass("wpb_first")) ? 'first' : '';
				var wpb_last = (element.hasClass("wpb_last")) ? 'last' : '';
				var pos_space = (element.hasClass("wpb_last") && element.hasClass("wpb_first")) ? ' ' : '';
				params += ' el_position="'+wpb_first+pos_space+wpb_last+'"';
			}

			// Get callback function name
			var cb = element.children(".wpb_vc_shortcode_callback");
			//
			if ( cb.length == 1 ) {
				var fn = window[cb.attr("value")];
				if ( typeof fn === 'function' ) {
				    var tmp_output = fn(element);
				}
			}


			output += '['+sc_base+params+sc_ending+' ';

			//deeper
			//if ( element.children('.wpb_element_wrapper').children('.wpb_column_container').children('.wpb_sortable').length > 0 ) {
			if ( element.children('.wpb_element_wrapper').find('.wpb_column_container').length > 0 ) {
				//output += generateShortcodesFromHtml(element.children('.wpb_element_wrapper').children('.wpb_column_container'));

				// Get callback function name
				var cb = element.children(".wpb_vc_shortcode_callback"),
					inner_element_count = 0;
				//
				element.children('.wpb_element_wrapper').find('.wpb_column_container').each(function(index) {
					//output += '[aaa]'+generateShortcodesFromHtml(jQuery(this))+'[/aaa]';

					var sc = generateShortcodesFromHtml(jQuery(this));
					//Fire SHORTCODE GENERATION callback if it is defined
					if ( cb.length == 1 ) {
						var fn = window[cb.attr("value")];
						if ( typeof fn === 'function' ) {
						    var tmp_output = fn(current_top_level, inner_element_count);
						}
						sc = " " + tmp_output.replace("%inner_shortcodes", sc) + " ";

						//console.log(current_top_level[0]);


						//var tmp_output = eval(cb.attr("value")+"("+current_top_level+")");
						//var tmp_output = eval(cb.attr("value")+"('"+current_top_level+"', "+inner_element_count+")");
						//sc = " " + tmp_output.replace("%inner_shortcodes", sc);
						inner_element_count++;
					}
					//else {
					//	output += sc;
					//}
					output += sc;
				});

				output += '[/'+sc_base+'] ';
			}
	});

	return output;
} // end generateShortcodesFromHtml()

/* This function adds a class name to the div#drag_placeholder,
   and this helps us to give a style to the draging placeholder
---------------------------------------------------------- */
function renderCorrectPlaceholder(event, ui) {
	jQuery("#drag_placeholder").addClass("column_placeholder").html("Drag and drop me into the editor");
}


/* Custom Callbacks
---------------------------------------------------------- */

/* Tabs Callbacks
---------------------------------------------------------- */
function wpbTabsInitCallBack(element) {
	element.find('.wpb_tabs_holder').not('.wpb_initialized').each(function(index) {
		jQuery(this).addClass('wpb_initialized');
		//var tab_counter = 4;
		//
		var $tabs,
			add_btn = jQuery(this).closest('.wpb_element_wrapper').find('.add_tab'),
			edit_btn = jQuery(this).closest('.wpb_element_wrapper').find('.edit_tab'),
			delete_btn = jQuery(this).closest('.wpb_element_wrapper').find('.delete_tab');
		//

		$tabs = jQuery(this).tabs({
			panelTemplate: '<div class="row-fluid wpb_column_container empty_column wpb_sortable_container not-column-inherit">' + jQuery('#container-helper-block').html() + '</div>',
			add: function( event, ui ) {
				var tabs_count = jQuery(this).tabs( "length" ) - 1;
				jQuery(this).tabs( "select" , tabs_count);
				//
				save_composer_html();
			}
		});
		var sort_axis = ( jQuery(this).closest('.wpb_sortable').hasClass('wpb_vc_tour')) ? 'y' : 'x';
		$tabs.find( ".ui-tabs-nav" ).sortable({
			axis: sort_axis,
			stop: function(event, ui) {
				$tabs.find('ul li').each(function(index) {
					var href = jQuery(this).find('a').attr('href').replace("#", "");
					$tabs.find('div.wpb_column_container#'+href).appendTo($tabs);
				});
				//
				save_composer_html();
			}
		});
		//
		delete_btn.click( function(e) {
			e.preventDefault();

			var tabs_asset = jQuery(this).parent().parent().find('.wpb_tabs_holder'),
				tab_name = jQuery(this).parent().parent().find('.ui-tabs-nav li.ui-state-active a').text(),
				tab_pos = jQuery(this).parent().parent().find('.ui-tabs-nav li.ui-state-active').index()
				alt_tab_pos = tab_pos + 1;
						
			var answer = confirm ('Press OK to delete "'+tab_name+'" tab, or cancel.');
			if ( answer ) {
				$tabs.find('.ui-tabs-nav li:eq('+tab_pos+')').remove();
				if ($tabs.closest('.wpb_sortable').hasClass('wpb_tour')) {
				$tabs.find('#tab-'+alt_tab_pos).remove();
				$tabs.find('#tab-slide-'+alt_tab_pos).remove();
				} else {
				tabs_asset.find('#tab-'+alt_tab_pos).remove();
				tabs_asset.find('#tab-tab-'+alt_tab_pos).remove();
				}
				//
				$tabs.tabs('refresh');
				save_composer_html();
			}
			return false;
			
		});

		add_btn.click( function(e) {
			e.preventDefault();

			var tab_title = ( jQuery(this).closest('.wpb_sortable').hasClass('wpb_vc_tour')) ? 'Slide' : 'Tab',
				tabs_count = jQuery(this).parent().parent().find('.ui-tabs-nav li').length + 1,
				tabs_asset = jQuery(this).parent().parent().find('.wpb_tabs_holder'),
				tabs_nav = tabs_asset.find('.ui-tabs-nav');
			
			if (jQuery(this).closest('.wpb_sortable').hasClass('wpb_vc_tour')) {
				tabs_nav.append('<li class="ui-state-default ui-corner-top" role="tab" tabindex="-1" aria-controls="tab-slide-'+tabs_count+'" aria-labelledby="ui-id-'+tabs_count+'" aria-selected="false"><a href="#tab-slide-'+tabs_count+'" class="ui-tabs-anchor" role="presentation" tabindex="-1" id="ui-id-'+tabs_count+'">'+tab_title+' '+tabs_count+'</a></li>');
				
				tabs_asset.append('<div id="tab-slide-'+tabs_count+'" class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit ui-sortable ui-droppable ui-tabs-panel ui-widget-content ui-corner-bottom" aria-labelledby="ui-id-'+tabs_count+'" role="tabpanel" aria-expanded="true" aria-hidden="false"> <div data-element_type="vc_column_text" class="wpb_vc_column_text wpb_content_element wpb_sortable span12 wpb_first wpb_last"><input type="hidden" class="wpb_vc_sc_base" name="element_name-vc_column_text" value="vc_column_text"><div class="controls sidebar-name"> <div class="column_size_wrapper"> <a class="column_decrease" href="#" title="Decrease width"></a> <span class="column_size">1/1</span> <a class="column_increase" href="#" title="Increase width"></a> </div><div class="controls_right"> <a class="column_popup" href="#" title="Pop up"></a> <a class="column_edit" href="#" title="Edit"></a> <a class="column_clone" href="#" title="Clone"></a> <a class="column_delete" href="#" title="Delete"></a></div></div><div class="wpb_element_wrapper clearfix"><input type="hidden" class="wpb_vc_param_value title textfield " name="title" value=""><input type="hidden" class="wpb_vc_param_value icon textfield " name="icon" value=""><div class="wpb_vc_param_value content textarea_html " name="content"><p>This is a text block. Click the edit button to change this text..</p></div><input type="hidden" class="wpb_vc_param_value pb_margin_bottom dropdown " name="pb_margin_bottom" value="no"><input type="hidden" class="wpb_vc_param_value pb_border_bottom dropdown " name="pb_border_bottom" value="no"><input type="hidden" class="wpb_vc_param_value el_class textfield " name="el_class" value=""></div> <!-- end .wpb_element_wrapper --></div> <!-- end #element-vc_column_text --> <div class="container-helper"><a href="javascript:open_elements_dropdown();" class="open-dropdown-content-element"><i class="icon"></i> Add Content Elements</a><span>- or -</span><a href="#" class="add-text-block-to-content" parent-container="#visual_composer_content"><i class="icon"></i> Add Text block with a single click</a></div></div>');
			} else {
				tabs_nav.append('<li class="ui-state-default ui-corner-top" role="tab" tabindex="-1" aria-controls="tab-tab-'+tabs_count+'" aria-labelledby="ui-id-'+tabs_count+'" aria-selected="false" style="position: relative; top: 0px;"><a href="#tab-tab-'+tabs_count+'" class="ui-tabs-anchor" role="presentation" tabindex="-1" id="ui-id-'+tabs_count+'">'+tab_title+' '+tabs_count+'</a></li>');
				
				tabs_asset.append('<div id="tab-tab-'+tabs_count+'" class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit ui-sortable ui-droppable ui-tabs-panel ui-widget-content ui-corner-bottom" aria-labelledby="ui-id-5" role="tabpanel" aria-expanded="true" aria-hidden="false"><div class="container-helper"><a href="javascript:open_elements_dropdown();" class="open-dropdown-content-element"><i class="icon"></i> Add Content Elements</a><span>- or -</span><a href="#" class="add-text-block-to-content" parent-container="#visual_composer_content"><i class="icon"></i> Add Text block with a single click</a></div><div data-element_type="vc_column_text" class="wpb_vc_column_text wpb_content_element wpb_sortable span12 wpb_first wpb_last" style=""><input type="hidden" class="wpb_vc_sc_base" name="element_name-vc_column_text" value="vc_column_text"><div class="controls sidebar-name"> <div class="column_size_wrapper"> <a class="column_decrease" href="#" title="Decrease width"></a> <span class="column_size">1/1</span> <a class="column_increase" href="#" title="Increase width"></a> </div><div class="controls_right"> <a class="column_popup" href="#" title="Pop up"></a> <a class="column_edit" href="#" title="Edit"></a> <a class="column_clone" href="#" title="Clone"></a> <a class="column_delete" href="#" title="Delete"></a></div></div><div class="wpb_element_wrapper clearfix"><input type="hidden" class="wpb_vc_param_value title textfield " name="title" value=""><input type="hidden" class="wpb_vc_param_value icon textfield " name="icon" value=""><div class="wpb_vc_param_value content textarea_html " name="content"><p>This is a text block. Click the edit button to change this text..</p></div><input type="hidden" class="wpb_vc_param_value pb_margin_bottom dropdown " name="pb_margin_bottom" value="no"><input type="hidden" class="wpb_vc_param_value pb_border_bottom dropdown " name="pb_border_bottom" value="no"><input type="hidden" class="wpb_vc_param_value el_class textfield " name="el_class" value=""></div> <!-- end .wpb_element_wrapper --></div></div>');
			}
			
			$tabs.tabs('refresh');
			
			initDroppable();
			save_composer_html();
		});

		edit_btn.click( function() {
			var tab_name = $tabs.find('ul li.ui-state-active a').text();

			var tab_title = prompt("Please enter new tab title", tab_name);
			if ( tab_title != null && tab_title != "" ) {
				$tabs.find('ul li.ui-tabs-active a').text(tab_title);
				//
				save_composer_html();
			}
			return false;
		});

	});

	initDroppable();
}

function wpbTabsGenerateShortcodeCallBack(current_top_level, inner_element_count) {
	var tab_title = current_top_level.find(".ui-tabs-nav li:eq("+inner_element_count+") a").text();
	output = '[vc_tab title="'+tab_title+'"] %inner_shortcodes [/vc_tab]';
	return output;
}

/* Accordion Callback
---------------------------------------------------------- */
function wpbAccordionInitCallBack(element) {
	element.find('.wpb_accordion_holder').not('.wpb_initialized').each(function(index) {
		jQuery(this).addClass('wpb_initialized');
		//var tab_counter = 4;
		//
		var $tabs,
			add_btn = jQuery(this).closest('.wpb_element_wrapper').find('.add_tab'),
			edit_btn = jQuery(this).closest('.wpb_element_wrapper').find('.edit_tab'),
			delete_btn = jQuery(this).closest('.wpb_element_wrapper').find('.delete_tab');
		//
		$tabs = jQuery(this).accordion({
			header: "> div > h3",
			autoHeight: false
		})
		.sortable({
			axis: "y",
			handle: "h3",
			stop: function( event, ui ) {
				// IE doesn't register the blur when sorting
				// so trigger focusout handlers to remove .ui-state-focus
				ui.item.children( "h3" ).triggerHandler( "focusout" );
				//
				save_composer_html();
			}
		});

		delete_btn.click( function(e) {
			e.preventDefault();

			var tab_name = $tabs.find('h3.ui-state-active a').text();

			var answer = confirm ('Press OK to delete "'+tab_name+'" section, Cancel to leave');
			if ( answer ) {
				$tabs.find('h3.ui-state-active a').closest('.group').remove();
				//
				save_composer_html();
			}
		});

		add_btn.click( function(e) {
			e.preventDefault();
			var tab_title = 'Section',
				section_template = '<div class="group"><h3><a href="#">Section</a></h3><div class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit"></div></div>';
			$tabs.append(section_template);
			$tabs.accordion( "destroy" )
			.accordion({
				header: "> div > h3",
				autoHeight: false
			})
			.sortable({
				axis: "y",
				handle: "h3",
				stop: function( event, ui ) {
					// IE doesn't register the blur when sorting
					// so trigger focusout handlers to remove .ui-state-focus
					ui.item.children( "h3" ).triggerHandler( "focusout" );
					//
					save_composer_html();
				}
			});

			//$tabs.tabs( "add", "#tabs-" + tabs_count, tab_title );
			//tab_counter++;
			//
			initDroppable();
			save_composer_html();
		});

		edit_btn.click( function() {
			var tab_name = $tabs.find('h3.ui-state-active a').text();

			var tab_title = prompt("Please enter new section title", tab_name);
			if ( tab_title != null && tab_title != "" ) {
				$tabs.find('h3.ui-state-active a').text(tab_title);
				//
				save_composer_html();
			}
			return false;
		});
	});
	initDroppable();
}

function wpbAccordionGenerateShortcodeCallBack(current_top_level, inner_element_count) {
	var tab_title = current_top_level.find(".group:eq("+inner_element_count+") > h3").text();
	output = '[vc_accordion_tab title="'+tab_title+'"] %inner_shortcodes [/vc_accordion_tab]';
	return output;
}

/* Message box Callbacks
---------------------------------------------------------- */
function wpbMessageInitCallBack(element) {
	var el = element.find('.wpb_vc_param_value.color');
	var class_to_set = el.val();
	el.closest('.wpb_element_wrapper').addClass(class_to_set);
}

/* Text Separator Callbacks
---------------------------------------------------------- */
function wpbTextSeparatorInitCallBack(element) {
	var el = element.find('.wpb_vc_param_value.title_align');
	var class_to_set = el.val();
	el.closest('.wpb_element_wrapper').addClass(class_to_set);
}

/* Call to action Callbacks
---------------------------------------------------------- */
function wpbCallToActionInitCallBack(element) {
	var el = element.find('.wpb_vc_param_value.position');
	var class_to_set = el.val();
	el.closest('.wpb_element_wrapper').addClass(class_to_set);
}
function wpbCallToActionSaveCallBack(element) {
	var el_class = element.find('.wpb_vc_param_value.color').val() + " " + element.find('.wpb_vc_param_value.icon').val();
	//
	element.find('.wpb_element_wrapper').removeClass(el_class);
}

/* Button Callbacks
---------------------------------------------------------- */
function wpbButtonInitCallBack(element) {
	var el_class = element.find('.wpb_vc_param_value.color').val() + ' ' + element.find('.wpb_vc_param_value.size').val() + ' ' + element.find('.wpb_vc_param_value.icon').val();
	//
	element.find('button.title').attr({ "class" : "wpb_vc_param_value title textfield btn " + el_class });

	var icon = element.find('.wpb_vc_param_value.icon').val();
	if ( icon != 'none' && element.find('button i.icon').length == 0  ) {
		element.find('button.title').append(' <i class="icon"></i>');
	}
}

function wpbButtonSaveCallBack(element) {
	var el_class = element.find('.wpb_vc_param_value.color').val() + ' ' + element.find('.wpb_vc_param_value.size').val() + ' ' + element.find('.wpb_vc_param_value.icon').val();
	//
	element.find('.wpb_element_wrapper').removeClass(el_class);
	element.find('button.title').attr({ "class" : "wpb_vc_param_value title textfield btn " + el_class });

	var icon = element.find('.wpb_vc_param_value.icon').val();
	if ( icon != 'none' && element.find('button i.icon').length == 0 ) {
		element.find('button.title').append(' <i class="icon"></i>');
	} else {
		element.find('button.title i.icon').remove();
	}
}