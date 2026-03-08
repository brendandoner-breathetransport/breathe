CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS raw.dim_geo (
    geo_id INTEGER PRIMARY KEY,
    state_name TEXT NOT NULL,
    state_abbrev TEXT NOT NULL UNIQUE,
    fips TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS raw.dim_time (
    period_id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL UNIQUE,
    frequency TEXT NOT NULL CHECK (frequency IN ('annual'))
);

CREATE TABLE IF NOT EXISTS raw.dim_metric (
    metric_id INTEGER PRIMARY KEY,
    metric_name TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL CHECK (domain IN ('income', 'housing', 'healthcare', 'childcare')),
    unit TEXT NOT NULL,
    measure_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.dim_source (
    source_id INTEGER PRIMARY KEY,
    source_name TEXT NOT NULL,
    publisher TEXT NOT NULL,
    url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.fact_metric (
    geo_id INTEGER NOT NULL REFERENCES raw.dim_geo (geo_id),
    period_id INTEGER NOT NULL REFERENCES raw.dim_time (period_id),
    metric_id INTEGER NOT NULL REFERENCES raw.dim_metric (metric_id),
    value NUMERIC(18, 4) NOT NULL,
    source_id INTEGER NOT NULL REFERENCES raw.dim_source (source_id),
    vintage_date DATE NOT NULL,
    PRIMARY KEY (geo_id, period_id, metric_id)
);

CREATE TABLE IF NOT EXISTS raw.fact_policy_event (
    event_id INTEGER PRIMARY KEY,
    geo_id INTEGER NOT NULL REFERENCES raw.dim_geo (geo_id),
    event_date DATE NOT NULL,
    year INTEGER NOT NULL,
    name TEXT NOT NULL,
    short_label TEXT NOT NULL,
    summary TEXT NOT NULL,
    category TEXT NOT NULL,
    impact_level TEXT NOT NULL CHECK (impact_level IN ('direct', 'indirect', 'minimal')),
    source_url TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fact_metric_geo_period ON raw.fact_metric (geo_id, period_id);
CREATE INDEX IF NOT EXISTS idx_policy_event_geo_year ON raw.fact_policy_event (geo_id, year);
