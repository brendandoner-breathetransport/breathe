import os
from typing import Any
from datetime import datetime, timezone
from decimal import Decimal

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


SUPPORTED_QUESTION_GUIDE = {
    "supported_categories": [
        "trend summary",
        "before/after year comparison",
        "largest affordability gap year",
        "component comparison",
        "policy year impact",
    ],
    "example_prompts": [
        "What was the largest affordability gap year?",
        "Compare before and after 2010 and 2023.",
        "Compare before and after 2010 and 2023 in inflation adjusted terms.",
        "How did policy impact in 2020?",
    ],
}


def _format_float(value: Any) -> str:
    try:
        return f"{float(value):.1f}"
    except Exception:
        return str(value)


def _json_safe(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    return value


def _normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{k: _json_safe(v) for k, v in row.items()} for row in rows]


def _validate_question_text(question: str) -> None:
    q = (question or "").strip().lower()
    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    blocked_patterns = [
        "drop ",
        "delete ",
        "truncate ",
        "alter ",
        "insert ",
        "update ",
        "select * from",
        "information_schema",
        "pg_catalog",
    ]
    if any(pattern in q for pattern in blocked_patterns):
        raise HTTPException(
            status_code=400,
            detail=(
                "This assistant only supports predefined affordability question templates. "
                "Please ask a trend, comparison, largest-gap, component, or policy-impact question."
            ),
        )


def _build_grounding(rows: list[dict[str, Any]], state: str) -> dict[str, Any]:
    years = [
        int(row["year"])
        for row in rows
        if "year" in row and str(row["year"]).isdigit()
    ]
    year_min = min(years) if years else None
    year_max = max(years) if years else None
    return {
        "state": state,
        "rows_used": len(rows),
        "year_min": year_min,
        "year_max": year_max,
    }


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


def _confidence_for_result(category: str, row_count: int, warnings: list[str]) -> str:
    if row_count == 0:
        return "low"
    if warnings:
        return "medium"
    if category in {"largest_affordability_gap_year", "component_comparison"} and row_count >= 1:
        return "high"
    if category in {"trend_summary", "before_after_comparison"} and row_count >= 2:
        return "high"
    return "medium"


def _follow_up_suggestions(category: str) -> list[str]:
    options = {
        "largest_affordability_gap_year": [
            "Compare the gap in that year versus 2010.",
            "What policy events happened around that year?",
        ],
        "before_after_comparison": [
            "Compare another year pair before and after a policy year.",
            "Show component comparison for the latest year.",
        ],
        "component_comparison": [
            "Show trend summary across all years.",
            "What was the largest affordability gap year?",
        ],
        "policy_year_impact": [
            "Compare affordability before and after that policy year.",
            "List all recent direct policy events.",
        ],
        "policy_events": [
            "Show policy impact for a specific year.",
            "Which year had the largest affordability gap?",
        ],
        "trend_summary": [
            "Compare before and after two specific years.",
            "Which year had the largest affordability gap?",
        ],
    }
    return options.get(category, ["Show trend summary.", "Compare before and after two years."])


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
    _validate_question_text(payload.question)
    try:
        plan = build_query_plan(payload.question, state=state)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                f"{exc} Supported asks: "
                + ", ".join(SUPPORTED_QUESTION_GUIDE["supported_categories"])
            ),
        ) from exc

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
    if not plan.extracted_years and plan.category == "before_after_comparison":
        warnings.append("No valid comparison years detected.")
    if len(rows) == 0:
        warnings.append("No rows matched this question. Try adding a specific year or metric.")
    elif len(rows) < 2 and plan.category in {"before_after_comparison", "trend_summary", "policy_year_impact"}:
        warnings.append("Limited result rows reduced comparison confidence.")
    if plan.is_inflation_adjusted:
        warnings.append("Inflation-adjusted mode inferred from your question keywords.")

    normalized_rows = _normalize_rows(rows)
    confidence = _confidence_for_result(plan.category, len(normalized_rows), warnings)
    grounding = _build_grounding(normalized_rows, state)
    answer_text = _compose_answer(plan.category, normalized_rows, state)
    if grounding["year_min"] is not None:
        answer_text += (
            f" Based on {grounding['rows_used']} row(s) from {grounding['state']} "
            f"covering {grounding['year_min']} to {grounding['year_max']}."
        )

    return {
        "status": "ok",
        "category": plan.category,
        "intent": plan.intent,
        "summary": plan.summary,
        "answer_text": answer_text,
        "query_template": plan.template_id,
        "query_sql": plan.sql,
        "query_params": plan.params,
        "is_inflation_adjusted": plan.is_inflation_adjusted,
        "extracted_years": plan.extracted_years,
        "confidence": confidence,
        "warnings": warnings,
        "row_count": len(normalized_rows),
        "table_rows": normalized_rows[:MAX_ROWS],
        "table_columns": list(normalized_rows[0].keys()) if normalized_rows else [],
        "follow_up_suggestions": _follow_up_suggestions(plan.category),
        "grounding": grounding,
        "question_guide": SUPPORTED_QUESTION_GUIDE,
        "approved_marts": sorted(ALLOWED_TABLES),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
