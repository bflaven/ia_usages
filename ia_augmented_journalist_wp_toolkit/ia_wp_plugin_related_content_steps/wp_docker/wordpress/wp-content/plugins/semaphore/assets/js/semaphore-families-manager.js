/**
 * Plugin Name: Semaphore
 * Description: Semantic clustering plugin (related posts, tag families, sidebar, breadcrumbs & schemas).
 * Version: 1.2.2
 * Author: Bruno Flaven & IA
 * Text Domain: semaphore
 */

jQuery(function ($) {
    'use strict';

    if (typeof semaphoreDashboard === 'undefined') {
        console.error('semaphoreDashboard is not defined – check wp_localize_script.');
        return;
    }

    var state = {
        selectedTagId: null,
        selectedFamilyId: null,
        selectedMemberTagId: null,
        tagsPaged: 1,
        tagsPerPage: 50,
        tagsSearch: '',
        familiesSearch: '',
        families: []
    };

    var $tagsTable    = $('#semaphore-all-tags-table');
    var $familiesList = $('#semaphore-families-list');
    var $membersList  = $('#semaphore-family-members');

    var $btnConvert = $('#semaphore-convert-to-family');
    var $btnAttach  = $('#semaphore-attach-to-family');
    var $btnDetach  = $('#semaphore-detach-from-family');

    var $inputTagSearch    = $('#semaphore-tag-search');
    var $inputFamilySearch = $('#semaphore-family-search');

    function escapeHtml(str) {
        if (str == null) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function ajaxError(jqXHR, textStatus, errorThrown) {
        alert('Network error: ' + (errorThrown || textStatus));
        console.error('Semaphore dashboard error:', jqXHR, textStatus, errorThrown);
    }

    function updateButtons() {
        $btnConvert.prop('disabled', !state.selectedTagId);
        $btnAttach.prop('disabled', !(state.selectedTagId && state.selectedFamilyId));
        $btnDetach.prop('disabled', !(state.selectedFamilyId && state.selectedMemberTagId));
    }

    /* Tags list */

    function renderTags(data) {
        var rows    = data.rows || [];
        var total   = data.total || 0;
        var perPage = data.per_page || state.tagsPerPage;
        var paged   = data.paged || state.tagsPaged;
        var maxPage = Math.max(1, Math.ceil(total / perPage));

        var html = '<table class="widefat fixed striped"><thead><tr>' +
            '<th style="width:70px;">ID</th>' +
            '<th>Tag</th>' +
            '<th style="width:80px;">Posts</th>' +
            '</tr></thead><tbody>';

        if (!rows.length) {
            html += '<tr><td colspan="3"><em>No tags found.</em></td></tr>';
        } else {
            rows.forEach(function (r) {
                var active = (r.term_id === state.selectedTagId) ? ' active' : '';
                html += '<tr class="semaphore-tag-row' + active + '" data-id="' + r.term_id + '">' +
                    '<td>#' + r.term_id + '</td>' +
                    '<td>' + escapeHtml(r.name) + '</td>' +
                    '<td>' + (r.count || 0) + '</td>' +
                    '</tr>';
            });
        }

        html += '</tbody></table>';

        html += '<div class="tablenav"><div class="tablenav-pages">' +
            '<span class="displaying-num">' + total + ' items</span> ';

        if (maxPage > 1) {
            var prevDisabled = (paged <= 1) ? ' disabled' : '';
            var nextDisabled = (paged >= maxPage) ? ' disabled' : '';
            html += '<span class="pagination-links">' +
                '<a href="#" class="first-page' + prevDisabled + '" data-page="1">«</a>' +
                '<a href="#" class="prev-page' + prevDisabled + '" data-page="' + (paged - 1) + '">‹</a>' +
                '<span class="paging-input">' + paged + ' of <span class="total-pages">' + maxPage + '</span></span>' +
                '<a href="#" class="next-page' + nextDisabled + '" data-page="' + (paged + 1) + '">›</a>' +
                '<a href="#" class="last-page' + nextDisabled + '" data-page="' + maxPage + '">»</a>' +
                '</span>';
        }

        html += '</div></div>';
        $tagsTable.html(html);
    }

    function loadTags() {
        $.ajax({
            url: semaphoreDashboard.ajax_url,
            data: {
                action:   'semaphore_list_tags',
                nonce:    semaphoreDashboard.nonce,
                paged:    state.tagsPaged,
                per_page: state.tagsPerPage,
                search:   state.tagsSearch
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error loading tags.');
                return;
            }
            renderTags(res.data || {});
        }).fail(ajaxError);
    }

    /* Families */

    function renderFamilies() {
        var list = state.families || [];

        if (state.familiesSearch) {
            var q = state.familiesSearch.toLowerCase();
            list = list.filter(function (f) {
                var idMatch  = String(f.family_id).indexOf(q) !== -1;
                var lblMatch = (f.canonical_label || '').toLowerCase().indexOf(q) !== -1;
                return idMatch || lblMatch;
            });
        }

        var html = '<table class="widefat fixed striped"><thead><tr>' +
            '<th style="width:70px;">Family ID</th>' +
            '<th>Canonical label</th>' +
            '<th style="width:80px;">Members</th>' +
            '</tr></thead><tbody>';

        if (!list.length) {
            html += '<tr><td colspan="3"><em>No families found.</em></td></tr>';
        } else {
            list.forEach(function (f) {
                var active = (f.family_id === state.selectedFamilyId) ? ' active' : '';
                html += '<tr class="semaphore-family-row' + active + '" data-family-id="' + f.family_id + '">' +
                    '<td>#' + f.family_id + '</td>' +
                    '<td>' + escapeHtml(f.canonical_label || '') + '</td>' +
                    '<td>' + (f.members || 0) + '</td>' +
                    '</tr>';
            });
        }

        html += '</tbody></table>';
        $familiesList.html(html);
    }

    function loadFamilies(keepSelection) {
        $.ajax({
            url: semaphoreDashboard.ajax_url,
            data: {
                action: 'semaphore_list_families',
                nonce:  semaphoreDashboard.nonce
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error loading families.');
                return;
            }
            state.families = (res.data && res.data.families) || [];
            if (!keepSelection) {
                state.selectedFamilyId    = null;
                state.selectedMemberTagId = null;
            }
            renderFamilies();
            if (state.selectedFamilyId) {
                loadMembers();
            } else {
                renderMembers([]);
            }
        }).fail(ajaxError);
    }

    /* Members */

    function renderMembers(list) {
        list = list || [];
        state.selectedMemberTagId = null;

        var html = '<table class="widefat fixed striped"><thead><tr>' +
            '<th style="width:70px;">Tag ID</th>' +
            '<th>Tag label</th>' +
            '<th style="width:80px;">Usage</th>' +
            '</tr></thead><tbody>';

        if (!list.length) {
            html += '<tr><td colspan="3"><em>No members in this family.</em></td></tr>';
        } else {
            list.forEach(function (m) {
                var active = (m.tag_id === state.selectedMemberTagId) ? ' active' : '';
                html += '<tr class="semaphore-member-row' + active + '" data-tag-id="' + m.tag_id + '">' +
                    '<td>#' + m.tag_id + '</td>' +
                    '<td>' + escapeHtml(m.tag_label || '') + '</td>' +
                    '<td>' + (m.usage_count || 0) + '</td>' +
                    '</tr>';
            });
        }

        html += '</tbody></table>';
        $membersList.html(html);
        updateButtons();
    }

    function loadMembers() {
        if (!state.selectedFamilyId) {
            renderMembers([]);
            return;
        }

        $.ajax({
            url: semaphoreDashboard.ajax_url,
            data: {
                action:    'semaphore_list_family_members',
                nonce:     semaphoreDashboard.nonce,
                family_id: state.selectedFamilyId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error loading members.');
                return;
            }
            renderMembers((res.data && res.data.members) || []);
        }).fail(ajaxError);
    }

    /* Selection handlers */

    $tagsTable.on('click', '.semaphore-tag-row', function () {
        var id = parseInt($(this).data('id'), 10) || 0;
        if (state.selectedTagId === id) {
            state.selectedTagId = null;
            $tagsTable.find('.semaphore-tag-row').removeClass('active');
        } else {
            state.selectedTagId = id;
            $tagsTable.find('.semaphore-tag-row').removeClass('active');
            $(this).addClass('active');
        }
        updateButtons();
    });

    $familiesList.on('click', '.semaphore-family-row', function () {
        var id = parseInt($(this).data('family-id'), 10) || 0;
        if (state.selectedFamilyId === id) {
            state.selectedFamilyId = null;
            $familiesList.find('.semaphore-family-row').removeClass('active');
            renderMembers([]);
        } else {
            state.selectedFamilyId = id;
            $familiesList.find('.semaphore-family-row').removeClass('active');
            $(this).addClass('active');
            loadMembers();
        }
        updateButtons();
    });

    $membersList.on('click', '.semaphore-member-row', function () {
        var id = parseInt($(this).data('tag-id'), 10) || 0;
        if (state.selectedMemberTagId === id) {
            state.selectedMemberTagId = null;
            $membersList.find('.semaphore-member-row').removeClass('active');
        } else {
            state.selectedMemberTagId = id;
            $membersList.find('.semaphore-member-row').removeClass('active');
            $(this).addClass('active');
        }
        updateButtons();
    });

    $tagsTable.on('click', '.tablenav-pages a', function (e) {
        e.preventDefault();
        var $a = $(this);
        if ($a.hasClass('disabled')) return;
        var page = parseInt($a.data('page'), 10) || 1;
        state.tagsPaged = page;
        loadTags();
    });

    /* Search fields */

    var tagTimer = null;
    $inputTagSearch.on('keyup', function () {
        state.tagsSearch = $(this).val();
        state.tagsPaged  = 1;
        if (tagTimer) clearTimeout(tagTimer);
        tagTimer = setTimeout(loadTags, 250);
    });

    var famTimer = null;
    $inputFamilySearch.on('keyup', function () {
        state.familiesSearch = $(this).val();
        if (famTimer) clearTimeout(famTimer);
        famTimer = setTimeout(renderFamilies, 150);
    });

    /* Actions */

    $btnConvert.on('click', function (e) {
        e.preventDefault();
        if (!state.selectedTagId) return;

        if (!window.confirm('Convert this tag into a family (canonical) in the overlay table?')) return;

        $.ajax({
            type: 'POST',
            url:  semaphoreDashboard.ajax_url,
            data: {
                action: 'semaphore_convert_to_family',
                nonce:  semaphoreDashboard.nonce,
                tag_id: state.selectedTagId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error converting tag to family.');
                return;
            }
            loadFamilies(true);
        }).fail(ajaxError);
    });

    $btnAttach.on('click', function (e) {
        e.preventDefault();
        if (!state.selectedTagId || !state.selectedFamilyId) return;

        $.ajax({
            type: 'POST',
            url:  semaphoreDashboard.ajax_url,
            data: {
                action:    'semaphore_attach_to_family',
                nonce:     semaphoreDashboard.nonce,
                family_id: state.selectedFamilyId,
                tag_id:    state.selectedTagId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error attaching tag to family.');
                return;
            }
            loadMembers();
            loadFamilies(true);
        }).fail(ajaxError);
    });

    $btnDetach.on('click', function (e) {
        e.preventDefault();
        if (!state.selectedFamilyId || !state.selectedMemberTagId) return;

        if (!window.confirm('Detach this tag from the current family in the overlay table?')) return;

        $.ajax({
            type: 'POST',
            url:  semaphoreDashboard.ajax_url,
            data: {
                action:    'semaphore_detach_from_family',
                nonce:     semaphoreDashboard.nonce,
                family_id: state.selectedFamilyId,
                tag_id:    state.selectedMemberTagId
            },
            dataType: 'json'
        }).done(function (res) {
            if (!res || !res.success) {
                alert((res && res.data && res.data.message) || 'Error detaching tag from family.');
                return;
            }
            loadMembers();
            loadFamilies(true);
        }).fail(ajaxError);
    });

    /* Help panel toggle (duplicate of inline PHP helper, but harmless if both exist) */
    var $helpToggle = jQuery('.semaphore-help-toggle');
    var $helpPanel  = jQuery('#semaphore-help-panel');

    $helpToggle.on('click', function () {
        var expanded = $helpToggle.attr('aria-expanded') === 'true';
        expanded = !expanded;
        $helpToggle.attr('aria-expanded', expanded ? 'true' : 'false');
        $helpToggle.text(expanded ? 'Hide help' : 'Show help');

        if (expanded) {
            $helpPanel.removeAttr('hidden');
        } else {
            $helpPanel.attr('hidden', 'hidden');
        }
    });

    /* Init */

    updateButtons();
    loadTags();
    loadFamilies(false);
});
