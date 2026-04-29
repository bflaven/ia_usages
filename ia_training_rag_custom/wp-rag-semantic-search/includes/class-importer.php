<?php
/**
 * RSS_Importer — Parse rag_bridge.json and upsert records into wp_rag_posts.
 *
 * Only rag_posts is populated here.
 * rag_results is written by the search layer (T6) when queries are executed.
 *
 * Public API:
 *   RSS_Importer::import_from_upload( $_FILES['rss_json'] )  → array of stats
 *   RSS_Importer::import_records( $records )                 → array of stats
 */

defined( 'ABSPATH' ) || exit;

class RSS_Importer {

    /** Required fields in every exchange-file record. */
    private const REQUIRED = [ 'id', 'title', 'url', 'date', 'slug', 'text' ];

    // ── Entry point: uploaded file ────────────────────────────────────────────

    /**
     * Validate and process a file from $_FILES.
     *
     * @param  array $file  One entry from $_FILES (keys: name, tmp_name, error, size).
     * @return array        Stats: imported, updated, skipped, errors (list of strings).
     */
    public static function import_from_upload( array $file ): array {
        $stats = [ 'imported' => 0, 'updated' => 0, 'skipped' => 0, 'errors' => [] ];

        // -- basic upload checks --
        if ( ! isset( $file['error'] ) || $file['error'] !== UPLOAD_ERR_OK ) {
            $stats['errors'][] = __( 'Upload error. Please try again.', 'rag-semantic-search' );
            return $stats;
        }

        $ext = strtolower( pathinfo( $file['name'], PATHINFO_EXTENSION ) );
        if ( $ext !== 'json' ) {
            $stats['errors'][] = __( 'Only .json files are accepted.', 'rag-semantic-search' );
            return $stats;
        }

        if ( $file['size'] > 50 * 1024 * 1024 ) { // 50 MB hard cap
            $stats['errors'][] = __( 'File exceeds the 50 MB limit.', 'rag-semantic-search' );
            return $stats;
        }

        // -- decode --
        $raw = file_get_contents( $file['tmp_name'] ); // phpcs:ignore
        if ( $raw === false ) {
            $stats['errors'][] = __( 'Could not read uploaded file.', 'rag-semantic-search' );
            return $stats;
        }

        $records = json_decode( $raw, true );
        if ( ! is_array( $records ) || json_last_error() !== JSON_ERROR_NONE ) {
            $stats['errors'][] = sprintf(
                /* translators: %s: JSON error message */
                __( 'Invalid JSON: %s', 'rag-semantic-search' ),
                json_last_error_msg()
            );
            return $stats;
        }

        return self::import_records( $records );
    }

    // ── Entry point: array of records ─────────────────────────────────────────

    /**
     * Process a decoded array of records (already loaded into memory).
     *
     * @param  array $records  Array of associative arrays from rag_bridge.json.
     * @return array           Stats: imported, updated, skipped, errors.
     */
    public static function import_records( array $records ): array {
        $stats = [ 'imported' => 0, 'updated' => 0, 'skipped' => 0, 'errors' => [] ];

        if ( empty( $records ) ) {
            $stats['errors'][] = __( 'The file contains no records.', 'rag-semantic-search' );
            return $stats;
        }

        foreach ( $records as $index => $record ) {
            if ( ! self::validate_record( $record ) ) {
                $stats['skipped']++;
                $stats['errors'][] = sprintf(
                    /* translators: 1: record index, 2: required fields list */
                    __( 'Record #%1$d skipped — missing required field(s): %2$s', 'rag-semantic-search' ),
                    $index,
                    implode( ', ', self::missing_fields( $record ) )
                );
                continue;
            }

            $result = self::upsert_post( $record );
            if ( $result === 'inserted' ) {
                $stats['imported']++;
            } elseif ( $result === 'updated' ) {
                $stats['updated']++;
            } else {
                $stats['skipped']++;
                $stats['errors'][] = sprintf(
                    /* translators: %d: post id */
                    __( 'DB error on post id %d. Check error log.', 'rag-semantic-search' ),
                    (int) $record['id']
                );
            }
        }

        return $stats;
    }

    // ── Single-record upsert ──────────────────────────────────────────────────

    /**
     * INSERT or UPDATE one post record in wp_rag_posts.
     * Uses ON DUPLICATE KEY UPDATE so re-importing the same file is idempotent.
     *
     * @return string  'inserted' | 'updated' | 'error'
     */
    private static function upsert_post( array $r ): string {
        global $wpdb;

        $table = rss_table_posts();
        $now   = current_time( 'mysql' );

        // Check whether the row already exists to determine the return value.
        $exists = (bool) $wpdb->get_var( // phpcs:ignore
            $wpdb->prepare( "SELECT 1 FROM {$table} WHERE id = %d", (int) $r['id'] ) // phpcs:ignore
        );

        $sql = $wpdb->prepare( // phpcs:ignore
            "INSERT INTO {$table} (id, title, url, date, slug, excerpt, text, imported_at)
             VALUES (%d, %s, %s, %s, %s, %s, %s, %s)
             ON DUPLICATE KEY UPDATE
               title       = VALUES(title),
               url         = VALUES(url),
               date        = VALUES(date),
               slug        = VALUES(slug),
               excerpt     = VALUES(excerpt),
               text        = VALUES(text),
               imported_at = VALUES(imported_at)",
            (int)    $r['id'],
            (string) $r['title'],
            (string) $r['url'],
            (string) $r['date'],
            (string) $r['slug'],
            (string) ( $r['excerpt'] ?? '' ),
            (string) $r['text'],
            $now
        );

        $result = $wpdb->query( $sql ); // phpcs:ignore

        if ( $result === false ) {
            return 'error';
        }

        // ON DUPLICATE KEY UPDATE returns 2 affected rows on update, 1 on insert.
        if ( $exists ) {
            return 'updated';
        }
        return 'inserted';
    }

    // ── Validation helpers ────────────────────────────────────────────────────

    private static function validate_record( array $r ): bool {
        return empty( self::missing_fields( $r ) );
    }

    private static function missing_fields( array $r ): array {
        $missing = [];
        foreach ( self::REQUIRED as $field ) {
            if ( ! array_key_exists( $field, $r ) || $r[ $field ] === '' || $r[ $field ] === null ) {
                $missing[] = $field;
            }
        }
        return $missing;
    }
}
