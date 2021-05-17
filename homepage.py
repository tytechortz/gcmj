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
from data import df_revenue, df_pc, df_rev, df_bidness
# from callbacks import df_combo


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
                    style = {'textAlign' : 'center', 'color':'white'}
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
    navbar_homepage = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Revenue'),
                href='/apps/revenue'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per Capita Rev.'),
                href='/apps/pc_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per License Rev.'),
                href='/apps/pl_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Businesses'),
                href='/apps/biz'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2')
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    navbar_revenue = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Home'),
                href='/homepage'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per Capita Rev.'),
                href='/apps/pc_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per License Rev.'),
                href='/apps/pl_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Businesses'),
                href='/apps/biz'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2')
    ],
    className = 'row',
    style = {'background-color' : 'fern',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    navbar_pcrev = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Home'),
                href='/homepage'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
            
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Revenue'),
                href='/apps/revenue'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per License Rev.'),
                href='/apps/pl_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Businesses'),
                href='/apps/biz'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2')
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    navbar_plrev = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Home'),
                href='/homepage'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Revenue'),
                href='/apps/revenue'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per Capita Rev.'),
                href='/apps/pc_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Businesses'),
                href='/apps/biz'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2')
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    navbar_biz = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Home'),
                href='/homepage'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Revenue'),
                href='/apps/revenue'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per Capita Rev.'),
                href='/apps/pc_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Per License Rev.'),
                href='/apps/pl_rev'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2')
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    if p == 'homepage':
        return navbar_homepage
    elif p == 'revenue':
        return navbar_revenue
    elif p == 'pc_rev':
        return navbar_pcrev
    elif p == 'pl_rev':
        return navbar_plrev
    elif p == 'biz':
        return navbar_biz

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

df = df_pc

df = df[df.county != 'SUM OF NR COUNTIES']
df.drop(['color', 'COUNTY', 'CENT_LAT', 'CENT_LONG'], axis=1, inplace=True)
df['diff'] = df['totalpopulation'] - df['totalpopulation'].shift(64)
df = df.fillna(0)

df['diff'] = df['diff'].astype(int)

df['cum_sum'] = df.groupby(['county'])['diff'].apply(lambda x: x.cumsum())
df['cum_pct'] = df.apply(lambda x: (x['cum_sum'] / x['totalpopulation']), axis=1)

df = df.fillna(0)
dataset = df
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

fig_dict["layout"]["xaxis"] = {"range": [-500, 5000],"title": "Per Capita Revenue"}
fig_dict["layout"]["yaxis"] = {"range": [5, 9.5], 'type': 'log',  "title": "Total Revenue Per Year"}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict['layout']['height'] = 500
fig_dict['layout']['margin'] = {'l': 50, 'r': 0, 'b': 0, 't': 0, 'pad': 4}
        
fig_dict['layout']['paper_bgcolor'] = 'green'
# fig_dict['layout']['plot_bgcolor'] = 'lightgreen'
fig_dict['layout']['font_color'] = 'white'
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
    "x": .1,
    "y": 0,
    "steps": []
}

