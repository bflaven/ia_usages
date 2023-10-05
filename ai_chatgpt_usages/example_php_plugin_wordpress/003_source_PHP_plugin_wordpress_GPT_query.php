<?php
/*
Plugin Name: MySocialBuddy
Description: A plugin to add social network accounts to your WordPress site.
Version: 1.0
Author: Your Name
License: GPL2
*/



// 003_source_PHP_plugin_wordpress_GPT_query.php
// source PHP for GPT query  
/*
QUERY_1 (unfinished) :: Write in PHP, a Wordpress plugin with comments, named MySocialBuddy. This Plugin MySocialBuddy will add a new entry in the main administration menu in "Settings". The name of the entrance will be “MySocialBuddy”. The purpose of this plugin is to manipulate 5 custom fields for social network accounts: mysocialbuddy_twitter, mysocialbuddy_linkedin, mysocialbuddy_facebook, mysocialbuddy_instagram, mysocialbuddy_vkontakt, mysocialbuddy_weibo.
You can you write also tips for each field and general explanation at the beginning of the plugin page settings to explain how does the plugin work.

QUERY_2 (unfinished) :: Write in PHP, a Wordpress plugin with comments, named MySocialBuddy. This Plugin MySocialBuddy will add a new entry in the main administration menu in "Settings". The name of the entrance will be “MySocialBuddy”. The purpose of this plugin is to manipulate 1 custom fields for social network accounts: mysocialbuddy_twitter.
You can you write also tips for this field and general explanation at the beginning of the plugin page settings to explain how does the plugin work.


*/

// Here is a sample code for a WordPress plugin called "MySocialBuddy" that adds a new menu entry in the "Settings" menu and manipulates a custom field called "mysocialbuddy_twitter":




// Add a new entry in the main administration menu in "Settings"
add_action('admin_menu', 'mysocialbuddy_add_admin_menu');

function mysocialbuddy_add_admin_menu() {
  add_options_page('MySocialBuddy', 'MySocialBuddy', 'manage_options', 'mysocialbuddy', 'mysocialbuddy_options_page');
}

// Display the options page for MySocialBuddy
function mysocialbuddy_options_page() {
  ?>
  <div class="wrap">
    <h1>MySocialBuddy Settings</h1>
    <p>Use this page to enter your social network accounts.</p>
    <form method="post" action="options.php">
      <?php
        settings_fields('mysocialbuddy_options');
        do_settings_sections('mysocialbuddy');
        submit_button('Save Settings');
      ?>
    </form>
  </div>
  <?php
}

// Register the custom field for social network accounts
add_action('admin_init', 'mysocialbuddy_register_settings');

function mysocialbuddy_register_settings() {
  register_setting('mysocialbuddy_options', 'mysocialbuddy_twitter');
  add_settings_section('mysocialbuddy_section', 'Social Network Accounts', 'mysocialbuddy_section_text', 'mysocialbuddy');
  add_settings_field('mysocialbuddy_twitter', 'Twitter', 'mysocialbuddy_twitter_input', 'mysocialbuddy', 'mysocialbuddy_section');
}

// Display the description for the social network accounts section
function mysocialbuddy_section_text() {
  echo '<p>Enter your social network accounts below.</p>';
}

// Display the input field for the Twitter account
function mysocialbuddy_twitter_input() {
  $twitter = esc_attr(get_option('mysocialbuddy_twitter'));
  echo '<input type="text" name="mysocialbuddy_twitter" value="' . $twitter . '" />';
}


/*
This plugin registers a custom field for the Twitter account under the "Social Network Accounts" section in the "MySocialBuddy" menu. The field can be accessed and edited by users with the "manage_options" capability. The settings are saved using the WordPress settings API and can be accessed using the get_option() function.

To add more social network accounts, you can add more fields using the add_settings_field() function and register them using the register_setting() function. You can also add more sections and descriptions using the add_settings_section() function and the corresponding text functions.

 */
?>














