import plotly
import plotly.express as px
import plotly.graph_objs as go

import numpy as np
import pandas as pd

from datetime import datetime
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


gridColor = '#dadada'
blueColor ='#2196F3'
darkBlueColor = '#3b6978'

BODY_STYLE = {"margin": "1em"}
FLOAT_RIGHT = {"float": "right"}
SUBTITLE_STYLE = {
    "color": "#aab",
    "font-style": "italic",
}
ACTIVE_LABEL = {
    "background-color": "#cbeaed",
    "border": "1px solid " + blueColor,
    "border-radius": "4px"
}

y_values = [4, 17, 12, 3, 6, 10, 11]
figure = {
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
        "yaxis": {"range": [0, 20], "zeroline": False},
        "plot_bgcolor": "#fdfdfe",
        "margin": {"l": 25, "b": 25, "r": 25, "t": 25}
    },
}

pie_figure = go.Figure(
    data=[
        go.Pie(
            values=y_values,
            hole=.86,
            marker=dict(
                colors=px.colors.sequential.Blues,
                line=dict(color='#fafafa', width=4)
            ),
            textinfo=None,
            text=None
        )
    ],
    layout=dict(
        showlegend=False,
        margin=dict(l=2, r=2, t=2, b=2)
    )
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
server = app.server

app.layout = html.Div([
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H3("Dashboard Analysis"),
                    html.Span("a metric-analysis tool", style=SUBTITLE_STYLE)
                ]),
                dbc.Col([
                    dbc.Select(
                        id="select",
                        value="Least Squares",
                        options=[
                            {"label": "Linear Regression", "value": "1"},
                            {"label": "Least Squares", "value": "2"},
                            {"label": "Stochastic Gradient Descent", "value": "3"},
                            {"label": "Principal Component Analysis", "value": "4", "disabled": True},
                            {"label": "Tensor Flow", "value": "3", "disabled": True},
                        ],
                    )

                ], width=6),
                dbc.Col([
                    dbc.ButtonGroup(
                        [dbc.Button("Run", color="success"),
                         dbc.Button("Stop", color="danger"),
                         dbc.Button("Verify", color="warning"),
                         dbc.Button("Sign Out", color="light")],
                        size="lg",
                        className="mr-1",
                        style=FLOAT_RIGHT
                    ),
                ], width=4),
            ]),
        ]),
        dbc.CardBody(dbc.Row([
            
            # 1st part
            dbc.Col([
                dbc.ListGroup([
                    dbc.ListGroupItem("Home"),
                    dbc.ListGroupItem("Plots", style=ACTIVE_LABEL),
                    dbc.ListGroupItem("Budget"),
                    dbc.ListGroupItem("Pricing"),
                    dbc.ListGroupItem("Invoice"),
                    dbc.ListGroupItem("Widgets"),
                ]),
                dbc.Button(
                    "Create Report",
                    id="create-report-button",
                    color="primary", style={"width": "100%", "top": "1.25rem"})
            ]),
            # 2nd part
            dbc.Col(
                dbc.Card([
                    dcc.Graph(id="plot",
                              figure=figure,
                              config={"displayModeBar": False})
                ], color="primary"), width=5
            ),
            # 3rd part
            dbc.Col(
                dbc.Card([
                    dcc.Graph(id="pie-plot",
                              figure=pie_figure,
                              config={"displayModeBar": False})
                ], color="primary"), width=5
            ),

        ]), className="mb-4"),
    ])
], style=BODY_STYLE)

if __name__ == "__main__":
    app.run_server(debug=True)
