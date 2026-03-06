import os
import re
from typing import Any
from datetime import datetime, timezone
from decimal import Decimal
from html import unescape
from urllib.parse import quote_plus

import httpx
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
GOOGLE_CIVIC_API_KEY = os.getenv("GOOGLE_CIVIC_API_KEY", "")
GOOGLE_CIVIC_BASE_URL = "https://www.googleapis.com/civicinfo/v2"
COLORADO_VOTER_LOOKUP_URL = "https://www.sos.state.co.us/voter/pages/pub/olvr/findVoterReg.xhtml"
TENNESSEE_VOTER_LOOKUP_URL = "https://web.go-vote-tn.elections.tn.gov/"
VOTING_INFO_PROJECT_URL = "https://www.votinginfoproject.org/"
SUPPORTED_POLLING_STATES = {"CO", "TN"}
STATE_NAME_BY_ABBREV = {"CO": "Colorado", "TN": "Tennessee"}

app = FastAPI(title="Civic Affordability API", version="0.1.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    state_abbrev: str = Field(default="CO", min_length=2, max_length=2)


class PollingLookupRequest(BaseModel):
    street: str = Field(min_length=3, max_length=200)
    city: str = Field(min_length=2, max_length=100)
    zip: str = Field(min_length=5, max_length=10)
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


TEMPLATE_CITATION_MAP = {
    "largest_affordability_gap_year": {
        "dataset": "analytics.mart_cost_pressure_annual",
        "metric_columns_nominal": ["cost_pressure_index", "affordability_gap_index"],
        "metric_columns_inflation_adjusted": ["cost_pressure_index", "affordability_gap_index"],
    },
    "before_after_comparison": {
        "dataset": "analytics.mart_affordability_index_annual",
        "metric_columns_nominal": ["income_index", "housing_index", "healthcare_index", "childcare_index"],
        "metric_columns_inflation_adjusted": ["income_cpi_2023_index", "housing_index", "healthcare_cpi_2023_index", "childcare_cpi_2023_index"],
    },
    "component_comparison": {
        "dataset": "analytics.mart_affordability_index_annual",
        "metric_columns_nominal": ["income_index", "housing_index", "healthcare_index", "childcare_index"],
        "metric_columns_inflation_adjusted": ["income_cpi_2023_index", "housing_index", "healthcare_cpi_2023_index", "childcare_cpi_2023_index"],
    },
    "policy_year_impact": {
        "dataset": "analytics.mart_policy_events_direct + analytics.mart_cost_pressure_annual",
        "metric_columns_nominal": ["short_label", "category", "cost_pressure_index", "affordability_gap_index"],
        "metric_columns_inflation_adjusted": ["short_label", "category", "cost_pressure_index", "affordability_gap_index"],
    },
    "policy_events": {
        "dataset": "analytics.mart_policy_events_direct",
        "metric_columns_nominal": ["year", "short_label", "summary", "category"],
        "metric_columns_inflation_adjusted": ["year", "short_label", "summary", "category"],
    },
    "trend_summary": {
        "dataset": "analytics.mart_affordability_index_annual",
        "metric_columns_nominal": ["income_index", "housing_index", "healthcare_index", "childcare_index"],
        "metric_columns_inflation_adjusted": ["income_cpi_2023_index", "housing_index", "healthcare_cpi_2023_index", "childcare_cpi_2023_index"],
    },
}

DOMAIN_SOURCE_REFERENCE = {
    "income": {
        "source_name": "Historical Income Tables",
        "publisher": "U.S. Census Bureau",
        "source_url": "https://www.census.gov/topics/income-poverty/income/data/tables.html",
    },
    "housing": {
        "source_name": "House Price Index (HPI)",
        "publisher": "Federal Housing Finance Agency (FHFA)",
        "source_url": "https://www.fhfa.gov/data/hpi",
    },
    "healthcare": {
        "source_name": "National Health Expenditure Data",
        "publisher": "Centers for Medicare & Medicaid Services (CMS)",
        "source_url": "https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data",
    },
    "childcare": {
        "source_name": "Child Care Cost Data",
        "publisher": "Child Care Aware of America",
        "source_url": "https://www.childcareaware.org/thechildcarechallenge/",
    },
    "policy": {
        "source_name": "Colorado Ballot Measure Archive",
        "publisher": "Ballotpedia",
        "source_url": "https://ballotpedia.org/Colorado",
    },
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


def _build_citations(
    category: str,
    grounding: dict[str, Any],
    is_inflation_adjusted: bool,
) -> list[dict[str, Any]]:
    config = TEMPLATE_CITATION_MAP.get(category)
    if not config:
        return []

    metric_columns = (
        config["metric_columns_inflation_adjusted"]
        if is_inflation_adjusted
        else config["metric_columns_nominal"]
    )
    domains_by_category = {
        "largest_affordability_gap_year": ["income", "housing", "healthcare", "childcare"],
        "before_after_comparison": ["income", "housing", "healthcare", "childcare"],
        "component_comparison": ["income", "housing", "healthcare", "childcare"],
        "trend_summary": ["income", "housing", "healthcare", "childcare"],
        "policy_year_impact": ["policy", "income", "housing", "healthcare", "childcare"],
        "policy_events": ["policy"],
    }
    external_sources = [
        {
            "domain": domain,
            **DOMAIN_SOURCE_REFERENCE[domain],
        }
        for domain in domains_by_category.get(category, [])
        if domain in DOMAIN_SOURCE_REFERENCE
    ]
    year_min = grounding.get("year_min")
    year_max = grounding.get("year_max")
    year_range = f"{year_min}-{year_max}" if year_min is not None and year_max is not None else "n/a"
    return [
        {
            "dataset": config["dataset"],
            "metric_columns": metric_columns,
            "state": grounding.get("state"),
            "year_range": year_range,
            "row_count_used": grounding.get("rows_used", 0),
            "method_note": "Template-based SQL query with approved marts only and MAX_ROWS=50.",
            "external_sources": external_sources,
        }
    ]


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


def _build_full_address(street: str, city: str, state_abbrev: str, zip_code: str) -> str:
    return f"{street.strip()}, {city.strip()}, {state_abbrev.strip().upper()} {zip_code.strip()}"


def _format_location_address(address: dict[str, Any] | None) -> str:
    if not address:
        return ""
    parts = [
        address.get("line1"),
        address.get("line2"),
        address.get("line3"),
        ", ".join(
            p for p in [address.get("city"), address.get("state"), address.get("zip")] if p
        ),
    ]
    return ", ".join([p for p in parts if p])


def _state_fallback_lookup_url(state_abbrev: str) -> str:
    state = (state_abbrev or "").upper()
    if state == "TN":
        return TENNESSEE_VOTER_LOOKUP_URL
    return COLORADO_VOTER_LOOKUP_URL


def _extract_source_url(sources: list[dict[str, Any]], state_abbrev: str) -> str:
    for source in sources:
        official = source.get("official")
        if official:
            return str(official)
    return _state_fallback_lookup_url(state_abbrev)


def _normalize_locations(raw_items: list[dict[str, Any]], location_type: str, state_abbrev: str) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in raw_items:
        address_obj = item.get("address", {})
        full_address = _format_location_address(address_obj)
        source_list = item.get("sources", []) or []
        normalized.append(
            {
                "location_type": location_type,
                "name": item.get("addressLocationName") or item.get("name") or "Polling Location",
                "address": full_address,
                "hours": item.get("pollingHours") or item.get("earlyVoteSiteHours") or None,
                "notes": item.get("notes"),
                "source_name": source_list[0].get("name") if source_list else "Voting Information Project",
                "source_url": _extract_source_url(source_list, state_abbrev),
                "maps_url": f"https://www.google.com/maps/search/?api=1&query={quote_plus(full_address)}" if full_address else None,
            }
        )
    return normalized


def _build_provider_plan(state_abbrev: str) -> list[dict[str, Any]]:
    official_url = _state_fallback_lookup_url(state_abbrev)
    state_name = STATE_NAME_BY_ABBREV.get(state_abbrev.upper(), state_abbrev.upper())
    return [
        {
            "provider_id": "state_official",
            "provider_name": f"{state_name} Secretary of State Lookup",
            "priority": 1,
            "mode": "official_lookup",
            "url": official_url,
            "notes": "Most authoritative source for current polling place details.",
        },
        {
            "provider_id": "vip",
            "provider_name": "Voting Information Project",
            "priority": 2,
            "mode": "national_nonprofit",
            "url": VOTING_INFO_PROJECT_URL,
            "notes": "National voter information provider with broader coverage tools.",
        },
        {
            "provider_id": "google_civic",
            "provider_name": "Google Civic Information API",
            "priority": 3,
            "mode": "api",
            "url": "https://developers.google.com/civic-information/docs/v2/voterinfo",
            "notes": "Used as a supplementary API source when election context is available.",
        },
    ]


def _strip_html(value: str) -> str:
    if not value:
        return ""
    no_tags = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(no_tags)).strip()


def _build_maps_url_from_address(address: str) -> str | None:
    clean = (address or "").strip()
    if not clean:
        return None
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(clean)}"


