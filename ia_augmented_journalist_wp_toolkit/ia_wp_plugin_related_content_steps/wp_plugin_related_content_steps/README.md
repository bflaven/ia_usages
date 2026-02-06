# Related Content AI - Implementation Guide

## Overview

This solution provides AI-powered multilingual related content recommendations for WordPress using semantic similarity. It supports 15+ languages including Vietnamese, Portuguese, Chinese, Persian, Khmer, Romanian, Russian, Swahili, and Hausa.

## Architecture

```
WordPress ← → Python Processing ← → MySQL Database
   ↑                                      ↑
   └──────────── Direct DB Access ───────┘
```

### Key Components

1. **Python Backend**: Generates embeddings and computes similarities
2. **MySQL Database**: Stores embeddings and similarity scores
3. **WordPress Plugin**: Displays related content to users

## Prerequisites

- Python 3.8+
- MySQL 5.7+ or MariaDB 10.3+
- WordPress 5.0+
- 2GB+ RAM (for embedding model)
- 1GB+ disk space (for model cache)

## Installation Steps

### Step 1: Database Setup

1. Connect to your MySQL database:
```bash
mysql -u root -p wordpress
```

2. Execute the schema:
```bash
mysql -u wordpress_user -p wordpress_db < schema.sql
```

3. Verify tables were created:
```sql
SHOW TABLES LIKE 'wp_post_%';
```

### Step 2: Python Environment Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp config.env.template .env
```

4. Edit `.env` with your settings:
```env
DB_HOST=localhost
DB_NAME=wordpress
DB_USER=wp_user
DB_PASSWORD=your_password

WP_URL=https://your-site.com
EMBEDDING_MODEL=paraphrase-multilingual-mpnet-base-v2

MAX_CONTENT_LENGTH=1000
MIN_SIMILARITY_THRESHOLD=0.3
MAX_RELATED_POSTS=10
BATCH_SIZE=32
```

### Step 3: Initial Data Processing

#### Option A: Using WordPress REST API

1. Process all existing posts:
```bash
python main.py --action full
```

2. Process specific post:
```bash
python main.py --action process --post-id 123
```

3. Compute similarities only:
```bash
python main.py --action similarities
```

#### Option B: Using Sample Data (for POC)

1. Generate sample dataset:
```bash
python generate_sample_data.py
```

2. Import sample data to WordPress (manual step)

3. Process sample posts:
```bash
python main.py --action full --max-posts 20
```

### Step 4: WordPress Plugin Installation

1. Copy plugin folder:
```bash
cp -r wordpress-plugin/related-content-ai /path/to/wordpress/wp-content/plugins/
```

2. Activate plugin in WordPress admin:
   - Navigate to Plugins → Installed Plugins
   - Find "Related Content AI"
   - Click "Activate"

3. Configure plugin:
   - Go to Settings → Related Content AI
   - Adjust settings as needed
   - Check system status

### Step 5: Verification

1. Check embedding coverage:
```bash
python main.py --action query --post-id 1
```

2. View related posts in WordPress:
   - Open any single post
   - Related posts should appear automatically
   - Or use shortcode: `[related_posts]`

## Usage Examples

### Python CLI

```bash
# Process all posts
python main.py --action full

# Process posts in specific language
python main.py --action full --language fr

# Compute similarities for one post
python main.py --action similarities --post-id 123

# Query related posts
python main.py --action query --post-id 123

# Process limited number of posts (for testing)
python main.py --action process --max-posts 50
```

### WordPress Shortcode

```php
// Basic usage
[related_posts]

// With parameters
[related_posts limit="10" min_similarity="0.4"]

// For specific post
[related_posts post_id="123" limit="5"]
```

### WordPress Widget

1. Go to Appearance → Widgets
2. Add "Related Posts (AI)" widget to sidebar
3. Configure title, limit, and minimum similarity

### REST API

```bash
# Get related posts via API
curl https://your-site.com/wp-json/related-content-ai/v1/related/123

# With parameters
curl "https://your-site.com/wp-json/related-content-ai/v1/related/123?limit=10&min_similarity=0.4"
```

### Programmatic Usage

```php
// In theme or plugin
$plugin = Related_Content_AI::get_instance();
$related = $plugin->get_related_posts(123, 5, 0.3);

foreach ($related as $post) {
    echo '<a href="' . get_permalink($post->related_post_id) . '">';
    echo $post->post_title . ' (' . $post->similarity_score . ')';
    echo '</a>';
}
```

## Performance Optimization

### 1. Embedding Model Selection

Choose based on your priorities:

**Best Quality (Default)**:
```env
EMBEDDING_MODEL=paraphrase-multilingual-mpnet-base-v2
```

**Faster Processing**:
```env
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

**Maximum Language Support**:
```env
EMBEDDING_MODEL=LaBSE
```

### 2. Batch Processing

For large sites, process in batches:

```bash
# Process 100 posts at a time
python main.py --action process --max-posts 100

# Run multiple times or in cron
0 2 * * * cd /path/to/project && /path/to/venv/bin/python main.py --action full
```

### 3. Caching

Configure WordPress cache:
```php
// In wp-config.php or plugin settings
define('RCAI_CACHE_TTL', 7200); // 2 hours
```

### 4. Pre-computation

Pre-compute similarities (recommended):

```bash
# Compute all similarities overnight
python main.py --action similarities
```

Or compute on-demand (for new posts only):

```bash
# Add to post-publish hook
python main.py --action similarities --post-id $POST_ID
```

## Automation & Maintenance

### Automated Processing

Create a cron job to process new posts:

