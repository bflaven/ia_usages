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