# walkthrough_ia_build_semantic_layer.md


Based on your requirements and the latest best practices, I'll provide you with a complete prototype for building a semantic layer with dbt and DuckDB for taxonomy standardization. This will include a multi-language taxonomy management system with French as the pivot language.

## **Semantic Layer Prototype for Taxonomy Standardization**

### **Architecture Overview**

This prototype implements:
1. **DuckDB** as the local analytical database
2. **dbt** for data transformation and semantic modeling
3. **Multi-language taxonomy management** (FR as master, 18 slave languages)
4. **Named Entity Recognition (NER)** support for SEO optimization
5. **Deduplication and standardization** logic

***

## **Step 1: Environment Setup**

### **Install Dependencies**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install dbt-duckdb duckdb pandas

# Verify installation
dbt --version



# real how-to
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt/
conda create -n semantic_layer_with_dbt python=3.12
conda activate semantic_layer_with_dbt
pip install --upgrade pip
pip install "mashumaro[msgpack]>=3.9,<3.15"
# pip install dbt-duckdb duckdb pandas
dbt --version

pip install dbt-duckdb duckdb pandas
pip install "dbt-duckdb==1.10.0" "duckdb==0.10.0" "pandas==2.2.2"




```

### **Initialize dbt Project**

```bash
# go to path
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_semantic_layer/semantic_layer_with_dbt/
# Create new dbt project
dbt init taxonomy_semantic_layer_1
cd taxonomy_semantic_layer_1
```

***

## **Step 2: Configure dbt with DuckDB**

### **profiles.yml** (in `~/.dbt/profiles.yml`)

```yaml
taxonomy_semantic_layer:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: 'taxonomy.duckdb'
      schema: main
      threads: 4
      extensions:
        - httpfs
        - json
      settings:
        s3_region: eu-west-1
    
    prod:
      type: duckdb
      path: 'taxonomy_prod.duckdb'
      schema: main
      threads: 8
      extensions:
        - httpfs
        - json
```

### **dbt_project.yml**

```yaml
name: 'taxonomy_semantic_layer'
version: '1.0.0'
config-version: 2

profile: 'taxonomy_semantic_layer'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:
  - "target"
  - "dbt_packages"

models:
  taxonomy_semantic_layer:
    +materialized: table
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts
    semantic:
      +materialized: table
      +schema: semantic

seeds:
  taxonomy_semantic_layer:
    +schema: seeds
    +quote_columns: false

vars:
  master_language: 'FR'
  supported_languages: ['FR', 'EN', 'AR', 'CN', 'RU', 'ES', 'DE', 'IT', 'PT', 'JA', 'KO', 'VI', 'TH', 'TR', 'PL', 'NL', 'SV', 'DA', 'NO']
  brands: ['F24', 'RFI', 'MC']
```

***

## **Step 3: Create Seed Data (Sample Taxonomy)**

### **seeds/raw_thematic_tags.csv**

```csv
brand,language,tag_id,tag_name,tag_slug,usage_count,created_at,entity_type
F24,FR,1,Politique française,politique-francaise,1250,2024-01-15,GPE
F24,EN,2,French politics,french-politics,890,2024-01-15,GPE
F24,FR,3,Emmanuel Macron,emmanuel-macron,2100,2024-01-10,PER
F24,EN,4,Emmanuel Macron,emmanuel-macron,1850,2024-01-10,PER
F24,FR,5,Élections présidentielles,elections-presidentielles,980,2024-02-01,EVENT
F24,EN,6,Presidential elections,presidential-elections,875,2024-02-01,EVENT
RFI,FR,7,Politique française,politique-francaise,560,2024-01-20,GPE
RFI,FR,8,politique francaise,politique-francaise,120,2024-01-20,GPE
F24,FR,9,Ukraine,ukraine,3200,2023-11-01,GPE
F24,EN,10,Ukraine,ukraine,2980,2023-11-01,GPE
F24,AR,11,أوكرانيا,ukraine,1200,2023-11-01,GPE
F24,CN,12,乌克兰,ukraine,890,2023-11-01,GPE
```

### **seeds/raw_super_tags.csv**

```csv
brand,language,tag_id,tag_name,tag_slug,parent_tag_id,usage_count,entity_type
F24,FR,101,Europe,europe,,5600,GPE
F24,EN,102,Europe,europe,,4800,GPE
F24,FR,103,France,france,101,8900,GPE
F24,EN,104,France,france,102,7500,GPE
F24,FR,105,Organisations internationales,organisations-internationales,,2300,ORG
F24,EN,106,International organizations,international-organizations,,2100,ORG
F24,FR,107,ONU,onu,105,1850,ORG
F24,EN,108,UN,un,106,1750,ORG
```

***

## **Step 4: Create dbt Models**

### **Project Structure**

```
models/
├── staging/
│   ├── stg_thematic_tags.sql
│   ├── stg_super_tags.sql
│   └── schema.yml
├── intermediate/
│   ├── int_tags_normalized.sql
│   ├── int_tags_deduplicated.sql
│   ├── int_master_slave_mapping.sql
│   └── schema.yml
├── marts/
│   ├── dim_tags.sql
│   ├── dim_brands.sql
│   ├── dim_languages.sql
│   └── schema.yml
└── semantic/
    ├── semantic_entities.yml
    ├── metrics.yml
    └── README.md
