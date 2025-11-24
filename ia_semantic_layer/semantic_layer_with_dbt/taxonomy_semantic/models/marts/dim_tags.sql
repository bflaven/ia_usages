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