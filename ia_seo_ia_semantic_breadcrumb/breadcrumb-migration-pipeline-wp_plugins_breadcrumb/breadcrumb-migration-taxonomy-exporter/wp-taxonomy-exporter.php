<?php
/**
 * Plugin Name: Breadcrumb Migration - Taxonomy Exporter
 * Description: Must be used the plugin breadcrumb-migration. It enables an export categories or post_tags to JSON/CSV with dry-run support. No security checks - pure functionality - NONCE FREE
 * Version: 1.4.0
 * Author: Bruno Flaven + Perplexity
 */



if (!defined('ABSPATH')) exit;

add_action('admin_menu', function() {
    add_submenu_page('options-general.php', 'Taxonomy Exporter', 'Tax Export', 'manage_options', 'tax-export-v4', 'TAX_EXPORT_V4_PAGE');
});

function TAX_EXPORT_V4_PAGE() {
    if (!current_user_can('manage_options')) {
        wp_die('❌ Admin access required');
    }
    
    $success = '';
    $error = '';
    $download_url = '';
    
    // Handle POST - NO NONCE CHECK
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['export_taxonomy'])) {
        $taxonomy = $_POST['taxonomy'] ?? 'category';
        $format = $_POST['format'] ?? 'csv';
        $limit = max(1, min(5000, intval($_POST['limit'] ?? 100)));
        $dry_run = isset($_POST['dry_run']);
        
        $terms = get_terms([
            'taxonomy' => in_array($taxonomy, ['category', 'post_tag']) ? $taxonomy : 'category',
            'hide_empty' => false,
            'number' => $limit
        ]);
        
        if (is_wp_error($terms)) {
            $error = 'Error fetching terms: ' . $terms->get_error_message();
        } else {
            $total = count($terms);
            $data = [];
            
            foreach ($terms as $term) {
                $data[] = [
                    'id' => intval($term->term_id),
                    'name' => $term->name,
                    'slug' => $term->slug,
                    'taxonomy' => $taxonomy,
                    'post_count' => intval($term->count),
                    'parent_id' => intval($term->parent)
                ];
            }
            
            if ($dry_run) {
                $success = "🧪 DRY RUN SUCCESS: {$total} terms processed";
            } else {
                // Generate filename
                $timestamp = current_time('Ymd\THisO');
                $filename = "{$taxonomy}_{$timestamp}_step_1_inventory.{$format}";
                $upload_dir = wp_upload_dir();
                $filepath = trailingslashit($upload_dir['path']) . $filename;
                
                // Create content
                $export_data = [
                    'timestamp' => current_time('c'),
                    'pipeline_step' => 'inventory',
                    'taxonomy' => $taxonomy,
                    'total_processed' => $total,
                    'config' => [
                        'limit' => $limit,
                        'dry_run' => false,
                        'taxonomy' => $taxonomy
                    ],
                    'data' => $data
                ];
                
                if ($format === 'json') {
                    $content = wp_json_encode($export_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
                } else {
                    $content = "taxonomy,id,name,slug,post_count,parent_id\n";
                    foreach ($data as $row) {
                        $name = str_replace('"', '""', $row['name']);
                        $content .= sprintf("%s,%d,\"%s\",%s,%d,%d\n", 
                            $row['taxonomy'], $row['id'], $name, $row['slug'], 
                            $row['post_count'], $row['parent_id']);
                    }
                }
                
                // Write file
                $bytes = file_put_contents($filepath, $content);
                if ($bytes !== false && $bytes > 0) {
                    $download_url = trailingslashit($upload_dir['url']) . $filename;
                    $success = "✅ SUCCESS! {$total} terms → " . $filename . " ({$bytes} bytes)";
                } else {
                    $error = "❌ Write failed. Path: " . $upload_dir['path'] . " | Writable: " . (is_writable($upload_dir['path']) ? 'YES' : 'NO');
                }
            }
        }
    }
    ?>
    
    <div class="wrap" style="max-width: 800px;">
        <h1>📊 Taxonomy Exporter v4.0 <small>(No security checks)</small></h1>
        
        <?php if ($success): ?>
            <div style="background: #d4edda; color: #155724; padding: 15px; border: 1px solid #c3e6cb; margin: 20px 0;">
                <strong><?php echo $success; ?></strong>
                <?php if ($download_url): ?>
                    <br><br>
                    <a href="<?php echo esc_url($download_url); ?>" target="_blank" 
                       class="button button-large button-primary" style="font-size: 16px;">
                        ⬇️ DOWNLOAD FILE NOW
                    </a>
                    <br><small><?php echo esc_html($download_url); ?></small>
                <?php endif; ?>
            </div>
        <?php endif; ?>
        
        <?php if ($error): ?>
            <div style="background: #f8d7da; color: #721c24; padding: 15px; border: 1px solid #f5c6cb; margin: 20px 0;">
                <strong><?php echo $error; ?></strong>
            </div>
        <?php endif; ?>
        
        <form method="POST" style="background: #f8f9fa; padding: 25px; border-radius: 8px;">
            <input type="hidden" name="export_taxonomy" value="1">
            
            <table class="form-table">
                <tr>
                    <th style="width: 150px;">Taxonomy</th>
                    <td>
                        <label><input type="radio" name="taxonomy" value="category" checked> 📁 Categories</label> &nbsp;
                        <label><input type="radio" name="taxonomy" value="post_tag"> 🏷️ Post Tags</label>
                    </td>
                </tr>
                <tr>
                    <th>Format</th>
                    <td>
                        <label><input type="radio" name="format" value="csv" checked> 📄 CSV</label> &nbsp;
                        <label><input type="radio" name="format" value="json"> 💾 JSON</label>
                    </td>
                </tr>
                <tr>
                    <th>Limit</th>
                    <td>
                        <input type="number" name="limit" value="100" min="1" max="5000" 
                               style="width: 120px; font-size: 16px; padding: 8px;">
                        <br><small>Terms to export (1-5000)</small>
                    </td>
                </tr>
                <tr>
                    <th>Dry Run</th>
                    <td>
                        <label>
                            <input type="checkbox" name="dry_run" value="1">
                            🧪 Test only (no file created)
                        </label>
                    </td>
                </tr>
            </table>
            
            <p style="margin-top: 25px;">
                <input type="submit" class="button button-hero button-primary" 
                       value="🚀 EXPORT TAXONOMY NOW" style="font-size: 18px; padding: 15px 30px;">
            </p>
        </form>
        
        <h3 style="margin-top: 40px;">📁 Recent Exports</h3>
        <div style="background: #f1f3f4; padding: 20px; border-radius: 5px;">
        <?php
        $files = glob(wp_upload_dir()['path'] . '/*step_1_inventory.*');
        if (empty($files)) {
            echo '<p>No export files found. First export creates one!</p>';
        } else {
            echo '<ul style="margin: 0;">';
            foreach (array_slice(array_reverse($files), 0, 10) as $file) {
                $url = wp_upload_dir()['url'] . '/' . basename($file);
                $size = number_format(filesize($file));
                $time = date('M j H:i', filemtime($file));
                printf('<li style="margin: 5px 0;">
                    <a href="%s" target="_blank">%s</a> 
                    <span style="color: #666;">(%s, %s bytes)</span>
                </li>', esc_url($url), basename($file), $time, $size);
            }
            echo '</ul>';
        }
        ?>
        </div>
    </div>
    <?php
}