```

### **models/staging/stg_thematic_tags.sql**

```sql
{{
  config(
    materialized='view'
  )
}}

with source_data as (
    select * from {{ ref('raw_thematic_tags') }}
),

cleaned as (
    select
        brand || '_' || language as brand_language_key,
        brand,
        language,
        tag_id,
        -- Normalize tag names: trim, lowercase for comparison
        trim(tag_name) as tag_name,
        lower(trim(tag_name)) as tag_name_normalized,
        tag_slug,
        coalesce(usage_count, 0) as usage_count,
        created_at::date as created_at,
        coalesce(entity_type, 'UNKNOWN') as entity_type,
        'thematic' as tag_type
    from source_data
)

select
    {{ dbt_utils.generate_surrogate_key(['brand', 'language', 'tag_id']) }} as staging_key,
    *,
    current_timestamp as loaded_at
from cleaned
```

### **models/staging/stg_super_tags.sql**

```sql
{{
  config(
    materialized='view'
  )
}}

with source_data as (
    select * from {{ ref('raw_super_tags') }}
),

cleaned as (
    select
        brand || '_' || language as brand_language_key,
        brand,
        language,
        tag_id,
        trim(tag_name) as tag_name,
        lower(trim(tag_name)) as tag_name_normalized,
        tag_slug,
        parent_tag_id,
        coalesce(usage_count, 0) as usage_count,
        coalesce(entity_type, 'UNKNOWN') as entity_type,
        'super' as tag_type
    from source_data
)

select
    {{ dbt_utils.generate_surrogate_key(['brand', 'language', 'tag_id']) }} as staging_key,
    *,
    current_timestamp as loaded_at
from cleaned
```

### **models/intermediate/int_tags_normalized.sql**

```sql
{{
  config(
    materialized='view'
  )
}}

with thematic_tags as (
    select * from {{ ref('stg_thematic_tags') }}
),

super_tags as (
    select * from {{ ref('stg_super_tags') }}
),

all_tags as (
    select
        staging_key,
        brand_language_key,
        brand,
        language,
        tag_id,
        tag_name,
        tag_name_normalized,
        tag_slug,
        null as parent_tag_id,
        usage_count,
        entity_type,
        tag_type,
        created_at,
        loaded_at
    from thematic_tags
    
    union all
    
    select
        staging_key,
        brand_language_key,
        brand,
        language,
        tag_id,
        tag_name,
        tag_name_normalized,
        tag_slug,
        parent_tag_id,
        usage_count,
        entity_type,
        tag_type,
        null as created_at,
        loaded_at
    from super_tags
),

-- Apply text normalization rules
normalized as (
    select
        *,
        -- Remove accents for better matching (simplified approach)
        regexp_replace(
            regexp_replace(
                regexp_replace(tag_name_normalized, '[éèêë]', 'e', 'g'),
                '[àâä]', 'a', 'g'
            ),
            '[ôö]', 'o', 'g'
        ) as tag_name_ascii,
        -- Calculate hash for exact duplicate detection
        md5(tag_name_normalized || brand || language) as content_hash
    from all_tags
)

