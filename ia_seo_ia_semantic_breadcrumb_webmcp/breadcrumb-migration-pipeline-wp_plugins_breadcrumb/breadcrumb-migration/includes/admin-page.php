<?php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// ── Tab navigation ─────────────────────────────────────────────────────────────

function bm_render_tabs( string $base_url, string $current ): void {
	$tabs = [
		'proposals'        => __( 'Proposals', 'breadcrumb-migration' ),
		'delta'            => __( 'Delta — New Tags', 'breadcrumb-migration' ),
		'bulk_assign'      => __( 'Bulk Assign', 'breadcrumb-migration' ),
		'bulk_description' => __( 'Bulk Description', 'breadcrumb-migration' ),
		'help_wikidata'    => __( 'Help — Wikidata', 'breadcrumb-migration' ),
		'import'           => __( 'Import & Export', 'breadcrumb-migration' ),
		'settings'         => __( 'Settings', 'breadcrumb-migration' ),
		'danger'           => __( 'Danger Zone', 'breadcrumb-migration' ),
	];
	echo '<nav class="nav-tab-wrapper bm-tab-nav">';
	foreach ( $tabs as $slug => $label ) {
		$cls = 'nav-tab' . ( $current === $slug ? ' nav-tab-active' : '' );
		if ( $slug === 'danger' ) {
			$cls .= ' bm-tab-danger';
		}
		printf(
			'<a href="%s" class="%s">%s</a>',
			esc_url( add_query_arg( 'tab', $slug, $base_url ) ),
			esc_attr( $cls ),
			esc_html( $label )
		);
	}
	echo '</nav>';
}

// ── Render main admin page ─────────────────────────────────────────────────────

function bm_render_admin_page(): void {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$base_url    = admin_url( 'admin.php?page=breadcrumb-migration' );
	$current_tab = sanitize_key( $_GET['tab'] ?? 'proposals' );

	?>
	<div class="wrap bm-wrap">
		<h1 class="wp-heading-inline">
			<?php esc_html_e( 'Breadcrumb Migration', 'breadcrumb-migration' ); ?>
		</h1>
		<hr class="wp-header-end">

		<?php bm_render_tabs( $base_url, $current_tab ); ?>

		<?php
		if ( $current_tab === 'delta' ) {
			bm_render_tab_delta();
		} elseif ( $current_tab === 'bulk_assign' ) {
			bm_render_tab_bulk_assign();
		} elseif ( $current_tab === 'bulk_description' ) {
			bm_render_tab_bulk_description();
		} elseif ( $current_tab === 'help_wikidata' ) {
			bm_render_tab_help_wikidata();
		} elseif ( $current_tab === 'import' ) {
			bm_render_tab_import();
		} elseif ( $current_tab === 'settings' ) {
			bm_render_tab_settings();
		} elseif ( $current_tab === 'danger' ) {
			bm_render_tab_danger();
		} else {
			bm_render_tab_proposals( $base_url );
		}
		?>
	</div>
	<?php
}

// ── Proposals tab ──────────────────────────────────────────────────────────────

function bm_render_tab_proposals( string $base_url ): void {
	global $wpdb;
	$t = bm_tables();

	// ── Filters ────────────────────────────────────────────────────────────────
	$filter_taxonomy    = sanitize_text_field( $_GET['bm_taxonomy']    ?? 'all' );
	$filter_state       = sanitize_text_field( $_GET['bm_state']       ?? 'all' );
	$search             = sanitize_text_field( $_GET['bm_search']      ?? '' );
	$filter_wikidata_id = sanitize_text_field( $_GET['bm_wikidata_id'] ?? '' );
	$filter_spacy         = sanitize_text_field( $_GET['bm_spacy']          ?? '' );
	$filter_bulk_keywords = sanitize_textarea_field( $_GET['bm_bulk_keywords'] ?? '' );
	$bulk_kws = [];
	if ( $filter_bulk_keywords !== '' ) {
		$bulk_kws = array_values( array_filter(
			array_map( 'trim', preg_split( '/[,\n\r]+/', $filter_bulk_keywords ) ),
			fn( $v ) => $v !== ''
		) );
	}
	$per_page        = 20;
	$current_page    = max( 1, absint( $_GET['paged'] ?? 1 ) );
	$offset          = ( $current_page - 1 ) * $per_page;

	// ── Build WHERE ────────────────────────────────────────────────────────────
	$where  = 'WHERE 1=1';
	$params = [];

	if ( $filter_taxonomy !== 'all' ) {
		$where   .= ' AND t.taxonomy = %s';
		$params[] = $filter_taxonomy;
	}
	if ( $filter_state !== 'all' ) {
		$where   .= ' AND COALESCE(p.validation_state, "pending") = %s';
		$params[] = $filter_state;
	}
	if ( $search !== '' ) {
		$where   .= ' AND (t.original_name LIKE %s OR t.original_slug LIKE %s)';
		$like     = '%' . $wpdb->esc_like( $search ) . '%';
		$params[] = $like;
		$params[] = $like;
	}
	if ( $filter_wikidata_id !== '' ) {
		$where   .= ' AND p.wikidata_id LIKE %s';
		$params[] = '%' . $wpdb->esc_like( $filter_wikidata_id ) . '%';
	}
	if ( $filter_spacy !== '' ) {
		$where   .= ' AND p.spacy_entity = %s';
		$params[] = $filter_spacy;
	}

	// ── Count ──────────────────────────────────────────────────────────────────
	$count_sql = "SELECT COUNT(*) FROM {$t['terms']} t
		LEFT JOIN {$t['proposals']} p ON p.term_id = t.id
		$where";
	$total = (int) ( $params
		? $wpdb->get_var( $wpdb->prepare( $count_sql, ...$params ) )
		: $wpdb->get_var( $count_sql )
	);

	// ── Fetch rows ─────────────────────────────────────────────────────────────
	$data_sql = "SELECT
		t.id AS term_internal_id, t.wp_term_id, t.taxonomy,
		t.original_name, t.original_slug, t.original_parent_id,
		t.content_count, t.status AS term_status,
		p.id AS proposal_id,
		p.proposed_name, p.proposed_slug, p.proposed_description,
		p.proposed_parent_id,
		p.spacy_entity,
		p.wikidata_id, p.wikidata_label, p.wikidata_description,
		p.proposed_breadcrumb, p.validation_state
	FROM {$t['terms']} t
	LEFT JOIN {$t['proposals']} p ON p.term_id = t.id
	$where
	ORDER BY t.taxonomy ASC, t.original_name ASC
	LIMIT %d OFFSET %d";

	$limit_params = array_merge( $params, [ $per_page, $offset ] );
	$rows = $params
		? $wpdb->get_results( $wpdb->prepare( $data_sql, ...$limit_params ) )
		: $wpdb->get_results( $wpdb->prepare( $data_sql, $per_page, $offset ) );

	// ── Stats ──────────────────────────────────────────────────────────────────
	$stats = $wpdb->get_results(
		"SELECT COALESCE(p.validation_state,'pending') AS state, COUNT(*) AS cnt
		 FROM {$t['terms']} t
		 LEFT JOIN {$t['proposals']} p ON p.term_id = t.id
		 GROUP BY state"
	);
	$stat_map = [];
	foreach ( $stats as $s ) {
		$stat_map[ $s->state ] = (int) $s->cnt;
	}

	bm_render_stats( $stat_map );
	bm_render_status_tag_browser();
	bm_render_filters( $base_url, $filter_taxonomy, $filter_state, $search, $filter_wikidata_id, $filter_spacy, $filter_bulk_keywords );

	// ── Bulk keyword results mode ──────────────────────────────────────────────
	if ( ! empty( $bulk_kws ) ) {
		bm_render_proposals_bulk_results( $bulk_kws, $wpdb, $t );
		return;
	}

	if ( empty( $rows ) ) {
		?>
		<div class="bm-empty">
			<?php if ( $total === 0 && $filter_taxonomy === 'all' && $search === '' && $filter_wikidata_id === '' && $filter_spacy === '' ) : ?>
				<p><?php esc_html_e( 'No terms found. Run the pipeline then import via the Import & Export tab, or run Step 4 with --no-dry-run.', 'breadcrumb-migration' ); ?></p>
				<code>python source/pipeline/004_step_4_breadcrumb_proposal.py --auto-input --no-dry-run</code>
			<?php else : ?>
				<p><?php esc_html_e( 'No terms match your filters.', 'breadcrumb-migration' ); ?></p>
			<?php endif; ?>
		</div>
		<?php
	} else {
		bm_render_wp_pagination( $total, $per_page, $current_page, $base_url, $filter_taxonomy, $filter_state, $search, $filter_wikidata_id, $filter_spacy, 'top' );
		?>
		<div class="bm-term-list">
			<?php foreach ( $rows as $row ) : ?>
				<?php bm_render_term_card( $row ); ?>
			<?php endforeach; ?>
		</div>
		<?php
		bm_render_wp_pagination( $total, $per_page, $current_page, $base_url, $filter_taxonomy, $filter_state, $search, $filter_wikidata_id, $filter_spacy, 'bottom' );
	}
}

// ── Proposals — Bulk keyword results ──────────────────────────────────────────

function bm_render_proposals_bulk_results( array $bulk_kws, object $wpdb, array $t ): void {
	$count       = count( $bulk_kws );
	$not_found   = [];
	$card_rows   = [];

	// Build a normalised map: lowercase → original keyword
	$kw_lower_map = [];
	foreach ( $bulk_kws as $kw ) {
		$kw_lower_map[ mb_strtolower( $kw, 'UTF-8' ) ] = $kw;
	}

	// Fetch full card data for all matching keywords in one query
	if ( ! empty( $kw_lower_map ) ) {
		$placeholders = implode( ', ', array_fill( 0, count( $kw_lower_map ), '%s' ) );
		$sql = "SELECT
			t.id AS term_internal_id, t.wp_term_id, t.taxonomy,
			t.original_name, t.original_slug, t.original_parent_id,
			t.content_count, t.status AS term_status,
			p.id AS proposal_id,
			p.proposed_name, p.proposed_slug, p.proposed_description,
			p.proposed_parent_id,
			p.spacy_entity,
			p.wikidata_id, p.wikidata_label, p.wikidata_description,
			p.proposed_breadcrumb, p.validation_state
		FROM {$t['terms']} t
		LEFT JOIN {$t['proposals']} p ON p.term_id = t.id
		WHERE LOWER(t.original_name) IN ( $placeholders )
		ORDER BY t.original_name ASC";

		$results = $wpdb->get_results(
			$wpdb->prepare( $sql, ...array_keys( $kw_lower_map ) )
		);

		// Index results by lowercase name for lookup
		$result_map = [];
		foreach ( $results as $r ) {
			$result_map[ mb_strtolower( $r->original_name, 'UTF-8' ) ] = $r;
		}

		// Preserve the user's input order; split found / not-found
		foreach ( $kw_lower_map as $lower => $original ) {
			if ( isset( $result_map[ $lower ] ) ) {
				$card_rows[] = $result_map[ $lower ];
			} else {
				$not_found[] = $original;
			}
		}
	}

	$found = count( $card_rows );
	?>
	<div class="bm-proposals-bulk-results">
		<h3 class="bm-proposals-bulk-results__title">
			<?php
			printf(
				/* translators: 1: total searched, 2: found in DB */
				esc_html__( 'Bulk Search Results — %1$d searched, %2$d found in database', 'breadcrumb-migration' ),
				$count,
				$found
			);
			?>
		</h3>

		<?php if ( ! empty( $not_found ) ) : ?>
		<div class="notice notice-warning inline bm-bulk-not-found-notice">
			<p>
				<strong><?php esc_html_e( 'Not found in database:', 'breadcrumb-migration' ); ?></strong>
				<?php echo esc_html( implode( ', ', $not_found ) ); ?>
			</p>
		</div>
		<?php endif; ?>

		<?php if ( ! empty( $card_rows ) ) : ?>
		<div class="bm-term-list">
			<?php foreach ( $card_rows as $row ) : ?>
				<?php bm_render_term_card( $row ); ?>
			<?php endforeach; ?>
		</div>
		<?php else : ?>
		<p class="bm-no-data"><?php esc_html_e( 'No matching terms found for the keywords entered.', 'breadcrumb-migration' ); ?></p>
		<?php endif; ?>

	</div>
	<?php
}

