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


def _format_float(value: Any) -> str:
    try:
        return f"{float(value):.1f}"
    except Exception:
        return str(value)


def _compose_answer(plan_category: str, rows: list[dict[str, Any]], state: str) -> str:
    if not rows:
        return f"No matching data was found for {state} with the current query template."

    first = rows[0]

    if plan_category == "largest_affordability_gap_year":
        year = first.get("year")
        gap = _format_float(first.get("affordability_gap_index"))
        return f"The largest affordability gap in {state} occurred in {year}, at approximately {gap} index points."

    if plan_category == "before_after_comparison":
        if len(rows) >= 2:
            start = rows[0]
            end = rows[-1]
            delta_income = float(end.get("income_index", 0)) - float(start.get("income_index", 0))
            delta_housing = float(end.get("housing_index", 0)) - float(start.get("housing_index", 0))
            return (
                f"From {start.get('year')} to {end.get('year')} in {state}, "
                f"income index changed by {delta_income:+.1f} and housing index changed by {delta_housing:+.1f}."
            )
        return "I found one of the requested years, but not enough rows to compare both years."

    if plan_category == "component_comparison":
        components = {
            "income": float(first.get("income_index", 0)),
            "housing": float(first.get("housing_index", 0)),
            "healthcare": float(first.get("healthcare_index", 0)),
            "childcare": float(first.get("childcare_index", 0)),
        }
        top_component, top_value = max(components.items(), key=lambda item: item[1])
        return (
            f"For {state} in {first.get('year')}, the highest indexed component is "
            f"{top_component} at {top_value:.1f}."
        )

    if plan_category == "policy_year_impact":
        year = first.get("year")
        return f"I found {len(rows)} direct policy event row(s) for {state} in {year} with affordability context."

    if plan_category == "policy_events":
        return f"I found {len(rows)} recent direct policy event row(s) for {state}."

    if plan_category == "trend_summary":
        start = rows[0]
        end = rows[-1]
        return (
            f"Trend summary for {state}: from {start.get('year')} to {end.get('year')}, "
            f"income index moved from {_format_float(start.get('income_index'))} to {_format_float(end.get('income_index'))}, "
            f"while housing moved from {_format_float(start.get('housing_index'))} to {_format_float(end.get('housing_index'))}."
        )

    return "I found matching data and returned the result rows."


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
            "income_real_cpi_2023, healthcare_pc_cpi_2023, childcare_annual_cpi_2023, "
            "income_index, housing_index, healthcare_index, childcare_index, "
            "income_cpi_2023_index, healthcare_cpi_2023_index, childcare_cpi_2023_index "
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

    warnings: list[str] = []
    confidence = "high"
    if len(rows) == 0:
        confidence = "low"
        warnings.append("No rows matched this question. Try adding a specific year or metric.")
    elif len(rows) < 2 and plan.category in {"before_after_comparison", "trend_summary"}:
        confidence = "medium"
        warnings.append("Limited result rows reduced comparison confidence.")

    return {
        "category": plan.category,
        "summary": plan.summary,
        "answer_text": _compose_answer(plan.category, rows, state),
        "query_template": plan.template_id,
        "query_sql": plan.sql,
        "query_params": plan.params,
        "confidence": confidence,
        "warnings": warnings,
        "row_count": len(rows),
        "table_rows": rows[:MAX_ROWS],
        "approved_marts": sorted(ALLOWED_TABLES),
    }
