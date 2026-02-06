<?php
/**
 * Template Name: SEO Blog Page
 * Description: Displays blog posts with featured images, excerpts, and metadata.
 * The template for displaying blog posts.
 *
 * @package Zaatar
 */

get_header(); ?>

<style>
.blog-posts-wrapper {
    margin-top: 30px;
}

.blog-post-item {
    margin-bottom: 50px;
    padding-bottom: 40px;
    border-bottom: 1px solid #e8ddf5;
}

.blog-post-item:last-child {
    border-bottom: none;
}

.blog-post-thumbnail {
    margin-bottom: 20px;
    overflow: hidden;
    border-radius: 8px;
}

.blog-post-thumbnail img {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.3s ease;
}

.blog-post-thumbnail:hover img {
    transform: scale(1.05);
}

.blog-post-header {
    margin-bottom: 15px;
}

.blog-post-title {
    font-size: 28px;
    margin-bottom: 10px;
    line-height: 1.3;
}

.blog-post-title a {
    color: #2a2a2a;
    text-decoration: none;
    transition: color 0.2s;
}

.blog-post-title a:hover {
    color: #4f1993;
}

.blog-post-meta {
    font-size: 14px;
    color: #666;
    margin-bottom: 15px;
}

.blog-post-meta span {
    margin-right: 15px;
}

.blog-post-meta a {
    color: #666;
    text-decoration: none;
    transition: color 0.2s;
}

.blog-post-meta a:hover {
    color: #4f1993;
}

.blog-post-excerpt {
    font-size: 16px;
    line-height: 1.6;
    color: #444;
    margin-bottom: 15px;
}

.blog-post-categories {
    margin-bottom: 15px;
}

.blog-post-categories a {
    display: inline-block;
    margin: 0 8px 8px 0;
    padding: 6px 14px;
    background: #f3eef9;
    color: #4f1993;
    border-radius: 6px;
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: background 0.2s, color 0.2s;
}

.blog-post-categories a:hover {
    background: #4f1993;
    color: #fff;
}

.blog-read-more {
    display: inline-block;
    padding: 10px 24px;
    background: #4f1993;
    color: #fff !important;
    text-decoration: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    transition: background 0.2s;
}

.blog-read-more:visited {
    background: #4f1993;
    color: #fff !important;
}

.blog-read-more:hover {
    background: #6b2bb8;
    color: #fff !important;
}

.blog-pagination {
    margin-top: 40px;
    margin-bottom: 40px;
    text-align: center;
    clear: both;
}

.blog-pagination .page-numbers {
    display: inline-block;
    margin: 0 5px;
    padding: 10px 16px;
    background: #f3eef9;
    color: #4f1993 !important;
    text-decoration: none;
    border-radius: 6px;
    font-size: 15px;
    font-weight: 500;
    transition: background 0.2s, color 0.2s;
    border: none;
}

.blog-pagination .page-numbers:hover,
.blog-pagination .page-numbers.current {
    background: #4f1993;
    color: #fff !important;
}

.blog-pagination .page-numbers.dots {
    background: transparent;
    color: #4f1993 !important;
    cursor: default;
}

.blog-pagination .page-numbers.dots:hover {
    background: transparent;
    color: #4f1993 !important;
}

.blog-no-posts {
    text-align: center;
    padding: 60px 20px;
    background: #f3eef9;
    border-radius: 8px;
}

.blog-no-posts p {
    font-size: 18px;
    color: #4f1993;
}
</style>

<div class="page-header-wrapper page-header-wrapper-archive">
    <div class="container">
        <div class="row">
            <div class="col">
                <header class="page-header">
                    <h1 class="page-title">Blog</h1>
                    <div class="taxonomy-description">
                        <!-- <p>Découvrez nos derniers articles et actualités</p> -->
                    </div>
                </header><!-- .page-header -->
            </div><!-- .col -->
        </div><!-- .row -->
    </div><!-- .container -->
</div><!-- .page-header-wrapper -->

