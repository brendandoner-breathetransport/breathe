import re
from dataclasses import dataclass
from typing import Any


MAX_ROWS = 50


@dataclass
class QueryPlan:
    category: str
    sql: str
    params: dict[str, Any]
    summary: str


def _extract_years(question: str) -> list[int]:
    return [int(y) for y in re.findall(r"\b(?:19|20)\d{2}\b", question)]


def build_query_plan(question: str, state: str = "CO") -> QueryPlan:
    q = (question or "").strip().lower()
    years = _extract_years(q)

    if not q:
        raise ValueError("Question cannot be empty.")

    if ("largest" in q or "biggest" in q or "max" in q) and "gap" in q:
        return QueryPlan(
            category="largest_affordability_gap_year",
            sql=(
                "SELECT geo_id, state_abbrev, year, cost_pressure_index, income_index, affordability_gap_index "
                "FROM analytics.mart_cost_pressure_annual "
                "WHERE state_abbrev = %(state)s "
                "ORDER BY affordability_gap_index DESC "
                "LIMIT 1"
            ),
            params={"state": state},
            summary="Largest affordability gap year",
        )

    if "before" in q and "after" in q and len(years) >= 2:
        y1, y2 = years[0], years[1]
        return QueryPlan(
            category="before_after_comparison",
            sql=(
                "SELECT year, income_index, housing_index, healthcare_index, childcare_index "
                "FROM analytics.mart_affordability_index_annual "
                "WHERE state_abbrev = %(state)s AND year IN (%(year_one)s, %(year_two)s) "
                "ORDER BY year "
                "LIMIT %(limit)s"
            ),
            params={"state": state, "year_one": y1, "year_two": y2, "limit": MAX_ROWS},
            summary=f"Before/after comparison for {y1} and {y2}",
        )

    if "compare" in q and any(c in q for c in ["income", "housing", "healthcare", "childcare", "component"]):
        return QueryPlan(
            category="component_comparison",
            sql=(
                "SELECT year, income_index, housing_index, healthcare_index, childcare_index "
                "FROM analytics.mart_affordability_index_annual "
                "WHERE state_abbrev = %(state)s "
                "ORDER BY year DESC "
                "LIMIT 1"
            ),
            params={"state": state},
            summary="Latest component comparison",
        )

    if "policy" in q or "event" in q:
        if years:
            return QueryPlan(
                category="policy_year_impact",
                sql=(
                    "SELECT p.year, p.short_label, p.category, c.cost_pressure_index, c.affordability_gap_index "
                    "FROM analytics.mart_policy_events_direct p "
                    "LEFT JOIN analytics.mart_cost_pressure_annual c "
                    "ON p.geo_id = c.geo_id AND p.year = c.year "
                    "WHERE p.state_abbrev = %(state)s AND p.year = %(year)s "
                    "ORDER BY p.year, p.short_label "
                    "LIMIT %(limit)s"
                ),
                params={"state": state, "year": years[0], "limit": MAX_ROWS},
                summary=f"Policy impact in {years[0]}",
            )
        return QueryPlan(
            category="policy_events",
            sql=(
                "SELECT year, short_label, summary, category "
                "FROM analytics.mart_policy_events_direct "
                "WHERE state_abbrev = %(state)s "
                "ORDER BY year DESC "
                "LIMIT %(limit)s"
            ),
            params={"state": state, "limit": MAX_ROWS},
            summary="Recent direct policy events",
        )

    return QueryPlan(
        category="trend_summary",
        sql=(
            "SELECT year, income_index, housing_index, healthcare_index, childcare_index "
            "FROM analytics.mart_affordability_index_annual "
            "WHERE state_abbrev = %(state)s "
            "ORDER BY year "
            "LIMIT %(limit)s"
        ),
        params={"state": state, "limit": MAX_ROWS},
        summary="Trend summary",
    )
