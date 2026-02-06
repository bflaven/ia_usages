<?php
/**
 * Swift Page Builder Plugin wordpress settings page
 *
 * @package VPBakeryVisualComposer
 *
 */

// don't load directly
if ( !defined('ABSPATH') ) die('-1');

$excluded = array('attachment', 'revision', 'nav_menu_item', 'mediapage');
$post_types = get_post_types(array('public'   => true));

// if this fails, check_admin_referer() will automatically print a "failed" page and die.
if ( !empty($_POST) && check_admin_referer('wpb_js_settings_save_action', 'wpb_js_nonce_field') ) {
		
	// process form data
	$pt_arr = array();
	foreach ( $_POST as $pt ) {
		if ( !in_array($pt, $excluded) && in_array($pt, $post_types) ) {
			$pt_array[] = $pt;
		}
	}
	
	if ( count($pt_array) > 0 ) {
		update_option('wpb_js_content_types', $pt_array);
	} else {
		delete_option('wpb_js_content_types');
	}
}

if ( current_user_can('switch_themes') ) : ?>
	<div id="custom-background" class="wrap">
		<div class="icon32" id="icon-themes"><br></div>
		
		<h2><?php _e("Swift Page Builder Settings VVVervsion", "js_composer"); ?></h2>
		
		<form action="<?php echo str_replace( '%7E', '~', $_SERVER['REQUEST_URI']); ?>" method="post">
			<table class="form-table">
				<tbody>
					<tr valign="top">
						<th scope="row"><?php _e("Content types", "js_composer"); ?></th>
						<td>
							<fieldset>
								<legend class="screen-reader-text"><span><?php _e("Post types", "js_composer"); ?></span></legend>
								<?php
								$pt_array = ($pt_array = get_option('wpb_js_content_types')) ? $pt_array : array();
								foreach ($post_types as $pt) {
									if (!in_array($pt, $excluded)) {
										$checked = (in_array($pt, $pt_array)) ? ' checked="checked"' : '';
									?>
										<label for="use_smilies">
											<input type="checkbox"<?php echo $checked; ?> value="<?php echo $pt; ?>" id="check_<?php echo $pt; ?>" name="post_type_<?php echo $pt; ?>">
												<?php echo $pt; ?>
										</label><br>
									<?php }
								}
								?>
							</fieldset>
						</td>
					</tr>
					
					<tr valign="top">
						<th>&nbsp;</th>
						<td>
							<p class="description indicator-hint"><?php _e("Select for which content types Swift Page Builder should be available during post creation/editing.", "js_composer"); ?></p>
						</td>
					</tr>
				</tbody>
			</table>

			<?php wp_nonce_field('wpb_js_settings_save_action', 'wpb_js_nonce_field'); ?>
			<p class="submit">
				<input type="submit" value="Save Changes" class="button-primary" id="save-background-options" name="save-background-options">
            </p>
		</form>
		
		<div>
			<h2><?php _e("Thank you", "js_composer"); ?></h2>
			<p><?php _e("Swift Page Builder will save you a lot of time while working with your sites content.", "js_composer"); ?></p>
		</div>
		
	</div>
<?php endif; ?>
<?php ?>