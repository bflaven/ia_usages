<?php
/**
 * Swift Page Builder Shortcodes settings
 *
 * @package VPBakeryVisualComposer
 *
 */
WPBMap::map( 'vc_column_text', array(
    "name"		=> __("Text block", "js_composer"),
    "base"		=> "vc_column_text",
    "class"		=> "",
    "icon"      => "icon-wpb-layer-shape-text",
    "wrapper_class" => "clearfix",
    "controls"	=> "full",
    "params"	=> array(
    	array(
    	    "type" => "textfield",
    	    "heading" => __("Widget title", "js_composer"),
    	    "param_name" => "title",
    	    "value" => "",
    	    "description" => __("Heading text. Leave it empty if not needed.", "js_composer")
    	),
        array(
            "type" => "textarea_html",
            "holder" => "div",
            "class" => "",
            "heading" => __("Text", "js_composer"),
            "param_name" => "content",
            "value" => __("<p>I am text block. click the edit button to change this text.</p>", "js_composer"),
            "description" => __("Enter your content.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Margin below widget", "js_composer"),
            "param_name" => "pb_margin_bottom",
            "value" => array(__('No', "js_composer") => "no", __('Yes', "js_composer") => "yes"),
            "description" => __("Add a bottom margin to the widget.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Border below widget", "js_composer"),
            "param_name" => "pb_border_bottom",
            "value" => array(__('No', "js_composer") => "no", __('Yes', "js_composer") => "yes"),
            "description" => __("Add a bottom border to the widget.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    )
) );


/* Boxed Content
---------------------------------------------------------- */
WPBMap::map( 'box', array(
    "name"		=> __("Boxed content", "js_composer"),
    "base"		=> "box",
    "class"		=> "",
    "icon"      => "icon-wpb-layer-shape-box",
    "wrapper_class" => "clearfix",
    "controls"	=> "full",
    "params"	=> array(
    	array(
    	    "type" => "textfield",
    	    "heading" => __("Widget title", "js_composer"),
    	    "param_name" => "title",
    	    "value" => "",
    	    "description" => __("Heading text. Leave it empty if not needed.", "js_composer")
    	),
        array(
            "type" => "textarea_html",
            "holder" => "div",
            "class" => "",
            "heading" => __("Text", "js_composer"),
            "param_name" => "content",
            "value" => __("<p>I am boxed content block. click the edit button to change this text.</p>", "js_composer"),
            "description" => __("Enter your content.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Box type", "js_composer"),
            "param_name" => "type",
            "value" => array(__('Coloured', "js_composer") => "coloured", __('White with stroke', "js_composer") => "whitestroke"),
            "description" => __("Choose the surrounding box type for this content", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Margin below widget", "js_composer"),
            "param_name" => "pb_margin_bottom",
            "value" => array(__('No', "js_composer") => "no", __('Yes', "js_composer") => "yes"),
            "description" => __("Add a bottom margin to the widget.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    )
) );
//
///* Latest tweets
//---------------------------------------------------------- */
//WPBMap::map( 'vc_twitter', array(
//    "name"		=> __("Twitter widget", "js_composer"),
//    "base"		=> "vc_twitter",
//    "class"		=> "wpb_vc_twitter_widget",
//	"icon"		=> 'icon-wpb-balloon-twitter-left',
//    "params"	=> array(
//        array(
//            "type" => "textfield",
//            "heading" => __("Widget title", "js_composer"),
//            "param_name" => "title",
//            "value" => "",
//            "description" => __("What text use as widget title. Leave blank if no title is needed.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Twitter name", "js_composer"),
//            "param_name" => "twitter_name",
//            "value" => "",
//            "description" => __("Type in twitter profile name from which load tweets.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Tweets count", "js_composer"),
//            "param_name" => "tweets_count",
//            "value" => array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
//            "description" => __("How many recent tweets to load.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Extra class name", "js_composer"),
//            "param_name" => "el_class",
//            "value" => "",
//            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
//        )
//    )
//) );

/* Separator (Divider)
---------------------------------------------------------- */
WPBMap::map( 'divider',  array(
    "name"		=> __("Divider", "js_composer"),
    "base"		=> "divider",
    "class"		=> "wpb_divider wpb_controls_top_right",
	'icon'		=> 'icon-wpb-ui-divider',
    "controls"	=> 'edit_popup_delete',
    "params"	=> array(
        array(
            "type" => "dropdown",
            "heading" => __("Divider type", "js_composer"),
            "param_name" => "type",
            "value" => array(__('Standard', "js_composer") => "standard", __('Thin', "js_composer") => "thin", __('Dotted', "js_composer") => "dotted", __('Go to top (text)', "js_composer") => "go_to_top", __('Go to top (Icon 1)', "js_composer") => "go_to_top_icon1", __('Go to top (Icon 2)', "js_composer") => "go_to_top_icon2"),
            "description" => __("Select divider type.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Go to top text", "js_composer"),
            "param_name" => "text",
            "value" => __("Go to top", "js_composer"),
            "description" => __("The text for the 'Go to top (text)' divider type.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    ),
    "js_callback" => array("init" => "wpbTextSeparatorInitCallBack")
) );

/* Blank Spacer (Divider)
---------------------------------------------------------- */
WPBMap::map( 'blank_spacer',  array(
    "name"		=> __("Blank Spacer", "js_composer"),
    "base"		=> "blank_spacer",
    "class"		=> "blank_spacer wpb_controls_top_right",
	'icon'		=> 'icon-wpb-ui-blank-spacer',
    "controls"	=> 'edit_popup_delete',
    "params"	=> array(
        array(
            "type" => "textfield",
            "heading" => __("Height", "js_composer"),
            "param_name" => "height",
            "value" => __("30px", "js_composer"),
            "description" => __("The height of the spacer, in px (required).", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    ),
    "js_callback" => array("init" => "wpbBlankSpacerInitCallBack")
) );

//
//* Textual block
//---------------------------------------------------------- */
//WPBMap::map( 'vc_text_separator', array(
//    "name"		=> __("Separator (Divider) with text", "js_composer"),
//    "base"		=> "vc_text_separator",
//    "class"		=> "wpb_controls_top_right",
//    "controls"	=> "edit_popup_delete",
//	"icon"		=> "icon-wpb-ui-separator-label",
//    "params"	=> array(
//        array(
//            "type" => "textfield",
//            "heading" => __("Title", "js_composer"),
//            "param_name" => "title",
//            "holder" => "div",
//            "value" => __("Title", "js_composer"),
//            "description" => __("Separator title.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Title position", "js_composer"),
//            "param_name" => "title_align",
//            "value" => array(__('Align center', "js_composer") => "separator_align_center", __('Align left', "js_composer") => "separator_align_left", __('Align right', "js_composer") => "separator_align_right"),
//            "description" => __("Select title location.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Extra class name", "js_composer"),
//            "param_name" => "el_class",
//            "value" => "",
//            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
//        )
//    ),
//    "js_callback" => array("init" => "wpbTextSeparatorInitCallBack")
//) );

/* Message box
---------------------------------------------------------- */
WPBMap::map( 'vc_message', array(
    "name"		=> __("Message box", "js_composer"),
    "base"		=> "vc_message",
    "class"		=> "wpb_vc_messagebox wpb_controls_top_right",
	"icon"		=> "icon-wpb-information-white",
    "wrapper_class" => "alert",
    "controls"	=> "edit_popup_delete",
    "params"	=> array(
        array(
            "type" => "dropdown",
            "heading" => __("Message box type", "js_composer"),
            "param_name" => "color",
            "value" => array(__('Informational', "js_composer") => "alert-info", __('Warning', "js_composer") => "alert-block", __('Success', "js_composer") => "alert-success", __('Error', "js_composer") => "alert-error"),
            "description" => __("Select message type.", "js_composer")
        ),
        array(
            "type" => "textarea_html",
            "holder" => "div",
            "class" => "messagebox_text",
            "heading" => __("Message text", "js_composer"),
            "param_name" => "content",
            "value" => __("<p>I am message box. click the edit button to change this text.</p>", "js_composer"),
            "description" => __("Message text.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    ),
    "js_callback" => array("init" => "wpbMessageInitCallBack")
) );
//
///* Facebook like button
//---------------------------------------------------------- */
//WPBMap::map( 'vc_facebook', array(
//    "name"		=> __("Facebook like", "js_composer"),
//    "base"		=> "vc_facebook",
//    "class"		=> "wpb_vc_facebooklike wpb_controls_top_right",
//	"icon"		=> "icon-wpb-balloon-facebook-left",
//    "controls"	=> "edit_popup_delete",
//    "params"	=> array(
//        array(
//            "type" => "dropdown",
//            "heading" => __("Button type", "js_composer"),
//            "param_name" => "type",
//            "value" => array(__("Standard", "js_composer") => "standard", __("Button count", "js_composer") => "button_count", __("Box count", "js_composer") => "box_count"),
//            "description" => __("Select button type.", "js_composer")
//        )
//    )
//) );
//
///* Tweetmeme button
//---------------------------------------------------------- */
//WPBMap::map( 'vc_tweetmeme', array(
//    "name"		=> __("Tweetmeme button", "js_composer"),
//    "base"		=> "vc_tweetmeme",
//    "class"		=> "wpb_controls_top_right",
//	"icon"		=> "icon-wpb-balloon-twitter-left",
//    "controls"	=> "edit_popup_delete",
//    "params"	=> array(
//        array(
//            "type" => "dropdown",
//            "heading" => __("Button type", "js_composer"),
//            "param_name" => "type",
//            "value" => array(__("Horizontal", "js_composer") => "horizontal", __("Vertical", "js_composer") => "vertical", __("None", "js_composer") => "none"),
//            "description" => __("Select button type.", "js_composer")
//        )
//    )
//) );
//
///* Google+ button
//---------------------------------------------------------- */
//WPBMap::map( 'vc_googleplus', array(
//    "name"		=> __("Google+ button", "js_composer"),
//    "base"		=> "vc_googleplus",
//    "class"		=> "wpb_vc_googleplus wpb_controls_top_right",
//	"icon"		=> "icon-wpb-application-plus",
//    "controls"	=> "edit_popup_delete",
//    "params"	=> array(
//        array(
//            "type" => "dropdown",
//            "heading" => __("Button size", "js_composer"),
//            "param_name" => "type",
//            "value" => array(__("Standard", "js_composer") => "", __("Small", "js_composer") => "small", __("Medium", "js_composer") => "medium", __("Tall", "js_composer") => "tall"),
//            "description" => __("Select button type.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Annotation", "js_composer"),
//            "param_name" => "annotation",
//            "value" => array(__("Inline", "js_composer") => "inline", __("Bubble", "js_composer") => "", __("None", "js_composer") => "none"),
//            "description" => __("Select annotation type.", "js_composer")
//        )
//    )
//) );
//
///* Google+ button
//---------------------------------------------------------- */
//WPBMap::map( 'vc_pinterest', array(
//    "name"		=> __("Pinterest button", "js_composer"),
//    "base"		=> "vc_pinterest",
//    "class"		=> "wpb_vc_pinterest wpb_controls_top_right",
//	"icon"		=> "icon-wpb-pinterest",
//    "controls"	=> "edit_popup_delete",
//    "params"	=> array(
//        array(
//            "type" => "dropdown",
//            "heading" => __("Button layout", "js_composer"),
//            "param_name" => "type",
//            "value" => array(__("Horizontal", "js_composer") => "", __("Vertical", "js_composer") => "vertical", __("No count", "js_composer") => "none"),
//            "description" => __("Select button type.", "js_composer")
//        )
//    )
//) );

/* Toggle (FAQ)
---------------------------------------------------------- */
WPBMap::map( 'vc_toggle', array(
    "name"		=> __("Toggle", "js_composer"),
    "base"		=> "vc_toggle",
    "class"		=> "wpb_vc_faq",
	"icon"		=> "icon-wpb-toggle-small-expand",
    "params"	=> array(
        array(
            "type" => "textfield",
            "holder" => "h4",
            "class" => "toggle_title",
            "heading" => __("Toggle title", "js_composer"),
            "param_name" => "title",
            "value" => __("Toggle title", "js_composer"),
            "description" => __("Toggle block title.", "js_composer")
        ),
        array(
            "type" => "textarea_html",
            "holder" => "div",
            "class" => "toggle_content",
            "heading" => __("Toggle content", "js_composer"),
            "param_name" => "content",
            "value" => __("<p>Toggle content goes here, click the edit button.</p>", "js_composer"),
            "description" => __("Toggle block content.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Default state", "js_composer"),
            "param_name" => "open",
            "value" => array(__("Closed", "js_composer") => "false", __("Open", "js_composer") => "true"),
            "description" => __("Select this if you want toggle to be open by default.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    )
) );

/* Single image */
WPBMap::map( 'vc_single_image', array(
	"name"		=> __("Single image", "js_composer"),
	"base"		=> "vc_single_image",
	"class"		=> "wpb_vc_single_image_widget",
	"icon"		=> "icon-wpb-single-image",
    "params"	=> array(
		array(
			"type" => "attach_image",
			"heading" => __("Image", "js_composer"),
			"param_name" => "image",
			"value" => "",
			"description" => ""
		),
		array(
		    "type" => "dropdown",
		    "heading" => __("Image Size", "js_composer"),
		    "param_name" => "image_size",
		    "value" => array(__("Full", "js_composer") => "full", __("Large", "js_composer") => "large", __("Medium", "js_composer") => "medium", __("Thumbnail", "js_composer") => "thumbnail"),
		    "description" => __("Select the source size for the image (NOTE: this doesn't affect it's size on the front-end, only the quality).", "js_composer")
		),
		array(
		    "type" => "dropdown",
		    "heading" => __("Image Frame", "js_composer"),
		    "param_name" => "frame",
		    "value" => array(__("No Frame", "js_composer") => "noframe", __("Border Frame", "js_composer") => "borderframe", __("Glow Frame", "js_composer") => "glowframe", __("Shadow Frame", "js_composer") => "shadowframe"),
		    "description" => __("Select a frame for the image.", "js_composer")
		),
		array(
		    "type" => "dropdown",
		    "heading" => __("Full width", "js_composer"),
		    "param_name" => "full_width",
		    "value" => array(__("No", "js_composer") => "no", __("Yes", "js_composer") => "yes"),
		    "description" => __("Select if you want the image to be the full width of the page. (Make sure the element width is 1/1 too).", "js_composer")
		),
		array(
		    "type" => "dropdown",
		    "heading" => __("Enable lightbox link", "js_composer"),
		    "param_name" => "lightbox",
		    "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
		    "description" => __("Select if you want the image to open in a lightbox on click", "js_composer")
		),
		array(
		    "type" => "textfield",
		    "heading" => __("Add link to image", "js_composer"),
		    "param_name" => "image_link",
		    "value" => "",
		    "description" => __("If you would like the image to link to a URL, then enter it here. NOTE: this will override the lightbox functionality if you have enabled it.", "js_composer")
		),
		array(
		    "type" => "dropdown",
		    "heading" => __("Link opens in new window?", "js_composer"),
		    "param_name" => "link_target",
		    "value" => array(__("Self", "js_composer") => "_self", __("New Window", "js_composer") => "_blank"),
		    "description" => __("Select if you want the link to open in a new window", "js_composer")
		),
		array(
		    "type" => "dropdown",
		    "heading" => __("Show bottom shadow", "js_composer"),
		    "param_name" => "shadow",
		    "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
		    "description" => __("Show a shadow below the asset.", "js_composer")
		)
    )
));

// Gallery/Slideshow
//---------------------------------------------------------- 
//WPBMap::map( 'vc_gallery', array(
//    "name"		=> __("Image gallery", "js_composer"),
//    "base"		=> "vc_gallery",
//    "class"		=> "wpb_vc_gallery_widget",
//	"icon"		=> "icon-wpb-images-stack",
//    "params"	=> array(
//        array(
//            "type" => "textfield",
//            "heading" => __("Widget title", "js_composer"),
//            "param_name" => "title",
//            "value" => "",
//            "description" => __("What text use as widget title. Leave blank if no title is needed.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Gallery type", "js_composer"),
//            "param_name" => "type",
//            "value" => array(__("Flex slider fade", "js_composer") => "flexslider_fade", __("Flex slider slide", "js_composer") => "flexslider_slide", __("Nivo slider", "js_composer") => "nivo", __("Image grid", "js_composer") => "image_grid"),
//            "description" => __("Select gallery type. Note: Nivo slider is not fully responsive.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Auto rotate slides", "js_composer"),
//            "param_name" => "interval",
//            "value" => array(3, 5, 10, 15, 0),
//            "description" => __("Auto rotate slides each X seconds. Select 0 to disable.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("On click", "js_composer"),
//            "param_name" => "onclick",
//            "value" => array(__("Open prettyPhoto", "js_composer") => "link_image", __("Do nothing", "js_composer") => "link_no", __("Open custom link", "js_composer") => "custom_link"),
//            "description" => __("What to do when slide is clicked?.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Image size", "js_composer"),
//            "param_name" => "img_size",
//            "value" => "",
//            "description" => __("Enter image size. Example: thumbnail, medium, large, full or other sizes defined by current theme. Alternatively enter image size in pixels: 200x100 (Width x Height). Leave empty to use 'thumbnail' size.", "js_composer")
//        ),
//        array(
//            "type" => "attach_images",
//            "heading" => __("Images", "js_composer"),
//            "param_name" => "images",
//            "value" => "",
//            "description" => ""
//        ),
//        array(
//            "type" => "exploded_textarea",
//            "heading" => __("Custom links", "js_composer"),
//            "param_name" => "custom_links",
//            "description" => __('Select "Open custom link" in "On click" parameter and then enter links for each slide here. Divide links with linebreaks (Enter).', 'js_composer')
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Extra class name", "js_composer"),
//            "param_name" => "el_class",
//            "value" => "",
//            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
//        )
//    )
//) );


/* Tabs
   This one is an advanced example. It has javascript
   callbacks in it. So basically in your theme you can do
   whatever you want. More detailed documentation located
   in the advanced documentation folder.
---------------------------------------------------------- */
WPBMap::map( 'vc_tabs', array(
    "name"		=> __("Tabs", "js_composer"),
    "base"		=> "vc_tabs",
    "controls"	=> "full",
    "class"		=> "wpb_tabs",
	"icon"		=> "icon-wpb-ui-tab-content",
    "params"	=> array(
        array(
            "type" => "textfield",
            "heading" => __("Widget title", "js_composer"),
            "param_name" => "tab_asset_title",
            "value" => "",
            "description" => __("What text use as widget title. Leave blank if no title is needed.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Tabs type", "js_composer"),
            "param_name" => "type",
            "value" => array(__('Standard', "js_composer") => "standard", __('Minimal', "js_composer") => "minimal"),
            "description" => __("Select tabs type.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    ),
    "custom_markup" => '
	<div class="tab_controls">
		<button class="add_tab">'.__("Add tab", "js_composer").'</button>
		<button class="edit_tab">'.__("Edit current tab title", "js_composer").'</button>
		<button class="delete_tab">'.__("Delete current tab", "js_composer").'</button>
	</div>

	<div class="wpb_tabs_holder">
		%content%
	</div>',
    'default_content' => '
	<ul>
		<li><a href="#tab-1"><span>'.__('Tab 1', 'js_composer').'</span></a></li>
		<li><a href="#tab-2"><span>'.__('Tab 2', 'js_composer').'</span></a></li>
	</ul>

	<div id="tab-1" class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit">
		[vc_column_text width="1/1"] '.__('I am text block. click the edit button to change this text.', 'js_composer').' [/vc_column_text]
	</div>

	<div id="tab-2" class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit">
		[vc_column_text width="1/1"] '.__('I am text block. click the edit button to change this text.', 'js_composer').' [/vc_column_text]
	</div>',
    "js_callback" => array("init" => "wpbTabsInitCallBack", "shortcode" => "wpbTabsGenerateShortcodeCallBack")
    //"js_callback" => array("init" => "wpbTabsInitCallBack", "edit" => "wpbTabsEditCallBack", "save" => "wpbTabsSaveCallBack", "shortcode" => "wpbTabsGenerateShortcodeCallBack")
) );

// Tour section
//---------------------------------------------------------- 
//WPBMap::map( 'vc_tour', array(
//    "name"		=> __("Tour section", "js_composer"),
//    "base"		=> "vc_tour",
//    "controls"	=> "full",
//    "class"		=> "wpb_tour",
//	"icon"		=> "icon-wpb-ui-tab-content-vertical",
//    "wrapper_class" => "clearfix",
//    "params"	=> array(
//        array(
//            "type" => "textfield",
//            "heading" => __("Widget title", "js_composer"),
//            "param_name" => "title",
//            "value" => "",
//            "description" => __("What text use as widget title. Leave blank if no title is needed.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Auto rotate slides", "js_composer"),
//            "param_name" => "interval",
//            "value" => array(0, 3, 5, 10, 15),
//            "description" => __("Auto rotate slides each X seconds. Select 0 to disable.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Extra class name", "js_composer"),
//            "param_name" => "el_class",
//            "value" => "",
//            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
//        )
//    ),
//    "custom_markup" => '
//	<div class="tab_controls">
//		<button class="add_tab">'.__("Add slide", "js_composer").'</button>
//		<button class="edit_tab">'.__("Edit current slide title", "js_composer").'</button>
//		<button class="delete_tab">'.__("Delete current slide", "js_composer").'</button>
//	</div>
//
//	<div class="wpb_tabs_holder clearfix">
//		%content%
//	</div>',
//    'default_content' => '
//	<ul>
//		<li><a href="#tab-1"><span>'.__('Slide 1', 'js_composer').'</span></a></li>
//		<li><a href="#tab-2"><span>'.__('Slide 2', 'js_composer').'</span></a></li>
//	</ul>
//
//	<div id="tab-1" class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit">
//		[vc_column_text width="1/1"] '.__('I am text block. click the edit button to change this text.', 'js_composer').' [/vc_column_text]
//	</div>
//
//	<div id="tab-2" class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit">
//		[vc_column_text width="1/1"] '.__('I am text block. click the edit button to change this text.', 'js_composer').' [/vc_column_text]
//	</div>',
//    "js_callback" => array("init" => "wpbTabsInitCallBack", "shortcode" => "wpbTabsGenerateShortcodeCallBack")
//) );

/* Accordion section
---------------------------------------------------------- */
WPBMap::map( 'vc_accordion', array(
    "name"		=> __("Accordion section", "js_composer"),
    "base"		=> "vc_accordion",
    "controls"	=> "full",
    "class"		=> "wpb_accordion",
	"icon"		=> "icon-wpb-ui-accordion",
//	"wrapper_class" => "clearfix",
    "params"	=> array(
        array(
            "type" => "textfield",
            "heading" => __("Widget title", "js_composer"),
            "param_name" => "widget_title",
            "value" => "",
            "description" => __("What text use as widget title. Leave blank if no title is needed.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Accordion type", "js_composer"),
            "param_name" => "type",
            "value" => array(__('Standard', "js_composer") => "standard", __('Minimal', "js_composer") => "minimal"),
            "description" => __("Select the type of accordion you'd like to show.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    ),
    "custom_markup" => '
	<div class="tab_controls">
		<button class="add_tab">'.__("Add section", "js_composer").'</button>
		<button class="edit_tab">'.__("Edit current section title", "js_composer").'</button>
		<button class="delete_tab">'.__("Delete current section", "js_composer").'</button>
	</div>

	<div class="wpb_accordion_holder clearfix">
		%content%
	</div>',
    'default_content' => '
	<div class="group">
		<h3><a href="#">'.__('Section 1', 'js_composer').'</a></h3>
		<div>
			<div class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit">
				[vc_column_text width="1/1"] '.__('I am text block. click the edit button to change this text.', 'js_composer').' [/vc_column_text]
			</div>
		</div>
	</div>
	<div class="group">
		<h3><a href="#">'.__('Section 2', 'js_composer').'</a></h3>
		<div>
			<div class="row-fluid wpb_column_container wpb_sortable_container not-column-inherit">
				[vc_column_text width="1/1"] '.__('I am text block. click the edit button to change this text.', 'js_composer').' [/vc_column_text]
			</div>
		</div>
	</div>',
    "js_callback" => array("init" => "wpbAccordionInitCallBack", "shortcode" => "wpbAccordionGenerateShortcodeCallBack")
) );

// Teaser grid
//---------------------------------------------------------- 
//WPBMap::map( 'vc_teaser_grid', array(
//    "name"		=> __("Teaser (posts) grid", "js_composer"),
//    "base"		=> "vc_teaser_grid",
//    "class"		=> "wpb_vc_teaser_grid_widget",
//	"icon"		=> "icon-wpb-application-icon-large",
//    "params"	=> array(
//        array(
//            "type" => "textfield",
//            "heading" => __("Widget title", "js_composer"),
//            "param_name" => "title",
//            "value" => "",
//            "description" => __("Heading text. Leave it empty if not needed.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Columns count", "js_composer"),
//            "param_name" => "grid_columns_count",
//            "value" => array(4, 3, 2, 1),
//            "description" => __("Select columns count.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Teaser count", "js_composer"),
//            "param_name" => "grid_teasers_count",
//            "value" => "",
//            "description" => __('How many teasers to show? Enter number or "All".', "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Content", "js_composer"),
//            "param_name" => "grid_content",
//            "value" => array(__("Teaser (Excerpt)", "js_composer") => "teaser", __("Full Content", "js_composer") => "content"),
//            "description" => __("Teaser layout template.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Layout", "js_composer"),
//            "param_name" => "grid_layout",
//            "value" => array(__("Title + Thumbnail + Text", "js_composer") => "title_thumbnail_text", __("Thumbnail + Title + Text", "js_composer") => "thumbnail_title_text", __("Thumbnail + Text", "js_composer") => "thumbnail_text", __("Thumbnail + Title", "js_composer") => "thumbnail_title", __("Thumbnail only", "js_composer") => "thumbnail", __("Title + Text", "js_composer") => "title_text"),
//            "description" => __("Teaser layout.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Link", "js_composer"),
//            "param_name" => "grid_link",
//            "value" => array(__("Link to post", "js_composer") => "link_post", __("Link to bigger image", "js_composer") => "link_image", __("Thumbnail to bigger image, title to post", "js_composer") => "link_image_post", __("No link", "js_composer") => "link_no"),
//            "description" => __("Link type.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Template", "js_composer"),
//            "param_name" => "grid_template",
//            "value" => array(__("Grid", "js_composer") => "grid", __("Carousel", "js_composer") => "carousel"),
//            "description" => __("Teaser layout template.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Thumbnail size", "js_composer"),
//            "param_name" => "grid_thumb_size",
//            "value" => "",
//            "description" => __('Enter thumbnail size. Example: thumbnail, medium, large, full or other sizes defined by current theme. Alternatively enter image size in pixels: 200x100 (Width x Height).', "js_composer")
//        ),
//        array(
//            "type" => "posttypes",
//            "heading" => __("Post types", "js_composer"),
//            "param_name" => "grid_posttypes",
//            "description" => __("Select post types to populate posts from.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Post/Page IDs", "js_composer"),
//            "param_name" => "posts_in",
//            "value" => "",
//            "description" => __('Fill this field with page/posts IDs separated by commas (,) to retrieve only them. Use this in conjunction with "Post types" field.', "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Exclude Post/Page IDs", "js_composer"),
//            "param_name" => "posts_not_in",
//            "value" => "",
//            "description" => __('Fill this field with page/posts IDs separated by commas (,) to exclude them from query.', "js_composer")
//        ),
//        array(
//            "type" => "exploded_textarea",
//            "heading" => __("Categories", "js_composer"),
//            "param_name" => "grid_categories",
//            "description" => __("If you want to narrow output, enter category names here. Note: Only listed categories will be included. Divide categories with linebreaks (Enter).", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Order by", "js_composer"),
//            "param_name" => "orderby",
//            "value" => array( "", __("Date", "js_composer") => "date", __("ID", "js_composer") => "ID", __("Author", "js_composer") => "author", __("Title", "js_composer") => "title", __("Modified", "js_composer") => "modified", __("Random", "js_composer") => "rand", __("Comment count", "js_composer") => "comment_count", __("Menu order", "js_composer") => "menu_order" ),
//            "description" => __('Select how to sort retrieved posts. More at <a href="http://codex.wordpress.org/Class_Reference/WP_Query#Order_.26_Orderby_Parameters" target="_blank">WordPress codex page</a>.', 'js_composer')
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Order by", "js_composer"),
//            "param_name" => "order",
//            "value" => array( __("Descending", "js_composer") => "DESC", __("Ascending", "js_composer") => "ASC" ),
//            "description" => __('Designates the ascending or descending order. More at <a href="http://codex.wordpress.org/Class_Reference/WP_Query#Order_.26_Orderby_Parameters" target="_blank">WordPress codex page</a>.', 'js_composer')
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Extra class name", "js_composer"),
//            "param_name" => "el_class",
//            "value" => "",
//            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
//        )
//    )
//) );

// Teaser grid
//---------------------------------------------------------- 
//WPBMap::map( 'vc_posts_slider', array(
//    "name"		=> __("Posts slider", "js_composer"),
//    "base"		=> "vc_posts_slider",
//    "class"		=> "wpb_vc_posts_slider_widget",
//	"icon"		=> "icon-wpb-slideshow",
//    "params"	=> array(
//        array(
//            "type" => "textfield",
//            "heading" => __("Widget title", "js_composer"),
//            "param_name" => "title",
//            "value" => "",
//            "description" => __("Heading text. Leave it empty if not needed.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Slider type", "js_composer"),
//            "param_name" => "type",
//            "value" => array(__("Flex slider fade", "js_composer") => "flexslider_fade", __("Flex slider slide", "js_composer") => "flexslider_slide", __("Nivo slider", "js_composer") => "nivo"),
//            "description" => __("Select slider type. Note: Nivo slider is not fully responsive.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Slides count", "js_composer"),
//            "param_name" => "count",
//            "value" => "",
//            "description" => __('How many slides to show? Enter number or "All".', "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Auto rotate slides", "js_composer"),
//            "param_name" => "interval",
//            "value" => array(3, 5, 10, 15, 0),
//            "description" => __("Auto rotate slides each X seconds. Select 0 to disable.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Description", "js_composer"),
//            "param_name" => "slides_content",
//            "value" => array(__("No description", "js_composer") => "", __("Teaser (Excerpt)", "js_composer") => "teaser" ),
//            "description" => __("Some sliders support description text, what content use for it?", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Link", "js_composer"),
//            "param_name" => "link",
//            "value" => array(__("Link to post", "js_composer") => "link_post", __("Link to bigger image", "js_composer") => "link_image", __("Open custom link", "js_composer") => "custom_link", __("No link", "js_composer") => "link_no"),
//            "description" => __("Link type.", "js_composer")
//        ),
//        array(
//            "type" => "exploded_textarea",
//            "heading" => __("Custom links", "js_composer"),
//            "param_name" => "custom_links",
//            "description" => __('Select "Open custom link" in "Link" parameter and then enter links for each slide here. Divide links with linebreaks (Enter).', 'js_composer')
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Thumbnail size", "js_composer"),
//            "param_name" => "thumb_size",
//            "value" => "",
//            "description" => __('Enter thumbnail size. Example: thumbnail, medium, large, full or other sizes defined by current theme. Alternatively enter image size in pixels: 200x100 (Width x Height).', "js_composer")
//        ),
//        array(
//            "type" => "posttypes",
//            "heading" => __("Post types", "js_composer"),
//            "param_name" => "posttypes",
//            "description" => __("Select post types to populate posts from.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Post/Page IDs", "js_composer"),
//            "param_name" => "posts_in",
//            "value" => "",
//            "description" => __('Fill this field with page/posts IDs separated by commas (,), to retrieve only them. Use this in conjunction with "Post types" field.', "js_composer")
//        ),
//        array(
//            "type" => "exploded_textarea",
//            "heading" => __("Categories", "js_composer"),
//            "param_name" => "categories",
//            "description" => __("If you want to narrow output, enter category names here. Note: Only listed categories will be included. Divide categories with linebreaks (Enter).", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Order by", "js_composer"),
//            "param_name" => "orderby",
//            "value" => array( "", __("Date", "js_composer") => "date", __("ID", "js_composer") => "ID", __("Author", "js_composer") => "author", __("Title", "js_composer") => "title", __("Modified", "js_composer") => "modified", __("Random", "js_composer") => "rand", __("Comment count", "js_composer") => "comment_count", __("Menu order", "js_composer") => "menu_order" ),
//            "description" => __('Select how to sort retrieved posts. More at <a href="http://codex.wordpress.org/Class_Reference/WP_Query#Order_.26_Orderby_Parameters" target="_blank">WordPress codex page</a>.', 'js_composer')
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Order by", "js_composer"),
//            "param_name" => "order",
//            "value" => array( __("Descending", "js_composer") => "DESC", __("Ascending", "js_composer") => "ASC" ),
//            "description" => __('Designates the ascending or descending order. More at <a href="http://codex.wordpress.org/Class_Reference/WP_Query#Order_.26_Orderby_Parameters" target="_blank">WordPress codex page</a>.', 'js_composer')
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Extra class name", "js_composer"),
//            "param_name" => "el_class",
//            "value" => "",
//            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
//        )
//    )
//) );


/* Button
---------------------------------------------------------- */
$icons_arr = array(
    __("None", "js_composer") => "none",
    __("Address book icon", "js_composer") => "wpb_address_book",
    __("Alarm clock icon", "js_composer") => "wpb_alarm_clock",
    __("Anchor icon", "js_composer") => "wpb_anchor",
    __("Application Image icon", "js_composer") => "wpb_application_image",
    __("Arrow icon", "js_composer") => "wpb_arrow",
    __("Asterisk icon", "js_composer") => "wpb_asterisk",
    __("Hammer icon", "js_composer") => "wpb_hammer",
    __("Balloon icon", "js_composer") => "wpb_balloon",
    __("Balloon Buzz icon", "js_composer") => "wpb_balloon_buzz",
    __("Balloon Facebook icon", "js_composer") => "wpb_balloon_facebook",
    __("Balloon Twitter icon", "js_composer") => "wpb_balloon_twitter",
    __("Battery icon", "js_composer") => "wpb_battery",
    __("Binocular icon", "js_composer") => "wpb_binocular",
    __("Document Excel icon", "js_composer") => "wpb_document_excel",
    __("Document Image icon", "js_composer") => "wpb_document_image",
    __("Document Music icon", "js_composer") => "wpb_document_music",
    __("Document Office icon", "js_composer") => "wpb_document_office",
    __("Document PDF icon", "js_composer") => "wpb_document_pdf",
    __("Document Powerpoint icon", "js_composer") => "wpb_document_powerpoint",
    __("Document Word icon", "js_composer") => "wpb_document_word",
    __("Bookmark icon", "js_composer") => "wpb_bookmark",
    __("Camcorder icon", "js_composer") => "wpb_camcorder",
    __("Camera icon", "js_composer") => "wpb_camera",
    __("Chart icon", "js_composer") => "wpb_chart",
    __("Chart pie icon", "js_composer") => "wpb_chart_pie",
    __("Clock icon", "js_composer") => "wpb_clock",
    __("Fire icon", "js_composer") => "wpb_fire",
    __("Heart icon", "js_composer") => "wpb_heart",
    __("Mail icon", "js_composer") => "wpb_mail",
    __("Play icon", "js_composer") => "wpb_play",
    __("Shield icon", "js_composer") => "wpb_shield",
    __("Video icon", "js_composer") => "wpb_video"
);

//$colors_arr = array(__("Grey", "js_composer") => "button_grey", __("Yellow", "js_composer") => "button_yellow", __("Green", "js_composer") => "button_green", __("Blue", "js_composer") => "button_blue", __("Red", "js_composer") => "button_red", __("Orange", "js_composer") => "button_orange");
$colors_arr = array(__("Accent", "js_composer") => "accent", __("Blue", "js_composer") => "blue", __("Grey", "js_composer") => "grey", __("Light grey", "js_composer") => "lightgrey", __("Purple", "js_composer") => "purple", __("Light Blue", "js_composer") => "lightblue", __("Green", "js_composer") => "green", __("Lime Green", "js_composer") => "limegreen", __("Turquoise", "js_composer") => "turquoise", __("Pink", "js_composer") => "pink", __("Orange", "js_composer") => "orange");

$size_arr = array(__("Small", "js_composer") => "small", __("Medium", "js_composer") => "medium", __("Large", "js_composer") => "large");

$type_arr = array(__("Standard", "js_composer") => "standard", __("Square with arrow", "js_composer") => "squarearrow", __("Slightly rounded", "js_composer") => "slightlyrounded", __("Slightly rounded with arrow", "js_composer") => "slightlyroundedarrow", __("Rounded", "js_composer") => "rounded", __("Rounded with arrow", "js_composer") => "roundedarrow", __("Outer glow effect", "js_composer") => "outerglow", __("Drop shadow effect", "js_composer") => "dropshadow");


$target_arr = array(__("Same window", "js_composer") => "_self", __("New window", "js_composer") => "_blank");

//WPBMap::map( 'vc_button', array(
//    "name"		=> __("Button", "js_composer"),
//    "base"		=> "vc_button",
//    "class"		=> "wpb_vc_button wpb_controls_top_right",
//	"icon"		=> "icon-wpb-ui-button",
//    "controls"	=> "edit_popup_delete",
//    "params"	=> array(
//        array(
//            "type" => "textfield",
//            "heading" => __("Text on the button", "js_composer"),
//            "holder" => "button",
//            "class" => "btn",
//            "param_name" => "title",
//            "value" => __("Text on the button", "js_composer"),
//            "description" => __("Text on the button.", "js_composer")
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("URL (Link)", "js_composer"),
//            "param_name" => "href",
//            "value" => "",
//            "description" => __("Button link.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Color", "js_composer"),
//            "param_name" => "color",
//            "value" => $colors_arr,
//            "description" => __("Button color.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Size", "js_composer"),
//            "param_name" => "size",
//            "value" => $size_arr,
//            "description" => __("Button size.", "js_composer")
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Type", "js_composer"),
//            "param_name" => "type",
//            "value" => $type_arr
//        ),
//        array(
//            "type" => "dropdown",
//            "heading" => __("Target", "js_composer"),
//            "param_name" => "target",
//            "value" => $target_arr
//        ),
//        array(
//            "type" => "textfield",
//            "heading" => __("Extra class name", "js_composer"),
//            "param_name" => "el_class",
//            "value" => "",
//            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
//        )
//    ),
//    "js_callback" => array("init" => "wpbButtonInitCallBack", "save" => "wpbButtonSaveCallBack")
    //"js_callback" => array("init" => "wpbCallToActionInitCallBack", "shortcode" => "wpbCallToActionShortcodeCallBack")
//) );

WPBMap::map( 'impact_text', array(
    "name"		=> __("Impact Text + Button", "js_composer"),
    "base"		=> "impact_text",
    "class"		=> "button_grey",
	"icon"		=> "icon-wpb-impact-text",
    "controls"	=> "edit_popup_delete",
    "params"	=> array(
    	array(
    	    "type" => "dropdown",
    	    "heading" => __("Include button", "js_composer"),
    	    "param_name" => "include_button",
    	    "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
    	    "description" => __("Include a button in the asset.", "js_composer")
    	),
        array(
            "type" => "textfield",
            "heading" => __("Text on the button", "js_composer"),
            "param_name" => "title",
            "value" => __("Text on the button", "js_composer"),
            "description" => __("Text on the button.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("URL (Link)", "js_composer"),
            "param_name" => "href",
            "value" => "",
            "description" => __("Button link.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Color", "js_composer"),
            "param_name" => "color",
            "value" => $colors_arr,
            "description" => __("Button color.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Size", "js_composer"),
            "param_name" => "size",
            "value" => $size_arr,
            "description" => __("Button size.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Type", "js_composer"),
            "param_name" => "type",
            "value" => $type_arr
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Target", "js_composer"),
            "param_name" => "target",
            "value" => $target_arr
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Button position", "js_composer"),
            "param_name" => "position",
            "value" => array(__("Align right", "js_composer") => "cta_align_right", __("Align left", "js_composer") => "cta_align_left", __("Align bottom", "js_composer") => "cta_align_bottom"),
            "description" => __("Select button alignment.", "js_composer")
        ),
        array(
            "type" => "textarea_html",
            "holder" => "div",
            "class" => "",
            "heading" => __("Text", "js_composer"),
            "param_name" => "content",
            "value" => __("click the edit button to change this text.", "js_composer"),
            "description" => __("Enter your content.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Include top border", "js_composer"),
            "param_name" => "border_top",
            "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
            "description" => __("Include a top border to the impact text.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Include bottom border", "js_composer"),
            "param_name" => "border_bottom",
            "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
            "description" => __("Include a bottom border to the impact text.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Show bottom shadow", "js_composer"),
            "param_name" => "shadow",
            "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
            "description" => __("Show a shadow below the asset (this will override the border).", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    ),
    "js_callback" => array("init" => "wpbCallToActionInitCallBack", "save" => "wpbCallToActionSaveCallBack")
) );

/* Video element
---------------------------------------------------------- */
WPBMap::map( 'vc_video', array(
    "name"		=> __("Video player", "js_composer"),
    "base"		=> "vc_video",
    "class"		=> "",
	"icon"		=> "icon-wpb-film-youtube",
    "params"	=> array(
        array(
            "type" => "textfield",
            "heading" => __("Widget title", "js_composer"),
            "param_name" => "title",
            "value" => "",
            "description" => __("Heading text. Leave it empty if not needed.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Video link", "js_composer"),
            "param_name" => "link",
            "value" => "",
            "description" => __('Link to the video. More about supported formats at <a href="http://codex.wordpress.org/Embeds#Okay.2C_So_What_Sites_Can_I_Embed_From.3F" target="_blank">WordPress codex page</a>.', "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Video size", "js_composer"),
            "param_name" => "size",
            "value" => "",
            "description" => __('Enter video size in pixels. Example: 200x100 (Width x Height).', "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Show bottom shadow", "js_composer"),
            "param_name" => "shadow",
            "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
            "description" => __("Show a shadow below the asset.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    )
) );

/* Google maps element
---------------------------------------------------------- */
WPBMap::map( 'vc_gmaps',  array(
    "name"		=> __("Google maps", "js_composer"),
    "base"		=> "vc_gmaps",
    "class"		=> "",
	"icon"		=> "icon-wpb-map-pin",
    "params"	=> array(
        array(
            "type" => "textfield",
            "heading" => __("Widget title", "js_composer"),
            "param_name" => "title",
            "value" => "",
            "description" => __("Heading text. Leave it empty if not needed.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Address", "js_composer"),
            "param_name" => "address",
            "value" => "",
            "description" => __('Enter the address that you would like to show on the map here, i.e. "Cupertino".', "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Map height", "js_composer"),
            "param_name" => "size",
            "value" => "300",
            "description" => __('Enter map height in pixels. Example: 300).', "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Map type", "js_composer"),
            "param_name" => "type",
            "value" => array(__("Map", "js_composer") => "ROADMAP", __("Satellite", "js_composer") => "SATELLITE", __("Hybrid", "js_composer") => "HYBRID", __("Terrain", "js_composer") => "TERRAIN"),
            "description" => __("Select button alignment.", "js_composer")
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Map Zoom", "js_composer"),
            "param_name" => "zoom",
            "value" => array(__("14 - Default", "js_composer") => 14, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20)
        ),
        array(
        	"type" => "attach_image",
        	"heading" => __("Custom Map Pin", "js_composer"),
        	"param_name" => "pin_image",
        	"value" => "",
        	"description" => "Choose an image to use as the custom pin for the address on the map. Upload your custom map pin, the image size must be 150px x 75px."
        ),
        array(
            "type" => "dropdown",
            "heading" => __("Show bottom shadow", "js_composer"),
            "param_name" => "shadow",
            "value" => array(__("Yes", "js_composer") => "yes", __("No", "js_composer") => "no"),
            "description" => __("Show a shadow below the asset.", "js_composer")
        ),
        array(
            "type" => "textfield",
            "heading" => __("Extra class name", "js_composer"),
            "param_name" => "el_class",
            "value" => "",
            "description" => __("If you wish to style particular content element differently, then use this field to add a class name and then refer to it in your css file.", "js_composer")
        )
    )
) );

WPBMap::map( 'vc_raw_html', array(
	"name"		=> __("Raw html", "js_composer"),
	"base"		=> "vc_raw_html",
	"class"		=> "div",
	"icon"      => "icon-wpb-raw-html",
	"wrapper_class" => "clearfix",
	"controls"	=> "full",
	"params"	=> array(
		array(
			"type" => "textarea_raw_html",
			"holder" => "div",
			"class" => "",
			"heading" => __("Raw HTML", "js_composer"),
			"param_name" => "content",
			"value" => base64_encode("<p>I am raw html block.<br/>click the edit button to change this html</p>"),
			"description" => __("Enter your HTML content.", "js_composer")
		),
	)
) );

WPBMap::map( 'vc_raw_js', array(
	"name"		=> __("Raw js", "js_composer"),
	"base"		=> "vc_raw_js",
	"class"		=> "div",
	"icon"      => "icon-wpb-raw-javascript",
	"wrapper_class" => "clearfix",
	"controls"	=> "full",
	"params"	=> array(
		array(
			"type" => "textarea_raw_html",
			"holder" => "div",
			"class" => "",
			"heading" => __("Raw js", "js_composer"),
			"param_name" => "content",
			"value" => __(base64_encode("alert('Enter your js here!');"), "js_composer"),
			"description" => __("Enter your Js.", "js_composer")
		),
	)
) );

WPBMap::layout(array('id'=>'column_12', 'title'=>'1/2'));
WPBMap::layout(array('id'=>'column_12-12', 'title'=>'1/2 + 1/2'));
WPBMap::layout(array('id'=>'column_13', 'title'=>'1/3'));
WPBMap::layout(array('id'=>'column_13-13-13', 'title'=>'1/3 + 1/3 + 1/3'));
WPBMap::layout(array('id'=>'column_13-23', 'title'=>'1/3 + 2/3'));
WPBMap::layout(array('id'=>'column_23-13', 'title'=>'2/3 + 1/3'));
WPBMap::layout(array('id'=>'column_14', 'title'=>'1/4'));
WPBMap::layout(array('id'=>'column_12-14-14', 'title'=>'1/2 + 1/4 + 1/4'));
WPBMap::layout(array('id'=>'column_14-12-14', 'title'=>'1/4 + 1/2 + 1/4'));
WPBMap::layout(array('id'=>'column_14-14-12', 'title'=>'1/4 + 1/4 + 1/2'));
WPBMap::layout(array('id'=>'column_14-14-14-14', 'title'=>'1/4 + 1/4 + 1/4 + 1/4'));
WPBMap::layout(array('id'=>'column_11', 'title'=>'1/1'));