<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// ── Import handler (admin-post) ────────────────────────────────────────────────

function bm_handle_import(): void {
	check_admin_referer( 'bm_import_nonce' );
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( 'Insufficient permissions.' );
	}

	$redirect = admin_url( 'admin.php?page=breadcrumb-migration&tab=import' );

	if ( empty( $_FILES['bm_import_file']['tmp_name'] ) ) {
		wp_safe_redirect( add_query_arg( 'bm_msg', 'no_file', $redirect ) );
		exit;
	}

	$file     = $_FILES['bm_import_file'];
	$tmp_path = $file['tmp_name'];
	$ext      = strtolower( pathinfo( $file['name'], PATHINFO_EXTENSION ) );
	$rows     = [];

	if ( $ext === 'json' ) {
		$content = file_get_contents( $tmp_path );
		$decoded = json_decode( $content, true );
		if ( ! $decoded ) {
			wp_safe_redirect( add_query_arg( 'bm_msg', 'invalid_json', $redirect ) );
			exit;
		}
		$rows = isset( $decoded['data'] ) && is_array( $decoded['data'] )
			? $decoded['data']
			: $decoded;
	} elseif ( $ext === 'csv' ) {
		$handle  = fopen( $tmp_path, 'r' );
		$headers = fgetcsv( $handle );
		if ( ! $headers ) {
			wp_safe_redirect( add_query_arg( 'bm_msg', 'empty_csv', $redirect ) );
			exit;
		}
		while ( ( $line = fgetcsv( $handle ) ) !== false ) {
			if ( count( $line ) === count( $headers ) ) {
				$rows[] = array_combine( $headers, $line );
			}
		}
		fclose( $handle );
	} else {
		wp_safe_redirect( add_query_arg( 'bm_msg', 'bad_format', $redirect ) );
		exit;
	}

	if ( empty( $rows ) ) {
		wp_safe_redirect( add_query_arg( 'bm_msg', 'empty_data', $redirect ) );
		exit;
	}

	global $wpdb;
	$t  = bm_tables();
	$ok = $err = 0;

	foreach ( $rows as $row ) {
		$wp_term_id = (int) ( $row['id'] ?? 0 );
		$taxonomy   = sanitize_text_field( $row['taxonomy'] ?? '' );

		if ( ! $wp_term_id || ! $taxonomy ) {
			$err++;
			continue;
		}

		// Upsert term
		$existing_term_id = $wpdb->get_var( $wpdb->prepare(
			"SELECT id FROM {$t['terms']} WHERE wp_term_id = %d AND taxonomy = %s",
			$wp_term_id,
			$taxonomy
		) );

		if ( $existing_term_id ) {
			$term_id = (int) $existing_term_id;
			$wpdb->update(
				$t['terms'],
				[ 'content_count' => (int) ( $row['post_count'] ?? 0 ) ],
				[ 'id' => $term_id ]
			);
		} else {
			$parent = ! empty( $row['parent_id'] ) ? (int) $row['parent_id'] : null;
			$wpdb->insert( $t['terms'], [
				'wp_term_id'         => $wp_term_id,
				'taxonomy'           => $taxonomy,
				'original_name'      => sanitize_text_field( $row['name'] ?? '' ),
				'original_slug'      => sanitize_title( $row['slug'] ?? '' ),
				'original_parent_id' => $parent,
				'content_count'      => (int) ( $row['post_count'] ?? 0 ),
				'language'           => 'fr',
				'status'             => 'original',
			] );
			$term_id = (int) $wpdb->insert_id;
		}

		if ( ! $term_id ) {
			$err++;
			continue;
		}

		// Build breadcrumb JSON — handle both list (from JSON) and "A > B" string (from CSV)
		$bc_raw = $row['proposed_breadcrumb'] ?? '';
		if ( is_array( $bc_raw ) ) {
			$bc_json = wp_json_encode( $bc_raw );
		} else {
			$parts   = array_map( 'trim', explode( '>', (string) $bc_raw ) );
			$bc_json = wp_json_encode( array_values( array_filter( $parts ) ) );
		}

		// Upsert proposal
		$existing_proposal_id = $wpdb->get_var( $wpdb->prepare(
			"SELECT id FROM {$t['proposals']} WHERE term_id = %d",
			$term_id
		) );

		$proposal_data = [
			'proposed_name'        => sanitize_text_field( $row['name'] ?? '' ),
			'proposed_slug'        => sanitize_title( $row['slug'] ?? '' ),
			'proposed_language'    => 'fr',
			'spacy_entity'         => ! empty( $row['spacy_entity'] ) ? sanitize_text_field( $row['spacy_entity'] ) : null,
			'wikidata_id'          => ! empty( $row['wikidata_id'] ) ? sanitize_text_field( $row['wikidata_id'] ) : null,
			'wikidata_label'       => ! empty( $row['wikidata_label'] ) ? sanitize_text_field( $row['wikidata_label'] ) : null,
			'wikidata_description' => ! empty( $row['wikidata_description'] ) ? sanitize_textarea_field( $row['wikidata_description'] ) : null,
			'proposed_breadcrumb'  => $bc_json,
			'validation_state'     => 'pending',
		];

		if ( $existing_proposal_id ) {
			$wpdb->update( $t['proposals'], $proposal_data, [ 'id' => (int) $existing_proposal_id ] );
		} else {
			$proposal_data['term_id'] = $term_id;
			$wpdb->insert( $t['proposals'], $proposal_data );
		}

		$ok++;
	}

	wp_safe_redirect( add_query_arg( [
		'bm_msg'   => 'imported',
		'bm_count' => $ok,
		'bm_err'   => $err,
	], $redirect ) );
	exit;
}

