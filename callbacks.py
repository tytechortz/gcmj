import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import os
from dash.dependencies import Input, Output, State
from app import app
from data import df_revenue, sources, df_rev, df_biz, categories_table, text, df_bidness, df_pc, df_pop
from dotenv import load_dotenv
import plotly.graph_objs as go
from apps.revenue import month_values

load_dotenv()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#########################################################
#PL REV Callbacks
#########################################################

@app.callback(
     Output('plrev-map', 'figure'),
     Input('pl-data', 'children'))         
def update_lic_map(data):
    
    df_year = df_pc.loc[df_pc['year'] == 2019]
    df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'revenue per cap.': df_year.pc_rev,'CENT_LAT':df_year.CENT_LAT,
                         'CENT_LON':df_year.CENT_LONG, 'marker_size':.5})

    df_smr_filtered = df_smr.loc[df_year['color'] == 'red']
    
    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]
    data = [dict(
        lat = df_smr['CENT_LAT'],
        lon = df_smr['CENT_LON'],
        text = df_smr['county'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        customdata = df_smr['county'],
        marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
        )]
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39.05, lon=-105.5),
                zoom = 5.85,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 450,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
    Output('pl-data', 'children'),
    Input('pl-data', 'children'))
def pl_rev_data(value):
    df_year = df_pc.loc[df_pc['year'] == 2019]
    # print(df_year)
    # df_rank = df.year.sort_values('tot_sales')
    # print(df_rank)
    df_cbc = df_biz.groupby(['County'], as_index=False)['License_No'].count()
    df_cbc = df_cbc.rename(columns={'License_No':'lic_count'})
    df_combo = pd.merge(df_year, df_cbc, how='left', left_on=['county'], right_on=['County'])
    df_combo['rpl'] = df_combo['tot_sales'] / df_combo['lic_count']
    df_combo.fillna(0, inplace=True)
    # print(df_combo)
    rev_max = df_combo['rpl'].max()
    rev_min = 0

    def get_color(x):
        if x == 0:
            return 'white'
        elif 0 < x <= 250000 :
            return 'greenyellow'
        elif 250000 < x <= 500000:
            return 'lightgreen'
        elif 500000 < x <= 1000000:
            return 'limegreen'
        elif 1000000 < x <= 1500000:
            return 'forestgreen'
        else:
            return 'darkgreen'

    df_combo['color'] = df_combo['rpl'].map(get_color)
    pd.set_option('display.max_rows', None)
    # print(df_combo)

    df_white_counties = df_combo.loc[df_combo['color'] == 'white']
    white_counties = df_white_counties['county'].unique().tolist()
    df_gy_counties = df_combo.loc[df_combo['color'] == 'greenyellow']
    pg_counties = df_gy_counties['county'].unique().tolist()
    df_lg_counties = df_combo.loc[df_combo['color'] == 'lightgreen']
    lg_counties = df_lg_counties['county'].unique().tolist()
    df_lime_counties = df_combo.loc[df_combo['color'] == 'limegreen']
    lime_counties = df_lime_counties['county'].unique().tolist()
    df_forest_counties = df_combo.loc[df_combo['color'] == 'forestgreen']
    forest_counties = df_forest_counties['county'].unique().tolist()
    df_dark_counties = df_combo.loc[df_combo['color'] == 'darkgreen']
    dark_counties = df_dark_counties['county'].unique().tolist()
    # print(lg_counties)

    def fill_color():
        for k in range(len(sources)):
            if sources[k]['features'][0]['properties']['COUNTY'] in white_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'white'
            elif sources[k]['features'][0]['properties']['COUNTY'] in pg_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'greenyellow'
            elif sources[k]['features'][0]['properties']['COUNTY'] in lg_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'lightgreen'
            elif sources[k]['features'][0]['properties']['COUNTY'] in lime_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'limegreen'
            elif sources[k]['features'][0]['properties']['COUNTY'] in forest_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'forestgreen'  
            else:
                sources[k]['features'][0]['properties']['COLOR'] = 'darkgreen'              
    fill_color()

    return df_combo.to_json()

@app.callback(
     Output('pl-info', 'children'),
     [Input('plrev-map', 'clickData'),
     Input('pl-data', 'children')])