year = 2014
for county in counties:
    dataset_by_year = dataset[dataset["year"] == year]
    dataset_by_year_and_county = dataset_by_year[dataset_by_year["county"] == county]
    # print(dataset_by_year_and_county)

    data_dict = {
        "x": list(dataset_by_year_and_county["pc_rev"]),
        "y": list(dataset_by_year_and_county["tot_sales"]),
        "mode": "markers",
        "text": list(dataset_by_year_and_county["county"]),
        "marker": {
            "sizemode": "area",
            "sizeref": 300,
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
                "sizeref": 300,
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

##############################################################
# ALL REVENUE BAR CHART
##############################################################
df = df_rev
df = df.drop(index=[8,87,134,166,249,339,378,487,517,1238,1173,1108,1043,978,913,720,655,590,5076])

df.index = pd.to_datetime(df['year'].astype(str) + df['month'].astype(str), format='%Y%m')

df_new = df.loc['2021-01-01':]
df_month = df.loc[:'2020-12-31']#.groupby('month')['tot_sales'].sum()
df_month = df_month.groupby('month')['tot_sales'].sum()

current_data_month = int(df_new['month'].iloc[-1])
df_new_rev = df_new.groupby('year')['tot_sales'].sum()


df_new_tot = df_new.groupby('month')['tot_sales'].sum()

df_ly = df.loc['2020-01-01':'2020-12-31'].groupby('month')['tot_sales'].sum()

last_year_tot = df_ly.sum()

df_ly_td = df_ly.head(current_data_month)

ly_tot_td = df_ly_td.sum()
ty_tot_td = df_new_tot.sum()
print(ly_tot_td)
print(ty_tot_td)

ty_proj_tot = (ty_tot_td / ly_tot_td) * last_year_tot
ty_per_sec = ty_proj_tot / 31536000

# df_new_rev['2021'] = (df_new_rev.iloc[0] / ly_tot_td) * last_year_tot
proj_rev = (df_new_rev.iloc[0] / ly_tot_td) * last_year_tot
print(proj_rev)

data = {'': proj_rev}
df_ty_rev = pd.DataFrame(data, index=[2021])
print(df_ty_rev)

df_new_rev = df_new_rev.to_frame()#.tail(1)
print(df_new_rev)

df = df.groupby('year')['tot_sales'].sum()
df.drop(df.tail(1).index, inplace=True)
tot_rev_thru_ly = df.sum()

fig_tot_rev = go.Figure()

fig_tot_rev.add_trace(go.Bar(x=df.index, 
                            y=df,
                            marker={'color': 'black'}
                            )),

fig_tot_rev.add_trace(go.Bar(x=df_new_rev.index,
                            y=df_new_rev['tot_sales'],
                            marker={'color': 'black'}
                            )),

fig_tot_rev.add_trace(go.Bar(x=df_ty_rev.index,
                            y=df_ty_rev.iloc[0],
                            marker={'color': 'green'}
                            )),

fig_tot_rev.update_layout(
    height=250,
    autosize=True,
    paper_bgcolor='green',
    plot_bgcolor='lightgreen',
    margin=dict(
        l=50,
        r=0,
        b=0,
        t=0,
        pad=4
    ),
    showlegend=False,
    font_color='white',
    barmode='stack'
)
    


    
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
                html.Div([
                    html.Div([
                        html.H4(children='Statewide Cannabis Data',
                        style={'color' : 'white', 'text-align' : 'center'}),
                    ],
                        className='col-12'
                    ),
                ],
                    className='row'
                ),
                html.Div([
                    html.Div([
                        dcc.Markdown('''The cannabis industry in Colorado has grown from $683 million in 2014 to over $2 billion in 2020, reaching the $10 billion total sales mark this year. This interactive app attempts to allow the user to look for trends in cannabis revenue data, and how those may relate to location, population or time of year in particular counties.''', 
                        style={'color': 'white'})
                    ],
                        className='col-7'
                    ),
                    html.Div([
                        html.Div([
                            html.Div(id='tot-rev-led')
                        ],
                            className='row'
                        ),
                        html.Div([
                            html.Div([ #blank column
                        ],
                            className='col-1'
                        ),
                            dcc.Markdown('''This page displays statewide cannabis data. Please use nav links to explore date further by county.''',
                            style={'color': 'white'})
                        ],
                            className='row'
                        ),
                    ],
                        className='col-5'
                    ),
                    # html.Div([
                    #     html.H6('Total Revenue Since 2014')
                    # ],
                    #     className='col-3'
                    # ),
                ],
                    className='row'
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='hp-map')
                    ],
                        className='col-6'
                    ),
                    html.Div([
                        dcc.Graph(figure=fig_tot_rev)
                    ],
                        className='col-6'
                    ),
                ],
                    className='row'
                ),
                get_emptyrow(),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Markdown('''Counties where cannabis sales are legal as of 2020 are shaded in green.''',
                            style={'color':'white'}),
                        ],
                            className='row'
                        ),
                        html.Div([
                            dcc.Markdown('''Graph below shows county per capita revenue and population growth changes since 2014, with the bubble sizes showing relative total population. Large per capita revenue values suggest tourism may be an important factor in a particular county's cannabis industry.''',
                            style={'color':'white'}),
                        ],
                            className='row'
                        ),
                    ],
                        className='col-7'
                    ),
                    html.Div([
                        dcc.Markdown('''Bar chart above shows total revenue for the entire state, with the last bar showing reported revenue at the current time in black, and projected revenue for the entire year in red. Projected revenue is based on comparison of reported revenue for current year with the same period last year, and using the percentage difference to projec the remaining months.''',
                        style={'color':'white'})
                    ],
                        className='col-5'
                    ),
                ],
                    className='row'
                ),
                get_emptyrow(),
                html.Div([
                    # html.Div([
                    # ],
                    #     className='col-2'
                    # ),
                    html.Div([
                        dcc.Graph(figure=fig)
                    ],
                        className='col-12'
                    ),
                    # html.Div([
                    #     dcc.Markdown('''Graph at left shows county per capita revenue and population growth changes since 2014, with the bubble sizes showing relative total population. Large per capita revenue values suggest tourism may be an important factor in a particular county's cannabis industry. As Arizona and New Mexico legalized recrational cannabis industries ramp up, it will be interesting to see the effects on revenue of counties which border these states in the near future, as they generally have high per capita revenue. ''',
                    #     style={'color': 'white'})
                    # ],
                    #     className='col-4'
                    # ),
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
                className = 'col-1', # Blank 1 column
            ),
        ],
        className='row',
        style=externalgraph_rowstyling, # External row
        ),
        
        html.Div([
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,
                n_intervals=0
            )
        ]),
        html.Div(id='pl-data', style={'display': 'none'}),
    ])


app.layout = home_page_App

