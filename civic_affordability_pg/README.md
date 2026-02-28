# Civic Affordability Postgres MVP

Separate implementation workspace for the `spec.md` Postgres + dbt + API stack. This does not modify the existing Shiny app.

## Included Components

- Postgres schema setup in `sql/001_init.sql`
- Base seed metadata in `sql/002_seed.sql`
- Seed data load script in `sql/003_load_seed_data.sql`
- Colorado seed files in `seeds/`
- dbt marts in `dbt/models/marts/`
- Guarded API (`/api/affordability`, `/api/policy`, `/api/ask`) in `api/`

## 1) Start Postgres

```bash
cd civic_affordability_pg
docker compose up -d
```

## 2) Initialize raw schema and load seed data

```bash
docker compose exec -T postgres psql -U postgres -d affordability -f /sql/001_init.sql
docker compose exec -T postgres psql -U postgres -d affordability -f /sql/002_seed.sql
docker compose exec -T postgres psql -U postgres -d affordability -f /sql/003_load_seed_data.sql
```

## 3) Run dbt marts

Configure a local dbt profile named `civic_affordability` pointing to the same Postgres DB, then run:

```bash
cd dbt
dbt run
```

This builds:

- `analytics.mart_affordability_index_annual`
- `analytics.mart_cost_pressure_annual`
- `analytics.mart_policy_events_direct`

## 4) Run the API

```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
```

## API Guardrails

- Only approved marts are queried
- Only templated `SELECT` statements are used
- Any DDL/DML tokens are rejected
- Results are capped at 50 rows

## Notes

- This is an MVP scaffold aligned to `spec.md` for Colorado-only data.
- The existing root-level app remains unchanged.
