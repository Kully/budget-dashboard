import plotly
import plotly.express as px
import plotly.graph_objs as go

import numpy as np
import pandas as pd

from datetime import datetime
import random
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


gridColor = "#dadada"
blueColor = "#2196F3"
redColor = "red"
darkBlueColor = "#3b6978"
plotTopMargin = 50

FUNDS_AVAILABLE = 3000
SHARES_AVAILABLE = 0

FLOAT_RIGHT = {"float": "right"}

RED_BORDER_STYLE = {"border": "1px solid red", "border-radius": "4px"}
GREEN_BORDER_STYLE = {"border": "1px solid green", "border-radius": "4px"}

SUBTITLE_STYLE = {
    "color": "#aab",
    "font-style": "italic",
}
ACTIVE_LABEL = {
    "background-color": "#cbeaed",
    "border": "1px solid " + blueColor,
    "border-radius": "4px"
}

budget_monthly_goals_dict = {
    "Groceries": 80,
    "Restaurants": 40,
    "Travel": 75,
    "Coffee": 65,
    "Misc": 50,
}
budget_monthly_spending_dict = {
    "Groceries": 80-10,
    "Restaurants": 40-20,
    "Travel": 75-5,
    "Coffee": 65+5,
    "Misc": 50-30,
}

y_values = [4, 17, 12, 3, 6, 10, 11]

weekly_spending_figure = {
    "data": [
        {
            "x":  ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"],
            "y":  y_values,
            "marker": {
                "color": blueColor,
                "size": 14
            }
        }
    ],
    "layout": {
        "title": "Weekly Spending",
        "yaxis": {"range": [0, 20], "zeroline": False},
        "plot_bgcolor": "#fdfdfe",
        "margin": {"l": 25, "b": 25, "r": 25, "t": plotTopMargin}
    },
}

pie_figure = go.Figure(
    data=[
        go.Pie(
            values=list(budget_monthly_spending_dict.values()),
            text=list(budget_monthly_spending_dict.keys()),
            hole=.86,
            marker=dict(
                colors=px.colors.sequential.Blues,
                line=dict(color="#fafafa", width=4)
            ),
        )
    ],
    layout=dict(
        showlegend=False,
        margin=dict(l=2, r=2, t=2, b=2)
    )
)

bar_figure = go.Figure(
    data=[
        go.Bar(
            x=[k for k in budget_monthly_spending_dict.keys()],
            y=[budget_monthly_spending_dict[k] for k in budget_monthly_spending_dict.keys()],
            marker=dict(
                color=[blueColor, blueColor, blueColor, redColor, blueColor],
            ),
        ),
    ],
    layout=dict(
        title="Monthly Goal Tracking",
        plot_bgcolor="#fdfdfe",
        margin={"l": 25, "b": 25, "r": 25, "t": plotTopMargin}
    ),
)
for idx, spendingCategory in enumerate(budget_monthly_goals_dict.keys()):
    bar_figure.add_shape(
        type="line",
        x0=-0.5+idx,
        x1=0.5+idx,
        y0=budget_monthly_goals_dict[spendingCategory],
        y1=budget_monthly_goals_dict[spendingCategory],
        line=dict(
            color="black",
            width=2,
            dash="dash",
        ),
    )


investment_filled_line_chart = go.Figure(
    data=[
        go.Bar(
            x=[k for k in budget_monthly_spending_dict.keys()],
            y=[budget_monthly_spending_dict[k] for k in budget_monthly_spending_dict.keys()],
            marker=dict(
                color=[blueColor, blueColor, blueColor, redColor, blueColor],
            ),
        ),
    ],
    layout=dict(
        title="Monthly Goal Tracking",
        plot_bgcolor="#fdfdfe",
        margin={"l": 25, "b": 25, "r": 25, "t": plotTopMargin}
    ),
)


def stock_chart():
    df = pd.read_csv(
        "./AAPL-Ticks-Sample/AAPL_2010-01-04.txt",
        header=None,
        names=["DateTime", "Price", "Volume", "Exchange"]
    )
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%Y-%m-%d %H:%M:%S:%f")

    tickvals_y = [212, 213, 214, 215, 216]
    ticktext_y = [f"${t}" for t in tickvals_y]

    # filter dates between 9:30am - 4:00pm on Jan 4, 2010
    market_start_date = datetime(2010, 1, 4, 9, 30)
    market_end_date = datetime(2010, 1, 4, 16, 0)
    mask = (df["DateTime"] > market_start_date) & (df["DateTime"] <= market_end_date)
    df = df.loc[mask]

    dateTimeArr = list(df["DateTime"])
    priceArr = list(df["Price"])
    current_time = int(len(dateTimeArr) / 2)

    fig = {
        "data": [
            {
                "x": dateTimeArr[:current_time],
                "y": priceArr[:current_time],
                "mode": "lines",
                "marker": {
                    "color": blueColor,
                }
            }
        ],
        "layout": {
            "margin": {"l": 7, "r": 7}
        },
    }

    # add marker to denote last point
    tail_x = fig["data"][0]["x"][-1]
    tail_y = fig["data"][0]["y"][-1]

    fig["layout"]["shapes"] = [{
        "type": "line",
        "xref": "x",
        "yref": "y",
        "x0": tail_x,
        "y0": min(priceArr),
        "x1": tail_x,
        "y1": max(priceArr),
        "line": {
            "color": darkBlueColor,
            "dash": "dot",
            "width": 1,
        },
        
    }]
    fig = go.Figure(fig)
    fig.update_xaxes(
        tickangle=-45,
        showspikes=True,
        spikecolor="#bababa",
        spikesnap="cursor",
        spikemode="across",
        spikethickness=1,
        spikedash="dot",
        gridcolor=gridColor,
        showgrid=True,
        tickmode="array",
        tickvals=[datetime(2010, 1, 4, i) for i in range(9, 17+1)],
        range=[market_start_date, market_end_date],
    )
    fig.update_yaxes(
        zeroline=False,
        gridcolor=gridColor,
        showgrid=True,

    )
    fig.update_layout(
        title="APPL",
        plot_bgcolor="#fdfdfe",
        hoverlabel=dict(
            bgcolor="#fafafa",
            font_size=13,
            bordercolor="#555",
        ),
        margin={"t": plotTopMargin}
    )
    return fig

