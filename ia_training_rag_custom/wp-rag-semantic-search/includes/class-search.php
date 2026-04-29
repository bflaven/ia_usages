<?php
/**
 * RSS_Search — Query wp_rag_posts and return ranked results.
 *
 * Strategy:
 *   1. MySQL FULLTEXT search in BOOLEAN MODE (fast, ranked).
 *   2. If FULLTEXT returns 0 results, fall back to LIKE search on title + excerpt.
 *
 * Scores are normalised so the top result always equals 1.0,
 * making the score bar in the template meaningful regardless of query.
 *
 * Public API:
 *   RSS_Search::search( $query, $limit )  → array of result objects
 */

defined( 'ABSPATH' ) || exit;

class RSS_Search {

    // ── Public entry point ────────────────────────────────────────────────────

    /**
     * Search wp_rag_posts and return up to $limit ranked results.
     *
     * Each result is a stdClass with:
     *   id, title, url, date, slug, excerpt, score (0.0–1.0), snippet.
     *
     * @param  string $query  Raw user query.
     * @param  int    $limit  Maximum results to return (default 10).
     * @return array          Array of stdClass result objects.
     */
    public static function search( string $query, int $limit = 10 ): array {
        $query = trim( $query );
        if ( $query === '' ) {
            return [];
        }

        // Ensure the FULLTEXT index exists before querying.
        self::ensure_fulltext_index();

        $rows = self::fulltext_search( $query, $limit );

        if ( empty( $rows ) ) {
            $rows = self::like_search( $query, $limit );
        }

        return self::normalise( $rows, $query );
    }

    // ── FULLTEXT search ───────────────────────────────────────────────────────

    private static function fulltext_search( string $query, int $limit ): array {
        global $wpdb;

        $table   = rss_table_posts();
        $boolean = self::to_boolean_query( $query );

        // phpcs:disable WordPress.DB.PreparedSQL.InterpolatedNotPrepared
        $sql = $wpdb->prepare(
            "SELECT id, title, url, date, slug, excerpt, text,
                    MATCH(title, excerpt, text) AGAINST (%s IN BOOLEAN MODE) AS ft_score
             FROM   {$table}
             WHERE  MATCH(title, excerpt, text) AGAINST (%s IN BOOLEAN MODE)
             ORDER  BY ft_score DESC
             LIMIT  %d",
            $boolean,
            $boolean,
            $limit
        );
        // phpcs:enable

        return $wpdb->get_results( $sql ) ?: []; // phpcs:ignore
    }

    // ── LIKE fallback ─────────────────────────────────────────────────────────

    private static function like_search( string $query, int $limit ): array {
        global $wpdb;

        $table = rss_table_posts();
        $like  = '%' . $wpdb->esc_like( $query ) . '%';

        // phpcs:disable WordPress.DB.PreparedSQL.InterpolatedNotPrepared
        $sql = $wpdb->prepare(
            "SELECT id, title, url, date, slug, excerpt, text,
                    1.0 AS ft_score
             FROM   {$table}
             WHERE  title   LIKE %s
                OR  excerpt LIKE %s
                OR  text    LIKE %s
             ORDER  BY date DESC
             LIMIT  %d",
            $like,
            $like,
            $like,
            $limit
        );
        // phpcs:enable

        return $wpdb->get_results( $sql ) ?: []; // phpcs:ignore
    }

    // ── Normalise + snippet ───────────────────────────────────────────────────

    /**
     * Normalise scores to 0–1, add a readable snippet, strip raw text field.
     */
    private static function normalise( array $rows, string $query ): array {
        if ( empty( $rows ) ) {
            return [];
        }

        $max = (float) $rows[0]->ft_score;

        $results = [];
        foreach ( $rows as $row ) {
            $score = ( $max > 0 ) ? round( (float) $row->ft_score / $max, 2 ) : 1.0;

            $result          = new stdClass();
            $result->id      = (int) $row->id;
            $result->title   = $row->title;
            $result->url     = $row->url;
            $result->date    = $row->date;
            $result->slug    = $row->slug;
            $result->excerpt = $row->excerpt;
            $result->score   = $score;
            $result->snippet = self::make_snippet( $row->text, $query );

            $results[] = $result;
        }

        return $results;
    }

