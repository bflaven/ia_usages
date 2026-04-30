<?php
/**
 * Admin page — RAG Semantic Search.
 *
 * Three sections:
 *   1. Status    — row counts for both tables.
 *   2. Import    — upload rag_bridge.json, insert/upsert into wp_rag_posts.
 *   3. Danger    — empty both tables.
 */

defined( 'ABSPATH' ) || exit;

if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( esc_html__( 'You do not have permission to access this page.', 'rag-semantic-search' ) );
}

// ── Handle POST actions ───────────────────────────────────────────────────────

$notice       = '';
$notice_class = 'notice-success';

// -- Settings action --
if ( isset( $_POST['rss_action'] ) && $_POST['rss_action'] === 'settings' ) {
    check_admin_referer( 'rss_settings_nonce', 'rss_nonce' );
    $enabled = isset( $_POST['rss_semantic_enabled'] ) ? '1' : '0';
    update_option( 'rss_semantic_enabled', $enabled );
    $notice = $enabled
        ? __( 'Semantic search enabled.', 'rag-semantic-search' )
        : __( 'Semantic search disabled — only standard search is active.', 'rag-semantic-search' );
}

// -- Content action --
if ( isset( $_POST['rss_action'] ) && $_POST['rss_action'] === 'content' ) {
    check_admin_referer( 'rss_content_nonce', 'rss_nonce' );
    update_option( 'rss_promo_text',   wp_kses_post( wp_unslash( $_POST['rss_promo_text']   ?? '' ) ) );
    update_option( 'rss_lang_notice',  wp_kses_post( wp_unslash( $_POST['rss_lang_notice']  ?? '' ) ) );
    $notice = __( 'Content saved.', 'rag-semantic-search' );
}

// -- Import action --
if ( isset( $_POST['rss_action'] ) && $_POST['rss_action'] === 'import' ) {
    check_admin_referer( 'rss_import_nonce', 'rss_nonce' );

    if ( empty( $_FILES['rss_json']['name'] ) ) {
        $notice       = __( 'Please select a JSON file before importing.', 'rag-semantic-search' );
        $notice_class = 'notice-error';
    } else {
        if ( isset( $_POST['rss_clear_before_import'] ) ) {
            RSS_DB::empty_posts();
        }

        $stats = RSS_Importer::import_from_upload( $_FILES['rss_json'] ); // phpcs:ignore

        if ( ! empty( $stats['errors'] ) && $stats['imported'] === 0 && $stats['updated'] === 0 ) {
            $notice_class = 'notice-error';
            $notice       = implode( '<br>', array_map( 'esc_html', $stats['errors'] ) );
        } else {
            $notice = sprintf(
                /* translators: 1: inserted, 2: updated, 3: skipped */
                __( 'Import complete — %1$d inserted, %2$d updated, %3$d skipped.', 'rag-semantic-search' ),
                $stats['imported'],
                $stats['updated'],
                $stats['skipped']
            );
            if ( ! empty( $stats['errors'] ) ) {
                $notice      .= '<br>' . implode( '<br>', array_map( 'esc_html', $stats['errors'] ) );
                $notice_class = 'notice-warning';
            }
        }
    }
}

// -- Clear results cache action --
if ( isset( $_POST['rss_action'] ) && $_POST['rss_action'] === 'clear_cache' ) {
    check_admin_referer( 'rss_clear_cache_nonce', 'rss_nonce' );

    $deleted      = RSS_DB::empty_results();
    $notice       = sprintf(
        /* translators: %d: number of cached rows deleted */
        __( 'Search cache cleared — %d cached result rows deleted. Posts are untouched.', 'rag-semantic-search' ),
        $deleted
    );
    $notice_class = 'notice-success';
}

// -- Empty tables action --
if ( isset( $_POST['rss_action'] ) && $_POST['rss_action'] === 'empty' ) {
    check_admin_referer( 'rss_empty_nonce', 'rss_nonce' );

    $deleted      = RSS_DB::empty_tables();
    $notice       = sprintf(
        /* translators: 1: posts deleted, 2: results deleted */
        __( 'Tables emptied — %1$d posts and %2$d results deleted.', 'rag-semantic-search' ),
        $deleted['posts'],
        $deleted['results']
    );
    $notice_class = 'notice-warning';
}