def _parse_tn_locations_list_page(html: str, type_param: str) -> list[dict[str, Any]]:
    if not html:
        return []
    forms = re.findall(r"<form method=\"GET\">(.*?)</form>", html, flags=re.S | re.I)
    parsed: list[dict[str, Any]] = []
    for form in forms:
        view_match = re.search(r'name=\"view\"\s+value=\"([^\"]+)\"', form, flags=re.I)
        if not view_match:
            continue
        # Top line is the location name; secondary line is street address.
        div_values = re.findall(r"<div[^>]*>(.*?)</div>", form, flags=re.S | re.I)
        if not div_values:
            continue
        name = _strip_html(div_values[0])
        address = _strip_html(div_values[1]) if len(div_values) > 1 else ""
        if not name and not address:
            continue
        parsed.append(
            {
                "view": view_match.group(1),
                "type_param": type_param,
                "name": name or "Polling Location",
                "address": address,
            }
        )
    return parsed


def _parse_tn_location_detail_page(html: str) -> tuple[str | None, str | None]:
    if not html:
        return None, None
    hours_match = re.search(
        r"<label>\s*Hours:\s*</label>\s*<br/?>\s*<span>(.*?)</span>",
        html,
        flags=re.S | re.I,
    )
    hours = _strip_html(hours_match.group(1)) if hours_match else None
    maps_match = re.search(r'<form\s+action=\"(https://www\.google\.com/maps/dir/[^\"]+)\"', html, flags=re.I)
    maps_url = maps_match.group(1) if maps_match else None
    return hours, maps_url


