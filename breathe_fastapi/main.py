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
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response

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
from data.economy_house_purchase_cost_as_percent_of_income_state_level import (
    house_purchase_cost_as_percent_of_income_state_level,
)

# ---------------------------------------------------------------------------
# One-time data prep
# ---------------------------------------------------------------------------
counties_json = json.loads(counties_json)
electricity_cost = electricity_cost.sort(["LCOE_Low_USD_MWh"], descending=True)
year_max = shares_wid.select(pl.max("year")).to_numpy().flatten()[0]

_STATE_ABBREVIATIONS = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
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
PLOT_MARGIN = dict(t=60, b=50, l=60, r=20)
AXIS_TITLE_INCOME = "<b>average pay</b>"
AXIS_TITLE_INCOME_FORMAT = ",.2s"
LAYOUT_ECONOMY_XRANGE = [1905, 2030]
LAYOUT_ECONOMY_INCOME_XRANGE = [
    1880,
    2030,
]  # extended to show 1880 max; revert by changing to LAYOUT_ECONOMY_XRANGE
COUNTRIES_MULTI = ["Canada", "Europe", "Japan", "United States"]

INCOME_LEVELS = {
    "Bottom 50%": "income_mean_bottom",
    "Upper 51-99%": "income_mean_upper",
    "Top 1%": "income_mean_top",
}

