import sys
import os
import json

# Allow importing data modules from the parent Breathe directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

# ---------------------------------------------------------------------------
# Data imports
# ---------------------------------------------------------------------------
from data.common_counties_json import counties_json
from data.economy_shares_wid import shares_wid
from data.economy_tax import tax
from data.economy_f150 import f150
from data.economy_house_purchase_cost_as_percent_of_income import (
    house_purchase_cost_as_percent_of_income,
)
from data.american_dream_mobility_international import mobility_international
from data.healthcare_healthcare_cost_per_capita import healthcare_cost_per_capita
from data.healthcare_healthcare_life_expectancy import healthcare_life_expectancy
from data.healthcare_healthcare_infant_mortality import healthcare_infant_mortality
from data.healthcare_healthcare_maternal_mortality import healthcare_maternal_mortality
from data.healthcare_healthcare_suicide_rates import healthcare_suicide_rates
from data.environment_electricity_cost import electricity_cost
from data.justice_outcomes_upward_mobility_jail import outcomes_upward_mobility_jail
from data.economy_house_purchase_cost_as_percent_of_income_state_level import house_purchase_cost_as_percent_of_income_state_level

# ---------------------------------------------------------------------------
# One-time data prep
# ---------------------------------------------------------------------------
counties_json = json.loads(counties_json)
electricity_cost = electricity_cost.sort(["LCOE_Low_USD_MWh"], descending=True)
year_max = shares_wid.select(pl.max("year")).to_numpy().flatten()[0]

_STATE_ABBREVIATIONS = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}
_ABBREV_TO_STATE = {v: k for k, v in _STATE_ABBREVIATIONS.items()}

# _income_index_cols = ["Series ID", "Series Name", "Units", "Region Name", "Region Code"]
# _cost_index_cols   = ["RegionID", "SizeRank", "RegionName", "RegionType",
#                       "StateName", "State", "Metro", "StateCodeFIPS", "MunicipalCodeFIPS"]
#
# _income_long = (
#     income_fred_states
#     .unpivot(index=_income_index_cols, variable_name="date_str", value_name="income")
#     .with_columns(
#         date=pl.col("date_str").str.to_datetime("%Y-%m-%d")
#                                .dt.offset_by("1y").dt.offset_by("-1d"),
#         state=pl.col("Region Name").replace(_STATE_ABBREVIATIONS),
#     )
#     .filter(pl.col("state").str.len_chars() == 2)
#     .select(["date", "state", "income"])
# )
#
# _cost_long = (
#     housing_buy_cost_zillow
#     .unpivot(index=_cost_index_cols, variable_name="date_str", value_name="cost")
#     .with_columns(date=pl.col("date_str").str.to_datetime("%Y-%m-%d"))
#     .group_by(["date", "State"])
#     .agg(pl.mean("cost").alias("cost"))
#     .rename({"State": "state"})
# )
#
# state_affordability = (
#     _income_long
#     .join(_cost_long, on=["state", "date"], how="inner")
#     .with_columns(
#         percent_of_income=(pl.col("cost") / pl.col("income")),
#     )
#     .with_columns(
#         us_average=pl.mean("percent_of_income").over("date"),
#     )
#     .sort(["state", "date"])
# )

# ---------------------------------------------------------------------------
# Config / constants
# ---------------------------------------------------------------------------
YAXIS_RANGE_PCT = 0.25
AXIS_TITLE_INCOME = "<b>income/yr average</b>"
AXIS_TITLE_INCOME_FORMAT = ",.2s"
LAYOUT_ECONOMY_XRANGE = [1905, 2030]
COUNTRIES_MULTI = ["Canada", "Europe", "Japan", "United States"]

INCOME_LEVELS = {
    "Bottom 50%": "income_mean_bottom",
    "Upper 51-99%": "income_mean_upper",
    "Top 1%": "income_mean_top",
}

