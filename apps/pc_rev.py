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
                html.H4(children='Per Capita Revenue by County')
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