<?php
/*
Plugin Name: MyFlagsSiteVersion (good or bad)
Plugin URI: http://example.com/myflagssiteversion
Description: A plugin for manipulating a single custom field for 2 languages (Spanish and Russian).
Version: 1.0
Author: Your Name
Author URI: http://example.com
License: GPL2
*/

/*
# SECOND CODE GENERATION
# 006_generate_php_plugin_wordpress_flags_header.php
# Write in PHP, a Wordpress plugin with comments, named MyFlagsSiteVersion. This Plugin MyFlagsSiteVersion will add a new entry in the main administration menu in "Settings". The name of the entrance will be MyFlagsSiteVersion. The purpose of this plugin is to manipulate a single custom fields for 2 languages (spanish, russian):  myflagssiteversion_sp, myflagssiteversion_ru. You can you write also tips for this field and general explanation at the beginning of the plugin page settings to explain how does the plugin work.

# Model: https://github.com/bflaven/PluginWordpressForFun/blob/master/johann_flags_header/johann_flags_header.php
*/



// Add the entry to the main administration menu in "Settings"
add_action('admin_menu', 'myflagssiteversion_admin_menu');
function myflagssiteversion_admin_menu() {
	add_options_page( 'MyFlagsSiteVersion Settings', 'MyFlagsSiteVersion', 'manage_options', 'myflagssiteversion-settings', 'myflagssiteversion_settings_page' );
}

// Function to display the plugin page settings
function myflagssiteversion_settings_page() {
	// Check if the user has the required capability
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	
	// Save the options if the form is submitted
	if( isset( $_POST['myflagssiteversion_submit'] ) ) {
		update_option( 'myflagssiteversion_sp', $_POST['myflagssiteversion_sp'] );
		update_option( 'myflagssiteversion_ru', $_POST['myflagssiteversion_ru'] );
		?>
		<div class="updated"><p><strong><?php _e('Options saved.'); ?></strong></p></div>
		<?php
	}
	?>
	<div class="wrap">
		<h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
		<p><?php _e('Hello Youtube, this is openai attempt. This plugin allows you to manipulate a single custom field for 2 languages (Spanish and Russian) on your site. Enter the values for each language below:'); ?></p>
		<form method="post" action="">
			<label for="myflagssiteversion_sp"><?php _e('Spanish:'); ?></label><br>
			<input type="text" id="myflagssiteversion_sp" name="myflagssiteversion_sp" value="<?php echo esc_attr( get_option('myflagssiteversion_sp') ); ?>" size="50"><br>
			<label for="myflagssiteversion_ru"><?php _e('Russian:'); ?></label><br>
			<input type="text" id="myflagssiteversion_ru" name="myflagssiteversion_ru" value="<?php echo esc_attr( get_option('myflagssiteversion_ru') ); ?>" size="50"><br><br>
			<input type="submit" name="myflagssiteversion_submit" class="button button-primary" value="<?php _e('Save Changes'); ?>">
		</form>
		<p><?php _e('Tips: You can use this field to display different versions or updates of your site for Spanish and Russian visitors.'); ?></p>
	</div>
	<?php
}
?>