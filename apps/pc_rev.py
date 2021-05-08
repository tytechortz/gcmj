import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from homepage import get_header, get_navbar, get_emptyrow



app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'green',
    'background-color' : 'green',
    'box-shadow' : '2px 5px 5px 1px rgba(0, 100, 0, .5)',
    'padding-top' : '10px'
}

externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

def pcrev_App():
    return html.Div([
        ##############################
        #Row 1 : Header
        get_header(),

        #Row 2 : Nav bar
        get_navbar('pc_rev'),

        #####################
        #Row 3 : Map, Instructions

        get_emptyrow(),
        html.Div([
            html.Div([
            ],
                className = 'col-1', #Blank column
            ),
            html.Div([ #External 10-column
                html.H4(children='Per Capita Revenue by County',
                        style={'color': 'white', 'text-align': 'center'}),
                html.Div([ #Internal Row
                    html.Div([
                        dcc.Graph('pcrev-map')
                    ],  
                        className='col-8'
                    ),
                    html.Div([
                        dcc.Markdown('''CLICK ON SHADED COUNTIES and use year slider to see annual county per capita revenue data and population and projected population growth.  Green counties have at least one form of legalized cannabis,green circles show relative cannabis per capita revenue for selected year.''',
                        style={'color': 'white'})
                    ],
                        className='col-4'
                    ),
                ],
                    className='row'
                ),
                get_emptyrow(),
                html.Div([ # Internal row
                    html.Div([
                        dcc.Slider(
                            id='year',
                            min=2014,
                            max=2020,
                            step=1,
                            marks={x: '{}'.format(x) for x in range(2014, 2021)},
                            value=2014,
                        ),
                    ],
                        className='col-8'
                    ),
                ],
                    className='row'
                ),
                html.Div([ #Internal row
                    html.Div([
                        dcc.RangeSlider(
                            id='year2',
                            min=1990,
                            max=2050,
                            step=1,
                            marks={
                                1990: '1990',
                                2014: '2014',
                                2020: '2020',
                                2050: '2050'
                            },
                            value=[2014,2020]
                        ),
                    ],
                        className='col-8'
                    ),
                ],
                    className='row'
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='per-cap-rev-bar')
                    ],
                        className='col-7'
                    ),
                    html.Div([
                        html.Div(id='pc-info')
                    ],
                        className='col-5'
                    ),
                ],
                    className='row'
                ),
                get_emptyrow(),
            ],
                className='col-10',
                style = externalgraph_colstyling, # External 10-column 
            ),
            html.Div([
            ],
                className = 'col-1', #Blank column
            ),
        ],
        className='row',
        style=externalgraph_rowstyling, # External row
        ),
        get_emptyrow(),
    ])



app.layout = pcrev_App