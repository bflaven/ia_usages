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