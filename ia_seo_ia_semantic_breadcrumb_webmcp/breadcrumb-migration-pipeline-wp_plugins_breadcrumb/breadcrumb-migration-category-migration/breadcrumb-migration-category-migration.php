<?php
/*
Plugin Name: Breadcrumb Category Migration
Description: Related to the plugin Breadcrumb Migration. Progressive category migration tool with drag & drop reassignment and redirect snippet generation. Do not forget to add the IDs for each new category and change the .htaccess
Version: 1.2.0
Author: Bruno Flaven + Claude Code
*/

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class BF_Breadcrumb_Category_Migration {

    const MENU_SLUG    = 'breadcrumb-migration-category-migration';
    const NONCE_ACTION = 'bf_bcm_nonce_action';
    const NONCE_NAME   = 'bf_bcm_nonce';

    public function __construct() {
        add_action( 'admin_menu', array( $this, 'add_admin_menu' ) );
        add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_assets' ) );

        add_action( 'wp_ajax_bf_bcm_get_source_categories',            array( $this, 'ajax_get_source_categories' ) );
        add_action( 'wp_ajax_bf_bcm_get_target_categories',            array( $this, 'ajax_get_target_categories' ) );
        add_action( 'wp_ajax_bf_bcm_get_posts_by_category',            array( $this, 'ajax_get_posts_by_category' ) );
        add_action( 'wp_ajax_bf_bcm_bulk_add_post_category',           array( $this, 'ajax_bulk_add_post_category' ) );
        add_action( 'wp_ajax_bf_bcm_delete_category_and_get_redirect', array( $this, 'ajax_delete_category_and_get_redirect' ) );
    }

    public function add_admin_menu() {
        add_submenu_page(
            'tools.php',
            __( 'Breadcrumb Category Migration', 'bf-bcm' ),
            __( 'Breadcrumb Migration', 'bf-bcm' ),
            'manage_options',
            self::MENU_SLUG,
            array( $this, 'render_admin_page' )
        );
    }

    public function enqueue_assets( $hook ) {
        if ( 'tools_page_' . self::MENU_SLUG !== $hook ) {
            return;
        }

        /* ── Inline CSS ──────────────────────────────────── */
        $css = '
        .bf-bcm-wrap { display: flex; gap: 20px; }
        .bf-bcm-column { flex: 1; min-width: 0; }
        .bf-bcm-panel { background: #fff; border: 1px solid #ccd0d4; padding: 10px; max-height: 70vh; overflow-y: auto; }
        .bf-bcm-panel h2 { margin-top: 0; }
        .bf-bcm-category-list { list-style: none; margin: 0; padding: 0; }
        .bf-bcm-category-list li { padding: 6px 8px; border-bottom: 1px solid #eee; cursor: pointer; display: flex; justify-content: space-between; align-items: flex-start; }
        .bf-bcm-category-list li.bf-bcm-active { background: #f0f6ff; }
        .bf-bcm-category-name { font-weight: 600; }
        .bf-bcm-category-slug { font-size: 10px; color: #888; display: block; margin-top: 2px; font-style: italic; }
        .bf-bcm-category-count { font-size: 11px; color: #666; margin-left: 10px; white-space: nowrap; flex-shrink: 0; }
        .bf-bcm-category-empty { color: #999; font-style: italic; }
        .bf-bcm-select-toolbar { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; padding: 4px 0; border-bottom: 1px solid #eee; }
        .bf-bcm-post-list { list-style: none; margin: 0; padding: 0; }
        .bf-bcm-post-item { padding: 6px 8px; border-bottom: 1px solid #eee; background: #fafafa; cursor: move; display: flex; align-items: flex-start; gap: 8px; border-left: 3px solid transparent; }
        .bf-bcm-post-item.bf-bcm-selected { background: #e8f4fd; border-left-color: #2271b1; }
        .bf-bcm-post-item.dragging { opacity: 0.5; }
        .bf-bcm-post-checkbox { margin-top: 3px; flex-shrink: 0; cursor: pointer; }
        .bf-bcm-post-content { flex: 1; min-width: 0; }
        @keyframes bf-bcm-flash-post { 0% { background: #d4edda; border-left-color: #28a745; } 100% { background: #fafafa; border-left-color: transparent; } }
        .bf-bcm-post-item.bf-bcm-flash-success { animation: bf-bcm-flash-post 0.9s ease-out forwards; }
        .bf-bcm-target-category { padding: 6px 10px; border: 1px dashed #ccc; margin-bottom: 5px; background: #f9f9f9; display: flex; justify-content: space-between; align-items: center; min-height: 36px; }
        .bf-bcm-target-category.bf-bcm-drop-over { border-color: #2271b1; background: #e9f5ff; }
        @keyframes bf-bcm-flash-target { 0% { background: #d4edda; border-color: #28a745; } 100% { background: #f9f9f9; border-color: #ccc; } }
        .bf-bcm-target-category.bf-bcm-flash-success { animation: bf-bcm-flash-target 0.9s ease-out forwards; }
        .bf-bcm-target-cat-name { font-weight: 600; }
        .bf-bcm-target-count { font-size: 11px; color: #666; margin-left: 8px; }
        .bf-bcm-delete-btn { margin-left: 8px; font-size: 11px; }
        .bf-bcm-redirect-snippet { margin-top: 10px; font-family: monospace; white-space: pre; background: #f5f5f5; padding: 8px; border: 1px solid #ddd; }
        .bf-bcm-feedback { margin: 0 0 10px; padding: 6px 10px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 3px; color: #155724; font-size: 13px; display: none; }
        .bf-bcm-feedback.bf-bcm-visible { display: block; }
        .bf-bcm-red-processed .bf-bcm-category-name { color: #999; text-decoration: line-through; }
        .bf-bcm-red-processed .bf-bcm-category-slug { color: #bbb; }
        .bf-bcm-red-preview-box { font-family: monospace; white-space: pre-wrap; word-break: break-all; background: #f0f0f0; padding: 10px; border: 1px solid #ccc; border-radius: 3px; font-size: 13px; min-height: 44px; color: #23282d; margin-bottom: 10px; }
        .bf-bcm-red-preview-box.has-value { background: #fff8e1; border-color: #f6c342; }
        .bf-bcm-red-btn-row { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; align-items: center; }
        .bf-bcm-red-textarea { width: 100%; min-height: 140px; font-family: monospace; font-size: 12px; padding: 8px; border: 1px solid #ccd0d4; background: #f9f9f9; resize: vertical; box-sizing: border-box; }
        .bf-bcm-red-sep { border: none; border-top: 1px solid #eee; margin: 12px 0; }
        ';
        wp_add_inline_style( 'wp-admin', $css );

        /* ── JS: register as dedicated footer script ─────── */
        wp_register_script( 'bf-bcm-admin', false, array( 'jquery' ), '1.2.0', true );
        wp_enqueue_script( 'bf-bcm-admin' );

        wp_localize_script( 'bf-bcm-admin', 'bfBcmConfig', array(
            'ajaxUrl' => admin_url( 'admin-ajax.php' ),
            'nonce'   => wp_create_nonce( self::NONCE_ACTION ),
        ) );

        $js = <<<'JSCODE'
(function () {
    'use strict';

    var ajaxUrl = bfBcmConfig.ajaxUrl;
    var nonce   = bfBcmConfig.nonce;

    /* ── Shared state ── */
    var reductionInitialized = false;

    /* ── Migration state ── */
    var currentSourceCatId = null;
    var draggedPosts       = [];

    /* ── Reduction state ── */
    var redSelectedSource = null;
    var redSelectedTarget = null;
    var redLines          = [];

    /* ── Utilities ── */
    function qs(sel, ctx)  { return (ctx || document).querySelector(sel); }
    function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

    function ajax(action, data, cb) {
        var params = new URLSearchParams();
        params.append('action', action);
        params.append('_ajax_nonce', nonce);
        if (data) {
            Object.keys(data).forEach(function (key) {
                var val = data[key];
                if (Array.isArray(val)) {
                    val.forEach(function (v) { params.append(key + '[]', v); });
                } else {
                    params.append(key, val);
                }
            });
        }
        fetch(ajaxUrl, {
            method:  'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body:    params.toString()
        }).then(function (res) {
            return res.json();
        }).then(cb).catch(function (err) {
            console.error('BF-BCM AJAX error:', action, err);
            alert('AJAX error: ' + action);
        });
    }

    function showFeedback(msg) {
        var el = qs('#bf-bcm-feedback');
        if (!el) return;
        el.textContent = msg;
        el.classList.add('bf-bcm-visible');
        clearTimeout(el._timer);
        el._timer = setTimeout(function () { el.classList.remove('bf-bcm-visible'); }, 3500);
    }

    function flashEl(el) {
        if (!el) return;
        el.classList.remove('bf-bcm-flash-success');
        void el.offsetWidth;
        el.classList.add('bf-bcm-flash-success');
        setTimeout(function () { el.classList.remove('bf-bcm-flash-success'); }, 950);
    }

    function copyToClipboard(text, btn, label) {
        var restore = function () { setTimeout(function () { btn.textContent = label; }, 1500); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function () {
                btn.textContent = 'Copied!';
                restore();
            }).catch(function () { fallbackCopy(text, btn, restore); });
        } else {
            fallbackCopy(text, btn, restore);
        }
    }

    function fallbackCopy(text, btn, restore) {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.cssText = 'position:fixed;top:-999px;left:-999px;';
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        try { document.execCommand('copy'); btn.textContent = 'Copied!'; } catch (e) { btn.textContent = 'Failed'; }
        document.body.removeChild(ta);
        restore();
    }

    /* ── Tab switching ── */
    function setupTabs() {
        qsa('.bf-bcm-nav-tab').forEach(function (tab) {
            tab.addEventListener('click', function (e) {
                e.preventDefault();
                var target = tab.dataset.tab;
                qsa('.bf-bcm-nav-tab').forEach(function (t) { t.classList.remove('nav-tab-active'); });
                tab.classList.add('nav-tab-active');
                qsa('.bf-bcm-tab-content').forEach(function (c) { c.style.display = 'none'; });
                var content = qs('#bf-bcm-tab-' + target);
                if (content) { content.style.display = ''; }
                if (target === 'reduction' && !reductionInitialized) {
                    reductionInitialized = true;
                    initReduction();
                }
            });
        });
    }

    /* ══════════════════════ MIGRATION TAB ══════════════════════ */

    function loadSourceCategories() {
        ajax('bf_bcm_get_source_categories', {}, function (resp) {
            if (!resp || !resp.success) { console.warn('bf_bcm_get_source_categories failed', resp); return; }
            renderSourceCategories(resp.data);
        });
    }

    function loadTargetCategories() {
        ajax('bf_bcm_get_target_categories', {}, function (resp) {
            if (!resp || !resp.success) { console.warn('bf_bcm_get_target_categories failed', resp); return; }
            renderTargetCategories(resp.data);
        });
    }

    function renderSourceCategories(cats) {
        var container = qs('#bf-bcm-source-cats');
        if (!container) return;
        container.innerHTML = '';
        if (!Array.isArray(cats) || !cats.length) {
            container.innerHTML = '<p>No source categories.</p>';
            return;
        }
        var ul = document.createElement('ul');
        ul.className = 'bf-bcm-category-list';
        cats.forEach(function (cat) {
            var li = document.createElement('li');
            li.dataset.catId = cat.id;
            li.innerHTML = '<span><span class="bf-bcm-category-name">' + cat.name + '</span></span>'
                         + '<span class="bf-bcm-category-count">(' + cat.count + ')</span>';
            li.addEventListener('click', function () {
                qsa('#bf-bcm-source-cats .bf-bcm-category-list li').forEach(function (l) { l.classList.remove('bf-bcm-active'); });
                li.classList.add('bf-bcm-active');
                currentSourceCatId = cat.id;
                loadPostsByCategory(cat.id);
            });
            ul.appendChild(li);
        });
        container.appendChild(ul);
    }

    function renderTargetCategories(cats) {
        var container = qs('#bf-bcm-target-cats');
        if (!container) return;
        container.innerHTML = '';
        if (!Array.isArray(cats) || !cats.length) {
            container.innerHTML = '<p>No target categories defined.</p>';
            return;
        }
        cats.forEach(function (cat) {
            var div       = document.createElement('div');
            var nameSpan  = document.createElement('span');
            var countSpan = document.createElement('span');
            div.className       = 'bf-bcm-target-category';
            div.dataset.catId   = cat.id;
            nameSpan.className  = 'bf-bcm-target-cat-name';
            nameSpan.textContent = cat.name;
            countSpan.className  = 'bf-bcm-target-count';
            countSpan.textContent = '(' + cat.count + ')';
            div.appendChild(nameSpan);
            div.appendChild(countSpan);

            div.addEventListener('dragover',  function (e) { e.preventDefault(); div.classList.add('bf-bcm-drop-over'); });
            div.addEventListener('dragleave', function ()  { div.classList.remove('bf-bcm-drop-over'); });
            div.addEventListener('drop', function (e) {
                e.preventDefault();
                div.classList.remove('bf-bcm-drop-over');
                if (!draggedPosts.length) return;

                var targetCatId   = cat.id;
                var targetCatName = cat.name;
                var count         = draggedPosts.length;
                var msg = count === 1
                    ? 'Add "' + draggedPosts[0].postTitle + '" to "' + targetCatName + '"?'
                    : 'Add ' + count + ' posts to "' + targetCatName + '"?';
                if (!confirm(msg)) return;

                var postIds = draggedPosts.map(function (p) { return p.postId; });
                var postEls = postIds.map(function (id) {
                    return qs('.bf-bcm-post-item[data-post-id="' + id + '"]');
                }).filter(Boolean);

                ajax('bf_bcm_bulk_add_post_category', { post_ids: postIds, target_cat_id: targetCatId }, function (resp) {
                    if (!resp || !resp.success) {
                        alert('Error: ' + (resp && resp.data && resp.data.message ? resp.data.message : 'unknown'));
                        return;
                    }
                    postEls.forEach(function (el) { flashEl(el); });
                    flashEl(div);
                    if (resp.data.target_count !== undefined) {
                        countSpan.textContent = '(' + resp.data.target_count + ')';
                    }
                    qsa('.bf-bcm-post-item.bf-bcm-selected').forEach(function (el) {
                        el.classList.remove('bf-bcm-selected');
                        var cb = el.querySelector('.bf-bcm-post-checkbox');
                        if (cb) cb.checked = false;
                    });
                    updateSelectAllState();
                    showFeedback(resp.data.added.length + ' post(s) added to "' + targetCatName + '".');
                });
            });
            container.appendChild(div);
        });
    }

    function loadPostsByCategory(catId) {
        var container = qs('#bf-bcm-posts');
        if (!container) return;
        container.innerHTML = '<p>Loading...</p>';
        ajax('bf_bcm_get_posts_by_category', { cat_id: catId }, function (resp) {
            if (!resp || !resp.success) {
                container.innerHTML = '<p>Error loading posts.</p>';
                console.warn(resp);
                return;
            }
            renderPosts(resp.data);
        });
    }

    function getSelectedPosts() {
        return qsa('.bf-bcm-post-item.bf-bcm-selected').map(function (el) {
            return { postId: parseInt(el.dataset.postId, 10), postTitle: el.dataset.postTitle };
        });
    }

    function updateSelectAllState() {
        var btn = qs('#bf-bcm-select-all-btn');
        if (!btn) return;
        var total    = qsa('.bf-bcm-post-item').length;
        var selected = qsa('.bf-bcm-post-item.bf-bcm-selected').length;
        if (total === 0)            { btn.textContent = 'Select All';   btn.dataset.state = 'none'; return; }
        if (selected === total)     { btn.textContent = 'Deselect All'; btn.dataset.state = 'all';  }
        else                        { btn.textContent = 'Select All';   btn.dataset.state = 'none'; }
    }

    function renderPosts(posts) {
        var container = qs('#bf-bcm-posts');
        if (!container) return;
        container.innerHTML = '';
        if (!Array.isArray(posts) || !posts.length) {
            container.innerHTML = '<p>No posts in this category.</p>';
            showDeleteButtonForActiveCategory();
            return;
        }

        var toolbar       = document.createElement('div');
        toolbar.className = 'bf-bcm-select-toolbar';

        var selectAllBtn          = document.createElement('button');
        selectAllBtn.id           = 'bf-bcm-select-all-btn';
        selectAllBtn.className    = 'button button-small';
        selectAllBtn.type         = 'button';
        selectAllBtn.textContent  = 'Select All';
        selectAllBtn.dataset.state = 'none';
        selectAllBtn.addEventListener('click', function () {
            var isAll = this.dataset.state === 'all';
            qsa('.bf-bcm-post-item').forEach(function (el) {
                var cb = el.querySelector('.bf-bcm-post-checkbox');
                if (isAll) { el.classList.remove('bf-bcm-selected'); if (cb) cb.checked = false; }
                else       { el.classList.add('bf-bcm-selected');    if (cb) cb.checked = true; }
            });
            updateSelectAllState();
        });

        var countLabel            = document.createElement('span');
        countLabel.style.cssText  = 'font-size:11px;color:#666;';
        countLabel.textContent    = posts.length + ' post(s)';

        toolbar.appendChild(selectAllBtn);
        toolbar.appendChild(countLabel);
        container.appendChild(toolbar);

        var ul = document.createElement('ul');
        ul.className = 'bf-bcm-post-list';

        posts.forEach(function (post) {
            var li = document.createElement('li');
            li.className          = 'bf-bcm-post-item';
            li.dataset.postId     = post.id;
            li.dataset.postTitle  = post.title;
            li.draggable          = true;

            var cb          = document.createElement('input');
            cb.type         = 'checkbox';
            cb.className    = 'bf-bcm-post-checkbox';
            cb.title        = 'Select post';

            var content         = document.createElement('div');
            content.className   = 'bf-bcm-post-content';
            content.innerHTML   = '<strong>' + post.title + '</strong>'
                                + '<br><span style="font-size:11px;color:#666;">ID: ' + post.id + '</span>';

            cb.addEventListener('change', function (e) {
                e.stopPropagation();
                li.classList.toggle('bf-bcm-selected', cb.checked);
                updateSelectAllState();
            });

            li.addEventListener('click', function (e) {
                if (e.target === cb) return;
                cb.checked = !cb.checked;
                li.classList.toggle('bf-bcm-selected', cb.checked);
                updateSelectAllState();
            });

            li.addEventListener('dragstart', function (e) {
                li.classList.add('dragging');
                var isSelected = li.classList.contains('bf-bcm-selected');
                draggedPosts = isSelected ? getSelectedPosts() : [{ postId: post.id, postTitle: post.title }];
                if (draggedPosts.length > 1) {
                    var ghost = document.createElement('div');
                    ghost.textContent = draggedPosts.length + ' posts';
                    ghost.style.cssText = 'position:absolute;top:-999px;background:#2271b1;color:#fff;padding:4px 10px;border-radius:3px;font-size:12px;font-weight:600;';
                    document.body.appendChild(ghost);
                    e.dataTransfer.setDragImage(ghost, 0, 0);
                    setTimeout(function () { if (ghost.parentNode) ghost.parentNode.removeChild(ghost); }, 0);
                }
            });

            li.addEventListener('dragend', function () {
                li.classList.remove('dragging');
                draggedPosts = [];
            });

            li.appendChild(cb);
            li.appendChild(content);
            ul.appendChild(li);
        });

        container.appendChild(ul);
        hideDeleteButtonForActiveCategory();
        updateSelectAllState();
    }

    function showDeleteButtonForActiveCategory() {
        var container = qs('#bf-bcm-delete-empty-cat');
        if (!container) return;
        container.innerHTML = '';
        var activeLi = qs('.bf-bcm-category-list li.bf-bcm-active');
        if (!activeLi) return;
        var catId     = activeLi.dataset.catId;
        var catName   = activeLi.querySelector('.bf-bcm-category-name').textContent;
        var countEl   = activeLi.querySelector('.bf-bcm-category-count');
        var countText = countEl ? countEl.textContent : '';
        if (countText !== '(0)') return;

        var btn = document.createElement('button');
        btn.className    = 'button button-secondary bf-bcm-delete-btn';
        btn.type         = 'button';
        btn.textContent  = 'Delete "' + catName + '" and show redirect snippet';
        btn.addEventListener('click', function () {
            if (!confirm('Delete category "' + catName + '" and get the .htaccess redirect line?')) return;
            var targetSlug = prompt('Target category slug for redirect (without /category/):', '');
            if (targetSlug === null) return;
            ajax('bf_bcm_delete_category_and_get_redirect', { source_cat_id: catId, target_slug: targetSlug }, function (resp) {
                if (!resp || !resp.success) {
                    alert('Error: ' + (resp && resp.message ? resp.message : 'unknown'));
                    return;
                }
                activeLi.classList.add('bf-bcm-category-empty');
                if (countEl) countEl.textContent = '(0)';
                var snippet = qs('#bf-bcm-redirect-snippet');
                if (snippet) snippet.textContent = resp.data.redirect;
            });
        });
        container.appendChild(btn);
    }

    function hideDeleteButtonForActiveCategory() {
        var container = qs('#bf-bcm-delete-empty-cat');
        if (container) container.innerHTML = '';
        var snippet = qs('#bf-bcm-redirect-snippet');
        if (snippet) snippet.textContent = '';
    }

    /* ══════════════════════ REDUCTION TAB ══════════════════════ */

    function initReduction() {
        ajax('bf_bcm_get_source_categories', {}, function (resp) {
            if (!resp || !resp.success) return;
            renderRedCategories(resp.data, qs('#bf-bcm-red-source-cats'), 'source');
        });
        ajax('bf_bcm_get_target_categories', {}, function (resp) {
            if (!resp || !resp.success) return;
            renderRedCategories(resp.data, qs('#bf-bcm-red-target-cats'), 'target');
        });
        setupRedButtons();
    }

    function renderRedCategories(cats, container, type) {
        if (!container) return;
        container.innerHTML = '';
        if (!Array.isArray(cats) || !cats.length) {
            container.innerHTML = '<p>No categories.</p>';
            return;
        }
        var ul = document.createElement('ul');
        ul.className = 'bf-bcm-category-list';
        cats.forEach(function (cat) {
            var li = document.createElement('li');
            li.dataset.catId   = cat.id;
            li.dataset.catSlug = cat.slug;
            li.innerHTML = '<span><span class="bf-bcm-category-name">' + cat.name + '</span>'
                         + '<span class="bf-bcm-category-slug">' + cat.slug + '</span></span>'
                         + '<span class="bf-bcm-category-count">(' + cat.count + ')</span>';
            li.addEventListener('click', function () {
                qsa('.bf-bcm-category-list li', container).forEach(function (l) { l.classList.remove('bf-bcm-active'); });
                li.classList.add('bf-bcm-active');
                if (type === 'source') {
                    redSelectedSource = { id: cat.id, name: cat.name, slug: cat.slug };
                } else {
                    redSelectedTarget = { id: cat.id, name: cat.name, slug: cat.slug };
                }
                updateRedPreview();
            });
            ul.appendChild(li);
        });
        container.appendChild(ul);
    }

    function buildRedLine() {
        if (!redSelectedSource || !redSelectedTarget) return '';
        return 'Redirect 301 /category/' + redSelectedSource.slug + '/ /category/' + redSelectedTarget.slug + '/';
    }

    function updateRedPreview() {
        var preview     = qs('#bf-bcm-red-preview');
        var copyLineBtn = qs('#bf-bcm-red-copy-line-btn');
        var addBtn      = qs('#bf-bcm-red-add-btn');
        if (!preview) return;
        var line = buildRedLine();
        if (!line) {
            var hint = (!redSelectedSource && !redSelectedTarget)
                ? 'Select a source category (left) and a target category (right).'
                : (!redSelectedSource ? 'Now select a source category on the left.' : 'Now select a target category on the right.');
            preview.textContent = hint;
            preview.classList.remove('has-value');
            if (copyLineBtn) copyLineBtn.disabled = true;
            if (addBtn)      addBtn.disabled      = true;
        } else {
            preview.textContent = line;
            preview.classList.add('has-value');
            if (copyLineBtn) copyLineBtn.disabled = false;
            if (addBtn)      addBtn.disabled      = false;
        }
    }

    function setupRedButtons() {
        var copyLineBtn = qs('#bf-bcm-red-copy-line-btn');
        var addBtn      = qs('#bf-bcm-red-add-btn');
        var copyAllBtn  = qs('#bf-bcm-red-copy-all-btn');
        var clearBtn    = qs('#bf-bcm-red-clear-btn');
        var textarea    = qs('#bf-bcm-red-textarea');

        if (copyLineBtn) {
            copyLineBtn.addEventListener('click', function () {
                var line = buildRedLine();
                if (line) copyToClipboard(line, copyLineBtn, 'Copy line');
            });
        }
        if (addBtn) {
            addBtn.addEventListener('click', function () {
                var line = buildRedLine();
                if (!line) return;
                if (redLines.indexOf(line) === -1) {
                    redLines.push(line);
                    if (textarea) textarea.value = redLines.join('\n');
                }
                var srcLi = qs('#bf-bcm-red-source-cats .bf-bcm-category-list li.bf-bcm-active');
                if (srcLi) srcLi.classList.add('bf-bcm-red-processed');
                addBtn.textContent = 'Added!';
                setTimeout(function () { addBtn.textContent = 'Add to list'; }, 1500);
            });
        }
        if (copyAllBtn) {
            copyAllBtn.addEventListener('click', function () {
                if (textarea && textarea.value.trim()) copyToClipboard(textarea.value, copyAllBtn, 'Copy All');
            });
        }
        if (clearBtn) {
            clearBtn.addEventListener('click', function () {
                if (!confirm('Clear all accumulated redirect lines?')) return;
                redLines = [];
                if (textarea) textarea.value = '';
                redSelectedSource = null;
                redSelectedTarget = null;
                qsa('#bf-bcm-red-source-cats .bf-bcm-red-processed').forEach(function (el) { el.classList.remove('bf-bcm-red-processed'); });
                qsa('#bf-bcm-red-source-cats .bf-bcm-active, #bf-bcm-red-target-cats .bf-bcm-active').forEach(function (el) { el.classList.remove('bf-bcm-active'); });
                updateRedPreview();
            });
        }
    }

    /* ── Boot (script loads in footer — DOM is ready) ── */
    setupTabs();
    loadSourceCategories();
    loadTargetCategories();

}());
JSCODE;

        wp_add_inline_script( 'bf-bcm-admin', $js );
    }

    public function render_admin_page() {
        if ( ! current_user_can( 'manage_options' ) ) {
            wp_die( __( 'You do not have sufficient permissions to access this page.', 'bf-bcm' ) );
        }
        ?>
        <div class="wrap">
            <h1><?php esc_html_e( 'Breadcrumb Category Migration', 'bf-bcm' ); ?></h1>

            <nav class="nav-tab-wrapper" style="margin-bottom:20px;">
                <a href="#" class="nav-tab nav-tab-active bf-bcm-nav-tab" data-tab="migration"><?php esc_html_e( 'Migration', 'bf-bcm' ); ?></a>
                <a href="#" class="nav-tab bf-bcm-nav-tab" data-tab="reduction"><?php esc_html_e( 'Reduction', 'bf-bcm' ); ?></a>
            </nav>

            <!-- Tab: Migration -->
            <div id="bf-bcm-tab-migration" class="bf-bcm-tab-content">
                <p><?php esc_html_e( 'Select posts (click row or checkbox) from a source category. Drag one or multiple posts to a target category to add that category to the posts. Source categories are kept — this tool only adds categories, never removes them.', 'bf-bcm' ); ?></p>
                <div id="bf-bcm-feedback" class="bf-bcm-feedback"></div>
                <div class="bf-bcm-wrap">
                    <div class="bf-bcm-column">
                        <div class="bf-bcm-panel">
                            <h2><?php esc_html_e( 'Source Categories', 'bf-bcm' ); ?></h2>
                            <p><?php esc_html_e( 'Click a category to list its posts.', 'bf-bcm' ); ?></p>
                            <div id="bf-bcm-source-cats"><p><?php esc_html_e( 'Loading...', 'bf-bcm' ); ?></p></div>
                        </div>
                    </div>
                    <div class="bf-bcm-column">
                        <div class="bf-bcm-panel">
                            <h2><?php esc_html_e( 'Posts in selected category', 'bf-bcm' ); ?></h2>
                            <p><?php esc_html_e( 'Click rows or checkboxes to select. Drag selection to a target category.', 'bf-bcm' ); ?></p>
                            <div id="bf-bcm-posts"><p><?php esc_html_e( 'Select a source category on the left.', 'bf-bcm' ); ?></p></div>
                            <div id="bf-bcm-delete-empty-cat" style="margin-top:10px;"></div>
                            <div id="bf-bcm-redirect-snippet" class="bf-bcm-redirect-snippet"></div>
                        </div>
                    </div>
                    <div class="bf-bcm-column">
                        <div class="bf-bcm-panel">
                            <h2><?php esc_html_e( 'Target Categories', 'bf-bcm' ); ?></h2>
                            <p><?php esc_html_e( 'Drop posts here to add this category. Source categories are preserved.', 'bf-bcm' ); ?></p>
                            <div id="bf-bcm-target-cats"><p><?php esc_html_e( 'Loading...', 'bf-bcm' ); ?></p></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab: Reduction -->
            <div id="bf-bcm-tab-reduction" class="bf-bcm-tab-content" style="display:none;">
                <p><?php esc_html_e( 'Generate .htaccess Redirect 301 directives by pairing source and target categories. Click a source category (left), then a target category (right) — the directive appears in the centre. Add lines to the list and copy them all at once into your .htaccess file.', 'bf-bcm' ); ?></p>
                <div class="bf-bcm-wrap">
                    <div class="bf-bcm-column">
                        <div class="bf-bcm-panel">
                            <h2><?php esc_html_e( 'Source Categories', 'bf-bcm' ); ?></h2>
                            <p><?php esc_html_e( 'Click the old / legacy category to redirect from.', 'bf-bcm' ); ?></p>
                            <div id="bf-bcm-red-source-cats"><p><?php esc_html_e( 'Loading...', 'bf-bcm' ); ?></p></div>
                        </div>
                    </div>
                    <div class="bf-bcm-column">
                        <div class="bf-bcm-panel">
                            <h2><?php esc_html_e( 'Generated Directive', 'bf-bcm' ); ?></h2>
                            <p><?php esc_html_e( 'Select source + target to preview the redirect line.', 'bf-bcm' ); ?></p>
                            <div id="bf-bcm-red-preview" class="bf-bcm-red-preview-box"><?php esc_html_e( 'Select a source category (left) and a target category (right).', 'bf-bcm' ); ?></div>
                            <div class="bf-bcm-red-btn-row">
                                <button id="bf-bcm-red-copy-line-btn" class="button" type="button" disabled><?php esc_html_e( 'Copy line', 'bf-bcm' ); ?></button>
                                <button id="bf-bcm-red-add-btn" class="button button-primary" type="button" disabled><?php esc_html_e( 'Add to list', 'bf-bcm' ); ?></button>
                            </div>
                            <hr class="bf-bcm-red-sep">
                            <h3 style="margin-top:0;"><?php esc_html_e( 'Accumulated .htaccess directives', 'bf-bcm' ); ?></h3>
                            <textarea id="bf-bcm-red-textarea" class="bf-bcm-red-textarea" placeholder="<?php esc_attr_e( 'Generated redirect lines will appear here...', 'bf-bcm' ); ?>"></textarea>
                            <div class="bf-bcm-red-btn-row" style="margin-top:8px;">
                                <button id="bf-bcm-red-copy-all-btn" class="button" type="button"><?php esc_html_e( 'Copy All', 'bf-bcm' ); ?></button>
                                <button id="bf-bcm-red-clear-btn" class="button button-secondary" type="button"><?php esc_html_e( 'Clear list', 'bf-bcm' ); ?></button>
                            </div>
                        </div>
                    </div>
                    <div class="bf-bcm-column">
                        <div class="bf-bcm-panel">
                            <h2><?php esc_html_e( 'Target Categories', 'bf-bcm' ); ?></h2>
                            <p><?php esc_html_e( 'Click the new pillar category to redirect to.', 'bf-bcm' ); ?></p>
                            <div id="bf-bcm-red-target-cats"><p><?php esc_html_e( 'Loading...', 'bf-bcm' ); ?></p></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <?php
    }

    public function ajax_get_source_categories() {
        $this->check_ajax_permissions();

        $pillar_ids = array(
            // Add pillar IDs here to exclude them from the source list.
        );

        $terms = get_terms( array( 'taxonomy' => 'category', 'hide_empty' => false ) );
        if ( is_wp_error( $terms ) ) {
            wp_send_json_error( array( 'message' => $terms->get_error_message() ) );
        }

        $data = array();
        foreach ( $terms as $term ) {
            if ( in_array( (int) $term->term_id, $pillar_ids, true ) ) continue;
            $data[] = array( 'id' => (int) $term->term_id, 'name' => $term->name, 'slug' => $term->slug, 'count' => (int) $term->count );
        }
        wp_send_json_success( $data );
    }

    public function ajax_get_target_categories() {
        $this->check_ajax_permissions();

        $pillar_ids = array(
            3438,    // AI & Machine Learning
            3439,    // APIs & Integration
            3437,    // Business & Case Studies
            3440,    // Cloud & Infrastructure
            3441,    // Data & Analytics
            3436,    // Digital Storytelling & Webdocs
            3454,    // Journalism & Writing
            3453,    // Miscellaneous / Other
            3442,    // Mobile & Devices
            3443,    // Multimedia & Video
            3444,    // Programming & Databases
            3445,    // SEO & Web Marketing
            3446,    // Social Media & Community
            3447,    // Technology & Trends
            3448,    // Tools & Productivity
            3449,    // Tutorials & How-to
            3450,    // UX & Product Design
            3451,    // Web Design & Front-end
            3435,    // Web Development
            3452,    // WordPress & CMS
            3433,    // 3WDOC - Tutorials
            3434,    // 3WDOC - Projects
            1,       // Miscellaneous / Other
        );

        if ( empty( $pillar_ids ) ) {
            wp_send_json_success( array() );
        }

        $terms = get_terms( array( 'taxonomy' => 'category', 'hide_empty' => false, 'include' => $pillar_ids ) );
        if ( is_wp_error( $terms ) ) {
            wp_send_json_error( array( 'message' => $terms->get_error_message() ) );
        }

        $data = array();
        foreach ( $terms as $term ) {
            $data[] = array( 'id' => (int) $term->term_id, 'name' => $term->name, 'slug' => $term->slug, 'count' => (int) $term->count );
        }
        wp_send_json_success( $data );
    }

    public function ajax_get_posts_by_category() {
        $this->check_ajax_permissions();

        $cat_id = isset( $_POST['cat_id'] ) ? (int) $_POST['cat_id'] : 0;
        if ( ! $cat_id ) {
            wp_send_json_error( array( 'message' => 'Missing cat_id' ) );
        }

        $posts = get_posts( array(
            'post_type'      => 'post',
            'posts_per_page' => -1,
            'fields'         => 'ids',
            'tax_query'      => array( array( 'taxonomy' => 'category', 'field' => 'term_id', 'terms' => $cat_id ) ),
        ) );

        $data = array();
        foreach ( $posts as $post_id ) {
            $data[] = array( 'id' => $post_id, 'title' => get_the_title( $post_id ) );
        }
        wp_send_json_success( $data );
    }

    public function ajax_bulk_add_post_category() {
        $this->check_ajax_permissions();

        $post_ids      = isset( $_POST['post_ids'] ) ? array_map( 'intval', (array) $_POST['post_ids'] ) : array();
        $target_cat_id = isset( $_POST['target_cat_id'] ) ? (int) $_POST['target_cat_id'] : 0;

        if ( empty( $post_ids ) || ! $target_cat_id ) {
            wp_send_json_error( array( 'message' => 'Missing parameters' ) );
        }

        $added = array();
        foreach ( $post_ids as $post_id ) {
            if ( ! $post_id ) continue;
            wp_set_post_terms( $post_id, array( $target_cat_id ), 'category', true );
            $added[] = $post_id;
        }

        $term         = get_term( $target_cat_id, 'category' );
        $target_count = ( $term && ! is_wp_error( $term ) ) ? (int) $term->count : 0;

        wp_send_json_success( array( 'added' => $added, 'target_count' => $target_count ) );
    }

    public function ajax_delete_category_and_get_redirect() {
        $this->check_ajax_permissions();

        $source_cat_id = isset( $_POST['source_cat_id'] ) ? (int) $_POST['source_cat_id'] : 0;
        $target_slug   = isset( $_POST['target_slug'] ) ? sanitize_title( wp_unslash( $_POST['target_slug'] ) ) : '';

        if ( ! $source_cat_id ) {
            wp_send_json_error( array( 'message' => 'Missing source_cat_id' ) );
        }

        $term = get_term( $source_cat_id, 'category' );
        if ( ! $term || is_wp_error( $term ) ) {
            wp_send_json_error( array( 'message' => 'Category not found.' ) );
        }

        $old_slug = $term->slug;
        wp_delete_term( $source_cat_id, 'category' );

        $old_path = '/category/' . $old_slug . '/';
        if ( $target_slug ) {
            $target_slug = trim( $target_slug, "/ \t\n\r\0\x0B" );
            $redirect    = 'Redirect 301 ' . $old_path . ' /category/' . $target_slug . '/';
        } else {
            $redirect = 'Redirect 410 ' . $old_path;
        }
        wp_send_json_success( array( 'redirect' => $redirect ) );
    }

    protected function check_ajax_permissions() {
        if ( ! current_user_can( 'manage_options' ) ) {
            wp_send_json_error( array( 'message' => 'Insufficient permissions.' ) );
        }
        if ( ! isset( $_POST['_ajax_nonce'] ) || ! wp_verify_nonce( $_POST['_ajax_nonce'], self::NONCE_ACTION ) ) {
            wp_send_json_error( array( 'message' => 'Invalid nonce.' ) );
        }
    }
}

new BF_Breadcrumb_Category_Migration();