// ── Delta — New Tags tab ───────────────────────────────────────────────────────

function bm_render_tab_delta(): void {
	global $wpdb;
	$t = bm_tables();

	$tracked  = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$t['terms']} WHERE taxonomy = 'post_tag'" ); // phpcs:ignore
	$total_wp = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->term_taxonomy} WHERE taxonomy = 'post_tag'" ); // phpcs:ignore
	?>
	<div class="bm-section">
		<h2><?php esc_html_e( 'Delta — New Tags', 'breadcrumb-migration' ); ?></h2>
		<p>
			<?php printf(
				/* translators: 1: total WP tags, 2: tracked in plugin */
				esc_html__( '%1$d post_tag(s) in WordPress · %2$d tracked in migration DB.', 'breadcrumb-migration' ),
				$total_wp,
				$tracked
			); ?>
		</p>
		<p class="description">
			<?php esc_html_e( 'Scan detects tags present in WordPress but not yet tracked. Fill spaCy entity and Wikidata fields manually, then add to migration. The tag will appear in the Proposals tab for validation.', 'breadcrumb-migration' ); ?>
		</p>

		<div class="bm-bulk-step" style="margin-bottom: 16px;">
			<label for="bm-delta-keywords" style="display:block; font-weight:600; margin-bottom:4px;">
				<?php esc_html_e( 'Filter by keywords (optional)', 'breadcrumb-migration' ); ?>
			</label>
			<p class="description" style="margin-bottom:6px;">
				<?php esc_html_e( 'Paste a comma or newline-separated list of tag names. Scan will be limited to these tags only. Leave empty to scan all tags.', 'breadcrumb-migration' ); ?>
			</p>
			<textarea id="bm-delta-keywords" rows="5" class="large-text"
				placeholder="<?php esc_attr_e( 'Applied computing, Automatic fact-checking, BeautifulSoup, Clickbait detection, Credibility…', 'breadcrumb-migration' ); ?>"></textarea>
		</div>

		<button class="button button-primary bm-btn-scan-delta">
			<?php esc_html_e( 'Scan for new tags', 'breadcrumb-migration' ); ?>
		</button>
		<div id="bm-delta-results" style="margin-top: 16px;"></div>
	</div>
	<?php
}

// ── Bulk Assign tab ────────────────────────────────────────────────────────────

function bm_render_tab_bulk_assign(): void {
	$all_cats = get_terms( [
		'taxonomy'   => 'category',
		'hide_empty' => false,
		'orderby'    => 'name',
		'number'     => 0,
	] );
	?>
	<div class="bm-section">
		<h2><?php esc_html_e( 'Bulk Assign Category', 'breadcrumb-migration' ); ?></h2>

		<!-- ── Step 1: Keyword Lookup ──────────────────────────────────────── -->
		<section class="bm-bulk-step bm-bulk-step--1" aria-label="<?php esc_attr_e( 'Step 1: Keyword Lookup', 'breadcrumb-migration' ); ?>">
			<h3 class="bm-bulk-step__title">
				<span class="bm-step-badge">1</span>
				<?php esc_html_e( 'Search Keywords — Check Existing Assignments', 'breadcrumb-migration' ); ?>
			</h3>
			<p class="description">
				<?php esc_html_e( 'Paste keywords (one per line or comma-separated), then click "Check" to preview which already have a parent category assigned in the migration database.', 'breadcrumb-migration' ); ?>
			</p>
			<div class="bm-bulk-form__field">
				<label for="bm-bulk-keywords">
					<strong><?php esc_html_e( 'Keywords', 'breadcrumb-migration' ); ?></strong>
					<span class="description"><?php esc_html_e( 'One per line or comma-separated', 'breadcrumb-migration' ); ?></span>
				</label>
				<textarea id="bm-bulk-keywords" rows="10" class="bm-bulk-keywords"
					placeholder="<?php esc_attr_e( 'One keyword per line, e.g.&#10;Tunisian Arabic&#10;Whisper&#10;Wordpress&#10;Yoruba&#10;Zulu', 'breadcrumb-migration' ); ?>"></textarea>
			</div>
			<div class="bm-bulk-step__actions">
				<button type="button" class="button bm-btn-bulk-check">
					<?php esc_html_e( 'Check Current Assignments', 'breadcrumb-migration' ); ?>
				</button>
			</div>
			<div id="bm-bulk-check-results" style="display:none;" class="bm-bulk-check-results"></div>
		</section>

		<!-- ── Step 2: Assign Category ─────────────────────────────────────── -->
		<section class="bm-bulk-step bm-bulk-step--2" aria-label="<?php esc_attr_e( 'Step 2: Assign Category', 'breadcrumb-migration' ); ?>">
			<h3 class="bm-bulk-step__title">
				<span class="bm-step-badge">2</span>
				<?php esc_html_e( 'Assign Parent Category to Keywords', 'breadcrumb-migration' ); ?>
			</h3>
			<p class="description">
				<?php esc_html_e( 'Select a parent category, then click Assign. Only the keywords checked in the Step 1 results table are sent — keywords that already have a parent category assigned will not be overwritten unless you explicitly checked them.', 'breadcrumb-migration' ); ?>
			</p>
			<div class="bm-bulk-form__field">
				<label for="bm-bulk-category">
					<strong><?php esc_html_e( 'Parent Category', 'breadcrumb-migration' ); ?></strong>
					<span class="description"><?php esc_html_e( 'Will be set as breadcrumb parent for all matched keywords', 'breadcrumb-migration' ); ?></span>
				</label>
				<select id="bm-bulk-category" class="bm-bulk-category">
					<option value="0"><?php esc_html_e( '— select a category —', 'breadcrumb-migration' ); ?></option>
					<?php foreach ( $all_cats as $cat ) : ?>
						<option value="<?php echo esc_attr( $cat->term_id ); ?>">
							<?php echo esc_html( $cat->name ); ?>
						</option>
					<?php endforeach; ?>
				</select>
			</div>
			<div class="bm-bulk-step__actions">
				<button type="button" class="button button-primary bm-btn-bulk-assign">
					<?php esc_html_e( 'Assign Category to Keywords', 'breadcrumb-migration' ); ?>
				</button>
			</div>
			<div id="bm-bulk-results" style="display:none;" class="bm-bulk-results"></div>
		</section>
	</div>
	<?php
}

// ── Bulk Description tab ───────────────────────────────────────────────────────