def display_per_lic_rev(clickData, pl_data):
    df = pd.read_json(pl_data)
    county = clickData['points'][-1]['text']
    
    df_rank = df.sort_values(by=['rpl'], ascending=False)
    df_rank.reset_index(inplace=True)
    
    rpl_rank_2019 = df_rank[df_rank['county'] == county].index[0] + 1
   
    df_rev = df_revenue[df_revenue['county'] == county]
    df_rev = df_rev[df_rev['year'] < 2021]
   
    df_pcrev = df_pc[df_pc['county'] == county]
    
    df_bpc = df_biz[df_biz['County'] == county]
    
    biz_count  = len(df_bpc.index)
    county_2019 = df_pcrev.loc[df_pcrev['year'] == 2019]
 
    total_rev_2019 = int(county_2019['tot_sales'])
    rpl_2019 = int(total_rev_2019 / biz_count)
   
    county_2020 = df_rev.loc[df_rev['year'] == 2020]
    total_rev_2020 = int(county_2020['tot_sales'])
    rev_change = (total_rev_2020 - total_rev_2019) / total_rev_2019

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6('{} COUNTY'.format(county), style={'text-align': 'center', 'color': 'white'}),
                        ],
                            className='col-12'
                        ),
                    ],
                        className=('row')
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Total Revenue in 2019',
                            style={'color': 'white'}),
                        ],
                            className='col-6'
                        ),
                        html.Div([
                            html.H6('${:,}'.format(total_rev_2019), style={'text-align': 'right', 'color': 'white'}),
                        ],
                            className='col-6'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('2019 License Count',
                            style={'color': 'white'}),
                        ],
                            className='col-6'
                        ),
                        html.Div([
                            html.H6('{}'.format(biz_count), style={'text-align': 'right','color': 'white'}),
                        ],
                            className='col-6'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Revenue Per License', style={'text-align': 'left','color': 'white'}),
                        ],
                            className='col-6'
                        ),
                        html.Div([
                            html.H6('${:,}'.format(rpl_2019), style={'text-align': 'right','color': 'white'}),
                        ],
                            className='col-6'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Revenue Per License Rank', style={'text-align': 'left','color': 'white'}),
                        ],
                            className='col-6'
                        ),
                        html.Div([
                            html.H6('{}'.format(rpl_rank_2019), style={'text-align': 'right','color': 'white'}),
                        ],
                            className='col-6'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Total Revenue in 2020',
                            style={'color': 'white'}),
                        ],
                            className='col-6'
                        ),
                        html.Div([
                            html.H6('${:,}'.format(total_rev_2020), style={'text-align': 'right','color': 'white'}),
                        ],
                            className='col-6'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Revenue Change 2019 to 2020',
                            style={'color': 'white'}),
                        ],
                            className='col-7'
                        ),
                        html.Div([
                            html.H6('{:.0%}'.format(rev_change), style={'text-align': 'right','color': 'white'}),
                        ],
                            className='col-5'
                        ),
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),
            ],
                className='pretty_container'
            ),
        ],
            className='col-12'
        ),
    ],
        className='row'
    ),

#########################################################
#PC REV Callbacks
#########################################################


@app.callback(
     Output('pcrev-map', 'figure'),
     Input('year', 'value'))         
def update_rev_map(selected_year):
   
    year1 = selected_year
    
    df_year = df_pc.loc[df_pc['year'] == selected_year]
    df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'revenue per cap.': df_year.pc_rev,'CENT_LAT':df_year.CENT_LAT,
                         'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.pc_rev)*(.5**4)})

    df_smr_filtered = df_smr.loc[df_year['color'] == 'red']

    color_counties = df_smr_filtered['county'].unique().tolist()
     
    def fill_color():
        for k in range(len(sources)):
            if sources[k]['features'][0]['properties']['COUNTY'] in color_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'lightgreen'
            else: sources[k]['features'][0]['properties']['COLOR'] = 'white'                 
    fill_color()
    
    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]
    data = [dict(
        lat = df_smr['CENT_LAT'],
        lon = df_smr['CENT_LON'],
        text = df_smr['county'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        #    customdata = df['uid'],
        marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
        )]
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39.05, lon=-105.5),
                zoom = 5.85,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 450,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
     Output('per-cap-rev-bar', 'figure'),
     [Input('pcrev-map', 'clickData'),
     Input('year2', 'value')])
