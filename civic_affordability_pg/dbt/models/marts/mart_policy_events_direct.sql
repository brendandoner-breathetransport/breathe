SELECT
    fpe.event_id,
    fpe.geo_id,
    dg.state_abbrev,
    fpe.year,
    fpe.short_label,
    fpe.summary,
    fpe.category
FROM {{ source('raw', 'fact_policy_event') }} fpe
JOIN {{ source('raw', 'dim_geo') }} dg ON dg.geo_id = fpe.geo_id
WHERE fpe.impact_level = 'direct'
ORDER BY fpe.year, fpe.event_id
