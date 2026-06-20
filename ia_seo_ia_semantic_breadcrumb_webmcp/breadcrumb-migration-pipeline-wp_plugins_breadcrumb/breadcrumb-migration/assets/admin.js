/* Breadcrumb Migration — Admin JS */
/* global bmData, jQuery */

( function ( $ ) {
	'use strict';

	const { ajaxUrl, nonce, i18n } = bmData;

	// Persistent filter state — survive button clicks that call bmDescApplyFilters()
	let bmActiveTagFilter   = [];
	let bmActiveSearchQuery = '';

	// spaCy named-entity list — shared by toolbar and per-row selects
	const BM_SPACY_ENTITIES = [
		[ '',            '— none —' ],
		[ 'PERSON',      'PERSON — People, including fictional' ],
		[ 'NORP',        'NORP — Nationalities, religious or political groups' ],
		[ 'FAC',         'FAC — Buildings, airports, highways, bridges' ],
		[ 'ORG',         'ORG — Companies, agencies, institutions' ],
		[ 'GPE',         'GPE — Countries, cities, states' ],
		[ 'LOC',         'LOC — Non-GPE locations, mountain ranges, bodies of water' ],
		[ 'PRODUCT',     'PRODUCT — Objects, vehicles, foods (not services)' ],
		[ 'EVENT',       'EVENT — Hurricanes, battles, wars, sports events' ],
		[ 'WORK_OF_ART', 'WORK_OF_ART — Titles of books, songs, etc.' ],
		[ 'LAW',         'LAW — Named documents made into laws' ],
		[ 'LANGUAGE',    'LANGUAGE — Any named language' ],
		[ 'DATE',        'DATE — Absolute or relative dates or periods' ],
		[ 'TIME',        'TIME — Times smaller than a day' ],
		[ 'PERCENT',     'PERCENT — Percentage, including "%"' ],
		[ 'MONEY',       'MONEY — Monetary values, including unit' ],
		[ 'QUANTITY',    'QUANTITY — Measurements, weight or distance' ],
		[ 'ORDINAL',     'ORDINAL — "first", "second", etc.' ],
		[ 'CARDINAL',    'CARDINAL — Numerals not under another type' ],
	];

	// ── Helper ────────────────────────────────────────────────────────────────

	function post( action, data ) {
		return $.post( ajaxUrl, { action, nonce, ...data } );
	}

	function flashNotice( message, type = 'success' ) {
		const $notice = $(
			`<div class="notice notice-${type} is-dismissible bm-notice"><p>${message}</p></div>`
		);
		$( '.bm-wrap h1' ).after( $notice );
		setTimeout( () => $notice.fadeOut( 400, () => $notice.remove() ), 4000 );
	}

	// ── Simulate breadcrumb ───────────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-simulate', function () {
		const $btn    = $( this );
		const termId  = $btn.data( 'term-id' );
		const $result = $( `.bm-simulate-result[data-term-id="${termId}"]` );

		$btn.addClass( 'bm-loading' ).text( '…' );

		post( 'bm_simulate_breadcrumb', { term_id: termId } )
			.done( function ( res ) {
				if ( res.success ) {
					$result.html( res.data.html ).slideDown( 200 );
				} else {
					$result.html( `<em class="bm-error">${res.data?.message ?? i18n.error}</em>` ).show();
				}
			} )
			.fail( () => $result.html( `<em class="bm-error">${i18n.error}</em>` ).show() )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Simulate' ) );
	} );

	// ── Validate (approve) ────────────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-validate', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $card      = $btn.closest( '.bm-card' );

		$btn.addClass( 'bm-loading' );

		post( 'bm_validate_proposal', { proposal_id: proposalId, action_type: 'approve' } )
			.done( function ( res ) {
				if ( res.success ) {
					const state = res.data.state;
					$card
						.removeClass( 'bm-state--pending bm-state--rejected' )
						.addClass( `bm-state--${state}` );
					$card.find( '.bm-badge--state' )
						.attr( 'class', `bm-badge bm-badge--state bm-badge--${state}` )
						.text( res.data.label );
					// Replace validate/reject buttons with publish button
					$card.find( '.bm-card__actions--original' )
						.find( '.bm-btn-validate, .bm-btn-reject' )
						.remove();
					$card.find( '.bm-card__actions--proposed' ).prepend(
						`<button class="button button-primary bm-btn-publish"
							data-proposal-id="${proposalId}">${ bmData.i18n.publishing.replace( '…', '' ) } →</button>`
					);
					flashNotice( `Approved: ${ $card.find('.bm-card__title').text() }` );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ) );
	} );

	// ── Reject ────────────────────────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-reject', function () {
		if ( ! window.confirm( i18n.confirmReject ) ) return;

		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $card      = $btn.closest( '.bm-card' );

		$btn.addClass( 'bm-loading' );

		post( 'bm_validate_proposal', { proposal_id: proposalId, action_type: 'reject' } )
			.done( function ( res ) {
				if ( res.success ) {
					const state = res.data.state;
					$card
						.removeClass( 'bm-state--pending bm-state--approved' )
						.addClass( `bm-state--${state}` );
					$card.find( '.bm-badge--state' )
						.attr( 'class', `bm-badge bm-badge--state bm-badge--${state}` )
						.text( res.data.label );
					flashNotice( `Rejected: ${ $card.find('.bm-card__title').text() }`, 'warning' );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ) );
	} );

	// ── Edit (show inline form) ───────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-edit', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		$( `.bm-edit-form[data-proposal-id="${proposalId}"]` ).slideToggle( 200 );
	} );

	$( document ).on( 'click', '.bm-btn-cancel-edit', function () {
		$( this ).closest( '.bm-edit-form' ).slideUp( 200 );
	} );

	// ── Save inline edit ──────────────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-save-edit', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $form      = $btn.closest( '.bm-edit-form' );

		const data = {
			proposal_id:             proposalId,
			proposed_name:           $form.find( '[name="proposed_name"]' ).val(),
			proposed_slug:           $form.find( '[name="proposed_slug"]' ).val(),
			proposed_description:    $form.find( '[name="proposed_description"]' ).val(),
			tag_parent_category_id:  $form.find( '[name="tag_parent_category_id"]' ).val() || 0,
			wikidata_label:          $form.find( '[name="wikidata_label"]' ).val().trim(),
			spacy_entity:            $form.find( '[name="spacy_entity"]' ).val(),
			wikidata_id:             $form.find( '[name="wikidata_id"]' ).val().trim(),
		};

		$btn.addClass( 'bm-loading' );

		post( 'bm_update_proposal', data )
			.done( function ( res ) {
				if ( res.success ) {
					// Update displayed values
					const $card = $form.closest( '.bm-card' );
					const f = res.data.fields;
					$card.find( `.bm-editable[data-field="proposed_name"]` ).text( f.proposed_name );
					$card.find( `.bm-editable[data-field="proposed_slug"]` ).html( `<code>${f.proposed_slug}</code>` );
					$card.find( '.bm-card__title' ).text( f.proposed_name );

					// Refresh spaCy entity display
					const $spaCyCell = $card.find( '.bm-col--proposed .bm-data-table' )
						.find( 'th' ).filter( function () {
							return $( this ).text().trim() === 'spaCy';
						} ).siblings( 'td' ).first();
					if ( $spaCyCell.length ) {
						$spaCyCell.html( f.spacy_entity
							? `<span class="bm-entity">${ escHtml( f.spacy_entity ) }</span>`
							: '—'
						);
					}

					// Refresh Wikidata ID display
					const $wdIdCell = $card.find( '.bm-col--proposed .bm-data-table' )
						.find( 'th' ).filter( function () {
							return $( this ).text().trim() === 'Wikidata ID';
						} ).siblings( 'td' ).first();
					if ( $wdIdCell.length ) {
						if ( f.wikidata_id ) {
							$wdIdCell.html(
								`<a href="https://www.wikidata.org/wiki/${ encodeURIComponent( f.wikidata_id ) }" target="_blank" rel="noopener">${ escHtml( f.wikidata_id ) }</a>`
							);
						} else {
							$wdIdCell.text( '—' );
						}
					}

					// Refresh Label display
					const $labelCell = $card.find( '.bm-col--proposed .bm-data-table' )
						.find( 'th' ).filter( function () {
							return $( this ).text().trim() === 'Label';
						} ).siblings( 'td' ).first();
					if ( $labelCell.length ) {
						$labelCell.text( f.wikidata_label || '—' );
					}

					// Refresh breadcrumb preview if the backend rebuilt it
					if ( res.data.proposed_breadcrumb ) {
						try {
							const crumbs = JSON.parse( res.data.proposed_breadcrumb );
							const sep    = ' <span class="bm-sep">›</span> ';
							const html   = crumbs.map( c => c.replace( /</g, '&lt;' ) ).join( sep );
							$card.find( '.bm-breadcrumb-preview' ).html( html );
						} catch ( e ) { /* leave preview as-is */ }
					}

					// Update Actual Desc cell + badge
					bmUpdateActualDescCell(
						$card,
						f.proposed_description ?? '',
						res.data.wikidata_description ?? ''
					);

					$form.slideUp( 200 );
					const msg = res.data.wp_synced
						? i18n.savedSynced
						: ( res.data.sync_error
							? 'Saved. WP sync failed: ' + res.data.sync_error
							: 'Proposal updated.' );
					flashNotice( msg );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ) );
	} );

	// ── Reset to Pending ─────────────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-reset', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $card      = $btn.closest( '.bm-card' );

		$btn.addClass( 'bm-loading' );

		post( 'bm_validate_proposal', { proposal_id: proposalId, action_type: 'reset' } )
			.done( function ( res ) {
				if ( res.success ) {
					$card
						.removeClass( 'bm-state--approved bm-state--rejected' )
						.addClass( 'bm-state--pending' );
					$card.find( '.bm-badge--state' )
						.attr( 'class', 'bm-badge bm-badge--state bm-badge--pending' )
						.text( 'Pending' );
					// Restore validate + reject in original column
					const $origActions = $card.find( '.bm-card__actions--original' );
					if ( ! $origActions.find( '.bm-btn-validate' ).length ) {
						$origActions.append(
							`<button class="button button-primary bm-btn-validate" data-proposal-id="${proposalId}">Validate</button>` +
							`<button class="button bm-btn-reject" data-proposal-id="${proposalId}">Reject</button>`
						);
					}
					// Remove publish + reset buttons from proposed column
					$card.find( '.bm-btn-publish, .bm-btn-reset' ).remove();
					flashNotice( `Reset to Pending: ${ $card.find('.bm-card__title').text() }`, 'warning' );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
					$btn.removeClass( 'bm-loading' );
				}
			} )
			.fail( () => {
				flashNotice( i18n.error, 'error' );
				$btn.removeClass( 'bm-loading' );
			} );
	} );

	// ── Empty tables (Danger Zone) ───────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-empty-tables', function () {
		const $btn    = $( this );
		const confirm = $btn.data( 'confirm' ) || 'Type CONFIRM to proceed.';
		const answer  = window.prompt( confirm );

		if ( answer !== 'CONFIRM' ) return;

		$btn.addClass( 'bm-loading' ).text( 'Deleting…' );

		post( 'bm_empty_tables', {} )
			.done( function ( res ) {
				if ( res.success ) {
					flashNotice( res.data.message, 'warning' );
					setTimeout( () => location.reload(), 2000 );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
					$btn.removeClass( 'bm-loading' ).text( 'Empty all tables' );
				}
			} )
			.fail( () => {
				flashNotice( i18n.error, 'error' );
				$btn.removeClass( 'bm-loading' ).text( 'Empty all tables' );
			} );
	} );

	// ── Publish to WordPress ──────────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-publish', function () {
		if ( ! window.confirm( i18n.confirmPublish ) ) return;

		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );

		$btn.addClass( 'bm-loading' ).text( i18n.publishing );

		post( 'bm_publish_term', { proposal_id: proposalId } )
			.done( function ( res ) {
				if ( res.success ) {
					$btn
						.removeClass( 'bm-loading bm-btn-publish button-primary' )
						.addClass( 'bm-btn-done' )
						.text( i18n.published )
						.prop( 'disabled', true );

					const $card = $btn.closest( '.bm-card' );
					$card.find( '.bm-badge--state' )
						.attr( 'class', 'bm-badge bm-badge--state bm-badge--published' )
						.text( 'Published' );

					flashNotice( res.data.message );
				} else {
					$btn.removeClass( 'bm-loading' ).text( 'Publish to WP' );
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => {
				$btn.removeClass( 'bm-loading' ).text( 'Publish to WP' );
				flashNotice( i18n.error, 'error' );
			} );
	} );


	// ── Bulk Assign ───────────────────────────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-bulk-assign', function () {
		const $btn     = $( this );
		const keywords = $( '#bm-check-selected-keywords' ).val().trim();
		const catId    = $( '#bm-bulk-category' ).val();
		const $results = $( '#bm-bulk-results' );

		if ( ! keywords ) {
			flashNotice( 'Check at least one keyword in Step 1 first.', 'error' );
			return;
		}
		if ( ! catId || catId === '0' ) {
			flashNotice( 'Select a parent category.', 'error' );
			return;
		}

		$btn.addClass( 'bm-loading' ).text( 'Assigning…' );
		$results.hide().empty();

		post( 'bm_bulk_assign', { keywords, category_id: catId } )
			.done( function ( res ) {
				if ( res.success ) {
					const { results, updated, skipped, total, category } = res.data;

					let html = `<h3 class="bm-bulk-results__title">Results — assigned to <strong>${ escHtml( category ) }</strong></h3>`;
					html += `<p class="bm-bulk-results__summary">`;
					html += `<span class="bm-bulk-ok">${ updated } updated</span> · `;
					html += `<span class="bm-bulk-skip">${ skipped } skipped</span> · `;
					html += `${ total } total</p>`;
					html += '<table class="widefat striped bm-bulk-table"><thead><tr>';
					html += '<th class="bm-bulk-col-cb"><label><input type="checkbox" id="bm-select-all-bulk"> All</label></th>';
					html += '<th>Keyword</th><th>Status</th><th>Breadcrumb</th>';
					html += '</tr></thead><tbody>';

					let hasSelectable = false;

					results.forEach( function ( r ) {
						const cls = r.status === 'updated'   ? 'bm-bulk-row--ok'
								  : r.status === 'created'   ? 'bm-bulk-row--created'
								  : r.status === 'not_found' ? 'bm-bulk-row--skip'
								  : 'bm-bulk-row--err';
						const label = r.status === 'updated'   ? 'Updated'
									: r.status === 'created'   ? 'Created'
									: r.status === 'not_found' ? 'Not found'
									: 'Error';
						const canSelect = ( r.status === 'updated' || r.status === 'created' ) && r.proposal_id;
						if ( canSelect ) hasSelectable = true;
						html += `<tr class="${ cls }">`;
						html += `<td class="bm-bulk-col-cb">${ canSelect
							? `<input type="checkbox" class="bm-bulk-publish-cb" value="${ escHtml( String( r.proposal_id ) ) }" checked>`
							: '' }</td>`;
						html += `<td><strong>${ escHtml( r.keyword ) }</strong></td>`;
						html += `<td><span class="bm-bulk-status bm-bulk-status--${ escHtml( r.status ) }">${ label }</span></td>`;
						html += `<td>${ r.breadcrumb
							? escHtml( r.breadcrumb )
							: ( r.message ? `<em>${ escHtml( r.message ) }</em>` : '—' ) }</td>`;
						html += '</tr>';
					} );

					html += '</tbody></table>';

					if ( hasSelectable ) {
						html += `<div class="bm-bulk-publish-actions">
							<button type="button" class="button button-primary bm-btn-bulk-publish">
								Publish Selected to WordPress
							</button>
							<span class="bm-bulk-publish-note description">
								Approves &amp; publishes each selected tag — breadcrumb goes live on the frontend.
							</span>
						</div>`;
					}

					$results.html( html ).slideDown( 200 );
					flashNotice( `Bulk assign done: ${ updated } updated, ${ skipped } skipped.` );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Assign Category to Selected Keywords' ) );
	} );

	// ── Bulk Publish — select all ─────────────────────────────────────────────

	$( document ).on( 'change', '#bm-select-all-bulk', function () {
		const checked = $( this ).prop( 'checked' );
		$( '#bm-bulk-results .bm-bulk-publish-cb:not(:disabled)' ).prop( 'checked', checked );
	} );

	// ── Bulk Publish — publish selected ──────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-bulk-publish', function () {
		const $btn     = $( this );
		const $results = $( '#bm-bulk-results' );

		const proposalIds = [];
		$results.find( '.bm-bulk-publish-cb:checked' ).each( function () {
			proposalIds.push( $( this ).val() );
		} );

		if ( ! proposalIds.length ) {
			flashNotice( 'Select at least one keyword to publish.', 'error' );
			return;
		}

		if ( ! window.confirm(
			`Publish ${ proposalIds.length } tag(s) to WordPress? This will update the live taxonomy and make breadcrumbs available on the frontend.`
		) ) return;

		$btn.addClass( 'bm-loading' ).text( 'Publishing…' );

		post( 'bm_bulk_publish', { proposal_ids: proposalIds } )
			.done( function ( res ) {
				if ( res.success ) {
					const { results, published, errors } = res.data;
					results.forEach( function ( r ) {
						if ( r.status === 'published' ) {
							const $cb  = $results.find( `.bm-bulk-publish-cb[value="${ r.proposal_id }"]` );
							const $row = $cb.closest( 'tr' );
							$cb.prop( 'disabled', true );
							$row.find( '.bm-bulk-status' )
								.attr( 'class', 'bm-bulk-status bm-bulk-status--published' )
								.text( 'Published' );
							$row.removeClass( 'bm-bulk-row--ok bm-bulk-row--created' )
								.addClass( 'bm-bulk-row--published' );
						}
					} );
					$btn.removeClass( 'bm-loading' ).text( 'Publish Selected to WordPress' );
					if ( errors === 0 ) {
						$btn.prop( 'disabled', true ).addClass( 'bm-btn-done' );
					}
					flashNotice( `Bulk publish done: ${ published } published${ errors ? ', ' + errors + ' error(s).' : '.' }` );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
					$btn.removeClass( 'bm-loading' ).text( 'Publish Selected to WordPress' );
				}
			} )
			.fail( () => {
				flashNotice( i18n.error, 'error' );
				$btn.removeClass( 'bm-loading' ).text( 'Publish Selected to WordPress' );
			} );
	} );

	// ── Bulk Assign — step 1: check existing assignments ─────────────────────

	$( document ).on( 'click', '.bm-btn-bulk-check', function () {
		const $btn     = $( this );
		const keywords = $( '#bm-bulk-keywords' ).val().trim();
		const $results = $( '#bm-bulk-check-results' );

		if ( ! keywords ) {
			flashNotice( 'Enter at least one keyword.', 'error' );
			return;
		}

		$btn.addClass( 'bm-loading' ).text( 'Checking…' );
		$results.hide().empty();

		post( 'bm_bulk_check', { keywords } )
			.done( function ( res ) {
				if ( res.success ) {
					const { results } = res.data;
					const found      = results.filter( r => r.found ).length;
					const withParent = results.filter( r => r.parent_name ).length;

					let html = '<table class="widefat striped bm-bulk-check-table"><thead><tr>';
					html += '<th class="bm-bulk-col-cb"><label><input type="checkbox" id="bm-check-select-all"> All</label></th>';
					html += '<th>Keyword</th><th>Found in DB</th><th>Current Parent Category</th>';
					html += '</tr></thead><tbody>';

					results.forEach( function ( r ) {
						const cls = ! r.found          ? 'bm-bulk-row--skip'
								  : r.parent_name       ? 'bm-bulk-row--ok'
								  : 'bm-bulk-row--err';
						const canCheck = r.found;
						html += `<tr class="${ cls }">`;
						html += `<td class="bm-bulk-col-cb">${ canCheck
							? `<input type="checkbox" class="bm-check-cb" value="${ escHtml( r.keyword ) }">`
							: '' }</td>`;
						html += `<td><strong>${ escHtml( r.keyword ) }</strong></td>`;
						html += `<td>${ r.found ? '&#10003; Yes' : '&#10007; Not found' }</td>`;
						html += `<td>${ r.parent_name
							? `<span class="bm-bulk-status bm-bulk-status--updated">${ escHtml( r.parent_name ) }</span>`
							: ( r.found ? '<em>— none —</em>' : '—' ) }</td>`;
						html += '</tr>';
					} );

					html += '</tbody></table>';
					html += `<div class="bm-check-selected-wrap">
						<label for="bm-check-selected-keywords">
							<strong>Selected keywords</strong>
							<span class="description"> — comma-separated list of checked keywords, copy &amp; paste ready</span>
						</label>
						<textarea id="bm-check-selected-keywords" class="bm-check-selected-keywords" rows="2" readonly
							placeholder="Check keywords above to populate this list…"></textarea>
					</div>`;

					$results.html( html ).slideDown( 200 );
					flashNotice( `Check done: ${ found }/${ results.length } found in DB, ${ withParent } already have a parent category.` );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Check Current Assignments' ) );
	} );

	// ── Bulk Check — select all ───────────────────────────────────────────────

	$( document ).on( 'change', '#bm-check-select-all', function () {
		const checked = $( this ).prop( 'checked' );
		$( '#bm-bulk-check-results .bm-check-cb' ).prop( 'checked', checked );
		bmUpdateCheckSelectedKeywords();
	} );

	// ── Bulk Check — individual checkbox → update textarea ────────────────────

	$( document ).on( 'change', '.bm-check-cb', function () {
		const total   = $( '#bm-bulk-check-results .bm-check-cb' ).length;
		const checked = $( '#bm-bulk-check-results .bm-check-cb:checked' ).length;
		$( '#bm-check-select-all' )
			.prop( 'indeterminate', checked > 0 && checked < total )
			.prop( 'checked', checked > 0 && checked === total );
		bmUpdateCheckSelectedKeywords();
	} );

	function bmUpdateCheckSelectedKeywords() {
		const keywords = [];
		$( '#bm-bulk-check-results .bm-check-cb:checked' ).each( function () {
			keywords.push( $( this ).val() );
		} );
		$( '#bm-check-selected-keywords' ).val( keywords.join( ', ' ) );
	}

	// ── Bulk Description tab ─────────────────────────────────────────────────

	// ── Bulk Description — row filter ────────────────────────────────────────

	function bmUpdateRowStatus( $row ) {
		const wdIdEmpty    = $row.attr( 'data-wd-id-empty' )       === '1';
		const wdDescEmpty  = $row.attr( 'data-wd-desc-empty' )     === '1';
		const actDescEmpty = $row.attr( 'data-actual-desc-empty' ) === '1';

		let status;
		if ( ! actDescEmpty ) {
			status = 'green';
		} else if ( ! wdIdEmpty || ! wdDescEmpty ) {
			status = 'orange';
		} else {
			status = 'red';
		}

		$row
			.removeClass( 'bm-desc-row--green bm-desc-row--orange bm-desc-row--red' )
			.addClass( `bm-desc-row--${ status }` )
			.attr( 'data-row-status', status );
	}

	function bmUpdateFilterCounts() {
		const $allRows = $( '#bm-bulk-desc-table tbody .bm-bulk-desc-row' );
		if ( ! $allRows.length ) return;

		$( '#bm-count-wd-id-empty' ).text(       $allRows.filter( '[data-wd-id-empty="1"]' ).length );
		$( '#bm-count-wd-id-filled' ).text(      $allRows.filter( '[data-wd-id-empty="0"]' ).length );
		$( '#bm-count-wd-desc-empty' ).text(     $allRows.filter( '[data-wd-desc-empty="1"]' ).length );
		$( '#bm-count-actual-desc-empty' ).text( $allRows.filter( '[data-actual-desc-empty="1"]' ).length );
		$( '#bm-count-manual-only' ).text(       $allRows.filter( '[data-desc-source="manual"]' ).length );
		$( '#bm-count-completed' ).text(         $allRows.filter( '[data-row-status="green"]' ).length );
		$( '#bm-desc-visible-count' ).text(      $allRows.filter( ':visible' ).length );
		$( '#bm-desc-total-count' ).text(        $allRows.length );
	}

	function bmSetActualBadge( $row, desc, isManual ) {
		const $cell  = $row.find( '.bm-desc-actual-text' );
		const $span  = $cell.find( '.bm-desc-actual-content' );
		let   $badge = $cell.find( '.bm-desc-actual-badge' );

		if ( desc ) {
			$span.text( desc );
			$row.attr( 'data-actual-desc-empty', '0' );
		} else {
			$span.html( '<em class="bm-no-data">Empty</em>' );
			$row.attr( 'data-actual-desc-empty', '1' );
		}

		if ( isManual && desc ) {
			if ( $badge.length ) {
				$badge.attr( 'class', 'bm-desc-actual-badge bm-desc-actual-badge--manual' ).html( '✍ Written' );
			} else {
				$cell.prepend( '<span class="bm-desc-actual-badge bm-desc-actual-badge--manual">✍ Written</span>' );
			}
			$row.attr( 'data-desc-source', 'manual' );
		} else if ( ! isManual && desc ) {
			if ( $badge.length ) {
				$badge.attr( 'class', 'bm-desc-actual-badge bm-desc-actual-badge--wikidata' ).text( 'Wikidata' );
			} else {
				$cell.prepend( '<span class="bm-desc-actual-badge bm-desc-actual-badge--wikidata">Wikidata</span>' );
			}
			$row.attr( 'data-desc-source', 'wikidata' );
		} else {
			$badge.remove();
			$row.attr( 'data-desc-source', 'empty' );
		}

		bmUpdateRowStatus( $row );
	}

	function bmDescApplyFilters() {
		const filterWdId       = $( '#bm-filter-wd-id-empty' ).prop( 'checked' );
		const filterWdIdFilled = $( '#bm-filter-wd-id-filled' ).prop( 'checked' );
		const filterWdDesc     = $( '#bm-filter-wd-desc-empty' ).prop( 'checked' );
		const filterActDesc    = $( '#bm-filter-actual-desc-empty' ).prop( 'checked' );
		const filterManual     = $( '#bm-filter-manual-only' ).prop( 'checked' );
		const filterCompleted  = $( '#bm-filter-completed' ).prop( 'checked' );
		const anyCheckbox      = filterWdId || filterWdIdFilled || filterWdDesc || filterActDesc || filterManual || filterCompleted;
		const hasTagFilter    = bmActiveTagFilter.length > 0;
		const hasSearch       = bmActiveSearchQuery.length > 0;
		const anyActive       = anyCheckbox || hasTagFilter || hasSearch;

		$( '#bm-bulk-desc-table tbody .bm-bulk-desc-row' ).each( function () {
			const $row = $( this );

			if ( ! anyActive ) {
				$row.show();
			} else {
				let show = true;
				if ( anyCheckbox ) {
					if ( filterWdId       && $row.attr( 'data-wd-id-empty' )       !== '1' ) { show = false; }
					if ( filterWdIdFilled && $row.attr( 'data-wd-id-empty' )       !== '0' ) { show = false; }
					if ( filterWdDesc     && $row.attr( 'data-wd-desc-empty' )     !== '1' ) { show = false; }
					if ( filterActDesc    && $row.attr( 'data-actual-desc-empty' ) !== '1' ) { show = false; }
					if ( filterManual     && $row.attr( 'data-desc-source' )       !== 'manual' ) { show = false; }
					if ( filterCompleted  && $row.attr( 'data-row-status' )        !== 'green' ) { show = false; }
				}
				if ( show && hasTagFilter ) {
					const name = $row.attr( 'data-tag-name' ) || '';
					if ( bmActiveTagFilter.indexOf( name ) === -1 ) { show = false; }
				}
				if ( show && hasSearch ) {
					const name = $row.attr( 'data-tag-name' ) || '';
					if ( name.indexOf( bmActiveSearchQuery ) === -1 ) { show = false; }
				}
				$row.toggle( show );
			}
		} );

		bmUpdateFilterCounts();
	}

	$( document ).on( 'change', '.bm-desc-filter', bmDescApplyFilters );

	$( document ).on( 'click', '#bm-desc-filter-reset', function () {
		$( '#bm-filter-wd-id-empty, #bm-filter-wd-id-filled, #bm-filter-wd-desc-empty, #bm-filter-actual-desc-empty, #bm-filter-manual-only, #bm-filter-completed' ).prop( 'checked', false );
		bmDescApplyFilters();
	} );

	$( document ).on( 'change', '#bm-desc-select-all', function () {
		const checked = $( this ).prop( 'checked' );
		$( '#bm-bulk-desc-table .bm-desc-cb:not(:disabled)' ).prop( 'checked', checked );
	} );

	$( document ).on( 'click', '.bm-btn-fetch-wikidata-desc', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $row       = $btn.closest( 'tr' );
		const wikidataId = $row.find( '.bm-desc-wikidata-id' ).val().trim().toUpperCase();

		if ( ! wikidataId ) {
			flashNotice( 'Enter a Wikidata ID first (e.g. Q42).', 'error' );
			return;
		}

		$btn.addClass( 'bm-loading' ).text( '…' );

		post( 'bm_fetch_wikidata_description', { proposal_id: proposalId, wikidata_id: wikidataId } )
			.done( function ( res ) {
				if ( res.success ) {
					const desc    = res.data.description || '';
					const $wdCell = $row.find( '.bm-desc-wikidata-text' );
					$wdCell.find( '.bm-desc-wikidata-content' ).text( desc );

					// Add or remove per-row copy button based on whether desc is now filled
					if ( desc ) {
						if ( ! $wdCell.find( '.bm-desc-wd-copy-wrap' ).length ) {
							$wdCell.append(
								`<div class="bm-desc-wd-copy-wrap"><button type="button" class="button button-small bm-btn-copy-wd-desc" data-proposal-id="${ escHtml( String( proposalId ) ) }">→ Copy to Actual</button></div>`
							);
						}
					} else {
						$wdCell.find( '.bm-desc-wd-copy-wrap' ).remove();
					}

					// Update the Wikidata link href in case the ID was corrected
					const $link = $row.find( '.bm-desc-wd-link' );
					if ( $link.length ) {
						$link.attr( 'href', 'https://www.wikidata.org/wiki/' + encodeURIComponent( res.data.wikidata_id ) );
					} else if ( res.data.wikidata_id ) {
						$row.find( '.bm-desc-wikidata-id-wrap' ).append(
							`<a href="https://www.wikidata.org/wiki/${ encodeURIComponent( res.data.wikidata_id ) }"
								target="_blank" rel="noopener noreferrer"
								class="bm-wikidata-ext-link bm-desc-wd-link">↗</a>`
						);
					}

					// Sync data attributes so filters stay accurate
					$row.attr( 'data-wd-id-empty',  res.data.wikidata_id ? '0' : '1' );
					$row.attr( 'data-wd-desc-empty', desc ? '0' : '1' );
					bmUpdateRowStatus( $row );
					bmDescApplyFilters();

					if ( desc ) {
						$wdCell.addClass( 'bm-field-filled' );
						setTimeout( () => $wdCell.removeClass( 'bm-field-filled' ), 1500 );
					}
					flashNotice( 'Wikidata description fetched.' + ( res.data.label ? ' Label: ' + res.data.label : '' ) );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Fetch' ) );
	} );

	// ── Bulk Description — inline Wikidata search ───────────────────────────────

	$( document ).on( 'click', '.bm-btn-search-single-wikidata', function ( e ) {
		e.stopPropagation();
		const $btn     = $( this );
		const tagName  = $btn.data( 'tag-name' );
		const $td      = $btn.closest( 'td' );
		const $results = $td.find( '.bm-desc-search-results' );

		if ( ! tagName ) return;

		$btn.addClass( 'bm-loading' ).text( '…' );
		$results.hide().empty();

		post( 'bm_search_wikidata', { query: tagName } )
			.done( function ( res ) {
				if ( res.success && res.data.results.length ) {
					const html = res.data.results.map( function ( r ) {
						return `<div class="bm-desc-search-result" data-id="${ escHtml( r.id ) }" data-label="${ escHtml( r.label ) }" tabindex="0">` +
							`<span class="bm-desc-sr-qid">${ escHtml( r.id ) }</span>` +
							`<span class="bm-desc-sr-label">${ escHtml( r.label ) }</span>` +
							( r.description ? `<span class="bm-desc-sr-desc">${ escHtml( r.description ) }</span>` : '' ) +
							`</div>`;
					} ).join( '' );
					$results.html( html ).show();
				} else {
					$results.html( '<p class="bm-desc-sr-empty">No results found on Wikidata.</p>' ).show();
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Search' ) );
	} );

	$( document ).on( 'click', '.bm-desc-search-result', function () {
		const $result = $( this );
		const $td     = $result.closest( 'td' );
		const qid     = $result.data( 'id' );

		$td.find( '.bm-desc-wikidata-id' ).val( qid ).addClass( 'bm-field-filled' );
		setTimeout( () => $td.find( '.bm-desc-wikidata-id' ).removeClass( 'bm-field-filled' ), 1200 );
		$td.find( '.bm-desc-search-results' ).hide().empty();
	} );

	$( document ).on( 'click', function ( e ) {
		if ( ! $( e.target ).closest( '.bm-desc-td-wikidata-id' ).length ) {
			$( '.bm-desc-search-results:visible' ).hide().empty();
		}
	} );

	$( document ).on( 'click', '.bm-btn-bulk-save-desc', function () {
		const $btn       = $( this );
		const proposalIds = [];

		$( '#bm-bulk-desc-table .bm-desc-cb:checked' ).each( function () {
			proposalIds.push( $( this ).val() );
		} );

		if ( ! proposalIds.length ) {
			flashNotice( 'Select at least one tag.', 'error' );
			return;
		}

		if ( ! window.confirm(
			`Save Wikidata description for ${ proposalIds.length } tag(s) to WordPress? This updates the live tag Description field.`
		) ) return;

		$btn.addClass( 'bm-loading' ).text( 'Saving…' );

		post( 'bm_bulk_save_description', { proposal_ids: proposalIds } )
			.done( function ( res ) {
				if ( res.success ) {
					const { results, saved, errors } = res.data;
					results.forEach( function ( r ) {
						const $cb  = $( `#bm-bulk-desc-table .bm-desc-cb[value="${ r.proposal_id }"]` );
						const $row = $cb.closest( 'tr' );
						if ( r.status === 'saved' ) {
							$cb.prop( 'disabled', true ).prop( 'checked', false );
							bmSetActualBadge( $row, r.description, false );
							bmUpdateRowStatus( $row );
							$row.removeClass( 'bm-bulk-desc-row--err' );
						} else {
							$row.addClass( 'bm-bulk-desc-row--err' );
						}
					} );
					bmDescApplyFilters();
					flashNotice( `Bulk description saved: ${ saved } saved${ errors ? ', ' + errors + ' skipped/error(s).' : '.' }` );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Save to WordPress' ) );
	} );

	// ── Bulk Description — export CSV / JSON ─────────────────────────────────

	function bmBulkDescGetSelectedRows() {
		const $checked = $( '#bm-bulk-desc-table .bm-desc-cb:checked' );
		if ( $checked.length ) {
			return $checked.map( function () { return $( this ).closest( 'tr' )[0]; } ).get();
		}
		return $( '#bm-bulk-desc-table tbody tr:visible' ).get();
	}

	function bmBulkDescRowToObject( row ) {
		const $row       = $( row );
		const $actualEl  = $row.find( '.bm-desc-actual-content' );
		const actualDesc = $actualEl.find( 'em.bm-no-data' ).length ? '' : $actualEl.text().trim();
		return {
			tag_name:             $row.find( '.bm-desc-tag-name' ).text().trim(),
			proposed_slug:        $row.find( '.bm-desc-td-tag code' ).text().trim(),
			wp_term_id:           $row.find( '.bm-desc-wp-id' ).val() || '',
			wikidata_id:          $row.find( '.bm-desc-wikidata-id' ).val().trim(),
			wikidata_description: $row.find( '.bm-desc-wikidata-content' ).text().trim(),
			actual_description:   actualDesc,
			desc_source:          $row.attr( 'data-desc-source' ) || '',
		};
	}

	function bmTriggerDownload( content, filename, mimeType ) {
		const blob = new Blob( [ content ], { type: mimeType } );
		const url  = URL.createObjectURL( blob );
		const a    = document.createElement( 'a' );
		a.href     = url;
		a.download = filename;
		document.body.appendChild( a );
		a.click();
		document.body.removeChild( a );
		URL.revokeObjectURL( url );
	}

	function bmExportTimestamp() {
		const d = new Date();
		return d.getFullYear() +
			String( d.getMonth() + 1 ).padStart( 2, '0' ) +
			String( d.getDate() ).padStart( 2, '0' ) + '_' +
			String( d.getHours() ).padStart( 2, '0' ) +
			String( d.getMinutes() ).padStart( 2, '0' ) +
			String( d.getSeconds() ).padStart( 2, '0' );
	}

	$( document ).on( 'click', '.bm-btn-export-json', function () {
		const rows = bmBulkDescGetSelectedRows();
		if ( ! rows.length ) { flashNotice( 'No rows to export.', 'error' ); return; }
		const data = rows.map( bmBulkDescRowToObject );
		bmTriggerDownload(
			JSON.stringify( data, null, 2 ),
			'breadcrumb_migration_bulk_description_' + bmExportTimestamp() + '.json',
			'application/json'
		);
		flashNotice( `Exported ${ data.length } row(s) as JSON.` );
	} );

	$( document ).on( 'click', '.bm-btn-export-csv', function () {
		const rows = bmBulkDescGetSelectedRows();
		if ( ! rows.length ) { flashNotice( 'No rows to export.', 'error' ); return; }
		const data    = rows.map( bmBulkDescRowToObject );
		const headers = Object.keys( data[0] );
		const csvRows = [ headers.join( ',' ) ].concat(
			data.map( function ( r ) {
				return headers.map( function ( h ) {
					return '"' + String( r[ h ] ).replace( /"/g, '""' ) + '"';
				} ).join( ',' );
			} )
		);
		bmTriggerDownload(
			'﻿' + csvRows.join( '\r\n' ),
			'breadcrumb_migration_bulk_description_' + bmExportTimestamp() + '.csv',
			'text/csv;charset=utf-8;'
		);
		flashNotice( `Exported ${ data.length } row(s) as CSV.` );
	} );

	// ── Delta — New Tags ──────────────────────────────────────────────────────

	function escHtml( str ) {
		return String( str )
			.replace( /&/g,  '&amp;' )
			.replace( /</g,  '&lt;' )
			.replace( />/g,  '&gt;' )
			.replace( /"/g,  '&quot;' );
	}

	function renderDeltaRow( tag ) {
		const opts = BM_SPACY_ENTITIES
			.map( ( [ v, label ] ) => `<option value="${v}">${ v || '— none —' }</option>` )
			.join( '' );
		const extUrl = 'https://www.wikidata.org/w/index.php?search=' +
			encodeURIComponent( tag.name ) + '&language=' + encodeURIComponent( bmData.wikidataLang || 'en' );

		return `
			<div class="bm-delta-row" data-wp-term-id="${escHtml( tag.wp_term_id )}">
				<div class="bm-delta-header">
					<input type="checkbox" class="bm-delta-cb" data-wp-term-id="${escHtml( tag.wp_term_id )}" title="Select for bulk action">
					<strong class="bm-delta-name">${escHtml( tag.name )}</strong>
					<code>${escHtml( tag.slug )}</code>
					<span class="bm-delta-count">${escHtml( tag.count )} post(s)</span>
				</div>
				<div class="bm-wikidata-search">
					<div class="bm-wikidata-search-row">
						<input type="text" class="bm-wikidata-query"
							value="${escHtml( tag.name )}" placeholder="Search Wikidata…">
						<button type="button" class="button bm-btn-wikidata-search">Search Wikidata</button>
						<a href="${extUrl}" target="_blank" rel="noopener noreferrer"
							class="bm-wikidata-ext-link">Open on Wikidata ↗</a>
					</div>
					<div class="bm-wikidata-results"></div>
				</div>
				<div class="bm-delta-fields">
					<label>spaCy entity
						<select name="spacy_entity">${opts}</select>
					</label>
					<label>Wikidata ID
						<input type="text" name="wikidata_id" placeholder="Q42">
					</label>
					<label>Wikidata label
						<input type="text" name="wikidata_label" value="${escHtml( tag.name )}">
					</label>
					<label>Description
						<textarea name="wikidata_description" placeholder="optional…"></textarea>
					</label>
					<label>Proposed name
						<input type="text" name="proposed_name" value="${escHtml( tag.name )}">
					</label>
					<label>Proposed slug
						<input type="text" name="proposed_slug" value="${escHtml( tag.slug )}">
					</label>
				</div>
				<div class="bm-delta-actions">
					<button class="button button-primary bm-btn-add-delta"
						data-wp-term-id="${escHtml( tag.wp_term_id )}">
						Add to migration
					</button>
				</div>
			</div>`;
	}

	function renderWikidataResults( results ) {
		if ( ! results.length ) {
			return '<p class="bm-wikidata-no-results">No results found on Wikidata.</p>';
		}
		return results.map( function ( r ) {
			const itemUrl = 'https://www.wikidata.org/wiki/' + encodeURIComponent( r.id );
			return `
				<div class="bm-wikidata-result"
					data-id="${escHtml( r.id )}"
					data-label="${escHtml( r.label )}"
					data-desc="${escHtml( r.description )}">
					<span class="bm-wikidata-qid">${escHtml( r.id )}</span>
					<span class="bm-wikidata-rlabel">${escHtml( r.label )}</span>
					<span class="bm-wikidata-rdesc">${escHtml( r.description )}</span>
					<a href="${itemUrl}" target="_blank" rel="noopener noreferrer"
						class="bm-wikidata-item-link" title="Open item on Wikidata">↗</a>
					<button type="button" class="button button-small bm-btn-use-wikidata">Use</button>
				</div>`;
		} ).join( '' );
	}

	$( document ).on( 'click', '.bm-btn-scan-delta', function () {
		const $btn      = $( this );
		const $results  = $( '#bm-delta-results' );
		const keywords  = $( '#bm-delta-keywords' ).val() || '';

		$btn.addClass( 'bm-loading' ).text( 'Scanning…' );
		$results.empty();

		post( 'bm_scan_delta', { keywords } )
			.done( function ( res ) {
				if ( res.success ) {
					const { tags, count } = res.data;
					if ( count === 0 ) {
						$results.html( '<p class="bm-delta-none">No new tags found — all post_tag terms are already tracked.</p>' );
					} else {
						const entityOpts = BM_SPACY_ENTITIES
							.map( ( [ v, label ] ) => `<option value="${v}">${label}</option>` )
							.join( '' );

						$results.html(
							`<div class="bm-delta-toolbar">
								<label class="bm-delta-select-all-wrap">
									<input type="checkbox" id="bm-delta-select-all"> Select all
								</label>
								<span class="bm-delta-selected-count">0 of ${count} selected</span>
								<span class="bm-delta-toolbar-sep" aria-hidden="true"></span>
								<label class="bm-delta-entity-label" for="bm-delta-bulk-entity">spaCy entity:</label>
								<select id="bm-delta-bulk-entity" class="bm-delta-bulk-entity">${entityOpts}</select>
								<button type="button" class="button bm-btn-apply-entity" title="Set this entity on all checked rows">Apply to selected</button>
								<span class="bm-delta-toolbar-sep" aria-hidden="true"></span>
								<button class="button button-primary bm-btn-bulk-add-delta" disabled>Add to migration</button>
							</div>` +
							`<p class="bm-delta-count-msg"><strong>${count}</strong> new tag(s) found.</p>` +
							`<div class="bm-delta-list">${ tags.map( renderDeltaRow ).join( '' ) }</div>`
						);
					}
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Scan for new tags' ) );
	} );

	$( document ).on( 'click', '.bm-btn-add-delta', function () {
		const $btn   = $( this );
		const $row   = $btn.closest( '.bm-delta-row' );
		const termId = $btn.data( 'wp-term-id' );

		const data = {
			wp_term_id:           termId,
			spacy_entity:         $row.find( '[name="spacy_entity"]' ).val(),
			wikidata_id:          $row.find( '[name="wikidata_id"]' ).val().trim(),
			wikidata_label:       $row.find( '[name="wikidata_label"]' ).val().trim(),
			wikidata_description: $row.find( '[name="wikidata_description"]' ).val().trim(),
			proposed_name:        $row.find( '[name="proposed_name"]' ).val().trim(),
			proposed_slug:        $row.find( '[name="proposed_slug"]' ).val().trim(),
		};

		$btn.addClass( 'bm-loading' );

		post( 'bm_add_delta_term', data )
			.done( function ( res ) {
				if ( res.success ) {
					flashNotice( res.data.message );
					$row.fadeOut( 400, function () {
						$row.remove();
						const remaining = $( '.bm-delta-row' ).length;
						if ( remaining === 0 ) {
							$( '#bm-delta-results' ).html( '<p class="bm-delta-none">All new tags added to migration.</p>' );
						} else {
							$( '.bm-delta-count-msg strong' ).text( remaining );
						}
					} );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
					$btn.removeClass( 'bm-loading' );
				}
			} )
			.fail( () => {
				flashNotice( i18n.error, 'error' );
				$btn.removeClass( 'bm-loading' );
			} );
	} );


	// ── Delta bulk: select-all + individual checkbox ─────────────────────────

	function bmUpdateDeltaBulkToolbar() {
		const total    = $( '.bm-delta-cb' ).length;
		const checked  = $( '.bm-delta-cb:checked' ).length;
		$( '.bm-delta-selected-count' ).text( checked + ' of ' + total + ' selected' );
		$( '.bm-btn-bulk-add-delta' ).prop( 'disabled', checked === 0 );
		$( '#bm-delta-select-all' ).prop( 'indeterminate', checked > 0 && checked < total )
			.prop( 'checked', total > 0 && checked === total );
	}

	$( document ).on( 'change', '#bm-delta-select-all', function () {
		$( '.bm-delta-cb' ).prop( 'checked', $( this ).is( ':checked' ) );
		bmUpdateDeltaBulkToolbar();
	} );

	$( document ).on( 'change', '.bm-delta-cb', function () {
		bmUpdateDeltaBulkToolbar();
	} );

	$( document ).on( 'click', '.bm-btn-apply-entity', function () {
		const entity = $( '#bm-delta-bulk-entity' ).val();
		const $checked = $( '.bm-delta-cb:checked' );
		if ( ! $checked.length ) {
			flashNotice( 'Select at least one tag first.', 'error' );
			return;
		}
		$checked.each( function () {
			const $select = $( this ).closest( '.bm-delta-row' ).find( '[name="spacy_entity"]' );
			$select.val( entity ).closest( '.bm-delta-fields' ).addClass( 'bm-entity-applied' );
			setTimeout( () => $select.closest( '.bm-delta-fields' ).removeClass( 'bm-entity-applied' ), 1200 );
		} );
		const label = entity || '— none —';
		flashNotice( `Entity "${label}" applied to ${$checked.length} selected tag(s).` );
	} );

	$( document ).on( 'click', '.bm-btn-bulk-add-delta', function () {
		const $btn = $( this );
		const terms = [];

		$( '.bm-delta-cb:checked' ).each( function () {
			const $row = $( this ).closest( '.bm-delta-row' );
			terms.push( {
				wp_term_id:           $row.data( 'wp-term-id' ),
				spacy_entity:         $row.find( '[name="spacy_entity"]' ).val(),
				wikidata_id:          $row.find( '[name="wikidata_id"]' ).val().trim(),
				wikidata_label:       $row.find( '[name="wikidata_label"]' ).val().trim(),
				wikidata_description: $row.find( '[name="wikidata_description"]' ).val().trim(),
				proposed_name:        $row.find( '[name="proposed_name"]' ).val().trim(),
				proposed_slug:        $row.find( '[name="proposed_slug"]' ).val().trim(),
			} );
		} );

		if ( ! terms.length ) return;

		$btn.addClass( 'bm-loading' ).text( 'Adding…' );

		post( 'bm_bulk_add_delta_terms', { terms: JSON.stringify( terms ) } )
			.done( function ( res ) {
				if ( res.success ) {
					const { added, skipped, errors } = res.data;
					const msg = added + ' tag(s) added to migration' +
						( skipped ? ', ' + skipped + ' skipped (already tracked)' : '' ) +
						( errors.length ? ', ' + errors.length + ' error(s)' : '' ) + '.';
					flashNotice( msg );

					$( '.bm-delta-cb:checked' ).each( function () {
						$( this ).closest( '.bm-delta-row' ).fadeOut( 300, function () {
							$( this ).remove();
							const remaining = $( '.bm-delta-row' ).length;
							if ( remaining === 0 ) {
								$( '#bm-delta-results' ).html( '<p class="bm-delta-none">All new tags added to migration.</p>' );
							} else {
								$( '.bm-delta-count-msg strong' ).text( remaining );
								bmUpdateDeltaBulkToolbar();
							}
						} );
					} );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Add to migration' ) );
	} );

	// ── Wikidata search (Delta tab) ───────────────────────────────────────────

	// Update "Open on Wikidata" href as user edits the search input
	$( document ).on( 'input', '.bm-wikidata-query', function () {
		const query  = $( this ).val().trim();
		const lang   = bmData.wikidataLang || 'en';
		const extUrl = 'https://www.wikidata.org/w/index.php?search=' +
			encodeURIComponent( query ) + '&language=' + encodeURIComponent( lang );
		$( this ).closest( '.bm-wikidata-search' )
			.find( '.bm-wikidata-ext-link' ).attr( 'href', extUrl );
	} );

	$( document ).on( 'click', '.bm-btn-wikidata-search', function () {
		const $btn     = $( this );
		const $search  = $btn.closest( '.bm-wikidata-search' );
		const query    = $search.find( '.bm-wikidata-query' ).val().trim();
		const $results = $search.find( '.bm-wikidata-results' );

		if ( ! query ) return;

		$btn.addClass( 'bm-loading' ).text( 'Searching…' );
		$results.empty();

		post( 'bm_search_wikidata', { query } )
			.done( function ( res ) {
				if ( res.success ) {
					$results.html( renderWikidataResults( res.data.results ) );
				} else {
					$results.html(
						`<p class="bm-wikidata-no-results">${ escHtml( res.data?.message ?? i18n.error ) }</p>`
					);
				}
			} )
			.fail( () => $results.html(
				`<p class="bm-wikidata-no-results">${ i18n.error }</p>`
			) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( 'Search Wikidata' ) );
	} );

	$( document ).on( 'click', '.bm-btn-use-wikidata', function () {
		const $result = $( this ).closest( '.bm-wikidata-result' );
		const $row    = $result.closest( '.bm-delta-row' );

		$row.find( '[name="wikidata_id"]' ).val( $result.attr( 'data-id' ) );
		$row.find( '[name="wikidata_label"]' ).val( $result.attr( 'data-label' ) );
		$row.find( '[name="wikidata_description"]' ).val( $result.attr( 'data-desc' ) );

		$row.find( '[name="wikidata_id"], [name="wikidata_label"]' )
			.addClass( 'bm-field-filled' );
		setTimeout(
			() => $row.find( '.bm-field-filled' ).removeClass( 'bm-field-filled' ),
			1500
		);

		$result.closest( '.bm-wikidata-results' ).slideUp( 200 );
	} );

	// ── Bulk Description — live name search (persistent) ─────────────────────────

	$( document ).on( 'input', '#bm-desc-name-search', function () {
		bmActiveSearchQuery = $( this ).val().trim().toLowerCase();
		bmDescApplyFilters();
	} );

	$( document ).on( 'click', '#bm-desc-search-submit', function () {
		bmActiveSearchQuery = $( '#bm-desc-name-search' ).val().trim().toLowerCase();
		bmDescApplyFilters();
	} );

	// ── Bulk Description — tag filter textarea ───────────────────────────────────

	$( document ).on( 'click', '#bm-desc-tag-filter-apply', function () {
		const raw  = $( '#bm-desc-tag-list' ).val();
		const tags = raw.split( /[,\n\r]+/ )
			.map( t => t.trim().toLowerCase() )
			.filter( t => t.length > 0 );

		if ( ! tags.length ) {
			flashNotice( 'Enter at least one tag name.', 'error' );
			return;
		}

		bmActiveTagFilter = tags;
		bmDescApplyFilters();

		const visible = $( '#bm-bulk-desc-table tbody .bm-bulk-desc-row:visible' ).length;
		flashNotice( `Filter applied: ${ visible } tag(s) visible.` );
	} );

	$( document ).on( 'click', '#bm-desc-tag-filter-clear', function () {
		$( '#bm-desc-tag-list' ).val( '' );
		$( '#bm-desc-name-search' ).val( '' );
		bmActiveTagFilter   = [];
		bmActiveSearchQuery = '';
		bmDescApplyFilters();
	} );

	// ── Bulk Description — init filter counts on page load ──────────────────────

	if ( $( '#bm-bulk-desc-table' ).length ) {
		bmUpdateFilterCounts();
	}

	// ── Bulk Description — synchronize descriptions from WordPress ───────────────

	$( document ).on( 'click', '#bm-sync-descriptions, #bm-sync-descriptions-bottom', function () {
		const $btn = $( this );
		$btn.addClass( 'bm-loading' ).text( '↺ Syncing…' );

		post( 'bm_sync_descriptions', {} )
			.done( function ( res ) {
				if ( res.success ) {
					const descs = res.data.descriptions;
					Object.keys( descs ).forEach( function ( pid ) {
						const entry = descs[ pid ];
						if ( entry.skipped ) return;
						const $cb  = $( `#bm-bulk-desc-table .bm-desc-cb[value="${ pid }"]` );
						const $row = $cb.closest( 'tr' );
						bmSetActualBadge( $row, entry.description, entry.is_manual );
						bmUpdateRowStatus( $row );
					} );
					bmDescApplyFilters();
					const skipped = res.data.skipped || 0;
					const notice  = skipped
						? `Synchronized: ${ res.data.updated } refreshed, ${ skipped } skipped (manually written).`
						: `Synchronized: ${ res.data.updated } tag(s) refreshed from WordPress.`;
					flashNotice( notice );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( '↺ Sync from WordPress' ) );
	} );

	// ── Bulk Description — copy Wikidata desc → Actual (per row) ────────────────

	$( document ).on( 'click', '.bm-btn-copy-wd-desc', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $row       = $btn.closest( 'tr' );

		if ( $row.attr( 'data-desc-source' ) === 'manual' ) {
			const tagName = $row.find( '.bm-desc-tag-name' ).text().trim();
			if ( ! window.confirm(
				'⚠ "' + tagName + '" has a hand-written description.\nOverwrite it with the Wikidata text?'
			) ) return;
		}

		$btn.addClass( 'bm-loading' ).text( '…' );

		post( 'bm_bulk_save_description', { proposal_ids: [ proposalId ] } )
			.done( function ( res ) {
				if ( res.success ) {
					const r = res.data.results[ 0 ];
					if ( r && r.status === 'saved' ) {
						bmSetActualBadge( $row, r.description, false );
						bmUpdateRowStatus( $row );
						$row.find( '.bm-desc-cb' ).prop( 'disabled', true ).prop( 'checked', false );
						$row.removeClass( 'bm-bulk-desc-row--err' );
						bmDescApplyFilters();
						flashNotice( 'Description copied to Actual.' );
					} else {
						flashNotice( ( r && r.message ) ? r.message : i18n.error, 'error' );
						$row.addClass( 'bm-bulk-desc-row--err' );
					}
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( '→ Copy to Actual' ) );
	} );

	// ── Bulk Description — per-row refresh from WordPress ───────────────────────

	$( document ).on( 'click', '.bm-btn-refresh-single-desc', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $row       = $btn.closest( 'tr' );

		$btn.addClass( 'bm-loading' ).text( '…' );

		post( 'bm_refresh_single_description', { proposal_id: proposalId } )
			.done( function ( res ) {
				if ( res.success ) {
					bmSetActualBadge( $row, res.data.description, res.data.is_manual );
					bmUpdateRowStatus( $row );
					bmDescApplyFilters();
					flashNotice( res.data.is_manual
						? 'Description pulled from WordPress → ✍ Written. Will show as Written in Proposals tab.'
						: 'Description refreshed from WordPress.' );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ).text( '↺' ) );
	} );

	// ── Bulk Description — checkbox → selected keywords textarea ────────────

	function bmUpdateDescSelectedKeywords() {
		const keywords = [];
		$( '#bm-bulk-desc-table .bm-desc-cb:checked' ).each( function () {
			keywords.push( $( this ).data( 'tagName' ) );
		} );
		const $wrap = $( '#bm-desc-selected-wrap' );
		const $ta   = $( '#bm-desc-selected-keywords' );
		$ta.val( keywords.join( ', ' ) );
		if ( keywords.length ) {
			$wrap.slideDown( 150 );
		} else {
			$wrap.slideUp( 150 );
		}
	}

	$( document ).on( 'change', '#bm-bulk-desc-table .bm-desc-cb', bmUpdateDescSelectedKeywords );

	// Also update when "Select All" is toggled (prop() doesn't fire change on children)
	$( document ).on( 'change', '#bm-desc-select-all', function () {
		setTimeout( bmUpdateDescSelectedKeywords, 0 );
	} );

	// ── Proposals — WP-style page jump (Enter on current-page input) ─────────

	$( document ).on( 'keydown', '.bm-page-jump', function ( e ) {
		if ( e.key !== 'Enter' ) return;
		e.preventDefault();
		const $input   = $( this );
		const page     = parseInt( $input.val(), 10 );
		const total    = parseInt( $input.data( 'totalPages' ), 10 );
		const template = $input.data( 'urlTemplate' );
		if ( isNaN( page ) || page < 1 || page > total ) {
			$input.addClass( 'bm-page-invalid' );
			setTimeout( () => $input.removeClass( 'bm-page-invalid' ), 800 );
			return;
		}
		window.location.href = template.replace( 'BM_PAGE', String( page ) );
	} );

	// ── Edit Original term (ORIGINAL column — Name + Slug) ───────────────────

	$( document ).on( 'click', '.bm-btn-edit-original', function () {
		const $btn  = $( this );
		const $card = $btn.closest( '.bm-card' );
		$card.find( '.bm-original-val' ).hide();
		$card.find( '.bm-original-input' ).show();
		$card.find( '.bm-btn-edit-original' ).hide();
		$card.find( '.bm-btn-save-original, .bm-btn-cancel-original' ).show();
	} );

	$( document ).on( 'click', '.bm-btn-cancel-original', function () {
		const $card = $( this ).closest( '.bm-card' );
		$card.find( '.bm-original-input' ).each( function () {
			$( this ).val( $( this ).data( 'original' ) ).hide();
		} );
		$card.find( '.bm-original-val' ).show();
		$card.find( '.bm-btn-save-original, .bm-btn-cancel-original' ).hide();
		$card.find( '.bm-btn-edit-original' ).show();
	} );

	$( document ).on( 'click', '.bm-btn-save-original', function () {
		const $btn   = $( this );
		const termId = $btn.data( 'term-id' );
		const $card  = $btn.closest( '.bm-card' );

		const originalName = $card.find( '.bm-original-input--name' ).val().trim();
		const originalSlug = $card.find( '.bm-original-input--slug' ).val().trim();

		if ( ! originalName ) {
			flashNotice( 'Name cannot be empty.', 'error' );
			return;
		}

		$btn.addClass( 'bm-loading' );

		post( 'bm_update_original_term', {
			term_id:       termId,
			original_name: originalName,
			original_slug: originalSlug,
		} )
			.done( function ( res ) {
				if ( res.success ) {
					const f = res.data;
					$card.find( '.bm-original-val:not(.bm-original-val--slug)' )
						.text( f.original_name );
					$card.find( '.bm-original-val--slug' )
						.html( `<code>${ escHtml( f.original_slug ) }</code>` );
					$card.find( '.bm-card__title' ).text( f.original_name );
					$card.find( '.bm-original-input--name' )
						.attr( 'data-original', f.original_name );
					$card.find( '.bm-original-input--slug' )
						.attr( 'data-original', f.original_slug );
					$card.find( '.bm-original-val' ).show();
					$card.find( '.bm-original-input' ).hide();
					$card.find( '.bm-btn-save-original, .bm-btn-cancel-original' ).hide();
					$card.find( '.bm-btn-edit-original' ).show();
					flashNotice( 'Original term updated.' );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ) );
	} );

	// ── Edit Breadcrumb (PROPOSED column — Breadcrumb row) ────────────────────

	$( document ).on( 'click', '.bm-btn-edit-breadcrumb', function () {
		const $btn = $( this );
		const $td  = $btn.closest( 'td' );
		$td.find( '.bm-breadcrumb-preview' ).hide();
		$td.find( '.bm-breadcrumb-edit-form' ).slideDown( 150 );
		$btn.hide();
	} );

	$( document ).on( 'click', '.bm-btn-cancel-breadcrumb', function () {
		const $td = $( this ).closest( 'td' );
		$td.find( '.bm-breadcrumb-edit-form' ).slideUp( 150 );
		$td.find( '.bm-breadcrumb-preview' ).show();
		$td.find( '.bm-btn-edit-breadcrumb' ).show();
	} );

	$( document ).on( 'click', '.bm-btn-save-breadcrumb', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $form      = $btn.closest( '.bm-breadcrumb-edit-form' );
		const $td        = $btn.closest( 'td' );

		const crumbs = [];
		$form.find( '.bm-crumb-input' ).each( function () {
			const val = $( this ).val().trim();
			if ( val ) crumbs.push( val );
		} );

		if ( ! crumbs.length ) {
			flashNotice( 'Breadcrumb cannot be empty.', 'error' );
			return;
		}

		$btn.addClass( 'bm-loading' );

		post( 'bm_update_breadcrumb', { proposal_id: proposalId, crumbs: crumbs } )
			.done( function ( res ) {
				if ( res.success ) {
					const sep  = ' <span class="bm-sep">›</span> ';
					const html = res.data.crumbs.map( c => escHtml( c ) ).join( sep );
					$td.find( '.bm-breadcrumb-preview' ).html( html ).show();
					$form.slideUp( 150 );
					$td.find( '.bm-btn-edit-breadcrumb' ).show();
					flashNotice( 'Breadcrumb updated.' );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ) );
	} );

	// ── Proposals — Actual Desc cell helper ─────────────────────────────────

	function bmUpdateActualDescCell( $card, proposedDesc, wikidataDesc ) {
		const $cell = $card.find( '.bm-actual-desc-cell' );
		if ( ! $cell.length ) return;

		let descSource;
		if ( proposedDesc !== '' && ( wikidataDesc === '' || proposedDesc !== wikidataDesc ) ) {
			descSource = 'manual';
		} else if ( proposedDesc !== '' ) {
			descSource = 'wikidata';
		} else {
			descSource = 'empty';
		}

		$cell.attr( 'data-proposed-desc', proposedDesc )
		     .attr( 'data-wikidata-desc', wikidataDesc );

		$cell.find( '.bm-desc-actual-badge' ).remove();
		if ( descSource === 'manual' ) {
			$cell.prepend( '<span class="bm-desc-actual-badge bm-desc-actual-badge--manual">✍ Written</span>' );
		} else if ( descSource === 'wikidata' ) {
			$cell.prepend( '<span class="bm-desc-actual-badge bm-desc-actual-badge--wikidata">Wikidata</span>' );
		}

		const $text = $cell.find( '.bm-actual-desc-text' );
		if ( proposedDesc !== '' ) {
			$text.text( proposedDesc );
		} else {
			$text.html( '<em class="bm-no-data">Empty</em>' );
		}
	}

	// ── Proposals — Clear Wikidata fields ────────────────────────────────────

	$( document ).on( 'click', '.bm-btn-clear-wikidata', function () {
		const $btn       = $( this );
		const proposalId = $btn.data( 'proposal-id' );
		const $form      = $btn.closest( '.bm-edit-form' );
		const $card      = $form.closest( '.bm-card' );

		if ( ! window.confirm( 'Clear Wikidata ID, label and WD description?\nActual Description will not be affected.' ) ) return;

		$btn.addClass( 'bm-loading' );

		post( 'bm_clear_wikidata_fields', { proposal_id: proposalId } )
			.done( function ( res ) {
				if ( res.success ) {
					// Clear form inputs
					$form.find( '[name="wikidata_id"]' ).val( '' );
					$form.find( '[name="wikidata_label"]' ).val( '' );

					// Update Wikidata ID cell
					$card.find( '.bm-col--proposed .bm-data-table th' )
						.filter( function () { return $( this ).text().trim() === 'Wikidata ID'; } )
						.siblings( 'td' ).first().text( '—' );

					// Update Label cell
					$card.find( '.bm-col--proposed .bm-data-table th' )
						.filter( function () { return $( this ).text().trim() === 'Label'; } )
						.siblings( 'td' ).first().text( '—' );

					// Update WD Desc cell
					$card.find( '.bm-wikidata-desc-cell' ).text( '—' );

					// Update Actual Desc badge — wikidata now empty so proposed becomes Written
					bmUpdateActualDescCell( $card, res.data.proposed_description ?? '', '' );

					flashNotice( 'Wikidata fields cleared. Actual Description preserved as ✍ Written.' );
				} else {
					flashNotice( res.data?.message ?? i18n.error, 'error' );
				}
			} )
			.fail( () => flashNotice( i18n.error, 'error' ) )
			.always( () => $btn.removeClass( 'bm-loading' ) );
	} );

	// ── Proposals — Tags by Status browser ───────────────────────────────────

	let bmStatusTagCurrentState = null;

	$( document ).on( 'click keydown', '.bm-stat[data-state]', function ( e ) {
		if ( e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ' ) return;
		e.preventDefault();

		const $btn   = $( this );
		const state  = $btn.data( 'state' );
		const $panel = $( '#bm-status-tag-browser' );
		const $ta    = $( '#bm-status-tag-textarea' );

		// Toggle off if same badge clicked again while panel is open
		if ( bmStatusTagCurrentState === state && $panel.is( ':visible' ) ) {
			$panel.slideUp( 200 );
			bmStatusTagCurrentState = null;
			return;
		}

		bmStatusTagCurrentState = state;

		// Set label badge text + colour class
		const labelText = $btn.text().trim().replace( /^\d+\s*/, '' );
		$( '#bm-status-tag-label' )
			.text( labelText )
			.attr( 'class', 'bm-badge bm-badge--' + state );
		$( '#bm-status-tag-count-wrap' ).hide();

		$ta.val( '' ).attr( 'placeholder', 'Loading…' );
		$panel.slideDown( 200 );

		post( 'bm_get_tags_by_status', { state } )
			.done( function ( res ) {
				if ( res.success ) {
					$ta.val( res.data.tags ).attr( 'placeholder', '' );
					$( '#bm-status-tag-count' ).text( res.data.count );
					$( '#bm-status-tag-count-wrap' ).show();
				} else {
					$ta.val( '' ).attr( 'placeholder', res.data?.message ?? i18n.error );
				}
			} )
			.fail( function () {
				$ta.val( '' ).attr( 'placeholder', i18n.error );
			} );
	} );

	$( document ).on( 'click', '#bm-status-tag-close', function () {
		$( '#bm-status-tag-browser' ).slideUp( 200 );
		bmStatusTagCurrentState = null;
	} );

	$( document ).on( 'click', '#bm-status-tag-copy', function () {
		const text = $( '#bm-status-tag-textarea' ).val();
		if ( ! text ) {
			flashNotice( 'Nothing to copy.', 'error' );
			return;
		}
		if ( navigator.clipboard && navigator.clipboard.writeText ) {
			navigator.clipboard.writeText( text )
				.then( function () { flashNotice( 'Copied to clipboard.' ); } )
				.catch( function () { flashNotice( 'Copy failed — select text manually.', 'warning' ); } );
		} else {
			$( '#bm-status-tag-textarea' )[0].select();
			document.execCommand( 'copy' );
			flashNotice( 'Copied to clipboard.' );
		}
	} );

	$( document ).on( 'click', '#bm-status-tag-send', function () {
		const text = $( '#bm-status-tag-textarea' ).val();
		if ( ! text ) {
			flashNotice( 'Nothing to send.', 'error' );
			return;
		}
		const $target = $( '#bm-proposals-bulk-keywords' );
		$target.val( text );
		$target[0].scrollIntoView( { behavior: 'smooth', block: 'center' } );
		$target.addClass( 'bm-field-filled' );
		setTimeout( function () { $target.removeClass( 'bm-field-filled' ); }, 1500 );
		flashNotice( 'Tags sent to Bulk Search — click Filter to search.' );
	} );

	// ── Help — Wikidata tab — accordion ──────────────────────────────────────

	$( document ).on( 'click', '.bm-help-article-toggle', function () {
		const $btn     = $( this );
		const $article = $btn.closest( '.bm-help-article' );
		const $body    = $article.find( '.bm-help-article-body' );
		const expanded = $btn.attr( 'aria-expanded' ) === 'true';

		$btn.attr( 'aria-expanded', ! expanded );
		$article.toggleClass( 'is-collapsed', expanded );
		if ( expanded ) {
			$body.slideUp( 180 );
		} else {
			$body.slideDown( 180 );
		}
	} );

} )( jQuery );