def display_cnty_pop(clickData, selected_year):
    county = clickData['points'][-1]['text']
    df_rev = df_revenue[df_revenue['county'] == county]
    df_rev = df_rev[df_rev['year'] < 2021]
    # print(df_pc)
    df_pcrev = df_pc[df_pc['county'] == county]

    df_county_pop = df_pop[df_pop['county'] == county]
    df_county_pop = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]


    fig = go.Figure(
        data=[
        #    go.Bar(
        #         name='Annual Revenue',
        #         x=df_rev['year'],
        #         y=df_rev['tot_sales'],
        #         yaxis='y',
        #         # offsetgroup=1
        #    ),
            go.Scatter(
                name='Population',
                x=df_county_pop['year'],
                y=df_county_pop['totalpopulation'],
                yaxis='y2',
                # offsetgroup=2
            ),
            go.Bar(
                name='Per Cap Revenue',
                x=df_pcrev['year'],
                y=df_pcrev['pc_rev'],
                yaxis='y',
                # offsetgroup=1
            ),
        #    go.Bar(
        #         name='Business Count',
        #         x=df_biz_count['year'],
        #         y=df_biz_count['licensee'],
        #         yaxis='y2',
        #         offsetgroup=2
        #    ),
        ],
        layout={
            'yaxis': {'title': 'Per Cap Revenue'},
            'yaxis2': {'title': 'Population', 'overlaying': 'y', 'side': 'right'},
            'height': 350,
        }
    )
    
    fig.update_layout(
        barmode='group',
        title={
            'text':'{} COUNTY'.format(county),
            'x':0.5,
            'xanchor':'center'
        }
    )
   
    return fig

@app.callback(
     Output('pc-info', 'children'),
     [Input('pcrev-map', 'clickData'),
     Input('year2', 'value')])
def display_per_cap_info(clickData, year):
    county = clickData['points'][-1]['text']
    year1 = year[0]
    year2 = year[1]
    df_rev = df_revenue[df_revenue['county'] == county]
    df_rev = df_rev[df_rev['year'] < 2021]
    # print(df_rev)
    df_rev = df_rev[df_rev['tot_sales'] != 0]
    # print(df_rev)
    rev_start_year = df_rev['year'].iloc[0]
    # print(rev_start_year)
    df_pcrev = df_pc[df_pc['year'] == 2020]
    # print(df_pcrev)
    df_cnty_pc_rev = df_pcrev[df_pcrev['county'] == county]
    # print(df_cnty_pc_rev)
    
    pcrev = df_cnty_pc_rev.iloc[0]['pc_rev']
    # print(pcrev)
    df_per_cap_rank = df_pcrev.sort_values(by=['pc_rev'], ascending=False)
    df_per_cap_rank.reset_index(inplace=True)
    # print(df_per_cap_rank)
    pc_rev_rank_2020 = df_per_cap_rank[df_per_cap_rank['county'] == county].index[0] + 1
    # print(pc_rev_rank_2020)

    df_county_pop = df_pop[df_pop['county'] == county]
    df_county_pop = df_county_pop[(df_county_pop['year'] >= year1) & (df_county_pop['year'] <= year2)]
    # print(df_county_pop)
    pop1 = df_county_pop['totalpopulation'].iloc[0]
    pop2 = df_county_pop['totalpopulation'].iloc[-1]
    pop_change = (pop2 - pop1) / pop1
    # print(pop_change)
    # print(df_pop)
    df_2020_pop = df_pop[df_pop['year'] == 2020]
    df_2020_pop.rename(columns={'totalpopulation':'2020_pop'}, inplace=True)
    df_2050_pop = df_pop[df_pop['year'] == 2050]
    df_2050_pop.rename(columns = {'totalpopulation':'2050_pop'}, inplace=True)
    # print(df_2050_pop)
    df_pop_change = pd.merge(df_2020_pop, df_2050_pop, how='left', left_on='county', right_on='county')
    df_pop_change['pop_change'] = df_pop_change['2050_pop'] - df_pop_change['2020_pop']
    # print(df_pop_change)
    df_pop_change_rank = df_pop_change.sort_values(by=['pop_change'], ascending=False)
    df_pop_change_rank.reset_index(inplace=True)
    pop_change_rank = df_pop_change_rank[df_pop_change_rank['county'] == county].index[0] + 1


    df1 = df_rev[df_rev['year'] == rev_start_year]
    # df2 = df_rev['tot_sales'].iloc[-1]
    # print(df1)
    # print(df2)
    # df2 = df_rev[df_rev['year'] == year2]
    rev1 = df1['tot_sales'].iloc[0]
    rev2 = df_rev['tot_sales'].iloc[-1]
    rev_year2 = df_rev['year'].iloc[-1]
    # rev2 = df2['tot_sales'].iloc[0]
    # print(rev1)
    # print(rev2)
    change = (rev2 - rev1) / rev1
    # print(change)


    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H6('Data for {} County'.format(county), style={'text-align': 'center','color': 'white'}),
                        ],
                            className='col-12'
                        ),
                    ],
                        className=('row')
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Revenue Change {}-{}'.format(rev_start_year, rev_year2),style={'color': 'white'}),
                        ],
                            className='col-9'
                        ),
                        html.Div([
                            html.H6('{:.0%}'.format(change), style={'text-align': 'right', 'color':'white'}),
                        ],
                            className='col-3'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Pop. Change {}-{}'.format(year1, year2),style={'color': 'white'}),
                        ],
                            className='col-10'
                        ),
                        html.Div([
                            html.H6('{:.0%}'.format(pop_change), style={'text-align': 'right', 'color':'white'}),
                        ],
                            className='col-2'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Per Capita Revenue in 2020', style={'text-align': 'left', 'color':'white'}),
                        ],
                            className='col-9'
                        ),
                        html.Div([
                            html.H6('${:.0f}'.format(pcrev), style={'text-align': 'right', 'color':'white'}),
                        ],
                            className='col-3'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('2020 Per Capita Revenue Rank', style={'text-align': 'left', 'color':'white'}),
                        ],
                            className='col-10'
                        ),
                        html.Div([
                            html.H6('{}'.format(pc_rev_rank_2020), style={'text-align': 'right', 'color':'white'}),
                        ],
                            className='col-2'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.H6('Proj. Pop. Growth Rank',style={'color': 'white'}),
                        ],
                            className='col-10'
                        ),
                        html.Div([
                            html.H6('{:,}'.format(pop_change_rank), style={'text-align': 'right', 'color':'white'}),
                        ],
                            className='col-2'
                        ),
                    ],
                        className='row'
                    ),
        #             html.Div([
        #                 html.Div([
        #                     html.H6('Revenue Change 2019 to 2020'),
        #                 ],
        #                     className='six columns'
        #                 ),
        #                 html.Div([
        #                     html.H6('{:.0%}'.format(rev_change), style={'text-align': 'right'}),
        #                 ],
        #                     className='six columns'
        #                 ),
                    # ],
                    #     className='row'
                    # ),
                ],
                    className='round1'
                ),
            ],
                className='pretty_container'
            ),
        ],
            className='col-12'
        ),
    ],
        className='row'
    ),