// ── Status ────────────────────────────────────────────────────────────────────

$counts           = RSS_DB::get_counts();
$semantic_enabled = (bool) get_option( 'rss_semantic_enabled', '1' );
$promo_text       = get_option( 'rss_promo_text',  '' );
$lang_notice      = get_option( 'rss_lang_notice', '' );

?>
<div class="wrap rss-admin">

    <h1 class="rss-admin__title">
        <span class="dashicons dashicons-search"></span>
        <?php esc_html_e( 'RAG Semantic Search', 'rag-semantic-search' ); ?>
    </h1>

    <?php if ( $notice ) : ?>
        <div class="notice <?php echo esc_attr( $notice_class ); ?> is-dismissible">
            <p><?php echo wp_kses( $notice, [ 'br' => [] ] ); ?></p>
        </div>
    <?php endif; ?>

    <!-- ── 1. Status ───────────────────────────────────────────────────── -->
    <section class="rss-section">
        <h2><?php esc_html_e( 'Table status', 'rag-semantic-search' ); ?></h2>
        <div class="rss-status-cards">
            <div class="rss-card">
                <span class="rss-card__count"><?php echo esc_html( $counts['posts'] ); ?></span>
                <span class="rss-card__label"><?php esc_html_e( 'Posts indexed', 'rag-semantic-search' ); ?></span>
                <code class="rss-card__table"><?php echo esc_html( rss_table_posts() ); ?></code>
            </div>
            <div class="rss-card">
                <span class="rss-card__count"><?php echo esc_html( $counts['results'] ); ?></span>
                <span class="rss-card__label"><?php esc_html_e( 'Search results cached', 'rag-semantic-search' ); ?></span>
                <code class="rss-card__table"><?php echo esc_html( rss_table_results() ); ?></code>
            </div>
        </div>
    </section>

    <!-- ── 2. Settings ──────────────────────────────────────────────────── -->
    <section class="rss-section">
        <h2><?php esc_html_e( 'Settings', 'rag-semantic-search' ); ?></h2>
        <p class="description">
            <?php esc_html_e(
                'When semantic search is disabled, the [rag_search] shortcode shows only the standard WordPress search. Re-enable it at any time — no data is lost.',
                'rag-semantic-search'
            ); ?>
        </p>
        <form method="post" class="rss-form">
            <?php wp_nonce_field( 'rss_settings_nonce', 'rss_nonce' ); ?>
            <input type="hidden" name="rss_action" value="settings">
            <div class="rss-form__row">
                <label>
                    <input
                        type="checkbox"
                        name="rss_semantic_enabled"
                        value="1"
                        <?php checked( $semantic_enabled ); ?>
                    >
                    <?php esc_html_e( 'Enable semantic search', 'rag-semantic-search' ); ?>
                </label>
                <p class="description" style="margin-top:6px;">
                    <?php if ( $semantic_enabled ) : ?>
                        <span style="color:#2a7a2a;">&#10003; <?php esc_html_e( 'Semantic search is currently active.', 'rag-semantic-search' ); ?></span>
                    <?php else : ?>
                        <span style="color:#b32d2e;">&#10007; <?php esc_html_e( 'Semantic search is currently disabled.', 'rag-semantic-search' ); ?></span>
                    <?php endif; ?>
                </p>
            </div>
            <?php submit_button( __( 'Save settings', 'rag-semantic-search' ), 'primary', 'rss_submit_settings', false ); ?>
        </form>
    </section>

    <!-- ── 3. Content ──────────────────────────────────────────────────── -->
    <section class="rss-section">
        <h2><?php esc_html_e( 'Content', 'rag-semantic-search' ); ?></h2>

        <form method="post" class="rss-form">
            <?php wp_nonce_field( 'rss_content_nonce', 'rss_nonce' ); ?>
            <input type="hidden" name="rss_action" value="content">

            <!-- Promotional banner -->
            <div class="rss-form__row">
                <label class="rss-form__label" for="rss_promo_text">
                    <?php esc_html_e( 'Promotional banner', 'rag-semantic-search' ); ?>
                </label>
                <p class="description" style="margin-bottom:6px;">
                    <?php esc_html_e( 'Displayed when rag_semantic_search() is called in your theme (e.g. search.php). HTML allowed. Leave blank to hide.', 'rag-semantic-search' ); ?>
                </p>
                <textarea
                    id="rss_promo_text"
                    name="rss_promo_text"
                    class="widefat"
                    rows="4"
                ><?php echo esc_textarea( $promo_text ); ?></textarea>
                <?php if ( empty( $promo_text ) ) : ?>
                    <p class="description" style="margin-top:6px;">
                        <?php esc_html_e( 'Suggested text (copy and edit):', 'rag-semantic-search' ); ?><br>
                        <code>&lt;strong&gt;Semantic Search — Beta&lt;/strong&gt; : Looking for something specific? Try our new semantic search — it understands the meaning of your query, not just keywords. &lt;a href="<?php echo esc_url( home_url( '/semantic-search/' ) ); ?>"&gt;Try it now &amp;rarr;&lt;/a&gt;</code>
                    </p>
                <?php endif; ?>
            </div>

            <!-- Language notice -->
            <div class="rss-form__row" style="margin-top:20px;">
                <label class="rss-form__label" for="rss_lang_notice">
                    <?php esc_html_e( 'Language notice', 'rag-semantic-search' ); ?>
                </label>
                <p class="description" style="margin-bottom:6px;">
                    <?php esc_html_e( 'Displayed below the [rag_search] shortcode output. HTML allowed. Leave blank to hide.', 'rag-semantic-search' ); ?>
                </p>
                <textarea
                    id="rss_lang_notice"
                    name="rss_lang_notice"
                    class="widefat"
                    rows="3"
                ><?php echo esc_textarea( $lang_notice ); ?></textarea>
                <?php if ( empty( $lang_notice ) ) : ?>
                    <p class="description" style="margin-top:6px;">
                        <?php esc_html_e( 'Suggested text (copy and edit):', 'rag-semantic-search' ); ?><br>
                        <code><?php esc_html_e( 'The semantic search only works on posts in English. For posts in other languages, please use the standard WordPress search.', 'rag-semantic-search' ); ?></code>
                    </p>
                <?php endif; ?>
            </div>

            <?php submit_button( __( 'Save content', 'rag-semantic-search' ), 'primary', 'rss_submit_content', false ); ?>
        </form>
    </section>

    <!-- ── 4. Import ───────────────────────────────────────────────────── -->
    <section class="rss-section">
        <h2><?php esc_html_e( 'Import posts from rag_bridge.json', 'rag-semantic-search' ); ?></h2>
        <p class="description">
            <?php esc_html_e(
                'Generate rag_bridge.json by running bridge_export.py on the RAG system, then upload it here. ' .
                'Re-importing the same file is safe — existing posts are updated, not duplicated.',
                'rag-semantic-search'
            ); ?>
        </p>

        <form method="post" enctype="multipart/form-data" class="rss-form">
            <?php wp_nonce_field( 'rss_import_nonce', 'rss_nonce' ); ?>
            <input type="hidden" name="rss_action" value="import">

            <div class="rss-form__row">
                <label for="rss_json" class="rss-form__label">
                    <?php esc_html_e( 'Exchange file (.json)', 'rag-semantic-search' ); ?>
                </label>
                <input
                    type="file"
                    id="rss_json"
                    name="rss_json"
                    accept=".json,application/json"
                    class="rss-form__file"
                    required
                >
            </div>

            <div class="rss-form__row">
                <label>
                    <input
                        type="checkbox"
                        name="rss_clear_before_import"
                        value="1"
                    >
                    <?php esc_html_e( 'Clear all existing posts before importing', 'rag-semantic-search' ); ?>
                </label>
                <p class="description" style="margin-top:4px;">
                    <?php esc_html_e( 'When checked, all rows in wp_rag_posts are deleted before the new file is inserted. Use this for a full replacement instead of an upsert.', 'rag-semantic-search' ); ?>
                </p>
            </div>

            <div class="rss-form__row">
                <?php submit_button(
                    __( 'Import posts', 'rag-semantic-search' ),
                    'primary',
                    'rss_submit_import',
                    false
                ); ?>
            </div>
        </form>
    </section>

    <!-- ── 5. Export ──────────────────────────────────────────────────── -->
    <section class="rss-section">
        <h2><?php esc_html_e( 'Export posts to JSON', 'rag-semantic-search' ); ?></h2>
        <p class="description">
            <?php esc_html_e(
                'Download all posts currently stored in wp_rag_posts as a rag_bridge.json-compatible file. ' .
                'You can edit the exported file and re-import it to add or update entries.',
                'rag-semantic-search'
            ); ?>
        </p>
        <p class="description" style="margin-top:6px;">
            <?php printf(
                /* translators: %d: number of posts available for export */
                esc_html__( 'Posts available for export: %d.', 'rag-semantic-search' ),
                (int) $counts['posts']
            ); ?>
        </p>

        <form method="post" class="rss-form" style="margin-top:12px;">
            <?php wp_nonce_field( 'rss_export_nonce', 'rss_nonce' ); ?>
            <input type="hidden" name="rss_action" value="export">
            <?php submit_button(
                __( 'Export posts', 'rag-semantic-search' ),
                'secondary',
                'rss_submit_export',
                false
            ); ?>
        </form>
    </section>

    <!-- ── 6. Clear search cache ──────────────────────────────────────── -->
    <section class="rss-section">
        <h2><?php esc_html_e( 'Search cache', 'rag-semantic-search' ); ?></h2>
        <p class="description">
            <?php esc_html_e(
                'Every search result set is cached in wp_rag_results for 7 days and expired rows are purged automatically before each search. ' .
                'Use this button to flush the cache immediately — posts in wp_rag_posts are not affected.',
                'rag-semantic-search'
            ); ?>
        </p>
        <p class="description" style="margin-top:6px;">
            <?php printf(
                /* translators: %d: current cache row count */
                esc_html__( 'Current cache size: %d rows.', 'rag-semantic-search' ),
                (int) $counts['results']
            ); ?>
        </p>

        <form method="post" class="rss-form" style="margin-top:12px;">
            <?php wp_nonce_field( 'rss_clear_cache_nonce', 'rss_nonce' ); ?>
            <input type="hidden" name="rss_action" value="clear_cache">
            <?php submit_button(
                __( 'Clear search cache', 'rag-semantic-search' ),
                'secondary',
                'rss_submit_clear_cache',
                false
            ); ?>
        </form>
    </section>

    <!-- ── 3. Danger zone ──────────────────────────────────────────────── -->
    <section class="rss-section rss-section--danger">
        <h2><?php esc_html_e( 'Danger zone', 'rag-semantic-search' ); ?></h2>
        <p class="description">
            <?php esc_html_e(
                'Empty both tables. All posts and cached search results will be deleted. ' .
                'The tables themselves are preserved — you can re-import at any time.',
                'rag-semantic-search'
            ); ?>
        </p>

        <form
            method="post"
            class="rss-form"
            onsubmit="return confirm('<?php echo esc_js( __( 'Delete all posts and results? This cannot be undone.', 'rag-semantic-search' ) ); ?>')"
        >
            <?php wp_nonce_field( 'rss_empty_nonce', 'rss_nonce' ); ?>
            <input type="hidden" name="rss_action" value="empty">

            <?php submit_button(
                __( 'Empty tables', 'rag-semantic-search' ),
                'delete',
                'rss_submit_empty',
                false
            ); ?>
        </form>
    </section>

</div><!-- .wrap.rss-admin -->
