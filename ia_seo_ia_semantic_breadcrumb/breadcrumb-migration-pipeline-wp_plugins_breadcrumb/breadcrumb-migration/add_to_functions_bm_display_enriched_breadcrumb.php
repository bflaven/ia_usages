<?php


// add_to_functions_bm_display_enriched_breadcrumb.php

/* -----------  // Enrich breadcrumb for tag and category.
				See plugin breadcrumb-migration ----------- */
 /**
   * Version: 1.3.0
   * Plugin: breadcrumb-migration
   * Function: bm_display_enriched_breadcrumb
   * Display enriched breadcrumb for tag and category archive pages.
   *
   * Reads proposed_breadcrumb from wp_breadcrumb_proposals (validation_state
   * must be 'approved' or 'published'). Falls back to native WP parent chain
   * when no enriched data exists.
   *
   * v1.1.0: graceful no-table guard in bm_fetch_breadcrumb_crumbs().
   *         Intermediate crumbs now link to categories for post_tag too.
   * v1.2.0: intermediate crumb resolution falls back to WP page by slug
   *         so "Tags" links to /tags/ (custom page) when not a category.
   * v1.3.0: category lookup now tries slug after name to fix silent mismatches
   *         (accents, entity encoding, case). Page fallback unchanged.
   *
   * Usage in template:
   *   <?php bm_display_enriched_breadcrumb(); ?>

   */                                                       
  function bm_display_enriched_breadcrumb(): void {                               
      if ( ! is_tag() && ! is_category() ) {
          return;                                                                 
      }                                                     

      $term     = get_queried_object();                                           
      $taxonomy = $term->taxonomy; // 'post_tag' or 'category'
      $crumbs   = bm_fetch_breadcrumb_crumbs( (int) $term->term_id, $taxonomy );  
                                                                                  
      if ( empty( $crumbs ) ) {                                                   
          $crumbs = bm_native_breadcrumb_crumbs( $term, $taxonomy );              
      }                                                                           
   
      bm_breadcrumb_output( $crumbs, $taxonomy );                                 
  }                                                         

  /**
   * Query wp_breadcrumb_proposals for the enriched crumb array.
   *                                                                              
   * @return array  e.g. ["Home","Tags","17 octobre 1961"] or []
   */                                                                             
  function bm_fetch_breadcrumb_crumbs( int $wp_term_id, string $taxonomy ): array
  {
      global $wpdb;
      $pfx = $wpdb->prefix;

      // Guard: if plugin tables don't exist, skip query entirely.
      $table_exists = $wpdb->get_var( $wpdb->prepare(
          'SELECT COUNT(1) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s',
          DB_NAME,
          $pfx . 'breadcrumb_proposals'
      ) );
      if ( ! $table_exists ) {
          return [];
      }

      $json = $wpdb->get_var( $wpdb->prepare(                                     
          "SELECT p.proposed_breadcrumb                     
             FROM {$pfx}breadcrumb_proposals p                                    
             JOIN {$pfx}breadcrumb_terms t ON t.id = p.term_id
            WHERE t.wp_term_id = %d                                               
              AND t.taxonomy   = %s                         
              AND p.validation_state IN ('approved','published')                  
            LIMIT 1",                                                             
          $wp_term_id,
          $taxonomy                                                               
      ) );                                                  

      if ( ! $json ) {
          return [];
      }
      $arr = json_decode( $json, true );
      return is_array( $arr ) ? $arr : [];                                        
  }
                                                                                  
  /**                                                       
   * Build crumbs from native WP data when no proposal is found.
   * Category: walks parent chain. Tag: ["Home","Tags","Name"].                   
   */                                                                             
  function bm_native_breadcrumb_crumbs( WP_Term $term, string $taxonomy ): array {
      if ( $taxonomy === 'post_tag' ) {                                           
          return [ 'Home', 'Tags', $term->name ];           
      }                                                                           
                                                            
      // Walk category ancestors                                                  
      $chain = [ $term->name ];                             
      $parent_id = (int) $term->parent;                                           
      $seen      = [];                                                            
   
      while ( $parent_id && ! isset( $seen[ $parent_id ] ) ) {                    
          $seen[ $parent_id ] = true;                       
          $parent = get_term( $parent_id, 'category' );                           
          if ( ! $parent || is_wp_error( $parent ) ) {
              break;                                                              
          }                                                 
          array_unshift( $chain, $parent->name );                                 
          $parent_id = (int) $parent->parent;               
      }

      return array_merge( [ 'Home' ], $chain );                                   
  }
                                                                                  
  /**                                                       
   * Render the breadcrumb trail.
   * Home → link. Last crumb → current span. Middle → linked if resolvable.
   */                                                                             
  function bm_breadcrumb_output( array $crumbs, string $taxonomy ): void {        
      echo '<div class="entry-breadcrumb"><nav class="bf-breadcrumbs"             
  aria-label="Breadcrumbs">';                                                     
      echo '<span class="breadcrumb-icon"><i class="fas fa-map-marker-alt" 
  style="color: #4F1993;"></i></span>';                                           
                                                            
      $last = count( $crumbs ) - 1;                                               
                                                            
      foreach ( $crumbs as $i => $label ) {                                       
          if ( $i > 0 ) {
              echo '<span class="breadcrumb-separator">›</span>';                 
          }                                                 

          if ( $i === $last ) {                                                   
              echo '<span class="breadcrumb-current">' . esc_html( $label ) .
  '</span>';                                                                      
          } elseif ( $i === 0 ) {                           
              
              echo '<a href="' . esc_url( home_url( '/' ) ) . '" class="breadcrumb-link">' . esc_html( $label ) . '</a>';


          } else {
              // Resolve intermediate crumb — three attempts in order:
              //   1. WP category by name  (exact, case-insensitive)
              //   2. WP category by slug  (handles accents/entity mismatch)
              //   3. WP page by slug      ("Tags" → /tags/ custom page)
              $url = '';
              $cat = get_term_by( 'name', $label, 'category' );
              if ( ! $cat || is_wp_error( $cat ) ) {
                  $cat = get_term_by( 'slug', sanitize_title( $label ), 'category' );
              }
              if ( $cat && ! is_wp_error( $cat ) ) {
                  $url = get_category_link( $cat->term_id );
              } else {
                  $page = get_page_by_path( sanitize_title( $label ) );
                  if ( $page ) {
                      $url = get_permalink( $page->ID );
                  }
              }                                                                   
              if ( $url ) {                                 
                  

                  echo '<a href="' . esc_url( $url ) . '"  class="breadcrumb-link">' . esc_html( $label ) . '</a>'; 


              } else {
                  echo '<span class="breadcrumb-link">' . esc_html( $label ) .    
  '</span>';                                                                      
              }
          }                                                                       
      }                                                     

      echo '</nav></div>';
  }

/* -----------  // Enrich breadcrumb for tag and category. 
				See plugin breadcrumb-migration ----------- */




?>