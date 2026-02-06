<?php
/**
 * Theme Customizer
 *
 * @package Zaatar
 */

/**
 * Add postMessage support for site title and description for the Theme Customizer.
 *
 * @param WP_Customize_Manager $wp_customize Theme Customizer object.
 */
function allium_customize_register ( $wp_customize ) {

	$wp_customize->get_setting( 'blogname' )->transport         = 'postMessage';
	$wp_customize->get_setting( 'blogdescription' )->transport  = 'postMessage';
	$wp_customize->get_setting( 'background_color' )->transport = 'postMessage';
	$wp_customize->get_setting( 'header_textcolor' )->transport = 'postMessage';

	/**
	 * Theme Options Panel
	 */
	$wp_customize->add_panel( 'allium_theme_options', array(
	    'title'     => esc_html__( 'Theme Options', 'zaatar' ),
	    'priority'  => 1,
	) );

	/**
	 * General Options Section
	 */
	$wp_customize->add_section( 'allium_general_options', array (
		'title'     => esc_html__( 'General Options', 'zaatar' ),
		'panel'     => 'allium_theme_options',
		'priority'  => 10,
		'description' => esc_html__( 'Personalize the general settings of your theme.', 'zaatar' ),
	) );

	// Read More Label
	$wp_customize->add_setting ( 'allium_read_more_label', array(
		'default'           => allium_default( 'allium_read_more_label' ),
		'transport'         => 'postMessage',
		'sanitize_callback' => 'sanitize_text_field',
	) );

	$wp_customize->add_control ( 'allium_read_more_label', array(
		'label'    => esc_html__( 'Read More Label', 'zaatar' ),
		'section'  => 'allium_general_options',
		'priority' => 1,
		'type'     => 'text',
	) );

	// Excerpt Length
	$wp_customize->add_setting ( 'allium_excerpt_length', array(
		'default'           => allium_default( 'allium_excerpt_length' ),
		'sanitize_callback' => 'absint',
	) );

	$wp_customize->add_control ( 'allium_excerpt_length', array(
		'label'    => esc_html__( 'Excerpt Length', 'zaatar' ),
		'description' => esc_html__( 'Zero (0) length will not show the excerpt.', 'zaatar' ),
		'section'  => 'allium_general_options',
		'priority' => 2,
		'type'     => 'number',
	) );

	// Post Thumbnail Single Control
	$wp_customize->add_setting ( 'allium_post_thumbnail_single', array (
		'default'           => allium_default( 'allium_post_thumbnail_single' ),
		'sanitize_callback' => 'allium_sanitize_checkbox',
	) );

	$wp_customize->add_control ( 'allium_post_thumbnail_single', array (
		'label'    => esc_html__( 'Display Featured Image at Single Posts', 'zaatar' ),
		'section'  => 'allium_general_options',
		'priority' => 3,
		'type'     => 'checkbox',
	) );

	/**
	 * Layout Options Section
	 */
	$wp_customize->add_section( 'allium_layout_options', array (
		'title'     => esc_html__( 'Layout Options', 'zaatar' ),
		'panel'     => 'allium_theme_options',
		'priority'  => 20,
		'description' => esc_html__( 'Personalize the layout settings of your theme.', 'zaatar' ),
	) );

	// Theme Layout
	$wp_customize->add_setting ( 'allium_theme_layout', array(
		'default'           => allium_default( 'allium_theme_layout' ),
		'sanitize_callback' => 'allium_sanitize_select',
	) );

	$wp_customize->add_control ( 'allium_theme_layout', array(
		'label'    => esc_html__( 'Theme Layout', 'zaatar' ),
		'description' => esc_html__( 'Box layout will be visible at minimum 1200px display', 'zaatar' ),
		'section'  => 'allium_layout_options',
		'priority' => 1,
		'type'     => 'select',
		'choices'  => array(
			'wide' => esc_html__( 'Wide', 'zaatar' ),
			'box'  => esc_html__( 'Box',  'zaatar' ),
		),
	) );

	// Main Sidebar Position
	$wp_customize->add_setting ( 'allium_sidebar_position', array (
		'default'           => allium_default( 'allium_sidebar_position' ),
		'sanitize_callback' => 'allium_sanitize_select',
	) );

	$wp_customize->add_control ( 'allium_sidebar_position', array (
		'label'    => esc_html__( 'Main Sidebar Position (if active)', 'zaatar' ),
		'section'  => 'allium_layout_options',
		'priority' => 2,
		'type'     => 'select',
		'choices'  => array(
			'right' => esc_html__( 'Right', 'zaatar'),
			'left'  => esc_html__( 'Left',  'zaatar'),
		),
	) );

	/**
	 * Footer Section
	 */
	$wp_customize->add_section( 'allium_footer_options', array (
		'title'       => esc_html__( 'Footer Options', 'zaatar' ),
		'panel'       => 'allium_theme_options',
		'priority'    => 30,
		'description' => esc_html__( 'Personalize the footer settings of your theme.', 'zaatar' ),
	) );

	// Copyright Control
	$wp_customize->add_setting ( 'allium_copyright', array (
		'default'           => allium_default( 'allium_copyright' ),
		'transport'         => 'postMessage',
		'sanitize_callback' => 'wp_kses_post',
	) );

	$wp_customize->add_control ( 'allium_copyright', array (
		'label'    => esc_html__( 'Copyright', 'zaatar' ),
		'section'  => 'allium_footer_options',
		'priority' => 1,
		'type'     => 'textarea',
	) );

	// Credit Control
	$wp_customize->add_setting ( 'allium_credit', array (
		'default'           => allium_default( 'allium_credit' ),
		'transport'         => 'postMessage',
		'sanitize_callback' => 'allium_sanitize_checkbox',
	) );

	$wp_customize->add_control ( 'allium_credit', array (
		'label'    => esc_html__( 'Display Designer Credit', 'zaatar' ),
		'section'  => 'allium_footer_options',
		'priority' => 2,
		'type'     => 'checkbox',
	) );

	/**
	 * Support Section
	 */
	$wp_customize->add_section( 'allium_support_options', array(
		'title'       => esc_html__( 'Support Options', 'zaatar' ),
		'description' => esc_html__( 'Thanks for your interest in Zaatar! To share your feedback and for any support query you can reach us at', 'zaatar' ),
		'panel'       => 'allium_theme_options',
		'priority'    => 40,
	) );

	// Theme Support
	$wp_customize->add_setting ( 'allium_theme_support', array(
		'default' => '',
	) );

	$wp_customize->add_control(
		new Zaatar_Button_Control(
			$wp_customize,
			'allium_theme_support',
			array(
				'label'         => esc_html__( 'Zaatar Support', 'zaatar' ),
				'section'       => 'allium_support_options',
				'priority'      => 1,
				'type'          => 'allium-button',
				'button_tag'    => 'a',
				'button_class'  => 'button button-primary',
				'button_href'   => 'https://templatelens.com/contact/',
				'button_target' => '_blank',
			)
		)
	);

	/**
	 * Review Section
	 */
	$wp_customize->add_section( 'allium_review_options', array(
		'title'       => esc_html__( 'Add Your Review', 'zaatar' ),
		'description' => esc_html__( 'Why not leave us a review on WordPress.org? Your review on WordPress will be highly appreciated, as it encourages us to keep updating and supporting the product.', 'zaatar' ),
		'panel'       => 'allium_theme_options',
		'priority'    => 50,
	) );

	// Theme
	$wp_customize->add_setting ( 'allium_theme_review', array(
		'default' => '',
	) );

	$wp_customize->add_control(
		new Zaatar_Button_Control(
			$wp_customize,
			'allium_theme_review',
			array(
				'label'         => esc_html__( 'Review on WordPress.org', 'zaatar' ),
				'section'       => 'allium_review_options',
				'type'          => 'allium-button',
				'button_tag'    => 'a',
				'button_class'  => 'button button-primary',
				'button_href'   => 'https://wordpress.org/support/theme/allium/reviews',
				'button_target' => '_blank',
			)
		)
	);
}
add_action( 'customize_register', 'allium_customize_register' );

/**
 * Binds JS handlers to make Theme Customizer preview reload changes asynchronously.
 */
function allium_customize_preview_js() {
	wp_enqueue_script( 'allium_customizer', get_template_directory_uri() . '/js/customizer.js', array( 'customize-preview' ), '20140120', true );
}
add_action( 'customize_preview_init', 'allium_customize_preview_js' );
