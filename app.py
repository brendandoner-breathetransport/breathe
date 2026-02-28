import numpy as np
import pandas as pd
import polars as pl
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import logging
# Configure basic logging to display INFO messages and above
logging.basicConfig(level=logging.INFO)
# Get a logger instance for the current module
logger = logging.getLogger(__name__)
logger.info(f"plotly.__version__: {plotly.__version__}")
logger.info(f"pl.__version__: {pl.__version__}")
logger.info(f"pd.__version__: {pd.__version__}")

from pathlib import Path
from htmltools import HTML, div
from shiny import App, reactive, ui, render
from shinywidgets import output_widget, render_widget


def get_path(folder, file_name):
    path = str(Path(__file__).parent / f"data/{folder}/{file_name}")
    return path

def read_data(folder, file_name, dtype=None):
    if dtype is None:
        data = pl.from_pandas(
            pd.read_csv(
                get_path(folder=folder, file_name=file_name),
                delimiter=",",
            )
        )
    else:
        data = pl.from_pandas(
            pd.read_csv(
                get_path(folder=folder, file_name=file_name),
                delimiter=",",
                dtype=dtype,
            )
        )
    return data

config = dict(
    fixedrange=True,
    yaxis_range_pct=0.25,
    plotly_mobile={
        'staticPlot': False,
        'responsive': True,
        'displayModeBar': False,
        'scrollZoom': False,
        'doubleClick': False,
    },
    colorscale={
        'upward_mobility':[
            [0.0, '#8B0000'],      # 0.00 - Dark red
            [0.40, '#CC0000'],    # 0.10 - Red
            [0.45, '#FF8C00'],    # 0.25 - Orange
            [0.5, '#FFD700'],      # 0.30 - Gold/Yellow
            [0.583, '#FFFF00'],    # 0.35 - Bright yellow
            [0.667, '#ADFF2F'],    # 0.40 - Yellow-green
            [0.833, '#32CD32'],    # 0.50 - Lime green
            [1.0, '#006400'],      # 0.60 - Dark green
        ],
        'jail':[
            [0.0, '#006400'],      # 0.00 - Dark green
            [0.02, '#228B22'],     # 0.03 - Forest green
            [0.05, '#32CD32'],      # 0.06 - Lime green
            [0.08, '#9ACD32'],     # 0.09 - Yellow-green
            [0.10, '#ADFF2F'],      # 0.12 - Green-yellow
            [0.12, '#FFD700'],     # 0.15 - Gold/Yellow
            [0.15, '#CC0000'],    # 0.375 - Red
            [1.0, '#8B0000'],      # 0.60 - Dark red
        ],
    },
    countries=[
        # 'Australia',
        'Canada',
        'Europe',
        'Japan',
        'United States',
    ],

)

#-----------------------------------------------------------------------------------------
# Race Data
#-----------------------------------------------------------------------------------------
outcomes_upward_mobility_jail = read_data(
    folder='race',
    file_name='outcomes_upward_mobility_jail.csv',
    dtype={
        'fips_county': str,
        'fips_state': str,
        'value': float,
        'state': str
    },
)
with open(get_path(folder='race', file_name='counties_json.pickle'), 'rb') as f:
    counties_json = pickle.load(f)
#-----------------------------------------------------------------------------------------
# Economy Data
#-----------------------------------------------------------------------------------------
n_workers_full_time = read_data(folder='economy', file_name='n_workers_full_time.csv')
shares_wid = read_data(folder='economy', file_name="shares_wid.csv")
shares_wid_full_distribution = read_data(folder='economy', file_name="shares_wid_full_distribution.csv")

year_max = shares_wid.select(pl.max('year')).to_numpy().flatten()[0]
tax = read_data(folder='economy', file_name="tax.csv")
income_total = read_data(folder='economy', file_name="income_total.csv")
population = read_data(folder='economy', file_name="population.csv")
workers_ratio = read_data(folder='economy', file_name="workers_ratio.csv")
f150 = read_data(folder='economy', file_name="f150.csv")

#-----------------------------------------------------------------------------------------
# Healthcare Data
#-----------------------------------------------------------------------------------------
healthcare_cost_per_capita = read_data(folder='healthcare', file_name='healthcare_cost_per_capita.csv')
healthcare_life_expectancy = read_data(folder='healthcare', file_name='healthcare_life_expectancy.csv')
healthcare_infant_mortality = read_data(folder='healthcare', file_name='healthcare_infant_mortality.csv')
healthcare_maternal_mortality = read_data(folder='healthcare', file_name='healthcare_maternal_mortality.csv')
healthcare_suicide = read_data(folder='healthcare', file_name='healthcare_suicide_rates.csv')

#-----------------------------------------------------------------------------------------
# American Dream Data
#-----------------------------------------------------------------------------------------
american_dream_kids = read_data(folder='american_dream', file_name='american_dream_kids.csv')
mobility_international = read_data(folder='american_dream', file_name='mobility_international.csv')

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Environment
#-----------------------------------------------------------------------------------------
electricity_cost = (
    read_data(folder='environment', file_name='levelized_cost_of_energy_comparison_lazard.csv')
    .sort(['LCOE_Low_USD_MWh'], descending=True)
)
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

axis_title_income = "<b>income/yr average</b>"
axis_title_income_format = ',.2s'

income_levels = {
    "Bottom 50%": "income_mean_bottom",
    "Upper 51-99%": "income_mean_upper",
    "Top 1%": "income_mean_top",
    "Bottom 50% to Top 1% Gap": 'income_mean_gap',
}
group_names = {
    "income_mean_bottom": "Bottom 50%",
    "income_mean_upper": "Upper 51-99%",
    'income_mean_top': "Top 1%",
    "income_mean_gap": "Bottom 50% to Top 1% Gap",
}

layout_economy = {
    'range':[1905, 2030],
    'tickvals':[1902, 1945, 1969, 1980, 2023, 2032],
    'ticktext':[1902, 1945, 1969, 1980, 2023, ''],
}

def get_source(name, link):
    return f"<a href='{link}'>{name}</a>"


sources = {
    'economy': get_source(name='Sources', link='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy'),
    'economy_f150': get_source(name='Sources', link='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy#ford-f-seriesf-150-historical-msrp-1950-2025'),
    'wid': get_source(name='Source: World Inequality Database', link='https://wid.world/wid-world/'),
    'irs': get_source(name='Source: Internal Revenue Service', link='https://www.irs.gov/statistics/soi-tax-stats-historical-table-23'),
    '1619': get_source(name='Source: The 1619 Project', link='https://www.nytimes.com/interactive/2019/08/14/magazine/1619-america-slavery.html'),
    'american_character': get_source(name='Source: American Character', link='https://colinwoodard.com/books/american-character/'),
    'american_dream': get_source(name='Sources', link='https://github.com/brendandoner-breathetransport/breathe/wiki/American-Dream'),
    'healthcare': get_source(name='Sources', link='https://github.com/brendandoner-breathetransport/breathe/wiki/Healthcare'),
}