function bm_render_tab_bulk_description(): void {
	global $wpdb;
	$t = bm_tables();

	$search_desc   = sanitize_text_field( $_GET['bm_desc_search'] ?? '' );
	$per_page_desc = 20;
	$current_page  = max( 1, absint( $_GET['paged'] ?? 1 ) );
	$offset        = ( $current_page - 1 ) * $per_page_desc;
	$base_url      = admin_url( 'admin.php?page=breadcrumb-migration' );
	$base_url_desc = add_query_arg( 'tab', 'bulk_description', $base_url );
	$bm_settings   = get_option( 'bm_settings', [] );

	$where_desc   = "WHERE p.validation_state = 'approved'";
	$where_params = [];
	if ( $search_desc !== '' ) {
		$where_desc    .= ' AND (t.original_name LIKE %s OR t.original_slug LIKE %s)';
		$like           = '%' . $wpdb->esc_like( $search_desc ) . '%';
		$where_params[] = $like;
		$where_params[] = $like;
	}

	$count_sql  = "SELECT COUNT(*) FROM {$t['proposals']} p JOIN {$t['terms']} t ON t.id = p.term_id $where_desc";
	$total_desc = (int) ( $where_params
		? $wpdb->get_var( $wpdb->prepare( $count_sql, ...$where_params ) )
		: $wpdb->get_var( $count_sql ) // phpcs:ignore
	);

	$data_sql     = "SELECT p.id AS proposal_id, p.wikidata_id, p.wikidata_description,
		                    p.proposed_description, p.proposed_slug,
		                    t.wp_term_id, t.original_name, t.status AS term_status
		             FROM {$t['proposals']} p
		             JOIN {$t['terms']} t ON t.id = p.term_id
		             $where_desc
		             ORDER BY t.original_name ASC
		             LIMIT %d OFFSET %d";
	$limit_params = array_merge( $where_params, [ $per_page_desc, $offset ] );
	$rows         = $where_params
		? $wpdb->get_results( $wpdb->prepare( $data_sql, ...$limit_params ) )
		: $wpdb->get_results( $wpdb->prepare( $data_sql, $per_page_desc, $offset ) ); // phpcs:ignore
	?>
	<div class="bm-section">
		<h2><?php esc_html_e( 'Bulk Description', 'breadcrumb-migration' ); ?></h2>

		<!-- ── Server-side search ────────────────────────────────────────────── -->
		<form method="get" action="<?php echo esc_url( admin_url( 'admin.php' ) ); ?>" class="bm-desc-server-search">
			<input type="hidden" name="page" value="breadcrumb-migration">
			<input type="hidden" name="tab" value="bulk_description">
			<p class="search-box">
				<label class="screen-reader-text" for="bm-desc-server-search-input">
					<?php esc_html_e( 'Search Tags:', 'breadcrumb-migration' ); ?>
				</label>
				<input type="search" id="bm-desc-server-search-input" name="bm_desc_search"
					value="<?php echo esc_attr( $search_desc ); ?>"
					placeholder="<?php esc_attr_e( 'Search tag name or slug…', 'breadcrumb-migration' ); ?>">
				<input type="submit" id="bm-desc-search-submit-server" class="button"
					value="<?php esc_attr_e( 'Search Tags', 'breadcrumb-migration' ); ?>">
				<?php if ( $search_desc !== '' ) : ?>
					<a href="<?php echo esc_url( $base_url_desc ); ?>" class="button bm-desc-search-clear">
						✕ <?php esc_html_e( 'Clear', 'breadcrumb-migration' ); ?>
					</a>
				<?php endif; ?>
			</p>
		</form>

		<!-- ── Section 1: Requirements ───────────────────────────────────────── -->
		<section class="bm-panel bm-panel--requirements" aria-label="<?php esc_attr_e( 'Requirements', 'breadcrumb-migration' ); ?>">
			<h3 class="bm-panel__title"><?php esc_html_e( 'Requirements', 'breadcrumb-migration' ); ?></h3>
			<p class="bm-requirements-intro"><?php esc_html_e( 'Tags appear in this tab only when both conditions are met:', 'breadcrumb-migration' ); ?></p>
			<ol class="bm-requirements-list">
				<li>
					<strong><?php esc_html_e( 'Proposal must be Approved', 'breadcrumb-migration' ); ?></strong>
					<?php printf(
						/* translators: %s: Proposals tab link */
						wp_kses( __( '— open the %s, find the tag, click Validate. Publishing is not required.', 'breadcrumb-migration' ), [ 'a' => [ 'href' => [] ] ] ),
						'<a href="' . esc_url( $base_url ) . '">' . esc_html__( 'Proposals tab', 'breadcrumb-migration' ) . '</a>'
					); ?>
				</li>
				<li>
					<strong><?php esc_html_e( 'Parent category must be assigned', 'breadcrumb-migration' ); ?></strong>
					<?php printf(
						/* translators: %s: Bulk Assign tab link */
						wp_kses( __( '— open the %s and map the tag to a category. Without a parent category the breadcrumb shows a generic "Tag" crumb instead of a real category link.', 'breadcrumb-migration' ), [ 'a' => [ 'href' => [] ] ] ),
						'<a href="' . esc_url( add_query_arg( 'tab', 'bulk_assign', $base_url ) ) . '">' . esc_html__( 'Bulk Assign tab', 'breadcrumb-migration' ) . '</a>'
					); ?>
				</li>
			</ol>
		</section>

		<?php if ( $total_desc === 0 && $search_desc === '' ) : ?>
			<p class="bm-no-data" style="margin-top:16px;"><?php esc_html_e( 'No approved tags found. Approve proposals in the Proposals tab first.', 'breadcrumb-migration' ); ?></p>
		<?php else : ?>

			<!-- ── Status Key ──────────────────────────────────────────────────── -->
			<section class="bm-panel bm-panel--legend" aria-label="<?php esc_attr_e( 'Status Key', 'breadcrumb-migration' ); ?>">
				<h3 class="bm-panel__title"><?php esc_html_e( 'Status Key', 'breadcrumb-migration' ); ?></h3>
				<ul class="bm-legend-list">
					<li class="bm-legend-item">
						<span class="bm-legend-swatch bm-legend-swatch--green"></span>
						<div>
							<strong><?php esc_html_e( 'Completed', 'breadcrumb-migration' ); ?></strong>
							<?php esc_html_e( '— Published to the frontend. Breadcrumb is live. No action needed.', 'breadcrumb-migration' ); ?>
						</div>
					</li>
					<li class="bm-legend-item">
						<span class="bm-legend-swatch bm-legend-swatch--orange"></span>
						<div>
							<strong><?php esc_html_e( 'Incomplete', 'breadcrumb-migration' ); ?></strong>
							<?php esc_html_e( '— One or more fields missing: Wikidata ID, Wikidata description, or actual tag description.', 'breadcrumb-migration' ); ?>
						</div>
					</li>
					<li class="bm-legend-item">
						<span class="bm-legend-swatch bm-legend-swatch--red"></span>
						<div>
							<strong><?php esc_html_e( 'Empty', 'breadcrumb-migration' ); ?></strong>
							<?php esc_html_e( '— No Wikidata ID, no Wikidata description, and no actual tag description. Needs full attention.', 'breadcrumb-migration' ); ?>
						</div>
					</li>
				</ul>
			</section>

			<!-- ── Batch Filter ────────────────────────────────────────────────── -->
			<section class="bm-panel bm-panel--batch-filter" aria-label="<?php esc_attr_e( 'Batch Filter', 'breadcrumb-migration' ); ?>">
				<h3 class="bm-panel__title"><?php esc_html_e( 'Batch Filter', 'breadcrumb-migration' ); ?></h3>
				<p class="description" style="margin-bottom:8px;"><?php esc_html_e( 'Paste a comma or newline-separated list of tag names to narrow the table to that batch only.', 'breadcrumb-migration' ); ?></p>
				<div class="bm-desc-tag-filter-row">
					<textarea id="bm-desc-tag-list" rows="3"
						placeholder="<?php esc_attr_e( 'Apidoc, Chai, cheerio, CRUD, ejs, Express…', 'breadcrumb-migration' ); ?>"></textarea>
					<div class="bm-desc-tag-filter-actions">
						<button type="button" class="button button-primary" id="bm-desc-tag-filter-apply">
							<?php esc_html_e( 'Apply Filter', 'breadcrumb-migration' ); ?>
						</button>
						<button type="button" class="button" id="bm-desc-tag-filter-clear">
							<?php esc_html_e( 'Clear', 'breadcrumb-migration' ); ?>
						</button>
					</div>
				</div>
			</section>

			<!-- ── Tag Descriptions ────────────────────────────────────────────── -->
			<section class="bm-panel bm-panel--tag-descriptions" aria-label="<?php esc_attr_e( 'Tag Descriptions', 'breadcrumb-migration' ); ?>">
				<h3 class="bm-panel__title"><?php esc_html_e( 'Tag Descriptions', 'breadcrumb-migration' ); ?></h3>

			<!-- ── Tablenav top ─────────────────────────────────────────────────── -->
			<div class="tablenav top bm-desc-tablenav">
				<div class="bm-desc-actions-bar">
					<button type="button" class="button button-primary bm-btn-bulk-save-desc">
						<?php esc_html_e( 'Save to WordPress', 'breadcrumb-migration' ); ?>
					</button>
					<button type="button" class="button" id="bm-sync-descriptions">
						↺ <?php esc_html_e( 'Sync from WordPress', 'breadcrumb-migration' ); ?>
					</button>
					<button type="button" class="button bm-btn-export-csv">
						↓ <?php esc_html_e( 'Export CSV', 'breadcrumb-migration' ); ?>
					</button>
					<button type="button" class="button bm-btn-export-json">
						↓ <?php esc_html_e( 'Export JSON', 'breadcrumb-migration' ); ?>
					</button>
				</div>
				<?php bm_render_bulk_desc_pagination( $total_desc, $per_page_desc, $current_page, $base_url_desc, $search_desc, 'top' ); ?>
			</div>

			<!-- ── Client-side filters ──────────────────────────────────────────── -->
			<div class="bm-bulk-desc-filters" id="bm-bulk-desc-filters">
				<strong><?php esc_html_e( 'Show only:', 'breadcrumb-migration' ); ?></strong>
				<label>
					<input type="checkbox" id="bm-filter-wd-id-empty" class="bm-desc-filter">
					<?php esc_html_e( 'Wikidata ID empty', 'breadcrumb-migration' ); ?>
					<span class="bm-filter-count" id="bm-count-wd-id-empty">0</span>
				</label>
				<label>
					<input type="checkbox" id="bm-filter-wd-id-filled" class="bm-desc-filter">
					<?php esc_html_e( 'Wikidata ID filled', 'breadcrumb-migration' ); ?>
					<span class="bm-filter-count" id="bm-count-wd-id-filled">0</span>
				</label>
				<label>
					<input type="checkbox" id="bm-filter-wd-desc-empty" class="bm-desc-filter">
					<?php esc_html_e( 'Wikidata description empty', 'breadcrumb-migration' ); ?>
					<span class="bm-filter-count" id="bm-count-wd-desc-empty">0</span>
				</label>
				<label>
					<input type="checkbox" id="bm-filter-actual-desc-empty" class="bm-desc-filter">
					<?php esc_html_e( 'Actual description empty', 'breadcrumb-migration' ); ?>
					<span class="bm-filter-count" id="bm-count-actual-desc-empty">0</span>
				</label>
				<label>
					<input type="checkbox" id="bm-filter-manual-only" class="bm-desc-filter">
					<?php esc_html_e( 'Written (manual) only', 'breadcrumb-migration' ); ?>
					<span class="bm-filter-count" id="bm-count-manual-only">0</span>
				</label>
				<label>
					<input type="checkbox" id="bm-filter-completed" class="bm-desc-filter">
					<?php esc_html_e( 'Completed', 'breadcrumb-migration' ); ?>
					<span class="bm-filter-count" id="bm-count-completed">0</span>
				</label>
				<button type="button" class="button button-small" id="bm-desc-filter-reset">
					<?php esc_html_e( 'Show all', 'breadcrumb-migration' ); ?>
				</button>
				<span class="bm-filter-visible-count">
					<span id="bm-desc-visible-count">0</span> / <span id="bm-desc-total-count">0</span>
				</span>
			</div>

			<div class="bm-desc-selected-wrap" id="bm-desc-selected-wrap" style="display:none;">
				<label for="bm-desc-selected-keywords">
					<strong><?php esc_html_e( 'Selected keywords', 'breadcrumb-migration' ); ?></strong>
					<span class="description"> &mdash; <?php esc_html_e( 'comma-separated list of checked keywords, copy &amp; paste ready', 'breadcrumb-migration' ); ?></span>
				</label>
				<textarea id="bm-desc-selected-keywords" class="bm-desc-selected-keywords large-text" rows="2" readonly
					placeholder="<?php esc_attr_e( 'Check tags above to populate this list…', 'breadcrumb-migration' ); ?>"></textarea>
			</div>

			<?php if ( empty( $rows ) ) : ?>
				<p class="bm-no-data" style="margin: 16px 0;">
					<?php if ( $search_desc !== '' ) :
						printf(
							/* translators: %s: search query */
							esc_html__( 'No tags match "%s". Try a different search or clear the search.', 'breadcrumb-migration' ),
							esc_html( $search_desc )
						);
					else :
						esc_html_e( 'No tags on this page.', 'breadcrumb-migration' );
					endif; ?>
				</p>
			<?php else : ?>

			<table class="widefat striped bm-bulk-desc-table" id="bm-bulk-desc-table">
				<thead>
					<tr>
						<th class="bm-bulk-col-cb">
							<label>
								<input type="checkbox" id="bm-desc-select-all">
								<?php esc_html_e( 'All', 'breadcrumb-migration' ); ?>
							</label>
						</th>
						<th><?php esc_html_e( 'Tag', 'breadcrumb-migration' ); ?></th>
						<th><?php esc_html_e( 'Wikidata ID', 'breadcrumb-migration' ); ?></th>
						<th><?php esc_html_e( 'Description from Wikidata', 'breadcrumb-migration' ); ?></th>
						<th><?php esc_html_e( 'Actual Description', 'breadcrumb-migration' ); ?></th>
					</tr>
				</thead>
				<tbody>
				<?php foreach ( $rows as $row ) :
					$proposal_id   = (int) $row->proposal_id;
					$proposed_desc = $row->proposed_description ?? '';
					$wikidata_desc = $row->wikidata_description ?? '';
					$tag_url       = $row->proposed_slug
						? home_url( '/tag/' . trailingslashit( sanitize_title( $row->proposed_slug ) ) )
						: '';
					$edit_url      = admin_url( 'term.php?taxonomy=post_tag&tag_ID=' . absint( $row->wp_term_id ) . '&post_type=post' );

					if ( $proposed_desc !== '' && ( $wikidata_desc === '' || $proposed_desc !== $wikidata_desc ) ) {
						$desc_source = 'manual';
					} elseif ( $proposed_desc !== '' ) {
						$desc_source = 'wikidata';
					} else {
						$desc_source = 'empty';
					}

					$is_published = ( ( $row->term_status ?? '' ) === 'published' );
					if ( $proposed_desc !== '' ) {
						$row_status = 'green';
					} elseif ( ! empty( $row->wikidata_id ) || $wikidata_desc !== '' ) {
						$row_status = 'orange';
					} else {
						$row_status = 'red';
					}
				?>
					<tr class="bm-bulk-desc-row bm-desc-row--<?php echo esc_attr( $row_status ); ?>"
						data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>"
						data-tag-name="<?php echo esc_attr( mb_strtolower( $row->original_name, 'UTF-8' ) ); ?>"
						data-desc-source="<?php echo esc_attr( $desc_source ); ?>"
						data-wd-id-empty="<?php echo empty( $row->wikidata_id ) ? '1' : '0'; ?>"
						data-wd-desc-empty="<?php echo $wikidata_desc === '' ? '1' : '0'; ?>"
						data-actual-desc-empty="<?php echo $proposed_desc === '' ? '1' : '0'; ?>"
						data-term-published="<?php echo $is_published ? '1' : '0'; ?>"
						data-row-status="<?php echo esc_attr( $row_status ); ?>">
						<td class="bm-bulk-col-cb">
							<input type="checkbox" class="bm-desc-cb"
								value="<?php echo esc_attr( $proposal_id ); ?>"
								data-tag-name="<?php echo esc_attr( $row->original_name ); ?>">
						</td>
						<!-- Tag name + slug + WP ID + links -->
						<td class="bm-desc-td-tag">
							<strong class="bm-desc-tag-name"><?php echo esc_html( $row->original_name ); ?></strong>
							<?php if ( $row->proposed_slug ) : ?>
								<code><?php echo esc_html( $row->proposed_slug ); ?></code>
							<?php endif; ?>
							<div class="bm-desc-tag-meta">
								<input type="text" readonly class="bm-desc-wp-id"
									value="<?php echo esc_attr( $row->wp_term_id ); ?>"
									title="<?php esc_attr_e( 'WP Term ID', 'breadcrumb-migration' ); ?>">
								<a href="<?php echo esc_url( $edit_url ); ?>"
									target="_blank" rel="noopener noreferrer"
									class="bm-desc-edit-link">✏ <?php esc_html_e( 'Edit', 'breadcrumb-migration' ); ?></a>
								<?php if ( $tag_url ) : ?>
									<a href="<?php echo esc_url( $tag_url ); ?>"
										target="_blank" rel="noopener noreferrer"
										class="bm-wikidata-ext-link">↗</a>
								<?php endif; ?>
							</div>
						</td>
						<!-- Wikidata ID input -->
						<td class="bm-desc-td-wikidata-id">
							<div class="bm-desc-wikidata-id-wrap">
								<input type="text" class="bm-desc-wikidata-id"
									value="<?php echo esc_attr( $row->wikidata_id ?? '' ); ?>"
									placeholder="Q42"
									data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
								<button type="button" class="button button-small bm-btn-fetch-wikidata-desc"
									data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
									<?php esc_html_e( 'Fetch', 'breadcrumb-migration' ); ?>
								</button>
								<button type="button" class="button button-small bm-btn-search-single-wikidata"
									data-tag-name="<?php echo esc_attr( $row->original_name ); ?>">
									<?php esc_html_e( 'Search', 'breadcrumb-migration' ); ?>
								</button>
								<a href="<?php echo esc_url( add_query_arg( [
											'search'   => $row->original_name,
											'language' => $bm_settings['wikidata_lang'] ?? 'en',
											'title'    => 'Special:Search',
											'ns0'      => '1',
										], 'https://www.wikidata.org/w/index.php' ) ); ?>"
									target="_blank" rel="noopener noreferrer"
									class="bm-wikidata-ext-link bm-desc-wd-search-link"
									title="<?php esc_attr_e( 'Search this tag on Wikidata (opens in new tab)', 'breadcrumb-migration' ); ?>">🔍</a>
								<?php if ( $row->wikidata_id ) : ?>
									<a href="<?php echo esc_url( 'https://www.wikidata.org/wiki/' . $row->wikidata_id ); ?>"
										target="_blank" rel="noopener noreferrer"
										class="bm-wikidata-ext-link bm-desc-wd-link">↗</a>
								<?php endif; ?>
							</div>
							<div class="bm-desc-search-results" style="display:none;"></div>
						</td>
						<!-- Wikidata description + per-row copy button -->
						<td class="bm-desc-wikidata-text">
							<span class="bm-desc-wikidata-content"><?php echo esc_html( $wikidata_desc ); ?></span>
							<?php if ( $wikidata_desc !== '' ) : ?>
								<div class="bm-desc-wd-copy-wrap">
									<button type="button"
										class="button button-small bm-btn-copy-wd-desc"
										data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
										<?php esc_html_e( '→ Copy to Actual', 'breadcrumb-migration' ); ?>
									</button>
								</div>
							<?php endif; ?>
						</td>
						<!-- Actual Description + badge + refresh + edit link -->
						<td class="bm-desc-actual-text">
							<?php if ( $desc_source === 'manual' ) : ?>
								<span class="bm-desc-actual-badge bm-desc-actual-badge--manual">✍ <?php esc_html_e( 'Written', 'breadcrumb-migration' ); ?></span>
							<?php elseif ( $desc_source === 'wikidata' ) : ?>
								<span class="bm-desc-actual-badge bm-desc-actual-badge--wikidata"><?php esc_html_e( 'Wikidata', 'breadcrumb-migration' ); ?></span>
							<?php endif; ?>
							<span class="bm-desc-actual-content">
								<?php if ( $proposed_desc !== '' ) :
									echo esc_html( $proposed_desc );
								else : ?>
									<em class="bm-no-data"><?php esc_html_e( 'Empty', 'breadcrumb-migration' ); ?></em>
								<?php endif; ?>
							</span>
							<div class="bm-desc-actual-actions">
								<button type="button"
									class="button button-small bm-btn-refresh-single-desc"
									data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>"
									title="<?php esc_attr_e( 'Pull description from WordPress — marks as ✍ Written in Proposals tab', 'breadcrumb-migration' ); ?>">↺</button>
								<a href="<?php echo esc_url( $edit_url ); ?>"
									target="_blank" rel="noopener noreferrer"
									class="bm-desc-edit-link">✏ <?php esc_html_e( 'Edit in WP', 'breadcrumb-migration' ); ?></a>
							</div>
						</td>
					</tr>
				<?php endforeach; ?>
				</tbody>
			</table>

			<?php endif; // empty( $rows ) ?>

			<!-- ── Tablenav bottom ──────────────────────────────────────────────── -->
			<div class="tablenav bottom bm-desc-tablenav">
				<?php bm_render_bulk_desc_pagination( $total_desc, $per_page_desc, $current_page, $base_url_desc, $search_desc, 'bottom' ); ?>
			</div>

			<div id="bm-bulk-desc-results" style="display:none; margin-top:16px;"></div>

			</section><!-- .bm-panel--tag-descriptions -->
		<?php endif; // total_desc === 0 && no search ?>
	</div>
	<?php
}

