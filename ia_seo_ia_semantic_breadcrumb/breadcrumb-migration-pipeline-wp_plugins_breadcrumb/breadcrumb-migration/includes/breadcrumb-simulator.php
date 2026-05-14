<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Render an HTML breadcrumb trail from a proposal's proposed_breadcrumb JSON.
 *
 * @param  int $term_id  Internal wp_breadcrumb_terms.id
 * @return string        HTML nav element or error message
 */
function bm_render_breadcrumb( int $term_id ): string {
	global $wpdb;
	$t = bm_tables();

	$row = $wpdb->get_row( $wpdb->prepare(
		"SELECT proposed_breadcrumb, proposed_name, validation_state
		 FROM {$t['proposals']}
		 WHERE term_id = %d
		 ORDER BY id DESC
		 LIMIT 1",
		$term_id
	) );

	if ( ! $row ) {
		return '<em class="bm-no-data">' . esc_html__( 'No proposal yet. Run the pipeline first.', 'breadcrumb-migration' ) . '</em>';
	}

	if ( empty( $row->proposed_breadcrumb ) ) {
		return '<em class="bm-no-data">' . esc_html__( 'No breadcrumb in proposal.', 'breadcrumb-migration' ) . '</em>';
	}

	$parts = json_decode( $row->proposed_breadcrumb, true );
	if ( ! is_array( $parts ) || empty( $parts ) ) {
		return '<em class="bm-error">' . esc_html__( 'Invalid breadcrumb data.', 'breadcrumb-migration' ) . '</em>';
	}

	$items = [];
	$last  = count( $parts ) - 1;
	foreach ( $parts as $i => $label ) {
		$css    = 'bm-crumb' . ( $i === $last ? ' bm-crumb--current' : '' );
		$items[] = '<span class="' . $css . '">' . esc_html( $label ) . '</span>';
	}

	return '<nav class="bm-breadcrumb" aria-label="breadcrumb preview">'
		. implode( '<span class="bm-sep" aria-hidden="true"> › </span>', $items )
		. '</nav>';
}

/**
 * Build breadcrumb parts array by walking wp_breadcrumb_terms parent chain.
 * Useful for computing breadcrumb on the fly (without pipeline JSON).
 *
 * @param  int    $term_internal_id  wp_breadcrumb_terms.id
 * @param  int    $max_depth
 * @return array  e.g. ["Home", "Parent", "Child"]
 */
function bm_compute_breadcrumb( int $term_internal_id, int $max_depth = 6 ): array {
	global $wpdb;
	$t = bm_tables();

	$parts = [];
	$id    = $term_internal_id;
	$seen  = [];

	while ( $id && count( $parts ) < $max_depth ) {
		if ( isset( $seen[ $id ] ) ) {
			break; // circular guard
		}
		$seen[ $id ] = true;

		$row = $wpdb->get_row( $wpdb->prepare(
			"SELECT original_name, original_parent_id, taxonomy FROM {$t['terms']} WHERE id = %d",
			$id
		) );

		if ( ! $row ) {
			break;
		}

		$parts[] = $row->original_name;

		// Resolve parent by wp_term_id
		if ( $row->original_parent_id ) {
			$parent = $wpdb->get_row( $wpdb->prepare(
				"SELECT id FROM {$t['terms']} WHERE wp_term_id = %d AND taxonomy = %s LIMIT 1",
				$row->original_parent_id,
				$row->taxonomy
			) );
			$id = $parent ? (int) $parent->id : 0;
		} else {
			$id = 0;
		}
	}

	$parts = array_reverse( $parts );

	// post_tag → insert "Tags" tier
	if ( isset( $row ) && $row->taxonomy === 'post_tag' ) {
		array_splice( $parts, 0, 0, [ 'Tags' ] );
	}

	return array_merge( [ 'Home' ], $parts );
}
