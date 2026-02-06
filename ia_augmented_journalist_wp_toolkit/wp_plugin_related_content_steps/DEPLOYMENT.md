# Deployment Guide & Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          WordPress Installation                      │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐        ┌──────────────────┐                   │
│  │   wp-content/   │        │   MySQL/MariaDB  │                   │
│  │    plugins/     │◄──────►│                  │                   │
│  │ related-content │        │  wp_posts        │                   │
│  │     -ai/        │        │  wp_post_        │                   │
│  └─────────────────┘        │   embeddings     │                   │
│          ▲                  │  wp_post_        │                   │
│          │                  │   similarities   │                   │
│          │                  └──────────────────┘                   │
└──────────┼───────────────────────────▲──────────────────────────────┘
           │                           │
           │ Display                   │ Read/Write
           │ Related Posts             │
           │                           │
┌──────────┼───────────────────────────┼──────────────────────────────┐
│          │      Python Backend       │                              │
├──────────┼───────────────────────────┼──────────────────────────────┤
│  ┌───────▼────────┐     ┌────────────▼─────────┐                   │
│  │  main.py       │────►│  database.py         │                   │
│  │  (Orchestrator)│     │  (MySQL Operations)  │                   │
│  └────────┬───────┘     └──────────────────────┘                   │
│           │                                                          │
│  ┌────────▼───────────────────────────────┐                        │
│  │  embeddings.py                         │                        │
│  │  ┌─────────────────┐  ┌──────────────┐ │                        │
│  │  │ EmbeddingGen    │  │ Content      │ │                        │
│  │  │ - Vectorization │  │ Processor    │ │                        │
│  │  │ - Similarity    │  │ - Clean HTML │ │                        │
│  │  └─────────────────┘  │ - Lang Detect│ │                        │
│  │                        └──────────────┘ │                        │
│  └────────────────────────────────────────┘                        │
│           │                                                          │
│  ┌────────▼─────────────────────────────────────┐                  │
│  │  sentence-transformers Library               │                  │
│  │  Model: paraphrase-multilingual-mpnet-base   │                  │
│  └──────────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Embedding Generation Flow

```
New Post Published
    │
    ▼
WordPress REST API
    │
    ▼
Python: main.py
    │
    ├──► ContentProcessor
    │    ├─ Clean HTML
    │    ├─ Detect Language
    │    └─ Create Hash
    │
    ├──► EmbeddingGenerator
    │    ├─ Load Model
    │    ├─ Generate Vector (768-dim)
    │    └─ Normalize
    │
    └──► DatabaseManager
         └─ Store in wp_post_embeddings
```

### 2. Similarity Computation Flow

```
All Posts with Embeddings
    │
    ▼
Load All Vectors from DB
    │
    ▼
Compute Pairwise Similarity Matrix
    │  (Cosine Similarity)
    │
    ▼
For Each Post:
    ├─ Filter by Threshold (>0.3)
    ├─ Sort by Score DESC
    ├─ Keep Top N (10)
    └─ Store in wp_post_similarities
```

### 3. Display Flow

```
User Views Post
    │
    ▼
WordPress Plugin
    │
    ├──► Check Cache
    │    └─ Cache Miss
    │
    ├──► Query Database
    │    SELECT FROM wp_post_similarities
    │    WHERE source_post_id = X
    │    ORDER BY similarity_score DESC
    │    LIMIT 5
    │
    ├──► Render HTML
    │
    └──► Cache Result (1 hour)
```

## Deployment Options

### Option 1: Same Server (Recommended for Small Sites)

**Setup**:
```
Server
├── /var/www/html/                    (WordPress)
│   └── wp-content/plugins/
│       └── related-content-ai/       (Plugin)
│
├── /opt/related-content/             (Python Backend)
│   ├── venv/
│   ├── main.py
│   ├── database.py
│   └── embeddings.py
│
└── MySQL/MariaDB                     (Database)
```

**Processing**:
- Cron job runs Python scripts
- Direct database access
- Low latency

### Option 2: Separate Processing Server (Recommended for Large Sites)

**Setup**:
```
Web Server                           Processing Server
├── WordPress                        ├── Python Backend
├── Plugin                           ├── Sentence Transformers
└── MySQL (read-only)                ├── GPU (optional)
         ▲                           └── MySQL (read-write)
         │                                   │
         └───────── Network ────────────────┘
```

**Benefits**:
- Dedicated resources for processing
- No impact on web server performance
- Can use GPU acceleration
- Horizontal scaling possible

### Option 3: Cloud/Serverless (Advanced)

