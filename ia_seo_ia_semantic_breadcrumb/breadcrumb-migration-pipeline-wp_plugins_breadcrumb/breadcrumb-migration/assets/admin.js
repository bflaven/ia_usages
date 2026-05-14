/* Breadcrumb Migration — Admin JS */
/* global bmData, jQuery */

( function ( $ ) {
	'use strict';

	const { ajaxUrl, nonce, i18n } = bmData;

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


	// ── Delta — New Tags ──────────────────────────────────────────────────────

	function escHtml( str ) {
		return String( str )
			.replace( /&/g,  '&amp;' )
			.replace( /</g,  '&lt;' )
			.replace( />/g,  '&gt;' )
			.replace( /"/g,  '&quot;' );
	}

	function renderDeltaRow( tag ) {
		const entities = [
			'', 'PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT',
			'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT',
			'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL',
		];
		const opts = entities
			.map( e => `<option value="${e}">${ e || '— none —' }</option>` )
			.join( '' );
		const extUrl = 'https://www.wikidata.org/w/index.php?search=' +
			encodeURIComponent( tag.name ) + '&language=' + encodeURIComponent( bmData.wikidataLang || 'en' );

		return `
			<div class="bm-delta-row" data-wp-term-id="${escHtml( tag.wp_term_id )}">
				<div class="bm-delta-header">
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
		const $btn     = $( this );
		const $results = $( '#bm-delta-results' );

		$btn.addClass( 'bm-loading' ).text( 'Scanning…' );
		$results.empty();

		post( 'bm_scan_delta', {} )
			.done( function ( res ) {
				if ( res.success ) {
					const { tags, count } = res.data;
					if ( count === 0 ) {
						$results.html( '<p class="bm-delta-none">No new tags found — all post_tag terms are already tracked.</p>' );
					} else {
						$results.html(
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

} )( jQuery );
