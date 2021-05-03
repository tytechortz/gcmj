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

def plrev_App():
    return html.Div([
        ##############################
        #Row 1 : Header
        get_header(),

        #Row 2 : Nav bar
        get_navbar('pl_rev'),

        #####################
        #Row 3 : Map, Instructions
        get_emptyrow(),
        html.Div([
            html.Div([
            ],
                className = 'col-1', #Blank column
            ),
            html.Div([ #External 10-column
                html.H4(children='Per License Revenue by County',
                style={'color': 'white', 'text-align': 'center'}),
                html.Div([ #Internal Row
                    html.Div([
                        dcc.Graph('plrev-map')
                    ],  
                        className='col-8'
                    ),
                    html.Div([
                        dcc.Markdown('''Click on green-shaded counties to show revenue, license count, revenue per license, county ranking, and revenue change from 2019 to 2020. Counties are shaded to indicate realative revenue per license, with darker shades representing higher values. 2019 is the most recent year for license information.''',
                        style={'color': 'white'})
                    ],
                        className='col-4'
                    ),
                ],
                    className='row'
                ),
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
        html.Div(id='pl-data', style={'display': 'none'}),
    ])



app.layout = plrev_App