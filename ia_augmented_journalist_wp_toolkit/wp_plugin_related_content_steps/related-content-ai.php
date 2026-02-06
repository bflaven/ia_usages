<?php
/**
 * Plugin Name: Related Content AI
 * Plugin URI: https://github.com/yourusername/related-content-ai
 * Description: AI-powered multilingual related content recommendations using semantic similarity
 * Version: 1.0.0
 * Author: Your Name
 * Author URI: https://yourwebsite.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: related-content-ai
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Plugin constants
define('RCAI_VERSION', '1.0.0');
define('RCAI_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('RCAI_PLUGIN_URL', plugin_dir_url(__FILE__));

/**
 * Main plugin class
 */
class Related_Content_AI {
    
    private static $instance = null;
    
    /**
     * Get singleton instance
     */
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    /**
     * Constructor
     */
    private function __construct() {
        $this->init_hooks();
    }
    
    /**
     * Initialize WordPress hooks
     */
    private function init_hooks() {
        // Activation/deactivation hooks
        register_activation_hook(__FILE__, array($this, 'activate'));
        register_deactivation_hook(__FILE__, array($this, 'deactivate'));
        
        // Add related posts to content
        add_filter('the_content', array($this, 'append_related_posts'));
        
        // Add shortcode
        add_shortcode('related_posts', array($this, 'related_posts_shortcode'));
        
        // Add widget
        add_action('widgets_init', array($this, 'register_widget'));
        
        // Admin menu
        add_action('admin_menu', array($this, 'add_admin_menu'));
        
        // REST API endpoint
        add_action('rest_api_init', array($this, 'register_rest_routes'));
        
        // Settings
        add_action('admin_init', array($this, 'register_settings'));
    }
    
    /**
     * Plugin activation
     */
    public function activate() {
        // Create tables (already done in schema.sql)
        // Set default options
        add_option('rcai_min_similarity', 0.3);
        add_option('rcai_max_posts', 5);
        add_option('rcai_cache_ttl', 3600);
        add_option('rcai_auto_display', true);
        add_option('rcai_display_position', 'bottom');
        
        flush_rewrite_rules();
    }
    
    /**
     * Plugin deactivation
     */
    public function deactivate() {
        flush_rewrite_rules();
    }
    
    /**
     * Get related posts from database
     */
    public function get_related_posts($post_id, $limit = 5, $min_similarity = 0.3) {
        global $wpdb;
        
        // Check cache first
        $cache_key = "rcai_related_{$post_id}_{$limit}_{$min_similarity}";
        $cached = wp_cache_get($cache_key, 'related_content_ai');
        
        if (false !== $cached) {
            return $cached;
        }
        
        // Query database
        $table = $wpdb->prefix . 'post_similarities';
        
        $query = $wpdb->prepare(
            "SELECT 
                ps.related_post_id,
                ps.similarity_score,
                p.post_title,
                p.post_name,
                p.post_date
            FROM {$table} ps
            INNER JOIN {$wpdb->posts} p ON ps.related_post_id = p.ID
            WHERE ps.source_post_id = %d
                AND ps.similarity_score >= %f
                AND p.post_status = 'publish'
            ORDER BY ps.similarity_score DESC
            LIMIT %d",
            $post_id,
            $min_similarity,
            $limit
        );
        
        $results = $wpdb->get_results($query);
        
        // Cache results
        $cache_ttl = get_option('rcai_cache_ttl', 3600);
        wp_cache_set($cache_key, $results, 'related_content_ai', $cache_ttl);
        
        return $results;
    }
    
    /**
     * Append related posts to content
     */
    public function append_related_posts($content) {
        // Only for single posts
        if (!is_single()) {
            return $content;
        }
        
        // Check if auto-display is enabled
        if (!get_option('rcai_auto_display', true)) {
            return $content;
        }
        
        $post_id = get_the_ID();
        $related_html = $this->render_related_posts($post_id);
        
        $position = get_option('rcai_display_position', 'bottom');
        
        if ('top' === $position) {
            return $related_html . $content;
        } else {
            return $content . $related_html;
        }
    }
    
