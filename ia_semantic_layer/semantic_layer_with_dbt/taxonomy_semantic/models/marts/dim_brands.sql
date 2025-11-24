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