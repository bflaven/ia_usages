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