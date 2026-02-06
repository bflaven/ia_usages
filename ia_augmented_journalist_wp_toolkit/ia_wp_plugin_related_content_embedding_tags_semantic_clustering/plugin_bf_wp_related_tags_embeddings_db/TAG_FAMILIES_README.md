# BF Tag Families via Embeddings (DB)

WordPress plugin for managing semantic tag families using NER + clustering embeddings.

## Overview

This plugin manages tag families created from semantic clustering (HDBSCAN) and Named Entity Recognition (NER). Tags are grouped into families based on semantic similarity, with a canonical tag representing each family.

---

## Installation

### Step 1: Copy Files

```bash
# Copy main plugin
docker cp bf_wp_tag_families_db.php wordpress:/var/www/html/wp-content/plugins/bf_wp_tag_families_db/

# Copy uninstall handler (MUST be named "uninstall.php")
docker cp tag_families_uninstall.php wordpress:/var/www/html/wp-content/plugins/bf_wp_tag_families_db/uninstall.php

# Set permissions
docker exec wordpress chown -R www-data:www-data /var/www/html/wp-content/plugins/bf_wp_tag_families_db/
```

### Step 2: Activate

Go to WordPress Admin → **Plugins** → Activate "BF Tag Families via Embeddings (DB)"

### Final File Structure

```
wp-content/plugins/bf_wp_tag_families_db/
├── bf_wp_tag_families_db.php    (main plugin)
└── uninstall.php                 (cleanup handler)
```

---

## CSV Format

### Required Columns

```csv
family_id,canonical_tag_id,canonical_label,tag_id,tag_label,similarity_to_canonical,usage_count,entity_label
```

### Column Definitions

| Column | Example | Description |
|--------|---------|-------------|
| **family_id** | `0` | Cluster ID from HDBSCAN |
| **canonical_tag_id** | `6` | WordPress tag ID of family representative (parent) |
| **canonical_label** | `information` | Name of canonical tag |
| **tag_id** | `8` | WordPress tag ID of family member |
| **tag_label** | `infosuroit` | Name of tag member |
| **similarity_to_canonical** | `0.804` | Cosine similarity (0-1) to canonical tag |
| **usage_count** | `5` | Number of posts using this tag |
| **entity_label** | `O` | NER entity type (see table below) |

### Entity Label Types

| Label | Meaning | Examples |
|-------|---------|----------|
| **O** | Outside (generic) | information, marketing, data |
| **PERSON** | Person | jackson, robert jackson |
| **ORG** | Organization | Adobe, 3WDOC, POC |
| **GPE** | Geo-political entity | Paris, France |
| **CARDINAL** | Number | 2012, 3 |
| **DATE** | Date | january 2024 |
| **PRODUCT** | Product | Adsense |

### Example CSV

```csv
family_id,canonical_tag_id,canonical_label,tag_id,tag_label,similarity_to_canonical,usage_count,entity_label
0,6,information,6,information,1.0,3,O
0,6,information,7,.info,0.966,1,O
0,6,information,8,infosuroit,0.804,1,O
0,6,information,9,information landscape,0.761,1,O
1,10,3WDOC,10,3WDOC,1.0,52,CARDINAL
1,10,3WDOC,11,3WDOC Studio,0.876,41,O
1,10,3WDOC,12,3WOC,0.859,1,GPE
1,10,3WDOC,13,W3C,0.794,2,O
```

**Important Rules:**
- Each family has ONE canonical_tag_id (the parent)
- canonical_label is IDENTICAL for all members of a family
- The canonical tag appears as the first row (similarity = 1.0)

---

## Usage

### 1. Import CSV

1. Go to **Settings → Tag Families**
2. Upload your CSV file
3. Check **"Truncate table first?"** to replace existing data
4. Click **"Import CSV"**

### 2. Manage Tag Families (Editorial Control)

Go to **Posts → Tags** → Click **Edit** on any tag:

**Default Mode (checkbox unchecked):**
- Shows all family members from CSV/database
- Drag to reorder
- Changes save to database

**Custom Selection (checkbox checked):**
- Click tags to select/deselect (green = selected)
- Drag to reorder selected tags
- Only selected tags will be displayed

**Reset Button:**
- Removes custom selection
- Returns to showing all family members from CSV

### 3. Display Related Tags

#### Shortcode

```
[bf_related_tags]
[bf_related_tags limit="5" title="Related Tags"]
```

#### Template Function

```php
$related = bf_get_related_tags( $tag_id, $limit );
foreach ( $related as $tag ) {
    echo '<a href="' . $tag['url'] . '">' . $tag['name'] . '</a>';
    echo ' (similarity: ' . number_format($tag['similarity'], 2) . ')';
}
```

#### Example: Display in Single Post

Add to your theme's `single.php`:

```php
<?php
// Show related tags at bottom of post
$post_tags = get_the_tags();
if ( $post_tags ) {
    $first_tag_id = $post_tags[0]->term_id;
    $related = bf_get_related_tags( $first_tag_id, 5 );
    
    if ( $related ) {
        echo '<div class="related-tags-section" style="margin-top: 40px; padding: 20px; background: #f9f9f9;">';
        echo '<h3>Related Topics</h3>';
        echo '<div class="tag-list">';
        foreach ( $related as $tag ) {
            echo '<a href="' . esc_url($tag['url']) . '" style="margin: 5px; padding: 8px 15px; background: white; border: 1px solid #ddd;">';
            echo esc_html($tag['name']) . ' <small>(' . $tag['count'] . ')</small>';
            echo '</a> ';
        }
        echo '</div></div>';
    }
}
?>
```