def _lookup_tn_official_locations(client: httpx.Client, street: str, zip_code: str) -> tuple[list[dict[str, Any]], str | None]:
    base = TENNESSEE_VOTER_LOOKUP_URL.rstrip("/")
    # Initialize a session, then perform the official address lookup workflow.
    client.get(f"{base}/search", timeout=15.0)
    search_resp = client.post(
        f"{base}/search/address",
        data={"address": street.strip(), "zip": zip_code.strip()},
        headers={"Referer": f"{base}/search"},
        timeout=20.0,
    )
    search_html = search_resp.text
    if "No Results Returned" in search_html:
        return [], "No registered voters were found at this address in Tennessee official lookup."

    all_locations: list[dict[str, Any]] = []
    location_types = [("election-day", "polling_location"), ("early-voting", "early_vote_site")]
    for type_param, location_type in location_types:
        list_resp = client.get(f"{base}/locations/list", params={"type": type_param}, timeout=20.0)
        cards = _parse_tn_locations_list_page(list_resp.text, type_param)
        for card in cards:
            detail_resp = client.get(
                f"{base}/locations/list",
                params={"type": type_param, "view": card["view"]},
                timeout=20.0,
            )
            hours, maps_url = _parse_tn_location_detail_page(detail_resp.text)
            location_address = card["address"]
            all_locations.append(
                {
                    "location_type": location_type,
                    "name": card["name"],
                    "address": location_address,
                    "hours": hours,
                    "notes": None,
                    "source_name": "Tennessee Secretary of State",
                    "source_url": base,
                    "maps_url": maps_url or _build_maps_url_from_address(location_address),
                }
            )
    if not all_locations:
        return [], "No polling locations were returned by Tennessee official lookup for this address."
    return all_locations, None


