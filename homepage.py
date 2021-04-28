import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
from datetime import datetime as dt
from app import app
import dash_bootstrap_components as dbc
from data import df_revenue, df_pc


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
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
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


# url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
# dataset2 = pd.read_csv(url)
# print(dataset2)

# df = df_revenue
# df = df.fillna(0)
df = df_pc.fillna(0)

dataset = df
# dataset.fillna(0)
print(dataset)

years = ["2014", "2015", "2016", "2017", "2018", "2019", "2020"]

counties = []
for county in dataset["county"]:
    if county not in counties:
        counties.append(county)
# print(counties)
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

fig_dict["layout"]["xaxis"] = {"range": [0, 2000], "title": "PerCap Rev"}
fig_dict["layout"]["yaxis"] = {"range": [0, 100000000], "title": "Tot. Rev."}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"                                                      
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {

        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

year = 2014
for county in counties:
    dataset_by_year = dataset[dataset["year"] == year]
    dataset_by_year_and_county = dataset_by_year[dataset_by_year["county"] == county]

    data_dict = {
        "x": list(dataset_by_year_and_county["pc_rev"]),
        "y": list(dataset_by_year_and_county["tot_sales"]),
        "mode": "markers",
        "text": list(dataset_by_year_and_county["county"]),
        "marker": {
            "sizemode": "area",
            "sizeref": 20000,
            "size": list(dataset_by_year_and_county["totalpopulation"])
        },
        "name": county
    }
    fig_dict["data"].append(data_dict)

for year in years:
    frame = {"data": [], "name": str(year)}
    for county in counties:
        dataset_by_year = dataset[dataset["year"] == int(year)]
        dataset_by_year_and_county = dataset_by_year[dataset_by_year["county"] == county]

        data_dict = {
            "x": list(dataset_by_year_and_county["pc_rev"]),
            "y": list(dataset_by_year_and_county["tot_sales"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_county["county"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 20000,
                "size": list(dataset_by_year_and_county["totalpopulation"]),
            },
            "name": county
        }
        frame["data"].append(data_dict)
    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": False},
        "mode": "immediate",
        "transition": {"duratiion": 300}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)




    
def home_page_App():
    return html.Div([
        get_header(),

        get_navbar('homepage'),

        get_emptyrow(),
        html.Div([
            html.Div([
            ],
                className = 'col-1', # Blank 1 column
            ),
            html.Div([
                html.H4(children='Cannabis Data',
                        style={'color' : 'white', 'textAlign' : 'center'}),
                html.Div(fig.show())
            ],
                className='col-10',
                style = externalgraph_colstyling, # External 10-column
            ),
            html.Div([
            ],
                className = 'col-1', # Blank 1 column
            ),
        ],
        className='row',
        style=externalgraph_rowstyling, # External row
        ),
    ])


app.layout = home_page_App