    /**
     * Render related posts HTML
     */
    public function render_related_posts($post_id, $limit = null, $min_similarity = null) {
        if (null === $limit) {
            $limit = get_option('rcai_max_posts', 5);
        }
        
        if (null === $min_similarity) {
            $min_similarity = get_option('rcai_min_similarity', 0.3);
        }
        
        $related_posts = $this->get_related_posts($post_id, $limit, $min_similarity);
        
        if (empty($related_posts)) {
            return '';
        }
        
        ob_start();
        ?>
        <div class="related-content-ai">
            <h3 class="related-posts-title"><?php _e('Related Articles', 'related-content-ai'); ?></h3>
            <ul class="related-posts-list">
                <?php foreach ($related_posts as $related): ?>
                    <li class="related-post-item" data-similarity="<?php echo esc_attr($related->similarity_score); ?>">
                        <a href="<?php echo esc_url(get_permalink($related->related_post_id)); ?>" 
                           class="related-post-link">
                            <?php echo esc_html($related->post_title); ?>
                        </a>
                        <span class="related-post-meta">
                            <?php echo esc_html(human_time_diff(strtotime($related->post_date), current_time('timestamp'))); ?> 
                            <?php _e('ago', 'related-content-ai'); ?>
                            <?php if (current_user_can('manage_options')): ?>
                                <span class="similarity-score">(<?php echo number_format($related->similarity_score, 2); ?>)</span>
                            <?php endif; ?>
                        </span>
                    </li>
                <?php endforeach; ?>
            </ul>
        </div>
        <?php
        return ob_get_clean();
    }
    
    /**
     * Shortcode handler
     */
    public function related_posts_shortcode($atts) {
        $atts = shortcode_atts(array(
            'limit' => 5,
            'min_similarity' => 0.3,
            'post_id' => get_the_ID()
        ), $atts);
        
        return $this->render_related_posts(
            intval($atts['post_id']),
            intval($atts['limit']),
            floatval($atts['min_similarity'])
        );
    }
    
    /**
     * Register widget
     */
    public function register_widget() {
        register_widget('RCAI_Related_Posts_Widget');
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_options_page(
            __('Related Content AI', 'related-content-ai'),
            __('Related Content AI', 'related-content-ai'),
            'manage_options',
            'related-content-ai',
            array($this, 'admin_page')
        );
    }
    
    /**
     * Admin settings page
     */
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1><?php _e('Related Content AI Settings', 'related-content-ai'); ?></h1>
            
            <form method="post" action="options.php">
                <?php
                settings_fields('rcai_settings');
                do_settings_sections('related-content-ai');
                submit_button();
                ?>
            </form>
            
            <hr>
            
