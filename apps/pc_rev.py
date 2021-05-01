import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from homepage import get_header, get_navbar, get_emptyrow



app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

def pcrev_App():
    return html.Div([
        ##############################
        #Row 1 : Header
        get_header(),
    ])



app.layout = pcrev_App