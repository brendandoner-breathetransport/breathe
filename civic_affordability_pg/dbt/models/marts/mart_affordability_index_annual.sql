WITH metric_values AS (
    SELECT
        fm.geo_id,
        dt.year,
        dg.state_abbrev,
        dm.metric_name,
        fm.value
    FROM {{ source('raw', 'fact_metric') }} fm
    JOIN {{ source('raw', 'dim_time') }} dt ON dt.period_id = fm.period_id
    JOIN {{ source('raw', 'dim_geo') }} dg ON dg.geo_id = fm.geo_id
    JOIN {{ source('raw', 'dim_metric') }} dm ON dm.metric_id = fm.metric_id
),
wide_values AS (
    SELECT
        geo_id,
        state_abbrev,
        year,
        MAX(CASE WHEN metric_name = 'income_real' THEN value END) AS income_real,
        MAX(CASE WHEN metric_name = 'housing_hpi' THEN value END) AS housing_hpi,
        MAX(CASE WHEN metric_name = 'healthcare_pc' THEN value END) AS healthcare_pc,
        MAX(CASE WHEN metric_name = 'childcare_annual' THEN value END) AS childcare_annual
    FROM metric_values
    GROUP BY geo_id, state_abbrev, year
),
base_values AS (
    SELECT
        geo_id,
        MAX(CASE WHEN year = {{ var('base_year', 2003) }} THEN income_real END) AS income_base,
        MAX(CASE WHEN year = {{ var('base_year', 2003) }} THEN housing_hpi END) AS housing_base,
        MAX(CASE WHEN year = {{ var('base_year', 2003) }} THEN healthcare_pc END) AS healthcare_base,
        MAX(CASE WHEN year = {{ var('base_year', 2003) }} THEN childcare_annual END) AS childcare_base
    FROM wide_values
    GROUP BY geo_id
)
SELECT
    w.geo_id,
    w.state_abbrev,
    w.year,
    w.income_real,
    w.housing_hpi,
    w.healthcare_pc,
    w.childcare_annual,
    (w.income_real / NULLIF(b.income_base, 0)) * 100.0 AS income_index,
    (w.housing_hpi / NULLIF(b.housing_base, 0)) * 100.0 AS housing_index,
    (w.healthcare_pc / NULLIF(b.healthcare_base, 0)) * 100.0 AS healthcare_index,
    (w.childcare_annual / NULLIF(b.childcare_base, 0)) * 100.0 AS childcare_index
FROM wide_values w
JOIN base_values b ON b.geo_id = w.geo_id
ORDER BY w.geo_id, w.year