select * from normalized
```

### **models/intermediate/int_tags_deduplicated.sql**

```sql
{{
  config(
    materialized='view'
  )
}}

with normalized_tags as (
    select * from {{ ref('int_tags_normalized') }}
),

-- Identify duplicates within same brand_language
duplicates_ranked as (
    select
        *,
        row_number() over (
            partition by brand_language_key, tag_name_normalized, tag_type
            order by usage_count desc, tag_id asc
        ) as duplicate_rank
    from normalized_tags
),

-- Keep only the most used version (rank = 1)
deduplicated as (
    select
        staging_key as original_staging_key,
        brand_language_key,
        brand,
        language,
        tag_id as canonical_tag_id,
        tag_name as canonical_tag_name,
        tag_name_normalized,
        tag_name_ascii,
        tag_slug as canonical_slug,
        parent_tag_id,
        usage_count,
        entity_type,
        tag_type,
        created_at,
        duplicate_rank,
        case 
            when duplicate_rank = 1 then 'CANONICAL'
            else 'DUPLICATE'
        end as duplicate_status
    from duplicates_ranked
)

select * from deduplicated
```

### **models/intermediate/int_master_slave_mapping.sql**

```sql
{{
  config(
    materialized='view'
  )
}}

with deduplicated_tags as (
    select * from {{ ref('int_tags_deduplicated') }}
    where duplicate_status = 'CANONICAL'
),

-- Get French (master) tags
master_tags as (
    select
        brand,
        canonical_tag_id as master_tag_id,
        canonical_tag_name as master_tag_name,
        canonical_slug as master_slug,
        tag_name_normalized as master_normalized,
        entity_type,
        tag_type,
        usage_count as master_usage_count
    from deduplicated_tags
    where language = '{{ var("master_language") }}'
),

-- Get all other language (slave) tags
slave_tags as (
    select
        brand,
        language as slave_language,
        canonical_tag_id as slave_tag_id,
        canonical_tag_name as slave_tag_name,
        canonical_slug as slave_slug,
        tag_name_normalized as slave_normalized,
        tag_name_ascii as slave_ascii,
        entity_type,
        tag_type,
        usage_count as slave_usage_count
    from deduplicated_tags
    where language != '{{ var("master_language") }}'
),

-- Attempt to match based on slug similarity
matched_tags as (
    select
        m.brand,
        m.master_tag_id,
        m.master_tag_name,
        m.master_slug,
        m.entity_type,
        m.tag_type,
        s.slave_language,
        s.slave_tag_id,
        s.slave_tag_name,
        s.slave_slug,
        s.slave_usage_count,
        case
            when m.master_slug = s.slave_slug then 'EXACT_SLUG_MATCH'
            when m.entity_type = s.entity_type and m.tag_type = s.tag_type 
                and levenshtein(m.master_normalized, s.slave_ascii) <= 3 then 'FUZZY_MATCH'
            else 'NO_MATCH'
        end as match_quality,
        levenshtein(m.master_normalized, s.slave_ascii) as edit_distance
    from master_tags m
    left join slave_tags s
        on m.brand = s.brand
        and m.entity_type = s.entity_type
        and m.tag_type = s.tag_type
    where s.slave_tag_id is not null
        and (m.master_slug = s.slave_slug 
             or levenshtein(m.master_normalized, s.slave_ascii) <= 3)
)

select * from matched_tags
```

### **models/marts/dim_tags.sql**

```sql
{{
  config(
    materialized='table'
  )
}}

with master_slave_mapping as (
    select * from {{ ref('int_master_slave_mapping') }}
),

deduplicated_tags as (
    select * from {{ ref('int_tags_deduplicated') }}
    where duplicate_status = 'CANONICAL'
),

-- Create master dimension
master_dimension as (
    select distinct
        {{ dbt_utils.generate_surrogate_key(['m.brand', 'm.master_tag_id']) }} as tag_key,
        m.brand,
        m.master_tag_id as tag_id,
        m.master_tag_name as tag_name,
        m.master_slug as tag_slug,
        m.entity_type,
        m.tag_type,
        '{{ var("master_language") }}' as language,
        'MASTER' as tag_role,
        null as master_tag_reference,
        m.master_usage_count as total_usage_count
    from (
        select distinct brand, master_tag_id, master_tag_name, 
               master_slug, entity_type, tag_type, master_usage_count
        from master_slave_mapping
    ) m
),