colors = [
    'rgba(167, 135, 114, 0.5)',
    'rgba( 10, 150, 81, 0.5)',
    'rgba(101, 104, 15, 0.5)',
    'rgba(38, 56, 224, 0.5)',
    'rgba(10, 206, 76, 0.5)',
    'rgba(16, 74, 183, 0.5)',
    'rgba(13, 200, 106, 0.5)',
    'rgba(220, 184, 61, 0.5)',
    'rgba(127, 202, 163, 0.5)',
]
colors_dem = [
    'rgba(117, 184, 116,   0.3)',
    'rgba(110, 167,  96,   0.3)',
    'rgba(108, 178,  88,   0.3)',
    'rgba( 90, 185, 111,   0.3)',
    'rgba(103, 188,  96,   0.3)',
    'rgba(117, 199,  95,   0.3)',
    'rgba(111, 174,  96,   0.3)',
]
colors_auth = [
    'rgba(230, 78, 67,    0.7)',
    'rgba(220, 88,  57,   0.7)',
    'rgba(225, 82,  62,   0.7)',
]
color_light_dark = {
    # 'light': 'rgba(0,0,0,0.5)',
    'light': 'rgba(68, 122, 219, 0.5)',
    'dark': 'rgba(255,255,255,0.5)',
}
colors_by_country = {
    'australia': 'rgba( 90, 185, 111,   0.3)',
    'france': 'rgba( 90, 185, 111,   0.3)',
    'switzerland': 'rgba( 90, 185, 111,   0.3)',
    'canada':'rgba( 90, 185, 111,   0.3)',
    'germany':'rgba( 90, 185, 111,   0.3)',
    'italy':'rgba( 90, 185, 111,   0.3)',
    'japan':'rgba( 90, 185, 111,   0.3)',
    'new_zealand':'rgba( 90, 185, 111,   0.3)',
    'norway':'rgba( 90, 185, 111,   0.3)',
    'uk':'rgba( 90, 185, 111,   0.3)',
    'russia':'rgba(230, 78, 67,    0.7)',
    'china':'rgba(230, 78, 67,    0.7)',
    'usa':color_light_dark['light'],
}
colors_tax_changes = {
    'up': 'rgba( 90, 185, 111,   0.3)',
    'down': 'rgba(230, 78, 67,    0.7)',
}



def get_color_template(mode):
    if mode == "light":
        return "plotly_white"
    else:
        return "plotly_dark"


def get_background_color_plotly(mode):
    if mode == "light":
        return "white"
    else:
        return "rgb(29, 32, 33)"


def plot_stick_figure(fig, x, y, add_hat=False):
    color_rect = "rgba(44, 76, 126, 0.3)" # rgba(44, 76, 126, 0.3) darkblue, rgba(150,55,55,0.5) red
    color_legs = "rgba(0,0,0,0.7)"
    # color_legs="rgba(150,55,55,0.7)"
    x0 = x
    x1 = x0 + 0.4
    y0 = y + 80000
    y1 = y0 + 80000

    fig.add_shape(
        # Body
        name='none',
        type="rect",
        # Rectangle reference to the axes xref="x", yref="y",
        # Rectangle reference to the plot xref="paper", yref="paper",
        xref="x", yref="y",
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(color=color_rect, ), fillcolor=color_rect,
    )
    fig.add_shape(
        # head
        type="circle",
        xref="x", yref="y",
        x0=(x0 + x1) / 2 - 0.3, x1=(x0 + x1) / 2 + 0.3, y0=(y1 + 10000), y1=(y1 + 70000),
        line_color="rgba(44, 76, 126, 0.7)", # darkblue rgba(44, 76, 126, 0.7)
        fillcolor="rgba(44, 76, 126, 0.7)",
    )
    if add_hat:
        fig.add_shape(
            # Brim
            name='none',
            type="line",
            # Rectangle reference to the axes xref="x", yref="y",
            # Rectangle reference to the plot xref="paper", yref="paper",
            xref="x", yref="y",
            x0=x0 - 0.45, x1=x1 + 0.45, y0=(y1 + 80000), y1=(y1 + 80000),
            line=dict(color=color_legs, width=2), fillcolor=color_legs,
        )
        fig.add_shape(
            # hat
            name='none',
            type="rect",
            # Rectangle reference to the axes xref="x", yref="y",
            # Rectangle reference to the plot xref="paper", yref="paper",
            xref="x", yref="y",
            x0=x0 - 0.08, x1=x1 + 0.08, y0=(y1 + 80000), y1=(y1 + 120000),
            line=dict(color=color_legs, ), fillcolor=color_legs,
        )
        fig.add_shape(
            # Leg 1
            name='none',
            type="line",
            xref="x", yref="y",
            x0=x0 - 0.03, x1=(x1 + x0) / 2, y0=y, y1=y0,
            line=dict(color=color_legs, ), fillcolor=color_legs,
        )
        fig.add_shape(
            # Leg 2
            name='none',
            type="line",
            xref="x", yref="y",
            x0=x1 + 0.03, x1=(x1 + x0) / 2, y0=y, y1=y0,
            line=dict(color=color_legs, ), fillcolor=color_legs,
        )
        fig.add_shape(
            # Arm 1
            name='none',
            type="line",
            xref="x", yref="y",
            x0=x0 - 0.4, x1=x0, y0=y1 - 80000, y1=y1,
            line=dict(color=color_legs, ), fillcolor=color_legs,
        )
        fig.add_shape(
            # Arm 2
            name='none',
            type="line",
            xref="x", yref="y",
            x0=x1, x1=x1 + 0.4, y0=y1, y1=y1 - 80000,
            line=dict(color=color_legs, ), fillcolor=color_legs,
        )
        fig.add_shape(
            # Cane
            name='none',
            type="line",
            # Rectangle reference to the axes xref="x", yref="y",
            # Rectangle reference to the plot xref="paper", yref="paper",
            xref="x", yref="y",
            x0=x1 + 0.4, x1=x1 + 0.4 + 0.3, y0=y1 - 80000, y1=y,
            line=dict(color=color_legs, ), fillcolor=color_legs,
        )
        return None

def get_income_mean(group, data):
    income_mean = (
        data
        .filter(pl.col('group') == group)
        .select('value')
        .to_numpy().flatten()[0]
    )
    return income_mean


def plot_timeseries_multiple_countries(data, title, yaxis_title, xaxis_title, dark_mode):
    data = (
        data
        .filter(pl.col('year')>=2000)
    )
    data_most_recent = (
        data
        .join(
            other=(
                data
                .group_by('country')
                .agg(
                    pl.max('year')
                )
            ),
            on=['country', 'year'],
            how='inner',
        )
    )

    countries = [
        "united states", "europe", "costa rica", "japan", "china",
        # 'costa rica',
        # # 'mexico',
        # 'australia',
        #
        # 'europe',
        #
        'canada',
        #
        # 'japan',
        # 'new zealand',  # New Zealand
        #
        # # 'Russian Federation',  # Russian Federation
        # 'china',
        # 'united states',  # United States
    ]

    fig = go.Figure(
        data=(
                [
                    go.Scatter(
                        name=f"{country}",
                        mode='lines',
                        x=data.filter(pl.col('country') == country)['year'],
                        y=data.filter(pl.col('country') == country)['value'],
                        line=dict(color=color_light_dark[dark_mode], width=3) if country=='united states' else dict(color="rgba(0,0,0,0.2)", width=2),
                    ) for country in countries
                ]
                + [
                    go.Scatter(
                        name="NONE",
                        mode='text',
                        x=data_most_recent.filter(pl.col('country') == country)['year'],
                        y=data_most_recent.filter(pl.col('country') == country)['value'],
                        text=f"<b>{country.title()}</b>" if country == 'united states' else f"<br>{country.title()}" if country == 'canada' else f"{country.title()}",
                        textposition='middle right',
                    ) for country in countries # ["united states", "europe", "costa rica", "japan", "china"]
                ]
        )
    )

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
        ),
        title_x=0.5,
        yaxis_title=f"<b>{yaxis_title}</b>",
        yaxis=dict(
            fixedrange=config['fixedrange'],  # This prevents zooming
        ),
        xaxis_title=xaxis_title,
        xaxis=dict(
            range=[2000, 2026],
            fixedrange=config['fixedrange'],  # This prevents zooming
        ),
        showlegend=False,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color_plotly(dark_mode),
    )

    for trace in fig['data']:
        if 'NONE' in trace['name']:
            trace['showlegend'] = False

    fig = go.FigureWidget(fig)
    fig._config = fig._config | config['plotly_mobile']
    return fig

def get_text(text, prefix, suffix, format, context):
    """
    rgb(68, 122, 219)=blue used for links
    :param text:
    :param prefix:
    :param suffix:
    :param format:
    :return:
    """
    return f"<span style='color:rgb(0, 0, 0)'><b>{prefix}{text:{format}}{suffix}</b><br>{context}</span>"

