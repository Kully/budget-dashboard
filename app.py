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


FUNDS_AVAILABLE = 3000
SHARES_AVAILABLE = 0

RIGHT_FLOAT_INPUT = {
    'float': 'right',
    'text-align': 'right',
    'border': 'none',
}

RED_BORDER_STYLE = {'border': '1px solid red', 'border-radius': '4px'}
GREEN_BORDER_STYLE = {'border': '1px solid green', 'border-radius': '4px'}

df = pd.read_csv(
    'AAPL-Ticks-Sample/AAPL_2010-01-04.txt',
    header=None,
    names=['DateTime', 'Price', 'Volume', 'Exchange']
)
df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S:%f')

tickvals_y = [212, 213, 214, 215, 216]
ticktext_y = [f'${t}' for t in tickvals_y]

# filter dates between 9:30am - 4:00pm on Jan 4, 2010
market_start_date = datetime(2010, 1, 4, 9, 30)
market_end_date = datetime(2010, 1, 4, 16, 0)
mask = (df['DateTime'] > market_start_date) & (df['DateTime'] <= market_end_date)
df = df.loc[mask]

dateTimeArr = list(df['DateTime'])
priceArr = list(df['Price'])
current_time = int(len(dateTimeArr) / 2)

gridColor = '#dadada'
blueColor ='#2196F3'
darkBlueColor = '#3b6978'

fig = {
    'data': [
        {
            'x': dateTimeArr[:current_time],
            'y': priceArr[:current_time],
            'mode': 'lines',
            'marker': {
                'color': blueColor,
            }
        }
    ],
    'layout': {
        'margin': {'l': 7, 'r': 7}
    },
}

# add marker to denote last point
tail_x = fig['data'][0]['x'][-1]
tail_y = fig['data'][0]['y'][-1]

fig['layout']['shapes'] = [{
    'type': 'line',
    'xref': 'x',
    'yref': 'y',
    'x0': tail_x,
    'y0': min(priceArr),
    'x1': tail_x,
    'y1': max(priceArr),
    'line': {
        'color': darkBlueColor,
        'dash': 'dot',
        'width': 1,
    },
    
}]
fig = go.Figure(fig)


fig.update_xaxes(
    tickangle=-45,
    showspikes=True,
    spikecolor='#bababa',
    spikesnap='cursor',
    spikemode='across',
    spikethickness=1,
    spikedash='dot',
    gridcolor=gridColor,
    showgrid=True,
    tickmode='array',
    tickvals=[datetime(2010, 1, 4, i) for i in range(9, 17+1)],
    range=[market_start_date, market_end_date],
)
fig.update_yaxes(
    zeroline=False,
    gridcolor=gridColor,
    showgrid=True,

)
fig.update_layout(
    title='APPL (Jan 4, 2010)',
    plot_bgcolor='#fdfdfe',
    hoverlabel=dict(
        bgcolor='#fafafa',
        font_size=13,
        bordercolor='#555',
    )
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
server = app.server

badge = dbc.Button(
    ['Notifications', dbc.Badge('4', color='light', className='ml-1')],
    color='primary',
)

items = [
    dbc.DropdownMenuItem('Item 1'),
    dbc.DropdownMenuItem('Item 2'),
    dbc.DropdownMenuItem('Item 3'),
]

search_bar = dbc.Row(
    [
        dbc.Col(
            badge,
            width='auto',
        ),
        dbc.Col(
            dbc.Button('LOG OUT', color='light', className='mr-1'),
            width='auto',
        ),
    ],
    no_gutters=True,
    className='ml-auto flex-nowrap mt-3 mt-md-0',
    align='center',
)

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand('Intraday Trading', className='ml-2')),
                ],
                align='center',
                no_gutters=True,
            ),
        ),
        dbc.NavbarToggler(id='navbar-toggler'),
        dbc.Collapse(search_bar, id='navbar-collapse', navbar=True),
    ],
    color='dark',
    dark=True,
)


