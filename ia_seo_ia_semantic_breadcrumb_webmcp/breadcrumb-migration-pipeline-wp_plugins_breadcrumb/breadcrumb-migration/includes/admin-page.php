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
	$filter_taxonomy = sanitize_text_field( $_GET['bm_taxonomy'] ?? 'all' );
	$filter_state    = sanitize_text_field( $_GET['bm_state']    ?? 'all' );
	$search          = sanitize_text_field( $_GET['bm_search']   ?? '' );
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
	bm_render_filters( $base_url, $filter_taxonomy, $filter_state, $search );

	if ( empty( $rows ) ) {
		?>
		<div class="bm-empty">
			<?php if ( $total === 0 && $filter_taxonomy === 'all' && $search === '' ) : ?>
				<p><?php esc_html_e( 'No terms found. Run the pipeline then import via the Import & Export tab, or run Step 4 with --no-dry-run.', 'breadcrumb-migration' ); ?></p>
				<code>python source/pipeline/004_step_4_breadcrumb_proposal.py --auto-input --no-dry-run</code>
			<?php else : ?>
				<p><?php esc_html_e( 'No terms match your filters.', 'breadcrumb-migration' ); ?></p>
			<?php endif; ?>
		</div>
		<?php
	} else {
		?>
		<div class="bm-term-list">
			<?php foreach ( $rows as $row ) : ?>
				<?php bm_render_term_card( $row ); ?>
			<?php endforeach; ?>
		</div>
		<?php bm_render_pagination( $total, $per_page, $current_page, $base_url, $filter_taxonomy, $filter_state, $search ); ?>
		<?php
	}
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
		<p class="description">
			<?php esc_html_e( 'Paste keywords (one per line or comma-separated). Select a parent category, then click Assign. Each keyword will be matched by name against post_tag terms in the migration database and assigned the selected category as breadcrumb parent.', 'breadcrumb-migration' ); ?>
		</p>

		<div class="bm-bulk-form">
			<div class="bm-bulk-form__field">
				<label for="bm-bulk-keywords">
					<strong><?php esc_html_e( 'Keywords', 'breadcrumb-migration' ); ?></strong>
					<span class="description"><?php esc_html_e( 'One per line or comma-separated', 'breadcrumb-migration' ); ?></span>
				</label>
				<textarea id="bm-bulk-keywords" rows="14" class="bm-bulk-keywords"
					placeholder="<?php esc_attr_e( 'One keyword per line, e.g.&#10;Adolph Zukor&#10;Brand content&#10;Hollywood', 'breadcrumb-migration' ); ?>"></textarea>
			</div>

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

			<div class="bm-bulk-form__actions">
				<button type="button" class="button button-primary bm-btn-bulk-assign">
					<?php esc_html_e( 'Assign Category to Selected Keywords', 'breadcrumb-migration' ); ?>
				</button>
			</div>
		</div>

		<div id="bm-bulk-results" style="display:none;" class="bm-bulk-results"></div>
	</div>
	<?php
}

// ── Bulk Description tab ───────────────────────────────────────────────────────

