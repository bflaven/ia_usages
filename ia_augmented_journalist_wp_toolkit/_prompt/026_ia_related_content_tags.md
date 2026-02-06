



- Take example on the main color theme zaatar e.g #4F1993 for bf_semantic_sidebar();
- Can you change the code for sidebar if the sidebar.php does not exists





## PROMPT_2
As Wordpress expert, can you 
1. Keep the comment and if you add some code, add comments with best practices so we document code.
1. clean the code, verify that there is no duplicate
2. add the sidebar widget

Note :  I want to cut and paste the code so I want it easy





```php
/* -----------  // For IA ----------- */

/******************** LEVEL_1 ********************/

/* ===========================================================================
   BF SEMANTIC SEO FEATURES
   Requires: bf_wp_related_embeddings_db plugin
   =========================================================================== */

// ============================================================================
// 1. SEMANTIC BREADCRUMBS
// ============================================================================

/**
 * Display semantic breadcrumbs with tag hierarchy
 * Called directly in template: template-parts/content-single.php
 */
function bf_semantic_breadcrumbs() {
    // Don't show on front page
    if ( is_front_page() ) {
        return;
    }
    
    // Only show on single posts and tag archives
    if ( ! is_single() && ! is_tag() ) {
        return;
    }
    
    global $wpdb;
    
    echo '<div class="entry-breadcrumb">';
    echo '<nav class="bf-breadcrumbs">';
    echo '<span class="breadcrumb-icon">📍</span> ';
    echo '<a href="' . esc_url( home_url() ) . '">Home</a>';
    echo ' <span class="breadcrumb-separator">›</span> ';
    
    if ( is_single() ) {
        bf_breadcrumbs_single_post( $wpdb );
    } elseif ( is_tag() ) {
        bf_breadcrumbs_tag_archive( $wpdb );
    }
    
    echo '</nav>';
    echo '</div>';
}

/**
 * Helper: Breadcrumbs for single post
 */
function bf_breadcrumbs_single_post( $wpdb ) {
    $tags = get_the_tags();
    
    if ( $tags ) {
        $first_tag = $tags[0];
        
        // Show canonical tag if exists
        $canonical_tag = bf_get_canonical_tag( $wpdb, $first_tag->term_id );
        if ( $canonical_tag && $canonical_tag->term_id != $first_tag->term_id ) {
            echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
            echo esc_html( $canonical_tag->name );
            echo '</a> <span class="breadcrumb-separator">›</span> ';
        }
        
        // Show current tag
        echo '<a href="' . esc_url( get_tag_link( $first_tag->term_id ) ) . '">';
        echo esc_html( $first_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show post title
    echo '<span class="breadcrumb-current">' . esc_html( get_the_title() ) . '</span>';
}

/**
 * Helper: Breadcrumbs for tag archive
 */
function bf_breadcrumbs_tag_archive( $wpdb ) {
    $current_tag = get_queried_object();
    
    // Show canonical tag if exists
    $canonical_tag = bf_get_canonical_tag( $wpdb, $current_tag->term_id );
    if ( $canonical_tag && $canonical_tag->term_id != $current_tag->term_id ) {
        echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
        echo esc_html( $canonical_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show current tag
    echo '<span class="breadcrumb-current">' . esc_html( $current_tag->name ) . '</span>';
}


/**
 * Helper: Get canonical tag for a given tag ID
 */
function bf_get_canonical_tag( $wpdb, $tag_id ) {
    $canonical = $wpdb->get_row( $wpdb->prepare(
        "SELECT canonical_tag_id 
         FROM {$wpdb->prefix}tag_families 
         WHERE tag_id = %d 
         LIMIT 1",
        $tag_id
    ) );
    
    if ( $canonical && $canonical->canonical_tag_id ) {
        return get_tag( $canonical->canonical_tag_id );
    }
    
    return null;
}

// ============================================================================
// 2. AUTO-RELATED CONTENT IN POST FOOTER
// ============================================================================

/**
 * Add related posts and tags to single post footer
 * Uses bf_get_related_posts() and bf_get_related_tags() from plugin
 */
function bf_auto_related_content( $content ) {
    // Only on single posts in main query
    if ( ! is_single() || ! is_main_query() ) {
        return $content;
    }
    
    // Prevent infinite loop
    remove_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    global $post;
    $footer = '';
    
    // Get related posts
    if ( function_exists( 'bf_get_related_posts' ) ) {
        $related_posts = bf_get_related_posts( $post->ID, 3 );
        if ( $related_posts ) {
            $footer .= bf_render_related_posts( $related_posts );
        }
    }
    
    // Get related tags
    if ( function_exists( 'bf_get_related_tags' ) ) {
        $tags = get_the_tags();
        if ( $tags ) {
            $related_tags = bf_get_related_tags( $tags[0]->term_id, 8 );
            if ( $related_tags ) {
                $footer .= bf_render_related_tags( $related_tags );
            }
        }
    }
    
    // Restore filter
    add_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    // Wrap and return
    if ( $footer ) {
        $footer = '<div class="bf-post-footer" style="margin-top: 50px; padding-top: 30px; border-top: 2px solid #eee;">' 
                . $footer 
                . '</div>';
    }
    
    return $content . $footer;
}
add_filter( 'the_content', 'bf_auto_related_content', 999 );

/**
 * Helper: Render related posts HTML
 */
function bf_render_related_posts( $related_posts ) {
    $html = '<h3 style="font-size: 24px; margin-bottom: 20px; color: #333;">Continue Reading</h3>';
    $html .= '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">';
    
    foreach ( $related_posts as $related ) {
        $html .= '<div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; transition: transform 0.2s;">';
        
        // Thumbnail
        if ( ! empty( $related['thumbnail'] ) ) {
            $html .= '<a href="' . esc_url( $related['permalink'] ) . '">';
            $html .= '<img src="' . esc_url( $related['thumbnail'] ) . '" style="width: 100%; height: 180px; object-fit: cover;" alt="' . esc_attr( $related['title'] ) . '">';
            $html .= '</a>';
        }
        
        // Content
        $html .= '<div style="padding: 20px;">';
        $html .= '<h4 style="font-size: 18px; margin: 0 0 10px 0; line-height: 1.4;">';
        $html .= '<a href="' . esc_url( $related['permalink'] ) . '" style="text-decoration: none; color: #333;">';
        $html .= esc_html( $related['title'] );
        $html .= '</a></h4>';
        $html .= '<p style="font-size: 14px; color: #666; margin: 0;">';
        $html .= esc_html( wp_trim_words( $related['excerpt'], 15 ) );
        $html .= '</p>';
        $html .= '</div>';
        
        $html .= '</div>';
    }
    
    $html .= '</div>';
    return $html;
}

/**
 * Helper: Render related tags HTML
 */
function bf_render_related_tags( $related_tags ) {
    $html = '<div style="background: #f9f9f9; padding: 20px; border-radius: 8px;">';
    $html .= '<h4 style="font-size: 16px; color: #666; margin: 0 0 15px 0;">Explore Related Topics</h4>';
    
    foreach ( $related_tags as $tag ) {
        $html .= '<a href="' . esc_url( $tag['url'] ) . '" ';
        $html .= 'style="display: inline-block; padding: 8px 15px; margin: 5px 5px 5px 0; ';
        $html .= 'background: white; border: 1px solid #ddd; border-radius: 4px; ';
        $html .= 'text-decoration: none; font-size: 14px; color: #0073aa; transition: all 0.2s;">';
        $html .= esc_html( $tag['name'] );
        $html .= ' <small style="color: #999;">(' . intval( $tag['count'] ) . ')</small>';
        $html .= '</a>';
    }
    
    $html .= '</div>';
    return $html;
}

/******************** // LEVEL_1 ********************/

/******************** // LEVEL_2 ********************/


/**
 * LEVEL 2: Schema.org BreadcrumbList for Google Rich Snippets
 * Adds JSON-LD structured data for breadcrumbs
 */
function bf_breadcrumb_schema() {
    if ( ! is_single() && ! is_tag() ) return;
    
    $items = array();
    $position = 1;
    
    // Always start with Home
    $items[] = array(
        '@type' => 'ListItem',
        'position' => $position++,
        'name' => 'Home',
        'item' => home_url()
    );
    
    if ( is_single() ) {
        global $post, $wpdb;
        
        $tags = get_the_tags();
        if ( $tags ) {
            $first_tag = $tags[0];
            
            // Get canonical tag from tag families
            $canonical = $wpdb->get_row( $wpdb->prepare(
                "SELECT canonical_tag_id, canonical_label 
                 FROM {$wpdb->prefix}tag_families 
                 WHERE tag_id = %d LIMIT 1",
                $first_tag->term_id
            ) );
            
            // Add canonical tag if it's different from current tag
            if ( $canonical && $canonical->canonical_tag_id != $first_tag->term_id ) {
                $canonical_tag = get_tag( $canonical->canonical_tag_id );
                if ( $canonical_tag ) {
                    $items[] = array(
                        '@type' => 'ListItem',
                        'position' => $position++,
                        'name' => $canonical_tag->name,
                        'item' => get_tag_link( $canonical_tag->term_id )
                    );
                }
            }
            
            // Add current tag
            $items[] = array(
                '@type' => 'ListItem',
                'position' => $position++,
                'name' => $first_tag->name,
                'item' => get_tag_link( $first_tag->term_id )
            );
        }
        
        // Add current post (no 'item' for last element)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => get_the_title()
        );
        
    } elseif ( is_tag() ) {
        global $wpdb;
        $current_tag = get_queried_object();
        
        // Get canonical tag
        $canonical = $wpdb->get_row( $wpdb->prepare(
            "SELECT canonical_tag_id, canonical_label 
             FROM {$wpdb->prefix}tag_families 
             WHERE tag_id = %d LIMIT 1",
            $current_tag->term_id
        ) );
        
        // Add canonical tag if different
        if ( $canonical && $canonical->canonical_tag_id != $current_tag->term_id ) {
            $canonical_tag = get_tag( $canonical->canonical_tag_id );
            if ( $canonical_tag ) {
                $items[] = array(
                    '@type' => 'ListItem',
                    'position' => $position++,
                    'name' => $canonical_tag->name,
                    'item' => get_tag_link( $canonical_tag->term_id )
                );
            }
        }
        
        // Add current tag (no 'item' for last element)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => $current_tag->name
        );
    }
    
    // Build schema
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'BreadcrumbList',
        'itemListElement' => $items
    );
    
    // Output as JSON-LD in <head>
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_breadcrumb_schema' );


/**
 * LEVEL 2: CollectionPage Schema for Tag Archives
 * Helps Google understand your topic cluster pages
 */
function bf_tag_archive_schema() {
    if ( ! is_tag() ) return;
    
    $current_tag = get_queried_object();
    global $wpdb;
    
    // Get tag family info
    $canonical = $wpdb->get_row( $wpdb->prepare(
        "SELECT canonical_tag_id, canonical_label 
         FROM {$wpdb->prefix}tag_families 
         WHERE tag_id = %d LIMIT 1",
        $current_tag->term_id
    ) );
    
    // Get related tags
    $related_tags = bf_get_related_tags( $current_tag->term_id, 10 );
    $related_urls = array();
    
    if ( $related_tags ) {
        foreach ( $related_tags as $tag ) {
            $related_urls[] = $tag['url'];
        }
    }
    
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'CollectionPage',
        'name' => $current_tag->name . ' - ' . get_bloginfo( 'name' ),
        'description' => $current_tag->description ?: 'Articles about ' . $current_tag->name,
        'url' => get_tag_link( $current_tag->term_id )
    );
    
    // Add parent topic if this is a subtopic
    if ( $canonical && $canonical->canonical_tag_id != $current_tag->term_id ) {
        $canonical_tag = get_tag( $canonical->canonical_tag_id );
        if ( $canonical_tag ) {
            $schema['isPartOf'] = array(
                '@type' => 'CollectionPage',
                'name' => $canonical_tag->name,
                'url' => get_tag_link( $canonical_tag->term_id )
            );
        }
    }
    
    // Add related pages
    if ( ! empty( $related_urls ) ) {
        $schema['relatedLink'] = $related_urls;
    }
    
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_tag_archive_schema', 20 );


/******************** // LEVEL_2 ********************/
/* -----------  // For IA ----------- */
```