portfolio_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Order Entry', className='card-title'),
            dbc.ListGroup(
                [
                    dbc.FormGroup(
                        [
                            dbc.RadioItems(
                                options=[
                                    {'label': 'STK', 'value': 'STK'},
                                    {'label': 'OPT', 'value': 'OPT'},
                                ],
                                value='STK',
                                id='stk-opt-input',
                            ),
                        ]
                    ),
                    dbc.ListGroupItem([
                        html.Span([
                            html.Span('My Funds'),
                            html.Span(10000,
                                      id='funds-amount',
                                      style=RIGHT_FLOAT_INPUT),
                        ]),
                    ], id='funds-list-group-item'),
                    dbc.ListGroupItem([
                        html.Span([
                            html.Span('My APPL Shares'),
                            html.Span(0,
                                      id='shares-amount',
                                      style=RIGHT_FLOAT_INPUT),
                        ]),
                    ], id='shares-list-group-item'),
                    dbc.ListGroupItem([
                        html.Span([
                            html.Span('Quantity'),
                            dcc.Input(id='quantity-amount',
                                      type='number', min=0, value=10, step=5,
                                      style=RIGHT_FLOAT_INPUT),
                        ]),
                    ]),
                    dbc.ListGroupItem([
                        html.Span([
                            html.Span('Limit Price'),
                            dcc.Input(type='number', min=0, value=55, step=1, style=RIGHT_FLOAT_INPUT),
                        ]),
                    ]),
                    dbc.ListGroupItem([
                        html.Span([
                            html.Span('Stop Price'),
                            dcc.Input(type='number', min=0, value=56, step=1, style=RIGHT_FLOAT_INPUT),
                        ]),
                    ]),
                ],
                flush=True,
            ),
            dbc.Row([
                dbc.Col(dbc.Button('Buy', id='buy-button', color='success', block=True), width=6),
                dbc.Col(dbc.Button('Sell', id='sell-button', color='danger', block=True), width=6),
            ])
        ]
    ),
    className='mt-3',
)

chart_card = dbc.Card(
    dbc.CardBody([
        dcc.Graph(
            id='line-chart',
            figure=fig,
            config={
                'displayModeBar': False
            }
        ),
        dbc.CardHeader(html.Span([
            html.B('Time '),
            html.Span(id='line-chart-x-now'),
            html.B(' Price '),
            html.Span('$'),
            html.Span(str(priceArr[current_time]), id='line-chart-y-now'),
        ])),
        
    ]),
    className='mt-3',
)



first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5('Card title', className='card-title'),
            html.P('This card has some text content, but not much else'),
            dbc.Button('Go somewhere', color='primary'),
        ]
    )
)


@app.callback(
    [Output('line-chart', 'figure'),
     Output('line-chart-x-now', 'children'),
     Output('line-chart-y-now', 'children'),],
    [Input('interval1', 'n_intervals')],
    [State('line-chart', 'figure')]
)
def update_line_chart(n_intervals, fig):
    current_x = dateTimeArr[current_time + n_intervals]
    current_y = priceArr[current_time + n_intervals]

    fig['data'][0]['x'].append(current_x)
    fig['data'][0]['y'].append(current_y)
    
    return fig, current_x, current_y


@app.callback(
    [Output('funds-amount', 'children'),
     Output('shares-amount', 'children'),
     Output('funds-list-group-item', 'style'),
     Output('shares-list-group-item', 'style')],
    [Input('buy-button', 'n_clicks'),
     Input('sell-button', 'n_clicks')],
    [State('funds-amount', 'children'),
     State('shares-amount', 'children'),
     State('quantity-amount', 'value'),
     State('line-chart-y-now', 'children')]
)
def buy_sell_button(buy_n_clicks, sell_n_clicks, funds, shares, quantity, price_now):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'buy-button' in changed_id:
        # not enough funds
        if (funds - float(quantity) * float(price_now) < 0):
            return funds, shares, RED_BORDER_STYLE, {}

        new_funds = funds - float(quantity) * float(price_now)
        new_shares = shares + float(quantity)

        new_funds = round(new_funds, 2)
        new_shares = round(new_shares, 2)

        return new_funds, new_shares, {}, {}

    elif 'sell-button' in changed_id:
        # not enough shares
        if (float(shares) - float(quantity) < 0):
            return funds, shares, {}, RED_BORDER_STYLE

        new_funds = funds + float(quantity) * float(price_now)
        new_shares = int(shares - int(quantity))

        new_funds = round(new_funds, 2)

        return new_funds, new_shares, {}, {}

    return funds, shares, {}, {}


app.layout = html.Div([
    navbar,
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(portfolio_card, width=3),
                dbc.Col(chart_card)
            ]),
            dcc.Interval(id='interval1', interval=1000, n_intervals=0),
        ])
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
