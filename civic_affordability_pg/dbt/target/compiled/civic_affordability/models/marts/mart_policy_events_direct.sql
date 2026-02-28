SELECT
    fpe.event_id,
    fpe.geo_id,
    dg.state_abbrev,
    fpe.year,
    fpe.short_label,
    fpe.summary,
    fpe.category
FROM "postgres"."raw"."fact_policy_event" fpe
JOIN "postgres"."raw"."dim_geo" dg ON dg.geo_id = fpe.geo_id
WHERE fpe.impact_level = 'direct'
ORDER BY fpe.year, fpe.event_id