            <h2><?php _e('System Status', 'related-content-ai'); ?></h2>
            <?php $this->display_system_status(); ?>
        </div>
        <?php
    }
    
    /**
     * Display system status
     */
    private function display_system_status() {
        global $wpdb;
        
        $embeddings_table = $wpdb->prefix . 'post_embeddings';
        $similarities_table = $wpdb->prefix . 'post_similarities';
        
        $total_posts = $wpdb->get_var("SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_status = 'publish' AND post_type = 'post'");
        $posts_with_embeddings = $wpdb->get_var("SELECT COUNT(*) FROM {$embeddings_table}");
        $total_similarities = $wpdb->get_var("SELECT COUNT(*) FROM {$similarities_table}");
        
        ?>
        <table class="widefat">
            <tr>
                <td><?php _e('Total Published Posts', 'related-content-ai'); ?></td>
                <td><strong><?php echo number_format($total_posts); ?></strong></td>
            </tr>
            <tr>
                <td><?php _e('Posts with Embeddings', 'related-content-ai'); ?></td>
                <td><strong><?php echo number_format($posts_with_embeddings); ?></strong></td>
            </tr>
            <tr>
                <td><?php _e('Coverage', 'related-content-ai'); ?></td>
                <td><strong><?php echo $total_posts > 0 ? number_format(($posts_with_embeddings / $total_posts) * 100, 1) : 0; ?>%</strong></td>
            </tr>
            <tr>
                <td><?php _e('Total Similarity Relationships', 'related-content-ai'); ?></td>
                <td><strong><?php echo number_format($total_similarities); ?></strong></td>
            </tr>
        </table>
        <?php
    }
    
    /**
     * Register settings
     */
    public function register_settings() {
        register_setting('rcai_settings', 'rcai_min_similarity');
        register_setting('rcai_settings', 'rcai_max_posts');
        register_setting('rcai_settings', 'rcai_cache_ttl');
        register_setting('rcai_settings', 'rcai_auto_display');
        register_setting('rcai_settings', 'rcai_display_position');
        
        add_settings_section(
            'rcai_general',
            __('General Settings', 'related-content-ai'),
            null,
            'related-content-ai'
        );
        
        add_settings_field(
            'rcai_min_similarity',
            __('Minimum Similarity Score', 'related-content-ai'),
            array($this, 'min_similarity_callback'),
            'related-content-ai',
            'rcai_general'
        );
        
        add_settings_field(
            'rcai_max_posts',
            __('Maximum Related Posts', 'related-content-ai'),
            array($this, 'max_posts_callback'),
            'related-content-ai',
            'rcai_general'
        );
        
        add_settings_field(
            'rcai_cache_ttl',
            __('Cache TTL (seconds)', 'related-content-ai'),
            array($this, 'cache_ttl_callback'),
            'related-content-ai',
            'rcai_general'
        );
        
        add_settings_field(
            'rcai_auto_display',
            __('Auto Display', 'related-content-ai'),
            array($this, 'auto_display_callback'),
            'related-content-ai',
            'rcai_general'
        );
        
        add_settings_field(
            'rcai_display_position',
            __('Display Position', 'related-content-ai'),
            array($this, 'display_position_callback'),
            'related-content-ai',
            'rcai_general'
        );
    }
    
    public function min_similarity_callback() {
        $value = get_option('rcai_min_similarity', 0.3);
        echo '<input type="number" step="0.01" min="0" max="1" name="rcai_min_similarity" value="' . esc_attr($value) . '" />';
        echo '<p class="description">' . __('Minimum similarity score (0-1) to show related posts', 'related-content-ai') . '</p>';
    }
    
    public function max_posts_callback() {
        $value = get_option('rcai_max_posts', 5);
        echo '<input type="number" min="1" max="20" name="rcai_max_posts" value="' . esc_attr($value) . '" />';
        echo '<p class="description">' . __('Maximum number of related posts to display', 'related-content-ai') . '</p>';
    }
    
    public function cache_ttl_callback() {
        $value = get_option('rcai_cache_ttl', 3600);
        echo '<input type="number" min="0" name="rcai_cache_ttl" value="' . esc_attr($value) . '" />';
        echo '<p class="description">' . __('Time in seconds to cache related posts (0 = no cache)', 'related-content-ai') . '</p>';
    }
    
    public function auto_display_callback() {
        $value = get_option('rcai_auto_display', true);
        echo '<input type="checkbox" name="rcai_auto_display" value="1" ' . checked($value, true, false) . ' />';
        echo '<label>' . __('Automatically display related posts on single post pages', 'related-content-ai') . '</label>';
    }
    
    public function display_position_callback() {
        $value = get_option('rcai_display_position', 'bottom');
        echo '<select name="rcai_display_position">';
        echo '<option value="top" ' . selected($value, 'top', false) . '>' . __('Above content', 'related-content-ai') . '</option>';
        echo '<option value="bottom" ' . selected($value, 'bottom', false) . '>' . __('Below content', 'related-content-ai') . '</option>';
        echo '</select>';
    }
    
    /**
     * Register REST API routes
     */
    public function register_rest_routes() {
        register_rest_route('related-content-ai/v1', '/related/(?P<id>\d+)', array(
            'methods' => 'GET',
            'callback' => array($this, 'rest_get_related'),
            'permission_callback' => '__return_true',
            'args' => array(
                'id' => array(
                    'required' => true,
                    'type' => 'integer'
                ),
                'limit' => array(
                    'default' => 5,
                    'type' => 'integer'
                ),
                'min_similarity' => array(
                    'default' => 0.3,
                    'type' => 'number'
                )
            )
        ));
    }
    
    /**
     * REST API callback
     */
    public function rest_get_related($request) {
        $post_id = $request->get_param('id');
        $limit = $request->get_param('limit');
        $min_similarity = $request->get_param('min_similarity');
        
        $related_posts = $this->get_related_posts($post_id, $limit, $min_similarity);
        
        $formatted = array();
        foreach ($related_posts as $post) {
            $formatted[] = array(
                'id' => $post->related_post_id,
                'title' => $post->post_title,
                'link' => get_permalink($post->related_post_id),
                'slug' => $post->post_name,
                'date' => $post->post_date,
                'similarity' => floatval($post->similarity_score)
            );
        }
        
        return new WP_REST_Response($formatted, 200);
    }
}