// ── Bulk Description — pagination ─────────────────────────────────────────────

function bm_render_bulk_desc_pagination( int $total, int $per_page, int $current, string $base_url, string $search, string $position ): void {
	$total_pages = max( 1, (int) ceil( $total / $per_page ) );
	$url_base    = $search !== '' ? add_query_arg( 'bm_desc_search', $search, $base_url ) : $base_url;

	$is_first  = $current <= 1;
	$is_last   = $current >= $total_pages;
	$first_url = esc_url( add_query_arg( 'paged', 1, $url_base ) );
	$prev_url  = $is_first ? '' : esc_url( add_query_arg( 'paged', $current - 1, $url_base ) );
	$next_url  = $is_last  ? '' : esc_url( add_query_arg( 'paged', $current + 1, $url_base ) );
	$last_url  = esc_url( add_query_arg( 'paged', $total_pages, $url_base ) );
	$url_tpl   = esc_attr( add_query_arg( 'paged', 'BM_PAGE', $url_base ) );
	$input_id  = 'bm-desc-page-selector-' . esc_attr( $position );
	?>
	<div class="tablenav-pages<?php echo $total_pages <= 1 ? ' one-page' : ''; ?>">
		<span class="displaying-num">
			<?php printf(
				esc_html( _n( '%s item', '%s items', $total, 'breadcrumb-migration' ) ),
				esc_html( number_format_i18n( $total ) )
			); ?>
		</span>
		<?php if ( $total_pages > 1 ) : ?>
		<span class="pagination-links">
			<?php if ( $is_first ) : ?>
				<span class="tablenav-pages-navspan button disabled" aria-hidden="true">«</span>
				<span class="tablenav-pages-navspan button disabled" aria-hidden="true">‹</span>
			<?php else : ?>
				<a class="first-page button" href="<?php echo $first_url; ?>">
					<span class="screen-reader-text"><?php esc_html_e( 'First page', 'breadcrumb-migration' ); ?></span>
					<span aria-hidden="true">«</span>
				</a>
				<a class="prev-page button" href="<?php echo $prev_url; ?>">
					<span class="screen-reader-text"><?php esc_html_e( 'Previous page', 'breadcrumb-migration' ); ?></span>
					<span aria-hidden="true">‹</span>
				</a>
			<?php endif; ?>
			<span class="paging-input">
				<label for="<?php echo $input_id; ?>" class="screen-reader-text">
					<?php esc_html_e( 'Current Page', 'breadcrumb-migration' ); ?>
				</label>
				<input class="current-page bm-page-jump" id="<?php echo $input_id; ?>"
					type="text" name="paged"
					value="<?php echo esc_attr( $current ); ?>" size="3"
					data-total-pages="<?php echo esc_attr( $total_pages ); ?>"
					data-url-template="<?php echo $url_tpl; ?>">
				<span class="tablenav-paging-text">
					<?php esc_html_e( 'of', 'breadcrumb-migration' ); ?>
					<span class="total-pages"><?php echo esc_html( number_format_i18n( $total_pages ) ); ?></span>
				</span>
			</span>
			<?php if ( $is_last ) : ?>
				<span class="tablenav-pages-navspan button disabled" aria-hidden="true">›</span>
				<span class="tablenav-pages-navspan button disabled" aria-hidden="true">»</span>
			<?php else : ?>
				<a class="next-page button" href="<?php echo $next_url; ?>">
					<span class="screen-reader-text"><?php esc_html_e( 'Next page', 'breadcrumb-migration' ); ?></span>
					<span aria-hidden="true">›</span>
				</a>
				<a class="last-page button" href="<?php echo $last_url; ?>">
					<span class="screen-reader-text"><?php esc_html_e( 'Last page', 'breadcrumb-migration' ); ?></span>
					<span aria-hidden="true">»</span>
				</a>
			<?php endif; ?>
		</span>
		<?php endif; ?>
	</div>
	<?php
}

// ── Help — Wikidata tab ────────────────────────────────────────────────────────

