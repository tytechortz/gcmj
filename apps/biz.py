import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from homepage import get_header, get_navbar, get_emptyrow



app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

mapdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'green',
    'background-color' : 'green',
    'box-shadow' : '2px 5px 5px 1px rgba(0, 100, 0, .5)'
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

externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

def biz_App():
    return html.Div([
        ##############################
        #Row 1 : Header
        get_header(),

        #Row 2 : Nav bar
        get_navbar('biz'),

        #####################
        #Row 3 : Map, Instructions
        get_emptyrow(),
        html.Div([
            html.Div([
            ],
                className = 'col-1', #Blank column
            ),
            html.Div([ #External 10-column
                html.H4(children='Cannabis Businesses',
                        style={'color' : 'white', 'textAlign' : 'center'}),
                html.Div([#Internal Row
                    html.Div([
                        dcc.Graph('biz-map')
                    ],
                        className='col-8'
                    ),
                    html.Div([
                        dcc.Markdown('''Map shows markers for locations of 2019 cannabis licenses, the latest year available, color coded by license type. Select license type radio buttons to filter map. Use year slider below map to display number of licensees for given year in bar graph below'''),
                        dcc.RadioItems(id='categories', options=[
                        {'label':'All', 'value':'all'},
                        {'label':'MED Licensed Transporters','value':'MED Licensed Transporters'},
                        {'label':'MED Licensed Center','value':'MED Licensed Center'},
                        {'label':'MED Licensed Cultivator','value':'MED Licensed Cultivator'},
                        {'label':'MED Licensed Infused Product Manufacturer','value':'MED Licensed Infused Product Manufacturer'},
                        {'label':'MED Licensed R&D Cultivation','value':'MED Licensed R&D Cultivation'},
                        {'label':'MED Licensed Retail Operator','value':'MED Licensed Retail Operator'},
                        {'label':'MED Licensed Testing Facility','value':'MED Licensed Testing Facility'},
                        {'label':'MED Licensed Retail Marijuana Product Manufacturer','value':'MED Licensed Retail Marijuana Product Manufacturer'},
                        {'label':'MED Licensed Retail Cultivator','value':'MED Licensed Retail Cultivator'},
                        {'label':'MED Licensed Retail Testing Facility','value':'MED Licensed Retail Testing Facility'},
                        {'label':'MED Licensed Retail Transporter','value':'MED Licensed Retail Transporter'},
                        {'label':'MED Licensed Retail Marijuana Store','value':'MED Licensed Retail Marijuana Store'},
                        ],        
                        labelStyle={'display':'block', 'margin': 0, 'padding': 1},
                        value = 'all'
                        ),
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
    ])



app.layout = biz_App