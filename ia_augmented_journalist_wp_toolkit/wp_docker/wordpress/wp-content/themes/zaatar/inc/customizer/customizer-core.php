<?php
/**
 * Theme Customizer Core
 *
 * @package Zaatar
 */

/**
 * Theme Mod Defaults
 *
 * @param string $theme_mod - Theme modification name.
 * @return mixed
 */
function allium_default( $theme_mod = '' ) {

	$default = apply_filters( 'allium_default', array (
		'allium_read_more_label'       => esc_html_x( 'Read More', 'Read More Label', 'zaatar' ),
		'allium_excerpt_length'        => 25,
		'allium_post_thumbnail_single' => false,
		'allium_theme_layout'          => 'wide',
		'allium_sidebar_position'      => 'right',
		'allium_copyright'             => sprintf( '%1$s %2$s - <a href="%3$s">%4$s</a>', esc_html__( '&copy; Copyright', 'zaatar' ), esc_html( date_i18n( __( 'Y', 'zaatar' ) ) ), esc_attr( esc_url( home_url( '/' ) ) ), esc_html( get_bloginfo( 'name' ) ) ),
		'allium_credit'                => true,
	) );

	return ( isset ( $default[$theme_mod] ) ? $default[$theme_mod] : '' );

}

/**
 * Theme Mod Wrapper
 *
 * @param string $theme_mod - Name of the theme mod to retrieve.
 * @return mixed
 */
function allium_mod( $theme_mod = '' ) {
	return get_theme_mod( $theme_mod, allium_default( $theme_mod ) );
}

/**
 * Customizer Button Control Class
 */
if ( class_exists( 'WP_Customize_Control' ) ) {

	class Zaatar_Button_Control extends WP_Customize_Control {
		/**
		 * @access public
		 * @var string
		 */
		public $type = 'allium-button';

		/**
		 * HTML tag to render button object.
		 *
		 * @var  string
		 */
		protected $button_tag = 'button';

		/**
		 * Class to render button object.
		 *
		 * @var  string
		 */
		protected $button_class = 'button button-primary';

		/**
		 * Link for <a> based button.
		 *
		 * @var  string
		 */
		protected $button_href = 'javascript:void(0)';

		/**
		 * Target for <a> based button.
		 *
		 * @var  string
		 */
		protected $button_target = '';

		/**
		 * Click event handler.
		 *
		 * @var  string
		 */
		protected $button_onclick = '';

		/**
		 * ID attribute for HTML tab.
		 *
		 * @var  string
		 */
		protected $button_tag_id = '';

		/**
		 * Render the control's content.
		 */
		public function render_content() {
		?>
			<span class="center">
				<?php
				// Print open tag
				echo '<' . esc_html( $this->button_tag );

				// button class
				if ( ! empty( $this->button_class ) ) {
					echo ' class="' . esc_attr( $this->button_class ) . '"';
				}

				// button or href
				if ( 'button' == $this->button_tag ) {
					echo ' type="button"';
				} else {
					echo ' href="' . esc_url( $this->button_href ) . '"' . ( empty( $this->button_tag ) ? '' : ' target="' . esc_attr( $this->button_target ) . '"' );
				}

				// onClick Event
				if ( ! empty( $this->button_onclick ) ) {
					echo ' onclick="' . esc_js( $this->button_onclick ) . '"';
				}

				// ID
				if ( ! empty( $this->button_tag_id ) ) {
					echo ' id="' . esc_attr( $this->button_tag_id ) . '"';
				}

				echo '>';

				// Print text inside tag
				echo esc_html( $this->label );

				// Print close tag
				echo '</' . esc_html( $this->button_tag ) . '>';
				?>
			</span>
		<?php
		}
	}

}

/**
 * Sanitize Select.
 *
 * @param string $input Slug to sanitize.
 * @param WP_Customize_Setting $setting Setting instance.
 * @return string Sanitized slug if it is a valid choice; otherwise, the setting default.
 */
function allium_sanitize_select( $input, $setting ) {

	// Ensure input is a slug.
	$input = sanitize_key( $input );

	// Get list of choices from the control associated with the setting.
	$choices = $setting->manager->get_control( $setting->id )->choices;

	// If the input is a valid key, return it; otherwise, return the default.
	return ( array_key_exists( $input, $choices ) ? $input : $setting->default );
}

/**
 * Sanitize the checkbox.
 *
 * @param bool $checked Whether the checkbox is checked.
 * @return bool Whether the checkbox is checked.
 */
function allium_sanitize_checkbox( $checked ) {
	return ( ( isset( $checked ) && true === $checked ) ? true : false );
}