function bm_render_tab_help_wikidata(): void {
	$json_path = BM_PLUGIN_DIR . 'data/wikidata-help.json';

	if ( ! file_exists( $json_path ) ) {
		?>
		<div class="bm-section">
			<p class="bm-error"><?php esc_html_e( 'Help data file not found: data/wikidata-help.json', 'breadcrumb-migration' ); ?></p>
		</div>
		<?php
		return;
	}

	$raw  = file_get_contents( $json_path ); // phpcs:ignore
	$data = json_decode( $raw, true );

	if ( ! is_array( $data ) || empty( $data['sections'] ) ) {
		?>
		<div class="bm-section">
			<p class="bm-error"><?php esc_html_e( 'Help data file is empty or has an invalid format.', 'breadcrumb-migration' ); ?></p>
		</div>
		<?php
		return;
	}
	?>
	<div class="bm-section bm-help-wrap">
		<h2><?php esc_html_e( 'Help — Wikidata', 'breadcrumb-migration' ); ?></h2>
		<p class="description">
			<?php esc_html_e( 'Step-by-step guides and reference material for working with Wikidata entities in the breadcrumb migration workflow. Content is loaded from ', 'breadcrumb-migration' ); ?>
			<code>data/wikidata-help.json</code> — <?php esc_html_e( 'edit that file to add new sections or articles without touching PHP.', 'breadcrumb-migration' ); ?>
		</p>

		<?php foreach ( $data['sections'] as $section ) :
			if ( empty( $section['id'] ) || empty( $section['title'] ) ) continue;
		?>
		<section class="bm-help-section-block" id="bm-help-<?php echo esc_attr( $section['id'] ); ?>">

			<div class="bm-help-section-header">
				<?php if ( ! empty( $section['icon'] ) ) : ?>
					<span class="bm-help-icon" aria-hidden="true"><?php echo esc_html( $section['icon'] ); ?></span>
				<?php endif; ?>
				<div>
					<h3 class="bm-help-section-title"><?php echo esc_html( $section['title'] ); ?></h3>
					<?php if ( ! empty( $section['description'] ) ) : ?>
						<p class="bm-help-section-desc description"><?php echo esc_html( $section['description'] ); ?></p>
					<?php endif; ?>
				</div>
			</div>

			<?php if ( ! empty( $section['articles'] ) ) :
				foreach ( $section['articles'] as $article ) :
					if ( empty( $article['id'] ) || empty( $article['title'] ) ) continue;
			?>
			<div class="bm-help-article" id="bm-help-article-<?php echo esc_attr( $article['id'] ); ?>">

				<button class="bm-help-article-toggle" type="button" aria-expanded="true"
					aria-controls="bm-help-body-<?php echo esc_attr( $article['id'] ); ?>">
					<span class="bm-help-article-title"><?php echo esc_html( $article['title'] ); ?></span>
					<span class="bm-help-toggle-icon" aria-hidden="true">&#9660;</span>
				</button>

				<div class="bm-help-article-body" id="bm-help-body-<?php echo esc_attr( $article['id'] ); ?>">

					<?php if ( ! empty( $article['item'] ) ) :
						$item = $article['item'];
					?>
					<div class="bm-help-item-card">
						<h4 class="bm-help-item-card__title"><?php esc_html_e( 'Item summary', 'breadcrumb-migration' ); ?></h4>
						<table class="bm-help-item-table">
							<?php if ( ! empty( $item['label'] ) ) : ?>
							<tr>
								<th><?php esc_html_e( 'Label', 'breadcrumb-migration' ); ?></th>
								<td><code><?php echo esc_html( $item['label'] ); ?></code></td>
							</tr>
							<?php endif; ?>
							<?php if ( ! empty( $item['language'] ) ) : ?>
							<tr>
								<th><?php esc_html_e( 'Language', 'breadcrumb-migration' ); ?></th>
								<td><span class="bm-help-badge"><?php echo esc_html( $item['language'] ); ?></span></td>
							</tr>
							<?php endif; ?>
							<?php if ( ! empty( $item['description'] ) ) : ?>
							<tr>
								<th><?php esc_html_e( 'Description', 'breadcrumb-migration' ); ?></th>
								<td><?php echo esc_html( $item['description'] ); ?></td>
							</tr>
							<?php endif; ?>
							<?php if ( ! empty( $item['aliases'] ) ) : ?>
							<tr>
								<th><?php esc_html_e( 'Aliases', 'breadcrumb-migration' ); ?></th>
								<td>
									<?php foreach ( $item['aliases'] as $alias ) : ?>
										<span class="bm-help-badge bm-help-badge--alias"><?php echo esc_html( $alias ); ?></span>
									<?php endforeach; ?>
								</td>
							</tr>
							<?php endif; ?>
						</table>
					</div>
					<?php endif; ?>

					<?php if ( ! empty( $article['steps'] ) ) : ?>
					<ol class="bm-help-steps">
						<?php foreach ( $article['steps'] as $step ) : ?>
						<li class="bm-help-step">

							<div class="bm-help-step-header">
								<strong class="bm-help-step-name"><?php echo esc_html( $step['name'] ?? '' ); ?></strong>
								<?php if ( ! empty( $step['url'] ) ) : ?>
									<a href="<?php echo esc_url( $step['url'] ); ?>"
										target="_blank" rel="noopener noreferrer"
										class="bm-help-step-url">
										<?php echo esc_html( $step['url'] ); ?> ↗
									</a>
								<?php endif; ?>
							</div>

							<?php if ( ! empty( $step['instructions'] ) ) : ?>
								<p class="bm-help-step-instructions"><?php echo esc_html( $step['instructions'] ); ?></p>
							<?php endif; ?>

							<?php if ( ! empty( $step['fields'] ) ) : ?>
							<table class="bm-help-fields-table">
								<?php foreach ( $step['fields'] as $key => $val ) : ?>
								<tr>
									<th><?php echo esc_html( ucwords( str_replace( '_', ' ', $key ) ) ); ?></th>
									<td><?php echo esc_html( $val ); ?></td>
								</tr>
								<?php endforeach; ?>
							</table>
							<?php endif; ?>

							<?php if ( ! empty( $step['statement'] ) ) :
								$prop = $step['statement']['property'] ?? [];
								$val  = $step['statement']['value']    ?? [];
							?>
							<div class="bm-help-statement">
								<span class="bm-help-property">
									<?php if ( ! empty( $prop['id'] ) ) : ?><code><?php echo esc_html( $prop['id'] ); ?></code><?php endif; ?>
									<?php echo esc_html( $prop['label'] ?? '' ); ?>
								</span>
								<span class="bm-help-arrow">&#8594;</span>
								<span class="bm-help-value">
									<?php if ( ! empty( $val['id'] ) ) : ?><code><?php echo esc_html( $val['id'] ); ?></code><?php endif; ?>
									<?php echo esc_html( $val['label'] ?? '' ); ?>
								</span>
							</div>
							<?php endif; ?>

							<?php if ( ! empty( $step['reference_properties'] ) ) : ?>
							<ul class="bm-help-ref-list">
								<?php foreach ( $step['reference_properties'] as $ref ) : ?>
								<li>
									<?php if ( ! empty( $ref['id'] ) ) : ?>
										<code><?php echo esc_html( $ref['id'] ); ?></code>
									<?php endif; ?>
									<strong><?php echo esc_html( $ref['label'] ?? '' ); ?></strong>
									<?php if ( ! empty( $ref['value'] ) ) : ?>
										— <?php echo esc_html( $ref['value'] ); ?>
									<?php endif; ?>
								</li>
								<?php endforeach; ?>
							</ul>
							<?php endif; ?>

						</li>
						<?php endforeach; ?>
					</ol>
					<?php endif; ?>

					<?php if ( ! empty( $article['result'] ) ) : ?>
					<div class="bm-help-result">
						<strong><?php esc_html_e( 'Result:', 'breadcrumb-migration' ); ?></strong>
						<?php echo esc_html( $article['result'] ); ?>
					</div>
					<?php endif; ?>

				</div><!-- .bm-help-article-body -->
			</div><!-- .bm-help-article -->
			<?php endforeach; endif; ?>

		</section>
		<?php endforeach; ?>

	</div><!-- .bm-help-wrap -->
	<?php
}

// ── Import & Export tab ────────────────────────────────────────────────────────

function bm_render_tab_import(): void {
	$msg = sanitize_key( $_GET['bm_msg'] ?? '' );
	if ( $msg ) {
		$messages = [
			'imported'     => sprintf(
				/* translators: 1: imported count, 2: error count */
				__( '%1$d term(s) imported (%2$d errors).', 'breadcrumb-migration' ),
				(int) ( $_GET['bm_count'] ?? 0 ),
				(int) ( $_GET['bm_err']   ?? 0 )
			),
			'no_file'      => __( 'No file selected.', 'breadcrumb-migration' ),
			'invalid_json' => __( 'Invalid JSON file.', 'breadcrumb-migration' ),
			'empty_csv'    => __( 'CSV file is empty or malformed.', 'breadcrumb-migration' ),
			'bad_format'   => __( 'Unsupported format. Use .json or .csv', 'breadcrumb-migration' ),
			'empty_data'   => __( 'File contained no importable rows.', 'breadcrumb-migration' ),
		];
		$type = $msg === 'imported' ? 'success' : 'error';
		$text = $messages[ $msg ] ?? $msg;
		printf(
			'<div class="notice notice-%s is-dismissible"><p>%s</p></div>',
			esc_attr( $type ),
			esc_html( $text )
		);
	}

	$export_nonce = wp_create_nonce( 'bm_export_nonce' );
	?>
	<div class="bm-section">
		<h2><?php esc_html_e( 'Import Pipeline Data', 'breadcrumb-migration' ); ?></h2>
		<p>
			<?php esc_html_e( 'Upload the JSON or CSV file produced by pipeline Step 4.', 'breadcrumb-migration' ); ?>
			<br><code>source/pipeline/exports/*_step_4_proposals.json</code>
		</p>
		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>"
			enctype="multipart/form-data" class="bm-import-form">
			<input type="hidden" name="action" value="bm_import">
			<?php wp_nonce_field( 'bm_import_nonce' ); ?>
			<div class="bm-import-row">
				<input type="file" name="bm_import_file" accept=".json,.csv" required>
				<button type="submit" class="button button-primary">
					<?php esc_html_e( 'Import', 'breadcrumb-migration' ); ?>
				</button>
			</div>
		</form>
	</div>

	<div class="bm-section">
		<h2><?php esc_html_e( 'Export Data', 'breadcrumb-migration' ); ?></h2>
		<p><?php esc_html_e( 'Download database tables as CSV or JSON files.', 'breadcrumb-migration' ); ?></p>
		<table class="bm-export-table widefat striped">
			<thead>
				<tr>
					<th><?php esc_html_e( 'Table', 'breadcrumb-migration' ); ?></th>
					<th><?php esc_html_e( 'CSV', 'breadcrumb-migration' ); ?></th>
					<th><?php esc_html_e( 'JSON', 'breadcrumb-migration' ); ?></th>
				</tr>
			</thead>
			<tbody>
			<?php
			foreach ( [
				'proposals' => __( 'Proposals', 'breadcrumb-migration' ),
				'terms'     => __( 'Terms', 'breadcrumb-migration' ),
				'redirects' => __( 'Redirects', 'breadcrumb-migration' ),
			] as $tbl => $label ) :
				$base_args = [
					'action'   => 'bm_export',
					'bm_table' => $tbl,
					'_wpnonce' => $export_nonce,
				];
				$url_csv  = add_query_arg( array_merge( $base_args, [ 'bm_format' => 'csv' ] ), admin_url( 'admin-post.php' ) );
				$url_json = add_query_arg( array_merge( $base_args, [ 'bm_format' => 'json' ] ), admin_url( 'admin-post.php' ) );
				?>
				<tr>
					<td><strong><?php echo esc_html( $label ); ?></strong></td>
					<td><a href="<?php echo esc_url( $url_csv ); ?>" class="button button-small">CSV</a></td>
					<td><a href="<?php echo esc_url( $url_json ); ?>" class="button button-small">JSON</a></td>
				</tr>
			<?php endforeach; ?>
			</tbody>
		</table>
	</div>
	<?php
}

// ── Danger Zone tab ────────────────────────────────────────────────────────────

function bm_render_tab_danger(): void {
	global $wpdb;
	$t = bm_tables();

	$term_count     = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$t['terms']}" );     // phpcs:ignore
	$proposal_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$t['proposals']}" ); // phpcs:ignore
	$redirect_count = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$t['redirects']}" ); // phpcs:ignore
	?>
	<div class="bm-section bm-danger-section">
		<h2 class="bm-danger-title">
			&#9888; <?php esc_html_e( 'Danger Zone', 'breadcrumb-migration' ); ?>
		</h2>
		<p class="bm-danger-desc">
			<?php esc_html_e( 'These actions are irreversible. Data cannot be recovered after deletion.', 'breadcrumb-migration' ); ?>
		</p>

		<div class="bm-danger-action">
			<div class="bm-danger-action__info">
				<strong><?php esc_html_e( 'Empty all tables', 'breadcrumb-migration' ); ?></strong>
				<p>
					<?php printf(
						/* translators: 1: term count, 2: proposal count, 3: redirect count */
						esc_html__( 'Will delete %1$d term(s), %2$d proposal(s), %3$d redirect(s) from the database.', 'breadcrumb-migration' ),
						$term_count,
						$proposal_count,
						$redirect_count
					); ?>
				</p>
			</div>
			<button class="button bm-btn-danger-action bm-btn-empty-tables"
				data-confirm="<?php esc_attr_e( 'This will permanently delete ALL data from the breadcrumb tables. Type CONFIRM to proceed.', 'breadcrumb-migration' ); ?>">
				<?php esc_html_e( 'Empty all tables', 'breadcrumb-migration' ); ?>
			</button>
		</div>
	</div>
	<?php
}

