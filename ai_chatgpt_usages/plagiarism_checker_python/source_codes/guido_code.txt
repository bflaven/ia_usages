<?php

/*
Plugin Name: MyFlagsSiteVersion (second YT chat-gpt-MyFlagsSiteVersion)
Plugin URI: https://www.example.com/myflagssiteversion
Description: A plugin to manipulate custom fields for two languages.
Version: 1.0
Author: Your Name
Author URI: https://www.example.com
*/
/*
# FIRST CODE GENERATION
# 005_generate_php_plugin_wordpress_flags_header.php
# Write in PHP, a Wordpress plugin with comments, named MyFlagsSiteVersion. This Plugin MyFlagsSiteVersion will add a new entry in the main administration menu in "Settings". The name of the entrance will be MyFlagsSiteVersion. The purpose of this plugin is to manipulate a single custom fields for 2 languages (spanish, russian):  myflagssiteversion_sp, myflagssiteversion_ru. You can you write also tips for this field and general explanation at the beginning of the plugin page settings to explain how does the plugin work.

# Model: https://github.com/bflaven/PluginWordpressForFun/blob/master/johann_flags_header/johann_flags_header.php
*/

// Add entry in main administration menu
add_action('admin_menu', 'myflagssiteversion_plugin_menu');

function myflagssiteversion_plugin_menu() {
    add_options_page(
        'MyFlagsSiteVersion Settings', 
        'MyFlagsSiteVersion', 
        'manage_options', 
        'myflagssiteversion', 
        'myflagssiteversion_plugin_settings_page'
    );
}

// Display settings page
function myflagssiteversion_plugin_settings_page() {
    if (!current_user_can('manage_options')) {
        wp_die(__('You do not have sufficient permissions to access this page.'));
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html(get_admin_page_title()); ?></h1>
        <p><?php echo __('This plugin allows you to manipulate custom fields for two languages.'); ?></p>
        <form method="post" action="options.php">
            <?php settings_fields('myflagssiteversion-settings-group'); ?>
            <?php do_settings_sections('myflagssiteversion'); ?>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

// Add custom fields for each language
add_action('admin_init', 'myflagssiteversion_plugin_settings');

function myflagssiteversion_plugin_settings() {
    add_settings_section(
        'myflagssiteversion-section',
        __('MyFlagsSiteVersion Custom Fields'),
        'myflagssiteversion_plugin_section_callback',
        'myflagssiteversion'
    );

    add_settings_field(
        'myflagssiteversion-sp',
        __('Spanish Field'),
        'myflagssiteversion_sp_callback',
        'myflagssiteversion',
        'myflagssiteversion-section'
    );

    add_settings_field(
        'myflagssiteversion-ru',
        __('Russian Field'),
        'myflagssiteversion_ru_callback',
        'myflagssiteversion',
        'myflagssiteversion-section'
    );

    register_setting(
        'myflagssiteversion-settings-group',
        'myflagssiteversion_sp'
    );

    register_setting(
        'myflagssiteversion-settings-group',
        'myflagssiteversion_ru'
    );
}

// Display custom fields for each language
function myflagssiteversion_plugin_section_callback() {
    echo '<p>' . __('Enter the text for each language below.') . '</p>';
}

function myflagssiteversion_sp_callback() {
    $sp_value = get_option('myflagssiteversion_sp');
    echo '<input type="text" name="myflagssiteversion_sp" value="' . esc_attr($sp_value) . '" />';
}

function myflagssiteversion_ru_callback() {
    $ru_value = get_option('myflagssiteversion_ru');
    echo '<input type="text" name="myflagssiteversion_ru" value="' . esc_attr($ru_value) . '" />';
}

?>