---

## Python Script Integration

This plugin works with clustering output from the Python script: `002_parsing_tags_similarity_sqlite_export_sqlite_csv.py`

### Python Workflow

1. **Load tags** from WordPress REST API
2. **Generate embeddings** (sentence-transformers/paraphrase-multilingual-mpnet-base-v2)
3. **Cluster tags** using HDBSCAN
4. **Run NER** using spaCy to detect entity types
5. **Select canonical tag** per family (highest usage_count)
6. **Export to CSV**

### Python Dependencies

```bash
conda activate tags_treatment
pip install sentence-transformers hdbscan spacy
python -m spacy download en_core_web_sm
```

### Generate CSV

```bash
# Export WordPress tags
curl "https://your-site.com/wp-json/wp/v2/tags?per_page=100" > tags.json

# Run clustering script
python 002_parsing_tags_similarity_sqlite_export_sqlite_csv.py

# Output: related_tags_embeddings_settings_csv_1.csv
```

---

## Database Schema

**Table:** `wp_tag_families`

| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT | Auto-increment primary key |
| family_id | INT | Cluster/family identifier |
| canonical_tag_id | BIGINT | Primary tag for family |
| canonical_label | VARCHAR(255) | Canonical tag name |
| tag_id | BIGINT | WordPress tag ID |
| tag_label | VARCHAR(255) | Tag name |
| similarity_to_canonical | DOUBLE | Cosine similarity score |
| usage_count | INT | Post count for tag |
| entity_label | VARCHAR(50) | NER entity type |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE KEY on `(family_id, tag_id)`
- KEY on `tag_id`, `family_id`, `canonical_tag_id`

---

## Uninstall

### Automatic Cleanup

When you delete the plugin via WordPress Admin:

1. **Deactivate** the plugin
2. Click **Delete**
3. Confirm deletion

The plugin will automatically:
- Drop `wp_tag_families` table
- Delete all term meta (`_bf_custom_family_selection`, `_bf_custom_mode_active`, `_bf_custom_family_order`)
- Delete all plugin options

### Verify Uninstall Worked

Check in phpMyAdmin or MySQL:

```sql
-- Should return empty (no table)
SHOW TABLES LIKE 'wp_tag_families';

-- Should return empty (no meta)
SELECT * FROM wp_termmeta WHERE meta_key LIKE '_bf_custom%';
```

### Manual Cleanup (if needed)

If automatic uninstall doesn't work:

```bash
docker exec wordpress mysql -u root -proot wordpress -e "DROP TABLE IF EXISTS wp_tag_families;"
docker exec wordpress mysql -u root -proot wordpress -e "DELETE FROM wp_termmeta WHERE meta_key LIKE '_bf_custom%';"
docker exec wordpress mysql -u root -proot wordpress -e "DELETE FROM wp_options WHERE option_name LIKE 'bf_tf_%';"
```

---

## Use Cases

### Content Discovery
Show semantically related tags to help users find similar content.

**Example:** User clicks "information" → sees ".info", "infosuroit", "data"

### Tag Consolidation
Identify tag clusters for cleanup.

**Example:** Family shows "marketing" contains "publicité", "Adsense", "commercial" → merge similar tags

### Entity-Based Navigation
Filter by NER entity types for specialized navigation.

**Example:** Show only PERSON tags, only ORG tags, etc.

### Multilingual Support
Works with multilingual embeddings to group tags across languages.

**Example:** "information" (EN) clusters with "información" (ES)

---

## Troubleshooting

### No family members showing when editing tag

**Check if tag is in database:**
```sql
SELECT * FROM wp_tag_families WHERE tag_id = 6;
```

If empty, the tag wasn't in your CSV import.

### Import says "0 rows imported"

**Solution:** Re-save CSV as UTF-8 without BOM

### Table still exists after uninstall

**Check uninstall.php exists:**
```bash
docker exec wordpress ls -la /var/www/html/wp-content/plugins/bf_wp_tag_families_db/uninstall.php
```

If missing, reinstall plugin with correct files.

### Tags don't match CSV IDs

Your WordPress tag IDs don't match the IDs in the CSV.

**Solution:** Either:
1. Import tags with correct IDs first
2. Or remap CSV IDs to match your WordPress tag IDs

---

## Example Workflow

### Scenario: Add "marketing" family

**1. Python generates CSV with these rows:**
```csv
2,468,marketing,468,marketing,1.0,4,O
2,468,marketing,103,publicité,0.805,1,O
2,468,marketing,100,Adsense,0.660,3,O
```

**2. Create tags in WordPress:**
- Add "marketing" → gets ID 14
- Add "publicité" → gets ID 15
- Add "Adsense" → gets ID 16

**3. Update CSV with new IDs:**
```csv
2,14,marketing,14,marketing,1.0,4,O
2,14,marketing,15,publicité,0.805,1,O
2,14,marketing,16,Adsense,0.660,3,O
```

**4. Import CSV** (Settings → Tag Families)

**5. Edit tag "marketing"** → see "publicité" and "Adsense" as related

**6. Create posts:**
- Post: "Digital Marketing Guide"
- Tags: `marketing, Adsense, publicité`

**7. Display on frontend:**
When users visit `/tag/marketing/`, they see links to `Adsense` and `publicité`

---

## Support

For issues or questions:
1. Check this README
2. Verify CSV format matches exactly
3. Check database table exists
4. Test with manual SQL queries

## License

Use freely for your projects.
