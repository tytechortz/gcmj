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

        # html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H1(children='Colorado Cannabis',
                    style = {'textAlign' : 'center'}
            )],
            className='col-12',
            style = {'padding-top' : '1%'}
        ),
        ],
        className = 'row',
        style = {'height' : '4%',
                'background-color' : 'green'}
        )

    return header

def get_navbar(p = 'homepage'):
    navbar_revenue = html.Div([
        html.Div([], className='col-3'),
        html.Div([
            dcc.Link(
                html.H6(children='Home'),
                href='/homepage'
            )
        ],
            className='col-2'
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per Capita Revenue'),
                href='/pcrev'
            )
        ],
            className='col-2'
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per License Revenue'),
                href='/plrev'
            )
        ],
            className='col-2'
        ),
        html.Div([], className = 'col-3')
    ],
    className = 'row',
    style = {'background-color' : 'fern',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )

    navbar_homepage = html.Div([
        html.Div([], className='col-3'),
        html.Div([
            dcc.Link(
                html.H6(children='Revenue'),
                href='/apps/revenue'
            )
        ],
            className='col-2'
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per Capita Rev.'),
                href='/apps/pcrev'
            )
        ],
            className='col-2'
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per License Rev.'),
                href='/apps/plrev'
            )
        ],
            className='col-2'
        ),
        html.Div([], className = 'col-3')
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )
    if p == 'homepage':
        return navbar_homepage
    elif p == 'revenue':
        return navbar_revenue

def get_emptyrow(h='15px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow

    
def home_page_App():
    return html.Div([
        get_header(),

        get_navbar('homepage'),

        
    ])


app.layout = home_page_App

#     html.Div([
#         html.Div([
#             html.H4('Revenue'),
#             html.P(""" Colorado cannabis total revenue. """),
#             dbc.Button("Click for Revenue Page", color="primary", href="/revenue"),
#         ],
#             className='twelve columns'
#         ),
#     ],
#         className='row'
#     ),
#     html.Div([
#         html.Div([
#             html.H4('Per Capita Revenue'),
#             html.P(""" Colorado cannabis per capita revenue. """),
#             dbc.Button("Click for Per Capita Revenue Page", color="primary", href="/pcrev"),
#         ],
#             className='twelve columns'
#         ),
#     ],
#         className='row'
#     ),
#     html.Div([
#         html.Div([
#             html.H4('Per License Revenue'),
#             html.P(""" Colorado cannabis per license revenue. """),
#             dbc.Button("Click for Per License Revenue Page", color="primary", href="/plrev"),
#         ],
#             className='twelve columns'
#         ),
#     ],
#         className='row'
#     ),
#     html.Div([
#         html.Div([
#             html.H4('Businesses'),
#             html.P(""" Colorado cannabis licensee locations. """),
#             dbc.Button("Click for Cannabis Businesses Page", color="primary", href="/biz"),
#         ],
#             className='twelve columns'
#         ),
#     ],
#         className='row'
#     ),

# ])

# def Homepage():
#     layout = html.Div([
#     home_page_body
#     ])
#     return layout