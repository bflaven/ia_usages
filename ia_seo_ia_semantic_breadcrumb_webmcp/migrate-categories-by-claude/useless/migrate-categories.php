<?php
/**
 * migrate-categories.php
 *
 * WordPress category migration: old French/mixed taxonomy → new English SEO taxonomy.
 *
 * Usage (from WordPress root):
 *   wp eval-file migrate-categories.php
 *
 * Safe to run multiple times (idempotent).
 * Dry-run mode: set DRY_RUN to true to preview changes without writing anything.
 *
 * Author: Bruno / flaven.fr
 * Date:   2026
 */

define( 'DRY_RUN', false ); // Set to true to preview only, no DB writes

// ---------------------------------------------------------------------------
// 1. MAPPING: old slug => new category name
//    New categories are created automatically if they don't exist.
// ---------------------------------------------------------------------------
$CATEGORY_MAP = [

    // AI & Machine Learning
    'ai'                        => 'AI & Machine Learning',
    'nlp'                       => 'AI & Machine Learning',

    // APIs & Integration
    'api'                       => 'APIs & Integration',
    'json'                      => 'APIs & Integration',

    // Cloud & Infrastructure
    'cloud'                     => 'Cloud & Infrastructure',
    'hebergement'               => 'Cloud & Infrastructure',
    'linux-apache'              => 'Cloud & Infrastructure',

    // Data & Analytics
    'big-data'                  => 'Data & Analytics',
    'statistiques-et-tracking'  => 'Data & Analytics',

    // Journalism & Writing
    'meilleurs-blogs'           => 'Journalism & Writing',

    // Miscellaneous / Other
    'autres'                    => 'Miscellaneous / Other',
    'divers'                    => 'Miscellaneous / Other',
    'non-classe'                => 'Miscellaneous / Other',

    // Mobile & Devices
    'android'                   => 'Mobile & Devices',
    'ios'                       => 'Mobile & Devices',
    'iphone-mobile'             => 'Mobile & Devices',

    // Multimedia & Video
    'lencodage-des-medias'      => 'Multimedia & Video',
    'photo'                     => 'Multimedia & Video',
    'video'                     => 'Multimedia & Video',

    // Programming & Databases
    'developpement'             => 'Programming & Databases',
    'flash-actionscript-flex'   => 'Programming & Databases',
    'flex'                      => 'Programming & Databases',
    'framework'                 => 'Programming & Databases',
    'javascript-ajax'           => 'Programming & Databases',
    'mysql'                     => 'Programming & Databases',
    'php-mysql'                 => 'Programming & Databases',
    'python'                    => 'Programming & Databases',
    'ruby-on-rails'             => 'Programming & Databases',

    // SEO & Web Marketing
    'marketing-web'             => 'SEO & Web Marketing',
    'referencement-seo'         => 'SEO & Web Marketing',

    // Social Media & Community
    'reseaux-sociaux'           => 'Social Media & Community',
    'social-tv'                 => 'Social Media & Community',

    // Technology & Trends
    'google'                    => 'Technology & Trends',
    'hbbtv'                     => 'Technology & Trends',
    'technologie'               => 'Technology & Trends',
    'tv-connectee'              => 'Technology & Trends',

    // Tools & Productivity
    'agile'                     => 'Tools & Productivity',
    'mac'                       => 'Tools & Productivity',
    'saas'                      => 'Tools & Productivity',
    'widget-gadget'             => 'Tools & Productivity',

    // Tutorials & How-to
    'tutoriaux'                 => 'Tutorials & How-to',

    // UX & Product Design
    'accessibilite'             => 'UX & Product Design',
    'ux'                        => 'UX & Product Design',
    'wireframe-mock-up'         => 'UX & Product Design',

    // Web Design & Front-end
    'css3'                      => 'Web Design & Front-end',
    'html5'                     => 'Web Design & Front-end',
    'image-graphisme-photoshop' => 'Web Design & Front-end',
    'jquery'                    => 'Web Design & Front-end',
    'style'                     => 'Web Design & Front-end',
    'webdesign'                 => 'Web Design & Front-end',
    'webgl'                     => 'Web Design & Front-end',
    'xhtml-css'                 => 'Web Design & Front-end',

    // WordPress & CMS
    'cms'                       => 'WordPress & CMS',
    'drupal'                    => 'WordPress & CMS',
    'joomla-virtuemart'         => 'WordPress & CMS',
    'wordpress'                 => 'WordPress & CMS',

    // Business & Case Studies (kept, name unchanged)
    'business-case-studies'     => 'Business & Case Studies',
    'ecommerce'                 => 'Business & Case Studies',

    // Digital Storytelling & Webdocs (kept, name unchanged)
    'digital-storytelling-webdocs' => 'Digital Storytelling & Webdocs',

    // Web Development (kept, name unchanged)
    'creation-de-site-web'      => 'Web Development',
    'web-development'           => 'Web Development',
];

