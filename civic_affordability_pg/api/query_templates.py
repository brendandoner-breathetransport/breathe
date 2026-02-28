import re
from dataclasses import dataclass
from typing import Any


MAX_ROWS = 50


@dataclass
class QueryPlan:
    category: str
    template_id: str
    intent: str
    sql: str
    params: dict[str, Any]
    summary: str
    extracted_years: list[int]
    is_inflation_adjusted: bool


def _extract_years(question: str) -> list[int]:
    return [int(y) for y in re.findall(r"\b(?:19|20)\d{2}\b", question)]


def _is_inflation_adjusted_question(question: str) -> bool:
    keywords = ["inflation", "real terms", "cpi", "constant dollars", "adjusted"]
    return any(k in question for k in keywords)


def build_query_plan(question: str, state: str = "CO") -> QueryPlan:
    q = (question or "").strip().lower()
    years = _extract_years(q)
    inflation_adjusted = _is_inflation_adjusted_question(q)
    income_col = "income_cpi_2023_index" if inflation_adjusted else "income_index"
    healthcare_col = "healthcare_cpi_2023_index" if inflation_adjusted else "healthcare_index"
    childcare_col = "childcare_cpi_2023_index" if inflation_adjusted else "childcare_index"

    if not q:
        raise ValueError("Question cannot be empty.")

    if ("largest" in q or "biggest" in q or "max" in q) and "gap" in q:
        return QueryPlan(
            category="largest_affordability_gap_year",
            template_id="largest_affordability_gap_year_v1",
            intent="largest_gap",
            sql=(
                "SELECT geo_id, state_abbrev, year, cost_pressure_index, affordability_gap_index "
                "FROM analytics.mart_cost_pressure_annual "
                "WHERE state_abbrev = %(state)s "
                "ORDER BY affordability_gap_index DESC "
                "LIMIT 1"
            ),
            params={"state": state},
            summary="Largest affordability gap year",
            extracted_years=years,
            is_inflation_adjusted=False,
        )

    if "before" in q and "after" in q and len(years) >= 2:
        y1, y2 = years[0], years[1]
        return QueryPlan(
            category="before_after_comparison",
            template_id="before_after_comparison_v1",
            intent="before_after",
            sql=(
                f"SELECT year, {income_col} AS income_index, housing_index, {healthcare_col} AS healthcare_index, {childcare_col} AS childcare_index "
                "FROM analytics.mart_affordability_index_annual "
                "WHERE state_abbrev = %(state)s AND year IN (%(year_one)s, %(year_two)s) "
                "ORDER BY year "
                "LIMIT %(limit)s"
            ),
            params={"state": state, "year_one": y1, "year_two": y2, "limit": MAX_ROWS},
            summary=f"Before/after comparison for {y1} and {y2}" + (" (inflation-adjusted)" if inflation_adjusted else ""),
            extracted_years=years,
            is_inflation_adjusted=inflation_adjusted,
        )

    if "compare" in q and any(c in q for c in ["income", "housing", "healthcare", "childcare", "component"]):
        return QueryPlan(
            category="component_comparison",
            template_id="component_comparison_latest_v1",
            intent="component_comparison",
            sql=(
                f"SELECT year, {income_col} AS income_index, housing_index, {healthcare_col} AS healthcare_index, {childcare_col} AS childcare_index "
                "FROM analytics.mart_affordability_index_annual "
                "WHERE state_abbrev = %(state)s "
                "ORDER BY year DESC "
                "LIMIT 1"
            ),
            params={"state": state},
            summary="Latest component comparison" + (" (inflation-adjusted)" if inflation_adjusted else ""),
            extracted_years=years,
            is_inflation_adjusted=inflation_adjusted,
        )

    if "policy" in q or "event" in q:
        if years:
            return QueryPlan(
                category="policy_year_impact",
                template_id="policy_year_impact_v1",
                intent="policy_impact",
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
                extracted_years=years,
                is_inflation_adjusted=False,
            )
        return QueryPlan(
            category="policy_events",
            template_id="policy_events_recent_v1",
            intent="policy_events",
            sql=(
                "SELECT year, short_label, summary, category "
                "FROM analytics.mart_policy_events_direct "
                "WHERE state_abbrev = %(state)s "
                "ORDER BY year DESC "
                "LIMIT %(limit)s"
            ),
            params={"state": state, "limit": MAX_ROWS},
            summary="Recent direct policy events",
            extracted_years=years,
            is_inflation_adjusted=False,
        )

    return QueryPlan(
        category="trend_summary",
        template_id="trend_summary_v1",
        intent="trend_summary",
        sql=(
            f"SELECT year, {income_col} AS income_index, housing_index, {healthcare_col} AS healthcare_index, {childcare_col} AS childcare_index "
            "FROM analytics.mart_affordability_index_annual "
            "WHERE state_abbrev = %(state)s "
            "ORDER BY year "
            "LIMIT %(limit)s"
        ),
        params={"state": state, "limit": MAX_ROWS},
        summary="Trend summary" + (" (inflation-adjusted)" if inflation_adjusted else ""),
        extracted_years=years,
        is_inflation_adjusted=inflation_adjusted,
    )