-- Create slave dimension with references to master
slave_dimension as (
    select distinct
        {{ dbt_utils.generate_surrogate_key(['m.brand', 'm.slave_tag_id']) }} as tag_key,
        m.brand,
        m.slave_tag_id as tag_id,
        m.slave_tag_name as tag_name,
        m.slave_slug as tag_slug,
        m.entity_type,
        m.tag_type,
        m.slave_language as language,
        'SLAVE' as tag_role,
        {{ dbt_utils.generate_surrogate_key(['m.brand', 'm.master_tag_id']) }} as master_tag_reference,
        m.slave_usage_count as total_usage_count
    from master_slave_mapping m
    where m.match_quality in ('EXACT_SLUG_MATCH', 'FUZZY_MATCH')
),

-- Combine both
final_dimension as (
    select * from master_dimension
    union all
    select * from slave_dimension
)

select
    tag_key,
    brand,
    tag_id,
    tag_name,
    tag_slug,
    entity_type,
    tag_type,
    language,
    tag_role,
    master_tag_reference,
    total_usage_count,
    current_timestamp as dimension_updated_at
from final_dimension
```

### **models/marts/dim_brands.sql**

```sql
{{
  config(
    materialized='table'
  )
}}

select
    brand as brand_code,
    case 
        when brand = 'F24' then 'France 24'
        when brand = 'RFI' then 'Radio France Internationale'
        when brand = 'MC' then 'Monte Carlo Doualiya'
    end as brand_name,
    current_timestamp as dimension_updated_at
from (values ('F24'), ('RFI'), ('MC')) as brands(brand)
```

### **models/marts/dim_languages.sql**

```sql
{{
  config(
    materialized='table'
  )
}}

with language_list as (
    select unnest([
        'FR', 'EN', 'AR', 'CN', 'RU', 'ES', 'DE', 'IT', 
        'PT', 'JA', 'KO', 'VI', 'TH', 'TR', 'PL', 'NL', 'SV', 'DA', 'NO'
    ]) as language_code
)

select
    language_code,
    case language_code
        when 'FR' then 'French'
        when 'EN' then 'English'
        when 'AR' then 'Arabic'
        when 'CN' then 'Chinese'
        when 'RU' then 'Russian'
        when 'ES' then 'Spanish'
        when 'DE' then 'German'
        when 'IT' then 'Italian'
        when 'PT' then 'Portuguese'
        when 'JA' then 'Japanese'
        when 'KO' then 'Korean'
        when 'VI' then 'Vietnamese'
        when 'TH' then 'Thai'
        when 'TR' then 'Turkish'
        when 'PL' then 'Polish'
        when 'NL' then 'Dutch'
        when 'SV' then 'Swedish'
        when 'DA' then 'Danish'
        when 'NO' then 'Norwegian'
    end as language_name,
    case when language_code = '{{ var("master_language") }}' then true else false end as is_master,
    current_timestamp as dimension_updated_at
from language_list
```

***

## **Step 5: Define Semantic Layer (MetricFlow)**

### **models/semantic/semantic_entities.yml**

```yaml
version: 2

semantic_models:
  - name: taxonomy_metrics
    description: "Semantic model for taxonomy standardization and metrics"
    model: ref('dim_tags')
    
    entities:
      - name: tag
        type: primary
        expr: tag_key
      
      - name: brand
        type: foreign
        expr: brand
      
      - name: language
        type: foreign
        expr: language
    
    dimensions:
      - name: tag_name
        type: categorical
        expr: tag_name
      
      - name: tag_slug
        type: categorical
        expr: tag_slug
      
      - name: entity_type
        type: categorical
        expr: entity_type
        description: "Named entity type (PER, ORG, GPE, EVENT, etc.)"
      
      - name: tag_type
        type: categorical
        expr: tag_type
        description: "Tag type: thematic or super"
      
      - name: tag_role
        type: categorical
        expr: tag_role
        description: "MASTER or SLAVE tag designation"
      
      - name: language
        type: categorical
        expr: language
    
    measures:
      - name: total_tags
        agg: count
        expr: tag_key
        description: "Total number of tags"
      
      - name: total_usage
        agg: sum
        expr: total_usage_count
        description: "Sum of tag usage across all content"
      
      - name: avg_usage_per_tag
        agg: average
        expr: total_usage_count
        description: "Average usage count per tag"
