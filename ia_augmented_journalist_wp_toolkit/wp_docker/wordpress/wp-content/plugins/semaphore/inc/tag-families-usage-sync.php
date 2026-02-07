<?php
// inc/tag-families-usage-sync.php

add_action( 'set_object_terms', function( $object_id, $terms, $tt_ids, $taxonomy, $append, $old_tt_ids ) {
    if ( $taxonomy !== 'post_tag' ) {
        return;
    }

    global $wpdb;

    $all_tt_ids = array_unique( array_merge( (array) $tt_ids, (array) $old_tt_ids ) );
    if ( empty( $all_tt_ids ) ) {
        return;
    }

    $in = implode( ',', array_map( 'intval', $all_tt_ids ) );

    $sql = "
        UPDATE {$wpdb->prefix}tag_families f
        JOIN (
            SELECT tr.term_taxonomy_id,
                   COUNT(*) AS real_usage
            FROM {$wpdb->term_relationships} tr
            JOIN {$wpdb->posts} p ON p.ID = tr.object_id
            WHERE tr.term_taxonomy_id IN ($in)
              AND p.post_status = 'publish'
            GROUP BY tr.term_taxonomy_id
        ) x ON x.term_taxonomy_id = f.tag_id
        SET f.usage_count = x.real_usage
    ";
    $wpdb->query( $sql );
}, 10, 6 );