// ---------------------------------------------------------------------------
// 2. HELPER: get or create a category term by name, return term_id
// ---------------------------------------------------------------------------
function get_or_create_category( string $name ): int {
    $existing = get_term_by( 'name', $name, 'category' );
    if ( $existing ) {
        return (int) $existing->term_id;
    }
    if ( DRY_RUN ) {
        WP_CLI::log( "[DRY-RUN] Would create category: {$name}" );
        return 0;
    }
    $result = wp_insert_term( $name, 'category' );
    if ( is_wp_error( $result ) ) {
        WP_CLI::warning( "Could not create category '{$name}': " . $result->get_error_message() );
        return 0;
    }
    WP_CLI::success( "Created category: {$name} (ID {$result['term_id']})" );
    return (int) $result['term_id'];
}

// ---------------------------------------------------------------------------
// 3. PRE-CREATE all new categories and cache their IDs
// ---------------------------------------------------------------------------
WP_CLI::log( '=== Phase 1: Ensuring new categories exist ===' );

$new_cat_ids = []; // name => term_id
foreach ( array_unique( array_values( $CATEGORY_MAP ) ) as $new_name ) {
    $new_cat_ids[ $new_name ] = get_or_create_category( $new_name );
}

// ---------------------------------------------------------------------------
// 4. ITERATE all posts and reassign categories
// ---------------------------------------------------------------------------
WP_CLI::log( '' );
WP_CLI::log( '=== Phase 2: Reassigning post categories ===' );

$post_ids = get_posts( [
    'post_type'      => 'post',
    'post_status'    => 'any',
    'numberposts'    => -1,
    'fields'         => 'ids',
] );

$total        = count( $post_ids );
$changed      = 0;
$skipped      = 0;
$old_slugs_used = [];

WP_CLI::log( "Processing {$total} posts..." );

foreach ( $post_ids as $post_id ) {
    $old_terms = wp_get_post_categories( $post_id, [ 'fields' => 'all' ] );
    if ( empty( $old_terms ) ) {
        $skipped++;
        continue;
    }

    $new_term_ids  = [];
    $post_modified = false;

    foreach ( $old_terms as $term ) {
        $slug = $term->slug;

        if ( isset( $CATEGORY_MAP[ $slug ] ) ) {
            // This old category has a mapping
            $new_name   = $CATEGORY_MAP[ $slug ];
            $new_term_id = $new_cat_ids[ $new_name ] ?? 0;

            if ( $new_term_id ) {
                $new_term_ids[]        = $new_term_id;
                $old_slugs_used[ $slug ] = true;
                $post_modified         = true;
            } else {
                // DRY_RUN: keep a placeholder
                $new_term_ids[] = $term->term_id;
            }
        } else {
            // No mapping found: keep the existing term untouched
            $new_term_ids[] = $term->term_id;
        }
    }

    $new_term_ids = array_unique( $new_term_ids );

    if ( $post_modified ) {
        if ( ! DRY_RUN ) {
            wp_set_post_categories( $post_id, $new_term_ids );
        }
        $changed++;
    } else {
        $skipped++;
    }
}

WP_CLI::success( "Posts updated: {$changed} | Skipped (no old categories matched): {$skipped}" );

// ---------------------------------------------------------------------------
// 5. DELETE empty old categories (only slugs that were actually reassigned)
// ---------------------------------------------------------------------------
WP_CLI::log( '' );
WP_CLI::log( '=== Phase 3: Removing old empty categories ===' );

$deleted  = 0;
$not_empty = 0;

foreach ( array_keys( $old_slugs_used ) as $old_slug ) {
    $term = get_term_by( 'slug', $old_slug, 'category' );
    if ( ! $term ) continue;

    // Recount to be safe
    $count = (int) $term->count;
    if ( $count > 0 ) {
        WP_CLI::warning( "Category '{$old_slug}' still has {$count} posts — skipping deletion." );
        $not_empty++;
        continue;
    }

    if ( ! DRY_RUN ) {
        $result = wp_delete_term( $term->term_id, 'category' );
        if ( is_wp_error( $result ) ) {
            WP_CLI::warning( "Could not delete '{$old_slug}': " . $result->get_error_message() );
        } else {
            WP_CLI::log( "  Deleted: {$old_slug}" );
            $deleted++;
        }
    } else {
        WP_CLI::log( "[DRY-RUN] Would delete: {$old_slug}" );
        $deleted++;
    }
}

WP_CLI::success( "Categories deleted: {$deleted} | Non-empty (kept): {$not_empty}" );

// ---------------------------------------------------------------------------
// 6. FLUSH rewrite rules
// ---------------------------------------------------------------------------
WP_CLI::log( '' );
WP_CLI::log( '=== Phase 4: Flushing rewrite rules ===' );
if ( ! DRY_RUN ) {
    flush_rewrite_rules();
    WP_CLI::success( 'Rewrite rules flushed.' );
} else {
    WP_CLI::log( '[DRY-RUN] Would flush rewrite rules.' );
}

WP_CLI::log( '' );
WP_CLI::success( DRY_RUN ? 'Dry-run complete. No changes were written.' : 'Migration complete.' );
