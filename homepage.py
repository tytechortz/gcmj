import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
from datetime import datetime as dt
from app import app
import dash_bootstrap_components as dbc


def get_header():

    header = html.Div([

        html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H1(children='Colorado Cannabis',
                    style = {'textAlign' : 'center'}
            )],
            className='col-8',
            style = {'padding-top' : '1%'}
        ),

        # html.Div([
            # html.Img(
            #         src = app.get_asset_url('logo_001c.png'),
            #         height = '43 px',
            #         width = 'auto')
            # ],
            # className = 'col-2',
            # style = {
            #         'align-items': 'center',
            #         'padding-top' : '1%',
            #         'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%'}
        )

    return header

def get_navbar(p='revenue'):
    navbar_revenue = html.Div([
        html.Div([], className='col-3'),
        html.Div([
            dcc.Link(
                html.H4(children='Revenue'),
                href='/revenue'
            )
        ],
            className='col-2'
        ),
    ])
    if p == 'revenue':
        return navbar_revenue
    

home_page_body = dbc.Container([
    html.Div([
        get_header(),
    ]),
    html.Div([
        get_navbar(),
    ]),
    html.Div([
        html.Div([
            html.H4('Revenue'),
            html.P(""" Colorado cannabis total revenue. """),
            dbc.Button("Click for Revenue Page", color="primary", href="/revenue"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H4('Per Capita Revenue'),
            html.P(""" Colorado cannabis per capita revenue. """),
            dbc.Button("Click for Per Capita Revenue Page", color="primary", href="/pcrev"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H4('Per License Revenue'),
            html.P(""" Colorado cannabis per license revenue. """),
            dbc.Button("Click for Per License Revenue Page", color="primary", href="/plrev"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H4('Businesses'),
            html.P(""" Colorado cannabis licensee locations. """),
            dbc.Button("Click for Cannabis Businesses Page", color="primary", href="/biz"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),

])

def Homepage():
    layout = html.Div([
    home_page_body
    ])
    return layout