// ── Status Tag Browser ────────────────────────────────────────────────────────

function bm_render_status_tag_browser(): void {
	?>
	<section class="bm-panel bm-panel--status-tags" id="bm-status-tag-browser" style="display:none;"
		aria-label="<?php esc_attr_e( 'Tags by Status', 'breadcrumb-migration' ); ?>">
		<h3 class="bm-panel__title">
			<?php esc_html_e( 'Tags by Status', 'breadcrumb-migration' ); ?>
			&mdash; <span id="bm-status-tag-label"></span>
			<span class="bm-status-tag-count" id="bm-status-tag-count-wrap" style="display:none;">
				(<span id="bm-status-tag-count">0</span>)
			</span>
		</h3>
		<p class="description">
			<?php esc_html_e( 'All tag names for the selected status — comma-separated, copy &amp; paste ready.', 'breadcrumb-migration' ); ?>
		</p>
		<textarea id="bm-status-tag-textarea" class="large-text bm-status-tag-textarea" rows="5" readonly
			placeholder="<?php esc_attr_e( 'Loading…', 'breadcrumb-migration' ); ?>"></textarea>
		<div class="bm-status-tag-actions">
			<button type="button" class="button button-primary" id="bm-status-tag-copy">
				<?php esc_html_e( 'Copy to Clipboard', 'breadcrumb-migration' ); ?>
			</button>
			<button type="button" class="button" id="bm-status-tag-send">
				&#8595; <?php esc_html_e( 'Send to Bulk Search', 'breadcrumb-migration' ); ?>
			</button>
			<button type="button" class="button" id="bm-status-tag-close">
				&#10005; <?php esc_html_e( 'Close', 'breadcrumb-migration' ); ?>
			</button>
		</div>
	</section>
	<?php
}

// ── Stats bar ──────────────────────────────────────────────────────────────────

function bm_render_stats( array $stats ): void {
	$labels = [
		'pending'  => __( 'Pending',  'breadcrumb-migration' ),
		'approved' => __( 'Approved', 'breadcrumb-migration' ),
		'rejected' => __( 'Rejected', 'breadcrumb-migration' ),
	];
	?>
	<section class="bm-panel bm-panel--overview" aria-label="<?php esc_attr_e( 'Overview', 'breadcrumb-migration' ); ?>">
		<h3 class="bm-panel__title"><?php esc_html_e( 'Overview', 'breadcrumb-migration' ); ?></h3>
		<div class="bm-stats">
			<?php foreach ( $labels as $key => $label ) :
				$count = $stats[ $key ] ?? 0;
			?>
			<span class="bm-stat bm-stat--<?php echo esc_attr( $key ); ?>"
				data-state="<?php echo esc_attr( $key ); ?>"
				role="button"
				tabindex="0"
				title="<?php
					/* translators: %s: status label e.g. Pending */
					printf( esc_attr__( 'Click to list all %s tags', 'breadcrumb-migration' ), esc_attr( $label ) );
				?>">
				<strong><?php echo (int) $count; ?></strong> <?php echo esc_html( $label ); ?>
			</span>
			<?php endforeach; ?>
		</div>
	</section>
	<?php
}

// ── Filter bar ─────────────────────────────────────────────────────────────────

function bm_render_filters( string $base_url, string $taxonomy, string $state, string $search, string $wikidata_id = '', string $spacy = '', string $bulk_keywords = '' ): void {
	$spacy_options = [
		'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT',
		'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT',
		'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL',
	];
	?>
	<form method="get" action="<?php echo esc_url( $base_url ); ?>" class="bm-filters">
		<input type="hidden" name="page" value="breadcrumb-migration">

		<!-- Bulk Keyword Search -->
		<section class="bm-panel bm-panel--bulk-search" aria-label="<?php esc_attr_e( 'Bulk Keyword Search', 'breadcrumb-migration' ); ?>">
			<h3 class="bm-panel__title"><?php esc_html_e( 'Bulk Keyword Search', 'breadcrumb-migration' ); ?></h3>
			<p class="description">
				<?php esc_html_e( 'Paste keywords (comma or line-separated) to check their migration status. Replaces the card view with a status table when active. Clear and click Filter to return to cards.', 'breadcrumb-migration' ); ?>
			</p>
			<textarea name="bm_bulk_keywords" id="bm-proposals-bulk-keywords"
				rows="4" class="bm-proposals-bulk-keywords large-text"
				placeholder="<?php esc_attr_e( 'agentic browsers, Atlas, Comet, dbt, DuckDB, GDPR…', 'breadcrumb-migration' ); ?>"><?php echo esc_textarea( $bulk_keywords ); ?></textarea>
		</section>

		<div class="bm-filter-sections">

			<!-- Filter -->
			<section class="bm-panel bm-filter-section" aria-label="<?php esc_attr_e( 'Filter', 'breadcrumb-migration' ); ?>">
				<h3 class="bm-panel__title"><?php esc_html_e( 'Filter', 'breadcrumb-migration' ); ?></h3>
				<div class="bm-filter-section__controls">
					<select name="bm_taxonomy">
						<option value="all"      <?php selected( $taxonomy, 'all' ); ?>><?php esc_html_e( 'All taxonomies', 'breadcrumb-migration' ); ?></option>
						<option value="category" <?php selected( $taxonomy, 'category' ); ?>><?php esc_html_e( 'Category', 'breadcrumb-migration' ); ?></option>
						<option value="post_tag" <?php selected( $taxonomy, 'post_tag' ); ?>><?php esc_html_e( 'Tag', 'breadcrumb-migration' ); ?></option>
					</select>
					<select name="bm_state">
						<option value="all"      <?php selected( $state, 'all' ); ?>><?php esc_html_e( 'All states', 'breadcrumb-migration' ); ?></option>
						<option value="pending"  <?php selected( $state, 'pending' ); ?>><?php esc_html_e( 'Pending', 'breadcrumb-migration' ); ?></option>
						<option value="approved" <?php selected( $state, 'approved' ); ?>><?php esc_html_e( 'Approved', 'breadcrumb-migration' ); ?></option>
						<option value="rejected" <?php selected( $state, 'rejected' ); ?>><?php esc_html_e( 'Rejected', 'breadcrumb-migration' ); ?></option>
					</select>
				</div>
			</section>

			<!-- Search -->
			<section class="bm-panel bm-filter-section" aria-label="<?php esc_attr_e( 'Search', 'breadcrumb-migration' ); ?>">
				<h3 class="bm-panel__title"><?php esc_html_e( 'Search', 'breadcrumb-migration' ); ?></h3>
				<div class="bm-filter-section__controls">
					<input type="search" name="bm_search" value="<?php echo esc_attr( $search ); ?>"
						placeholder="<?php esc_attr_e( 'Name or slug…', 'breadcrumb-migration' ); ?>">
					<input type="search" name="bm_wikidata_id" value="<?php echo esc_attr( $wikidata_id ); ?>"
						placeholder="<?php esc_attr_e( 'Wikidata ID, e.g. Q41773', 'breadcrumb-migration' ); ?>"
						class="bm-filter-wikidata-id">
					<select name="bm_spacy">
						<option value=""><?php esc_html_e( 'All spaCy entities', 'breadcrumb-migration' ); ?></option>
						<?php foreach ( $spacy_options as $entity ) : ?>
							<option value="<?php echo esc_attr( $entity ); ?>" <?php selected( $spacy, $entity ); ?>>
								<?php echo esc_html( $entity ); ?>
							</option>
						<?php endforeach; ?>
					</select>
				</div>
			</section>

		</div><!-- .bm-filter-sections -->

		<div class="bm-filter-actions">
			<a href="<?php echo esc_url( $base_url ); ?>" class="button"><?php esc_html_e( 'Reset', 'breadcrumb-migration' ); ?></a>
			<button type="submit" class="button button-primary"><?php esc_html_e( 'Filter', 'breadcrumb-migration' ); ?></button>
		</div>
	</form>
	<?php
}

// ── Term card (2-column layout) ────────────────────────────────────────────────