```bash
# /etc/cron.d/related-content-ai
# Process new posts daily at 2 AM
0 2 * * * www-data cd /var/www/html/related-content && /usr/bin/python3 main.py --action full

# Update similarities weekly on Sunday
0 3 * * 0 www-data cd /var/www/html/related-content && /usr/bin/python3 main.py --action similarities
```

### WordPress Hook Integration

Add to your theme's `functions.php`:

```php
// Process post on publish
add_action('publish_post', 'rcai_process_new_post');
function rcai_process_new_post($post_id) {
    // Call Python script
    $cmd = sprintf(
        'python3 /path/to/main.py --action process --post-id %d > /dev/null 2>&1 &',
        $post_id
    );
    exec($cmd);
}
```

### Database Maintenance

```sql
-- Clean up old embeddings for deleted posts
DELETE pe FROM wp_post_embeddings pe
LEFT JOIN wp_posts p ON pe.post_id = p.ID
WHERE p.ID IS NULL;

-- Clean up orphaned similarities
DELETE ps FROM wp_post_similarities ps
LEFT JOIN wp_posts p ON ps.source_post_id = p.ID
WHERE p.ID IS NULL;

-- Recompute for changed content
SELECT post_id FROM wp_post_embeddings 
WHERE updated_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

## Troubleshooting

### Common Issues

#### 1. No embeddings generated

**Check**: Python script execution
```bash
python main.py --action process --post-id 1
# Check logs: related_content.log
```

**Solution**: Ensure WordPress REST API is accessible
```bash
curl https://your-site.com/wp-json/wp/v2/posts/1
```

#### 2. Slow processing

**Check**: Model size and batch size
```bash
# Use smaller model
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Reduce batch size
BATCH_SIZE=16
```

#### 3. Language detection issues

**Check**: Content encoding
```python
# In embeddings.py, verify:
result = ContentProcessor.detect_language(text)
print(f"Detected: {result}")
```

#### 4. Low similarity scores

**Adjust**: Minimum threshold
```php
// In WordPress settings or .env
MIN_SIMILARITY_THRESHOLD=0.2
```

### Debug Mode

Enable detailed logging:

```python
# In main.py
logging.basicConfig(level=logging.DEBUG)
```

```php
// In WordPress
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
```

## Scaling Considerations

### For Large Sites (10,000+ posts)

1. **Use Queue System**:
```bash
# Install Celery for background processing
pip install celery redis

# Process in background
celery -A tasks worker --loglevel=info
```

2. **Database Optimization**:
```sql
-- Add additional indexes
CREATE INDEX idx_post_language ON wp_post_embeddings(language, post_id);
CREATE INDEX idx_similarity_range ON wp_post_similarities(similarity_score, source_post_id);
```

3. **Sharding by Language**:
```python
# Process each language separately
for lang in ['en', 'fr', 'es', 'de']:
    processor.compute_similarities(language=lang)
```

### For Multi-Server Setup

1. Centralized database for embeddings
2. Distributed processing with job queue
3. CDN caching for API responses

## Model Comparison

| Model | Dimension | Size | Speed | Languages | Best For |
|-------|-----------|------|-------|-----------|----------|
| mpnet-base | 768 | 1.1GB | Moderate | 50+ | Quality |
| MiniLM-L12 | 384 | 420MB | Fast | 50+ | Balance |
| distiluse | 512 | 500MB | Fast | 15+ | Speed |
| LaBSE | 768 | 1.9GB | Slow | 109 | Coverage |

## Testing

### Unit Tests

```bash
# Test database connection
python -c "from database import DatabaseManager; dm = DatabaseManager(config); print('OK')"

# Test embedding generation
python -c "from embeddings import EmbeddingGenerator; eg = EmbeddingGenerator(); print(eg.generate_embedding('test'))"

# Test similarity calculation
python -c "from embeddings import EmbeddingGenerator; eg = EmbeddingGenerator(); print(eg.cosine_similarity([1,0], [1,0]))"
```

### Integration Tests

```bash
# End-to-end test with sample data
python generate_sample_data.py
python main.py --action full --max-posts 20
python main.py --action query --post-id 1
```

## Advanced Features

### Custom Similarity Metrics

Modify `embeddings.py` to use different metrics:

```python
# Euclidean distance
def euclidean_similarity(emb1, emb2):
    distance = np.linalg.norm(emb1 - emb2)
    return 1 / (1 + distance)

# Dot product
def dot_product_similarity(emb1, emb2):
    return np.dot(emb1, emb2)
```

### Weighted Embeddings

Give more weight to titles:

```python
# In ContentProcessor.prepare_content()
combined_text = f"{clean_title} {clean_title} {clean_title} {clean_content}"
```

### Category-Based Filtering

Add category filtering:

```sql
-- In plugin, modify query
WHERE ps.source_post_id = %d
    AND ps.similarity_score >= %f
    AND p.post_status = 'publish'
    AND t.term_id IN (SELECT term_id FROM wp_term_relationships WHERE object_id = %d)
```

## Security Considerations

1. **Database Access**: Use read-only user for WordPress plugin
2. **API Authentication**: Protect REST endpoints if needed
3. **Input Validation**: Sanitize all user inputs
4. **Rate Limiting**: Limit API calls to prevent abuse

## License & Credits

- Sentence Transformers: Apache 2.0
- MySQL Connector: GPL v2
- WordPress Plugin: GPL v2

## Support & Contribution

For issues, questions, or contributions, please refer to the project repository.

## Changelog

### Version 1.0.0 (Initial Release)
- Multilingual semantic similarity
- WordPress plugin integration
- REST API support
- Caching system
- Admin dashboard
- Widget and shortcode support
