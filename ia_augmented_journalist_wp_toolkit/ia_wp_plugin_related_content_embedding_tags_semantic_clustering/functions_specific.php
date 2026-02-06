<?php

/* -----------  // For IA ----------- */


/* ===========================================================================
   BF SEMANTIC SEO FEATURES
   
   Dependencies:
   - bf_wp_related_embeddings_db plugin (provides bf_get_related_posts)
   - bf_wp_tag_families_db plugin (provides bf_get_related_tags)
   
   Features:
   - Level 1: Semantic breadcrumbs, related content footer, sidebar widget
   - Level 2: Schema.org structured data (Breadcrumbs, Article, CollectionPage)
   
   Usage:
   - Breadcrumbs: Call bf_semantic_breadcrumbs() in your template
   - Sidebar: Auto-added OR use widget OR shortcode [bf_sidebar]
   - Footer: Auto-added via 'the_content' filter
   - Schema: Auto-added via 'wp_head' action
   =========================================================================== */

/* ===========================================================================
   LEVEL 1: BASIC SEMANTIC SEO FEATURES
   =========================================================================== */

// ============================================================================
// 1. SEMANTIC BREADCRUMBS
// Shows: Home › Canonical Tag › Current Tag › Post Title
// ============================================================================

/**
 * Display semantic breadcrumbs with tag hierarchy
 * 
 * Shows hierarchical navigation using tag families:
 * - On single posts: Home > Parent Tag > Tag > Post Title
 * - On tag archives: Home > Parent Tag > Current Tag
 * 
 * @return void Echoes HTML directly
 * 
 * Usage: Add to single.php or content-single.php:
 * <?php bf_semantic_breadcrumbs(); ?>
 */