function bm_render_term_card( object $row ): void {
	$state       = $row->validation_state ?? 'pending';
	$proposal_id = (int) ( $row->proposal_id ?? 0 );
	$term_id     = (int) $row->term_internal_id;

	$bc_parts = [];
	if ( ! empty( $row->proposed_breadcrumb ) ) {
		$bc_parts = json_decode( $row->proposed_breadcrumb, true ) ?: [];
	}
	$bc_html = $bc_parts
		? implode( ' <span class="bm-sep">›</span> ', array_map( 'esc_html', $bc_parts ) )
		: '<em>' . esc_html__( 'None', 'breadcrumb-migration' ) . '</em>';

	$proposed_desc = $row->proposed_description ?? '';
	$wikidata_desc = $row->wikidata_description ?? '';
	if ( $proposed_desc !== '' && ( $wikidata_desc === '' || $proposed_desc !== $wikidata_desc ) ) {
		$desc_source = 'manual';
	} elseif ( $proposed_desc !== '' ) {
		$desc_source = 'wikidata';
	} else {
		$desc_source = 'empty';
	}

	$taxonomy_label = $row->taxonomy === 'category'
		? __( 'Category', 'breadcrumb-migration' )
		: __( 'Tag', 'breadcrumb-migration' );
	?>
	<div class="bm-card bm-state--<?php echo esc_attr( $state ); ?>"
		data-term-id="<?php echo esc_attr( $term_id ); ?>"
		data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">

		<div class="bm-card__header">
			<span class="bm-badge bm-badge--taxonomy"><?php echo esc_html( $taxonomy_label ); ?></span>
			<span class="bm-badge bm-badge--state bm-badge--<?php echo esc_attr( $state ); ?>">
				<?php echo esc_html( ucfirst( $state ) ); ?>
			</span>
			<span class="bm-card__title"><?php echo esc_html( $row->original_name ); ?></span>
		</div>

		<div class="bm-card__body">

			<!-- ORIGINAL column -->
			<div class="bm-col bm-col--original">
				<h3><?php esc_html_e( 'Original', 'breadcrumb-migration' ); ?></h3>
				<table class="bm-data-table">
					<tr><th><?php esc_html_e( 'WP ID',     'breadcrumb-migration' ); ?></th><td><?php echo esc_html( $row->wp_term_id ); ?></td></tr>
					<tr>
						<th><?php esc_html_e( 'Name', 'breadcrumb-migration' ); ?></th>
						<td>
							<span class="bm-original-val"><?php echo esc_html( $row->original_name ); ?></span>
							<input type="text" class="bm-original-input bm-original-input--name"
								value="<?php echo esc_attr( $row->original_name ); ?>"
								data-original="<?php echo esc_attr( $row->original_name ); ?>"
								style="display:none">
						</td>
					</tr>
					<tr>
						<th><?php esc_html_e( 'Slug', 'breadcrumb-migration' ); ?></th>
						<td>
							<span class="bm-original-val bm-original-val--slug"><code><?php echo esc_html( $row->original_slug ); ?></code></span>
							<input type="text" class="bm-original-input bm-original-input--slug"
								value="<?php echo esc_attr( $row->original_slug ); ?>"
								data-original="<?php echo esc_attr( $row->original_slug ); ?>"
								style="display:none">
						</td>
					</tr>
					<tr><th><?php esc_html_e( 'Parent ID', 'breadcrumb-migration' ); ?></th><td><?php echo $row->original_parent_id ? esc_html( $row->original_parent_id ) : '—'; ?></td></tr>
					<tr><th><?php esc_html_e( 'Posts',     'breadcrumb-migration' ); ?></th><td><?php echo esc_html( $row->content_count ); ?></td></tr>
				</table>

				<div class="bm-card__actions bm-card__actions--original">
					<button class="button bm-btn-simulate"
						data-term-id="<?php echo esc_attr( $term_id ); ?>">
						<?php esc_html_e( 'Simulate', 'breadcrumb-migration' ); ?>
					</button>
					<button class="button bm-btn-edit-original"
						data-term-id="<?php echo esc_attr( $term_id ); ?>">
						<?php esc_html_e( 'Edit Original', 'breadcrumb-migration' ); ?>
					</button>
					<button class="button button-primary bm-btn-save-original"
						data-term-id="<?php echo esc_attr( $term_id ); ?>"
						style="display:none">
						<?php esc_html_e( 'Save', 'breadcrumb-migration' ); ?>
					</button>
					<button class="button bm-btn-cancel-original" style="display:none">
						<?php esc_html_e( 'Cancel', 'breadcrumb-migration' ); ?>
					</button>
					<?php if ( $proposal_id && $state === 'pending' ) : ?>
						<button class="button button-primary bm-btn-validate"
							data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
							<?php esc_html_e( 'Validate', 'breadcrumb-migration' ); ?>
						</button>
						<button class="button bm-btn-reject"
							data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
							<?php esc_html_e( 'Reject', 'breadcrumb-migration' ); ?>
						</button>
					<?php endif; ?>
				</div>
			</div>

			<!-- PROPOSED column -->
			<div class="bm-col bm-col--proposed">
				<h3><?php esc_html_e( 'Proposed', 'breadcrumb-migration' ); ?></h3>

				<?php if ( ! $proposal_id ) : ?>
					<p class="bm-no-data"><?php esc_html_e( 'No proposal yet.', 'breadcrumb-migration' ); ?></p>
				<?php else : ?>
					<table class="bm-data-table">
						<tr>
							<th><?php esc_html_e( 'Name', 'breadcrumb-migration' ); ?></th>
							<td class="bm-editable" data-field="proposed_name"><?php echo esc_html( $row->proposed_name ?? '—' ); ?></td>
						</tr>
<!-- V2 -->	
		<tr>
	<th><?php esc_html_e( 'Slug', 'breadcrumb-migration' ); ?></th>
	<td class="bm-editable" data-field="proposed_slug">
		<?php if ( ! empty( $row->proposed_slug ) ) : ?>
			<code><?php echo esc_html( $row->proposed_slug ); ?></code>
			<?php
			$tag_url = home_url( '/tag/' . trailingslashit( sanitize_title( $row->proposed_slug ) ) );
			?>
			&nbsp;
			<a href="<?php echo esc_url( $tag_url ); ?>" target="_blank" rel="noopener noreferrer">
				<?php esc_html_e( 'View tag', 'breadcrumb-migration' ); ?>
			</a>
		<?php else : ?>
			<code>&mdash;</code>
		<?php endif; ?>
	</td>
</tr>				

						<tr>
							<th><?php esc_html_e( 'spaCy', 'breadcrumb-migration' ); ?></th>
							<td><?php echo $row->spacy_entity ? '<span class="bm-entity">' . esc_html( $row->spacy_entity ) . '</span>' : '—'; ?></td>
						</tr>
						<tr>
							<th><?php esc_html_e( 'Wikidata ID', 'breadcrumb-migration' ); ?></th>
							<td>
								<?php if ( $row->wikidata_id ) : ?>
									<a href="https://www.wikidata.org/wiki/<?php echo esc_attr( $row->wikidata_id ); ?>"
										target="_blank" rel="noopener">
										<?php echo esc_html( $row->wikidata_id ); ?>
									</a>
								<?php else : ?>
									—
								<?php endif; ?>
							</td>
						</tr>
						<tr>
							<th><?php esc_html_e( 'Label', 'breadcrumb-migration' ); ?></th>
							<td><?php echo esc_html( $row->wikidata_label ?? '—' ); ?></td>
						</tr>
						<tr>
							<th><?php esc_html_e( 'WD Desc', 'breadcrumb-migration' ); ?></th>
							<td class="bm-wikidata-desc-cell"><?php echo esc_html( $row->wikidata_description ?? '—' ); ?></td>
						</tr>
						<tr>
							<th><?php esc_html_e( 'Actual Desc', 'breadcrumb-migration' ); ?></th>
							<td class="bm-actual-desc-cell"
								data-proposed-desc="<?php echo esc_attr( $proposed_desc ); ?>"
								data-wikidata-desc="<?php echo esc_attr( $wikidata_desc ); ?>">
								<?php if ( $desc_source === 'manual' ) : ?>
									<span class="bm-desc-actual-badge bm-desc-actual-badge--manual">✍ <?php esc_html_e( 'Written', 'breadcrumb-migration' ); ?></span>
								<?php elseif ( $desc_source === 'wikidata' ) : ?>
									<span class="bm-desc-actual-badge bm-desc-actual-badge--wikidata"><?php esc_html_e( 'Wikidata', 'breadcrumb-migration' ); ?></span>
								<?php endif; ?>
								<span class="bm-actual-desc-text">
									<?php if ( $proposed_desc !== '' ) :
										echo esc_html( $proposed_desc );
									else : ?>
										<em class="bm-no-data"><?php esc_html_e( 'Empty', 'breadcrumb-migration' ); ?></em>
									<?php endif; ?>
								</span>
							</td>
						</tr>
						<tr>
							<th><?php esc_html_e( 'Breadcrumb', 'breadcrumb-migration' ); ?></th>
							<td class="bm-breadcrumb-td">
								<div class="bm-breadcrumb-preview"><?php echo $bc_html; // already escaped above ?></div>
								<?php if ( $proposal_id ) : ?>
								<button class="button button-small bm-btn-edit-breadcrumb"
									data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
									<?php esc_html_e( '✎ Edit', 'breadcrumb-migration' ); ?>
								</button>
								<div class="bm-breadcrumb-edit-form" style="display:none">
									<?php if ( ! empty( $bc_parts ) ) :
										foreach ( $bc_parts as $crumb ) : ?>
										<input type="text" class="bm-crumb-input"
											value="<?php echo esc_attr( $crumb ); ?>">
									<?php endforeach; else : ?>
										<input type="text" class="bm-crumb-input" placeholder="<?php esc_attr_e( 'Home', 'breadcrumb-migration' ); ?>">
										<input type="text" class="bm-crumb-input" placeholder="<?php esc_attr_e( 'Category', 'breadcrumb-migration' ); ?>">
										<input type="text" class="bm-crumb-input" placeholder="<?php esc_attr_e( 'Tag', 'breadcrumb-migration' ); ?>">
									<?php endif; ?>
									<div class="bm-breadcrumb-edit-actions">
										<button class="button button-primary button-small bm-btn-save-breadcrumb"
											data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
											<?php esc_html_e( 'Save', 'breadcrumb-migration' ); ?>
										</button>
										<button class="button button-small bm-btn-cancel-breadcrumb">
											<?php esc_html_e( 'Cancel', 'breadcrumb-migration' ); ?>
										</button>
									</div>
								</div>
								<?php endif; ?>
							</td>
						</tr>
					</table>

					<div class="bm-card__actions bm-card__actions--proposed">
						<button class="button bm-btn-edit"
							data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
							<?php esc_html_e( 'Edit', 'breadcrumb-migration' ); ?>
						</button>
						<?php if ( $state === 'approved' && $row->term_status !== 'published' ) : ?>
							<button class="button bm-btn-reset"
								data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
								<?php esc_html_e( '↩ Reset to Pending', 'breadcrumb-migration' ); ?>
							</button>
							<button class="button button-primary bm-btn-publish"
								data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
								<?php esc_html_e( 'Publish to WP', 'breadcrumb-migration' ); ?>
							</button>
						<?php elseif ( $row->term_status === 'published' ) : ?>
							<span class="bm-badge bm-badge--published"><?php esc_html_e( 'Published', 'breadcrumb-migration' ); ?></span>
						<?php endif; ?>
					</div>
				<?php endif; ?>

				<!-- Simulate result area -->
				<div class="bm-simulate-result" data-term-id="<?php echo esc_attr( $term_id ); ?>" style="display:none;"></div>

				<!-- Inline edit form (hidden) -->
				<?php if ( $proposal_id ) : ?>
				<div class="bm-edit-form" data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>" style="display:none;">
					<h4><?php esc_html_e( 'Edit Proposal', 'breadcrumb-migration' ); ?></h4>
					<label><?php esc_html_e( 'Name', 'breadcrumb-migration' ); ?>
						<input type="text" name="proposed_name" value="<?php echo esc_attr( $row->proposed_name ?? '' ); ?>">
					</label>
					<label><?php esc_html_e( 'Slug', 'breadcrumb-migration' ); ?>
						<input type="text" name="proposed_slug" value="<?php echo esc_attr( $row->proposed_slug ?? '' ); ?>">
					</label>
					<label><?php esc_html_e( 'Label', 'breadcrumb-migration' ); ?>
						<input type="text" name="wikidata_label" value="<?php echo esc_attr( $row->wikidata_label ?? '' ); ?>">
					</label>
					<label><?php esc_html_e( 'spaCy', 'breadcrumb-migration' ); ?>
						<select name="spacy_entity">
							<option value=""><?php esc_html_e( '— none —', 'breadcrumb-migration' ); ?></option>
							<?php
							$spacy_options = [
						'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT',
						'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT',
						'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL',
					];
							$current_entity = $row->spacy_entity ?? '';
							foreach ( $spacy_options as $entity ) :
							?>
							<option value="<?php echo esc_attr( $entity ); ?>" <?php selected( $current_entity, $entity ); ?>>
								<?php echo esc_html( $entity ); ?>
							</option>
							<?php endforeach; ?>
						</select>
					</label>
					<label><?php esc_html_e( 'Wikidata ID', 'breadcrumb-migration' ); ?>
						<input type="text" name="wikidata_id" value="<?php echo esc_attr( $row->wikidata_id ?? '' ); ?>" placeholder="Q42">
					</label>
					<div class="bm-clear-wikidata-section">
						<button type="button" class="button button-small bm-btn-clear-wikidata"
							data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
							<?php esc_html_e( '✕ Clear Wikidata fields', 'breadcrumb-migration' ); ?>
						</button>
						<small><?php esc_html_e( 'Clears ID, label and WD description — keeps Actual Description.', 'breadcrumb-migration' ); ?></small>
					</div>
					<label><?php esc_html_e( 'Actual Description', 'breadcrumb-migration' ); ?>
						<textarea name="proposed_description"><?php echo esc_textarea( $row->proposed_description ?? '' ); ?></textarea>
					</label>

					<?php if ( $row->taxonomy === 'post_tag' ) :
						$all_cats = get_terms( [
							'taxonomy'   => 'category',
							'hide_empty' => false,
							'orderby'    => 'name',
							'number'     => 0,
						] );
						$saved_cat_id = (int) ( $row->proposed_parent_id ?? 0 );
					?>
					<label class="bm-tag-category-label">
						<?php esc_html_e( 'Parent category in breadcrumb (tags only)', 'breadcrumb-migration' ); ?>
						<select name="tag_parent_category_id" class="bm-tag-category-select">
							<option value="0"><?php esc_html_e( '— none (shows "Tag") —', 'breadcrumb-migration' ); ?></option>
							<?php foreach ( $all_cats as $cat ) : ?>
								<option value="<?php echo esc_attr( $cat->term_id ); ?>"
									<?php selected( $saved_cat_id, $cat->term_id ); ?>>
									<?php echo esc_html( $cat->name ); ?>
								</option>
							<?php endforeach; ?>
						</select>
						<small><?php esc_html_e( 'Replaces "Tag" in the breadcrumb with this category (clickable link).', 'breadcrumb-migration' ); ?></small>
					</label>
					<?php endif; ?>

					<div class="bm-edit-form__actions">
						<button class="button button-primary bm-btn-save-edit"
							data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>">
							<?php esc_html_e( 'Save', 'breadcrumb-migration' ); ?>
						</button>
						<button class="button bm-btn-cancel-edit"><?php esc_html_e( 'Cancel', 'breadcrumb-migration' ); ?></button>
					</div>
				</div>
				<?php endif; ?>

			</div><!-- .bm-col--proposed -->
		</div><!-- .bm-card__body -->
	</div><!-- .bm-card -->
	<?php
}