trading_chart = stock_chart()


def filled_line_chart():
    fig = go.Figure(
        data=[
            go.Scatter(
                x=[i for i in range(350)],
                y=[i + 3*random.normalvariate(0, 1) for i in range(350)],
                mode="lines",
                fill="tozeroy",
                marker=dict(
                    color=blueColor,
                )
            )
        ],
        layout=dict(
            margin=dict(
                l=7,
                r=7,
                b=0,
                t=plotTopMargin,
            )
        )
    )

    # tail_x = fig["data"][0]["x"][-1]
    # tail_y = fig["data"][0]["y"][-1]

    fig = go.Figure(fig)
    fig.update_xaxes(
        tickangle=-45,
        showspikes=True,
        spikecolor="#bababa",
        spikesnap="cursor",
        spikemode="across",
        spikethickness=1,
        spikedash="dot",
        gridcolor=gridColor,
        showgrid=True,
        tickmode="array",
    )
    fig.update_yaxes(
        zeroline=False,
        gridcolor=gridColor,
        showgrid=True,

    )
    fig.update_layout(
        title="Net Worth",
        plot_bgcolor="#fdfdfe",
        hoverlabel=dict(
            bgcolor="#fafafa",
            font_size=13,
            bordercolor="#555",
        ),
        margin={"t": plotTopMargin}
    )
    return fig




tab1_content = html.Div([
    dbc.CardBody([
        dbc.Row([
            # line chart
            dbc.Col(
                dcc.Graph(id="plot",
                          figure=weekly_spending_figure,
                          config={"displayModeBar": False},
                          style={"height": "33.5vh"}), width=8
            ),
            # pie chart
            dbc.Col(
                dcc.Graph(id="pie-plot",
                          figure=pie_figure,
                          config={"displayModeBar": False},
                          style={"height": "33.5vh"})
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                          figure=filled_line_chart(),
                          config={"displayModeBar": False},
                          style={"height": "33.5vh"}
                          ), width=12
            ),
        ]),
    ]),
], id="tab1-content")

tab2_content = html.Div([
    dbc.CardBody([
        dbc.Col(
            dcc.Graph(id="bar-chart",
                      figure=bar_figure,
                      style={"height": "67vh"},
                      config={"displayModeBar": False}),
             width=12
        ),
    ])    

], id="tab2-content")

tab3_content = html.Div([
    dbc.CardBody([
        dbc.Col(
            dcc.Graph(
                id="trading_chart",
                figure=trading_chart,
                style={"height": "67vh"},
                config={
                    "displayModeBar": False
                }
            ),
             width=12
        ),
    ])    

], id="tab3-content")

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Overview", href="#")),
        dbc.NavItem(dbc.NavLink("Banking", href="#")),
        dbc.NavItem(dbc.NavLink("Investing", href="#")),
        dbc.NavItem(dbc.NavLink("Insights", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Settings", href="#"),
                dbc.DropdownMenuItem("Help", href="#"),
                dbc.DropdownMenuItem("Metrics", href="#"),
                dbc.DropdownMenuItem("Tools", href="#"),
                dbc.DropdownMenuItem("Log Out", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Hi, User1423",
        ),
        dbc.Button(
            ["", dbc.Badge("+5", color="light", className="ml-1")],
            color="primary",
        ),
    ],
    brand="Personal Finance and Budgeting Tool",
    brand_href="#",
    color="primary",
    fluid=True,
)

tab_card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Budget", tab_id="tab-1"),
                    dbc.Tab(label="Goals", tab_id="tab-2"),
                    dbc.Tab(label="Investments", tab_id="tab-3"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
server = app.server


app.layout = html.Div([
    navbar,
    dbc.Container(tab_card, fluid=True),
],)


@app.callback(
    Output("card-content", "children"),
    [Input("card-tabs", "active_tab")],
)
def update_tab_content(activeTab):
    if activeTab == "tab-1":
        return tab1_content
    elif activeTab == "tab-2":
        return tab2_content
    elif activeTab == "tab-3":
        return tab3_content


if __name__ == "__main__":
    app.run_server(debug=True)