COLOR_LIGHT_DARK = {
    "light": "rgba(68, 122, 219, 0.5)",
    "dark": "rgba(74, 144, 226, 0.9)",
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


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def get_color_template(mode: str) -> str:
    return "plotly_white" if mode == "light" else "plotly_dark"


def get_background_color(mode: str) -> str:
    return "rgb(245, 245, 242)" if mode == "light" else "rgb(62, 72, 88)"


def get_yaxis_range(y_data):
    if not isinstance(y_data, np.ndarray):
        try:
            y_data = y_data.to_numpy()
        except Exception:
            y_data = y_data.values
    mn, mx = float(np.min(y_data)), float(np.max(y_data))
    rng = mx - mn
    return mn - rng * YAXIS_RANGE_PCT, mx + rng * YAXIS_RANGE_PCT


def _fmt_text(value, prefix, suffix, fmt, context, color="rgb(0,0,0)"):
    return f"<span style='color:{color}'><b>{prefix}{value:{fmt}}{suffix}</b><br>{context}</span>"


def get_highlights_line_min_max(
    data,
    col_date,
    col_metric,
    number_type,
    max_or_min,
    dark_mode="light",
    fig=None,
    xrange=None,
    show_current=True,
):
    fmt = {"thousands": ".0f", "percentage": ".0%"}[number_type]
    pfx = {"thousands": "$", "percentage": ""}[number_type]
    sfx = {"thousands": "k", "percentage": ""}[number_type]
    div = {"thousands": 1000, "percentage": 1}[number_type]

    visible = (
        data.filter(pl.col(col_date).is_between(xrange[0], xrange[1]))
        if xrange
        else data
    )
    d_latest = data.filter(pl.col(col_date) == data[col_date].max())
    d_min = (
        visible.filter(pl.col(col_metric) == visible[col_metric].min())
        .sort(col_date)
        .tail(1)
    )
    d_max = (
        visible.filter(pl.col(col_metric) == visible[col_metric].max())
        .sort(col_date)
        .tail(1)
    )

    latest_val = d_latest[col_metric].to_numpy().flatten()[0]
    min_val = d_min[col_metric].to_numpy().flatten()[0]
    max_val = d_max[col_metric].to_numpy().flatten()[0]

    text_color = "rgba(255,255,255,0.85)" if dark_mode == "dark" else "rgba(0,0,0,0.85)"

    def scatter(d, label, textposition="top center"):
        return go.Scatter(
            name="NONE",
            mode="markers+text",
            x=d[col_date],
            y=d[col_metric],
            marker=dict(color="orange", size=8),
            text=_fmt_text(
                value=d[col_metric].to_numpy().flatten()[0] / div,
                prefix=pfx,
                suffix=sfx,
                fmt=fmt,
                context=label,
                color=text_color,
            ),
            textposition=textposition,
            textfont=dict(color=text_color),
            cliponaxis=False,
            hoverinfo="skip",
        )

    latest_label = "current"
    if max_or_min in ("max", "both") and latest_val == max_val:
        latest_label = "max"
    elif max_or_min in ("min", "both") and latest_val == min_val:
        latest_label = "min"
    highlights = [scatter(d_latest, latest_label)] if show_current else []
    if max_or_min in ("max", "both") and latest_val != max_val:
        highlights.append(scatter(d_max, "max"))
    if max_or_min in ("min", "both") and latest_val != min_val:
        highlights.append(scatter(d_min, "min"))

    if fig is not None:
        max_year = d_max[col_date].to_numpy().flatten()[0]
        line_color = (
            "rgba(255,255,255,0.3)" if dark_mode == "dark" else "rgba(0,0,0,0.3)"
        )
        font_color = "rgba(255,255,255,0.85)" if dark_mode == "dark" else "black"
        fig.add_vline(
            x=max_year,
            line=dict(color=line_color, width=2, dash="dash"),
            annotation_text=str(max_year),
            annotation_position="bottom right",
            annotation_font_color=font_color,
        )

    return highlights


def add_period_lines(fig, year=None, text=None, dark_mode="light"):
    line_color = "rgba(255,255,255,0.3)" if dark_mode == "dark" else "rgba(0,0,0,0.3)"
    font_color = "rgba(255,255,255,0.85)" if dark_mode == "dark" else "black"
    # fig.add_vline(
    #     x=1969,
    #     line=dict(color=line_color, width=2, dash="dash"),
    #     annotation_text="1969",
    #     annotation_position="bottom right",
    #     annotation_font_color=font_color,
    # )
    if year is not None:
        fig.add_vline(
            x=year,
            line=dict(color=line_color, width=2, dash="dash"),
            annotation_text=text,
            annotation_position="bottom right",
            annotation_font_color=font_color,
        )


def add_period_shading(fig, dark_mode="light"):
    dark_fill = "white" if dark_mode == "dark" else "black"
    for x0, x1, color in [(1938, 1979, "green"), (1980, 2020, dark_fill)]:
        fig.add_vrect(
            x0=x0,
            x1=x1,
            line_width=0,
            fillcolor=color,
            opacity=0.05,
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


def _title_dict(main: str, subtitle: str = "", font_size: int = 14) -> dict:
    """Word-wrap main title and return a Plotly title dict.
    automargin=True lets Plotly expand the top margin to fit wrapped lines.
    Subtitles are never wrapped — they render on a single <sup> line.
    """
    words = main.split()
    lines, line, length = [], [], 0
    for word in words:
        word_len = len(word) + (1 if line else 0)
        if line and length + word_len > 35:
            lines.append(" ".join(line))
            line, length = [word], len(word)
        else:
            line.append(word)
            length += word_len
    if line:
        lines.append(" ".join(line))
    text = f"<b>{'<br>'.join(lines)}</b>"
    if subtitle:
        text += f"<br><sup>{subtitle}</sup>"
    return dict(
        text=text,
        font=dict(size=font_size),
        yref="container",
        y=0.96,
        yanchor="top",
        pad=dict(t=12, b=12),
    )


def _yaxis_title_dict(main: str, subtitle: str = "", font_size: int = 12) -> dict:
    """Return a Plotly yaxis title dict with an optional subtitle in parentheses."""
    text = f"<b>{main}</b>"
    if subtitle:
        text += f" ({subtitle})"
    return dict(
        text=text,
        font=dict(size=font_size),
    )


def _economy_base_layout(
    fig,
    title,
    income_level,
    dark_mode,
    xrange=None,
    y_data=None,
    yaxis_title=None,
    ytickfmt=None,
    ytickpfx=None,
    xaxis_title="",
):
    ymin, ymax = get_yaxis_range(y_data=y_data) if y_data is not None else (None, None)
    ydict = dict(fixedrange=True)
    if ymin is not None:
        ydict["range"] = [ymin, ymax]
    if ytickpfx:
        ydict["tickprefix"] = ytickpfx
    if ytickfmt:
        ydict["tickformat"] = ytickfmt
    fig.update_layout(
        title=_title_dict(main=title) if isinstance(title, str) else title,
        title_x=0.5,
        yaxis_title=yaxis_title or AXIS_TITLE_INCOME,
        yaxis=ydict,
        xaxis_title=xaxis_title,
        xaxis=dict(
            range=xrange or LAYOUT_ECONOMY_XRANGE, tickmode="array", fixedrange=True
        ),
        showlegend=True,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
    )


def make_economy_income(
    dark_mode: str, income_level: str, country: str, title: str = ""
) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    data = shares_wid.filter(pl.col("country") == country).filter(
        pl.col("year") >= 1880
    )
    usa = shares_wid.filter(pl.col("country") == "usa").filter(pl.col("year") >= 1880)

    _income_hover = (
        "<b>%{fullData.name}</b><br>Year: %{x} | average pay: $%{y:,.0f}<extra></extra>"
    )
    other_color = "rgba(255,255,255,0.35)" if dark_mode == "dark" else "rgba(0,0,0,0.2)"
    country_traces = (
        []
        if country == "usa"
        else (
            [
                go.Scatter(
                    name=country.upper(),
                    x=data["year"],
                    y=data[income_col],
                    line=dict(color=other_color, width=3),
                    hovertemplate=_income_hover,
                )
            ]
            + get_highlights_line_min_max(
                data=data,
                col_date="year",
                col_metric=income_col,
                number_type="thousands",
                max_or_min="max",
                dark_mode=dark_mode,
                xrange=LAYOUT_ECONOMY_INCOME_XRANGE,
            )
        )
    )
    traces = (
        country_traces
        + [
            go.Scatter(
                name="USA",
                x=usa["year"],
                y=usa[income_col],
                line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3),
                hovertemplate=_income_hover,
            )
        ]
        + get_highlights_line_min_max(
            data=usa,
            col_date="year",
            col_metric=income_col,
            number_type="thousands",
            max_or_min="max",
            dark_mode=dark_mode,
            xrange=LAYOUT_ECONOMY_INCOME_XRANGE,
        )
    )
    fig = go.Figure(data=traces)
    if country not in ("canada", "france"):
        get_highlights_line_min_max(
            data=usa,
            col_date="year",
            col_metric=income_col,
            number_type="thousands",
            max_or_min="max",
            dark_mode=dark_mode,
            fig=fig,
            xrange=LAYOUT_ECONOMY_INCOME_XRANGE,
        )

    vline_year = {"canada": 2004, "france": 1995}.get(country)
    vline_text = {
        "canada": "2004<br>Canadian<br>corporate<br>money<br>ban",
        "france": "1995<br>French<br>corporate<br>money<br>ban",
    }.get(country)
    add_period_lines(fig=fig, year=vline_year, text=vline_text, dark_mode=dark_mode)

    all_y = np.concatenate([data[income_col].to_numpy(), usa[income_col].to_numpy()])
    _economy_base_layout(
        fig,
        title=_title_dict(
            main=title
            or "American workers get less & less of the pie while the rich take more",
            subtitle=None,
        ),
        income_level=income_level,
        dark_mode=dark_mode,
        xrange=LAYOUT_ECONOMY_INCOME_XRANGE,
        y_data=all_y,
        ytickpfx="$",
        ytickfmt=AXIS_TITLE_INCOME_FORMAT,
        yaxis_title=_yaxis_title_dict(
            main="average pay", subtitle=f"{year_max} dollars"
        ),
    )

    for trace in fig["data"]:
        if "min" in trace["name"] or "NONE" in trace["name"]:
            trace["showlegend"] = False
    return fig


def make_economy_barchart(
    dark_mode: str,
    income_level: str,
    highlight_canada: bool = False,
    selected_country: str = "usa",
) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    latest = shares_wid.filter(pl.col("year") == shares_wid["year"].max()).sort(
        [income_col], descending=[False]
    )
    countries = latest.select("country").to_numpy().flatten()
    highlight_country = selected_country if selected_country != "usa" else None
    gray = "rgba(255,255,255,0.35)" if dark_mode == "dark" else "rgba(0,0,0,0.2)"
    bar_colors = [
        gray
        if (c == "canada" and highlight_canada) or c == highlight_country
        else COLORS_BY_COUNTRY.get(c, "rgba(100,100,100,0.3)")
        for c in countries
    ]

    texttemplate = {
        "income_mean_bottom": "<b>%{text:.2s}</b>",
        "income_mean_upper": "<b>%{text:.3s}</b>",
        "income_mean_top": "<b>%{text:.3s}</b>",
    }[income_col]

    legend_traces = (
        [
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                name="Democracies",
                marker=dict(color="rgba(90,185,111,0.3)", size=12, symbol="square"),
            ),
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                name="Authoritarian",
                marker=dict(color="rgba(230,78,67,0.7)", size=12, symbol="square"),
            ),
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                name="USA",
                marker=dict(
                    color=COLOR_LIGHT_DARK[dark_mode], size=12, symbol="square"
                ),
            ),
        ]
        + (
            [
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="markers",
                    name="Canada",
                    marker=dict(color=gray, size=12, symbol="square"),
                )
            ]
            if highlight_canada
            else []
        )
        + (
            [
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="markers",
                    name=highlight_country.replace("_", " ").title(),
                    marker=dict(color=gray, size=12, symbol="square"),
                )
            ]
            if highlight_country and not highlight_canada
            else []
        )
    )
    x_labels = [c.replace("_", " ").upper() for c in countries]
    fig = go.Figure(
        data=[
            go.Bar(
                x=x_labels,
                y=latest[income_col],
                text=latest[income_col],
                texttemplate=texttemplate,
                textfont=dict(
                    size=12,
                    color="rgba(255,255,255,0.85)"
                    if dark_mode == "dark"
                    else "rgba(0,0,0,0.85)",
                ),
                textangle=0,
                marker_color=bar_colors,
                showlegend=False,
                hovertemplate="Country: %{x} | Average Pay: $%{y:,.0f}<extra></extra>",
            )
        ]
        + legend_traces
    )
    fig.update_layout(
        title=_title_dict(
            main="With the same sized pie, how do other countries divide it?",
            subtitle=None,
        ),
        title_x=0.5,
        yaxis=dict(
            tickprefix="$", tickformat=AXIS_TITLE_INCOME_FORMAT, fixedrange=True
        ),
        yaxis_title=_yaxis_title_dict(
            main="average pay", subtitle=f"{year_max} dollars"
        ),
        xaxis_tickangle=-45,
        xaxis=dict(fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
    )
    return fig


def make_economy_income_taxes(dark_mode: str, income_level: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    usa = shares_wid.filter(pl.col("country") == "usa").filter(pl.col("year") > 1880)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_traces(
        [
            go.Scatter(
                name=income_level,
                showlegend=False,
                x=usa["year"],
                y=usa[income_col],
                line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3),
                hovertemplate="<b>%{fullData.name}</b><br>Year: %{x} | average pay: $%{y:,.0f}<extra></extra>",
            )
        ]
        + get_highlights_line_min_max(
            data=usa,
            col_date="year",
            col_metric=income_col,
            number_type="thousands",
            max_or_min="max",
            dark_mode=dark_mode,
        )
    )

    tax_data = tax.filter(pl.col("change_top_bracket") != 0).sort(["year"])
    indices = {"up": 0, "down": 0}
    names = {"up": "tax rate increase", "down": "tax rate decrease"}
    for yr, chg in zip(
        tax_data["year"].to_list(), tax_data["change_top_bracket"].to_list()
    ):
        direction = "up" if chg > 0 else "down"
        name = names[direction] if indices[direction] == 0 else "NONE"
        indices[direction] += 1
        fig.add_trace(
            go.Scatter(
                name=name,
                mode="lines",
                x=[yr, yr],
                y=[0, chg],
                line=dict(color=COLORS_TAX_CHANGES[direction], width=5),
                yaxis="y2",
                hoverinfo="skip",
            )
        )

    fig.add_hline(
        y=0, line=dict(color="rgba(0,0,0,0.2)", width=1, dash="solid"), secondary_y=True
    )
    add_period_lines(fig=fig, dark_mode=dark_mode)
    add_period_shading(fig=fig, dark_mode=dark_mode)

    ymin, ymax = get_yaxis_range(y_data=usa[income_col])
    fig.update_layout(
        title=_title_dict(
            main="Lower taxes for the rich is part of the system that shrinks your paycheck",
            subtitle=None,
        ),
        title_x=0.5,
        yaxis=dict(
            range=[ymin, ymax],
            tickprefix="$",
            tickformat=AXIS_TITLE_INCOME_FORMAT,
            fixedrange=True,
        ),
        yaxis2=dict(
            title="top tax bracket changes",
            range=[-0.60, 0.60],
            anchor="x",
            overlaying="y",
            side="right",
            tickformat="+.0%",
            fixedrange=True,
        ),
        yaxis_title=_yaxis_title_dict(
            main="average pay", subtitle=f"{year_max} dollars"
        ),
        xaxis=dict(range=LAYOUT_ECONOMY_XRANGE, tickmode="array", fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
        legend=dict(x=0.01, y=0.99, xanchor="left", yanchor="top"),
    )
    hide_none_traces(fig=fig)
    return fig


def make_economy_house_purchase(dark_mode: str, income_level: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    income = shares_wid.filter(pl.col("country") == "usa").filter(
        pl.col("year") >= 1880
    )
    col = "house_pct"
    data = house_purchase_cost_as_percent_of_income.join(
        income, on=["year"], how="inner"
    ).with_columns((pl.col("cost") / pl.col(income_col)).alias(col))
    fig = go.Figure(
        data=(
            [
                go.Scatter(
                    name=income_level,
                    showlegend=False,
                    x=data["year"],
                    y=data[col],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3),
                    hovertemplate=f"<b>%{{fullData.name}}</b><br>Year: %{{x}} | % of {income_level} Paycheck: %{{y:.1%}}<extra></extra>",
                )
            ]
            + get_highlights_line_min_max(
                data=data,
                col_date="year",
                col_metric=col,
                number_type="percentage",
                max_or_min="min",
                dark_mode=dark_mode,
            )
        )
    )
    ymin, ymax = get_yaxis_range(y_data=data[col])
    fig.update_layout(
        title=_title_dict(main=f"Percent of {income_level} Income to Purchase a Home"),
        title_x=0.5,
        yaxis_title=f"<b>% of {income_level} Paycheck</b>",
        yaxis=dict(range=[ymin, ymax], tickformat=",.0%", fixedrange=True),
        xaxis=dict(
            range=[data["year"].min() - 5, data["year"].max() + 4], fixedrange=True
        ),
        showlegend=True,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
    )
    for trace in fig["data"]:
        if "min" in trace["name"] or "NONE" in trace["name"]:
            trace["showlegend"] = False
    return fig


def make_economy_f150(dark_mode: str, income_level: str) -> go.Figure:
    income_col = INCOME_LEVELS[income_level]
    usa = shares_wid.filter(pl.col("country") == "usa").filter(pl.col("year") >= 1880)
    data = f150.join(usa, on=["year"], how="inner").with_columns(
        (pl.col("price") / pl.col(income_col)).alias("price_ratio")
    )
    fig = go.Figure(
        data=(
            [
                go.Scatter(
                    name=income_level,
                    showlegend=False,
                    x=data["year"],
                    y=data["price_ratio"],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3),
                    hovertemplate=f"<b>%{{fullData.name}}</b><br>Year: %{{x}} | % of {income_level} Paycheck: %{{y:.1%}}<extra></extra>",
                )
            ]
            + get_highlights_line_min_max(
                data=data,
                col_date="year",
                col_metric="price_ratio",
                number_type="percentage",
                max_or_min="min",
                dark_mode=dark_mode,
            )
        )
    )
    add_period_lines(fig=fig, dark_mode=dark_mode)
    add_period_shading(fig=fig, dark_mode=dark_mode)
    ymin, ymax = get_yaxis_range(y_data=data["price_ratio"])
    fig.update_layout(
        title=_title_dict(
            main=f"Percent of {income_level} Income to Purchase a Ford F-150"
        ),
        title_x=0.5,
        yaxis_title=f"<b>% of {income_level} Paycheck</b>",
        yaxis=dict(range=[ymin, ymax], tickformat=",.0%", fixedrange=True),
        xaxis=dict(
            range=[data["year"].min() - 5, data["year"].max() + 4], fixedrange=True
        ),
        showlegend=True,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
    )
    for trace in fig["data"]:
        if "min" in trace["name"] or "NONE" in trace["name"]:
            trace["showlegend"] = False
    return fig


def _spread_labels(label_y: dict, y_range: float, min_gap_frac: float = 0.06) -> dict:
    """Push label y-positions apart so no two are closer than min_gap_frac * y_range."""
    min_gap = min_gap_frac * y_range
    keys = sorted(label_y, key=label_y.__getitem__)
    pos = [label_y[k] for k in keys]
    for _ in range(200):
        moved = False
        for i in range(1, len(pos)):
            if pos[i] - pos[i - 1] < min_gap:
                mid = (pos[i] + pos[i - 1]) / 2
                pos[i - 1] = mid - min_gap / 2
                pos[i] = mid + min_gap / 2
                moved = True
        if not moved:
            break
    return dict(zip(keys, pos))


def _multi_country_mobility(
    dark_mode: str, col: str, title: str, subtitle: str = ""
) -> go.Figure:
    data = mobility_international.filter(pl.col(col).is_not_nan()).filter(
        pl.col("country").is_in(COUNTRIES_MULTI)
    )
    last = data.join(
        data.group_by("country").agg(pl.max("year")),
        on=["country", "year"],
        how="inner",
    )
    countries = np.sort(np.unique(data["country"].to_numpy()))

    other_color = "rgba(255,255,255,0.35)" if dark_mode == "dark" else "rgba(0,0,0,0.2)"
    text_color = "rgba(255,255,255,0.85)" if dark_mode == "dark" else "rgba(0,0,0,0.85)"

    raw_label_y = {
        c: float(last.filter(pl.col("country") == c)[col].to_numpy()[0])
        for c in COUNTRIES_MULTI
    }
    ymin, ymax = get_yaxis_range(y_data=data[col])
    label_y = _spread_labels(label_y=raw_label_y, y_range=ymax - ymin)

    fig = go.Figure(
        data=(
            [
                go.Scatter(
                    name=c,
                    mode="lines",
                    x=data.filter(pl.col("country") == c)["year"],
                    y=data.filter(pl.col("country") == c)[col],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3)
                    if c.lower() == "united states"
                    else dict(color=other_color, width=2),
                    hovertemplate="<b>%{fullData.name}</b><br>Year: %{x} | % earning more than parents: %{y:.1%}<extra></extra>",
                )
                for c in countries
            ]
            + [
                go.Scatter(
                    name="NONE",
                    mode="text",
                    x=last.filter(pl.col("country") == c)["year"],
                    y=[label_y[c]],
                    text=f"<span style='color:{text_color}'><b>{c}</b></span>"
                    if c == "United States"
                    else f"<span style='color:{text_color}'>{c}</span>",
                    textposition="middle right",
                    hoverinfo="skip",
                )
                for c in COUNTRIES_MULTI
            ]
        )
    )
    for trace in get_highlights_line_min_max(
        data=data.filter(pl.col("country") == "United States"),
        col_date="year",
        col_metric=col,
        number_type="percentage",
        max_or_min="max",
        dark_mode=dark_mode,
        fig=fig,
        show_current=False,
    ):
        fig.add_trace(trace)

    ymin, ymax = get_yaxis_range(y_data=data[col])
    fig.update_layout(
        title=_title_dict(main=title, subtitle=subtitle),
        title_x=0.5,
        yaxis_title=None,
        xaxis=dict(
            fixedrange=True, range=[data["year"].min() - 5, data["year"].max() + 15]
        ),
        yaxis=dict(range=[ymin, ymax], tickformat=".0%", fixedrange=True),
        showlegend=False,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
    )
    hide_none_traces(fig=fig)
    return fig


