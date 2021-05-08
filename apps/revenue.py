import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from homepage import get_header, get_navbar, get_emptyrow



app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

month_values ={1:'JANUARY', 2:'FEBRUARY', 3:'MARCH', 4:'APRIL', 5:'MAY', 6:'JUNE', 7:'JULY', 8:'AUGUST', 9:'SEPTEMBER', 10:'OCTOBER', 11:'NOVEMBER', 12:'DECEMBER'}

mapdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'green',
    'background-color' : 'green',
    'box-shadow' : '2px 5px 5px 1px rgba(0, 100, 0, .5)'
    }

externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'green',
    'background-color' : 'green',
    'box-shadow' : '2px 5px 5px 1px rgba(0, 100, 0, .5)',
    'padding-top' : '10px'
}




def revenue_App():
    return html.Div([

        ##############################
        #Row 1 : Header
        get_header(),

        #Row 2 : Nav bar
        get_navbar('revenue'),

        #####################
        #Row 3 : Map, Instructions
        
        get_emptyrow(),
        html.Div([
            html.Div([
            ],
                className = 'col-1', # Blank 1 column
            ),
            html.Div([ # External 10-column
                html.H4(children="Revenue By County",
                        style={'color' : 'white', 'textAlign' : 'center'}),
                html.Div([ # Internal Row
                    html.Div([
                        dcc.Graph('revenue-map')
                    ],
                        className='col-8'
                    ),
                    html.Div([
                        dcc.Markdown('''CLICK ON GREEN SHADED COUNTIES and use year slider to see annual county revenue data displayed in graphs.  Green counties have at least one form of legalized cannabis, green circles show relative cannabis revenue for selected year. 
                        Select sales check boxes to display revenue graphically by type below left. Select Year or Month button below to display county revenue by month across years, or to display cumulative revenue totals for each month, respectively.''',
                        style={'color': 'white'})    
                    ],
                        className='col-4'
                    ),
                ],
                    className='row'
                ),
                get_emptyrow(),
                html.Div([
                    html.Div([
                        dcc.Slider(
                            id='year',
                            min=2014,
                            max=2020,
                            step=1,
                            marks={x: '{}'.format(x) for x in range(2014, 2021)},
                            value=2014
                        ),
                    ],
                        className='col-8'
                    ),
                    html.Div([
                        dcc.RadioItems(
                            id='month-year', 
                            options=[
                                {'label':'Year', 'value':'yr'},
                                {'label':'Month', 'value':'mo'},
                            ],
                            labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1},
                            value='mo',
                            style = {'text-align': 'center', 'color': 'white'}
                        ),
                    ],
                        className='col-4'
                    ),
                ],
                    className='row'
                ),
                html.Div([
                    html.Div([
                        dcc.Checklist(
                            id='rev',
                            options=[
                                {'label':'Total Sales', 'value':'TOTAL'},
                                {'label':'Rec Sales','value':'REC'},
                                {'label':'Med Sales','value':'MED'},
                            ],
                            labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1},
                            value = ['TOTAL'],
                            style = {'text-align': 'center', 'color': 'white' }
                            ),
                    ],
                        className='col-6'
                    ),
                    html.Div([
                        dcc.Slider(
                            id='month',
                            min=1,
                            max=12,
                            step=1,
                            marks={x: '{}'.format(x) for x in range(1, 13)},
                            value=1,
                        )
                    ],
                        className='col-6'
                    ),
                ],
                    className='row'
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='rev-scatter')
                    ],
                        className='col-6'
                    ),
                    html.Div([
                        dcc.Graph(id='month-rev-bar')
                    ],
                        className='col-6'
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
                className='col-1', # Blank 1 column
            ),
        ],
        className='row',
        style=externalgraph_rowstyling, # External row
        ),
        get_emptyrow(),
        html.Div(id='crat', style={'display': 'none'}),
    ])

app.layout = revenue_App