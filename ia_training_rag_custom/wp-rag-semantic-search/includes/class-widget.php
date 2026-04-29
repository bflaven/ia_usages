<?php
/**
 * RSS_Widget — Sidebar widget for RAG Semantic Search.
 *
 * Renders a compact search form that submits the query to the configured
 * results page (e.g. /semantic-search/?rss_q=…).
 *
 * Add it via Appearance → Widgets → "RAG Semantic Search".
 * Configure the "Results page URL" to match the page where [rag_search]
 * is placed.
 */

defined( 'ABSPATH' ) || exit;

class RSS_Widget extends WP_Widget {

    public function __construct() {
        parent::__construct(
            'rss_semantic_search',
            __( 'RAG Semantic Search', 'rag-semantic-search' ),
            [
                'description' => __( 'Semantic search box — submits to your RAG search results page.', 'rag-semantic-search' ),
                'classname'   => 'widget_rss_semantic_search',
            ]
        );
    }

    // ── Front-end output ──────────────────────────────────────────────────────

    public function widget( $args, $instance ) {
        $title    = apply_filters( 'widget_title', $instance['title'] ?? '', $instance, $this->id_base );
        $page_url = ! empty( $instance['page_url'] )
            ? esc_url( $instance['page_url'] )
            : esc_url( home_url( '/semantic-search/' ) );

        echo $args['before_widget']; // phpcs:ignore

        if ( $title ) {
            echo $args['before_title'] . esc_html( $title ) . $args['after_title']; // phpcs:ignore
        }

        // Current query value (pre-fill if the widget is on the results page).
        $current_q = isset( $_GET['rss_q'] ) // phpcs:ignore
            ? sanitize_text_field( wp_unslash( $_GET['rss_q'] ) ) // phpcs:ignore
            : '';
        ?>
        <form role="search" method="get" class="rss-widget-form" action="<?php echo $page_url; // phpcs:ignore ?>">
            <div class="rss-widget-form__row">
                <input
                    type="search"
                    name="rss_q"
                    class="rss-widget-form__input"
                    value="<?php echo esc_attr( $current_q ); ?>"
                    placeholder="<?php esc_attr_e( 'Search articles…', 'rag-semantic-search' ); ?>"
                    autocomplete="off"
                    aria-label="<?php esc_attr_e( 'Semantic search', 'rag-semantic-search' ); ?>"
                >
                <button type="submit" class="rss-widget-form__submit">
                    <?php esc_html_e( 'Search', 'rag-semantic-search' ); ?>
                </button>
            </div>
        </form>
        <?php

        echo $args['after_widget']; // phpcs:ignore
    }

    // ── Admin form ────────────────────────────────────────────────────────────

    public function form( $instance ) {
        $title    = $instance['title']    ?? __( 'Semantic Search', 'rag-semantic-search' );
        $page_url = $instance['page_url'] ?? '';
        ?>
        <p>
            <label for="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>">
                <?php esc_html_e( 'Title:', 'rag-semantic-search' ); ?>
            </label>
            <input
                class="widefat"
                id="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>"
                name="<?php echo esc_attr( $this->get_field_name( 'title' ) ); ?>"
                type="text"
                value="<?php echo esc_attr( $title ); ?>"
            >
        </p>
        <p>
            <label for="<?php echo esc_attr( $this->get_field_id( 'page_url' ) ); ?>">
                <?php esc_html_e( 'Results page URL:', 'rag-semantic-search' ); ?>
            </label>
            <input
                class="widefat"
                id="<?php echo esc_attr( $this->get_field_id( 'page_url' ) ); ?>"
                name="<?php echo esc_attr( $this->get_field_name( 'page_url' ) ); ?>"
                type="url"
                value="<?php echo esc_attr( $page_url ); ?>"
                placeholder="<?php echo esc_attr( home_url( '/semantic-search/' ) ); ?>"
            >
            <span class="description">
                <?php esc_html_e( 'URL of the page containing the [rag_search] shortcode.', 'rag-semantic-search' ); ?>
            </span>
        </p>
        <?php
    }

    // ── Save settings ─────────────────────────────────────────────────────────

    public function update( $new_instance, $old_instance ) {
        return [
            'title'    => sanitize_text_field( $new_instance['title'] ?? '' ),
            'page_url' => esc_url_raw( $new_instance['page_url'] ?? '' ),
        ];
    }
}