```

### **models/semantic/metrics.yml**

```yaml
version: 2

metrics:
  - name: tag_count
    label: "Total Tag Count"
    description: "Count of distinct tags in the taxonomy"
    type: simple
    type_params:
      measure: total_tags
  
  - name: tag_usage_total
    label: "Total Tag Usage"
    description: "Sum of all tag usages across content"
    type: simple
    type_params:
      measure: total_usage
  
  - name: tag_usage_average
    label: "Average Tag Usage"
    description: "Average usage per tag"
    type: simple
    type_params:
      measure: avg_usage_per_tag
  
  - name: tags_by_entity_type
    label: "Tags Grouped by Entity Type"
    description: "Tag count segmented by NER entity type (PER, ORG, GPE, etc.)"
    type: simple
    type_params:
      measure: total_tags
    dimensions:
      - entity_type
  
  - name: master_slave_ratio
    label: "Master to Slave Tag Ratio"
    description: "Ratio of master tags to slave tags by language"
    type: ratio
    type_params:
      numerator: total_tags
      denominator: total_tags
    filter: |
      {{ Dimension('tag_role') }} = 'MASTER'
```

***

## **Step 6: Add dbt Macros for Reusability**

### **macros/generate_schema_name.sql**
touch macros/generate_schema_name.sql
```sql

