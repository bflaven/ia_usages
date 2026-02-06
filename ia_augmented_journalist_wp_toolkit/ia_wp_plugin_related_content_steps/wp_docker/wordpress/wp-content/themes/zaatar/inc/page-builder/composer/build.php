<?php
/**
 * Swift Page Builder build plugin
 *
 * @package SwiftPageBuilder
 *
 */


if (!defined('ABSPATH')) die('-1');

class SwiftPageBuilderSetup extends SwiftPageBuilderAbstract {
    public static $version = '1.0';
    protected $composer;

    public function __construct() {
    }

    public function init($settings) {
        parent::init($settings);

        $this->composer = SwiftPageBuilder::getInstance();

        $this->composer->createColumnShortCode(); // Refactored
				
        $this->composer->setTheme();
        $this->setUpTheme();

        if ( function_exists( 'add_theme_support' ) ) {
            add_theme_support( 'post-thumbnails', array( 'page' ) );
        }

        load_plugin_textdomain( 'js_composer', false, self::$config['APP_ROOT'] . '/locale/' );
        add_post_type_support( 'page', 'excerpt' );
    }

    public function setUpPlugin() {
        register_activation_hook( __FILE__, Array( $this, 'activate' ) );
        if (!is_admin()) {
            $this->addAction('template_redirect', 'frontCss');
            $this->addAction('template_redirect', 'frontJsRegister');
            $this->addAction('wp_enqueue_scripts', 'frontendJsLoad');
            $this->addFilter('the_content', 'fixPContent', 10000);
        }
    }

    public function fixPContent($content = null) {
        //$content = preg_replace( '#^<\/p>|^<br \/>|<p>$#', '', $content );
        $s = array("<p><div class=\"row-fluid\"", "</div></p>");
        $r = array("<div class=\"row-fluid\"", "</div>");
        $content = str_ireplace($s, $r, $content);
        return $content;
    }
    public function frontendJsLoad() {
        wp_enqueue_script( 'jquery' );
        wp_enqueue_script( 'wpb_composer_front_js' );
    }

    public function frontCss() {
        wp_register_style( 'bootstrap', $this->assetURL( 'bootstrap/css/bootstrap.css' ), false, SPB_VERSION, 'screen' );
        wp_register_style( 'ui-custom-theme', $this->assetURL( 'ui-custom-theme/jquery-ui-' . SPB_JQUERY_UI_VERSION . '.custom.css' ), false, SPB_VERSION, 'screen');
        //wp_register_style( 'flexslider', $this->assetURL( 'js/flexslider/flexslider.css' ), false, SPB_VERSION, 'screen' );

        wp_register_style( 'prettyphoto', $this->assetURL( 'js/prettyphoto/css/prettyPhoto.css' ), false, SPB_VERSION, 'screen' );

        wp_register_style( 'js_composer_front', $this->assetURL( 'js_composer_front.css' ), false, SPB_VERSION, 'screen' );

        wp_enqueue_style( 'bootstrap' );
        wp_enqueue_style( 'js_composer_front' );
    }

    public function frontJsRegister() {
        wp_register_script( 'wpb_composer_front_js', $this->assetURL( 'js_composer_front.js' ), array( 'jquery' ));

        wp_register_script( 'tweet', $this->assetURL( 'js/jquery.tweet.js' ), array( 'jquery' ));
        wp_register_script( 'isotope', $this->assetURL( 'js/jquery.isotope.min.js' ), array( 'jquery' ));
        wp_register_script( 'jcarousellite', $this->assetURL( 'js/jcarousellite_1.0.1.min.js' ), array( 'jquery' ));

        //wp_register_script( 'cycle', $this->assetURL( 'js/jquery.cycle.all.js' ), array( 'jquery' ));
        wp_register_script( 'nivo-slider', $this->assetURL( 'js/jquery.nivo.slider.pack.js' ), array( 'jquery' ));
        //wp_register_script( 'flexslider', $this->assetURL( 'js/flexslider/jquery.flexslider-min.js' ), array( 'jquery' ));
        wp_register_script( 'prettyphoto', $this->assetURL( 'js/prettyphoto/js/jquery.prettyPhoto.js' ), array( 'jquery' ));

        //wp_register_script( 'jcarousellite', $this->assetURL( 'js/jcarousellite_1.0.1.min.js' ), array( 'jquery' ));
        //wp_register_script( 'anythingslider', $this->assetURL 'js/jquery.anythingslider.min.js' ), array( 'jquery' ));
    }

    /* Activation hook for plugin */
    public function activate() {
        add_option( 'wpb_js_composer_do_activation_redirect', true );
    }

    public function setUpTheme() {
	    if (!is_admin()) {
	        $this->addAction('template_redirect', 'frontCss');
	        $this->addAction('template_redirect', 'frontJsRegister');
	        $this->addAction('wp_enqueue_scripts', 'frontendJsLoad');
	        $this->addFilter('the_content', 'fixPContent', 10000);
	   	}
    }
}

