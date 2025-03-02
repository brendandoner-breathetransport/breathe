from shiny import App, reactive, ui, render
from shinywidgets import output_widget, render_widget
import numpy as np
import pandas as pd
import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from htmltools import HTML, div


def read_data(file_name):
    data = pl.from_pandas(pd.read_csv(
        str(Path(__file__).parent / f"data/{file_name}.csv"), delimiter=","
    ))
    return data

n_workers_full_time = read_data(file_name='n_workers_full_time')
shares_wid = read_data(file_name="shares_wid")
shares_wid_full_distribution = read_data(file_name="shares_wid_full_distribution")
shares_data = shares_wid
year_max = shares_data.select(pl.max('year')).to_numpy().flatten()[0]
tax = read_data(file_name="tax")
income_total = read_data(file_name="income_total")
population = read_data(file_name="population")
workers_ratio = read_data(file_name="workers_ratio")

axis_title_income = "<b>income</b>/yr average"
axis_title_income_format = ',.2s'

income_levels = {
    "Main Street": "income_mean_bottom",
    "Mega Rich": "income_mean_top",
    "Gap": 'income_mean_gap',
}
group_names = {
    "income_mean_bottom": "Main Street",
    'income_mean_top': "Mega Rich",
    "income_mean_gap": "Gap (Mega Rich - Main Street)",
}

def get_source(name, link):
    return f"<br><sup><a href='{link}'>{name}</a></sup>"

