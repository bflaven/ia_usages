SELECT
    State,
    COUNT(*) AS total_failures,
    SUM("Assets ($mil.)") AS total_assets
FROM
    {{ ref('base_bank_failures') }}
GROUP BY
    State