#########################################################
#Business Callbacks
#########################################################

@app.callback(
    Output('biz-map', 'figure'),
    Input('categories', 'value'))
def update_biz_map(selected_values):
    # print(df_biz)
    # print(df_biz.columns)
    # print(df_biz['License_No'])
    df1 = pd.DataFrame(df_biz.loc[df_biz['Category'] == selected_values])
   
    if selected_values == 'all':
        filtered_df = df_biz
        data = [dict(
            lat = df_biz['lat'],
            lon = df_biz['long'],
            text = text,
            hoverinfo = 'text',
            type = 'scattermapbox',
            customdata = df_biz['uid'],
            marker = dict(size=10,color=df_biz['color'],opacity=.6)
        )]
    else: 
        filtered_df = df1
        data = [dict(
            lat = filtered_df['lat'],
            lon = filtered_df['long'],
            text = text,
            hoverinfo = 'text',
            type = 'scattermapbox',
            customdata = df1['uid'],
            marker = dict(size=7,color=df1['color'],opacity=.6)
        )]

    def fill_color():
        for k in range(len(sources)):
            sources[k]['features'][0]['properties']['COLOR'] = 'white'                 
    fill_color()

    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]
    
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39, lon=-105.5),
                # zoom = 5.6,
                zoom = 6,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 500,
            margin = dict(r=0, l=0, t=0, b=0),
            clickmode = 'event+select'
        )  
  
    fig = dict(data=data, layout=layout)
    return fig

######################################################
#REVENUE CALLBACKS
######################################################


@app.callback(
     Output('revenue-map', 'figure'),
     Input('year', 'value'))         
def update_rev_map(selected_year):
   
    year1 = selected_year
  
    df_year = df_revenue.loc[df_revenue['year'] == selected_year]
    df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'total revenue': df_year.tot_sales,'CENT_LAT':df_year.CENT_LAT,
                    'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.tot_sales)*(.35**14)})

    df_smr_filtered = df_smr.loc[df_year['color'] == 'red']

    color_counties = df_smr_filtered['county'].unique().tolist()
     
    def fill_color():
        for k in range(len(sources)):
            if sources[k]['features'][0]['properties']['COUNTY'] in color_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'lightgreen'
            else: sources[k]['features'][0]['properties']['COLOR'] = 'white'                 
    fill_color()
    
    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]
    data = [dict(
        lat = df_smr['CENT_LAT'],
        lon = df_smr['CENT_LON'],
        text = df_smr['county'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        #    customdata = df['uid'],
        marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
        )]
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39.05, lon=-105.5),
                zoom = 5.85,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 450,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
    Output('rev-scatter', 'figure'),
    [Input('revenue-map', 'clickData'),
    Input('year','value'),
    Input('rev', 'value')])