def make_american_dream_kids(dark_mode: str) -> go.Figure:
    return _multi_country_mobility(
        dark_mode=dark_mode,
        col="mobility",
        title="How likely are you to make more than your parents?",
    )


def make_mobility_international(dark_mode: str) -> go.Figure:
    return _multi_country_mobility(
        dark_mode=dark_mode,
        col="growth_controlled",
        title="How does the rich taking more hurt the American Dream?",
        subtitle=None,
    )


def make_county_heatmap(
    dark_mode: str, race: str, metric: str, title: str, subtitle: str = ""
) -> go.Figure:
    start = outcomes_upward_mobility_jail.filter(pl.col("metric") == metric)[
        "value"
    ].min()
    stop = outcomes_upward_mobility_jail.filter(pl.col("metric") == metric)[
        "value"
    ].max()
    df = (
        outcomes_upward_mobility_jail.filter(pl.col("metric") == metric)
        .filter(pl.col("race") == race)
        .to_pandas()
    )
    fig = go.Figure(
        go.Choropleth(
            locations=df["fips_county"],
            z=df["value"],
            locationmode="geojson-id",
            geojson=counties_json,
            colorscale=COLORSCALE[metric],
            zmin=start,
            zmax=stop,
            hovertemplate="<b>%{text}</b><br>"
            + f"{title}: %{{z:.2f}}<br><extra></extra>",
            text=df["county"] + ", " + df["state"],
            marker=dict(line=dict(width=0)),
            colorbar=dict(
                title=None,
                orientation="h",
                y=-0.1,
                yanchor="top",
                thickness=10,
                len=0.80,
            ),
        )
    )
    fig.update_layout(
        title=_title_dict(main=title, subtitle=subtitle),
        title_x=0.5,
        showlegend=False,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type="albers usa"),
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
            bgcolor=get_background_color(dark_mode),
        ),
    )
    return fig