COLOR_LIGHT_DARK = {
    "light": "rgba(68, 122, 219, 0.5)",
    "dark": "rgba(255,255,255,0.5)",
}

COLORS_BY_COUNTRY = {
    "australia": "rgba( 90, 185, 111, 0.3)",
    "canada": "rgba( 90, 185, 111, 0.3)",
    "france": "rgba( 90, 185, 111, 0.3)",
    "germany": "rgba( 90, 185, 111, 0.3)",
    "italy": "rgba( 90, 185, 111, 0.3)",
    "japan": "rgba( 90, 185, 111, 0.3)",
    "new_zealand": "rgba( 90, 185, 111, 0.3)",
    "norway": "rgba( 90, 185, 111, 0.3)",
    "switzerland": "rgba( 90, 185, 111, 0.3)",
    "uk": "rgba( 90, 185, 111, 0.3)",
    "russia": "rgba(230, 78, 67, 0.7)",
    "china": "rgba(230, 78, 67, 0.7)",
    "usa": COLOR_LIGHT_DARK["light"],
}

COLORS_TAX_CHANGES = {
    "up": "rgba( 90, 185, 111, 0.3)",
    "down": "rgba(230, 78, 67, 0.7)",
}

COLORSCALE = {
    "upward_mobility": [
        [0.0, "#8B0000"],
        [0.40, "#CC0000"],
        [0.45, "#FF8C00"],
        [0.5, "#FFD700"],
        [0.583, "#FFFF00"],
        [0.667, "#ADFF2F"],
        [0.833, "#32CD32"],
        [1.0, "#006400"],
    ],
    "jail": [
        [0.0, "#006400"],
        [0.02, "#228B22"],
        [0.05, "#32CD32"],
        [0.08, "#9ACD32"],
        [0.10, "#ADFF2F"],
        [0.12, "#FFD700"],
        [0.15, "#CC0000"],
        [1.0, "#8B0000"],
    ],
}