// ── WP-style pagination ────────────────────────────────────────────────────────

function bm_render_wp_pagination( int $total, int $per_page, int $current, string $base_url, string $taxonomy, string $state, string $search, string $wikidata_id = '', string $spacy = '', string $position = 'bottom' ): void {
	$total_pages = (int) ceil( $total / $per_page );

	$url_params = add_query_arg( [
		'bm_taxonomy'    => $taxonomy,
		'bm_state'       => $state,
		'bm_search'      => $search,
		'bm_wikidata_id' => $wikidata_id,
		'bm_spacy'       => $spacy,
	], $base_url );

	$is_first  = $current <= 1;
	$is_last   = $current >= $total_pages;
	$first_url = esc_url( add_query_arg( 'paged', 1, $url_params ) );
	$prev_url  = $is_first ? '' : esc_url( add_query_arg( 'paged', $current - 1, $url_params ) );
	$next_url  = $is_last  ? '' : esc_url( add_query_arg( 'paged', $current + 1, $url_params ) );
	$last_url  = esc_url( add_query_arg( 'paged', $total_pages, $url_params ) );
	$url_tpl   = esc_attr( add_query_arg( 'paged', 'BM_PAGE', $url_params ) );
	$input_id  = 'bm-page-selector-' . esc_attr( $position );
	?>
	<div class="tablenav bm-tablenav bm-tablenav--<?php echo esc_attr( $position ); ?>">
		<div class="tablenav-pages<?php echo $total_pages <= 1 ? ' one-page' : ''; ?>">
			<span class="displaying-num">
				<?php
				printf(
					/* translators: %s: formatted item count */
					esc_html( _n( '%s item', '%s items', $total, 'breadcrumb-migration' ) ),
					esc_html( number_format_i18n( $total ) )
				);
				?>
			</span>
			<?php if ( $total_pages > 1 ) : ?>
			<span class="pagination-links">
				<?php if ( $is_first ) : ?>
					<span class="tablenav-pages-navspan button disabled" aria-hidden="true">«</span>
					<span class="tablenav-pages-navspan button disabled" aria-hidden="true">‹</span>
				<?php else : ?>
					<a class="first-page button" href="<?php echo $first_url; ?>">
						<span class="screen-reader-text"><?php esc_html_e( 'First page', 'breadcrumb-migration' ); ?></span>
						<span aria-hidden="true">«</span>
					</a>
					<a class="prev-page button" href="<?php echo $prev_url; ?>">
						<span class="screen-reader-text"><?php esc_html_e( 'Previous page', 'breadcrumb-migration' ); ?></span>
						<span aria-hidden="true">‹</span>
					</a>
				<?php endif; ?>
				<span class="paging-input">
					<label for="<?php echo $input_id; ?>" class="screen-reader-text">
						<?php esc_html_e( 'Current Page', 'breadcrumb-migration' ); ?>
					</label>
					<input class="current-page bm-page-jump" id="<?php echo $input_id; ?>"
						type="text" name="paged"
						value="<?php echo esc_attr( $current ); ?>" size="3"
						data-total-pages="<?php echo esc_attr( $total_pages ); ?>"
						data-url-template="<?php echo $url_tpl; ?>">
					<span class="tablenav-paging-text">
						<?php esc_html_e( 'of', 'breadcrumb-migration' ); ?>
						<span class="total-pages"><?php echo esc_html( number_format_i18n( $total_pages ) ); ?></span>
					</span>
				</span>
				<?php if ( $is_last ) : ?>
					<span class="tablenav-pages-navspan button disabled" aria-hidden="true">›</span>
					<span class="tablenav-pages-navspan button disabled" aria-hidden="true">»</span>
				<?php else : ?>
					<a class="next-page button" href="<?php echo $next_url; ?>">
						<span class="screen-reader-text"><?php esc_html_e( 'Next page', 'breadcrumb-migration' ); ?></span>
						<span aria-hidden="true">›</span>
					</a>
					<a class="last-page button" href="<?php echo $last_url; ?>">
						<span class="screen-reader-text"><?php esc_html_e( 'Last page', 'breadcrumb-migration' ); ?></span>
						<span aria-hidden="true">»</span>
					</a>
				<?php endif; ?>
			</span>
			<?php endif; ?>
		</div>
	</div>
	<?php
}

// ── Settings tab ───────────────────────────────────────────────────────────────

function bm_render_tab_settings(): void {
	$settings = get_option( 'bm_settings', [] );
	$lang     = $settings['wikidata_lang'] ?? 'en';
	$msg      = sanitize_key( $_GET['bm_msg'] ?? '' );
	?>
	<?php if ( $msg === 'saved' ) : ?>
		<div class="notice notice-success is-dismissible"><p>
			<?php esc_html_e( 'Settings saved.', 'breadcrumb-migration' ); ?>
		</p></div>
	<?php endif; ?>

	<div class="bm-section">
		<h2><?php esc_html_e( 'Settings', 'breadcrumb-migration' ); ?></h2>
		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
			<input type="hidden" name="action" value="bm_save_settings">
			<?php wp_nonce_field( 'bm_save_settings_nonce' ); ?>

			<table class="form-table" role="presentation">
				<tr>
					<th scope="row">
						<label for="bm_wikidata_lang">
							<?php esc_html_e( 'Wikidata search language', 'breadcrumb-migration' ); ?>
						</label>
					</th>
					<td>
						<input type="text" id="bm_wikidata_lang" name="bm_wikidata_lang"
							value="<?php echo esc_attr( $lang ); ?>"
							class="regular-text" maxlength="10" placeholder="en">
						<p class="description">
							<?php esc_html_e( 'BCP 47 language code for Wikidata API searches and "Open on Wikidata" link (e.g. en, fr, de, es, pt).', 'breadcrumb-migration' ); ?>
						</p>
					</td>
				</tr>
			</table>

			<?php submit_button( __( 'Save Settings', 'breadcrumb-migration' ) ); ?>
		</form>
	</div>

	<div class="bm-section">
		<h2><?php esc_html_e( 'spaCy Named Entity Types — Reference', 'breadcrumb-migration' ); ?></h2>
		<p class="description">
			<?php esc_html_e( 'Full list of named entity recognition (NER) types recognised by spaCy. Used in the Proposals and Delta tabs.', 'breadcrumb-migration' ); ?>
		</p>
		<table class="widefat striped bm-spacy-ref-table">
			<thead>
				<tr>
					<th><?php esc_html_e( 'Entity', 'breadcrumb-migration' ); ?></th>
					<th><?php esc_html_e( 'Description', 'breadcrumb-migration' ); ?></th>
				</tr>
			</thead>
			<tbody>
			<?php
			$spacy_ref = [
				'PERSON'      => __( 'People, including fictional.', 'breadcrumb-migration' ),
				'NORP'        => __( 'Nationalities or religious or political groups.', 'breadcrumb-migration' ),
				'FAC'         => __( 'Buildings, airports, highways, bridges, etc.', 'breadcrumb-migration' ),
				'ORG'         => __( 'Companies, agencies, institutions, etc.', 'breadcrumb-migration' ),
				'GPE'         => __( 'Countries, cities, states.', 'breadcrumb-migration' ),
				'LOC'         => __( 'Non-GPE locations, mountain ranges, bodies of water.', 'breadcrumb-migration' ),
				'PRODUCT'     => __( 'Objects, vehicles, foods, etc. (Not services.)', 'breadcrumb-migration' ),
				'EVENT'       => __( 'Named hurricanes, battles, wars, sports events, etc.', 'breadcrumb-migration' ),
				'WORK_OF_ART' => __( 'Titles of books, songs, etc.', 'breadcrumb-migration' ),
				'LAW'         => __( 'Named documents made into laws.', 'breadcrumb-migration' ),
				'LANGUAGE'    => __( 'Any named language.', 'breadcrumb-migration' ),
				'DATE'        => __( 'Absolute or relative dates or periods.', 'breadcrumb-migration' ),
				'TIME'        => __( 'Times smaller than a day.', 'breadcrumb-migration' ),
				'PERCENT'     => __( 'Percentage, including "%".', 'breadcrumb-migration' ),
				'MONEY'       => __( 'Monetary values, including unit.', 'breadcrumb-migration' ),
				'QUANTITY'    => __( 'Measurements, as of weight or distance.', 'breadcrumb-migration' ),
				'ORDINAL'     => __( '"first", "second", etc.', 'breadcrumb-migration' ),
				'CARDINAL'    => __( 'Numerals that do not fall under another type.', 'breadcrumb-migration' ),
			];
			foreach ( $spacy_ref as $entity => $description ) :
			?>
				<tr>
					<td><code class="bm-entity"><?php echo esc_html( $entity ); ?></code></td>
					<td><?php echo esc_html( $description ); ?></td>
				</tr>
			<?php endforeach; ?>
			</tbody>
		</table>
	</div>
	<?php
}

// ── Save settings (admin-post handler) ────────────────────────────────────────

function bm_handle_save_settings(): void {
	check_admin_referer( 'bm_save_settings_nonce' );

	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( 'Insufficient permissions.' );
	}

	$raw  = sanitize_text_field( $_POST['bm_wikidata_lang'] ?? 'en' );
	$lang = preg_replace( '/[^a-z\-]/', '', strtolower( $raw ) );
	if ( ! $lang ) {
		$lang = 'en';
	}

	update_option( 'bm_settings', [ 'wikidata_lang' => $lang ] );

	wp_redirect( add_query_arg( [
		'page'   => 'breadcrumb-migration',
		'tab'    => 'settings',
		'bm_msg' => 'saved',
	], admin_url( 'admin.php' ) ) );
	exit;
}