def make_healthcare(data, title, yaxis_title, dark_mode: str) -> go.Figure:
    data = data.filter(pl.col("year") >= 2000)
    last = data.join(
        data.group_by("country").agg(pl.max("year")),
        on=["country", "year"],
        how="inner",
    )
    countries = ["united states", "europe", "costa rica", "japan", "china", "canada"]

    other_color = "rgba(255,255,255,0.35)" if dark_mode == "dark" else "rgba(0,0,0,0.2)"
    text_color = "rgba(255,255,255,0.85)" if dark_mode == "dark" else "rgba(0,0,0,0.85)"

    def country_label(c):
        if c == "united states":
            return "<b>USA</b>"
        return f"<br>{c.title()}" if c == "canada" else c.title()

    fig = go.Figure(
        data=(
            [
                go.Scatter(
                    name=c,
                    mode="lines",
                    x=data.filter(pl.col("country") == c)["year"],
                    y=data.filter(pl.col("country") == c)["value"],
                    line=dict(color=COLOR_LIGHT_DARK[dark_mode], width=3)
                    if c == "united states"
                    else dict(color=other_color, width=2),
                    hovertemplate=f"<b>%{{fullData.name}}</b><br>Year: %{{x}} | {yaxis_title}: %{{y:,.2f}}<extra></extra>",
                )
                for c in countries
            ]
            + [
                go.Scatter(
                    name="NONE",
                    mode="text",
                    x=last.filter(pl.col("country") == c)["year"],
                    y=last.filter(pl.col("country") == c)["value"],
                    text=f"<span style='color:{text_color}'>{country_label(c)}</span>",
                    textposition="middle right",
                    hoverinfo="skip",
                )
                for c in countries
            ]
        )
    )
    max_year = int(data["year"].max())
    fig.update_layout(
        title=_title_dict(main=title),
        title_x=0.5,
        yaxis_title=f"<b>{yaxis_title}</b>",
        xaxis=dict(range=[data["year"].min() - 5, max_year + 8], fixedrange=True),
        showlegend=False,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
    )
    hide_none_traces(fig=fig)
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
        fig.add_trace(
            go.Scatter(
                x=[
                    float(row["LCOE_Low_USD_MWh"].to_numpy()[0]),
                    float(row["LCOE_High_USD_MWh"].to_numpy()[0]),
                ],
                y=[str(row["Technology"].to_numpy()[0])] * 2,
                mode="lines+markers",
                line=dict(color=color_map[cat], width=6),
                marker=dict(size=8, color=color_map[cat]),
                name=cat if counts[cat] <= 1 else "",
                showlegend=counts[cat] <= 1,
                hovertemplate=f"<b>{tech}</b><br>LCOE Range: ${row['LCOE_Low_USD_MWh'].to_numpy()[0]}"
                f"–${row['LCOE_High_USD_MWh'].to_numpy()[0]}/MWh<br><extra></extra>",
            )
        )
    grid_color = "rgba(255,255,255,0.15)" if dark_mode == "dark" else "lightgray"
    legend_bg = "rgba(40,45,48,0.9)" if dark_mode == "dark" else "rgba(255,255,255,0.8)"
    legend_border = "rgba(255,255,255,0.2)" if dark_mode == "dark" else "gray"
    fig.update_layout(
        title={
            **_title_dict(main="Cost of Electricity", subtitle="Ranges by Source"),
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis=dict(
            title="$ / megawatt hour",
            showgrid=True,
            gridcolor=grid_color,
            range=[0, 300],
        ),
        yaxis=dict(
            title="Technology",
            showgrid=True,
            gridcolor=grid_color,
            categoryorder="array",
            categoryarray=list(electricity_cost["Technology"].to_numpy().flatten()),
            tickmode="array",
            tickvals=list(electricity_cost["Technology"].to_numpy().flatten()),
            ticktext=list(electricity_cost["Technology"].to_numpy().flatten()),
        ),
        legend=dict(
            x=0.7, y=0.98, bgcolor=legend_bg, bordercolor=legend_border, borderwidth=1
        ),
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
    )
    return fig


# --- State home affordability ---


def make_state_home_affordability(state: str, dark_mode: str) -> go.Figure:
    data = house_purchase_cost_as_percent_of_income_state_level.filter(
        pl.col("state") == state
    ).sort("date")
    state_name = _ABBREV_TO_STATE.get(state, state)
    accent = COLOR_LIGHT_DARK[dark_mode]

    fig = go.Figure(
        data=[
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
        ]
    )
    ymin, ymax = get_yaxis_range(y_data=data["percent_of_income"])
    fig.update_layout(
        title=_title_dict(
            main="Percent of Income to Purchase a Home", subtitle=state_name
        ),
        title_x=0.5,
        yaxis_title="<b>% of Annual Income</b>",
        yaxis=dict(range=[ymin, ymax], tickformat=".0%", fixedrange=True),
        xaxis=dict(type="date", fixedrange=True),
        showlegend=True,
        template=get_color_template(dark_mode),
        plot_bgcolor=get_background_color(dark_mode),
        paper_bgcolor=get_background_color(dark_mode),
        margin=PLOT_MARGIN,
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(str(_parent / "static" / "images" / "favicon.ico"))


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse((_here / "index.html").read_text(encoding="utf-8"))


# --- Meta endpoints ---


def _inline_md(text: str) -> str:
    """Convert inline markdown (bold, links, bare URLs) to HTML."""
    import re

    # Markdown links — handle URLs containing one level of parentheses
    text = re.sub(
        r"\[([^\]]+)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)",
        r'<a href="\2" target="_blank">\1</a>',
        text,
    )
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Auto-link bare URLs, stripping trailing punctuation
    text = re.sub(
        r'(?<!href=")(https?://[^\s<>"]+?)([.,;:)]*)(?=\s|$)',
        lambda m: f'<a href="{m.group(1)}" target="_blank">{m.group(1)}</a>{m.group(2)}',
        text,
    )
    return text


# Display names for the Sources tab, keyed by function name
_FUNC_DISPLAY: dict[str, str] = {
    "make_economy_income": "Income",
    "make_economy_barchart": "Income Bar Chart",
    "make_economy_house_purchase": "Housing Costs",
    "make_economy_f150": "Ford F-150 Price",
    "make_economy_income_taxes": "Income Taxes",
    "make_american_dream_kids": "American Dream — Kids",
    "make_mobility_international": "Mobility — International",
    "make_county_heatmap": "Upward Mobility",
    "make_healthcare": "Healthcare",
    "make_justice_jail": "Justice — Incarceration",
    "make_electricity_cost": "Electricity Cost",
    "make_state_home_affordability": "State Home Affordability",
    "Additional": "Additional Sources",
    "co_ballot_2025": "Colorado 2025 — Healthy School Meals for All",
}


def _func_display(category: str, func_name: str) -> str:
    if func_name in _FUNC_DISPLAY:
        return _FUNC_DISPLAY[func_name]
    name = func_name.removeprefix("make_")
    cat_prefix = category.lower().replace(" ", "_") + "_"
    if name.startswith(cat_prefix):
        name = name[len(cat_prefix) :]
    return name.replace("_", " ").title() or category


# Chart titles produced by each plot function.
# Each entry lists the exact title strings shown on the rendered charts.
_FUNC_CHARTS: dict[str, list[str]] = {
    "make_economy_income": [
        "American workers get less & less of the pie while the rich take more",
    ],
    "make_economy_barchart": [
        "With the same sized pie, how do other countries divide it?",
    ],
    "make_economy_income_taxes": [
        "Lower taxes for the rich is part of the system that shrinks your paycheck",
    ],
    "make_economy_house_purchase": [
        "Percent of Income to Purchase a Home",
    ],
    "make_economy_f150": [
        "Percent of Income to Purchase a Ford F-150",
    ],
    "make_american_dream_kids": [
        "How likely are you to make more than your parents?",
    ],
    "make_mobility_international": [
        "How does the rich taking more hurt the American Dream?",
    ],
    "make_county_heatmap": [
        "White Male Upward Mobility",
        "Black Male Upward Mobility",
        "White Male Jail Rate",
        "Black Male Jail Rate",
    ],
    "make_healthcare": [
        "Healthcare Cost per Person",
        "Life Expectancy",
        "Infant Mortality",
        "Mother Mortality",
        "Suicide Rates",
    ],
    "make_justice_jail": [
        "White Male Jail Rate",
        "Black Male Jail Rate",
    ],
    "make_electricity_cost": [
        "Cost of Electricity",
    ],
    "make_state_home_affordability": [
        "Percent of Income to Purchase a Home (by State)",
    ],
    "co_ballot_2025": [
        "Colorado 2025 Ballot — Proposition LL & MM",
    ],
}


def _parse_sources_md() -> dict:
    """Parse sources.md at startup into {popup: {func: html}, page: html}.

    sources.md structure:
      # Category       ← tier 1
      ## func_name     ← tier 2 (plot function or "Additional")
      ### Sources / Steps / Notes  ← tier 3
    """
    import re

    sources_path = _here.parent / "sources.md"
    if not sources_path.exists():
        return {"popup": {}, "page": ""}

    # ── Parse into structured dict ──────────────────────────────────────
    parsed: dict = {}
    current_category: str | None = None
    current_func: str | None = None
    current_subsec: str | None = None

    for raw_line in sources_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if re.match(r"^# [^#]", line):
            current_category = line[2:].strip()
            parsed[current_category] = {}
            current_func = None
            current_subsec = None
        elif re.match(r"^## [^#]", line):
            current_func = line[3:].strip()
            if current_category is not None:
                parsed[current_category][current_func] = {
                    "sources": [],
                    "steps": [],
                    "notes": [],
                }
            current_subsec = None
        elif re.match(r"^### [^#]", line):
            label = line[4:].strip().rstrip(":").lower()
            current_subsec = label if label in ("sources", "steps", "notes") else None
        elif current_category and current_func and current_subsec:
            bucket = parsed[current_category][current_func][current_subsec]
            if re.match(r"^#### [^#]", line):
                # Sub-heading within a recognised subsection — stored with marker
                bucket.append("__h__" + line[5:].strip())
            elif line.startswith("* ") or line.startswith("- "):
                bucket.append(line[2:].strip())
            elif re.match(r"^\d+\. ", line):
                bucket.append(re.sub(r"^\d+\. ", "", line).strip())
            elif line:
                bucket.append(line)

    def _render_sources_list(items: list[str], tag: str = "ul") -> list[str]:
        """Render a list of source items, treating __h__ entries as sub-headings."""
        out: list[str] = []
        in_list = False
        for item in items:
            if item.startswith("__h__"):
                if in_list:
                    out.append(f"</{tag}>")
                    in_list = False
                out.append(f'<p class="sources-subhead">{item[5:]}</p>')
            else:
                if not in_list:
                    out.append(f"<{tag}>")
                    in_list = True
                out.append(f"  <li>{_inline_md(item)}</li>")
        if in_list:
            out.append(f"</{tag}>")
        return out

    # ── Build popup HTML {func_name: html} ─────────────────────────────
    popup: dict[str, str] = {}
    for _cat, funcs in parsed.items():
        for func_name, data in funcs.items():
            if func_name == "Additional":
                continue
            sources, steps = data["sources"], data["steps"]
            charts = _FUNC_CHARTS.get(func_name, [])
            if not sources and not steps:
                continue
            parts: list[str] = []
            if charts:
                parts += ["<p><strong>Charts using this data</strong></p>", "<ul>"]
                parts += [f"  <li>{c}</li>" for c in charts]
                parts.append("</ul>")
            if sources:
                parts.append("<p><strong>Sources</strong></p>")
                parts += _render_sources_list(sources)
            if steps:
                parts += ["<p><strong>Steps</strong></p>"]
                parts += _render_sources_list(steps, tag="ol")
            popup[func_name] = "\n".join(parts)

    # ── Build Sources tab page HTML ─────────────────────────────────────
    page_lines = [
        "<h1>Sources</h1>",
        '<p class="sources-intro">The data used for the Breathe Voter Compass comes from publicly available sources listed below.</p>',
        "",
    ]
    for category, funcs in parsed.items():
        for func_name, data in funcs.items():
            sources, steps, notes = data["sources"], data["steps"], data["notes"]
            charts = _FUNC_CHARTS.get(func_name, [])
            if not sources and not steps and not notes:
                continue
            display = _func_display(category, func_name)
            if func_name == "Additional":
                title = f"{category} — Additional Sources"
            else:
                title = (
                    display
                    if display.lower().startswith(category.lower())
                    else f"{category} — {display}"
                )
            page_lines.append("  <section>")
            page_lines.append(f"    <h2>{title}</h2>")
            if charts:
                chart_list = ", ".join(f"<em>{c}</em>" for c in charts)
                page_lines.append(
                    f'    <p class="chart-list">Used in: {chart_list}</p>'
                )
            for note in notes:
                page_lines.append(f"    <p>{_inline_md(note)}</p>")
            if sources:
                page_lines += ["    " + ln for ln in _render_sources_list(sources)]
            if steps:
                page_lines += [
                    "    " + ln for ln in _render_sources_list(steps, tag="ol")
                ]
            page_lines.append("  </section>")
            page_lines.append("")

    return {"popup": popup, "page": "\n".join(page_lines)}


# Parsed once at startup; restart server after editing sources.md
_SOURCES_CACHE: dict = _parse_sources_md()


@app.get("/api/sources")
async def api_sources():
    return JSONResponse(_SOURCES_CACHE)


@app.get("/api/countries")
async def api_countries():
    countries = (
        shares_wid.select("country")
        .unique()
        .sort("country")
        .to_numpy()
        .flatten()
        .tolist()
    )
    return {"countries": countries}


# --- Economy ---


@app.get("/api/economy/income")
async def api_economy_income(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
    country: str = Query("usa"),
    title: str = Query(""),
):
    return fig_to_json(
        fig=make_economy_income(
            dark_mode=dark_mode, income_level=income_level, country=country, title=title
        )
    )


@app.get("/api/economy/barchart")
async def api_economy_barchart(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
    highlight_canada: bool = Query(False),
    selected_country: str = Query("usa"),
):
    return fig_to_json(
        fig=make_economy_barchart(
            dark_mode=dark_mode,
            income_level=income_level,
            highlight_canada=highlight_canada,
            selected_country=selected_country,
        )
    )


@app.get("/api/economy/income-taxes")
async def api_economy_income_taxes(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
):
    return fig_to_json(
        fig=make_economy_income_taxes(dark_mode=dark_mode, income_level=income_level)
    )


@app.get("/api/economy/house-purchase-cost")
async def api_economy_house(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
):
    return fig_to_json(
        fig=make_economy_house_purchase(dark_mode=dark_mode, income_level=income_level)
    )


@app.get("/api/economy/f150")
async def api_economy_f150(
    dark_mode: str = Query("light"),
    income_level: str = Query("Bottom 50%"),
):
    return fig_to_json(
        fig=make_economy_f150(dark_mode=dark_mode, income_level=income_level)
    )


@app.get("/api/economy/american-dream-kids")
async def api_american_dream_kids(dark_mode: str = Query("light")):
    return fig_to_json(fig=make_american_dream_kids(dark_mode=dark_mode))


@app.get("/api/economy/mobility-international")
async def api_mobility_international(dark_mode: str = Query("light")):
    return fig_to_json(fig=make_mobility_international(dark_mode=dark_mode))


@app.get("/api/economy/upward-mobility")
async def api_upward_mobility(
    dark_mode: str = Query("light"),
    race: str = Query("white"),
):
    return fig_to_json(
        fig=make_county_heatmap(
            dark_mode=dark_mode,
            race=race,
            metric="upward_mobility",
            title=f"{race.title()} Male Upward Mobility",
            subtitle="parents in bottom 25th of income",
        )
    )


# --- Healthcare ---


@app.get("/api/healthcare/cost-per-capita")
async def api_healthcare_cost(dark_mode: str = Query("light")):
    return fig_to_json(
        fig=make_healthcare(
            data=healthcare_cost_per_capita,
            title="Healthcare Cost per Person",
            yaxis_title="U.S. $",
            dark_mode=dark_mode,
        )
    )


@app.get("/api/healthcare/life-expectancy")
async def api_healthcare_life(dark_mode: str = Query("light")):
    return fig_to_json(
        fig=make_healthcare(
            data=healthcare_life_expectancy,
            title="Life Expectancy",
            yaxis_title="years",
            dark_mode=dark_mode,
        )
    )


@app.get("/api/healthcare/infant-mortality")
async def api_healthcare_infant(dark_mode: str = Query("light")):
    return fig_to_json(
        fig=make_healthcare(
            data=healthcare_infant_mortality,
            title="Infant Mortality",
            yaxis_title="deaths per 1,000 babies",
            dark_mode=dark_mode,
        )
    )


@app.get("/api/healthcare/maternal-mortality")
async def api_healthcare_maternal(dark_mode: str = Query("light")):
    return fig_to_json(
        fig=make_healthcare(
            data=healthcare_maternal_mortality,
            title="Mother Mortality",
            yaxis_title="deaths per 100,000 births",
            dark_mode=dark_mode,
        )
    )


@app.get("/api/healthcare/suicide-rates")
async def api_healthcare_suicide(dark_mode: str = Query("light")):
    return fig_to_json(
        fig=make_healthcare(
            data=healthcare_suicide_rates,
            title="Suicide Rates",
            yaxis_title="deaths per 100,000",
            dark_mode=dark_mode,
        )
    )


# --- Justice ---


@app.get("/api/justice/jail")
async def api_justice_jail(
    dark_mode: str = Query("light"),
    race: str = Query("white"),
):
    return fig_to_json(
        fig=make_county_heatmap(
            dark_mode=dark_mode,
            race=race,
            metric="jail",
            title=f"{race.title()} Male Jail Rate",
            subtitle="parents in bottom 25th of income",
        )
    )


# --- State home affordability ---


@app.get("/api/economy/state-home-affordability")
async def api_state_home_affordability(
    state: str = Query("CO"),
    dark_mode: str = Query("light"),
):
    return fig_to_json(
        fig=make_state_home_affordability(state=state, dark_mode=dark_mode)
    )


# --- Environment ---


@app.get("/api/environment/electricity-cost")
async def api_electricity_cost(dark_mode: str = Query("light")):
    return fig_to_json(fig=make_electricity_cost(dark_mode=dark_mode))


# ---------------------------------------------------------------------------
# CSV download endpoints
# ---------------------------------------------------------------------------


def _csv(df: pl.DataFrame, filename: str) -> Response:
    return Response(
        content=df.write_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}.csv"'},
    )


@app.get("/api/csv/income")
async def csv_income(
    income_level: str = Query("Bottom 50%"), country: str = Query("usa")
):
    income_col = INCOME_LEVELS[income_level]
    usa = (
        shares_wid.filter(pl.col("country") == "usa")
        .filter(pl.col("year") >= 1880)
        .select(["year", income_col])
        .rename({income_col: "usa"})
    )
    if country == "usa":
        return _csv(usa, "income_usa")
    other = (
        shares_wid.filter(pl.col("country") == country)
        .filter(pl.col("year") >= 1880)
        .select(["year", income_col])
        .rename({income_col: country})
    )
    return _csv(
        usa.join(other, on="year", how="full").sort("year"), f"income_usa_vs_{country}"
    )


@app.get("/api/csv/barchart")
async def csv_barchart(income_level: str = Query("Bottom 50%")):
    income_col = INCOME_LEVELS[income_level]
    df = (
        shares_wid.filter(pl.col("year") == shares_wid["year"].max())
        .select(["country", income_col])
        .sort("country")
    )
    return _csv(df, "income_by_country")


@app.get("/api/csv/income-taxes")
async def csv_income_taxes(income_level: str = Query("Bottom 50%")):
    income_col = INCOME_LEVELS[income_level]
    usa = (
        shares_wid.filter(pl.col("country") == "usa")
        .filter(pl.col("year") > 1880)
        .select(["year", income_col])
    )
    df = usa.join(
        tax.select(["year", "rate_top_bracket", "change_top_bracket"]),
        on="year",
        how="left",
    ).sort("year")
    return _csv(df, "income_and_taxes")


@app.get("/api/csv/house-purchase-cost")
async def csv_house_purchase(income_level: str = Query("Bottom 50%")):
    income_col = INCOME_LEVELS[income_level]
    income = (
        shares_wid.filter(pl.col("country") == "usa")
        .filter(pl.col("year") >= 1880)
        .select(["year", income_col])
    )
    df = (
        house_purchase_cost_as_percent_of_income.join(income, on="year", how="inner")
        .with_columns(
            (pl.col("cost") / pl.col(income_col)).alias("house_pct_of_income")
        )
        .sort("year")
    )
    return _csv(df, "house_purchase_cost")


@app.get("/api/csv/f150")
async def csv_f150(income_level: str = Query("Bottom 50%")):
    income_col = INCOME_LEVELS[income_level]
    income = (
        shares_wid.filter(pl.col("country") == "usa")
        .filter(pl.col("year") >= 1880)
        .select(["year", income_col])
    )
    df = (
        f150.join(income, on="year", how="inner")
        .with_columns((pl.col("price") / pl.col(income_col)).alias("price_ratio"))
        .sort("year")
    )
    return _csv(df, "f150_cost")


@app.get("/api/csv/american-dream-kids")
async def csv_american_dream_kids():
    df = (
        mobility_international.select(["country", "year", "mobility"])
        .filter(pl.col("mobility").is_not_nan())
        .sort(["country", "year"])
    )
    return _csv(df, "american_dream_kids")


@app.get("/api/csv/mobility-international")
async def csv_mobility_international():
    df = (
        mobility_international.select(["country", "year", "growth_controlled"])
        .filter(pl.col("growth_controlled").is_not_nan())
        .sort(["country", "year"])
    )
    return _csv(df, "mobility_international")


@app.get("/api/csv/upward-mobility")
async def csv_upward_mobility(race: str = Query("white")):
    df = (
        outcomes_upward_mobility_jail.filter(pl.col("metric") == "upward_mobility")
        .filter(pl.col("race") == race)
        .select(["fips_county", "county", "state", "race", "value"])
        .sort(["state", "county"])
    )
    return _csv(df, f"upward_mobility_{race}")


@app.get("/api/csv/healthcare")
async def csv_healthcare(metric: str = Query("cost-per-capita")):
    data_map = {
        "cost-per-capita": healthcare_cost_per_capita,
        "life-expectancy": healthcare_life_expectancy,
        "infant-mortality": healthcare_infant_mortality,
        "maternal-mortality": healthcare_maternal_mortality,
        "suicide-rates": healthcare_suicide_rates,
    }
    df = data_map.get(metric, healthcare_cost_per_capita)
    return _csv(df.sort(["country", "year"]), metric.replace("-", "_"))


@app.get("/api/csv/jail")
async def csv_jail(race: str = Query("white")):
    df = (
        outcomes_upward_mobility_jail.filter(pl.col("metric") == "jail")
        .filter(pl.col("race") == race)
        .select(["fips_county", "county", "state", "race", "value"])
        .sort(["state", "county"])
    )
    return _csv(df, f"jail_{race}")


@app.get("/api/csv/electricity-cost")
async def csv_electricity_cost():
    return _csv(electricity_cost, "electricity_cost")


@app.get("/api/csv/state-home-affordability")
async def csv_state_home_affordability(state: str = Query("CO")):
    df = house_purchase_cost_as_percent_of_income_state_level.filter(
        pl.col("state") == state
    ).sort("date")
    return _csv(df, f"home_affordability_{state}")
