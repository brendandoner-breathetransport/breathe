# Notebook Workspace

This folder is for ad-hoc data exploration against the Postgres analytics marts.

## Security
- Do not commit real credentials.
- Use a read-only DB user for notebooks.
- Store secrets in a local `.env` file or your shell environment.

## Setup
1. Create a local virtualenv (optional):
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Install notebook dependencies:
   - `pip install jupyter pandas sqlalchemy psycopg[binary] python-dotenv pyspark`
3. Copy env template and fill your readonly DB URL:
   - `cp .env.example .env`
4. Launch Jupyter from this folder:
   - `jupyter lab`

## Environment Variables
- `DATABASE_URL` (required)

Expected format:
`postgresql://readonly_user:[PASSWORD]@aws-0-us-west-2.pooler.supabase.com:5432/postgres`

## Starter Notebook
- `explore.ipynb` includes:
  - secure `DATABASE_URL` loading
  - connection test
  - sample query to `analytics.mart_expense_share_monthly_income_annual`

## Spark Shortcut API
This repo includes a tiny helper package for Spark reads from Postgres:

```python
from civic_io import io
df = io.read("analytics.mart_expense_share_monthly_income_annual")
```

Notes:
- It uses `DATABASE_URL` automatically.
- It expects a Spark environment where the PostgreSQL JDBC driver is available.
- You can pass your own Spark session: `io.read("analytics.mart_cost_pressure_annual", spark=spark)`.