**Setup**:
```
WordPress (Web Host)
    │
    ▼
Cloud Function / Lambda
    │
    ├──► Vector Database (Pinecone/Weaviate)
    └──► Cache (Redis)
```

## Deployment Steps

### Production Deployment

#### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Install MySQL client
sudo apt install mysql-client -y

# Create application user
sudo useradd -r -s /bin/bash -d /opt/related-content relatedcontent
sudo mkdir -p /opt/related-content
sudo chown relatedcontent:relatedcontent /opt/related-content
```

#### 2. Application Setup

```bash
# Switch to app user
sudo su - relatedcontent

# Clone or copy application files
cd /opt/related-content
# (Copy your files here)

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config.env.template .env
nano .env  # Edit with production settings
```

#### 3. Database Setup

```bash
# Create production database
mysql -u root -p <<EOF
CREATE DATABASE wordpress_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'relatedcontent'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT SELECT, INSERT, UPDATE, DELETE ON wordpress_prod.* TO 'relatedcontent'@'localhost';
FLUSH PRIVILEGES;
EOF

# Load schema
mysql -u relatedcontent -p wordpress_prod < schema.sql
```

#### 4. Initial Processing

```bash
# Test connection
python main.py --action query --post-id 1

# Process all posts (this will take time)
nohup python main.py --action full > processing.log 2>&1 &

# Monitor progress
tail -f processing.log
```

#### 5. WordPress Plugin Installation

```bash
# Copy plugin
sudo cp -r wordpress-plugin/related-content-ai /var/www/html/wp-content/plugins/

# Set permissions
sudo chown -R www-data:www-data /var/www/html/wp-content/plugins/related-content-ai

# Activate in WordPress admin
# Navigate to Plugins → Installed Plugins → Activate
```

#### 6. Automation Setup

Create cron jobs for automated processing:

```bash
# Edit crontab
sudo crontab -u relatedcontent -e

# Add these lines:
# Process new posts every hour
0 * * * * cd /opt/related-content && /opt/related-content/venv/bin/python main.py --action process >> /var/log/related-content/hourly.log 2>&1

# Recompute all similarities daily at 2 AM
0 2 * * * cd /opt/related-content && /opt/related-content/venv/bin/python main.py --action similarities >> /var/log/related-content/daily.log 2>&1

# Clean old logs weekly
0 3 * * 0 find /var/log/related-content/ -name "*.log" -mtime +30 -delete
```

#### 7. Monitoring Setup

```bash
# Create log directory
sudo mkdir -p /var/log/related-content
sudo chown relatedcontent:relatedcontent /var/log/related-content

# Setup logrotate
sudo cat > /etc/logrotate.d/related-content <<EOF
/var/log/related-content/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 relatedcontent relatedcontent
}
EOF
```

#### 8. Performance Tuning

**MySQL Optimization**:
```sql
-- Add covering indexes
CREATE INDEX idx_post_similarity_lookup 
ON wp_post_similarities (source_post_id, similarity_score DESC, related_post_id);

-- Configure InnoDB buffer pool
SET GLOBAL innodb_buffer_pool_size = 1073741824; -- 1GB
```

**WordPress Caching**:
```php
// In wp-config.php
define('WP_CACHE', true);
define('RCAI_CACHE_TTL', 7200); // 2 hours
```

**Python Process Pool** (for large sites):
```python
# In main.py, use multiprocessing
from multiprocessing import Pool

def process_batch(posts):
    with Pool(processes=4) as pool:
        pool.map(process_single_post, posts)
```

## Security Considerations

### 1. Database Security

```sql
-- Separate read/write users
CREATE USER 'relatedcontent_read'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT ON wordpress_prod.wp_posts TO 'relatedcontent_read'@'localhost';
GRANT SELECT ON wordpress_prod.wp_post_embeddings TO 'relatedcontent_read'@'localhost';
GRANT SELECT ON wordpress_prod.wp_post_similarities TO 'relatedcontent_read'@'localhost';

-- WordPress plugin uses read-only user
UPDATE wp_config SET db_user = 'relatedcontent_read' WHERE context = 'plugin';
```

### 2. File Permissions

```bash
# Restrict access to config
chmod 600 /opt/related-content/.env

