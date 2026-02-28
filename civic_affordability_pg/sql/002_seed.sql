BEGIN;

INSERT INTO raw.dim_geo (geo_id, state_name, state_abbrev, fips)
VALUES (8, 'Colorado', 'CO', '08')
ON CONFLICT (geo_id) DO UPDATE
SET state_name = EXCLUDED.state_name,
    state_abbrev = EXCLUDED.state_abbrev,
    fips = EXCLUDED.fips;

INSERT INTO raw.dim_metric (metric_id, metric_name, domain, unit, measure_type)
VALUES
    (1, 'income_real', 'income', 'usd', 'level'),
    (2, 'housing_hpi', 'housing', 'index', 'level'),
    (3, 'healthcare_pc', 'healthcare', 'usd', 'level'),
    (4, 'childcare_annual', 'childcare', 'usd', 'level')
ON CONFLICT (metric_id) DO UPDATE
SET metric_name = EXCLUDED.metric_name,
    domain = EXCLUDED.domain,
    unit = EXCLUDED.unit,
    measure_type = EXCLUDED.measure_type;

INSERT INTO raw.dim_source (source_id, source_name, publisher, url)
VALUES
    (1, 'Civic Affordability MVP Seed', 'Internal Seed', 'https://example.local/seed')
ON CONFLICT (source_id) DO UPDATE
SET source_name = EXCLUDED.source_name,
    publisher = EXCLUDED.publisher,
    url = EXCLUDED.url;

COMMIT;