function bm_render_tab_bulk_description(): void {
	global $wpdb;
	$t = bm_tables();

	$rows = $wpdb->get_results( // phpcs:ignore
		"SELECT p.id AS proposal_id, p.wikidata_id, p.wikidata_description,
		        p.proposed_description, p.proposed_slug,
		        t.wp_term_id, t.original_name
		 FROM {$t['proposals']} p
		 JOIN {$t['terms']} t ON t.id = p.term_id
		 WHERE p.validation_state = 'approved'
		 ORDER BY t.original_name ASC"
	);
	?>
	<div class="bm-section">
		<h2><?php esc_html_e( 'Bulk Description', 'breadcrumb-migration' ); ?></h2>
		<div class="notice notice-warning inline bm-bulk-desc-caution">
			<p>
				<strong><?php esc_html_e( 'Use after Bulk Assign:', 'breadcrumb-migration' ); ?></strong>
				<?php esc_html_e( 'Each approved tag needs a breadcrumb parent category assigned (via the Bulk Assign tab) before saving a description. Without it the breadcrumb shows the generic "Tag" crumb instead of a real category.', 'breadcrumb-migration' ); ?>
			</p>
		</div>

		<p class="description">
			<?php esc_html_e( 'For each approved tag, review the Wikidata description and save it as the WordPress tag description. Edit the Wikidata ID if incorrect, click Fetch to retrieve the description, then select rows and click "Save Description to WordPress".', 'breadcrumb-migration' ); ?>
		</p>

		<?php if ( empty( $rows ) ) : ?>
			<p class="bm-no-data"><?php esc_html_e( 'No approved tags found. Approve proposals in the Proposals tab first.', 'breadcrumb-migration' ); ?></p>
		<?php else : ?>
			<div class="bm-bulk-desc-actions-top">
				<button type="button" class="button button-primary bm-btn-bulk-save-desc">
					<?php esc_html_e( 'Save Description to WordPress', 'breadcrumb-migration' ); ?>
				</button>
				<span class="description">
					<?php esc_html_e( 'Copies Wikidata description → tag Description field for all selected rows.', 'breadcrumb-migration' ); ?>
				</span>
			</div>

			<div class="bm-bulk-desc-filters" id="bm-bulk-desc-filters">
				<strong><?php esc_html_e( 'Show only:', 'breadcrumb-migration' ); ?></strong>
				<label>
					<input type="checkbox" id="bm-filter-wd-id-empty" class="bm-desc-filter">
					<?php esc_html_e( 'Wikidata ID empty', 'breadcrumb-migration' ); ?>
				</label>
				<label>
					<input type="checkbox" id="bm-filter-wd-desc-empty" class="bm-desc-filter">
					<?php esc_html_e( 'Description from Wikidata empty', 'breadcrumb-migration' ); ?>
				</label>
				<label>
					<input type="checkbox" id="bm-filter-actual-desc-empty" class="bm-desc-filter">
					<?php esc_html_e( 'Actual Description empty', 'breadcrumb-migration' ); ?>
				</label>
				<button type="button" class="button button-small" id="bm-desc-filter-reset">
					<?php esc_html_e( 'Show all', 'breadcrumb-migration' ); ?>
				</button>
			</div>

			<table class="widefat striped bm-bulk-desc-table" id="bm-bulk-desc-table">
				<thead>
					<tr>
						<th class="bm-bulk-col-cb">
							<label>
								<input type="checkbox" id="bm-desc-select-all">
								<?php esc_html_e( 'All', 'breadcrumb-migration' ); ?>
							</label>
						</th>
						<th><?php esc_html_e( 'Wikidata ID', 'breadcrumb-migration' ); ?></th>
						<th><?php esc_html_e( 'Slug', 'breadcrumb-migration' ); ?></th>
						<th><?php esc_html_e( 'Description from Wikidata', 'breadcrumb-migration' ); ?></th>
						<th><?php esc_html_e( 'Actual Description', 'breadcrumb-migration' ); ?></th>
					</tr>
				</thead>
				<tbody>
				<?php foreach ( $rows as $row ) :
					$proposal_id = (int) $row->proposal_id;
					$tag_url     = $row->proposed_slug
						? home_url( '/tag/' . trailingslashit( sanitize_title( $row->proposed_slug ) ) )
						: '';
				?>
					<tr class="bm-bulk-desc-row"
						data-proposal-id="<?php echo esc_attr( $proposal_id ); ?>"
						data-wd-id-empty="<?php echo empty( $row->wikidata_id ) ? '1' : '0'; ?>"
						data-wd-desc-empty="<?php echo empty( $row->wikidata_description ) ? '1' : '0'; ?>"
						data-actual-desc-empty="<?php echo empty( $row->proposed_description ) ? '1' : '0'; ?>">
						<td class="bm-bulk-col-cb">
							<input type="checkbox" class="bm-desc-cb"
								value="<?php echo esc_attr( $proposal_id ); ?>">
						</td>
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
								<?php if ( $row->wikidata_id ) : ?>
									<a href="<?php echo esc_url( 'https://www.wikidata.org/wiki/' . $row->wikidata_id ); ?>"
										target="_blank" rel="noopener noreferrer"
										class="bm-wikidata-ext-link bm-desc-wd-link">↗</a>
								<?php endif; ?>
							</div>
						</td>
						<td>
							<?php if ( $row->proposed_slug ) : ?>
								<code><?php echo esc_html( $row->proposed_slug ); ?></code>
								<?php if ( $tag_url ) : ?>
									&nbsp;<a href="<?php echo esc_url( $tag_url ); ?>"
										target="_blank" rel="noopener noreferrer">
										<?php esc_html_e( 'View tag', 'breadcrumb-migration' ); ?>
									</a>
								<?php endif; ?>
							<?php else : ?>
								<code>—</code>
							<?php endif; ?>
						</td>
						<td class="bm-desc-wikidata-text">
							<?php echo esc_html( $row->wikidata_description ?? '' ); ?>
						</td>
						<td class="bm-desc-actual-text">
							<?php if ( ! empty( $row->proposed_description ) ) :
								echo esc_html( $row->proposed_description );
							else : ?>
								<em class="bm-no-data"><?php esc_html_e( 'Empty', 'breadcrumb-migration' ); ?></em>
							<?php endif; ?>
						</td>
					</tr>
				<?php endforeach; ?>
				</tbody>
			</table>

			<div class="bm-bulk-desc-actions-bottom">
				<button type="button" class="button button-primary bm-btn-bulk-save-desc">
					<?php esc_html_e( 'Save Description to WordPress', 'breadcrumb-migration' ); ?>
				</button>
				<span class="description">
					<?php esc_html_e( 'Copies Wikidata description → tag Description field for all selected rows.', 'breadcrumb-migration' ); ?>
				</span>
			</div>

			<div id="bm-bulk-desc-results" style="display:none; margin-top:16px;"></div>
		<?php endif; ?>
	</div>
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

// ── Stats bar ──────────────────────────────────────────────────────────────────

function bm_render_stats( array $stats ): void {
	$labels = [
		'pending'  => __( 'Pending',  'breadcrumb-migration' ),
		'approved' => __( 'Approved', 'breadcrumb-migration' ),
		'rejected' => __( 'Rejected', 'breadcrumb-migration' ),
	];
	echo '<div class="bm-stats">';
	foreach ( $labels as $key => $label ) {
		$count = $stats[ $key ] ?? 0;
		printf(
			'<span class="bm-stat bm-stat--%s"><strong>%d</strong> %s</span>',
			esc_attr( $key ),
			(int) $count,
			esc_html( $label )
		);
	}
	echo '</div>';
}

// ── Filter bar ─────────────────────────────────────────────────────────────────

function bm_render_filters( string $base_url, string $taxonomy, string $state, string $search ): void {
	?>
	<form method="get" action="<?php echo esc_url( $base_url ); ?>" class="bm-filters">
		<input type="hidden" name="page" value="breadcrumb-migration">

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

		<input type="search" name="bm_search" value="<?php echo esc_attr( $search ); ?>"
			placeholder="<?php esc_attr_e( 'Search term name…', 'breadcrumb-migration' ); ?>">

		<button type="submit" class="button"><?php esc_html_e( 'Filter', 'breadcrumb-migration' ); ?></button>
		<a href="<?php echo esc_url( $base_url ); ?>" class="button"><?php esc_html_e( 'Reset', 'breadcrumb-migration' ); ?></a>
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
					<tr><th><?php esc_html_e( 'Name',      'breadcrumb-migration' ); ?></th><td><?php echo esc_html( $row->original_name ); ?></td></tr>
					<tr><th><?php esc_html_e( 'Slug',      'breadcrumb-migration' ); ?></th><td><code><?php echo esc_html( $row->original_slug ); ?></code></td></tr>
					<tr><th><?php esc_html_e( 'Parent ID', 'breadcrumb-migration' ); ?></th><td><?php echo $row->original_parent_id ? esc_html( $row->original_parent_id ) : '—'; ?></td></tr>
					<tr><th><?php esc_html_e( 'Posts',     'breadcrumb-migration' ); ?></th><td><?php echo esc_html( $row->content_count ); ?></td></tr>
				</table>

				<div class="bm-card__actions bm-card__actions--original">
					<button class="button bm-btn-simulate"
						data-term-id="<?php echo esc_attr( $term_id ); ?>">
						<?php esc_html_e( 'Simulate', 'breadcrumb-migration' ); ?>
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
							<th><?php esc_html_e( 'Description', 'breadcrumb-migration' ); ?></th>
							<td class="bm-desc"><?php echo esc_html( $row->wikidata_description ?? '—' ); ?></td>
						</tr>
						<tr>
							<th><?php esc_html_e( 'Breadcrumb', 'breadcrumb-migration' ); ?></th>
							<td class="bm-breadcrumb-preview"><?php echo $bc_html; // already escaped above ?></td>
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
					<label><?php esc_html_e( 'Description', 'breadcrumb-migration' ); ?>
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

// ── Pagination ─────────────────────────────────────────────────────────────────

function bm_render_pagination( int $total, int $per_page, int $current, string $base_url, string $taxonomy, string $state, string $search ): void {
	$total_pages = (int) ceil( $total / $per_page );
	if ( $total_pages <= 1 ) {
		return;
	}

	$url_params = add_query_arg( [
		'bm_taxonomy' => $taxonomy,
		'bm_state'    => $state,
		'bm_search'   => $search,
	], $base_url );

	echo '<div class="bm-pagination">';
	printf(
		'<span class="bm-pagination__info">%s</span>',
		sprintf(
			/* translators: 1: current page, 2: total pages, 3: total items */
			esc_html__( 'Page %1$d of %2$d (%3$d terms)', 'breadcrumb-migration' ),
			$current,
			$total_pages,
			$total
		)
	);

	if ( $current > 1 ) {
		printf(
			'<a href="%s" class="button">%s</a>',
			esc_url( add_query_arg( 'paged', $current - 1, $url_params ) ),
			esc_html__( '← Previous', 'breadcrumb-migration' )
		);
	}
	if ( $current < $total_pages ) {
		printf(
			'<a href="%s" class="button">%s</a>',
			esc_url( add_query_arg( 'paged', $current + 1, $url_params ) ),
			esc_html__( 'Next →', 'breadcrumb-migration' )
		);
	}
	echo '</div>';
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
