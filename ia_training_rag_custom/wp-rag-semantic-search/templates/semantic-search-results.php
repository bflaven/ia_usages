<?php
/**
 * Template: semantic-search-results.php
 *
 * Rendered by the [rag_search] shortcode.
 * Receives from the shortcode function:
 *   $query   (string)  — sanitised query string (may be empty)
 *   $results (array)   — array of stdClass from RSS_Search::search()
 *   $mode    (string)  — 'semantic' | 'standard'
 *   $limit   (int)     — max results configured in shortcode
 *
 * The "Standard search" mode submits to WP native search (/?s=query).
 * The "Semantic search" mode submits to the current page (?rss_q=query).
 */

defined( 'ABSPATH' ) || exit;

$current_url = get_permalink() ?: home_url( add_query_arg( [] ) );
?>

<div class="rss-wrap">

    <!-- ── Search form ─────────────────────────────────────────────────── -->
    <div class="rss-form-wrap">
        <form class="rss-search-form" method="get" action="<?php echo esc_url( $current_url ); ?>">

            <div class="rss-search-form__input-row">
                <input
                    type="search"
                    name="rss_q"
                    class="rss-search-form__input"
                    value="<?php echo esc_attr( $query ); ?>"
                    placeholder="<?php esc_attr_e( 'Search articles…', 'rag-semantic-search' ); ?>"
                    autocomplete="off"
                    required
                >
                <button type="submit" class="rss-search-form__submit">
                    <?php esc_html_e( 'Search', 'rag-semantic-search' ); ?>
                </button>
            </div>

            <?php if ( $semantic_enabled ) : ?>
            <div class="rss-search-form__modes">
                <span class="rss-mode-label"><?php esc_html_e( 'Mode:', 'rag-semantic-search' ); ?></span>

                <label class="rss-mode-pill <?php echo $mode === 'standard' ? 'rss-mode-pill--active' : ''; ?>">
                    <input
                        type="radio"
                        name="rss_mode"
                        value="standard"
                        <?php checked( $mode, 'standard' ); ?>
                        onchange="this.form.submit()"
                    >
                    <?php esc_html_e( 'Standard search', 'rag-semantic-search' ); ?>
                </label>

                <label class="rss-mode-pill <?php echo $mode === 'semantic' ? 'rss-mode-pill--active' : ''; ?>">
                    <input
                        type="radio"
                        name="rss_mode"
                        value="semantic"
                        <?php checked( $mode, 'semantic' ); ?>
                        onchange="this.form.submit()"
                    >
                    <?php esc_html_e( 'Semantic search', 'rag-semantic-search' ); ?>
                </label>
            </div>
            <?php endif; ?>

        </form>
    </div><!-- .rss-form-wrap -->

    <!-- ── Results area ────────────────────────────────────────────────── -->
    <div class="rss-results">

        <?php if ( $query && $mode === 'semantic' ) : ?>

            <!-- Results header -->
            <p class="rss-results__header">
                <?php if ( ! empty( $results ) ) : ?>
                    <?php printf(
                        /* translators: 1: count, 2: query */
                        wp_kses(
                            _n(
                                '%1$d result for <em>%2$s</em>',
                                '%1$d results for <em>%2$s</em>',
                                count( $results ),
                                'rag-semantic-search'
                            ),
                            [ 'em' => [] ]
                        ),
                        count( $results ),
                        esc_html( $query )
                    ); ?>
                <?php else : ?>
                    <?php printf(
                        /* translators: %s: query */
                        esc_html__( 'No results found for "%s".', 'rag-semantic-search' ),
                        esc_html( $query )
                    ); ?>
                <?php endif; ?>
            </p>

            <?php if ( ! empty( $results ) ) : ?>

                <ol class="rss-results__list">
                <?php foreach ( $results as $r ) : ?>

                    <li class="rss-result-card">

                        <!-- Score bar -->
                        <div class="rss-result-card__score-wrap" title="<?php echo esc_attr( __( 'Relevance score', 'rag-semantic-search' ) ); ?>">
                            <div class="rss-result-card__score-bar">
                                <div
                                    class="rss-result-card__score-fill"
                                    style="width: <?php echo esc_attr( round( $r->score * 100 ) ); ?>%"
                                ></div>
                            </div>
                            <span class="rss-result-card__score-num"><?php echo esc_html( number_format( $r->score, 2 ) ); ?></span>
                        </div>

                        <!-- Title -->
                        <h3 class="rss-result-card__title">
                            <a href="<?php echo esc_url( $r->url ); ?>" target="_blank" rel="noopener">
                                <?php echo esc_html( $r->title ); ?>
                            </a>
                        </h3>

                        <!-- Meta -->
                        <p class="rss-result-card__meta">
                            <span class="rss-result-card__date">
                                <?php echo esc_html( date_i18n( get_option( 'date_format' ), strtotime( $r->date ) ) ); ?>
                            </span>
                            <span class="rss-result-card__sep" aria-hidden="true">·</span>
                            <span class="rss-result-card__source">
                                <?php echo esc_html( wp_parse_url( $r->url, PHP_URL_HOST ) ?: $r->url ); ?>
                            </span>
                        </p>

                        <!-- Snippet -->
                        <p class="rss-result-card__snippet">
                            <?php echo esc_html( $r->snippet ?: $r->excerpt ); ?>
                        </p>

                        <!-- Read more -->
                        <a class="rss-result-card__link" href="<?php echo esc_url( $r->url ); ?>" target="_blank" rel="noopener">
                            <?php esc_html_e( 'Read article', 'rag-semantic-search' ); ?>
                            <span aria-hidden="true">→</span>
                        </a>

                    </li>

                <?php endforeach; ?>
                </ol>

            <?php else : ?>

                <div class="rss-no-results">
                    <p><?php esc_html_e( 'Try different keywords, or switch to Standard search above.', 'rag-semantic-search' ); ?></p>
                </div>

            <?php endif; ?>

        <?php elseif ( ! $query ) : ?>

            <p class="rss-hint">
                <?php esc_html_e( 'Type a question or keywords above and press Search.', 'rag-semantic-search' ); ?>
            </p>

        <?php endif; ?>

    </div><!-- .rss-results -->

    <!-- ── Language notice (editable via WP Admin → RAG Search → Content) ─ -->
    <?php $rss_lang_notice = get_option( 'rss_lang_notice', '' ); ?>
    <?php if ( ! empty( trim( strip_tags( $rss_lang_notice ) ) ) ) : ?>
    <p class="rss-lang-notice">
        <?php echo wp_kses_post( $rss_lang_notice ); ?>
    </p>
    <?php endif; ?>

</div><!-- .rss-wrap -->