def _get_state_election_id(client: httpx.Client, state_abbrev: str) -> str | None:
    state_name = STATE_NAME_BY_ABBREV.get(state_abbrev.upper())
    if not state_name:
        return None
    try:
        resp = client.get(
            f"{GOOGLE_CIVIC_BASE_URL}/elections",
            params={"key": GOOGLE_CIVIC_API_KEY},
            timeout=12.0,
        )
        if resp.status_code >= 400:
            return None
        payload = resp.json()
        elections = payload.get("elections", []) or []
        today = datetime.now(timezone.utc).date().isoformat()
        candidates = [
            e for e in elections
            if state_name.lower() in str(e.get("name", "")).lower()
            and str(e.get("electionDay", "")) >= today
        ]
        if not candidates:
            return None
        target = sorted(candidates, key=lambda e: str(e.get("electionDay", "")))[0]
        election_id = target.get("id")
        return str(election_id) if election_id is not None else None
    except Exception:
        return None


def _list_state_elections(client: httpx.Client, state_abbrev: str) -> list[dict[str, Any]]:
    state_name = STATE_NAME_BY_ABBREV.get(state_abbrev.upper())
    if not state_name:
        return []
    resp = client.get(
        f"{GOOGLE_CIVIC_BASE_URL}/elections",
        params={"key": GOOGLE_CIVIC_API_KEY},
        timeout=12.0,
    )
    if resp.status_code >= 400:
        return []
    payload = resp.json()
    elections = payload.get("elections", []) or []
    matches = [
        e for e in elections
        if state_name.lower() in str(e.get("name", "")).lower()
    ]
    return sorted(matches, key=lambda e: str(e.get("electionDay", "")))


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