    // ── Format cached rows ────────────────────────────────────────────────────

    /**
     * Convert rows returned by RSS_DB::get_cached_results() into the same
     * stdClass format produced by search(). Scores are already normalised (0–1)
     * so no further computation is needed.
     *
     * @param  array  $rows   Rows from RSS_DB::get_cached_results().
     * @param  string $query  Original query (used to build the snippet).
     * @return array          Array of stdClass result objects.
     */
    public static function format_cached( array $rows, string $query ): array {
        $results = [];
        foreach ( $rows as $row ) {
            $result          = new stdClass();
            $result->id      = (int) $row->id;
            $result->title   = $row->title;
            $result->url     = $row->url;
            $result->date    = $row->date;
            $result->slug    = $row->slug;
            $result->excerpt = $row->excerpt;
            $result->score   = (float) $row->score;
            $result->snippet = self::make_snippet( $row->text, $query );
            $results[]       = $result;
        }
        return $results;
    }

    // ── Snippet helper ────────────────────────────────────────────────────────

    /**
     * Extract a ~200-char snippet from $text centred on the first query word match.
     * Falls back to the stored excerpt if no match found in the text.
     */
    public static function make_snippet( string $text, string $query, int $length = 200 ): string {
        $text  = wp_strip_all_tags( $text );
        $words = preg_split( '/\s+/', trim( $query ), -1, PREG_SPLIT_NO_EMPTY );

        $pos = false;
        foreach ( $words as $word ) {
            $pos = stripos( $text, $word );
            if ( $pos !== false ) {
                break;
            }
        }

        if ( $pos === false ) {
            // No match: return the first $length chars.
            return mb_substr( $text, 0, $length ) . ( mb_strlen( $text ) > $length ? '…' : '' );
        }

        $start   = max( 0, $pos - 60 );
        $snippet = mb_substr( $text, $start, $length );

        if ( $start > 0 ) {
            $snippet = '…' . $snippet;
        }
        if ( $start + $length < mb_strlen( $text ) ) {
            $snippet .= '…';
        }

        return $snippet;
    }

    // ── Query helpers ─────────────────────────────────────────────────────────

    /**
     * Convert a plain query string to MySQL BOOLEAN MODE operators.
     * Each word becomes a +word (required) term.
     * Falls back to plain string if it already contains operators.
     */
    private static function to_boolean_query( string $query ): string {
        if ( preg_match( '/[+\-*"<>~()]/', $query ) ) {
            return $query; // already uses operators
        }
        $words = preg_split( '/\s+/', trim( $query ), -1, PREG_SPLIT_NO_EMPTY );
        // Require all words but allow partial match; for short words use plain mode.
        if ( count( $words ) === 1 && mb_strlen( $words[0] ) < 4 ) {
            return $query; // let MySQL decide
        }
        return implode( ' ', array_map( fn( $w ) => '+' . $w, $words ) );
    }

    // ── Index management ─────────────────────────────────────────────────────

    /**
     * Add a FULLTEXT index on (title, excerpt, text) if it does not exist.
     * Safe to call on every page load — the information_schema check is cheap.
     */
    public static function ensure_fulltext_index(): void {
        global $wpdb;

        $table = rss_table_posts();

        $exists = (int) $wpdb->get_var( // phpcs:ignore
            $wpdb->prepare(
                "SELECT COUNT(*)
                 FROM   information_schema.STATISTICS
                 WHERE  table_schema = DATABASE()
                   AND  table_name   = %s
                   AND  index_name   = 'ft_rag_posts_content'",
                $table
            )
        );

        if ( ! $exists ) {
            $wpdb->query( "ALTER TABLE {$table} ADD FULLTEXT INDEX ft_rag_posts_content (title, excerpt, text)" ); // phpcs:ignore
        }
    }
}