// ── Export handler (admin-post) ────────────────────────────────────────────────

function bm_handle_export(): void {
	if ( ! isset( $_GET['_wpnonce'] ) ||
	     ! wp_verify_nonce( sanitize_text_field( $_GET['_wpnonce'] ), 'bm_export_nonce' ) ) {
		wp_die( 'Invalid nonce.' );
	}
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( 'Insufficient permissions.' );
	}

	$table   = sanitize_key( $_GET['bm_table'] ?? 'proposals' );
	$allowed = [ 'proposals', 'terms', 'redirects' ];
	if ( ! in_array( $table, $allowed, true ) ) {
		wp_die( 'Invalid table.' );
	}

	$format  = sanitize_key( $_GET['bm_format'] ?? 'csv' );
	$allowed_formats = [ 'csv', 'json' ];
	if ( ! in_array( $format, $allowed_formats, true ) ) {
		$format = 'csv';
	}

	global $wpdb;
	$t    = bm_tables();
	$rows = $wpdb->get_results( "SELECT * FROM {$t[ $table ]}", ARRAY_A ); // phpcs:ignore

	$date     = gmdate( 'Ymd_His' );
	$basename = 'bm_' . $table . '_' . $date;

	header( 'Pragma: no-cache' );
	header( 'Expires: 0' );

	if ( $format === 'json' ) {
		$filename = $basename . '.json';
		header( 'Content-Type: application/json; charset=utf-8' );
		header( 'Content-Disposition: attachment; filename="' . $filename . '"' );

		$payload = [
			'exported_at' => gmdate( 'c' ),
			'table'       => $table,
			'total'       => count( $rows ),
			'data'        => $rows ?: [],
		];
		echo wp_json_encode( $payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE );
		exit;
	}

	// CSV (default)
	$filename = $basename . '.csv';
	header( 'Content-Type: text/csv; charset=utf-8' );
	header( 'Content-Disposition: attachment; filename="' . $filename . '"' );

	if ( empty( $rows ) ) {
		exit;
	}

	$out = fopen( 'php://output', 'w' );
	fputcsv( $out, array_keys( $rows[0] ) );
	foreach ( $rows as $row ) {
		fputcsv( $out, $row );
	}
	fclose( $out );
	exit;
}