<div class="site-content-inside">
    <div class="container">
        <div class="row">
            <div id="primary" class="content-area <?php allium_layout_class( 'content' ); ?>">
                <main id="main" class="site-main" role="main">
                    <div class="blog-posts-wrapper">
                        <?php
                        // Query blog posts
                        $paged = ( get_query_var( 'paged' ) ) ? get_query_var( 'paged' ) : 1;
                        
                        $blog_query = new WP_Query( array(
                            'post_type'      => 'post',
                            'post_status'    => 'publish',
                            'posts_per_page' => 10, // Number of posts per page
                            'paged'          => $paged,
                            'orderby'        => 'date',
                            'order'          => 'DESC'
                        ) );

                        if ( $blog_query->have_posts() ) :
                            while ( $blog_query->have_posts() ) : $blog_query->the_post();
                        ?>
                                <article id="post-<?php the_ID(); ?>" <?php post_class( 'blog-post-item' ); ?>>
                                    
                                    <?php if ( has_post_thumbnail() ) : ?>
                                        <div class="blog-post-thumbnail">
                                            <a href="<?php the_permalink(); ?>">
                                                <?php the_post_thumbnail( 'large' ); ?>
                                            </a>
                                        </div>
                                    <?php endif; ?>

                                    <header class="blog-post-header">
                                        <h2 class="blog-post-title">
                                            <a href="<?php the_permalink(); ?>">
                                                <?php the_title(); ?>
                                            </a>
                                        </h2>

                                        <div class="blog-post-meta">
                                            <span class="post-date">
                                                <i class="fa fa-calendar"></i>
                                                <?php echo get_the_date(); ?>
                                            </span>
                                            <span class="post-author">
                                                <i class="fa fa-user"></i>
                                                <a href="<?php echo esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ); ?>">
                                                    <?php the_author(); ?>
                                                </a>
                                            </span>
                                            <?php if ( comments_open() || get_comments_number() ) : ?>
                                                <span class="post-comments">
                                                    <i class="fa fa-comments"></i>
                                                    <?php comments_number( '0 commentaire', '1 commentaire', '% commentaires' ); ?>
                                                </span>
                                            <?php endif; ?>
                                        </div>
                                    </header>

                                    <?php
                                    $categories = get_the_category();
                                    if ( ! empty( $categories ) ) :
                                    ?>
                                        <div class="blog-post-categories">
                                            <?php foreach ( $categories as $category ) : ?>
                                                <a href="<?php echo esc_url( get_category_link( $category->term_id ) ); ?>">
                                                    <?php echo esc_html( $category->name ); ?>
                                                </a>
                                            <?php endforeach; ?>
                                        </div>
                                    <?php endif; ?>

                                    <div class="blog-post-excerpt">
                                        <?php the_excerpt(); ?>
                                    </div>

                                    <!-- <a href="<?php the_permalink(); ?>" class="blog-read-more">
                                        Lire la suite &rarr;
                                    </a> -->

                                </article><!-- .blog-post-item -->
                        <?php
                            endwhile;

                            // Pagination
                            ?>
                            <div class="blog-pagination">
                                <?php
                                echo paginate_links( array(
                                    'total'        => $blog_query->max_num_pages,
                                    'current'      => $paged,
                                    'prev_text'    => '&laquo; Précédent',
                                    'next_text'    => 'Suivant &raquo;',
                                    'type'         => 'plain',
                                    'mid_size'     => 2,
                                    'end_size'     => 1,
                                ) );
                                ?>
                            </div>
                            <?php

                            wp_reset_postdata();
                        else :
                        ?>
                            <div class="blog-no-posts">
                                <p>Aucun article trouvé.</p>
                            </div>
                        <?php
                        endif;
                        ?>
                    </div><!-- .blog-posts-wrapper -->
                </main><!-- #main -->
            </div><!-- #primary -->
            <?php get_sidebar(); ?>
        </div><!-- .row -->
    </div><!-- .container -->
</div><!-- .site-content-inside -->

<?php get_footer(); ?>