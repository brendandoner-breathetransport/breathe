import os
from typing import Any

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from query_templates import MAX_ROWS, build_query_plan


ALLOWED_TABLES = {
    "analytics.mart_affordability_index_annual",
    "analytics.mart_cost_pressure_annual",
    "analytics.mart_policy_events_direct",
}

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/affordability")

app = FastAPI(title="Civic Affordability API", version="0.1.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    state_abbrev: str = Field(default="CO", min_length=2, max_length=2)


def _run_query(sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            columns = [desc.name for desc in cur.description]
            rows = cur.fetchall()
    return [dict(zip(columns, row)) for row in rows]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/affordability")
def get_affordability(state_abbrev: str = "CO") -> dict[str, Any]:
    rows = _run_query(
        (
            "SELECT geo_id, state_abbrev, year, income_real, housing_hpi, healthcare_pc, childcare_annual, "
            "income_index, housing_index, healthcare_index, childcare_index "
            "FROM analytics.mart_affordability_index_annual "
            "WHERE state_abbrev = %(state)s "
            "ORDER BY year "
            "LIMIT %(limit)s"
        ),
        {"state": state_abbrev.upper(), "limit": MAX_ROWS},
    )
    return {"rows": rows, "row_count": len(rows)}


@app.get("/api/policy")
def get_policy(state_abbrev: str = "CO") -> dict[str, Any]:
    rows = _run_query(
        (
            "SELECT event_id, geo_id, state_abbrev, year, short_label, summary, category "
            "FROM analytics.mart_policy_events_direct "
            "WHERE state_abbrev = %(state)s "
            "ORDER BY year "
            "LIMIT %(limit)s"
        ),
        {"state": state_abbrev.upper(), "limit": MAX_ROWS},
    )
    return {"rows": rows, "row_count": len(rows)}


@app.post("/api/ask")
def ask_data(payload: AskRequest) -> dict[str, Any]:
    state = payload.state_abbrev.upper()
    plan = build_query_plan(payload.question, state=state)

    # Guardrail: only analytics mart access and read-only SQL templates.
    normalized_sql = " ".join(plan.sql.lower().split())
    if not normalized_sql.startswith("select "):
        raise HTTPException(status_code=400, detail="Only SELECT statements are allowed.")
    if any(token in normalized_sql for token in ["insert", "update", "delete", "drop", "alter", "truncate"]):
        raise HTTPException(status_code=400, detail="DDL/DML operations are blocked.")
    if not any(table in normalized_sql for table in ALLOWED_TABLES):
        raise HTTPException(status_code=400, detail="Query must target approved marts only.")

    try:
        rows = _run_query(plan.sql, plan.params)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {exc}") from exc

    return {
        "category": plan.category,
        "summary": plan.summary,
        "row_count": len(rows),
        "rows": rows[:MAX_ROWS],
        "approved_marts": sorted(ALLOWED_TABLES),
    }