SOURCES = {
    "economy": "<a href='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy'>Sources</a>",
    "economy_f150": "<a href='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy#ford-f-seriesf-150-historical-msrp-1950-2025'>Sources</a>",
    "economy_house": "<a href='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy#housing'>Sources</a>",
    "american_dream": "<a href='https://github.com/brendandoner-breathetransport/breathe/wiki/American-Dream'>Sources</a>",
    "healthcare": "<a href='https://github.com/brendandoner-breathetransport/breathe/wiki/Healthcare'>Sources</a>",
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_color_template(mode: str) -> str:
    return "plotly_white" if mode == "light" else "plotly_dark"


def get_background_color(mode: str) -> str:
    return "white" if mode == "light" else "rgb(29, 32, 33)"


def get_yaxis_range(y_data):
    if not isinstance(y_data, np.ndarray):
        try:
            y_data = y_data.to_numpy()
        except Exception:
            y_data = y_data.values
    mn, mx = float(np.min(y_data)), float(np.max(y_data))
    rng = mx - mn
    return mn - rng * YAXIS_RANGE_PCT, mx + rng * YAXIS_RANGE_PCT


def _fmt_text(value, prefix, suffix, fmt, context):
    return f"<span style='color:rgb(0,0,0)'><b>{prefix}{value:{fmt}}{suffix}</b><br>{context}</span>"


def get_highlights_line_min_max(data, col_date, col_metric, number_type, max_or_min):
    fmt   = {"thousands": ".0f",  "percentage": ".0%"}[number_type]
    pfx   = {"thousands": "$",    "percentage": ""}[number_type]
    sfx   = {"thousands": "k",    "percentage": ""}[number_type]
    div   = {"thousands": 1000,   "percentage": 1}[number_type]

    d_latest = data.filter(pl.col(col_date) == data[col_date].max())
    d_min    = data.filter(pl.col(col_metric) == data[col_metric].min())
    d_max    = data.filter(pl.col(col_metric) == data[col_metric].max())

    latest_val = d_latest[col_metric].to_numpy().flatten()[0]
    min_val    = d_min[col_metric].to_numpy().flatten()[0]
    max_val    = d_max[col_metric].to_numpy().flatten()[0]

    def scatter(d, label):
        return go.Scatter(
            name="NONE", mode="markers+text",
            x=d[col_date], y=d[col_metric],
            marker=dict(color="orange", size=8),
            text=_fmt_text(d[col_metric].to_numpy().flatten()[0] / div, pfx, sfx, fmt, label),
            textposition="middle center",
        )

    highlights = [scatter(d_latest, "")]
    if max_or_min in ("max", "both") and latest_val != max_val:
        highlights.append(scatter(d_max, "max"))
    if max_or_min in ("min", "both") and latest_val != min_val:
        highlights.append(scatter(d_min, "min"))
    return highlights


def add_period_lines(fig, year=None, text=None):
    fig.add_vline(
        x=1980,
        line=dict(color="rgba(0,0,0,0.9)", width=2, dash="dash"),
        annotation_text="1980",
        annotation_position="top right",
        annotation_font_color="black",
    )
    if year is not None:
        fig.add_vline(
            x=year,
            line=dict(color="rgba(0,0,0,0.9)", width=2, dash="dash"),
            annotation_text=text,
            annotation_position="top right",
            annotation_font_color="black",
        )


def add_period_shading(fig):
    for x0, x1, color in [(1938, 1979, "green"), (1980, 2020, "black")]:
        fig.add_vrect(
            x0=x0, x1=x1, line_width=0, fillcolor=color, opacity=0.05,
            annotation_text="<b><a href='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy#policies'>Policies</a></b>",
            annotation_position="bottom",
        )


def hide_none_traces(fig):
    for trace in fig["data"]:
        if "NONE" in trace["name"]:
            trace["showlegend"] = False


def fig_to_json(fig) -> JSONResponse:
    return JSONResponse(content=json.loads(fig.to_json()))


# ---------------------------------------------------------------------------
# Chart builders
# ---------------------------------------------------------------------------

def _economy_base_layout(fig, title, income_level, dark_mode, xrange=None, y_data=None,
                          yaxis_title=None, ytickfmt=None, ytickpfx=None,
                          xaxis_title=""):
    ymin, ymax = (get_yaxis_range(y_data) if y_data is not None else (None, None))
    ydict = dict(fixedrange=True)
    if ymin is not None:
        ydict["range"] = [ymin, ymax]
    if ytickpfx:
        ydict["tickprefix"] = ytickpfx
    if ytickfmt:
        ydict["tickformat"] = ytickfmt
    fig.update_layout(
        title=dict(text=title),
        title_x=0.5,
        yaxis_title=yaxis_title or AXIS_TITLE_INCOME,
        yaxis=ydict,
        xaxis_title=xaxis_title,
        xaxis=dict(range=xrange or LAYOUT_ECONOMY_XRANGE, tickmode="array", fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
    )


def make_economy_income(dark_mode: str, income_level: str, country: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    data = shares_wid.filter(pl.col("country") == country).filter(pl.col("year") >= 1880)
    usa = shares_wid.filter(pl.col("country") == "usa").filter(pl.col("year") >= 1880)

    traces = (
        [go.Scatter(name=country, x=data["year"], y=data[income_col],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3))]
        + get_highlights_line_min_max(data, "year", income_col, "thousands", "max")
        + [go.Scatter(name="usa", x=usa["year"], y=usa[income_col],
                      line=dict(color="rgba(0,0,0,0.2)", width=3))]
        + get_highlights_line_min_max(usa, "year", income_col, "thousands", "max")
    )
    fig = go.Figure(data=traces)

    vline_year = {"canada": 2004, "france": 1995}.get(country)
    vline_text = {
        "canada": "2004<br>canadian<br>corporate<br>money<br>ban",
        "france": "1995<br>french<br>corporate<br>money<br>ban",
    }.get(country)
    add_period_lines(fig, year=vline_year, text=vline_text)
    add_period_shading(fig)

    _economy_base_layout(
        fig,
        title=f"<b>{income_level} Paycheck</b><br><sup>{year_max} dollars</sup>",
        income_level=income_level,
        dark_mode=dark_mode,
        y_data=data[income_col],
        ytickpfx="$",
        ytickfmt=AXIS_TITLE_INCOME_FORMAT,
        xaxis_title=SOURCES["economy"],
    )

    for trace in fig["data"]:
        if "min" in trace["name"] or "NONE" in trace["name"]:
            trace["showlegend"] = False
    return fig


def make_economy_barchart(dark_mode: str, income_level: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    latest = (
        shares_wid.filter(pl.col("year") == shares_wid["year"].max())
        .sort([income_col], descending=[False])
    )
    countries = latest.select("country").to_numpy().flatten()
    bar_colors = [COLORS_BY_COUNTRY.get(c, "rgba(100,100,100,0.3)") for c in countries]

    texttemplate = {
        "income_mean_bottom": "<b>%{text:.2s}</b>",
        "income_mean_upper": "<b>%{text:.3s}</b>",
        "income_mean_top": "<b>%{text:.3s}</b>",
    }[income_col]

    fig = go.Figure(data=[go.Bar(
        x=latest["country"], y=latest[income_col],
        text=latest[income_col], texttemplate=texttemplate,
        textfont=dict(size=12), textangle=0,
        marker_color=bar_colors,
    )])
    fig.update_layout(
        title=dict(text=f"<b>{income_level} Comparison</b><br><sup>Each country's share & U.S. {year_max} income</sup>"),
        title_x=0.5,
        yaxis_title=AXIS_TITLE_INCOME,
        yaxis=dict(tickprefix="$", tickformat=AXIS_TITLE_INCOME_FORMAT, fixedrange=True),
        xaxis_title=SOURCES["economy"], xaxis_tickangle=-45, xaxis=dict(fixedrange=True),
        showlegend=False,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
    )
    return fig


def make_economy_income_taxes(dark_mode: str, income_level: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    usa = shares_wid.filter(pl.col("country") == "usa").filter(pl.col("year") > 1880)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_traces(
        [go.Scatter(name="NONE", x=usa["year"], y=usa[income_col],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3))]
        + get_highlights_line_min_max(usa, "year", income_col, "thousands", "max")
    )

    tax_data = tax.filter(pl.col("change_top_bracket") != 0).sort(["year"])
    indices = {"up": 0, "down": 0}
    names = {"up": "tax rate increase", "down": "tax rate decrease"}
    for yr, chg in zip(tax_data["year"].to_list(), tax_data["change_top_bracket"].to_list()):
        direction = "up" if chg > 0 else "down"
        name = names[direction] if indices[direction] == 0 else "NONE"
        indices[direction] += 1
        fig.add_trace(go.Scatter(
            name=name, mode="lines",
            x=[yr, yr], y=[0, chg],
            line=dict(color=COLORS_TAX_CHANGES[direction], width=5),
            yaxis="y2",
        ))

    fig.add_hline(y=0, line=dict(color="rgba(0,0,0,0.2)", width=1, dash="solid"), secondary_y=True)
    add_period_lines(fig)
    add_period_shading(fig)

    ymin, ymax = get_yaxis_range(usa[income_col])
    fig.update_layout(
        title=dict(text=f"<b>Taxes on Top 1%</b><br><sup>{year_max} dollars</sup>"),
        title_x=0.5,
        yaxis_title=AXIS_TITLE_INCOME,
        yaxis=dict(range=[ymin, ymax], tickprefix="$", tickformat=AXIS_TITLE_INCOME_FORMAT, fixedrange=True),
        yaxis2=dict(title="top tax bracket changes", range=[-0.60, 0.60],
                    anchor="x", overlaying="y", side="right", tickformat="+.0%", fixedrange=True),
        xaxis_title=SOURCES["economy"],
        xaxis=dict(range=LAYOUT_ECONOMY_XRANGE, tickmode="array", fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        legend=dict(x=0.01, y=0.99, xanchor="left", yanchor="top"),
    )
    hide_none_traces(fig)
    return fig


def make_economy_house_purchase(dark_mode: str, income_level: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    income = shares_wid.filter(pl.col("country") == "usa").filter(pl.col("year") >= 1880)
    col = "house_pct"
    data = (
        house_purchase_cost_as_percent_of_income
        .join(income, on=["year"], how="inner")
        .with_columns((pl.col("cost") / pl.col(income_col)).alias(col))
    )
    fig = go.Figure(data=(
        [go.Scatter(name="NONE", x=data["year"], y=data[col],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3))]
        + get_highlights_line_min_max(data, "year", col, "percentage", "min")
    ))
    ymin, ymax = get_yaxis_range(data[col])
    fig.update_layout(
        title=dict(text=f"<b>Percent of {income_level} Income to Purchase a Home</b>"),
        title_x=0.5,
        yaxis_title=f"<b>% of {income_level} Paycheck</b>",
        yaxis=dict(range=[ymin, ymax], tickformat=",.0%", fixedrange=True),
        xaxis_title=SOURCES["economy_house"],
        xaxis=dict(range=[data["year"].min() - 4, data["year"].max() + 4], fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
    )
    for trace in fig["data"]:
        if "min" in trace["name"] or "NONE" in trace["name"]:
            trace["showlegend"] = False
    return fig


def make_economy_f150(dark_mode: str, income_level: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    usa = shares_wid.filter(pl.col("country") == "usa").filter(pl.col("year") >= 1880)
    data = (
        f150.join(usa, on=["year"], how="inner")
        .with_columns((pl.col("price") / pl.col(income_col)).alias("price_ratio"))
    )
    fig = go.Figure(data=(
        [go.Scatter(name="NONE", x=data["year"], y=data["price_ratio"],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3))]
        + get_highlights_line_min_max(data, "year", "price_ratio", "percentage", "min")
    ))
    add_period_lines(fig)
    add_period_shading(fig)
    ymin, ymax = get_yaxis_range(data["price_ratio"])
    fig.update_layout(
        title=dict(text=f"<b>Percent of {income_level} Income to Purchase a Ford F-150</b>"),
        title_x=0.5,
        yaxis_title=f"<b>% of {income_level} Paycheck</b>",
        yaxis=dict(range=[ymin, ymax], tickformat=",.0%", fixedrange=True),
        xaxis_title=SOURCES["economy_f150"],
        xaxis=dict(range=[data["year"].min() - 4, data["year"].max() + 4], fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
    )
    for trace in fig["data"]:
        if "min" in trace["name"] or "NONE" in trace["name"]:
            trace["showlegend"] = False
    return fig


def _multi_country_mobility(dark_mode: str, col: str, title: str) -> go.Figure:
    data = (
        mobility_international
        .filter(pl.col(col).is_not_nan())
        .filter(pl.col("country").is_in(COUNTRIES_MULTI))
    )
    last = data.join(
        data.group_by("country").agg(pl.max("year")),
        on=["country", "year"], how="inner",
    )
    countries = np.sort(np.unique(data["country"].to_numpy()))

    fig = go.Figure(data=(
        [go.Scatter(
            name=c, mode="lines",
            x=data.filter(pl.col("country") == c)["year"],
            y=data.filter(pl.col("country") == c)[col],
            line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3)
            if c.lower() == "united states" else dict(color="rgba(0,0,0,0.2)", width=2),
        ) for c in countries]
        + get_highlights_line_min_max(
            data.filter(pl.col("country") == "United States"),
            "year", col, "percentage", "max",
        )
        + [go.Scatter(
            name="NONE", mode="text",
            x=last.filter(pl.col("country") == c)["year"],
            y=last.filter(pl.col("country") == c)[col],
            text=f"<b>{c}</b>" if c == "United States" else c,
            textposition="middle right",
        ) for c in COUNTRIES_MULTI]
    ))

    add_period_lines(fig)
    add_period_shading(fig)
    ymin, ymax = get_yaxis_range(data[col])
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>"), title_x=0.5,
        yaxis_title="% of 30 year olds that earn more than parents",
        xaxis_title=SOURCES["american_dream"],
        xaxis=dict(fixedrange=True, range=[data["year"].min() - 4, data["year"].max() + 15]),
        yaxis=dict(range=[ymin, ymax], tickformat=".0%", fixedrange=True),
        showlegend=False,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
    )
    hide_none_traces(fig)
    return fig


def make_american_dream_kids(dark_mode: str) -> go.Figure:
    return _multi_country_mobility(dark_mode, "mobility", "Upward Mobility")


def make_mobility_international(dark_mode: str) -> go.Figure:
    return _multi_country_mobility(
        dark_mode, "growth_controlled",
        "Upward Mobility Breakdown<br><sup>Fixed income growth, impact of Top 1% taking more</sup>",
    )


def make_county_heatmap(dark_mode: str, race: str, metric: str, title: str) -> go.Figure:
    start = outcomes_upward_mobility_jail.filter(pl.col("metric") == metric)["value"].min()
    stop  = outcomes_upward_mobility_jail.filter(pl.col("metric") == metric)["value"].max()
    df = (
        outcomes_upward_mobility_jail
        .filter(pl.col("metric") == metric)
        .filter(pl.col("race") == race)
        .to_pandas()
    )
    fig = go.Figure(go.Choropleth(
        locations=df["fips_county"], z=df["value"],
        locationmode="geojson-id", geojson=counties_json,
        colorscale=COLORSCALE[metric],
        zmin=start, zmax=stop,
        hovertemplate="<b>%{text}</b><br>" + f"{title}: %{{z:.2f}}<br><extra></extra>",
        text=df["county"] + ", " + df["state"],
        marker=dict(line=dict(width=0)),
        colorbar=dict(title=None, orientation="h", y=-0.1, yanchor="top", thickness=10, len=0.80),
    ))
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>"), title_x=0.5,
        showlegend=False,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        geo=dict(scope="usa", projection=go.layout.geo.Projection(type="albers usa"),
                 showlakes=True, lakecolor="rgb(255, 255, 255)"),
    )
    return fig


def make_timeseries_countries(data, title, yaxis_title, xaxis_title, dark_mode: str) -> go.Figure:
    data = data.filter(pl.col("year") >= 2000)
    last = data.join(data.group_by("country").agg(pl.max("year")), on=["country", "year"], how="inner")
    countries = ["united states", "europe", "costa rica", "japan", "china", "canada"]

    fig = go.Figure(data=(
        [go.Scatter(
            name=c, mode="lines",
            x=data.filter(pl.col("country") == c)["year"],
            y=data.filter(pl.col("country") == c)["value"],
            line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3)
            if c == "united states" else dict(color="rgba(0,0,0,0.2)", width=2),
        ) for c in countries]
        + [go.Scatter(
            name="NONE", mode="text",
            x=last.filter(pl.col("country") == c)["year"],
            y=last.filter(pl.col("country") == c)["value"],
            text=f"<b>{c.title()}</b>" if c == "united states"
                 else f"<br>{c.title()}" if c == "canada" else c.title(),
            textposition="middle right",
        ) for c in countries]
    ))
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>"), title_x=0.5,
        yaxis_title=f"<b>{yaxis_title}</b>",
        xaxis_title=xaxis_title,
        showlegend=False,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
    )
    hide_none_traces(fig)
    return fig


def make_electricity_cost(dark_mode: str) -> go.Figure:
    color_map = {
        "Renewable Energy": "rgb(60, 179, 113)",
        "Conventional Energy": "rgb(139, 129, 130)",
    }
    counts = {"Renewable Energy": 0, "Conventional Energy": 0}
    fig = go.Figure()
    for tech in electricity_cost.select(["Technology"]).to_numpy().flatten():
        row = electricity_cost.filter(pl.col("Technology") == tech)
        cat = row["Category"].to_numpy()[0]
        counts[cat] += 1
        fig.add_trace(go.Scatter(
            x=[float(row["LCOE_Low_USD_MWh"].to_numpy()[0]),
               float(row["LCOE_High_USD_MWh"].to_numpy()[0])],
            y=[str(row["Technology"].to_numpy()[0])] * 2,
            mode="lines+markers",
            line=dict(color=color_map[cat], width=6),
            marker=dict(size=8, color=color_map[cat]),
            name=cat if counts[cat] <= 1 else "",
            showlegend=counts[cat] <= 1,
            hovertemplate=f"<b>{tech}</b><br>LCOE Range: ${row['LCOE_Low_USD_MWh'].to_numpy()[0]}"
                          f"–${row['LCOE_High_USD_MWh'].to_numpy()[0]}/MWh<br><extra></extra>",
        ))
    fig.update_layout(
        title={"text": "Cost of Electricity<br><sub>Ranges by Source</sub>", "x": 0.5, "xanchor": "center"},
        xaxis=dict(title="$ / megawatt hour", showgrid=True, gridcolor="lightgray", range=[0, 300]),
        yaxis=dict(title="Technology", showgrid=True, gridcolor="lightgray",
                   categoryorder="array",
                   categoryarray=list(electricity_cost["Technology"].to_numpy().flatten())),
        plot_bgcolor="white",
        legend=dict(x=0.7, y=0.98, bgcolor="rgba(255,255,255,0.8)", bordercolor="gray", borderwidth=1),
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
    )
    return fig

# --- State home affordability ---

def make_state_home_affordability(state: str, dark_mode: str) -> go.Figure:
    data = house_purchase_cost_as_percent_of_income_state_level.filter(pl.col("state") == state).sort("date")
    state_name = _ABBREV_TO_STATE.get(state, state)
    accent = COLOR_LIGHT_DARK[dark_mode]

    fig = go.Figure(data=[
        go.Scatter(
            name=state_name,
            x=data["date"],
            y=data["percent_of_income"],
            mode="markers+lines",
            line=dict(color=accent, width=2),
        ),
        go.Scatter(
            name="U.S. Average",
            x=data["date"],
            y=data["percent_of_income_mean"],
            mode="markers+lines",
            line=dict(color="rgba(128,128,128,0.5)", width=2, dash="dash"),
        ),
    ])
    ymin, ymax = get_yaxis_range(data["percent_of_income"])
    fig.update_layout(
        title=dict(text=f"<b>Percent of Income to Purchase a Home</b><br><sup>{state_name}</sup>"),
        title_x=0.5,
        yaxis_title="<b>% of Annual Income</b>",
        yaxis=dict(range=[ymin, ymax], tickformat=".0%", fixedrange=True),
        xaxis_title=SOURCES["economy_house"],
        xaxis=dict(type="date", fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        legend=dict(x=0.01, y=0.99, xanchor="left", yanchor="top"),
    )
    return fig

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(title="Breathe Dashboard", version="1.0.0")

_parent = Path(__file__).parent.parent
app.mount("/static", StaticFiles(directory=str(_parent / "static")), name="static")

_here = Path(__file__).parent


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse((_here / "index.html").read_text(encoding="utf-8"))


# --- Meta endpoints ---

@app.get("/api/countries")
async def api_countries():
    countries = shares_wid.select("country").unique().sort("country").to_numpy().flatten().tolist()
    return {"countries": countries}


# --- Economy ---

@app.get("/api/economy/income")
async def api_economy_income(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
    country: str = Query("usa"),
):
    return fig_to_json(make_economy_income(dark_mode, income_level, country))


@app.get("/api/economy/barchart")
async def api_economy_barchart(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
):
    return fig_to_json(make_economy_barchart(dark_mode, income_level))


@app.get("/api/economy/income-taxes")
async def api_economy_income_taxes(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
):
    return fig_to_json(make_economy_income_taxes(dark_mode, income_level))


@app.get("/api/economy/house-purchase-cost")
async def api_economy_house(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
):
    return fig_to_json(make_economy_house_purchase(dark_mode, income_level))


@app.get("/api/economy/f150")
async def api_economy_f150(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
):
    return fig_to_json(make_economy_f150(dark_mode, income_level))


@app.get("/api/economy/american-dream-kids")
async def api_american_dream_kids(dark_mode: str = Query("light")):
    return fig_to_json(make_american_dream_kids(dark_mode))


@app.get("/api/economy/mobility-international")
async def api_mobility_international(dark_mode: str = Query("light")):
    return fig_to_json(make_mobility_international(dark_mode))


@app.get("/api/economy/upward-mobility")
async def api_upward_mobility(
    dark_mode: str = Query("light"),
    race: str = Query("white"),
):
    return fig_to_json(make_county_heatmap(dark_mode, race, "upward_mobility",
                                           f"{race.title()} Male Upward Mobility<br>(parents in bottom 25th of income)"))


# --- Healthcare ---

@app.get("/api/healthcare/cost-per-capita")
async def api_healthcare_cost(dark_mode: str = Query("light")):
    return fig_to_json(make_timeseries_countries(
        healthcare_cost_per_capita, "Healthcare Cost per Person", "U.S. $", SOURCES["healthcare"], dark_mode))


@app.get("/api/healthcare/life-expectancy")
async def api_healthcare_life(dark_mode: str = Query("light")):
    return fig_to_json(make_timeseries_countries(
        healthcare_life_expectancy, "Life Expectancy", "years", SOURCES["healthcare"], dark_mode))


@app.get("/api/healthcare/infant-mortality")
async def api_healthcare_infant(dark_mode: str = Query("light")):
    return fig_to_json(make_timeseries_countries(
        healthcare_infant_mortality, "Infant Mortality", "deaths per 1,000 babies", SOURCES["healthcare"], dark_mode))


@app.get("/api/healthcare/maternal-mortality")
async def api_healthcare_maternal(dark_mode: str = Query("light")):
    return fig_to_json(make_timeseries_countries(
        healthcare_maternal_mortality, "Mother Mortality", "deaths per 100,000 births", SOURCES["healthcare"], dark_mode))


@app.get("/api/healthcare/suicide-rates")
async def api_healthcare_suicide(dark_mode: str = Query("light")):
    return fig_to_json(make_timeseries_countries(
        healthcare_suicide_rates, "Suicide Rates", "deaths per 100,000", SOURCES["healthcare"], dark_mode))


# --- Justice ---

@app.get("/api/justice/jail")
async def api_justice_jail(
    dark_mode: str = Query("light"),
    race: str = Query("white"),
):
    return fig_to_json(make_county_heatmap(dark_mode, race, "jail",
                                           f"{race.title()} Male Jail Rate<br>(parents in bottom 25th of income)"))



# --- State home affordability ---

@app.get("/api/economy/state-home-affordability")
async def api_state_home_affordability(
    state: str = Query("CO"),
    dark_mode: str = Query("light"),
):
    return fig_to_json(make_state_home_affordability(state, dark_mode))


# --- Environment ---

@app.get("/api/environment/electricity-cost")
async def api_electricity_cost(dark_mode: str = Query("light")):
    return fig_to_json(make_electricity_cost(dark_mode))
