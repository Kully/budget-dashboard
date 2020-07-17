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


BODY_STYLE = {
    "margin": "1em",
}

HEADER_STYLE  = {
    
}

FLOAT_RIGHT = {
    "float": "right",
}

# figure stuff

gridColor = '#dadada'
blueColor ='#2196F3'
darkBlueColor = '#3b6978'

figure = {
    "data": [
        {
            "x":  ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"],
            "y":  [4, 17, 12, 3, 6, 10, 11],
            # 'mode': 'lines',
            "marker": {
                "color": blueColor,
                "size": 14
            }
        }
    ],
    "layout": {
        "yaxis": {"range": [0, 20], "zeroline": False},
        "plot_bgcolor": "#fdfdfe",
        # "margin": {"l": 7, "r": 7}
    },
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
server = app.server

app.layout = html.Div([
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H3("Budget"),
                ]),
                dbc.Col([
                    dbc.Input(id="nav-input", type="text", placeholder="search algorithm...", bs_size="md", className="mr-3"),
                ], width=7),
                dbc.Col([
                    dbc.Button("LOG OUT", color="light", className="mr-1", style=FLOAT_RIGHT),
                    dbc.Button("VERIFY", color="success", className="mr-1", style=FLOAT_RIGHT),
                    dbc.Button("RUN", color="primary", className="mr-1", style=FLOAT_RIGHT),
                ], width=4),
            ]),
        ]),
        dbc.CardBody(dbc.Row([
            # side bar
            dbc.Col(
                dbc.ListGroup([
                    dbc.ListGroupItem("Home"),
                    dbc.ListGroupItem("Design"),
                    dbc.ListGroupItem("Analysis"),
                    dbc.ListGroupItem("Tensor"),
                    dbc.ListGroupItem("Eval"),
                ])
                # dbc.Card([
                #     dbc.ListGroup
                # ])
            ),
            # main app view
            dbc.Col(
                dbc.Card([
                    dcc.Graph(id="plot",
                              figure=figure,
                              config={"displayModeBar": False})
                ], color="primary", outline=True), width=10
            ),
        ]), className="mb-4"),
    ])
], style=BODY_STYLE)

if __name__ == "__main__":
    app.run_server(debug=True)