sources = {
    'money': get_source(name='Sources', link='https://github.com/brendandoner-breathetransport/breathe/wiki/Money'),
    'wid': get_source(name='Source: World Inequality Database', link='https://wid.world/wid-world/'),
    'irs': get_source(name='Source: Internal Revenue Service', link='https://www.irs.gov/statistics/soi-tax-stats-historical-table-23'),
    '1619': get_source(name='Source: The 1619 Project', link='https://www.nytimes.com/interactive/2019/08/14/magazine/1619-america-slavery.html'),
    'american_character': get_source(name='Source: American Character', link='https://colinwoodard.com/books/american-character/'),
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
# colors_by_country = {
#     'canada':'rgba(117, 184, 116,   0.3)',
#     'germany':'rgba(110, 167,  96,   0.3)',
#     'italy':'rgba(108, 178,  88,   0.3)',
#     'japan':'rgba( 90, 185, 111,   0.3)',
#     'new_zealand':'rgba(103, 188,  96,   0.3)',
#     'norway':'rgba(117, 199,  95,   0.3)',
#     'uk':'rgba(111, 174,  96,   0.3)',
#     'russia':'rgba(220, 88,  57,   0.7)',
#     'china':'rgba(230, 78, 67,    0.7)',
#     'usa':'rgba(0, 0,  0,   0.7)'
# }
colors_by_country = {
    'canada':'rgba( 90, 185, 111,   0.3)',
    'germany':'rgba( 90, 185, 111,   0.3)',
    'italy':'rgba( 90, 185, 111,   0.3)',
    'japan':'rgba( 90, 185, 111,   0.3)',
    'new_zealand':'rgba( 90, 185, 111,   0.3)',
    'norway':'rgba( 90, 185, 111,   0.3)',
    'uk':'rgba( 90, 185, 111,   0.3)',
    'russia':'rgba(230, 78, 67,    0.7)',
    'china':'rgba(230, 78, 67,    0.7)',
    'usa':'rgba(0, 0,  0,   0.7)'
}
colors_tax_changes = {
    'up': 'rgba( 90, 185, 111,   0.3)',
    'down': 'rgba(230, 78, 67,    0.7)',
}

color_light_dark = {
    'light': 'rgba(0,0,0,0.5)',
    'dark': 'rgba(255,255,255,0.5)',
}


def read_data():
    df = pd.read_csv(
        Path(__file__).parent / "data/anonymized_cb_data.csv", delimiter=";"
    )
    df["cohort"] = df["cohort"].astype(str)
    return df


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

def get_period_shading(fig):
    fig.add_vrect(
        x0=1880,
        x1=1902,
        line_width=0,
        fillcolor='black',
        opacity=0.05,
        annotation_text='<b>Guilded Age</b>',
        annotation_position='bottom left',
    )
    fig.add_vrect(
        x0=1940,
        x1=1945,
        line_width=0,
        fillcolor='black',
        opacity=0.05,
        annotation_text='<b>WWII</b>',
        annotation_position='bottom left',
    )
    fig.add_vrect(
        x0=1980,
        x1=1988,
        line_width=0,
        fillcolor='black',
        opacity=0.05,
        annotation_text='<b>Trickle Down</b>',
        annotation_position='bottom left',
    )
    # fig.add_vrect(
    #     x0=2016.5,
    #     x1=2018,
    #     line_width=0,
    #     fillcolor='black',
    #     opacity=0.05,
    #     annotation_text='<b>2017 Tax Cut</b>',
    #     annotation_position='bottom left',
    # )

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

app_ui = ui.page_fillable(
    ui.page_navbar(
        ui.nav_panel(
            "Money",
            ui.row(ui.h1(ui.span(HTML("Why are Americans struggling?"), style="color:rgba(255,255,255,0.9)"))),
            # Income
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_barchart_income_usa")),
                    ui.card(output_widget("plot_barchart_income_countries")),
                    col_widths=(6, 6,),
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.input_radio_buttons(
                        id='income_level',
                        label=None,
                        # choices=['Main Street', "Mega Rich", "Gap"],
                        choices={
                            "Main Street": ui.span("Main Street", style=f"color:rgba(255,255,255,0.6)"),
                            "Mega Rich": ui.span("Mega Rich", style=f"color:rgba(255,255,255,0.6)"),
                            "Gap": ui.span("Gap", style=f"color:rgba(255,255,255,0.6)"),
                        },
                        selected="Main Street",
                        inline=True,
                    ),
                    col_widths=(12,),
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.card(output_widget("plot_timeseries_income_countries")),
                    ui.card(output_widget("plot_timeseries_income_taxes")),
                    col_widths=(6, 6,),
                )
            ),
            # Cost of Living
            ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
            ui.row(ui.h2(ui.span("Food & Shelter", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(ui.h3(ui.span("income vs rent/mortgage", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("income vs energy(gas, mileage, utilities, i.e. ENERGY)",
                                          style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(6, 6),
                )
            ),
            ui.row(
                ui.layout_columns(
                    ui.card(ui.h3(ui.span("income vs childcare", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("income vs cost of living", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("income vs college/trade school", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(4, 4, 4),
                )
            ),
        ),
        ui.nav_panel(
            "Fairness",
            # education, sick care, justice, laws/rules,
            ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(ui.h3(
                        ui.span("incarceration rate (by race, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("likelihood rates for education levels (race, time) vs countries",
                                          style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("loan approval rates (race, time)", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(4, 4, 4),
                )
            ),
            ui.row(ui.h2(ui.span("Justice", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(ui.h3(ui.span("stop and frisk rates (by race, by state)", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("immigration (crime rate, race, time) vs benchmarks & countries", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("crime (by state, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(4, 4, 4),
                )
            ),
        ),
        ui.nav_panel(
            "Health",
            # [live healthy, sick care]
            ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(ui.h3(ui.span("life expectancy vs countries", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("sport performance metric vs countries", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("birth survival rate vs countries", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(4, 4, 4),
                )
            ),

        ),
        ui.nav_panel(
            "Pollution",
            # Air & Water
            ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(ui.h3(ui.span("air (standards, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("water (standards, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("soil (standards, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(4, 4, 4),
                )
            ),
        ),

        ui.nav_panel(
            "Spotlight",
            # education, sick care, justice, laws/rules,
            ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
            ui.row(ui.h6(ui.span("Replace below with data driven plots...", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.output_image("img_freedom_scale")
            ),
            ui.row(ui.h1(ui.span("Disruptions", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(ui.h3(ui.span("Climate Change", style="color:rgba(0,0,0,0.9)"))),
                    ui.card(ui.h3(ui.span("AI",
                                          style="color:rgba(0,0,0,0.9)"))),
                    # ui.card(ui.h3(ui.span("crime (by state, time) vs countries", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(6, 6,),
                )
            ),
            ui.row(ui.h1(ui.span("Wants", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(
                        ui.h3(ui.span("regional cultures and government preferences", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(12,),
                )
            ),
            ui.row(ui.h1(ui.span("Voter supression", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.card(
                        ui.h3(ui.span("Voter turn out vs laws that restrict voting", style="color:rgba(0,0,0,0.9)"))),
                    col_widths=(12,),
                )
            ),
        ),
        ui.nav_panel(
            "About Us",
            # [live healthy, sick care]
            ui.row(ui.h1(ui.span("Under construction...", style="color:rgba(255,255,255,0.9)"))),
            ui.row(ui.h2(ui.span("Purpose", style="color:rgba(255,255,255,0.9)"))),
            ui.row(ui.h2(ui.span("Values", style="color:rgba(255,255,255,0.9)"))),
            ui.row(ui.h2(ui.span("Vision", style="color:rgba(255,255,255,0.9)"))),
            ui.row(ui.h1(ui.span("Books", style="color:rgba(255,255,255,0.9)"))),
            ui.row(
                ui.layout_columns(
                    ui.tags.a(
                        ui.output_image("img_american_character"),
                        href='https://colinwoodard.com/books/american-character/',
                        target="_blank"
                    ),
                    ui.tags.a(
                        ui.output_image("img_1619"),
                        href='https://www.nytimes.com/interactive/2019/08/14/magazine/1619-america-slavery.html',
                        target="_blank"
                    ),
                    col_widths=(6,6,),
                )
            ),
        ),
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
            /* Background image */
            background-image: url("images/background_dark_full.jpg");
            height: 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }
        div#map_full.html-fill-container {
            height: -webkit-fill-available !important;
            min-height: 850px !important;
            max-height: 2000px !important;
        }
        div#main_panel.html-fill-container {
            height: -webkit-fill-available !important;
        }
        """
    ),
    ui.head_content(div(HTML("<link rel='icon' href='images/browser.png'>"))),
    icon="images/browser.png",
)


def server(input, output, session):
    @output
    @render_widget
    def plot_barchart_income_usa():
        """
        ['country','year','bottom_50','top_1','gap','income_mean_bottom','income_mean_top','multiple']
        """

        cols = [
            'income_mean_bottom',
            # 'income_mean_upper',
            'income_mean_top',
        ]
        # cols = ['share_bottom', 'share_upper', 'share_top',]
        data = (
            shares_data
            .filter(pl.col('country') == 'usa')
            .filter(pl.col('year') == year_max)
            .select([
                'country', 'year',
                'income_mean_bottom', 'income_mean_upper', 'income_mean_top',
            ])
            .unpivot(
                index=['country', 'year', ],
                on=cols,
                variable_name='group',
                value_name='value',
            )
            .with_columns(
                bin_bottom=pl.sql_expr(f"""
                    CASE
                        WHEN group='{[col for col in cols if 'bottom' in col][0]}' THEN 0
                        
                        WHEN group='{[col for col in cols if 'top' in col][0]}' THEN 99
                        ELSE NULL
                    END
                """), # WHEN group='{[col for col in cols if 'upper' in col][0]}' THEN 51
                bin_top=pl.sql_expr(f"""
                    CASE 
                        WHEN group='{[col for col in cols if 'bottom' in col][0]}' THEN 50

                        WHEN group='{[col for col in cols if 'top' in col][0]}' THEN 100
                        ELSE NULL
                    END
                """), # WHEN group='{[col for col in cols if 'upper' in col][0]}' THEN 98
            )
            .filter(pl.col('group').is_in(cols))
            .sort(['bin_bottom'])
        )

        income_mean_bottom = get_income_mean(group="income_mean_bottom", data=data)
        # income_mean_upper = get_income_mean(group="income_mean_upper", data=data)
        income_mean_top = get_income_mean(group="income_mean_top", data=data)

        #------------------------------------------------------------------------------------------------
        fig = go.Figure(
        )
        for group in cols:
            fig.add_shape(
                type="rect",
                x0=data.filter(pl.col('group')==group).select('bin_bottom').to_numpy().flatten()[0],
                x1=data.filter(pl.col('group')==group).select('bin_top').to_numpy().flatten()[0],
                y0=0,
                y1=data.filter(pl.col('group')==group).select('value').to_numpy().flatten()[0],
                line=dict(
                    color=color_light_dark[input.dark_mode()],
                    width=1,
                ),
                fillcolor=color_light_dark[input.dark_mode()],
                opacity=1.0,
            )

        fig.add_traces([
            go.Scatter(
                # Text for bottom
                name='none',
                x=[25, ], y=[income_mean_bottom + 10000, ],
                mode='text',
                text=f"<b>${income_mean_bottom/1000:,.0f}k</b>/yr average<br>{n_workers_full_time.filter(pl.col('group')=='bottom_50')['n_workers_full_time'].to_numpy().flatten()[0]/1000000:,.0f}M Americans",
                textposition="top center",
                textfont=dict(size=16),
            ),
            go.Scatter(
                # Text for top
                name='none',
                x=[100, ], y=[income_mean_top + 10000, ],
                mode='text',
                text=f"<b>${income_mean_top/1000000:,.1f}M</b>/yr average<br>{n_workers_full_time.filter(pl.col('group')=='top_1')['n_workers_full_time'].to_numpy().flatten()[0]/1000000:,.0f}M Americans",
                textposition="top center",
                textfont=dict(size=16),
            ),
        ])

        fig.update_layout(
            title=dict(
                text=f"<b>What is the income balance of main street vs the mega rich?</b><br><sup>U.S. Full-Time Income Data for {year_max}</sup>",
            ),
            title_x=0.5,
            xaxis_title=f"percent of population ranked by income{sources['money']}",
            xaxis=dict(
                range=[-10, 130],
                tickmode='array',
                tickvals=[25, 50, 75, 100],
                ticktext=['<b>main street</b><br>(bottom 50%)', '', '', '<b>mega rich</b><br>(richest 1%)'],
            ),
            yaxis_title=axis_title_income,
            yaxis=dict(
                range=[0, 3000000],
                tickprefix="$",
                tickformat=axis_title_income_format,
            ),
            showlegend=True,
            template=get_color_template('light'),
            paper_bgcolor=get_background_color_plotly('light'),
        )

        for trace in fig['data']:
            if 'none' in trace['name']:
                trace['showlegend'] = False

        return fig

    @output
    @render_widget
    def plot_barchart_income_countries():

        income_level=income_levels[input.income_level()]
        group_name = group_names[income_level]

        income_latest = (
            shares_data
            .filter(pl.col('year') == shares_data['year'].max())
            .sort([income_level,], descending=[True,])
        )
        countries = income_latest.select('country').to_numpy().flatten()
        colors = [colors_by_country[country] for country in countries]

        fig = go.Figure(data=[
            go.Bar(
                x=income_latest['country'],
                y=income_latest[income_level],
                text=income_latest[income_level],
                texttemplate='%{text:.2s}',
                marker_color=colors,
            )
        ])

        fig.update_layout(
            title=dict(
                text=f"<b>How does U.S. Main Street income compare to other countries?</b><br><sup>Based on {year_max} U.S. total income and each country's income share for the selected group</sup>",
            ),
            title_x=0.5,
            yaxis_title=axis_title_income + f"<br>{group_name}",
            yaxis=dict(
                # range=[0, 3000000],
                tickprefix="$",
                tickformat=axis_title_income_format,
            ),
            xaxis_title=f"{sources['money']}",
            xaxis_tickangle=-45,
            showlegend=False,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        return fig

    @output
    @render_widget
    def plot_scale():
        income_level='income_mean_bottom'

        income_latest = shares_data.filter(pl.col('year') == shares_data['year'].max())
        dem = (
            income_latest
            .filter(pl.col('country').is_in([
                'canada',
                'germany',
                'italy',
                'japan',
                'new_zealand',
                'norway',
                'uk',
            ]))
            .sort('country')
        )
        auth = (
            income_latest
            .filter(pl.col('country').is_in(['russia', 'china', 'usa']))
            .sort(income_level)
        )
        # countries_dem = np.sort(dem.select('country').unique().to_numpy().flatten()).tolist()
        # countries_auth = np.sort(auth.select('country').unique().to_numpy().flatten()).tolist()

        countries_dem = dem.select('country').to_numpy().flatten()
        countries_auth = auth.select('country').unique().to_numpy().flatten()

        fig = go.Figure(data=[
            go.Scatter(
                name='none',
                y=[70000, ], x=[0, ],
                marker=dict(
                    symbol='triangle-up',
                    size=15, 
                    color=color_light_dark[input.dark_mode()],
                ),
                mode='markers+text',
                text=["<b>power for main street</b>", ],
                textposition="bottom right",

            ),
            go.Scatter(
                name='none',
                y=[20000, ], x=[0, ],
                marker=dict(
                    symbol='triangle-down',
                    size=15, 
                    color=color_light_dark[input.dark_mode()],
                ),
                mode='markers+text',
                text=['<b>power for mega rich</b>'],
                textposition='bottom right',
            ),
        ])
        fig.add_shape(
            type='line',
            y0=20000, y1=70000, x0=0, x1=0,
            line=dict(
                color=color_light_dark[input.dark_mode()],
                width=5,
            ),
        )

        def _plot_countries(country_list, color_list):
            for idx, country in enumerate(country_list):
                income_mean = income_latest.filter(pl.col('country') == country)[income_level].to_numpy().flatten()[0]
                color = color_list[idx] if country != 'usa' else color_light_dark[input.dark_mode()]
                x = -0.2 if idx%2==0 else 0.2
                textposition = "bottom left" if idx%2==0 else "bottom right"

                fig.add_shape(
                    type='line',
                    y0=income_mean, y1=income_mean, x0=-0.2, x1=0.2,
                    line=dict(color=color, width=4)
                )
                fig.add_traces(data=[
                    go.Scatter(
                        # Text of gap
                        name='none',
                        x=[x, ], y=[income_mean, ],
                        mode='text',
                        text=f"<b>U.S.</b>" if 'usa' in country else country,
                        textposition=textposition,
                        textfont=dict(size=16),
                    ),
                ])
                # fig.add_annotation(
                #     y=income_mean, x=0.5 if idx%2==0 else -0.5,
                #     text=f"<b>U.S.</b>" if 'usa' in country else country,
                #     # textangle=330,
                #     showarrow=False,
                #     # ax=3 + (2) * (idx % 2),
                #     # ay=-10 + (-32) * (idx % 2),
                # )

        _plot_countries(country_list=countries_auth, color_list=colors_auth)
        _plot_countries(country_list=countries_dem, color_list=colors_dem)
        # fig.add_hline(
        #     y=0,
        #     line=dict(color='rgba(230, 78, 67, 0.7)', width=4, dash='dash', ),
        # )
        # fig.add_vrect(
        #     x0=0,
        #     x1=0.20,
        #     line_width=0,
        #     fillcolor='darkred',
        #     opacity=0.07,
        # )

        fig.update_layout(
            title=dict(
                text=f"<b>How does the U.S. income on Main Street compare to other countries?</b><br><sup>Income data for {shares_data.select(pl.max('year')).to_numpy().flatten()[0]}</sup>",
            ),
            title_x=0.5,
            yaxis_title=f"income/yr",
            xaxis_title=f"{sources['money']}",
            yaxis=dict(
                # tickformat=',.0%',
                # title_font_color="red",
                range=[15000, 75000],
            ),
            xaxis=dict(
                range=[-1, 1],
                tickmode='array',
                tickvals=[-0.2, 0, 0.2],
                ticktext=['', '', '',],
            ),
            showlegend=True,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        for trace in fig['data']:
            if ('none' in trace['name']) | ('min' in trace['name']):
                trace['showlegend'] = False

        return fig

    @output
    @render_widget
    def plot_timeseries_income_countries():
        """
        Source: https://wid.world/country/usa/
        Share of total,
        Pre-tax national income Bottom 50% share
        Pre-tax national income Top 1% share
        :return:
        """
        # todo: add selector for country comparison and dem/auth means
        income_level=income_levels[input.income_level()]
        group_name = group_names[income_level]
        # "bottom_50"
        # "top_1"
        usa = shares_data.filter(pl.col('country') == 'usa').filter(pl.col('year')>=1880)
        dem = (
            shares_data
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
            shares_data
            .filter(pl.col('country').is_in(['russia', 'china']))
        )
        countries_dem = np.sort(dem.select('country').unique().to_numpy().flatten()).tolist()
        countries_auth = np.sort(auth.select('country').unique().to_numpy().flatten()).tolist()

        fig = go.Figure(data=(
            [
                go.Scatter(
                    name='NONE',
                    x=usa['year'],
                    y=usa[income_level],
                    line=dict(color=color_light_dark[input.dark_mode()], width=3),
                    text=f"<b>U.S.</b>",
                ),
                go.Scatter(
                    name='NONE',
                    mode='markers+text',
                    x=usa.filter(pl.col(income_level)==usa[income_level].max())['year'],
                    y=usa.filter(pl.col(income_level)==usa[income_level].max())[income_level],
                    marker=dict(color='orange', size=10),
                    text=f"<b>${usa.filter(pl.col(income_level)==usa[income_level].max())[income_level].to_numpy().flatten()[0]/1000:.0f}k</b>",
                    textposition='top center',
                ),
                go.Scatter(
                    name='NONE',
                    mode='markers+text',
                    x=usa.filter(pl.col('year') == usa['year'].max())['year'],
                    y=usa.filter(pl.col('year') == usa['year'].max())[income_level],
                    marker=dict(color='orange', size=10),
                    text=f"<b>${usa.filter(pl.col('year') == usa['year'].max())[income_level].to_numpy().flatten()[0] / 1000:.0f}k</b>",
                    textposition='top center',
                ),
            ]
             # +
             # [
             #     go.Scatter(
             #         name=country,
             #         x=dem.filter(pl.col('country') == country)['year'],
             #         y=dem.filter(pl.col('country') == country)['gap'],
             #         line=dict(color=colors_dem[idx], width=2),
             #         text=f"<b>{country}</b>",
             #     ) for idx, country in enumerate(countries_dem)
             # ]
             # +
             # [
             #     go.Scatter(
             #         name=country,
             #         x=auth.filter(pl.col('country') == country)['year'],
             #         y=auth.filter(pl.col('country') == country)['gap'],
             #         line=dict(color=colors_auth[idx], width=2),
             #         text=f"<b>{country}</b>",
             #     ) for idx, country in enumerate(countries_auth)
             # ]
        ))
        
        get_period_shading(fig=fig)

        fig.update_layout(
            title=dict(
                text=f"<b>Where has income been in the past?</b><br><sup>Based on {year_max} dollars</sup>", #
            ),
            title_x=0.5,
            yaxis_title=axis_title_income + f"<br>{group_name}",
            yaxis=dict(
                # range=[0, 3000000],
                tickprefix="$",
                tickformat=axis_title_income_format,
            ),
            xaxis_title=f"{sources['money']}",
            xaxis=dict(
                range=[1880,2030],
                tickmode='array',
                tickvals=[1902, 1945, 1969, 1980, 2023, 2032],
                ticktext=[1902, 1945, 1969, 1980, 2023, ''],
            ),
            showlegend=True,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        for trace in fig['data']:
            if ('min' in trace['name']) | ('NONE' in trace['name']):
                trace['showlegend'] = False

        return fig

    @output
    @render_widget
    def plot_timeseries_income_taxes():
        """
        Source: https://wid.world/country/usa/
        Share of total,
        Pre-tax national income Bottom 50% share
        Pre-tax national income Top 1% share
        :return:
        """
        # "bottom_50"
        # "top_1"
        income_level=income_levels[input.income_level()]
        group_name = group_names[income_level]
        usa = shares_data.filter(pl.col('country') == 'usa').filter(pl.col('year')>1880)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_traces([
            go.Scatter(
                name='NONE',
                x=usa['year'],
                y=usa[income_level],
                line=dict(color=color_light_dark[input.dark_mode()], width=3),
                text="<b>U.S.</b>",
            ),
            # go.Scatter(
            #     name='NONE',
            #     mode='markers+text',
            #     x=usa.filter(pl.col(income_level) == usa[income_level].max())['year'],
            #     y=usa.filter(pl.col(income_level) == usa[income_level].max())[income_level],
            #     marker=dict(color='orange', size=8),
            #     text=f"<b>${usa.filter(pl.col(income_level) == usa[income_level].max())[income_level].to_numpy().flatten()[0] / 1000:.0f}k</b>",
            #     textposition='top center',
            # ),
            # go.Scatter(
            #     name='NONE',
            #     mode='markers+text',
            #     x=usa.filter(pl.col('year') == usa['year'].max())['year'],
            #     y=usa.filter(pl.col('year') == usa['year'].max())[income_level],
            #     marker=dict(color='orange', size=8),
            #     text=f"<b>${usa.filter(pl.col('year') == usa['year'].max())[income_level].to_numpy().flatten()[0] / 1000:.0f}k</b>",
            #     textposition='bottom center',
            # ),
        ])
        #---------------------------------------------------
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
            multiplier = 1 if idx%2==0 else 2
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

        get_period_shading(fig=fig)

        fig.update_layout(
            title=dict(
                text=f"<b>Do taxes on the top 1% influence the gap?</b><br><sup>Based on {year_max} dollars</sup>",
            ),
            title_x=0.5,
            yaxis_title=axis_title_income + f"<br>{group_name}",
            yaxis=dict(
                # range=[0, 3000000],
                tickprefix="$",
                tickformat=axis_title_income_format,
            ),
            yaxis2=dict(
                title='top tax bracket changes',
                range=[-0.60,0.60],
                anchor='x',
                overlaying='y',
                side='right',
                tickformat='+.0%',
            ),
            xaxis_title=f"{sources['money']}",
            xaxis=dict(
                range=[1880,2030],
                tickmode='array',
                tickvals=[1902, 1945, 1969, 1980, 2023, 2032],
                ticktext=[1902, 1945, 1969, 1980, 2023, ''],
            ),
            showlegend=True,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        for trace in fig['data']:
            if ('NONE' in trace['name']):
                trace['showlegend'] = False

        return fig


    @output
    @render_widget
    def plot_timeseries_shares():
        # "bottom_50"
        # "top_1"
        usa = shares_data.filter(pl.col('country')=='usa')
        benchmarks = shares_data.filter(pl.col('country')!='usa')
        countries = benchmarks.select('country').unique().to_numpy().flatten().tolist()

        fig = go.Figure(data=(
            [
                go.Scatter(
                name='top 1%',
                x=usa['year'],
                y=usa['top_1'],
                line=dict(color="rgba(150,55,55,0.5)", width=4),
                text="<b>USA</b> Top 1%",
                ),

                go.Scatter(
                    name='bottom 50%',
                    x=usa['year'],
                    y=usa['bottom_50'],
                    line=dict(color="rgba(42,86,121,0.5)", width=4),
                    text="<b>USA</b> Bottom 50%",
                ),
            ]
        ))

        if input.show_country_comparisons()==True:
            fig.add_traces(
                [
                    go.Scatter(
                        name=country,
                        x=benchmarks.filter(pl.col('country') == country)['year'],
                        y=benchmarks.filter(pl.col('country') == country)['top_1'],
                        line=dict(color="rgba(42,86,121,0.5)"),
                        text=f"<b>{country}</b>",
                    ) for country in countries
                ]
                +
                [
                    go.Scatter(
                        name=country,
                        x=benchmarks.filter(pl.col('country') == country)['year'],
                        y=benchmarks.filter(pl.col('country') == country)['bottom_50'],
                        line=dict(color="rgba(150,55,55,0.5)"),
                        text=f"<b>{country}</b>",
                    ) for country in countries
                ]
            )

        get_period_shading(fig=fig)


        fig.update_layout(
            title="<b>Income Shares</b>",
            title_x=0.5,
            yaxis_title="share",
            yaxis=dict(
                # range=[-0.35, 0.35],
                tickformat=',.0%',
            ),
            xaxis=dict(
                range=[1880,2025],
                tickmode='array',
                tickvals=[1902, 1945, 1980, 2017],
                ticktext=[1902, 1945, 1980, 2017],
            ),
            showlegend=True,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        for trace in fig['data']:
            if ('top' in trace['name']) | ('bottom' in trace['name']):
                trace['showlegend']=True
            else:
                trace['showlegend'] = False
        return fig

    @output
    @render_widget
    def plot_tax():

        fig = go.Figure(data=(
                [
                    go.Scatter(
                        name='top bracket',
                        x=tax['year'],
                        y=tax['rate_max'],
                        line=dict(color="rgba(0,0,0,0.9)", width=3, dash='solid'),
                    ),
                    go.Scatter(
                        name='median',
                        x=tax['year'],
                        y=tax['rate_median'],
                        line=dict(color="rgba(0,0,0,0.3)", width=3),
                    ),
                    go.Scatter(
                        name='bottom bracket',
                        x=tax['year'],
                        y=tax['rate_min'],
                        line=dict(color="rgba(0,0,0,0.6)", width=3, dash='solid'),
                    ),

                ]
        ))

        fig.add_vrect(
            x0=1880,
            x1=1902,
            line_width=0,
            fillcolor='black',
            opacity=0.05,
            annotation_text='Guilded Age',
            annotation_position='bottom left',
        )
        fig.add_vrect(
            x0=1940,
            x1=1945,
            line_width=0,
            fillcolor='black',
            opacity=0.05,
            annotation_text='WWII',
            annotation_position='bottom left',
        )
        fig.add_vrect(
            x0=1980,
            x1=1988,
            line_width=0,
            fillcolor='black',
            opacity=0.05,
            annotation_text='Trickle Down Economics',
            annotation_position='bottom left',
        )
        fig.add_vrect(
            x0=2017,
            x1=2018,
            line_width=0,
            fillcolor='black',
            opacity=0.05,
            annotation_text='2017 Cuts',
            annotation_position='bottom left',
        )


        fig.update_layout(
            title="<b>Tax Rates</b>",
            title_x=0.5,
            yaxis_title="rate",
            yaxis=dict(
                # range=[-0.35, 0.35],
                tickformat=',.0%',
            ),
            xaxis=dict(range=[1880,2025]),
            showlegend=True,
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color_plotly(input.dark_mode()),
        )

        # for trace in fig['data']:
        #     if ('bottom_50' not in trace['name']) & ('top_1' not in trace['name']):
        #         trace['showlegend']=False

        return fig

    @render.image
    def img_freedom_scale():
        img = {
            "src": str(Path(__file__).parent / "static/images/freedom_scale.png"),
            "width": "90%",
        }
        return img

    @render.image
    def img_1619():
        img = {
            "src": str(Path(__file__).parent / "static/images/1619.jpg"),
            "width": "30%",
        }
        return img

    @render.image
    def img_american_character():
        img = {
            "src": str(Path(__file__).parent / "static/images/american_character.jpg"),
            "width": "30%",
        }
        return img





static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets=static_dir)