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