def get_highlights_line_min_max(data, col_date, col_metric, number_type, max_or_min):
    format = {
        'thousands': ".0f",
        'percentage': ".0%",
    }[number_type]
    prefix = {
        'thousands': "$",
        'percentage': "",
    }[number_type]
    suffix = {
        'thousands': "k",
        'percentage': "",
    }[number_type]
    divide_by = {
        'thousands': 1000,
        'percentage': 1,
    }[number_type]

    data_latest = data.filter(pl.col(col_date) == data[col_date].max())
    data_min = data.filter(pl.col(col_metric) == data[col_metric].min())
    data_max = data.filter(pl.col(col_metric) == data[col_metric].max())

    highlight_latest = [
        go.Scatter(
            # highlight the most recent value
            name='NONE',
            mode='markers+text',
            x=data_latest[col_date],
            y=data_latest[col_metric],
            marker=dict(color='orange', size=8),
            text=get_text(
                text=data_latest[col_metric].to_numpy().flatten()[0] / divide_by,
                prefix=prefix,
                suffix=suffix,
                format=format,
                context='',
            ),
            textposition='middle center',
        ),
    ]

    if (max_or_min=='min') | (max_or_min=='both'):
        highlight_min = [
            go.Scatter(
                # highlight the min of the metric
                name='NONE',
                mode='markers+text',
                x=data_min[col_date],
                y=data_min[col_metric],
                marker=dict(color='orange', size=8),
                text=get_text(
                    text=data_min[col_metric].to_numpy().flatten()[0] / divide_by,
                    prefix=prefix,
                    suffix=suffix,
                    format=format,
                    context='min',
                ),
                textposition='middle center',
            ),
        ]
    if (max_or_min == 'max') | (max_or_min == 'both'):
        highlight_max = [
            go.Scatter(
                # highlight the max of the metric
                name='NONE',
                mode='markers+text',
                x=data_max[col_date],
                y=data_max[col_metric],
                marker=dict(color='orange', size=8),
                text=get_text(
                    text=data_max[col_metric].to_numpy().flatten()[0] / divide_by,
                    prefix=prefix,
                    suffix=suffix,
                    format=format,
                    context='max',
                ),
                textposition='middle center',
            ),
        ]

    highlights = highlight_latest
    # if data_latest[col_metric].to_numpy().flatten()[0] != data_min[col_metric].to_numpy().flatten()[0]:
    #     highlights = highlights + highlight_min

    # make sure the most recent value (latest) is not equal to the max
    if (data_latest[col_metric].to_numpy().flatten()[0] != data_max[col_metric].to_numpy().flatten()[0]) & (max_or_min in ['max', 'both']):
        highlights = highlights + highlight_max
    # make sure the most recent value (latest) is not equal to the min
    if (data_latest[col_metric].to_numpy().flatten()[0] != data_min[col_metric].to_numpy().flatten()[0]) & (
            max_or_min in ['min', 'both']):
        highlights = highlights + highlight_min

    return highlights

def plot_period_dashed_line(fig, year=None, text=None):
    fig.add_vline(
        x=1980,
        line=dict(color='rgba(0,0,0,0.9)', width=2, dash='dash', ),
        annotation_text="1980",
        annotation_position="top right",
        annotation_font_color="black",
    )
    if year is not None:
        fig.add_vline(
            x=year,
            line=dict(color='rgba(0,0,0,0.9)', width=2, dash='dash', ),
            annotation_text=text,
            annotation_position="top right",
            annotation_font_color="black",
        )

def plot_period_shading(fig):
    fig.add_vrect(
        x0=1938,
        x1=1979,
        line_width=0,
        fillcolor='green',
        opacity=0.05,
        annotation_text="<b><a href='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy#policies'>Policies</a></b>",
        annotation_position='bottom',
    )
    fig.add_vrect(
        x0=1980,
        x1=2020,
        line_width=0,
        fillcolor='black',
        opacity=0.05,
        annotation_text="<b><a href='https://github.com/brendandoner-breathetransport/breathe/wiki/Economy#policies'>Policies</a></b>",
        annotation_position='bottom',
    )

# config['plotly_mobile'] = {
#     'responsive': True,
#     'displayModeBar': True,
#     'displaylogo': False,
#     'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
#     'toImageButtonOptions': {
#         'format': 'png',
#         'filename': 'custom_image',
#         'height': 500,
#         'width': 700,
#         'scale': 1
#     }
# }

config['plotly_mobile'] = {
    # 'staticPlot': True,
    'responsive': True,
    'displayModeBar': False,
    'displaylogo': False,
    'scrollZoom': False,        # Disable scroll wheel zoom
    'doubleClick': 'reset',     # Double click resets instead of zooms
    'showTips': False,          # Hide zoom tips
    'modeBarButtonsToRemove': [
        'pan2d', 'lasso2d', 'select2d', 'autoScale2d',
        'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
        'zoom2d', 'zoomIn2d', 'zoomOut2d',  # Remove zoom buttons
        'autoScale2d', 'resetScale2d'        # Remove scale buttons
    ],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'income_timeseries',
        'height': 400,
        'width': 700,
        'scale': 1
    }
}

def plot_county_heatmap(
        data: pl.DataFrame,
        counties_json,
        race: str,
        metric: str,
        title: str,
        colorscale,
        dark_mode,
):
    """
    Create a county-level heatmap for the US
    """
    start = data.filter(pl.col('metric') == metric)['value'].min()
    stop = data.filter(pl.col('metric') == metric)['value'].max()

    data_filtered = (
        data
        .filter(pl.col('metric') == metric)
        .filter(pl.col('race') == race)
        # .filter(pl.col('state') == "CA")
        .to_pandas()
    )
    # logger.info(
    #     f"outcomes_upward_mobility_jail CA shape: {data_filtered.query("state=='CA'").dropna().shape}")
    fig = go.Figure(
        go.Choropleth(
            locations=data_filtered['fips_county'],  # You'll need county FIPS codes
            z=data_filtered['value'],
            locationmode='geojson-id',
            geojson=counties_json,
            colorscale=colorscale,
            zmin=start,
            zmax=stop,
            hovertemplate='<b>%{text}</b><br>' +
                          f'{title}: %{{z:.2f}}<br>' +
                          '<extra></extra>',
            text=data_filtered['county'] + ', ' + data_filtered['state'],
            marker=dict(
                line=dict(
                    width=0  # Set to 0 to remove outlines completely
                )
            ),
            colorbar=dict(
                # title=metric + ' % of cohort<br>',
                title=None,
                orientation="h",  # horizontal orientation
                # x=0.0,  # center horizontally
                # xanchor="center",
                y=-0.1,  # position below the plot
                yanchor="top",
                thickness=10,  # adjust thickness as needed
                len=0.80  # adjust length (0.8 = 80% of plot width)
            ),
        )
    )

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
        ),
        title_x=0.5,
        showlegend=False,
        template=get_color_template(dark_mode),
        paper_bgcolor=get_background_color_plotly(dark_mode),
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'
        ),
    )

    fig = go.FigureWidget(fig)
    fig._config = fig._config | config['plotly_mobile']

    return fig

def get_yaxis_range(y_data):
    if ~isinstance(y_data, np.ndarray):
        try:
            # polars
            y_data = y_data.to_numpy()
        except:
            # pandas
            y_data = y_data.values

    min = np.min(y_data)
    max = np.max(y_data)
    range = max - min
    yaxis_min = min - (range * config['yaxis_range_pct'])
    yaxis_max = max + (range * config['yaxis_range_pct'])

    return yaxis_min, yaxis_max