function bf_semantic_breadcrumbs() {
    // Don't show breadcrumbs on front page
    if ( is_front_page() ) {
        return;
    }
    
    // Only show on single posts and tag archives
    if ( ! is_single() && ! is_tag() ) {
        return;
    }
    
    global $wpdb;
    
    echo '<div class="entry-breadcrumb">';
    echo '<nav class="bf-breadcrumbs" aria-label="Breadcrumb">';
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
 * Helper: Generate breadcrumbs for single post
 * 
 * @param object $wpdb WordPress database object
 * @return void Echoes HTML directly
 */
function bf_breadcrumbs_single_post( $wpdb ) {
    $tags = get_the_tags();
    
    if ( $tags ) {
        $first_tag = $tags[0];
        
        // Show canonical (parent) tag if exists and is different from current tag
        $canonical_tag = bf_get_canonical_tag( $wpdb, $first_tag->term_id );
        if ( $canonical_tag && $canonical_tag->term_id != $first_tag->term_id ) {
            echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
            echo esc_html( $canonical_tag->name );
            echo '</a> <span class="breadcrumb-separator">›</span> ';
        }
        
        // Show current post's primary tag
        echo '<a href="' . esc_url( get_tag_link( $first_tag->term_id ) ) . '">';
        echo esc_html( $first_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show current post title (not linked)
    echo '<span class="breadcrumb-current">' . esc_html( get_the_title() ) . '</span>';
}

/**
 * Helper: Generate breadcrumbs for tag archive page
 * 
 * @param object $wpdb WordPress database object
 * @return void Echoes HTML directly
 */
function bf_breadcrumbs_tag_archive( $wpdb ) {
    $current_tag = get_queried_object();
    
    // Show canonical (parent) tag if exists
    $canonical_tag = bf_get_canonical_tag( $wpdb, $current_tag->term_id );
    if ( $canonical_tag && $canonical_tag->term_id != $current_tag->term_id ) {
        echo '<a href="' . esc_url( get_tag_link( $canonical_tag->term_id ) ) . '">';
        echo esc_html( $canonical_tag->name );
        echo '</a> <span class="breadcrumb-separator">›</span> ';
    }
    
    // Show current tag (not linked)
    echo '<span class="breadcrumb-current">' . esc_html( $current_tag->name ) . '</span>';
}

/**
 * Helper: Get canonical (parent) tag for a given tag ID
 * 
 * Queries the tag_families table to find the canonical tag
 * that represents the parent topic cluster
 * 
 * @param object $wpdb WordPress database object
 * @param int $tag_id The tag ID to look up
 * @return object|null Tag object or null if not found
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
// 2. SIDEBAR WIDGET (Related Posts + Tags)
// Shows both related articles and related topics in sidebar
// Multiple integration options: Widget, Shortcode, or Auto-inject
// ============================================================================

/**
 * Semantic Sidebar Widget - Core Function
 * 
 * Displays:
 * - Related posts (5 most similar articles)
 * - Related tags (5 semantically similar topics)
 * 
 * Styled with Zaatar theme colors (#4F1993)
 * 
 * @return void Echoes HTML directly
 */
/**
 * Semantic Sidebar Widget - SUPER DEBUG VERSION
 */
function bf_semantic_sidebar() {
    if ( ! is_single() ) {
        echo '<div class="semantic-sidebar-widget"><p>⚠️ Not a single post page</p></div>';
        return;
    }
    
    global $post, $wpdb;
    
    ?>
    <div class="semantic-sidebar-widget">
        
        <!-- DEBUG INFO -->
        <div style="background: #fff3cd; padding: 10px; margin-bottom: 15px; border-left: 4px solid #ffc107; font-size: 12px;">
            <strong>🔍 Debug Info:</strong><br>
            Post ID: <?php echo $post->ID; ?><br>
            bf_get_related_posts exists: <?php echo function_exists('bf_get_related_posts') ? '✅ Yes' : '❌ No'; ?><br>
            bf_get_related_tags exists: <?php echo function_exists('bf_get_related_tags') ? '✅ Yes' : '❌ No'; ?><br>
            <?php
            $tags = get_the_tags();
            echo 'Post has tags: ' . ($tags ? '✅ Yes (' . count($tags) . ')' : '❌ No') . '<br>';
            
            if ($tags) {
                echo 'First tag ID: ' . $tags[0]->term_id . ' (' . $tags[0]->name . ')<br>';
            }
            
            // Check database directly
            $db_count = $wpdb->get_var($wpdb->prepare(
                "SELECT COUNT(*) FROM {$wpdb->prefix}related_posts_embeddings WHERE post_id = %d",
                $post->ID
            ));
            echo 'Related posts in DB for this post: ' . ($db_count ? $db_count : '0') . '<br>';
            
            if ($tags) {
                $tag_db_count = $wpdb->get_var($wpdb->prepare(
                    "SELECT COUNT(*) FROM {$wpdb->prefix}tag_families WHERE tag_id = %d",
                    $tags[0]->term_id
                ));
                echo 'Tag family data in DB: ' . ($tag_db_count ? '✅ Yes' : '❌ No') . '<br>';
            }
            ?>
        </div>
        
        <!-- Related Posts Section -->
        <?php if ( function_exists( 'bf_get_related_posts' ) ) : ?>
            <?php
            $related_posts = bf_get_related_posts( $post->ID, 5 );
            
            // Debug output
            echo '<div style="background: #e7f3ff; padding: 10px; margin-bottom: 10px; font-size: 11px;">';
            echo '<strong>Related Posts Debug:</strong><br>';
            echo 'Function returned type: ' . gettype($related_posts) . '<br>';
            if (is_array($related_posts)) {
                echo 'Array count: ' . count($related_posts) . '<br>';
                if (count($related_posts) > 0) {
                    echo 'First item keys: ' . implode(', ', array_keys($related_posts[0])) . '<br>';
                }
            } else {
                echo 'Return value: ' . var_export($related_posts, true) . '<br>';
            }
            echo '</div>';
            
            if ( $related_posts && is_array($related_posts) && count($related_posts) > 0 ) :
            ?>
                <div class="related-posts-section">
                    <h3>Related Articles (<?php echo count($related_posts); ?>)</h3>
                    <ul>
                        <?php foreach ( $related_posts as $related ) : ?>
                            <li>
                                <a href="<?php echo esc_url( $related['permalink'] ); ?>">
                                    <?php echo esc_html( $related['title'] ); ?>
                                </a>
                                <small class="similarity-score">
                                    (<?php echo number_format( $related['similarity'], 2 ); ?>)
                                </small>
                            </li>
                        <?php endforeach; ?>
                    </ul>
                </div>
            <?php else: ?>
                <div style="background: #f8d7da; padding: 10px; margin-bottom: 15px; border-left: 4px solid #dc3545;">
                    ⚠️ No related posts returned from bf_get_related_posts()<br>
                    <small>Check if post ID <?php echo $post->ID; ?> exists in wp_related_posts_embeddings table</small>
                </div>
            <?php endif; ?>
        <?php endif; ?>
        
        <!-- Related Tags Section -->
        <?php if ( function_exists( 'bf_get_related_tags' ) ) : ?>
            <?php
            $tags = get_the_tags();
            
            if ( $tags && is_array($tags) && count($tags) > 0 ) {
                $first_tag_id = $tags[0]->term_id;
                $related_tags = bf_get_related_tags( $first_tag_id, 5 );
                
                // Debug output
                echo '<div style="background: #e7f3ff; padding: 10px; margin-bottom: 10px; font-size: 11px;">';
                echo '<strong>Related Tags Debug:</strong><br>';
                echo 'First tag ID: ' . $first_tag_id . ' (' . $tags[0]->name . ')<br>';
                echo 'Function returned type: ' . gettype($related_tags) . '<br>';
                if (is_array($related_tags)) {
                    echo 'Array count: ' . count($related_tags) . '<br>';
                    if (count($related_tags) > 0) {
                        echo 'First item keys: ' . implode(', ', array_keys($related_tags[0])) . '<br>';
                    }
                } else {
                    echo 'Return value: ' . var_export($related_tags, true) . '<br>';
                }
                echo '</div>';
                
                if ( $related_tags && is_array($related_tags) && count($related_tags) > 0 ) :
                ?>
                    <div class="related-tags-section">
                        <h3>Explore Topics (<?php echo count($related_tags); ?>)</h3>
                        <div class="tag-cloud">
                            <?php foreach ( $related_tags as $tag ) : ?>
                                <a href="<?php echo esc_url( $tag['url'] ); ?>" class="tag-badge">
                                    <?php echo esc_html( $tag['name'] ); ?>
                                    <small>(<?php echo intval( $tag['count'] ); ?>)</small>
                                </a>
                            <?php endforeach; ?>
                        </div>
                    </div>
                <?php else: ?>
                    <div style="background: #f8d7da; padding: 10px; margin-bottom: 15px; border-left: 4px solid #dc3545;">
                        ⚠️ No related tags returned from bf_get_related_tags()<br>
                        <small>Check if tag ID <?php echo $first_tag_id; ?> exists in wp_tag_families table</small>
                    </div>
                <?php endif;
            }
            ?>
        <?php endif; ?>
        
    </div>
    
    <!-- Styles -->
    <style>
    .semantic-sidebar-widget {
        background: linear-gradient(135deg, #f8f5fc 0%, #ffffff 100%);
        padding: 25px;
        border-left: 5px solid #4F1993;
        margin-bottom: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(79, 25, 147, 0.08);
    }
    .semantic-sidebar-widget h3 {
        margin-top: 0;
        font-size: 19px;
        color: #4F1993;
        font-weight: 700;
        border-bottom: 3px solid #4F1993;
        padding-bottom: 12px;
        margin-bottom: 18px;
    }
    .semantic-sidebar-widget ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .semantic-sidebar-widget ul li {
        padding: 10px 0;
        border-bottom: 1px solid rgba(79, 25, 147, 0.1);
    }
    .semantic-sidebar-widget ul li a {
        color: #4F1993;
        text-decoration: none;
        font-weight: 500;
        font-size: 15px;
    }
    .semantic-sidebar-widget ul li a:hover {
        color: #6d2cc4;
        text-decoration: underline;
    }
    .semantic-sidebar-widget .similarity-score {
        color: #999;
        font-size: 11px;
    }
    .tag-badge {
        display: inline-block;
        padding: 7px 14px;
        margin: 4px;
        background: white;
        border: 2px solid #4F1993;
        border-radius: 20px;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        color: #4F1993;
        transition: all 0.3s ease;
    }
    .tag-badge:hover {
        background: #4F1993;
        color: white;
    }
    </style>
    <?php
}

/**
 * Register Shortcode for Sidebar Widget
 * 
 * Usage: Add [bf_sidebar] anywhere in content or use in widgets
 */
function bf_semantic_sidebar_shortcode( $atts ) {
    ob_start();
    bf_semantic_sidebar();
    return ob_start();
}
add_shortcode( 'bf_sidebar', 'bf_semantic_sidebar_shortcode' );

/**
 * Register as WordPress Widget
 * 
 * This allows adding the widget via Appearance > Widgets
 */
class BF_Semantic_Sidebar_Widget extends WP_Widget {
    
    /**
     * Constructor
     */
    public function __construct() {
        parent::__construct(
            'bf_semantic_sidebar_widget',
            'BF Semantic Sidebar',
            array( 
                'description' => 'Shows related posts and tags using semantic AI matching'
            )
        );
    }
    
    /**
     * Front-end display of widget
     */
    public function widget( $args, $instance ) {
        echo $args['before_widget'];
        bf_semantic_sidebar();
        echo $args['after_widget'];
    }
    
    /**
     * Back-end widget form (no options needed)
     */
    public function form( $instance ) {
        echo '<p>This widget automatically shows related content on single posts.</p>';
        echo '<p>No configuration needed.</p>';
    }
}

/**
 * Register the widget
 */
function bf_register_semantic_sidebar_widget() {
    register_widget( 'BF_Semantic_Sidebar_Widget' );
}
add_action( 'widgets_init', 'bf_register_semantic_sidebar_widget' );

/**
 * OPTIONAL: Auto-inject sidebar widget
 * 
 * Automatically adds the widget to the primary sidebar on single posts
 * Uncomment this if you want automatic injection without editing sidebar.php
 */
/*
function bf_auto_inject_sidebar_widget( $sidebars_widgets ) {
    if ( is_single() && ! is_admin() ) {
        // Get the primary sidebar (adjust 'sidebar-1' to match your theme)
        $sidebar_id = 'sidebar-1'; // Common IDs: sidebar-1, primary, main-sidebar
        
        if ( isset( $sidebars_widgets[ $sidebar_id ] ) ) {
            // Add our widget at the top of the sidebar
            array_unshift( $sidebars_widgets[ $sidebar_id ], 'bf_semantic_sidebar_widget' );
        }
    }
    return $sidebars_widgets;
}
add_filter( 'sidebars_widgets', 'bf_auto_inject_sidebar_widget' );
*/

// ============================================================================
// 3. AUTO-RELATED CONTENT IN POST FOOTER
// Automatically adds related posts and tags after post content
// ============================================================================

/**
 * Auto-add related content to single post footer
 * 
 * Appends to post content:
 * - 3 related posts with thumbnails
 * - 8 related tags in a tag cloud
 * 
 * @param string $content The post content
 * @return string Modified content with related items appended
 */
function bf_auto_related_content( $content ) {
    // Only on single posts in main query
    if ( ! is_single() || ! is_main_query() ) {
        return $content;
    }
    
    // Prevent infinite loop when rendering related post excerpts
    remove_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    global $post;
    $footer = '';
    
    // Render related posts section
    if ( function_exists( 'bf_get_related_posts' ) ) {
        $related_posts = bf_get_related_posts( $post->ID, 3 );
        if ( $related_posts ) {
            $footer .= bf_render_related_posts( $related_posts );
        }
    }
    
    // Render related tags section
    if ( function_exists( 'bf_get_related_tags' ) ) {
        $tags = get_the_tags();
        if ( $tags ) {
            $related_tags = bf_get_related_tags( $tags[0]->term_id, 8 );
            if ( $related_tags ) {
                $footer .= bf_render_related_tags( $related_tags );
            }
        }
    }
    
    // Restore filter for next post
    add_filter( 'the_content', 'bf_auto_related_content', 999 );
    
    // Wrap footer content if we have any
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
 * 
 * Creates a responsive grid of related post cards with:
 * - Featured image (if available)
 * - Post title
 * - Excerpt (trimmed to 15 words)
 * 
 * @param array $related_posts Array of related post data from plugin
 * @return string HTML markup for related posts grid
 */
function bf_render_related_posts( $related_posts ) {
    $html = '<h3 style="font-size: 24px; margin-bottom: 20px; color: #333;">Continue Reading</h3>';
    $html .= '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">';
    
    foreach ( $related_posts as $related ) {
        $html .= '<div style="border: 1px solid #ddd; border-radius: 8px; overflow: hidden; transition: transform 0.2s;">';
        
        // Featured image (if exists)
        if ( ! empty( $related['thumbnail'] ) ) {
            $html .= '<a href="' . esc_url( $related['permalink'] ) . '">';
            $html .= '<img src="' . esc_url( $related['thumbnail'] ) . '" ';
            $html .= 'style="width: 100%; height: 180px; object-fit: cover;" ';
            $html .= 'alt="' . esc_attr( $related['title'] ) . '">';
            $html .= '</a>';
        }
        
        // Post title and excerpt
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
 * 
 * Creates a tag cloud of semantically related topics
 * Shows tag name and post count for each tag
 * 
 * @param array $related_tags Array of related tag data from plugin
 * @return string HTML markup for related tags section
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

/* ===========================================================================
   LEVEL 2: STRUCTURED DATA (Schema.org JSON-LD)
   Adds rich snippets for better Google search appearance
   =========================================================================== */

// ============================================================================
// 4. BREADCRUMB SCHEMA (Rich Snippets in Google)
// Makes breadcrumbs appear in search results
// ============================================================================

/**
 * Schema.org BreadcrumbList for Google Rich Snippets
 * 
 * Adds JSON-LD structured data to show breadcrumb trail in Google search results.
 * Uses semantic tag families to build hierarchical navigation.
 * 
 * @return void Echoes JSON-LD script tag in <head>
 */
function bf_breadcrumb_schema() {
    // Only add schema on single posts and tag archives
    if ( ! is_single() && ! is_tag() ) {
        return;
    }
    
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
            
            // Get canonical (parent) tag from tag families table
            $canonical = $wpdb->get_row( $wpdb->prepare(
                "SELECT canonical_tag_id, canonical_label 
                 FROM {$wpdb->prefix}tag_families 
                 WHERE tag_id = %d 
                 LIMIT 1",
                $first_tag->term_id
            ) );
            
            // Add canonical tag to breadcrumb if it's different from current tag
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
            
            // Add current post's primary tag
            $items[] = array(
                '@type' => 'ListItem',
                'position' => $position++,
                'name' => $first_tag->name,
                'item' => get_tag_link( $first_tag->term_id )
            );
        }
        
        // Add current post (last item has no 'item' property per schema.org spec)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => get_the_title()
        );
        
    } elseif ( is_tag() ) {
        global $wpdb;
        $current_tag = get_queried_object();
        
        // Get canonical (parent) tag
        $canonical = $wpdb->get_row( $wpdb->prepare(
            "SELECT canonical_tag_id, canonical_label 
             FROM {$wpdb->prefix}tag_families 
             WHERE tag_id = %d 
             LIMIT 1",
            $current_tag->term_id
        ) );
        
        // Add canonical tag if this is a child tag
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
        
        // Add current tag (last item has no 'item' property)
        $items[] = array(
            '@type' => 'ListItem',
            'position' => $position,
            'name' => $current_tag->name
        );
    }
    
    // Build complete schema
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'BreadcrumbList',
        'itemListElement' => $items
    );
    
    // Output JSON-LD script in <head>
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_breadcrumb_schema' );

// ============================================================================
// 5. TAG ARCHIVE SCHEMA (CollectionPage for Topic Clusters)
// Helps Google understand topic cluster pages
// ============================================================================

/**
 * CollectionPage Schema for Tag Archives
 * 
 * Adds structured data to tag archive pages showing:
 * - Parent topic relationship
 * - Related tag pages
 * 
 * This helps Google understand your topic cluster structure.
 * 
 * @return void Echoes JSON-LD script tag in <head>
 */
function bf_tag_archive_schema() {
    // Only add on tag archive pages
    if ( ! is_tag() ) {
        return;
    }
    
    $current_tag = get_queried_object();
    global $wpdb;
    
    // Get tag family information
    $canonical = $wpdb->get_row( $wpdb->prepare(
        "SELECT canonical_tag_id, canonical_label 
         FROM {$wpdb->prefix}tag_families 
         WHERE tag_id = %d 
         LIMIT 1",
        $current_tag->term_id
    ) );
    
    // Get semantically related tags (limit to 8 for performance)
    $related_tags = array();
    if ( function_exists( 'bf_get_related_tags' ) ) {
        $related_tags_data = bf_get_related_tags( $current_tag->term_id, 8 );
        if ( $related_tags_data ) {
            foreach ( $related_tags_data as $tag ) {
                $related_tags[] = $tag['url'];
            }
        }
    }
    
    // Build base schema
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'CollectionPage',
        'name' => $current_tag->name . ' - ' . get_bloginfo( 'name' ),
        'description' => $current_tag->description ?: 'Articles about ' . $current_tag->name,
        'url' => get_tag_link( $current_tag->term_id )
    );
    
    // Add parent topic if this is a subtopic (not the canonical tag itself)
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
    
    // Add related tag pages
    if ( ! empty( $related_tags ) ) {
        $schema['relatedLink'] = $related_tags;
    }
    
    // Output JSON-LD script in <head>
    echo "\n" . '<script type="application/ld+json">' . "\n";
    echo json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n" . '</script>' . "\n";
}
add_action( 'wp_head', 'bf_tag_archive_schema', 20 );

/* ===========================================================================
   END BF SEMANTIC SEO FEATURES
   =========================================================================== */

   
/* -----------  // For IA ----------- */

?>
