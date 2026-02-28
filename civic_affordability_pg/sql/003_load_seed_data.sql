BEGIN;

CREATE TEMP TABLE tmp_affordability (
    geo_id INTEGER,
    state_abbrev TEXT,
    year INTEGER,
    income_real NUMERIC,
    housing_hpi NUMERIC,
    healthcare_pc NUMERIC,
    childcare_annual NUMERIC,
    income_index NUMERIC,
    housing_index NUMERIC,
    healthcare_index NUMERIC,
    childcare_index NUMERIC,
    cost_pressure_index NUMERIC,
    affordability_gap_index NUMERIC
);

\copy tmp_affordability FROM 'seeds/co_affordability_index_annual.csv' CSV HEADER;

INSERT INTO raw.dim_time (period_id, year, frequency)
SELECT DISTINCT year AS period_id, year, 'annual'
FROM tmp_affordability
ON CONFLICT (period_id) DO UPDATE
SET year = EXCLUDED.year,
    frequency = EXCLUDED.frequency;

INSERT INTO raw.fact_metric (geo_id, period_id, metric_id, value, source_id, vintage_date)
SELECT geo_id, year, 1, income_real, 1, CURRENT_DATE FROM tmp_affordability
UNION ALL
SELECT geo_id, year, 2, housing_hpi, 1, CURRENT_DATE FROM tmp_affordability
UNION ALL
SELECT geo_id, year, 3, healthcare_pc, 1, CURRENT_DATE FROM tmp_affordability
UNION ALL
SELECT geo_id, year, 4, childcare_annual, 1, CURRENT_DATE FROM tmp_affordability
ON CONFLICT (geo_id, period_id, metric_id) DO UPDATE
SET value = EXCLUDED.value,
    source_id = EXCLUDED.source_id,
    vintage_date = EXCLUDED.vintage_date;

CREATE TEMP TABLE tmp_policy_events (
    event_id INTEGER,
    geo_id INTEGER,
    state_abbrev TEXT,
    event_date DATE,
    year INTEGER,
    name TEXT,
    short_label TEXT,
    summary TEXT,
    category TEXT,
    impact_level TEXT,
    source_url TEXT
);

\copy tmp_policy_events FROM 'seeds/co_policy_events_direct.csv' CSV HEADER;

INSERT INTO raw.fact_policy_event (
    event_id,
    geo_id,
    event_date,
    year,
    name,
    short_label,
    summary,
    category,
    impact_level,
    source_url
)
SELECT
    event_id,
    geo_id,
    event_date,
    year,
    name,
    short_label,
    summary,
    category,
    impact_level,
    source_url
FROM tmp_policy_events
ON CONFLICT (event_id) DO UPDATE
SET geo_id = EXCLUDED.geo_id,
    event_date = EXCLUDED.event_date,
    year = EXCLUDED.year,
    name = EXCLUDED.name,
    short_label = EXCLUDED.short_label,
    summary = EXCLUDED.summary,
    category = EXCLUDED.category,
    impact_level = EXCLUDED.impact_level,
    source_url = EXCLUDED.source_url;

COMMIT;
