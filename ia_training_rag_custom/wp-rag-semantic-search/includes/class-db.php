<?php
/**
 * RSS_DB — Table lifecycle management.
 *
 * Handles: create, drop, empty.
 * Schema mirrors data/bridge/rag_schema.sql exactly.
 * Called by: activation hook, uninstall.php, admin empty-tables action.
 */

defined( 'ABSPATH' ) || exit;

class RSS_DB {

    // ── Create ────────────────────────────────────────────────────────────────

    /**
     * Create rag_posts and rag_results tables if they do not exist.
     * Safe to call multiple times (uses dbDelta / IF NOT EXISTS logic).
     */
    public static function create_tables(): void {
        global $wpdb;

        $charset_collate = $wpdb->get_charset_collate();
        $posts_table     = rss_table_posts();
        $results_table   = rss_table_results();

        // dbDelta requires two spaces before each column definition line.
        $sql_posts = "CREATE TABLE {$posts_table} (
          id          INT          NOT NULL,
          title       VARCHAR(500) NOT NULL,
          url         VARCHAR(1000) NOT NULL,
          date        DATE         NOT NULL,
          slug        VARCHAR(500) NOT NULL,
          excerpt     TEXT,
          text        LONGTEXT     NOT NULL,
          imported_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (id)
        ) {$charset_collate};";