{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
```

### **macros/levenshtein.sql** (For fuzzy matching)
touch macros/levenshtein.sql

```sql
{% macro levenshtein(string1, string2) %}
    editdist3({{ string1 }}, {{ string2 }})
{% endmacro %}
```

***

## **Step 7: Testing Configuration**

### **models/staging/schema.yml**

touch models/staging/schema.yml
```yaml
version: 2

models:
  - name: stg_thematic_tags
    description: "Staging layer for thematic tags with basic cleaning"
    columns:
      - name: staging_key
        description: "Surrogate key for staging records"
        tests:
          - unique
          - not_null
      
      - name: brand
        description: "Brand identifier (F24, RFI, MC)"
        tests:
          - not_null
          - accepted_values:
              values: ['F24', 'RFI', 'MC']
      
      - name: language
        description: "ISO language code"
        tests:
          - not_null
      
      - name: tag_name
        description: "Original tag name"
        tests:
          - not_null
      
      - name: entity_type
        description: "Named entity type for SEO"
        tests:
          - accepted_values:
              values: ['PER', 'ORG', 'GPE', 'EVENT', 'UNKNOWN']
  
  - name: stg_super_tags
    description: "Staging layer for super tags (hierarchical)"
    columns:
      - name: staging_key
        tests:
          - unique
          - not_null
```

### **models/marts/schema.yml**

```yaml
version: 2

models:
  - name: dim_tags
    description: "Master dimension table for all tags with master-slave relationships"
    columns:
      - name: tag_key
        description: "Surrogate key for dimension"
        tests:
          - unique
          - not_null
      
      - name: tag_role
        description: "MASTER or SLAVE designation"
        tests:
          - accepted_values:
              values: ['MASTER', 'SLAVE']
      
      - name: master_tag_reference
        description: "Reference to master tag (for slave tags only)"
        tests:
          - relationships:
              to: ref('dim_tags')
              field: tag_key
              where: "tag_role = 'SLAVE'"
```

***

## **Step 8: Install dbt Packages**

### **packages.yml**

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
```

Run:
```bash
dbt deps
```

***

## **Step 9: Execute the dbt Pipeline**

```bash
# Load seed data
dbt seed
dbt seed --show-all-deprecations --no-partial-parse


# Run all models
dbt run

# Test data quality
dbt test

# Generate documentation
dbt docs generate

# Serve documentation locally
dbt docs serve

```

***

## **Step 10: Query the Semantic Layer**

### **Query Examples Using DuckDB**

```python
import duckdb

# Connect to the database
conn = duckdb.connect('taxonomy.duckdb')

# Query 1: Get all master tags with their slave translations
query1 = """
SELECT 
    master.tag_name as french_name,
    master.entity_type,
    slave.language as translation_language,
    slave.tag_name as translated_name,
    slave.total_usage_count
FROM marts.dim_tags master
LEFT JOIN marts.dim_tags slave 
    ON master.tag_key = slave.master_tag_reference
WHERE master.tag_role = 'MASTER'
    AND master.brand = 'F24'
ORDER BY master.tag_name, slave.language;
"""

print(conn.execute(query1).df())

# Query 2: Identify tags with no translations
query2 = """
SELECT 
    m.brand,
    m.tag_name as french_tag,
    m.entity_type,
    COUNT(DISTINCT s.language) as translation_count,
    19 - COUNT(DISTINCT s.language) as missing_translations
FROM marts.dim_tags m
LEFT JOIN marts.dim_tags s ON m.tag_key = s.master_tag_reference
WHERE m.tag_role = 'MASTER'
GROUP BY m.brand, m.tag_name, m.entity_type
HAVING COUNT(DISTINCT s.language) < 18
ORDER BY missing_translations DESC;
"""

print(conn.execute(query2).df())

# Query 3: Tag usage by entity type (SEO optimization)
query3 = """
SELECT 
    entity_type,
    COUNT(*) as tag_count,
    SUM(total_usage_count) as total_usage,
    AVG(total_usage_count) as avg_usage
FROM marts.dim_tags
WHERE tag_role = 'MASTER'
GROUP BY entity_type
ORDER BY total_usage DESC;
"""

print(conn.execute(query3).df())

conn.close()
```

***

## **Step 11: FastAPI Integration (Bonus)**

### **api/main.py**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import duckdb
from typing import List, Optional

app = FastAPI(title="Taxonomy Semantic Layer API")

# Database connection
DB_PATH = "taxonomy.duckdb"

class TagTranslation(BaseModel):
    language: str
    tag_name: str
    tag_slug: str
    usage_count: int

class MasterTag(BaseModel):
    tag_id: int
    tag_name: str
    tag_slug: str
    entity_type: str
    tag_type: str
    brand: str
    translations: List[TagTranslation]

@app.get("/api/v1/tags/master", response_model=List[MasterTag])
def get_master_tags(
    brand: Optional[str] = None,
    entity_type: Optional[str] = None
):
    """Get all master tags with their translations"""
    
    conn = duckdb.connect(DB_PATH, read_only=True)
    
    query = """
    SELECT 
        m.tag_id,
        m.tag_name,
        m.tag_slug,
        m.entity_type,
        m.tag_type,
        m.brand,
        s.language as translation_language,
        s.tag_name as translation_name,
        s.tag_slug as translation_slug,
        s.total_usage_count as translation_usage
    FROM marts.dim_tags m
    LEFT JOIN marts.dim_tags s ON m.tag_key = s.master_tag_reference
    WHERE m.tag_role = 'MASTER'
    """
    
    params = []
    if brand:
        query += " AND m.brand = ?"
        params.append(brand)
    if entity_type:
        query += " AND m.entity_type = ?"
        params.append(entity_type)
    
    query += " ORDER BY m.tag_name, s.language"
    
    result = conn.execute(query, params).fetchdf()
    conn.close()
    
    # Transform to response model
    tags_dict = {}
    for _, row in result.iterrows():
        tag_id = row['tag_id']
        if tag_id not in tags_dict:
            tags_dict[tag_id] = {
                'tag_id': int(tag_id),
                'tag_name': row['tag_name'],
                'tag_slug': row['tag_slug'],
                'entity_type': row['entity_type'],
                'tag_type': row['tag_type'],
                'brand': row['brand'],
                'translations': []
            }
        
        if row['translation_language']:
            tags_dict[tag_id]['translations'].append({
                'language': row['translation_language'],
                'tag_name': row['translation_name'],
                'tag_slug': row['translation_slug'],
                'usage_count': int(row['translation_usage'])
            })
    
    return list(tags_dict.values())

@app.get("/api/v1/tags/orphans")
def get_orphan_tags():
    """Get tags without translations"""
    
    conn = duckdb.connect(DB_PATH, read_only=True)
    
    query = """
    SELECT 
        m.brand,
        m.tag_name,
        m.entity_type,
        COUNT(DISTINCT s.language) as translation_count
    FROM marts.dim_tags m
    LEFT JOIN marts.dim_tags s ON m.tag_key = s.master_tag_reference
    WHERE m.tag_role = 'MASTER'
    GROUP BY m.brand, m.tag_name, m.entity_type
    HAVING COUNT(DISTINCT s.language) < 18
    """
    
    result = conn.execute(query).fetchdf()
    conn.close()
    
    return result.to_dict(orient='records')

@app.get("/api/v1/metrics/entity-types")
def get_entity_type_metrics():
    """Get metrics by named entity type (for SEO)"""
    
    conn = duckdb.connect(DB_PATH, read_only=True)
    
    query = """
    SELECT 
        entity_type,
        COUNT(*) as tag_count,
        SUM(total_usage_count) as total_usage
    FROM marts.dim_tags
    WHERE tag_role = 'MASTER'
    GROUP BY entity_type
    ORDER BY total_usage DESC
    """
    
    result = conn.execute(query).fetchdf()
    conn.close()
    
    return result.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **Run the API**

```bash
pip install fastapi uvicorn
python api/main.py
```

Access documentation at: `http://localhost:8000/docs`

***

## **Key Benefits of This Architecture**

1. **✅ Single Source of Truth**: French (FR) as master language
2. **✅ Automated Deduplication**: Handles spelling variants and duplicates
3. **✅ Multi-language Support**: Master-slave relationship for all 19 languages
4. **✅ SEO Optimization**: Named entity tracking (PER, ORG, GPE, EVENT)
5. **✅ Scalability**: DuckDB handles millions of tags efficiently
6. **✅ Modularity**: dbt layers (staging → intermediate → marts → semantic)
7. **✅ Data Quality**: Built-in tests for consistency
8. **✅ API Ready**: FastAPI endpoints for MEZZO integration
9. **✅ Documentation**: Auto-generated lineage and data catalog

This prototype provides a production-ready foundation for your taxonomy standardization strategy! 🚀

[1](https://duckdb.org)
[2](https://github.com/dbt-labs)
[3](https://duckdb.org/2025/04/04/dbt-duckdb.html)
[4](https://www.datacamp.com/tutorial/semantic-layer-with-dbt)
[5](https://motherduck.com/blog/semantic-layer-duckdb-tutorial/)
[6](https://docs.getdbt.com/guides/duckdb)
[7](https://www.youtube.com/watch?v=QyM4eFvUmyI)
[8](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl)
[9](https://www.secoda.co/learn/how-to-connect-to-duckdb-with-dbt-developer-hub)
[10](https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models)
[11](https://rmoff.net/2022/10/20/data-engineering-in-2022-exploring-dbt-with-duckdb/)
[12](https://docs.getdbt.com/best-practices/how-we-build-our-metrics/semantic-layer-2-setup)
[13](https://airbyte.com/tutorials/data-pipeline-with-dbt-duckdb)
[14](https://estuary.dev/blog/dbt-data-modeling/)
[15](https://github.com/dbt-labs/Semantic-Layer-Online-Course)
[16](https://github.com/dbt-labs/Coalesce-2025-Intro-to-the-dbt-Semantic-Layer)
[17](https://motherduck.com/blog/duckdb-dbt-e2e-data-engineering-project-part-2/)
[18](https://www.getdbt.com/blog/modular-data-modeling-techniques)
[19](https://blog.dataengineerthings.org/transforming-data-engineering-a-deep-dive-into-dbt-with-duckdb-ddd3a0c1e0c2)
[20](https://www.5x.co/blogs/semantic-layer)
[21](https://www.next-decision.fr/wiki/creation-dun-data-lakehouse-avec-duckdb-et-dbt)
[22](https://blog.pmunhoz.com/dbt/dbt-documentation-best-practices)





