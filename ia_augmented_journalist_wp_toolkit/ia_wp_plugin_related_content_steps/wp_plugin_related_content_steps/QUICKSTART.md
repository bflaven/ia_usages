# Quick Start Guide - POC Testing

This guide will help you set up and test the related content system in 15 minutes.

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python3 --version

# Check MySQL access
mysql --version

# Check pip
pip3 --version
```

## Step 1: Setup (5 minutes)

### 1.1 Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

**Expected**: All packages install successfully. This may take 2-3 minutes.

### 1.2 Configure Database

```bash
# Copy configuration template
cp config.env.template .env

# Edit .env file with your database credentials
nano .env  # or use your preferred editor
```

**Required settings**:
```env
DB_HOST=localhost
DB_NAME=wordpress
DB_USER=your_user
DB_PASSWORD=your_password
WP_URL=http://your-site.com
```

### 1.3 Create Database Tables

```bash
# Connect to MySQL
mysql -u your_user -p your_database < schema.sql
```

**Verify**:
```bash
mysql -u your_user -p -e "SHOW TABLES LIKE 'wp_post_%'" your_database
```

**Expected output**:
```
wp_post_embeddings
wp_post_similarities
```

## Step 2: Generate Test Data (2 minutes)

```bash
# Generate sample posts
python generate_sample_data.py
```

**Expected**: Creates `sample_posts.json` with 20 multilingual posts.

**Output should show**:
```
Sample dataset saved to sample_posts.json

Dataset Summary:
--------------------------------------------------
Total posts: 20

Posts by language:
  en: 8
  fr: 4
  vi: 2
  pt: 1
  ...
```

## Step 3: Process Sample Data (5 minutes)

### Option A: Direct Processing (Recommended for POC)

```bash
# This processes sample data directly without WordPress
python test_poc.py
```

See `test_poc.py` script below.

### Option B: Via WordPress API

```bash
# Process all posts from WordPress
python main.py --action full --max-posts 20

# Check logs
tail -f related_content.log
```

## Step 4: Test Results (3 minutes)

### 4.1 Query Related Posts

```bash
# Get related posts for post ID 1
python main.py --action query --post-id 1
```

**Expected output**:
```
Related posts for ID 1:
--------------------------------------------------------------------------------
ID: 4
Title: Élections présidentielles américaines 2024
Score: 0.867
Language: fr
Date: 2024-11-07 11:00:00
--------------------------------------------------------------------------------
ID: 2
Title: American Electoral College System Explained
Score: 0.743
Language: en
...
```

### 4.2 Check Database

```sql
-- Connect to MySQL
mysql -u your_user -p your_database

-- Check embeddings
SELECT COUNT(*) as total_embeddings FROM wp_post_embeddings;

-- Check similarities
SELECT COUNT(*) as total_similarities FROM wp_post_similarities;

-- View top similarities
SELECT 
    source_post_id, 
    related_post_id, 
    ROUND(similarity_score, 3) as score
FROM wp_post_similarities 
ORDER BY similarity_score DESC 
LIMIT 10;
```

**Expected**:
- total_embeddings: ~20 (one per post)
- total_similarities: ~100-200 (depending on threshold)

## Step 5: Install WordPress Plugin (Optional)

```bash
# Copy plugin to WordPress
cp -r wordpress-plugin/related-content-ai /path/to/wordpress/wp-content/plugins/

# Or create symlink for development
ln -s $(pwd)/wordpress-plugin/related-content-ai /path/to/wordpress/wp-content/plugins/
```

Then in WordPress admin:
1. Go to Plugins → Installed Plugins
2. Activate "Related Content AI"
3. Go to Settings → Related Content AI
4. Check system status

## Verification Checklist

- [ ] Virtual environment activated
- [ ] All Python packages installed
- [ ] Database tables created
- [ ] Sample data generated
- [ ] Embeddings generated (check wp_post_embeddings table)
- [ ] Similarities computed (check wp_post_similarities table)
- [ ] Query command returns related posts
- [ ] WordPress plugin installed (optional)

## Common Issues & Solutions

### Issue: "No module named 'sentence_transformers'"

**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Can't connect to MySQL server"

**Solution**: Check database credentials in `.env`
```bash
# Test connection
mysql -u your_user -p -h localhost your_database -e "SELECT 1"
```

### Issue: "Model download fails"

**Solution**: The first run downloads ~1.1GB model. Ensure internet connection.
```bash
# Manual download
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

### Issue: "Memory error during processing"

**Solution**: Reduce batch size in `.env`
```env
BATCH_SIZE=8
```

### Issue: "No related posts found"

**Solution**: Lower similarity threshold
```env
MIN_SIMILARITY_THRESHOLD=0.2
```

## Performance Expectations

### Initial Setup
- Package installation: 2-3 minutes
- Model download (first run): 3-5 minutes
- Database schema: < 10 seconds

### Processing
- 20 posts embedding generation: ~30 seconds
- Similarity computation (20 posts): ~5 seconds
- Total POC time: < 1 minute

### Scale Estimates
- 100 posts: ~2 minutes
- 1,000 posts: ~15 minutes
- 10,000 posts: ~2-3 hours

## Next Steps

After successful POC:

1. **Integration**: Connect to live WordPress site
2. **Automation**: Set up cron jobs for new posts
3. **Optimization**: Tune similarity thresholds
4. **Monitoring**: Set up logging and alerts
5. **Scaling**: Implement queue system for large sites

## POC Success Criteria

✓ Embeddings generated for all test posts
✓ Similarities computed between related posts
✓ Query returns relevant related posts
✓ Similar posts across languages are detected
✓ Processing completes in reasonable time

## Sample Query Results to Expect

For **"2024 US Presidential Election Results"** (English):
- Related in English: Electoral College article (~0.74)
- Related in French: French election article (~0.86)
- Related in Vietnamese: Vietnamese election post (~0.81)

For **"Artificial Intelligence Revolution"**:
- Related: Machine Learning in Healthcare (~0.72)
- Related: French AI article (~0.79)
- Not related: Climate Change article (~0.25)

## Testing Different Languages

```bash
# Test English-French similarity
python main.py --action query --post-id 1  # English post
# Should show French posts with high scores

# Test Vietnamese content
python main.py --action query --post-id 6  # Vietnamese post

# Test Arabic/RTL languages (if data available)
python main.py --action query --post-id 13  # Persian post
```

## Monitoring & Logs

```bash
# Watch processing in real-time
tail -f related_content.log

# Filter for errors
grep ERROR related_content.log

# Check processing stats
grep "Successfully processed" related_content.log | wc -l
```

## Ready for Production?

Before going live:

- [ ] Test with 100+ real posts
- [ ] Verify accuracy of related posts
- [ ] Test all supported languages
- [ ] Benchmark processing time
- [ ] Set up automated processing
- [ ] Configure caching
- [ ] Add monitoring
- [ ] Backup database
- [ ] Document for team
- [ ] Plan rollout strategy