# Restrict Python files
chmod 755 /opt/related-content/*.py

# Secure logs
chmod 640 /var/log/related-content/*.log
```

### 3. Network Security

```bash
# If using separate servers, use SSH tunneling
ssh -L 3306:localhost:3306 processing-server

# Or configure MySQL to accept connections only from specific IPs
```

## Monitoring & Alerting

### Key Metrics to Monitor

1. **Processing Metrics**:
   - Posts processed per hour
   - Average processing time
   - Error rate

2. **Database Metrics**:
   - Table sizes
   - Query performance
   - Index usage

3. **Application Metrics**:
   - Memory usage
   - CPU usage
   - Disk usage

### Monitoring Script

```bash
#!/bin/bash
# /opt/related-content/monitor.sh

# Check embeddings coverage
coverage=$(mysql -u relatedcontent -pPASSWORD -D wordpress_prod -N -e "
SELECT ROUND(100.0 * COUNT(DISTINCT pe.post_id) / COUNT(DISTINCT p.ID), 2)
FROM wp_posts p
LEFT JOIN wp_post_embeddings pe ON p.ID = pe.post_id
WHERE p.post_status = 'publish' AND p.post_type = 'post';
")

echo "Embedding coverage: $coverage%"

# Alert if coverage drops below 90%
if (( $(echo "$coverage < 90" | bc -l) )); then
    echo "WARNING: Low embedding coverage"
    # Send alert (email, Slack, etc.)
fi
```

## Backup Strategy

### Database Backup

```bash
#!/bin/bash
# Backup embeddings and similarities daily

mysqldump -u relatedcontent -p wordpress_prod \
    wp_post_embeddings wp_post_similarities \
    | gzip > /backups/related-content-$(date +%Y%m%d).sql.gz

# Keep only last 30 days
find /backups/ -name "related-content-*.sql.gz" -mtime +30 -delete
```

### Application Backup

```bash
# Backup configuration and code
tar -czf /backups/related-content-app-$(date +%Y%m%d).tar.gz \
    /opt/related-content/ \
    --exclude=venv/ \
    --exclude=__pycache__/
```

## Scaling Strategies

### Vertical Scaling (Single Server)

1. **Increase RAM**: Improves model loading and caching
2. **Add GPU**: 5-10x faster embedding generation
3. **SSD Storage**: Faster database operations

### Horizontal Scaling (Multiple Servers)

1. **Distribute by Language**:
   ```bash
   # Server 1: Process English/French
   python main.py --action full --language en
   
   # Server 2: Process Asian languages
   python main.py --action full --language zh
   ```

2. **Load Balancing**:
   - Use queue system (RabbitMQ, Redis Queue)
   - Multiple workers process queue
   - Distribute load across servers

3. **Database Replication**:
   - Master-slave setup
   - Read replicas for WordPress
   - Master for Python processing

## Troubleshooting

### Common Production Issues

1. **Out of Memory**:
   ```bash
   # Reduce batch size
   BATCH_SIZE=8
   
   # Or use model swap
   EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
   ```

2. **Slow Processing**:
   ```bash
   # Check MySQL performance
   EXPLAIN SELECT * FROM wp_post_similarities WHERE source_post_id = 123;
   
   # Add missing indexes
   CREATE INDEX idx_missing ON wp_post_similarities(source_post_id, similarity_score);
   ```

3. **High CPU Usage**:
   ```bash
   # Limit concurrent processing
   nice -n 10 python main.py --action full
   ```

## Health Check Endpoint

Add to WordPress plugin:

```php
// In related-content-ai.php
add_action('rest_api_init', function() {
    register_rest_route('related-content-ai/v1', '/health', array(
        'methods' => 'GET',
        'callback' => 'rcai_health_check',
        'permission_callback' => '__return_true'
    ));
});

function rcai_health_check() {
    global $wpdb;
    
    $health = array(
        'status' => 'healthy',
        'embeddings_count' => $wpdb->get_var("SELECT COUNT(*) FROM wp_post_embeddings"),
        'similarities_count' => $wpdb->get_var("SELECT COUNT(*) FROM wp_post_similarities"),
        'timestamp' => current_time('mysql')
    );
    
    return new WP_REST_Response($health, 200);
}
```

## Success Criteria

### Pre-Production Checklist

- [ ] All dependencies installed
- [ ] Database schema created
- [ ] Initial embeddings generated
- [ ] Similarities computed
- [ ] WordPress plugin activated
- [ ] Cron jobs configured
- [ ] Monitoring setup
- [ ] Backups configured
- [ ] Security hardened
- [ ] Performance tested
- [ ] Documentation complete

### Post-Deployment Validation

- [ ] Query related posts successfully
- [ ] Check embedding coverage > 95%
- [ ] Verify cross-language matches
- [ ] Test WordPress display
- [ ] Monitor performance for 24h
- [ ] Verify cron job execution
- [ ] Test backup restoration
- [ ] Load test (if applicable)