        $sql_results = "CREATE TABLE {$results_table} (
          id          INT          NOT NULL AUTO_INCREMENT,
          query_hash  CHAR(64)     NOT NULL,
          query_text  TEXT         NOT NULL,
          post_id     INT          NOT NULL,
          score       FLOAT        NOT NULL,
          `rank`      TINYINT      NOT NULL,
          created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
          expires_at  DATETIME     NOT NULL,
          PRIMARY KEY (id),
          KEY idx_query_hash (query_hash),
          KEY idx_expires_at (expires_at)
        ) {$charset_collate};";

        // dbDelta is the WordPress-recommended way to create/update tables.
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta( $sql_posts );
        dbDelta( $sql_results );

        // Add FK separately — dbDelta does not support FOREIGN KEY constraints.
        // We skip it here and rely on application-level integrity (the importer
        // always inserts into rag_posts before rag_results).
    }

    // ── Drop ──────────────────────────────────────────────────────────────────

    /**
     * Drop both tables. Called only from uninstall.php.
     * Results table first to respect the FK dependency.
     */
    public static function drop_tables(): void {
        global $wpdb;

        // phpcs:disable WordPress.DB.PreparedSQL.NotPrepared
        $wpdb->query( 'DROP TABLE IF EXISTS ' . rss_table_results() );
        $wpdb->query( 'DROP TABLE IF EXISTS ' . rss_table_posts() );
        // phpcs:enable
    }

    // ── Empty ─────────────────────────────────────────────────────────────────

    /**
     * Delete all rows from both tables without dropping them.
     * Called from the admin "Empty tables" action.
     * Returns an array with the row counts deleted.
     */
    public static function empty_tables(): array {
        global $wpdb;

        $deleted_results = $wpdb->query( 'DELETE FROM ' . rss_table_results() ); // phpcs:ignore
        $deleted_posts   = $wpdb->query( 'DELETE FROM ' . rss_table_posts() );   // phpcs:ignore

        return [
            'posts'   => (int) $deleted_posts,
            'results' => (int) $deleted_results,
        ];
    }

    /**
     * Delete all rows from rag_results only — posts are untouched.
     * Lighter alternative to empty_tables() when you only want to flush the cache.
     *
     * @return int Number of rows deleted.
     */
    public static function empty_results(): int {
        global $wpdb;
        return (int) $wpdb->query( 'DELETE FROM ' . rss_table_results() ); // phpcs:ignore
    }

    // ── Status ────────────────────────────────────────────────────────────────

    /**
     * Return row counts for both tables (used by the admin page dashboard).
     * Returns zeroes if tables do not exist yet (e.g. right after file copy).
     */
    public static function get_counts(): array {
        global $wpdb;

        $results_table = rss_table_results();

        // Guard: if the results table is missing, tables were never created.
        if ( ! $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $results_table ) ) ) {
            return [ 'posts' => 0, 'results' => 0 ];
        }

        return [
            'posts'   => (int) $wpdb->get_var( 'SELECT COUNT(*) FROM ' . rss_table_posts() ),   // phpcs:ignore
            'results' => (int) $wpdb->get_var( 'SELECT COUNT(*) FROM ' . $results_table ),       // phpcs:ignore
        ];
    }

    // ── TTL purge ─────────────────────────────────────────────────────────────

    /**
     * Delete expired rows from rag_results (expires_at < NOW()).
     * Called automatically before each search query.
     */
    public static function purge_expired_results(): int {
        global $wpdb;

        $results_table = rss_table_results();

        // Guard: skip silently if the table does not exist yet.
        if ( ! $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $results_table ) ) ) {
            return 0;
        }

        return (int) $wpdb->query( // phpcs:ignore
            'DELETE FROM ' . $results_table . ' WHERE expires_at < NOW()'
        );
    }

    // ── Cache write ───────────────────────────────────────────────────────────

    /**
     * Persist a set of search results in rag_results for $ttl_days days.
     *
     * Each call replaces any previous cached rows for the same query so that
     * re-running the same search always reflects the current wp_rag_posts data.
     *
     * @param  string    $query     Raw query string.
     * @param  array     $results   Array of stdClass from RSS_Search::search().
     * @param  int       $ttl_days  Cache lifetime in days (default 7).
     */
    public static function save_results( string $query, array $results, int $ttl_days = 7 ): void {
        global $wpdb;

        $table      = rss_table_results();
        $query_hash = hash( 'sha256', mb_strtolower( trim( $query ) ) );
        $expires_at = gmdate( 'Y-m-d H:i:s', time() + $ttl_days * DAY_IN_SECONDS );

        // Replace stale cache for this query before inserting fresh rows.
        $wpdb->delete( $table, [ 'query_hash' => $query_hash ], [ '%s' ] ); // phpcs:ignore

        foreach ( $results as $rank => $result ) {
            $wpdb->insert( // phpcs:ignore
                $table,
                [
                    'query_hash' => $query_hash,
                    'query_text' => $query,
                    'post_id'    => $result->id,
                    'score'      => $result->score,
                    'rank'       => $rank + 1,
                    'expires_at' => $expires_at,
                ],
                [ '%s', '%s', '%d', '%f', '%d', '%s' ]
            );
        }
    }

    // ── Cache read ────────────────────────────────────────────────────────────

    /**
     * Return cached results for $query, or an empty array on cache miss.
     *
     * JOINs rag_results with rag_posts so callers receive full post data
     * ready for display — no second query needed.
     *
     * @param  string $query  Raw query string (hashed internally).
     * @return array          Rows as stdClass objects ordered by rank ASC,
     *                        or [] on cache miss / expired.
     */
    public static function get_cached_results( string $query ): array {
        global $wpdb;

        $results_table = rss_table_results();
        $posts_table   = rss_table_posts();
        $query_hash    = hash( 'sha256', mb_strtolower( trim( $query ) ) );

        // phpcs:disable WordPress.DB.PreparedSQL.InterpolatedNotPrepared
        $rows = $wpdb->get_results(
            $wpdb->prepare(
                "SELECT p.id, p.title, p.url, p.date, p.slug, p.excerpt, p.text,
                        r.score, r.rank
                 FROM   {$results_table} r
                 JOIN   {$posts_table}   p ON p.id = r.post_id
                 WHERE  r.query_hash = %s
                   AND  r.expires_at > NOW()
                 ORDER  BY r.rank ASC",
                $query_hash
            )
        );
        // phpcs:enable

        return $rows ?: [];
    }
}
