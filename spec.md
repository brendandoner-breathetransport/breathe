# Civic Affordability Intelligence – MVP Specification

## 🎯 Product Goal

Build a minimal, production-ready web application that:

- Displays affordability trends for a single U.S. state (Colorado for MVP)
- Indexes Income, Housing, Healthcare, and Childcare to a base year (2003 = 100)
- Overlays Direct Ballot Measures affecting affordability
- Allows limited AI-based natural language queries against approved datasets
- Supports CSV download of the indexed dataset and policy events

This is a lean MVP intended to validate demand before multi-state expansion.

---

# 🧱 System Architecture

## Backend
- Supabase (Postgres)
- dbt Core
- Analytics schema for marts
- Raw schema for base data

## Frontend
- Next.js
- Deployed on Vercel
- Single state dashboard page

## AI Layer
- OpenAI API
- Strictly limited to querying approved dbt marts
- No direct raw table access

---

# 📊 Data Model

## Schemas

- `raw`
- `analytics`

---

## Core Tables (raw)

### raw.dim_geo
- geo_id (PK)
- state_name
- state_abbrev
- fips

### raw.dim_time
- period_id (PK)
- year
- frequency (annual only for MVP)

### raw.dim_metric
- metric_id (PK)
- metric_name
- domain (income, housing, healthcare, childcare)
- unit
- measure_type

### raw.dim_source
- source_id (PK)
- source_name
- publisher
- url

### raw.fact_metric
Primary key: (geo_id, period_id, metric_id)

Columns:
- geo_id (FK)
- period_id (FK)
- metric_id (FK)
- value
- source_id
- vintage_date

### raw.fact_policy_event
- event_id (PK)
- geo_id
- event_date
- year
- name
- short_label
- summary
- category
- impact_level (direct / indirect / minimal)
- source_url

---

# 📈 dbt Marts (analytics schema)

## 1. mart_affordability_index_annual

Grain: geo_id, year

Columns:
- geo_id
- state_abbrev
- year
- income_real
- housing_hpi
- healthcare_pc
- childcare_annual
- income_index
- housing_index
- healthcare_index
- childcare_index

Indexing:
All index columns use base year = 2003 (configurable dbt var)

---

## 2. mart_cost_pressure_annual

Grain: geo_id, year

Columns:
- geo_id
- state_abbrev
- year
- cost_pressure_index
- affordability_gap_index

Definitions:
cost_pressure_index = average(housing_index, healthcare_index, childcare_index)

affordability_gap_index = cost_pressure_index - income_index

---

## 3. mart_policy_events_direct

Filter:
impact_level = 'direct'

Columns:
- event_id
- geo_id
- state_abbrev
- year
- short_label
- summary
- category

---

# 🖥 Frontend Layout

## Route Structure

- `/`
- `/state/co`
- `/api/affordability`
- `/api/policy`
- `/api/ask`

---

## Dashboard Components

1. Header
   - Title
   - State selector (Colorado only for MVP)
   - Toggle: Show policy markers

2. Summary Cards
   - Income Index (latest year)
   - Housing Index
   - Healthcare Index
   - Childcare Index
   - Cost Pressure Index
   - Affordability Gap

3. Main Chart
   - Four indexed series
   - Hover tooltips
   - Policy markers (dashed vertical lines)
   - Numbered markers with legend box

4. Download Section
   - CSV: Affordability dataset
   - CSV: Direct policy events

5. Ask the Data
   - Limited natural language input
   - Template-based SQL generation only
   - No arbitrary SQL execution

---

# 🤖 AI Guardrails

The AI layer must:

- Only query:
  - analytics.mart_affordability_index_annual
  - analytics.mart_cost_pressure_annual
  - analytics.mart_policy_events_direct
- Use SELECT statements only
- Reject DDL or DML operations
- Limit results to 50 rows max
- Use predefined query templates

Allowed question categories:
- Trend summary
- Before/after year comparison
- Largest affordability gap year
- Component comparison
- Policy year impact

Disallowed:
- Schema introspection
- Raw SQL from user
- Internet lookups
- Cross-state comparisons (MVP)

---

# 🚫 Explicit Non-Goals (MVP)

Do NOT implement:

- Multi-state comparison UI
- Maps
- User authentication
- Payments
- Automated data ingestion
- Complex filtering beyond policy toggle
- Indirect policy overlay

---

# 📦 Naming Conventions

- snake_case for all tables and columns
- stg_ prefix for staging models
- mart_ prefix for final models
- geo_id format: US-CO

---

# 🧪 dbt Tests Required

- uniqueness of fact_metric composite key
- not_null on primary keys
- relationships between facts and dims
- no duplicate years in marts
- index columns must not be null

---

# 🚀 Definition of Done (MVP)

- Colorado dashboard loads successfully
- Indexed data accurate (2003 = 100)
- Policy overlay readable
- CSV downloads work
- AI responds accurately to 5–10 sample questions
- dbt build + dbt test pass
- Deployed publicly

---

# 🔮 Future Expansion (Not MVP)

- Add additional states
- Multi-state compare
- Paid API tier
- Policy intensity scoring
- Automated data refresh jobs
- Map visualization

---

This file defines the scope and constraints for Codex.
Codex should not add features beyond this specification without explicit instruction.