/* Setup for admin */

class SwiftPageBuilderSetupAdmin extends SwiftPageBuilderSetup {
    public function __construct() {
        parent::__construct();
    }

    /* Setup plugin composer */

    public function setUpTheme() {
        parent::setUpPlugin();

        $this->composer->addAction( 'edit_post', 'saveMetaBoxes' );
        $this->composer->addAction( 'wp_ajax_wpb_get_element_backend_html', 'elementBackendHtmlJavascript_callback' );
        $this->composer->addAction( 'wp_ajax_wpb_shortcodes_to_visualComposer', 'shortCodesVisualComposerJavascript_callback' );
        $this->composer->addAction( 'wp_ajax_wpb_show_edit_form', 'showEditFormJavascript_callback' );
        $this->composer->addAction('wp_ajax_wpb_save_template', 'saveTemplateJavascript_callback');
        $this->composer->addAction('wp_ajax_wpb_load_template', 'loadTemplateJavascript_callback');
        $this->composer->addAction('wp_ajax_wpb_delete_template', 'deleteTemplateJavascript_callback');

        // Add specific CSS class by filter
        $this->addFilter('body_class', 'jsComposerBodyClass');
        $this->addFilter( 'get_media_item_args', 'jsForceSend' );

        $this->addAction( 'admin_menu','composerSettings' );
        $this->addAction( 'admin_init', 'composerRedirect' );
        $this->addAction( 'admin_init', 'jsComposerEditPage', 5 );

        $this->addAction( 'admin_init', 'registerCss' );
        $this->addAction( 'admin_init', 'registerJavascript' );

        $this->addAction( 'admin_print_scripts-post.php', 'editScreen_js' );
        $this->addAction( 'admin_print_scripts-post-new.php', 'editScreen_js' );

        /* Create Media tab for images */
        $this->composer->createImagesMediaTab();
    }

    public function jsComposerBodyClass($classes) {
        $classes[] = 'wpb-js-composer js-comp-ver-'.SPB_VERSION;
        return $classes;
    }

    public function jsForceSend($args) {
        $args['send'] = true;
        return $args;
    }

    public function editScreen_js() {
        wp_enqueue_style('bootstrap');
        wp_enqueue_style('ui-custom-theme');
        wp_enqueue_style('js_composer');

        wp_enqueue_script('jquery-ui-tabs');
        wp_enqueue_script('jquery-ui-droppable');
        wp_enqueue_script('jquery-ui-draggable');
        wp_enqueue_script('jquery-ui-accordion');

        wp_enqueue_script('bootstrap-js');
        wp_enqueue_script('wpb_js_composer_js');
    }

    public function registerJavascript() {
        wp_register_script('wpb_js_composer_js', $this->assetURL( 'js_composer.js' ), array('jquery'), SPB_VERSION, true);
        wp_register_script('bootstrap-js', $this->assetURL( 'bootstrap/js/bootstrap.min.js' ), false, SPB_VERSION, true);

    }

    public function registerCss() {

        wp_register_style( 'bootstrap', $this->assetURL( 'bootstrap/css/bootstrap.css' ), false, SPB_VERSION, false );
        wp_register_style( 'ui-custom-theme', $this->assetURL( 'ui-custom-theme/jquery-ui-' . SPB_JQUERY_UI_VERSION . '.custom.css' ), false, SPB_VERSION, false );
        wp_register_style( 'js_composer', $this->assetURL( 'js_composer.css' ), false, SPB_VERSION, false );

    }
    /* Call to generate main template editor */

    public function jsComposerEditPage() {
        $pt_array = $this->composer->getPostTypes();
        foreach ($pt_array as $pt) {
            add_meta_box( 'wpb_visual_composer', __('Swift Page Builder', "js_composer"), Array($this->composer->getLayout(), 'output'), $pt, 'normal', 'high');
        }
    }

    /* Add option to Settings menu */
    public function composerSettings() {

        if ( current_user_can('manage_options') && $this->composer->isPlugin()) {
            //add_options_page(__("Swift Page Builder Settings", "js_composer"), __("Swift Page Builder", "js_composer"), 'install_plugins', "wpb_vc_settings", array($this, "composerSettingsMenuHTML"));
        }
    }

    /* Include plugin settings page */

    public static function composerSettingsMenuHTML() {
        /* TODO: Refactor file js_composer_settings_menu.php */
        include_once( self::$config['COMPOSER'] . 'settings/' . 'js_composer_settings_menu.php' );
    }


    public function composerRedirect() {
        if ( get_option('wpb_js_composer_do_activation_redirect', false) ) {
            delete_option('wpb_js_composer_do_activation_redirect');
            wp_redirect(admin_url().'options-general.php?page=wpb_vc_settings');
        }
    }
}