<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// ── Guards ─────────────────────────────────────────────────────────────────────

function bm_verify_request(): void {
	check_ajax_referer( 'bm_nonce', 'nonce' );
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_send_json_error( [ 'message' => 'Insufficient permissions.' ], 403 );
	}
}

// ── Validate / Reject ──────────────────────────────────────────────────────────

function bm_ajax_validate_proposal(): void {
	bm_verify_request();

	$proposal_id = absint( $_POST['proposal_id'] ?? 0 );
	$action_type = sanitize_text_field( $_POST['action_type'] ?? '' );

	if ( ! $proposal_id || ! in_array( $action_type, [ 'approve', 'reject', 'reset' ], true ) ) {
		wp_send_json_error( [ 'message' => 'Invalid parameters.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	if ( $action_type === 'reset' ) {
		$updated = $wpdb->update(
			$t['proposals'],
			[
				'validation_state' => 'pending',
				'validated_by'     => null,
				'validated_at'     => null,
			],
			[ 'id' => $proposal_id ]
		);
		$state = 'pending';
	} else {
		$state = $action_type === 'approve' ? 'approved' : 'rejected';
		$updated = $wpdb->update(
			$t['proposals'],
			[
				'validation_state' => $state,
				'validated_by'     => get_current_user_id(),
				'validated_at'     => current_time( 'mysql' ),
			],
			[ 'id' => $proposal_id ]
		);
	}

	if ( $updated === false ) {
		wp_send_json_error( [ 'message' => 'DB update failed.' ] );
	}

	wp_send_json_success( [
		'proposal_id' => $proposal_id,
		'state'       => $state,
		'label'       => ucfirst( $state ),
	] );
}

// ── Simulate breadcrumb ────────────────────────────────────────────────────────

function bm_ajax_simulate_breadcrumb(): void {
	bm_verify_request();

	$term_id = absint( $_POST['term_id'] ?? 0 );
	if ( ! $term_id ) {
		wp_send_json_error( [ 'message' => 'Missing term_id.' ] );
	}

	$html = bm_render_breadcrumb( $term_id );
	wp_send_json_success( [ 'html' => $html ] );
}

// ── Inline edit proposal ───────────────────────────────────────────────────────

function bm_ajax_update_proposal(): void {
	bm_verify_request();

	$proposal_id = absint( $_POST['proposal_id'] ?? 0 );
	if ( ! $proposal_id ) {
		wp_send_json_error( [ 'message' => 'Missing proposal_id.' ] );
	}

	$raw_spacy = sanitize_text_field( $_POST['spacy_entity'] ?? '' );
	$allowed_entities = [
		'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT',
		'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT',
		'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL',
	];
	$spacy_entity = in_array( $raw_spacy, $allowed_entities, true ) ? $raw_spacy : null;

	$fields = [
		'proposed_name'        => sanitize_text_field( $_POST['proposed_name']        ?? '' ),
		'proposed_slug'        => sanitize_title(      $_POST['proposed_slug']         ?? '' ),
		'proposed_description' => sanitize_textarea_field( $_POST['proposed_description'] ?? '' ),
		'spacy_entity'         => $spacy_entity,
		'wikidata_id'          => sanitize_text_field( $_POST['wikidata_id']    ?? '' ) ?: null,
		'wikidata_label'       => sanitize_text_field( $_POST['wikidata_label'] ?? '' ) ?: null,
	];

	global $wpdb;
	$t = bm_tables();

	// ── Tag parent-category reassignment ───────────────────────────────────────
	// When a post_tag proposal gets a parent category selected, rebuild the
	// proposed_breadcrumb so the middle crumb is the real category name
	// (clickable via bm_breadcrumb_output) instead of the generic "Tag" label.
	$tag_parent_category_id = absint( $_POST['tag_parent_category_id'] ?? 0 );
	$proposed_breadcrumb    = null;

	$term_info = $wpdb->get_row( $wpdb->prepare(
		"SELECT t.original_name, t.taxonomy
		   FROM {$t['proposals']} p
		   JOIN {$t['terms']} t ON t.id = p.term_id
		  WHERE p.id = %d",
		$proposal_id
	) );

	if ( $term_info && $term_info->taxonomy === 'post_tag' ) {
		$fields['proposed_parent_id'] = $tag_parent_category_id ?: null;

		if ( $tag_parent_category_id ) {
			$cat = get_term( $tag_parent_category_id, 'category' );
			if ( $cat && ! is_wp_error( $cat ) ) {
				$crumbs              = [ 'Home', $cat->name, $term_info->original_name ];
				$proposed_breadcrumb = wp_json_encode( $crumbs );
				$fields['proposed_breadcrumb'] = $proposed_breadcrumb;
			}
		} else {
			// Cleared: reset to generic tag breadcrumb
			$crumbs              = [ 'Home', 'Tags', $term_info->original_name ];
			$proposed_breadcrumb = wp_json_encode( $crumbs );
			$fields['proposed_breadcrumb'] = $proposed_breadcrumb;
		}
	}

	$updated = $wpdb->update( $t['proposals'], $fields, [ 'id' => $proposal_id ] );

	if ( $updated === false ) {
		wp_send_json_error( [ 'message' => 'DB update failed.' ] );
	}

	// ── Sync to live WP term if already published ──────────────────────────────
	$wp_synced  = false;
	$sync_error = '';

	$term_row = $wpdb->get_row( $wpdb->prepare(
		"SELECT t.wp_term_id, t.taxonomy, t.status AS term_status
		   FROM {$t['proposals']} p
		   JOIN {$t['terms']} t ON t.id = p.term_id
		  WHERE p.id = %d",
		$proposal_id
	) );

	if ( $term_row && $term_row->term_status === 'published' ) {
		$update_args = [];
		if ( ! empty( $fields['proposed_name'] ) ) {
			$update_args['name'] = $fields['proposed_name'];
		}
		if ( ! empty( $fields['proposed_slug'] ) ) {
			$update_args['slug'] = $fields['proposed_slug'];
		}
		if ( isset( $fields['proposed_description'] ) ) {
			$update_args['description'] = $fields['proposed_description'];
		}

		if ( $update_args ) {
			$result    = wp_update_term( (int) $term_row->wp_term_id, $term_row->taxonomy, $update_args );
			$wp_synced = ! is_wp_error( $result );
			if ( is_wp_error( $result ) ) {
				$sync_error = $result->get_error_message();
			}
		}
	}

	wp_send_json_success( [
		'proposal_id'         => $proposal_id,
		'fields'              => $fields,
		'proposed_breadcrumb' => $proposed_breadcrumb,
		'wp_synced'           => $wp_synced,
		'sync_error'          => $sync_error,
	] );
}

// ── Update original term (Name + Slug in terms table) ─────────────────────────

function bm_ajax_update_original_term(): void {
	bm_verify_request();

	$term_id       = absint( $_POST['term_id']       ?? 0 );
	$original_name = sanitize_text_field( $_POST['original_name'] ?? '' );
	$original_slug = sanitize_title( $_POST['original_slug']      ?? '' );

	if ( ! $term_id || ! $original_name ) {
		wp_send_json_error( [ 'message' => 'Missing required fields.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$updated = $wpdb->update(
		$t['terms'],
		[
			'original_name' => $original_name,
			'original_slug' => $original_slug,
		],
		[ 'id' => $term_id ]
	);

	if ( $updated === false ) {
		wp_send_json_error( [ 'message' => 'DB update failed.' ] );
	}

	wp_send_json_success( [
		'term_id'       => $term_id,
		'original_name' => $original_name,
		'original_slug' => $original_slug,
	] );
}

// ── Update breadcrumb directly (proposed_breadcrumb in proposals table) ────────

function bm_ajax_update_breadcrumb(): void {
	bm_verify_request();

	$proposal_id = absint( $_POST['proposal_id'] ?? 0 );
	$crumbs_raw  = isset( $_POST['crumbs'] ) ? (array) $_POST['crumbs'] : [];

	if ( ! $proposal_id || empty( $crumbs_raw ) ) {
		wp_send_json_error( [ 'message' => 'Missing required fields.' ] );
	}

	$crumbs = array_values( array_filter(
		array_map( 'sanitize_text_field', $crumbs_raw ),
		fn( $c ) => $c !== ''
	) );

	if ( empty( $crumbs ) ) {
		wp_send_json_error( [ 'message' => 'Breadcrumb cannot be empty.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$breadcrumb_json = wp_json_encode( $crumbs );

	$updated = $wpdb->update(
		$t['proposals'],
		[ 'proposed_breadcrumb' => $breadcrumb_json ],
		[ 'id' => $proposal_id ]
	);

	if ( $updated === false ) {
		wp_send_json_error( [ 'message' => 'DB update failed.' ] );
	}

	wp_send_json_success( [
		'proposal_id'         => $proposal_id,
		'proposed_breadcrumb' => $breadcrumb_json,
		'crumbs'              => $crumbs,
	] );
}

// ── Empty all tables (Danger Zone) ────────────────────────────────────────────

function bm_ajax_empty_tables(): void {
	bm_verify_request();

	global $wpdb;
	$t = bm_tables();

	// Delete in FK-safe order: proposals → redirects → terms
	$wpdb->query( "DELETE FROM {$t['proposals']}" ); // phpcs:ignore
	$p = $wpdb->rows_affected;
	$wpdb->query( "DELETE FROM {$t['redirects']}" );  // phpcs:ignore
	$r = $wpdb->rows_affected;
	$wpdb->query( "DELETE FROM {$t['terms']}" );      // phpcs:ignore
	$te = $wpdb->rows_affected;

	wp_send_json_success( [
		'message' => sprintf(
			/* translators: 1: proposals, 2: redirects, 3: terms */
			__( 'Deleted: %1$d proposal(s), %2$d redirect(s), %3$d term(s).', 'breadcrumb-migration' ),
			$p, $r, $te
		),
		'counts'  => [ 'proposals' => $p, 'redirects' => $r, 'terms' => $te ],
	] );
}

// ── Wikidata label search (proxy) ─────────────────────────────────────────────

function bm_ajax_search_wikidata(): void {
	bm_verify_request();

	$query = sanitize_text_field( $_POST['query'] ?? '' );
	if ( ! $query ) {
		wp_send_json_error( [ 'message' => 'Empty query.' ] );
	}

	$bm_settings = get_option( 'bm_settings', [] );
	$lang        = $bm_settings['wikidata_lang'] ?? 'en';

	$api_url = add_query_arg( [
		'action'   => 'wbsearchentities',
		'search'   => $query,
		'language' => $lang,
		'uselang'  => $lang,
		'type'     => 'item',
		'limit'    => 5,
		'format'   => 'json',
	], 'https://www.wikidata.org/w/api.php' );

	$response = wp_remote_get( $api_url, [
		'timeout'    => 8,
		'user-agent' => 'BreadcrumbMigrationPlugin/1.8.0 (WordPress; ' . get_bloginfo( 'url' ) . ')',
	] );

	if ( is_wp_error( $response ) ) {
		wp_send_json_error( [ 'message' => 'Wikidata unreachable: ' . $response->get_error_message() ] );
	}

	$body = json_decode( wp_remote_retrieve_body( $response ), true );

	if ( ! isset( $body['search'] ) ) {
		wp_send_json_error( [ 'message' => 'Unexpected Wikidata API response.' ] );
	}

	$results = array_map( function ( $item ) {
		return [
			'id'          => $item['id']          ?? '',
			'label'       => $item['label']       ?? '',
			'description' => $item['description'] ?? '',
		];
	}, $body['search'] );

	wp_send_json_success( [ 'results' => $results ] );
}

// ── Delta: scan new tags ───────────────────────────────────────────────────────

function bm_ajax_scan_delta(): void {
	bm_verify_request();

	global $wpdb;
	$t = bm_tables();

	$raw_keywords = sanitize_textarea_field( wp_unslash( $_POST['keywords'] ?? '' ) );
	$keyword_filter = '';

	if ( '' !== $raw_keywords ) {
		$names = array_values( array_filter( array_map( 'trim', preg_split( '/[\r\n,]+/', $raw_keywords ) ) ) );
		if ( ! empty( $names ) ) {
			$placeholders   = implode( ', ', array_fill( 0, count( $names ), '%s' ) );
			$keyword_filter = $wpdb->prepare( " AND t.name IN ($placeholders)", $names ); // phpcs:ignore
		}
	}

	$rows = $wpdb->get_results( // phpcs:ignore
		"SELECT tt.term_id AS wp_term_id, t.name, t.slug, tt.count
		 FROM {$wpdb->term_taxonomy} tt
		 JOIN {$wpdb->terms} t ON t.term_id = tt.term_id
		 WHERE tt.taxonomy = 'post_tag'
		   AND tt.term_id NOT IN (
		       SELECT wp_term_id FROM {$t['terms']} WHERE taxonomy = 'post_tag'
		   )
		 {$keyword_filter}
		 ORDER BY t.name ASC",
		ARRAY_A
	);

	$rows = $rows ?: [];
	wp_send_json_success( [ 'tags' => $rows, 'count' => count( $rows ) ] );
}

// ── Delta: add single new tag to migration ─────────────────────────────────────

function bm_ajax_add_delta_term(): void {
	bm_verify_request();

	$wp_term_id = absint( $_POST['wp_term_id'] ?? 0 );
	if ( ! $wp_term_id ) {
		wp_send_json_error( [ 'message' => 'Missing wp_term_id.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$exists = $wpdb->get_var( $wpdb->prepare( // phpcs:ignore
		"SELECT id FROM {$t['terms']} WHERE wp_term_id = %d AND taxonomy = 'post_tag'",
		$wp_term_id
	) );
	if ( $exists ) {
		wp_send_json_error( [ 'message' => 'Term already tracked.' ] );
	}

	$wp_term = get_term( $wp_term_id, 'post_tag' );
	if ( ! $wp_term || is_wp_error( $wp_term ) ) {
		wp_send_json_error( [ 'message' => 'WP term not found.' ] );
	}

	$wpdb->insert( $t['terms'], [
		'wp_term_id'         => $wp_term_id,
		'taxonomy'           => 'post_tag',
		'original_name'      => $wp_term->name,
		'original_slug'      => $wp_term->slug,
		'original_parent_id' => $wp_term->parent ?: null,
		'content_count'      => $wp_term->count,
		'language'           => 'fr',
		'status'             => 'original',
	] );
	$term_internal_id = (int) $wpdb->insert_id;

	$proposed_name        = sanitize_text_field( $_POST['proposed_name'] ?? $wp_term->name );
	$proposed_slug        = sanitize_title( $_POST['proposed_slug'] ?? $wp_term->slug );
	$proposed_description = sanitize_textarea_field( $_POST['proposed_description'] ?? '' );
	$spacy_entity         = sanitize_text_field( $_POST['spacy_entity'] ?? '' );
	$wikidata_id          = sanitize_text_field( $_POST['wikidata_id'] ?? '' );
	$wikidata_label       = sanitize_text_field( $_POST['wikidata_label'] ?? '' );
	$wikidata_description = sanitize_textarea_field( $_POST['wikidata_description'] ?? '' );
	$tag_parent_cat_id    = absint( $_POST['tag_parent_category_id'] ?? 0 );

	$crumbs = [ 'Home', 'Tags', $wp_term->name ];
	if ( $tag_parent_cat_id ) {
		$cat = get_term( $tag_parent_cat_id, 'category' );
		if ( $cat && ! is_wp_error( $cat ) ) {
			$crumbs[1] = $cat->name;
		}
	}

	$wpdb->insert( $t['proposals'], [
		'term_id'              => $term_internal_id,
		'proposed_name'        => $proposed_name,
		'proposed_slug'        => $proposed_slug,
		'proposed_description' => $proposed_description ?: null,
		'proposed_parent_id'   => $tag_parent_cat_id ?: null,
		'proposed_language'    => 'fr',
		'spacy_entity'         => $spacy_entity ?: null,
		'wikidata_id'          => $wikidata_id ?: null,
		'wikidata_label'       => $wikidata_label ?: null,
		'wikidata_description' => $wikidata_description ?: null,
		'proposed_breadcrumb'  => wp_json_encode( $crumbs ),
		'validation_state'     => 'pending',
	] );

	wp_send_json_success( [
		'term_id'    => $term_internal_id,
		'wp_term_id' => $wp_term_id,
		'message'    => sprintf( '"%s" added to migration.', $wp_term->name ),
	] );
}

// ── Delta: bulk add multiple new tags to migration ────────────────────────────

function bm_ajax_bulk_add_delta_terms(): void {
	bm_verify_request();

	$raw = sanitize_text_field( wp_unslash( $_POST['terms'] ?? '' ) );
	if ( ! $raw ) {
		wp_send_json_error( [ 'message' => 'No terms provided.' ] );
	}

	$items = json_decode( stripslashes( $raw ), true );
	if ( ! is_array( $items ) || empty( $items ) ) {
		wp_send_json_error( [ 'message' => 'Invalid terms payload.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$added   = 0;
	$skipped = 0;
	$errors  = [];

	foreach ( $items as $item ) {
		$wp_term_id = absint( $item['wp_term_id'] ?? 0 );
		if ( ! $wp_term_id ) {
			$errors[] = 'Missing wp_term_id.';
			continue;
		}

		$exists = $wpdb->get_var( $wpdb->prepare( // phpcs:ignore
			"SELECT id FROM {$t['terms']} WHERE wp_term_id = %d AND taxonomy = 'post_tag'",
			$wp_term_id
		) );
		if ( $exists ) {
			$skipped++;
			continue;
		}

		$wp_term = get_term( $wp_term_id, 'post_tag' );
		if ( ! $wp_term || is_wp_error( $wp_term ) ) {
			$errors[] = sprintf( 'WP term %d not found.', $wp_term_id );
			continue;
		}

		$wpdb->insert( $t['terms'], [
			'wp_term_id'         => $wp_term_id,
			'taxonomy'           => 'post_tag',
			'original_name'      => $wp_term->name,
			'original_slug'      => $wp_term->slug,
			'original_parent_id' => $wp_term->parent ?: null,
			'content_count'      => $wp_term->count,
			'language'           => 'fr',
			'status'             => 'original',
		] );
		$term_internal_id = (int) $wpdb->insert_id;

		$proposed_name        = sanitize_text_field( $item['proposed_name'] ?? $wp_term->name );
		$proposed_slug        = sanitize_title( $item['proposed_slug'] ?? $wp_term->slug );
		$spacy_entity         = sanitize_text_field( $item['spacy_entity'] ?? '' );
		$wikidata_id          = sanitize_text_field( $item['wikidata_id'] ?? '' );
		$wikidata_label       = sanitize_text_field( $item['wikidata_label'] ?? '' );
		$wikidata_description = sanitize_textarea_field( $item['wikidata_description'] ?? '' );

		$wpdb->insert( $t['proposals'], [
			'term_id'              => $term_internal_id,
			'proposed_name'        => $proposed_name,
			'proposed_slug'        => $proposed_slug,
			'proposed_description' => null,
			'proposed_parent_id'   => null,
			'proposed_language'    => 'fr',
			'spacy_entity'         => $spacy_entity ?: null,
			'wikidata_id'          => $wikidata_id ?: null,
			'wikidata_label'       => $wikidata_label ?: null,
			'wikidata_description' => $wikidata_description ?: null,
			'proposed_breadcrumb'  => wp_json_encode( [ 'Home', 'Tags', $wp_term->name ] ),
			'validation_state'     => 'pending',
		] );

		$added++;
	}

	wp_send_json_success( [
		'added'   => $added,
		'skipped' => $skipped,
		'errors'  => $errors,
	] );
}

// ── Bulk Assign category to keywords ──────────────────────────────────────────

function bm_ajax_bulk_assign(): void {
	bm_verify_request();

	$raw_keywords = sanitize_textarea_field( $_POST['keywords'] ?? '' );
	$category_id  = absint( $_POST['category_id'] ?? 0 );

	if ( ! $raw_keywords ) {
		wp_send_json_error( [ 'message' => 'No keywords provided.' ] );
	}
	if ( ! $category_id ) {
		wp_send_json_error( [ 'message' => 'No category selected.' ] );
	}

	$cat = get_term( $category_id, 'category' );
	if ( ! $cat || is_wp_error( $cat ) ) {
		wp_send_json_error( [ 'message' => 'Category not found.' ] );
	}

	// Support newline and/or comma separation
	$lines    = preg_split( '/[\r\n,]+/', $raw_keywords );
	$keywords = [];
	foreach ( $lines as $line ) {
		$kw = trim( $line );
		if ( $kw !== '' ) {
			$keywords[] = $kw;
		}
	}
	$keywords = array_unique( $keywords );

	if ( empty( $keywords ) ) {
		wp_send_json_error( [ 'message' => 'No valid keywords after parsing.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$results = [];
	$updated = 0;
	$skipped = 0;

	foreach ( $keywords as $keyword ) {
		$term_row = $wpdb->get_row( $wpdb->prepare(
			"SELECT id, original_name FROM {$t['terms']}
			 WHERE taxonomy = 'post_tag' AND LOWER(original_name) = LOWER(%s)
			 LIMIT 1",
			$keyword
		) );

		if ( ! $term_row ) {
			$results[] = [
				'keyword' => $keyword,
				'status'  => 'not_found',
				'message' => 'Not found in migration DB.',
			];
			$skipped++;
			continue;
		}

		$term_internal_id = (int) $term_row->id;
		$crumbs           = [ 'Home', $cat->name, $term_row->original_name ];
		$breadcrumb_json  = wp_json_encode( $crumbs );

		$proposal = $wpdb->get_row( $wpdb->prepare(
			"SELECT id FROM {$t['proposals']} WHERE term_id = %d LIMIT 1",
			$term_internal_id
		) );

		$result_proposal_id = 0;

		if ( $proposal ) {
			$ok = $wpdb->update(
				$t['proposals'],
				[
					'proposed_parent_id'  => $category_id,
					'proposed_breadcrumb' => $breadcrumb_json,
				],
				[ 'id' => (int) $proposal->id ]
			);
			$status = ( $ok !== false ) ? 'updated' : 'error';
			if ( $status === 'updated' ) {
				$result_proposal_id = (int) $proposal->id;
			}
		} else {
			$ok = $wpdb->insert( $t['proposals'], [
				'term_id'             => $term_internal_id,
				'proposed_name'       => $term_row->original_name,
				'proposed_slug'       => sanitize_title( $term_row->original_name ),
				'proposed_parent_id'  => $category_id,
				'proposed_language'   => 'fr',
				'proposed_breadcrumb' => $breadcrumb_json,
				'validation_state'    => 'pending',
			] );
			$status = ( $ok !== false ) ? 'created' : 'error';
			if ( $status === 'created' ) {
				$result_proposal_id = (int) $wpdb->insert_id;
			}
		}

		if ( $status !== 'error' ) {
			$updated++;
		} else {
			$skipped++;
		}

		$results[] = [
			'keyword'     => $keyword,
			'status'      => $status,
			'breadcrumb'  => implode( ' › ', $crumbs ),
			'proposal_id' => $result_proposal_id,
		];
	}

	wp_send_json_success( [
		'results'  => $results,
		'updated'  => $updated,
		'skipped'  => $skipped,
		'total'    => count( $keywords ),
		'category' => $cat->name,
	] );
}

// ── Bulk Publish (approve + publish in one step) ──────────────────────────────

function bm_ajax_bulk_publish(): void {
	bm_verify_request();

	$raw_ids = isset( $_POST['proposal_ids'] ) ? (array) $_POST['proposal_ids'] : [];
	if ( empty( $raw_ids ) ) {
		wp_send_json_error( [ 'message' => 'No proposal IDs provided.' ] );
	}

	$proposal_ids = array_values( array_filter( array_map( 'absint', $raw_ids ) ) );
	if ( empty( $proposal_ids ) ) {
		wp_send_json_error( [ 'message' => 'No valid proposal IDs.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$results   = [];
	$published = 0;
	$errors    = 0;

	foreach ( $proposal_ids as $proposal_id ) {
		// Approve
		$wpdb->update(
			$t['proposals'],
			[
				'validation_state' => 'approved',
				'validated_by'     => get_current_user_id(),
				'validated_at'     => current_time( 'mysql' ),
			],
			[ 'id' => $proposal_id ]
		);

		// Load proposal + linked term
		$row = $wpdb->get_row( $wpdb->prepare(
			"SELECT p.*, t.wp_term_id, t.taxonomy, t.id AS term_internal_id
			 FROM {$t['proposals']} p
			 JOIN {$t['terms']} t ON t.id = p.term_id
			 WHERE p.id = %d",
			$proposal_id
		) );

		if ( ! $row ) {
			$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'error', 'message' => 'Proposal not found.' ];
			$errors++;
			continue;
		}

		$old_term = get_term( (int) $row->wp_term_id, $row->taxonomy );
		if ( is_wp_error( $old_term ) || ! $old_term ) {
			$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'error', 'message' => 'WP term not found.' ];
			$errors++;
			continue;
		}

		$old_url     = get_term_link( $old_term );
		$update_args = [ 'name' => $row->proposed_name ];
		if ( ! empty( $row->proposed_slug ) ) {
			$update_args['slug'] = $row->proposed_slug;
		}
		if ( ! empty( $row->proposed_description ) ) {
			$update_args['description'] = $row->proposed_description;
		}

		$result = wp_update_term( (int) $row->wp_term_id, $row->taxonomy, $update_args );
		if ( is_wp_error( $result ) ) {
			$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'error', 'message' => $result->get_error_message() ];
			$errors++;
			continue;
		}

		$new_term = get_term( (int) $row->wp_term_id, $row->taxonomy );
		$new_url  = get_term_link( $new_term );

		if ( ! is_wp_error( $old_url ) && ! is_wp_error( $new_url ) && $old_url !== $new_url ) {
			$wpdb->insert( $t['redirects'], [
				'original_url'  => $old_url,
				'new_url'       => $new_url,
				'term_id'       => (int) $row->term_internal_id,
				'taxonomy'      => $row->taxonomy,
				'redirect_type' => '301',
				'is_active'     => 1,
			] );
		}

		$wpdb->update(
			$t['terms'],
			[ 'status' => 'published', 'updated_at' => current_time( 'mysql' ) ],
			[ 'id' => (int) $row->term_internal_id ]
		);

		$results[] = [
			'proposal_id' => $proposal_id,
			'status'      => 'published',
			'name'        => $row->proposed_name,
			'new_url'     => is_wp_error( $new_url ) ? '' : $new_url,
		];
		$published++;
	}

	wp_send_json_success( [
		'results'   => $results,
		'published' => $published,
		'errors'    => $errors,
		'total'     => count( $proposal_ids ),
	] );
}

// ── Fetch Wikidata description by QID (Bulk Description tab) ─────────────────

function bm_ajax_fetch_wikidata_description(): void {
	bm_verify_request();

	$proposal_id = absint( $_POST['proposal_id'] ?? 0 );
	$raw_id      = sanitize_text_field( $_POST['wikidata_id'] ?? '' );
	$wikidata_id = strtoupper( trim( $raw_id ) );

	if ( ! $proposal_id || ! $wikidata_id ) {
		wp_send_json_error( [ 'message' => 'Missing parameters.' ] );
	}

	if ( ! preg_match( '/^Q\d+$/', $wikidata_id ) ) {
		wp_send_json_error( [ 'message' => 'Invalid Wikidata ID. Use Q followed by digits (e.g. Q42).' ] );
	}

	$bm_settings = get_option( 'bm_settings', [] );
	$lang        = $bm_settings['wikidata_lang'] ?? 'en';

	$api_url = add_query_arg( [
		'action'    => 'wbgetentities',
		'ids'       => $wikidata_id,
		'props'     => 'descriptions|labels',
		'languages' => $lang . '|en',
		'format'    => 'json',
	], 'https://www.wikidata.org/w/api.php' );

	$response = wp_remote_get( $api_url, [
		'timeout'    => 8,
		'user-agent' => 'BreadcrumbMigrationPlugin/1.14.0 (WordPress; ' . get_bloginfo( 'url' ) . ')',
	] );

	if ( is_wp_error( $response ) ) {
		wp_send_json_error( [ 'message' => 'Wikidata unreachable: ' . $response->get_error_message() ] );
	}

	$body        = json_decode( wp_remote_retrieve_body( $response ), true );
	$entity_data = $body['entities'][ $wikidata_id ] ?? null;

	if ( ! $entity_data || isset( $entity_data['missing'] ) ) {
		wp_send_json_error( [ 'message' => 'Entity not found on Wikidata.' ] );
	}

	$description = $entity_data['descriptions'][ $lang ]['value']
		?? $entity_data['descriptions']['en']['value']
		?? '';

	$label = $entity_data['labels'][ $lang ]['value']
		?? $entity_data['labels']['en']['value']
		?? '';

	global $wpdb;
	$t = bm_tables();

	$wpdb->update(
		$t['proposals'],
		[
			'wikidata_id'          => $wikidata_id,
			'wikidata_description' => $description ?: null,
			'wikidata_label'       => $label ?: null,
		],
		[ 'id' => $proposal_id ]
	);

	wp_send_json_success( [
		'proposal_id' => $proposal_id,
		'wikidata_id' => $wikidata_id,
		'description' => $description,
		'label'       => $label,
	] );
}

// ── Bulk save Wikidata description → proposed_description + WP term ───────────

function bm_ajax_bulk_save_description(): void {
	bm_verify_request();

	$raw_ids = isset( $_POST['proposal_ids'] ) ? (array) $_POST['proposal_ids'] : [];
	if ( empty( $raw_ids ) ) {
		wp_send_json_error( [ 'message' => 'No proposal IDs provided.' ] );
	}

	$proposal_ids = array_values( array_filter( array_map( 'absint', $raw_ids ) ) );
	if ( empty( $proposal_ids ) ) {
		wp_send_json_error( [ 'message' => 'No valid proposal IDs.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$results = [];
	$saved   = 0;
	$errors  = 0;

	foreach ( $proposal_ids as $proposal_id ) {
		$row = $wpdb->get_row( $wpdb->prepare(
			"SELECT p.wikidata_description, t.wp_term_id, t.taxonomy
			   FROM {$t['proposals']} p
			   JOIN {$t['terms']} t ON t.id = p.term_id
			  WHERE p.id = %d AND p.validation_state = 'approved'",
			$proposal_id
		) );

		if ( ! $row ) {
			$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'error', 'message' => 'Proposal not found or not approved.' ];
			$errors++;
			continue;
		}

		if ( empty( $row->wikidata_description ) ) {
			$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'skipped', 'message' => 'No Wikidata description to save.' ];
			$errors++;
			continue;
		}

		$ok = $wpdb->update(
			$t['proposals'],
			[ 'proposed_description' => $row->wikidata_description ],
			[ 'id' => $proposal_id ]
		);

		if ( $ok === false ) {
			$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'error', 'message' => 'DB update failed.' ];
			$errors++;
			continue;
		}

		$result = wp_update_term( (int) $row->wp_term_id, $row->taxonomy, [
			'description' => $row->wikidata_description,
		] );

		if ( is_wp_error( $result ) ) {
			$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'error', 'message' => 'WP sync failed: ' . $result->get_error_message() ];
			$errors++;
			continue;
		}

		$results[] = [ 'proposal_id' => $proposal_id, 'status' => 'saved', 'description' => $row->wikidata_description ];
		$saved++;
	}

	wp_send_json_success( [
		'results' => $results,
		'saved'   => $saved,
		'errors'  => $errors,
		'total'   => count( $proposal_ids ),
	] );
}

// ── Sync WP descriptions → proposed_description ───────────────────────────────

function bm_ajax_sync_descriptions(): void {
	bm_verify_request();

	global $wpdb;
	$t = bm_tables();

	$rows = $wpdb->get_results( // phpcs:ignore
		"SELECT p.id AS proposal_id, p.proposed_description, p.wikidata_description,
		        t.wp_term_id, t.taxonomy
		 FROM {$t['proposals']} p
		 JOIN {$t['terms']} t ON t.id = p.term_id
		 WHERE p.validation_state = 'approved'"
	);

	$updated      = 0;
	$skipped      = 0;
	$descriptions = [];

	foreach ( $rows as $row ) {
		$pid           = (int) $row->proposal_id;
		$proposed_desc = $row->proposed_description ?? '';
		$wikidata_desc = $row->wikidata_description ?? '';

		// Skip manually written descriptions — user authored content takes priority.
		$is_manual = $proposed_desc !== '' && ( $wikidata_desc === '' || $proposed_desc !== $wikidata_desc );
		if ( $is_manual ) {
			$descriptions[ $pid ] = [ 'description' => $proposed_desc, 'is_manual' => true, 'skipped' => true ];
			$skipped++;
			continue;
		}

		$term = get_term( (int) $row->wp_term_id, $row->taxonomy );
		if ( ! $term || is_wp_error( $term ) ) {
			continue;
		}

		$wp_desc = $term->description ?? '';

		$wpdb->update(
			$t['proposals'],
			[ 'proposed_description' => $wp_desc ?: null ],
			[ 'id' => $pid ]
		);

		$descriptions[ $pid ] = [ 'description' => $wp_desc, 'is_manual' => false, 'skipped' => false ];
		$updated++;
	}

	wp_send_json_success( [
		'descriptions' => $descriptions,
		'updated'      => $updated,
		'skipped'      => $skipped,
	] );
}

// ── Refresh single row description from WordPress ─────────────────────────────

function bm_ajax_refresh_single_description(): void {
	bm_verify_request();

	$proposal_id = absint( $_POST['proposal_id'] ?? 0 );
	if ( ! $proposal_id ) {
		wp_send_json_error( [ 'message' => 'Missing proposal_id.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$row = $wpdb->get_row( $wpdb->prepare(
		"SELECT p.wikidata_description, t.wp_term_id, t.taxonomy
		 FROM {$t['proposals']} p
		 JOIN {$t['terms']} t ON t.id = p.term_id
		 WHERE p.id = %d AND p.validation_state = 'approved'",
		$proposal_id
	) );

	if ( ! $row ) {
		wp_send_json_error( [ 'message' => 'Proposal not found or not approved.' ] );
	}

	$term = get_term( (int) $row->wp_term_id, $row->taxonomy );
	if ( ! $term || is_wp_error( $term ) ) {
		wp_send_json_error( [ 'message' => 'WordPress term not found.' ] );
	}

	$wp_desc      = $term->description ?? '';
	$wikidata_desc = $row->wikidata_description ?? '';

	$wpdb->update(
		$t['proposals'],
		[ 'proposed_description' => $wp_desc ?: null ],
		[ 'id' => $proposal_id ]
	);

	$is_manual = $wp_desc !== '' && ( $wikidata_desc === '' || $wp_desc !== $wikidata_desc );

	wp_send_json_success( [
		'proposal_id' => $proposal_id,
		'description' => $wp_desc,
		'is_manual'   => $is_manual,
	] );
}

// ── Publish to WordPress ───────────────────────────────────────────────────────

function bm_ajax_publish_term(): void {
	bm_verify_request();

	$proposal_id = absint( $_POST['proposal_id'] ?? 0 );
	if ( ! $proposal_id ) {
		wp_send_json_error( [ 'message' => 'Missing proposal_id.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	// Load proposal + term (only approved proposals)
	$row = $wpdb->get_row( $wpdb->prepare(
		"SELECT p.*, t.wp_term_id, t.taxonomy, t.id AS term_internal_id
		 FROM {$t['proposals']} p
		 JOIN {$t['terms']} t ON t.id = p.term_id
		 WHERE p.id = %d AND p.validation_state = 'approved'",
		$proposal_id
	) );

	if ( ! $row ) {
		wp_send_json_error( [ 'message' => 'Proposal not found or not approved.' ] );
	}

	// Capture old URL before update
	$old_term = get_term( (int) $row->wp_term_id, $row->taxonomy );
	if ( is_wp_error( $old_term ) || ! $old_term ) {
		wp_send_json_error( [ 'message' => 'WP term not found.' ] );
	}
	$old_url = get_term_link( $old_term );

	// Update WP term
	$update_args = [ 'name' => $row->proposed_name ];
	if ( ! empty( $row->proposed_slug ) ) {
		$update_args['slug'] = $row->proposed_slug;
	}
	if ( ! empty( $row->proposed_description ) ) {
		$update_args['description'] = $row->proposed_description;
	}

	$result = wp_update_term( (int) $row->wp_term_id, $row->taxonomy, $update_args );

	if ( is_wp_error( $result ) ) {
		wp_send_json_error( [ 'message' => $result->get_error_message() ] );
	}

	// New URL after slug change
	$new_term = get_term( (int) $row->wp_term_id, $row->taxonomy );
	$new_url  = get_term_link( $new_term );

	// Store redirect if URL changed
	if ( ! is_wp_error( $old_url ) && ! is_wp_error( $new_url ) && $old_url !== $new_url ) {
		$wpdb->insert( $t['redirects'], [
			'original_url'  => $old_url,
			'new_url'       => $new_url,
			'term_id'       => (int) $row->term_internal_id,
			'taxonomy'      => $row->taxonomy,
			'redirect_type' => '301',
			'is_active'     => 1,
		] );
	}

	// Mark term as published
	$wpdb->update(
		$t['terms'],
		[ 'status' => 'published', 'updated_at' => current_time( 'mysql' ) ],
		[ 'id' => (int) $row->term_internal_id ]
	);

	wp_send_json_success( [
		'proposal_id' => $proposal_id,
		'new_url'     => is_wp_error( $new_url ) ? '' : $new_url,
		'message'     => sprintf(
			/* translators: %s: term name */
			__( '"%s" published successfully.', 'breadcrumb-migration' ),
			$row->proposed_name
		),
	] );
}

// ── Bulk check existing parent-category assignments (read-only) ───────────────

function bm_ajax_bulk_check(): void {
	bm_verify_request();

	$keywords_raw = sanitize_textarea_field( $_POST['keywords'] ?? '' );
	if ( ! $keywords_raw ) {
		wp_send_json_error( [ 'message' => 'No keywords provided.' ] );
	}

	$keywords = array_values( array_unique( array_filter(
		array_map( 'trim', preg_split( '/[\n\r,]+/', $keywords_raw ) )
	) ) );

	if ( empty( $keywords ) ) {
		wp_send_json_error( [ 'message' => 'No valid keywords.' ] );
	}

	global $wpdb;
	$t = bm_tables();

	$results = [];
	foreach ( $keywords as $kw ) {
		$row = $wpdb->get_row( $wpdb->prepare(
			"SELECT t.id, p.id AS proposal_id, p.proposed_parent_id
			 FROM {$t['terms']} t
			 LEFT JOIN {$t['proposals']} p ON p.term_id = t.id
			 WHERE t.taxonomy = 'post_tag'
			   AND (t.original_name = %s OR t.original_slug = %s)
			 LIMIT 1",
			$kw,
			sanitize_title( $kw )
		) );

		if ( ! $row ) {
			$results[] = [
				'keyword'     => $kw,
				'found'       => false,
				'parent_id'   => null,
				'parent_name' => null,
			];
			continue;
		}

		$parent_id   = (int) ( $row->proposed_parent_id ?? 0 );
		$parent_name = null;
		if ( $parent_id ) {
			$cat = get_term( $parent_id, 'category' );
			$parent_name = ( $cat && ! is_wp_error( $cat ) ) ? $cat->name : null;
		}

		$results[] = [
			'keyword'     => $kw,
			'found'       => true,
			'parent_id'   => $parent_id ?: null,
			'parent_name' => $parent_name,
		];
	}

	wp_send_json_success( [ 'results' => $results, 'total' => count( $results ) ] );
}