@app.post("/api/vote/co/polling-location")
def get_colorado_polling_location(payload: PollingLookupRequest) -> dict[str, Any]:
    state = payload.state_abbrev.strip().upper()
    if state not in SUPPORTED_POLLING_STATES:
        raise HTTPException(status_code=400, detail="This endpoint currently supports CO and TN addresses only.")

    full_address = _build_full_address(payload.street, payload.city, state, payload.zip)
    official_fallback_url = _state_fallback_lookup_url(state)
    provider_plan = _build_provider_plan(state)

    if not GOOGLE_CIVIC_API_KEY:
        return {
            "status": "official_lookup_recommended",
            "message": "Primary official lookup is available. Civic API is not configured.",
            "request_address": full_address,
            "provider_used": "state_official",
            "providers": provider_plan,
            "official_fallback_url": official_fallback_url,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        }

    try:
        with httpx.Client() as client:
            tn_detail: str | None = None
            if state == "TN":
                tn_locations, tn_detail = _lookup_tn_official_locations(client, payload.street, payload.zip)
                if tn_locations:
                    return {
                        "status": "ok",
                        "message": "Polling locations found from Tennessee official lookup.",
                        "request_address": full_address,
                        "provider_used": "state_official",
                        "providers": provider_plan,
                        "result_count": len(tn_locations),
                        "locations": tn_locations,
                        "citations": [
                            {
                                "source_name": "Tennessee Secretary of State GoVoteTN",
                                "publisher": "Tennessee Secretary of State",
                                "source_url": TENNESSEE_VOTER_LOOKUP_URL,
                            },
                            {
                                "source_name": "Voting Information Project",
                                "publisher": "Voting Information Project",
                                "source_url": VOTING_INFO_PROJECT_URL,
                            },
                        ],
                        "official_fallback_url": official_fallback_url,
                        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                    }

            params: dict[str, Any] = {"key": GOOGLE_CIVIC_API_KEY, "address": full_address}

            response = client.get(f"{GOOGLE_CIVIC_BASE_URL}/voterinfo", params=params, timeout=15.0)
            if response.status_code >= 400:
                detail = ""
                try:
                    detail = response.json().get("error", {}).get("message", "")
                except Exception:
                    detail = response.text
                # Retry with a state-specific election id when Civic cannot infer election context.
                if "election unknown" in detail.lower():
                    state_election_id = _get_state_election_id(client, state)
                    if state_election_id:
                        retry_params: dict[str, Any] = {
                            "key": GOOGLE_CIVIC_API_KEY,
                            "address": full_address,
                            "electionId": state_election_id,
                        }
                        retry_response = client.get(
                            f"{GOOGLE_CIVIC_BASE_URL}/voterinfo",
                            params=retry_params,
                            timeout=15.0,
                        )
                        if retry_response.status_code < 400:
                            response = retry_response
                        else:
                            try:
                                detail = retry_response.json().get("error", {}).get("message", detail)
                            except Exception:
                                detail = retry_response.text or detail
                if response.status_code >= 400:
                    return {
                        "status": "official_lookup_recommended",
                        "message": "Civic API could not resolve a polling location. Use official state lookup.",
                        "provider_detail": tn_detail or detail,
                        "request_address": full_address,
                        "provider_used": "state_official",
                        "providers": provider_plan,
                        "official_fallback_url": official_fallback_url,
                        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                    }

            data = response.json()
            polling = _normalize_locations(data.get("pollingLocations", []) or [], "polling_location", state)
            early = _normalize_locations(data.get("earlyVoteSites", []) or [], "early_vote_site", state)
            drop_off = _normalize_locations(data.get("dropOffLocations", []) or [], "drop_off_location", state)
            all_locations = polling + early + drop_off

            if not all_locations:
                response_election = data.get("election", {}) if isinstance(data, dict) else {}
                return {
                    "status": "official_lookup_recommended",
                    "message": "No polling locations were returned by Civic. Use official state lookup.",
                    "request_address": full_address,
                    "election": {
                        "id": str(response_election.get("id")) if response_election.get("id") is not None else None,
                        "name": response_election.get("name"),
                        "date": response_election.get("electionDay"),
                    } if response_election else {},
                    "provider_detail": tn_detail,
                    "provider_used": "state_official",
                    "providers": provider_plan,
                    "official_fallback_url": official_fallback_url,
                    "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                }

            response_election = data.get("election", {}) if isinstance(data, dict) else {}
            return {
                "status": "ok",
                "message": "Polling locations found.",
                "request_address": full_address,
                "election": {
                    "id": str(response_election.get("id")) if response_election.get("id") is not None else None,
                    "name": response_election.get("name"),
                    "date": response_election.get("electionDay"),
                } if response_election else {},
                "provider_used": "google_civic",
                "providers": provider_plan,
                "result_count": len(all_locations),
                "locations": all_locations,
                "citations": [
                    {
                        "source_name": "Google Civic Information API",
                        "publisher": "Google / Voting Information Project",
                        "source_url": "https://developers.google.com/civic-information/docs/v2/voterinfo",
                    },
                    {
                        "source_name": "State Voter Lookup",
                        "publisher": "Secretary of State",
                        "source_url": official_fallback_url,
                    },
                ],
                "official_fallback_url": official_fallback_url,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
            }
    except Exception as exc:
        return {
            "status": "official_lookup_recommended",
            "message": "Polling API is temporarily unavailable. Use official state lookup.",
            "provider_detail": str(exc),
            "request_address": full_address,
            "provider_used": "state_official",
            "providers": provider_plan,
            "official_fallback_url": official_fallback_url,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        }


@app.get("/api/vote/debug/elections")
def debug_state_elections(
    state_abbrev: str = "TN",
    address: str | None = None,
    street: str | None = None,
    city: str | None = None,
    zip: str | None = None,
    limit: int = 8,
) -> dict[str, Any]:
    state = state_abbrev.strip().upper()
    if state not in SUPPORTED_POLLING_STATES:
        raise HTTPException(status_code=400, detail="Supported debug states: CO, TN.")
    if not GOOGLE_CIVIC_API_KEY:
        return {
            "status": "unavailable",
            "message": "Google Civic API key is not configured.",
            "state_abbrev": state,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        }

    if address and address.strip():
        full_address = address.strip()
    elif street and city and zip:
        full_address = _build_full_address(street, city, state, zip)
    else:
        full_address = None

    safe_limit = max(1, min(limit, 25))
    today = datetime.now(timezone.utc).date().isoformat()

    try:
        with httpx.Client() as client:
            elections = _list_state_elections(client, state)
            upcoming = [e for e in elections if str(e.get("electionDay", "")) >= today]
            selected = (upcoming or elections)[:safe_limit]

            probes: list[dict[str, Any]] = []
            if full_address:
                for e in selected:
                    election_id = e.get("id")
                    params: dict[str, Any] = {
                        "key": GOOGLE_CIVIC_API_KEY,
                        "address": full_address,
                    }
                    if election_id is not None:
                        params["electionId"] = str(election_id)
                    resp = client.get(
                        f"{GOOGLE_CIVIC_BASE_URL}/voterinfo",
                        params=params,
                        timeout=15.0,
                    )
                    detail = ""
                    payload: dict[str, Any] = {}
                    if resp.status_code >= 400:
                        try:
                            payload = resp.json()
                            detail = payload.get("error", {}).get("message", "")
                        except Exception:
                            detail = resp.text
                    else:
                        try:
                            payload = resp.json()
                        except Exception:
                            payload = {}

                    probes.append(
                        {
                            "election_id": str(election_id) if election_id is not None else None,
                            "election_name": e.get("name"),
                            "election_day": e.get("electionDay"),
                            "http_status": resp.status_code,
                            "provider_detail": detail or None,
                            "polling_count": len(payload.get("pollingLocations", []) or []) if isinstance(payload, dict) else 0,
                            "early_vote_count": len(payload.get("earlyVoteSites", []) or []) if isinstance(payload, dict) else 0,
                            "dropoff_count": len(payload.get("dropOffLocations", []) or []) if isinstance(payload, dict) else 0,
                        }
                    )

            return {
                "status": "ok",
                "state_abbrev": state,
                "state_name": STATE_NAME_BY_ABBREV.get(state, state),
                "today_utc": today,
                "candidate_elections_count": len(elections),
                "candidate_elections": [
                    {
                        "id": str(e.get("id")) if e.get("id") is not None else None,
                        "name": e.get("name"),
                        "date": e.get("electionDay"),
                    }
                    for e in selected
                ],
                "probe_address": full_address,
                "probes": probes,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
            }
    except Exception as exc:
        return {
            "status": "error",
            "message": "Election debug lookup failed.",
            "provider_detail": str(exc),
            "state_abbrev": state,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        }


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
        "citations": _build_citations(
            category=plan.category,
            grounding=grounding,
            is_inflation_adjusted=plan.is_inflation_adjusted,
        ),
        "question_guide": SUPPORTED_QUESTION_GUIDE,
        "approved_marts": sorted(ALLOWED_TABLES),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