/**
 * Widget class
 */
class RCAI_Related_Posts_Widget extends WP_Widget {
    
    public function __construct() {
        parent::__construct(
            'rcai_related_posts',
            __('Related Posts (AI)', 'related-content-ai'),
            array('description' => __('Display AI-powered related posts', 'related-content-ai'))
        );
    }
    
    public function widget($args, $instance) {
        if (!is_single()) {
            return;
        }
        
        echo $args['before_widget'];
        
        if (!empty($instance['title'])) {
            echo $args['before_title'] . apply_filters('widget_title', $instance['title']) . $args['after_title'];
        }
        
        $plugin = Related_Content_AI::get_instance();
        echo $plugin->render_related_posts(
            get_the_ID(),
            isset($instance['limit']) ? intval($instance['limit']) : 5,
            isset($instance['min_similarity']) ? floatval($instance['min_similarity']) : 0.3
        );
        
        echo $args['after_widget'];
    }
    
    public function form($instance) {
        $title = !empty($instance['title']) ? $instance['title'] : __('Related Articles', 'related-content-ai');
        $limit = !empty($instance['limit']) ? $instance['limit'] : 5;
        $min_similarity = !empty($instance['min_similarity']) ? $instance['min_similarity'] : 0.3;
        ?>
        <p>
            <label for="<?php echo esc_attr($this->get_field_id('title')); ?>"><?php _e('Title:', 'related-content-ai'); ?></label>
            <input class="widefat" id="<?php echo esc_attr($this->get_field_id('title')); ?>" 
                   name="<?php echo esc_attr($this->get_field_name('title')); ?>" type="text" 
                   value="<?php echo esc_attr($title); ?>">
        </p>
        <p>
            <label for="<?php echo esc_attr($this->get_field_id('limit')); ?>"><?php _e('Number of posts:', 'related-content-ai'); ?></label>
            <input class="tiny-text" id="<?php echo esc_attr($this->get_field_id('limit')); ?>" 
                   name="<?php echo esc_attr($this->get_field_name('limit')); ?>" type="number" 
                   value="<?php echo esc_attr($limit); ?>" min="1" max="10">
        </p>
        <p>
            <label for="<?php echo esc_attr($this->get_field_id('min_similarity')); ?>"><?php _e('Min similarity:', 'related-content-ai'); ?></label>
            <input class="small-text" id="<?php echo esc_attr($this->get_field_id('min_similarity')); ?>" 
                   name="<?php echo esc_attr($this->get_field_name('min_similarity')); ?>" type="number" 
                   value="<?php echo esc_attr($min_similarity); ?>" step="0.01" min="0" max="1">
        </p>
        <?php
    }
    
    public function update($new_instance, $old_instance) {
        $instance = array();
        $instance['title'] = (!empty($new_instance['title'])) ? sanitize_text_field($new_instance['title']) : '';
        $instance['limit'] = (!empty($new_instance['limit'])) ? intval($new_instance['limit']) : 5;
        $instance['min_similarity'] = (!empty($new_instance['min_similarity'])) ? floatval($new_instance['min_similarity']) : 0.3;
        return $instance;
    }
}

// Initialize plugin
Related_Content_AI::get_instance();
