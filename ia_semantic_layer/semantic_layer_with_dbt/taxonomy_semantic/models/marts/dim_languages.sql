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