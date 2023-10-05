<?php
/*
Plugin Name: MySocialBuddy
Plugin URI: https://example.com/mysocialbuddy/
Description: This plugin allows you to add social network accounts to your WordPress site.
Version: 1.0
Author: slave GPT and lazy Bruno Flaven :)
Author URI: https://flaven.fr/ and https://chat.openai.com/chat
License: GPL2
*/



// 001_source_PHP_plugin_wordpress_GPT_query.php
// source PHP for GPT query  
/*
QUERY_1 (unfinished) :: Write in PHP, a Wordpress plugin with comments, named MySocialBuddy. This Plugin MySocialBuddy will add a new entry in the main administration menu in "Settings". The name of the entrance will be “MySocialBuddy”. The purpose of this plugin is to manipulate 5 custom fields for social network accounts: mysocialbuddy_twitter, mysocialbuddy_linkedin, mysocialbuddy_facebook, mysocialbuddy_instagram, mysocialbuddy_vkontakt, mysocialbuddy_weibo.
You can you write also tips for each field and general explanation at the beginning of the plugin page settings to explain how does the plugin work.

QUERY_2 (unfinished) :: Write in PHP, a Wordpress plugin with comments, named MySocialBuddy. This Plugin MySocialBuddy will add a new entry in the main administration menu in "Settings". The name of the entrance will be “MySocialBuddy”. The purpose of this plugin is to manipulate 1 custom fields for social network accounts: mysocialbuddy_twitter.
You can you write also tips for this field and general explanation at the beginning of the plugin page settings to explain how does the plugin work.


*/

// Here's an example PHP code for a Wordpress plugin named "MySocialBuddy" that adds a new entry in the main administration menu under "Settings" and manipulates 5 custom fields for social network accounts:

// Add the MySocialBuddy menu item in the admin menu
function mysocialbuddy_admin_menu() {
	add_options_page( 'MySocialBuddy Settings', 'MySocialBuddy', 'manage_options', 'mysocialbuddy', 'mysocialbuddy_settings_page' );
}
add_action( 'admin_menu', 'mysocialbuddy_admin_menu' );

// Display the MySocialBuddy settings page
function mysocialbuddy_settings_page() {
?>
	<div class="wrap">
		<h1>MySocialBuddy Settings</h1>
		<p>Welcome to MySocialBuddy! This plugin allows you to add social network accounts to your WordPress site. Enter your account information below to get started.</p>
		<form method="post" action="options.php">
			<?php settings_fields( 'mysocialbuddy-settings-group' ); ?>
			<?php do_settings_sections( 'mysocialbuddy-settings-group' ); ?>
			<table class="form-table">
				<tr valign="top">
					<th scope="row">Twitter</th>
					<td><input type="text" name="mysocialbuddy_twitter" value="<?php echo esc_attr( get_option('mysocialbuddy_twitter') ); ?>" /></td>
				</tr>
				<tr valign="top">
					<th scope="row">LinkedIn</th>
					<td><input type="text" name="mysocialbuddy_linkedin" value="<?php echo esc_attr( get_option('mysocialbuddy_linkedin') ); ?>" /></td>
				</tr>
				<tr valign="top">
					<th scope="row">Facebook</th>
					<td><input type="text" name="mysocialbuddy_facebook" value="<?php echo esc_attr( get_option('mysocialbuddy_facebook') ); ?>" /></td>
				</tr>
				<tr valign="top">
					<th scope="row">Instagram</th>
					<td><input type="text" name="mysocialbuddy_instagram" value="<?php echo esc_attr( get_option('mysocialbuddy_instagram') ); ?>" /></td>
				</tr>
				<tr valign="top">
					<th scope="row">Vkontakte</th>
					<td><input type="text" name="mysocialbuddy_vkontakte" value="<?php echo esc_attr( get_option('mysocialbuddy_vkontakte') ); ?>" /></td>
				</tr>
				<tr valign="top">
					<th scope="row">Weibo</th>
					<td><input type="text" name="mysocialbuddy_weibo" value="<?php echo esc_attr( get_option('mysocialbuddy_weibo') ); ?>" /></td>
				</tr>
			</table>
			<?php submit_button(); ?>
		</form>
	</div>
<?php
}

// Register the MySocialBuddy settings
function mysocialbuddy_register_settings() {
	register_setting( 'mysocialbuddy-settings-group', 'mysocialbuddy_twitter');


	// CAUTION :: lazy GPT stops here, need to complete
	register_setting('mysocialbuddy-settings-group', 'mysocialbuddy_linkedin' );

  	register_setting( 'mysocialbuddy_settings', 'mysocialbuddy_facebook' );

	register_setting( 'mysocialbuddy_settings', 'mysocialbuddy_facebook' );

	register_setting( 'mysocialbuddy_settings', 'mysocialbuddy_instagram' );
	register_setting( 'mysocialbuddy_settings', 'mysocialbuddy_vkontakte' );
	register_setting( 'mysocialbuddy_settings', 'mysocialbuddy_weibo' );


}




?> 