def create_rev_scat(clickData,year,rev):
    year_df = df_rev[df_rev['year'] == str(year)]

    filtered_df = year_df[year_df['county'] == clickData['points'][-1]['text']]
    
    filtered_df = filtered_df.sort_values('month')
   
    labels = ['Feb', 'Apr', 'Jun','Aug','Oct','Dec']
    tickvals = [2,4,6,8,10,12]
    traces = []

    if 'TOTAL' in rev:
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['tot_sales'],
            name = 'Total Sales',
            line = {'color':'red'} 
            ))
    if 'REC' in rev:  
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['rec_sales'],
            name = 'Rec Sales',
            line = {'color':'dodgerblue'}
            ))
    if 'MED' in rev:  
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['med_sales'],
            name = 'Med Sales',
            line = {'color':'black'}
            ))

    return {
            'data': traces,
            'layout': go.Layout(
                xaxis = {'title': 'Month','tickvals':tickvals,'tickmode': 'array','ticktext': labels},
                yaxis = {'title': 'Revenue'},
                hovermode = 'closest',
                title = '{} COUNTY {} REVENUE - {}'.format(clickData['points'][-1]['text'],rev,year),
                height = 350,
                font = {'size': 8}
            )
        }

@app.callback(
    Output('crat', 'children'),
    Input('revenue-map', 'clickData'))
def clean_crat(clickData):
    county_revenue_df = df_rev.groupby(['county', 'year'])
    crat = county_revenue_df.sum()
    crat.reset_index(inplace=True)
    
    return crat.to_json()

@app.callback(
    Output('month-rev-bar', 'figure'),
    [Input('revenue-map', 'clickData'),
    Input('month', 'value'),
    Input('crat', 'children'),
    Input('month-year', 'value')])         
def create_month_bar(clickData, month, crat, mo_yr):
    crat = pd.read_json(crat)
    crat.reset_index(inplace=True)
    df = df_rev
    filtered_county = clickData['points'][-1]['text']
  
    county_rev = df[df['county'] == filtered_county]

    county_rev_month = county_rev.groupby(['month'], as_index=False)['tot_sales'].sum()

    crm = county_rev[county_rev['month'] == month]
    
    if mo_yr == 'yr':
        trace1 = [
            {'y': county_rev_month['tot_sales'], 'x': county_rev_month['month'], 'type': 'bar', 'name': 'month'}
        ]

        return {
            'data': trace1,
            'layout': go.Layout(
                height = 350,
                title = 'ANNUAL {} COUNTY REVENUE'.format(clickData['points'][-1]['text']),
                font = {'size': 8}
            ),
        }

    elif mo_yr == 'mo':
        trace1 = [
            {'y': crm['tot_sales'], 'x': crm['year'], 'type': 'bar', 'name': 'month'}
        ]
    
        return {
            'data': trace1,
            'layout': go.Layout(
                height = 350,
                title = '{} COUNTY REVENUE FOR {}'.format(clickData['points'][-1]['text'], month_values[month]),
                font = {'size': 8}
            ),
        }


@app.callback(
    Output('rev-bar', 'figure'),
    [Input('revenue-map', 'clickData'),
    Input('crat', 'children')])         
def create_month_bar(clickData, crat):
    # print(clickData)
    # print(df_revenue.head())
    crat = pd.read_json(crat)
    crat.reset_index(inplace=True)
    # print(crat)
    filtered_county = crat['county'] ==  clickData['points'][-1]['text']
    # # print(filtered_county)
    selected_county = crat[filtered_county]
    # selected_county.reset_index(inplace=True)
    # print(selected_county)

    trace1 = [
        {'x': selected_county['year'], 'y': selected_county['med_sales'], 'type': 'bar', 'name': 'Med Sales' },
        {'x': selected_county['year'], 'y': selected_county['rec_sales'], 'type': 'bar', 'name': 'Rec Sales' },
        {'x': selected_county['year'], 'y': selected_county['tot_sales'], 'type': 'bar', 'name': 'Tot Sales' },
    ]

    
    return {
        'data': trace1,
        'layout': go.Layout(
            height = 350,
            title = '{} COUNTY REVENUE BY YEAR'.format(clickData['points'][-1]['text']),
            font = {'size': 8}
        ),
    }