app_ui = ui.page_fillable(
    ui.tags.head(
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1.0"),
    ),
    ui.page_navbar(
        #--------------------------------------------------------------------------------------------------
        # Economy
        #--------------------------------------------------------------------------------------------------
        ui.nav_panel(
            "Economy",
            ui.row(ui.h1(ui.span(HTML("How healthy is the economy for Americans?"), style="color:rgba(255,255,255,0.9)"))),

            # Income
            ui.row(
                ui.layout_columns(
                    ui.input_radio_buttons(
                        id='income_level',
                        label=None,
                        choices={
                            "Bottom 50%": ui.span("Bottom 50%", style=f"color:rgba(255,255,255,0.6)"),
                            "Upper 51-99%": ui.span("Upper 51-99%", style=f"color:rgba(255,255,255,0.6)"),
                            "Top 1%": ui.span("Top 1%", style=f"color:rgba(255,255,255,0.6)"),
                            # "Bottom 50% to Top 1% Gap": ui.span("Bottom 50% to Top 1% Gap", style=f"color:rgba(255,255,255,0.6)"),
                        },
                        selected="Bottom 50%",
                        inline=True,
                    ),
                    col_widths=(12,),
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.input_radio_buttons(
                        id='country',
                        label=None,
                        choices={
                            country: ui.span(country, style=f"color:rgba(255,255,255,0.6)")
                            for country in
                            shares_wid.select(['country']).unique().sort(['country']).to_numpy().flatten().tolist()
                        },
                        selected="usa",
                        inline=True,
                    ),
                    col_widths=(12,),
                )
            ),
            ui.row(ui.h3(ui.span(HTML("Income"), style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_economy_timeseries_income")),
                    ui.card(output_widget("plot_economy_barchart_income_countries")),
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},  # Stack on mobile, side-by-side on desktop
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_economy_timeseries_income_taxes")),
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},  # Stack on mobile, side-by-side on desktop
                )
            ),
            # Cost of Living
            ui.row(ui.h2(ui.span("How has the cost of food & shelter changed?", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_economy_f150")),
                    # Stack on mobile, side-by-side on desktop
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                )
            ),
            # ui.row(
            #     ui.layout_columns(
            #         ui.card(ui.h3(ui.span("main_street_income_avg vs rent/mortgage, over time", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("main_street_income_avg vs energy bills (gas, mileage, utilities, i.e. ENERGY), over time",
            #                               style="color:rgba(0,0,0,0.9)"))),
            #         col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},  # Stack on mobile, side-by-side on desktop
            #     )
            # ),
            # ui.row(
            #     ui.layout_columns(
            #         ui.card(ui.h3(ui.span("main_street_income_avg vs childcare, over time", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("main_street_income_avg vs cost of living, over time", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("main_street_income_avg vs college/trade school, over time", style="color:rgba(0,0,0,0.9)"))),
            #         col_widths={"xs": (12, 12, 12), "sm": (12, 12, 12), "md": (4, 4, 4)},
            #     )
            # ),
        ),
        #--------------------------------------------------------------------------------------------------
        # American Dream
        #--------------------------------------------------------------------------------------------------
        ui.nav_panel(
            "American Dream",
            # education, sick care, justice, laws/rules,
            ui.row(ui.h1(ui.span(
                HTML("How healthy is the American Dream?"),
                style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_american_dream_kids")),
                    ui.card(output_widget("plot_american_dream_mobility_international")),
                    # Stack on mobile, side-by-side on desktop
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_white_upward_mobility")),
                    ui.card(output_widget("plot_black_upward_mobility")),
                    # Stack on mobile, side-by-side on desktop
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                )
            ),
            # ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
            # ui.row(
            #     ui.layout_columns(
            #         ui.card(ui.h3(
            #             ui.span("incarceration rate (by race, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("likelihood rates for education levels (race, time) vs countries",
            #                               style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("loan approval rates (race, time)", style="color:rgba(0,0,0,0.9)"))),
            #         col_widths={"xs": (12, 12, 12), "sm": (12, 12, 12), "md": (4, 4, 4)},
            #     )
            # ),
            # ui.row(
            #     ui.layout_columns(
            #         ui.card(ui.h3(ui.span("stop and frisk rates (by race, by state)", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("immigration (crime rate, race, time) vs benchmarks & countries", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("crime (by state, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
            #         col_widths={"xs": (12, 12, 12), "sm": (12, 12, 12), "md": (4, 4, 4)},
            #     )
            # ),
        ),
        # --------------------------------------------------------------------------------------------------
        # Healthcare
        # --------------------------------------------------------------------------------------------------
        ui.nav_panel(
            "Healthcare",
            ui.row(ui.h1(ui.span(HTML("What is the cost and performance of the American healthcare system?"), style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_healthcare_cost_per_capita")),
                    ui.card(output_widget("plot_healthcare_life_expectancy")),
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_healthcare_infant_mortality")),
                    ui.card(output_widget("plot_healthcare_maternal_mortality")),
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_healthcare_suicide")),
                    # ui.card(output_widget("plot_healthcare_suicide")),
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                )
            ),

        ),
        # --------------------------------------------------------------------------------------------------
        # Justice
        # --------------------------------------------------------------------------------------------------
        ui.nav_panel(
            "Justice",
            ui.row(ui.h1(ui.span(HTML("How many Americans are in jail?"), style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_white_jail")),
                    ui.card(output_widget("plot_black_jail")),
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                    # Stack on mobile, side-by-side on desktop
                )
            ),
            # ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),

        ),
        # --------------------------------------------------------------------------------------------------
        # Environment
        # --------------------------------------------------------------------------------------------------
        ui.nav_panel(
            "Environment",
            # Air & Water
            ui.row(
                ui.h1(
                    ui.span(HTML("Fossil fuels are not the cheapest sources for energy."),
                                 style="color:rgba(255,255,255,0.9)")
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_electricity_cost")),
                    # ui.card(output_widget("plot_black_jail")),
                    col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},
                    # Stack on mobile, side-by-side on desktop
                )
            ),

            # ui.row(
            #     ui.layout_columns(
            #         ui.card(ui.h3(ui.span("air (standards, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("water (standards, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
            #         ui.card(ui.h3(ui.span("soil (standards, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
            #         col_widths={"xs": (12, 12, 12), "sm": (12, 12, 12), "md": (4, 4, 4)},
            #     )
            # ),
        ),
        # ui.nav_panel(
        #     "Immigration",
        #     # Air & Water
        #     ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
        # ),
        # ui.nav_panel(
        #     "Freedom",
        #     # Air & Water
        #     ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
        #     ui.row(
        #         ui.layout_columns(
        #             ui.card(ui.h3(ui.span("story of the 100 years after civil war", style="color:rgba(0,0,0,0.9)"))),
        #             ui.card(ui.h3(ui.span("incarceration rates", style="color:rgba(0,0,0,0.9)"))),
        #             ui.card(ui.h3(ui.span("rape convictions based on race of victim", style="color:rgba(0,0,0,0.9)"))),
        #             col_widths={"xs": (12, 12, 12), "sm": (12, 12, 12), "md": (4, 4, 4)},
        #         )
        #     ),
        # ),
        #
        # ui.nav_panel(
        #     "Efficiency",
        #     # Air & Water
        #     ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
        # ),
        # ui.nav_panel(
        #     "Money in Politics",
        #     # Air & Water
        #     ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
        # ),
        # ui.nav_panel(
        #     "MisInformation",
        #     # Air & Water
        #     ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
        # ),
        # ui.nav_panel(
        #     "Spotlight",
        #     # education, sick care, justice, laws/rules,
        #     ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
        #     ui.row(ui.h6(ui.span("Replace below with data driven plots...", style="color:rgba(255,255,255,0.9)"))),
        #     ui.row(
        #         ui.output_image("img_freedom_scale")
        #     ),
        #     ui.row(ui.h1(ui.span("Disruptions", style="color:rgba(255,255,255,0.9)"))),
        #     ui.row(
        #         ui.layout_columns(
        #             ui.card(ui.h3(ui.span("Climate Change", style="color:rgba(0,0,0,0.9)"))),
        #             ui.card(ui.h3(ui.span("AI",
        #                                   style="color:rgba(0,0,0,0.9)"))),
        #             # ui.card(ui.h3(ui.span("crime (by state, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
        #             col_widths={"xs": (12, 12), "sm": (12, 12), "md": (6, 6)},  # Stack on mobile, side-by-side on desktop
        #         )
        #     ),
        #     ui.row(ui.h1(ui.span("Wants", style="color:rgba(255,255,255,0.9)"))),
        #     ui.row(
        #         ui.layout_columns(
        #             ui.card(
        #                 ui.h3(ui.span("regional cultures and government preferences", style="color:rgba(0,0,0,0.9)"))),
        #             col_widths=(12,),
        #         )
        #     ),
        #     ui.row(ui.h1(ui.span("Voter supression", style="color:rgba(255,255,255,0.9)"))),
        #     ui.row(
        #         ui.layout_columns(
        #             ui.card(
        #                 ui.h3(ui.span("Voter turn out vs laws that restrict voting", style="color:rgba(0,0,0,0.9)"))),
        #             col_widths=(12,),
        #         )
        #     ),
        # ),
        # ui.nav_panel(
        #     "About Us",
        #     ui.row(ui.span(
        #         ui.markdown("""
        #             # Breathe
        #             We are a grassroots community group that has come together to support
        #             each other, pool our<br>diverse backgrounds, and bring
        #             truth, understanding, and togetherness<br>into today's conversations.
        #
        #             &ndash; Founded February, 2025
        #
        #             ### Purpose
        #             Improve the lives of Americans and make our democracy stronger.
        #
        #             ##### How
        #             * **Dashboard**
        #
        #             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Simple and reproducible, bring together data and history.
        #
        #             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Diagnose problems, see the health of the country in the context of our past and the world.
        #
        #             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Understand causes.
        #
        #             * **Community**
        #
        #             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Ideas, collaborate, support, expand impact.
        #
        #             * **Outreach**
        #
        #             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Expand impact, expand resources.
        #
        #
        #             ### Values
        #             * **Balance** (public good vs individualism)
        #             * **Fairness** (equal opportunity, equal justice, fair markets, no exploitation)
        #             * **Diversity** (team strength and learning come from diverse ideas, backgrounds, races, gender, etc.)
        #             * **Evidence** (learn from history and data)
        #
        #         """),
        #         style="color:rgba(255,255,255,0.9)")),
        #     ui.row(ui.h1(ui.span("Books Recommendations", style="color:rgba(255,255,255,0.9)"))),
        #     ui.row(
        #         ui.layout_columns(
        #             ui.tags.a(
        #                 ui.output_image("img_american_character"),
        #                 href='https://colinwoodard.com/books/american-character/',
        #                 target="_blank"
        #             ),
        #             col_widths=(12),
        #         )
        #     ),
        #     ui.row(
        #         ui.layout_columns(
        #             ui.tags.a(
        #                 ui.output_image("img_1619"),
        #                 href='https://www.nytimes.com/interactive/2019/08/14/magazine/1619-america-slavery.html',
        #                 target="_blank"
        #             ),
        #             col_widths=(12,),
        #         )
        #     ),
        # ),
        # ui.nav_control(
        #     ui.a("Support Us", href="https://gofund.me/d7238719")
        # ),
        title=ui.img(src="images/logo_street.png", style="max-width:100px;width:45%"),
        # title=ui.img(src="www/logo_street.png", style="max-width:100px;width:50%"),
        # title = ui.img(src=f"www/logo_street.png", style="max-width:100px;width:50%"),
        id="page",
        sidebar=ui.sidebar(
            ui.input_dark_mode(id="dark_mode", mode="light"),
            open="closed",
        ),
        footer=ui.h6(
            "Breathe © 2025",
            style="color: white !important; text-align: center;",
        ),
        window_title="Breathe",
        # window_title="<img>src='images/browser.png'</img> Breathe",
        # window_title=div(HTML("<head><link rel='icon' href='images/browser.png'></head>")),
        # window_title='<html><head><title>My Page Title</title><link rel="icon" type="image/x-icon" href="images/browser.png"></head></html>',
        # window_title=ui.div(ui.img(src="images/browser.png", style="max-width:100px;width:50%")),
        # window_title=ui.img(src="images/browser.png", style="max-width:100px;width:50%"),
    ),
    ui.tags.style(
        """
        /* Your existing styles */
        .leaflet-popup-content {
            width: 600px !important;
        }
        .leaflet-div-icon {
            background: transparent !important;
            border: transparent !important;
        }
        .collapse-toggle {
            color: #FD9902 !important;
        }
        .main {
            background-image: url("images/background_dark_full.jpg");
            height: 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }

        /* NEW MOBILE-SPECIFIC STYLES */
        @media (max-width: 768px) {
            /* Make text larger and more readable on mobile */
            h1 { font-size: 1.8rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.2rem !important; }

            /* Stack radio buttons vertically on mobile */
            .form-check-inline {
                display: block !important;
                margin-bottom: 0.5rem;
            }

            /* Make cards full width with proper spacing */
            .card {
                margin-bottom: 1rem;
                width: 100% !important;
            }

            /* Adjust navbar for mobile */
            .navbar-nav {
                text-align: center;
            }

            /* Make plots responsive */
            .js-plotly-plot {
                width: 100% !important;
            }

            /* Reduce padding on mobile */
            .container-fluid {
                padding-left: 10px;
                padding-right: 10px;
            }
        }

        /* For very small screens */
        @media (max-width: 480px) {
            h1 { font-size: 1.5rem !important; }
            .navbar-brand img {
                max-width: 80px !important;
            }
        }
        """
    ),
    ui.head_content(div(HTML("<link rel='icon' href='images/browser.png'>"))),
    icon="images/browser.png",
)


def server(input, output, session):
    @output
    @render_widget
    def plot_economy_timeseries_income():
        """
        Source: https://wid.world/country/usa/
        Share of total,
        Pre-tax national income Bottom 50% share
        Pre-tax national income Top 1% share
        :return:
        """
        country = input.country()
        income_level = income_levels[input.income_level()]
        data = shares_wid.filter(pl.col('country') == country).filter(pl.col('year') >= 1880)
        usa = shares_wid.filter(pl.col('country') == 'usa').filter(pl.col('year') >= 1880)
        dark_mode=input.dark_mode()

        fig = go.Figure(data=(
                [
                    go.Scatter(
                        name=country,
                        x=data['year'],
                        y=data[income_level],
                        line=dict(color=color_light_dark[dark_mode], width=3),
                        text=f"<b>{country}</b>",
                    ),
                ]
                +
                get_highlights_line_min_max(
                    data=data,
                    col_date='year',
                    col_metric=income_level,
                    number_type='thousands',
                    max_or_min='max',
                )
                +
                [
                    go.Scatter(
                        name='usa',
                        x=usa['year'],
                        y=usa[income_level],
                        line=dict(color='rgba(0,0,0,0.2)', width=3),
                        text=f"<b>usa</b>",
                    ),
                ]
                +
                get_highlights_line_min_max(
                    data=usa,
                    col_date='year',
                    col_metric=income_level,
                    number_type='thousands',
                    max_or_min='max',
                )
        ))

        if country in ['canada', 'france']:
            year = {
                'canada':2004,
                'france':1995,
            }[country]
            text = {
                'canada': '2004<br>canadian<br>corporate<br>money<br>ban',
                'france': '1995<br>french<br>corporate<br>money<br>ban',
            }[country]

        else:
            year=None
            text=None

        plot_period_dashed_line(fig=fig, year=year, text=text)
        plot_period_shading(fig=fig)

        yaxis_min, yaxis_max = get_yaxis_range(y_data=data[income_level])
        fig.update_layout(
            title=dict(
                text=f"<b>{income_level if income_level != 'Gap' else 'the ' + income_level + ' of'} Paycheck</b><br><sup>{year_max} dollars</sup>",
                #
            ),
            title_x=0.5,
            yaxis_title=axis_title_income,
            yaxis=dict(
                range=[yaxis_min, yaxis_max],
                tickprefix="$",
                tickformat=axis_title_income_format,
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            xaxis_title=f"{sources['economy']}",
            xaxis=dict(
                range=layout_economy['range'],
                tickmode='array',
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            showlegend=True,
            template=get_color_template(dark_mode),
            paper_bgcolor=get_background_color_plotly(dark_mode),
            # dragmode=False,  # ← This disables drag interactions
        )

        for trace in fig['data']:
            if ('min' in trace['name']) | ('NONE' in trace['name']):
                trace['showlegend'] = False
        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']
        return fig

    @output
    @render_widget
    def plot_economy_barchart_income_countries():

        income_level=income_levels[input.income_level()]
        group_name = group_names[income_level]
        dark_mode=input.dark_mode()

        income_latest = (
            shares_wid
            .filter(pl.col('year') == shares_wid['year'].max())
            .sort([income_level,], descending=[False,])
        )
        countries = income_latest.select('country').to_numpy().flatten()
        colors = [colors_by_country[country] for country in countries]

        texttemplate = {
            'income_mean_bottom': "<b>%{text:.2s}</b>",
            'income_mean_upper': "<b>%{text:.3s}</b>",
            'income_mean_top': "<b>%{text:.3s}</b>",
        }

        fig = go.Figure(data=[
            go.Bar(
                x=income_latest['country'],
                y=income_latest[income_level],
                text=income_latest[income_level],
                texttemplate=texttemplate[income_level],
                textfont=dict(
                    size=12,
                ),
                textangle=0,
                marker_color=colors,
            )
        ])

        fig.update_layout(
            title=dict(
                text=f"<b>{input.income_level()} Comparison</b><br><sup>Each country's share & U.S. 2023 income</sup>",
            ),
            title_x=0.5,
            yaxis_title=axis_title_income,
            yaxis=dict(
                # range=[0, 3000000],
                tickprefix="$",
                tickformat=axis_title_income_format,
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            xaxis_title=f"{sources['economy']}",
            xaxis_tickangle=-45,
            xaxis=dict(
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            showlegend=False,
            template=get_color_template(dark_mode),
            paper_bgcolor=get_background_color_plotly(dark_mode),
        )

        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']
        return fig

    @output
    @render_widget
    def plot_economy_timeseries_income_policies():
        """
        Source: https://wid.world/country/usa/
        Share of total,
        Pre-tax national income Bottom 50% share
        Pre-tax national income Top 1% share
        :return:
        """
        income_level = income_levels[input.income_level()]
        group_name = group_names[income_level]
        dark_mode=input.dark_mode()
        # "bottom_50"
        # "top_1"
        usa = shares_wid.filter(pl.col('country') == 'usa').filter(pl.col('year') >= 1880)
        dem = (
            shares_wid
            .filter(pl.col('country').is_in([
                'canada',
                'germany',
                'italy',
                'japan',
                'new_zealand',
                'norway',
                'uk',
            ]))
        )
        auth = (
            shares_wid
            .filter(pl.col('country').is_in(['russia', 'china']))
        )

        fig = go.Figure(data=(
            [
                go.Scatter(
                    name='NONE',
                    x=usa['year'],
                    y=usa[income_level],
                    line=dict(color=color_light_dark[dark_mode], width=3),
                    text=f"<b>U.S.</b>",
                ),
            ] + get_highlights_line_min_max(
                data=usa,
                col_date='year',
                col_metric=income_level,
                number_type='thousands',
                max_or_min='max',
            )
        ))

        plot_period_dashed_line(fig)
        plot_period_shading(fig=fig)


        fig.update_layout(
            title=dict(
                text=f"<b>Taxes Impact on {input.income_level()} Income</b><br><sup>{year_max} dollars</sup>",
                #
            ),
            title_x=0.5,
            yaxis_title=axis_title_income,
            yaxis=dict(
                # range=[0, 3000000],
                tickprefix="$",
                tickformat=axis_title_income_format,
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            xaxis_title=f"{sources['economy']}",
            xaxis=dict(
                range=layout_economy['range'],
                tickmode='array',
                fixedrange=config['fixedrange'],  # This prevents zooming
                # tickvals=layout_economy['tickvals'],
                # ticktext=layout_economy['ticktext'],
            ),
            showlegend=True,
            template=get_color_template(dark_mode),
            paper_bgcolor=get_background_color_plotly(dark_mode),
        )

        for trace in fig['data']:
            if ('min' in trace['name']) | ('NONE' in trace['name']):
                trace['showlegend'] = False

        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']
        return fig

    @output
    @render_widget
    def plot_economy_timeseries_income_taxes():
        """
        Source: https://wid.world/country/usa/
        Share of total,
        Pre-tax national income Bottom 50% share
        Pre-tax national income Top 1% share
        :return:
        """
        # "bottom_50"
        # "top_1"
        income_level = income_levels[input.income_level()]
        group_name = group_names[income_level]
        usa = shares_wid.filter(pl.col('country') == 'usa').filter(pl.col('year') > 1880)
        dark_mode=input.dark_mode()

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_traces(
            [
                go.Scatter(
                    name='NONE',
                    x=usa['year'],
                    y=usa[income_level],
                    line=dict(color=color_light_dark[dark_mode], width=3),
                    text="<b>U.S.</b>",
                ),
            ] + get_highlights_line_min_max(
                data=usa,
                col_date='year',
                col_metric=income_level,
                number_type='thousands',
                max_or_min='max',
            )
        )

        # ---------------------------------------------------
        # tax changes
        data = tax.filter(pl.col('change_top_bracket') != 0).sort(['year'])
        changes = data['change_top_bracket'].to_list()
        years = data['year'].to_list()
        indices = dict(
            up=0,
            down=0,
        )
        names = dict(
            up='tax rate increase',
            down='tax rate decrease',
        )
        y_adjustment = dict(
            up=0.02,
            down=-0.02,
        )

        for year, change in zip(years, changes):
            # logic for displaying a trace name once depending on direction of change
            change_direction = 'up' if change > 0 else 'down'
            idx = indices[change_direction]
            multiplier = 1 if idx % 2 == 0 else 2
            name = names[change_direction] if idx == 0 else 'NONE'
            indices[change_direction] = indices[change_direction] + 1

            # change_amount_clipped = change_amount if change_amount <= 0.25 else 0.25
            fig.add_trace(go.Scatter(
                name=name,
                mode="lines",
                x=[year, year], y=[0, change],
                line=dict(color=colors_tax_changes[change_direction], width=5),
                yaxis='y2',
            ))

        fig.add_hline(
            y=0,
            line=dict(color='rgba(0,0,0,0.2)', width=1, dash='solid', ),
            secondary_y=True,
        )

        plot_period_dashed_line(fig=fig)
        plot_period_shading(fig=fig)

        yaxis_min, yaxis_max = get_yaxis_range(y_data=usa[income_level])
        fig.update_layout(
            title=dict(
                text=f"<b>Taxes on Top 1%</b><br><sup>{year_max} dollars</sup>",
            ),
            title_x=0.5,
            yaxis_title=axis_title_income,
            yaxis=dict(
                range=[yaxis_min, yaxis_max],
                tickprefix="$",
                tickformat=axis_title_income_format,
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            yaxis2=dict(
                title='top tax bracket changes',
                range=[-0.60, 0.60],
                anchor='x',
                overlaying='y',
                side='right',
                tickformat='+.0%',
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            xaxis_title=f"{sources['economy']}",
            xaxis=dict(
                range=layout_economy['range'],
                tickmode='array',
                fixedrange=config['fixedrange'],  # This prevents zooming
                # tickvals=layout_economy['tickvals'],
                # ticktext=layout_economy['ticktext'],
            ),
            showlegend=True,
            template=get_color_template(dark_mode),
            paper_bgcolor=get_background_color_plotly(dark_mode),
            legend=dict(
                x=0.01,  # x position (0 = left, 1 = right)
                y=0.99,  # y position (0 = bottom, 1 = top)
                xanchor='left',  # anchor point x position ('left', 'center', 'right')
                yanchor='top',  # anchor point y position ('top', 'middle', 'bottom')
            )
        )

        for trace in fig['data']:
            if ('NONE' in trace['name']):
                trace['showlegend'] = False

        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']
        return fig

    @output
    @render_widget
    def plot_economy_f150():
        """
        Source: claude.ai compiling of prices

        :return:
        """
        income_level = income_levels[input.income_level()]
        usa = (
            shares_wid.filter(pl.col('country') == 'usa')
            .filter(pl.col('year') >= 1880)
        )
        dark_mode=input.dark_mode()
        data = (
            f150
            .join(
                other=usa,
                on=['year'],
                how='inner',
            )
            .with_columns(
                price_ratio = pl.col('price')/pl.col(income_level)
            )
        )

        fig = go.Figure(data=(
            [
                go.Scatter(
                    name='NONE',
                    x=data['year'],
                    y=data['price_ratio'],
                    line=dict(color=color_light_dark[dark_mode], width=3),
                    text=f"<b>U.S.</b>",
                ),
            ] + get_highlights_line_min_max(
            data=data,
            col_date='year',
            col_metric='price_ratio',
            number_type='percentage',
            max_or_min='min',
        )
        ))

        plot_period_dashed_line(fig=fig)
        plot_period_shading(fig=fig)

        yaxis_min, yaxis_max = get_yaxis_range(y_data=data['price_ratio'])
        fig.update_layout(
            title=dict(
                text=f"<b>Ford F-150 Price</b>",
            ),
            title_x=0.5,
            yaxis_title=f"<b>% of {input.income_level()} Paycheck</b>",
            yaxis=dict(
                range=[yaxis_min, yaxis_max],
                # tickprefix="$",
                tickformat=',.0%',
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            xaxis_title=f"{sources['economy_f150']}",
            xaxis=dict(
                # range=layout_economy['range'],
                range=[data['year'].min() - 4, data['year'].max() + 4],
                tickmode='array',
                fixedrange=config['fixedrange'],  # This prevents zooming
                # tickvals=layout_economy['tickvals'],
                # ticktext=layout_economy['ticktext'],
            ),
            showlegend=True,
            template=get_color_template(dark_mode),
            paper_bgcolor=get_background_color_plotly(dark_mode),
        )

        for trace in fig['data']:
            if ('min' in trace['name']) | ('NONE' in trace['name']):
                trace['showlegend'] = False

        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']
        return fig

    # @output
    # @render_widget
    # def plot_american_dream_kids():
    #
    #     fig = go.Figure(
    #         data=[
    #             go.Scatter(
    #                 name=f"United States",
    #                 mode='lines',
    #                 x=american_dream_kids['cohort_work_year'],
    #                 y=american_dream_kids['probability'],
    #                 line=dict(color=color_light_dark[input.dark_mode()], width=3),
    #             )
    #         ] + get_highlights_line_min_max(
    #             data=american_dream_kids,
    #             col_date='cohort_work_year',
    #             col_metric='probability',
    #             number_type='percentage',
    #             max_or_min='max',
    #         )
    #     )
    #
    #     plot_period_dashed_line(fig=fig)
    #     plot_period_shading(fig=fig)
    #
    #     yaxis_min, yaxis_max = get_yaxis_range(y_data=american_dream_kids['probability'])
    #     fig.update_layout(
    #         title=dict(
    #             text=f"<b>Upward Mobility</b>",
    #         ),
    #         title_x=0.5,
    #         yaxis_title=f"% of 30 year olds that earn more than parents",
    #         xaxis_title=f"{sources['american_dream']}",
    #         xaxis=dict(
    #             fixedrange=config['fixedrange'],  # This prevents zooming
    #             range=[american_dream_kids['cohort_work_year'].min() - 4, american_dream_kids['cohort_work_year'].max() + 4],
    #         ),
    #         yaxis=dict(
    #             range=[yaxis_min, yaxis_max],
    #             tickformat='.0%',
    #             fixedrange=config['fixedrange'],  # This prevents zooming
    #         ),
    #         showlegend=False,
    #         template=get_color_template(input.dark_mode()),
    #         paper_bgcolor=get_background_color_plotly(input.dark_mode()),
    #     )
    #
    #     for trace in fig['data']:
    #         if 'NONE' in trace['name']:
    #             trace['showlegend'] = False
    #
    #     fig = go.FigureWidget(fig)
    #     fig._config = fig._config | config['plotly_mobile']
    #     return fig

    @output
    @render_widget
    def plot_american_dream_kids():
        col = 'mobility'
        data = (
            mobility_international
            .filter(pl.col(col).is_not_nan())
            .filter(pl.col('country').is_in(config['countries']))
        )
        last = (
            data
            .join(
                other=(
                    data
                    .group_by('country')
                    .agg(
                        pl.max('year')
                    )
                ),
                on=['country', 'year'],
                how='inner',
            )
        )
        countries = np.sort(np.unique(data['country'].to_numpy().flatten()))
        dark_mode = input.dark_mode()

        fig = go.Figure(
            data=(
                    [
                        go.Scatter(
                            name=f"{country}",
                            mode='lines',
                            x=data.filter(pl.col('country') == country)['year'],
                            y=data.filter(pl.col('country') == country)[col],
                            line=(
                                dict(
                                    color=color_light_dark[dark_mode],
                                    width=3)
                                if country.lower() == 'united states'
                                else dict(
                                    color="rgba(0,0,0,0.2)",
                                    width=2,
                                )
                            ),
                        ) for country in countries
                    ] + get_highlights_line_min_max(
                data=data.filter(pl.col('country') == 'United States'),
                col_date='year',
                col_metric=col,
                number_type='percentage',
                max_or_min='max',
            )
                    + [
                        go.Scatter(
                            name="NONE",
                            mode='text',
                            x=last.filter(pl.col('country') == country)['year'],
                            y=last.filter(pl.col('country') == country)[col],
                            text=f"<b>{country.title()}</b>" if country == 'United States' else f"{country.title()}",
                            textposition='middle right',
                        ) for country in  ["United States", "Europe",]
                    ]
            )
        )

        plot_period_dashed_line(fig=fig)
        plot_period_shading(fig=fig)

        yaxis_min, yaxis_max = get_yaxis_range(y_data=data[col])
        fig.update_layout(
            title=dict(
                text=f"<b>Upward Mobility</b><br><sup>Kids doing better than parents</sup>",
            ),
            title_x=0.5,
            yaxis_title=f"% of 30 year olds that earn more than parents",
            xaxis_title=f"{sources['american_dream']}",
            xaxis=dict(
                fixedrange=config['fixedrange'],  # This prevents zooming
                range=[data['year'].min() - 4, data['year'].max() + 15],
            ),
            yaxis=dict(
                range=[yaxis_min, yaxis_max],
                tickformat='.0%',
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            showlegend=False,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        for trace in fig['data']:
            if 'NONE' in trace['name']:
                trace['showlegend'] = False

        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']
        return fig

    @output
    @render_widget
    def plot_american_dream_mobility_international():
        col = 'growth_controlled'

        data = (
            mobility_international
            .filter(pl.col(col).is_not_nan())
            .filter(pl.col('country').is_in(config['countries']))
        )
        last = (
            data
            .join(
                other=(
                    data
                    .group_by('country')
                    .agg(
                        pl.max('year')
                    )
                ),
                on=['country', 'year'],
                how='inner',
            )
        )
        countries = np.sort(np.unique(data['country'].to_numpy().flatten()))
        dark_mode = input.dark_mode()


        fig = go.Figure(
            data=(
                [
                    go.Scatter(
                        name=f"{country}",
                        mode='lines',
                        x=data.filter(pl.col('country') == country)['year'],
                        y=data.filter(pl.col('country') == country)[col],
                        line=(
                            dict(
                                color=color_light_dark[dark_mode],
                                width=3)
                            if country.lower() == 'united states'
                            else dict(
                                color="rgba(0,0,0,0.2)",
                                width=2,
                            )
                        ),
                    ) for country in countries
                ] + get_highlights_line_min_max(
                data=data.filter(pl.col('country')=='United States'),
                col_date='year',
                col_metric=col,
                number_type='percentage',
                max_or_min='max',
            )
            + [
                go.Scatter(
                    name="NONE",
                    mode='text',
                    x=last.filter(pl.col('country') == country)['year'],
                    y=last.filter(pl.col('country') == country)[col],
                    text=f"<b>{country.title()}</b>" if country == 'United States' else f"{country.title()}",
                    textposition='middle right',
                ) for country in config['countries'] # ["United States", "Norway", "Sweden", "France", "Australia"]
            ]
            )
        )

        plot_period_dashed_line(fig=fig)
        plot_period_shading(fig=fig)

        yaxis_min, yaxis_max = get_yaxis_range(y_data=data[col])
        fig.update_layout(
            title=dict(
                text=f"<b>Upward Mobility Breakdown</b><br><sup>Fixed income growth, impact of Top 1% taking more</sup>",
            ),
            title_x=0.5,
            yaxis_title=f"% of 30 year olds that earn more than parents",
            xaxis_title=f"{sources['american_dream']}",
            xaxis=dict(
                fixedrange=config['fixedrange'],  # This prevents zooming
                range=[data['year'].min()-4, data['year'].max()+15],
            ),
            yaxis=dict(
                range=[yaxis_min, yaxis_max],
                tickformat='.0%',
                fixedrange=config['fixedrange'],  # This prevents zooming
            ),
            showlegend=False,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        for trace in fig['data']:
            if 'NONE' in trace['name']:
                trace['showlegend'] = False

        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']
        return fig

    @output
    @render_widget
    def plot_black_upward_mobility():
        metric = 'upward_mobility'
        fig = plot_county_heatmap(
            data=outcomes_upward_mobility_jail,
            counties_json=counties_json,
            race='black',
            metric=metric,
            title=f"Black Male Upward Mobility<br>(parents in bottom 25th of income)",
            colorscale=config['colorscale'][metric],
            dark_mode=input.dark_mode(),
            )
        return fig

    @output
    @render_widget
    def plot_white_upward_mobility():
        metric = 'upward_mobility'
        fig = plot_county_heatmap(
            data=outcomes_upward_mobility_jail,
            counties_json=counties_json,
            race='white',
            metric=metric,
            title=f"White Male Upward Mobility<br>(parents in bottom 25th of income)",
            colorscale=config['colorscale'][metric],
            dark_mode=input.dark_mode(),
            )
        return fig

    @output
    @render_widget
    def plot_black_jail():
        metric = 'jail'
        fig = plot_county_heatmap(
            data=outcomes_upward_mobility_jail,
            counties_json=counties_json,
            race='black',
            metric=metric,
            title=f"Black Male Jail Rate<br>(parents in bottom 25th of income)",
            colorscale=config['colorscale'][metric],
            dark_mode=input.dark_mode(),
        )
        return fig

    @output
    @render_widget
    def plot_white_jail():
        metric = 'jail'
        fig = plot_county_heatmap(
            data=outcomes_upward_mobility_jail,
            counties_json=counties_json,
            race='white',
            metric=metric,
            title=f"White Male Jail Rate<br>(parents in bottom 25th of income)",
            colorscale=config['colorscale'][metric],
            dark_mode=input.dark_mode(),
        )
        return fig

    @output
    @render_widget
    def plot_healthcare_cost_per_capita():
        fig = plot_timeseries_multiple_countries(
            data=healthcare_cost_per_capita,
            title="Healthcare Cost per Person",
            yaxis_title='U.S. $',
            xaxis_title=f"{sources['healthcare']}",
            dark_mode=input.dark_mode(),
        )

        return fig

    @output
    @render_widget
    def plot_healthcare_life_expectancy():
        fig = plot_timeseries_multiple_countries(
            data=healthcare_life_expectancy,
            title="Life Expectancy",
            yaxis_title="years",
            dark_mode=input.dark_mode(),
            xaxis_title=f"{sources['healthcare']}",
        )
        return fig

    @output
    @render_widget
    def plot_healthcare_infant_mortality():
        fig = plot_timeseries_multiple_countries(
            data=healthcare_infant_mortality,
            title="Infant Mortality",
            yaxis_title="deaths per 1,000 babies",
            dark_mode=input.dark_mode(),
            xaxis_title=f"{sources['healthcare']}",
        )
        return fig

    @output
    @render_widget
    def plot_healthcare_maternal_mortality():
        fig = plot_timeseries_multiple_countries(
            data=healthcare_maternal_mortality,
            title="Mother Mortality",
            yaxis_title="deaths per 100,000 births",
            dark_mode=input.dark_mode(),
            xaxis_title=f"{sources['healthcare']}",
        )
        return fig



    @output
    @render_widget
    def plot_healthcare_suicide():
        fig = plot_timeseries_multiple_countries(
            data=healthcare_suicide,
            title="Suicide Rates",
            yaxis_title="deaths per 100,000",
            dark_mode=input.dark_mode(),
            xaxis_title=f"{sources['healthcare']}",
        )
        return fig

    @output
    @render_widget
    def plot_electricity_cost():
        colors = {
            "Renewable Energy": "rgb(60, 179, 113, 0.9)",
            "Conventional Energy": "rgb(139, 129, 130, 0.9)",
        }
        counts = {
            "Renewable Energy": 0,
            "Conventional Energy": 0,
        }

        # Create the figure
        fig = go.Figure()

        # Add renewable energy technologies
        for technology in electricity_cost.select(["Technology"]).to_numpy().flatten():
            row = (
                electricity_cost
                .filter(pl.col('Technology') == technology)
            )
            category = row['Category'].to_numpy()[0]
            counts[category] += 1
            fig.add_trace(go.Scatter(
                x=[row['LCOE_Low_USD_MWh'].to_numpy().flatten()[0], row['LCOE_High_USD_MWh'].to_numpy().flatten()[0]],
                y=[row['Technology'].to_numpy().flatten()[0], row['Technology'].to_numpy().flatten()[0]],
                mode='lines+markers',
                line=dict(color=colors[category], width=6),
                marker=dict(size=8, color=colors[category]),
                name=category if counts[category] <= 1 else '',
                showlegend=True if counts[category] <= 1 else False,
                hovertemplate=f"<b>{row['Technology']}</b><br>" +
                              f"LCOE Range: ${row['LCOE_Low_USD_MWh']}-${row['LCOE_High_USD_MWh']}/MWh<br>" +
                              f"<extra></extra>"
            ))

        # Update layout
        fig.update_layout(
            title={
                'text': "Cost of Electricity<br><sub>Ranges by Source</sub>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis=dict(
                title='$ / megawatt hour',
                showgrid=True,
                gridcolor='lightgray',
                range=[0, 300]
            ),
            yaxis=dict(
                title='Technology',
                showgrid=True,
                gridcolor='lightgray',
                categoryorder='array',
                categoryarray=list(electricity_cost['Technology'].to_numpy().flatten()),
            ),
            # width=1000,
            # height=800,
            plot_bgcolor='white',
            legend=dict(
                x=0.7,
                y=0.98,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='gray',
                borderwidth=1
            ),
            # annotations=[
            #     dict(
            #         text="Source: Lazard and Roland Berger estimates and publicly available information",
            #         xref="paper", yref="paper",
            #         x=0.5, y=-0.12,
            #         showarrow=False,
            #         font=dict(size=10, color="gray"),
            #         xanchor="center"
            #     )
            # ],
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        # fig.update_layout(
        #     title=dict(
        #         text=f"<b>Upward Mobility Breakdown</b><br><sup>Fixed income growth, impact of Top 1% taking more</sup>",
        #     ),
        #     title_x=0.5,
        #     yaxis_title=f"% of 30 year olds that earn more than parents",
        #     xaxis_title=f"{sources['american_dream']}",
        #     xaxis=dict(
        #         fixedrange=config['fixedrange'],  # This prevents zooming
        #         range=[data['year'].min()-4, data['year'].max()+15],
        #     ),
        #     yaxis=dict(
        #         range=[yaxis_min, yaxis_max],
        #         tickformat='.0%',
        #         fixedrange=config['fixedrange'],  # This prevents zooming
        #     ),
            # showlegend=False,
        # )
        #
        # for trace in fig['data']:
        #     if 'NONE' in trace['name']:
        #         trace['showlegend'] = False

        fig = go.FigureWidget(fig)
        fig._config = fig._config | config['plotly_mobile']

        return fig



    @render.image
    def img_freedom_scale():
        img = {
            "src": str(Path(__file__).parent / "static/images/freedom_scale.png"),
            "width": "70%",
        }
        return img

    @render.image
    def img_1619():
        img = {
            "src": str(Path(__file__).parent / "static/images/1619.jpg"),
            "width": "15%",
        }
        return img

    @render.image
    def img_american_character():
        img = {
            "src": str(Path(__file__).parent / "static/images/american_character.jpg"),
            "width": "15%",
        }
        return img


static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets=static_dir)