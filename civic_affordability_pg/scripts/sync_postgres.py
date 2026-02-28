from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
import psycopg


ROOT = Path(__file__).resolve().parents[1]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def execute_sql_file(cur: psycopg.Cursor, path: Path) -> None:
    sql = path.read_text()
    cur.execute(sql)


def upsert_dim_time(cur: psycopg.Cursor, years: list[int]) -> None:
    rows = [(year, year, "annual") for year in sorted(set(years))]
    cur.executemany(
        """
        INSERT INTO raw.dim_time (period_id, year, frequency)
        VALUES (%s, %s, %s)
        ON CONFLICT (period_id) DO UPDATE
        SET year = EXCLUDED.year,
            frequency = EXCLUDED.frequency
        """,
        rows,
    )


def upsert_fact_metric(cur: psycopg.Cursor, aff: pd.DataFrame) -> None:
    metric_map = {
        1: "income_real",
        2: "housing_hpi",
        3: "healthcare_pc",
        4: "childcare_annual",
    }
    rows: list[tuple] = []
    for rec in aff.to_dict(orient="records"):
        for metric_id, column in metric_map.items():
            rows.append(
                (
                    int(rec["geo_id"]),
                    int(rec["year"]),
                    int(metric_id),
                    float(rec[column]),
                    1,
                )
            )
    cur.executemany(
        """
        INSERT INTO raw.fact_metric (geo_id, period_id, metric_id, value, source_id, vintage_date)
        VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
        ON CONFLICT (geo_id, period_id, metric_id) DO UPDATE
        SET value = EXCLUDED.value,
            source_id = EXCLUDED.source_id,
            vintage_date = EXCLUDED.vintage_date
        """,
        rows,
    )


def upsert_policy_events(cur: psycopg.Cursor, policy: pd.DataFrame) -> None:
    rows = []
    for rec in policy.to_dict(orient="records"):
        rows.append(
            (
                int(rec["event_id"]),
                int(rec["geo_id"]),
                rec["event_date"],
                int(rec["year"]),
                rec["name"],
                rec["short_label"],
                rec["summary"],
                rec["category"],
                rec["impact_level"],
                rec["source_url"],
            )
        )
    cur.executemany(
        """
        INSERT INTO raw.fact_policy_event (
            event_id, geo_id, event_date, year, name, short_label, summary, category, impact_level, source_url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (event_id) DO UPDATE
        SET geo_id = EXCLUDED.geo_id,
            event_date = EXCLUDED.event_date,
            year = EXCLUDED.year,
            name = EXCLUDED.name,
            short_label = EXCLUDED.short_label,
            summary = EXCLUDED.summary,
            category = EXCLUDED.category,
            impact_level = EXCLUDED.impact_level,
            source_url = EXCLUDED.source_url
        """,
        rows,
    )


def create_analytics_views(cur: psycopg.Cursor, base_year: int) -> None:
    cur.execute(
        f"""
        CREATE OR REPLACE VIEW analytics.mart_affordability_index_annual AS
        WITH metric_values AS (
            SELECT
                fm.geo_id,
                dt.year,
                dg.state_abbrev,
                dm.metric_name,
                fm.value
            FROM raw.fact_metric fm
            JOIN raw.dim_time dt ON dt.period_id = fm.period_id
            JOIN raw.dim_geo dg ON dg.geo_id = fm.geo_id
            JOIN raw.dim_metric dm ON dm.metric_id = fm.metric_id
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
                MAX(CASE WHEN year = {base_year} THEN income_real END) AS income_base,
                MAX(CASE WHEN year = {base_year} THEN housing_hpi END) AS housing_base,
                MAX(CASE WHEN year = {base_year} THEN healthcare_pc END) AS healthcare_base,
                MAX(CASE WHEN year = {base_year} THEN childcare_annual END) AS childcare_base
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
        JOIN base_values b ON b.geo_id = w.geo_id;
        """
    )

    cur.execute(
        """
        CREATE OR REPLACE VIEW analytics.mart_cost_pressure_annual AS
        WITH affordability AS (
            SELECT * FROM analytics.mart_affordability_index_annual
        )
        SELECT
            geo_id,
            state_abbrev,
            year,
            (housing_index + healthcare_index + childcare_index) / 3.0 AS cost_pressure_index,
            ((housing_index + healthcare_index + childcare_index) / 3.0) - income_index AS affordability_gap_index
        FROM affordability;
        """
    )

    cur.execute(
        """
        CREATE OR REPLACE VIEW analytics.mart_policy_events_direct AS
        SELECT
            fpe.event_id,
            fpe.geo_id,
            dg.state_abbrev,
            fpe.year,
            fpe.short_label,
            fpe.summary,
            fpe.category
        FROM raw.fact_policy_event fpe
        JOIN raw.dim_geo dg ON dg.geo_id = fpe.geo_id
        WHERE fpe.impact_level = 'direct';
        """
    )


def verify(cur: psycopg.Cursor) -> None:
    checks = {
        "raw.fact_metric": "SELECT COUNT(*) FROM raw.fact_metric",
        "raw.fact_policy_event": "SELECT COUNT(*) FROM raw.fact_policy_event",
        "analytics.mart_affordability_index_annual": "SELECT COUNT(*) FROM analytics.mart_affordability_index_annual",
        "analytics.mart_cost_pressure_annual": "SELECT COUNT(*) FROM analytics.mart_cost_pressure_annual",
        "analytics.mart_policy_events_direct": "SELECT COUNT(*) FROM analytics.mart_policy_events_direct",
    }
    for name, sql in checks.items():
        cur.execute(sql)
        count = cur.fetchone()[0]
        print(f"{name}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Civic Affordability MVP schema and data")
    parser.add_argument("--base-year", type=int, default=2003)
    args = parser.parse_args()

    load_env_file(ROOT / ".env")
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not found. Set it in environment or civic_affordability_pg/.env")

    aff_path = ROOT / "seeds" / "co_affordability_index_annual.csv"
    policy_path = ROOT / "seeds" / "co_policy_events_direct.csv"
    aff = pd.read_csv(aff_path)
    policy = pd.read_csv(policy_path)

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            execute_sql_file(cur, ROOT / "sql" / "001_init.sql")
            execute_sql_file(cur, ROOT / "sql" / "002_seed.sql")
            upsert_dim_time(cur, aff["year"].tolist())
            upsert_fact_metric(cur, aff)
            upsert_policy_events(cur, policy)
            create_analytics_views(cur, base_year=args.base_year)
            verify(cur)
        conn.commit()

    print("Sync complete.")


if __name__ == "__main__":
    main()
