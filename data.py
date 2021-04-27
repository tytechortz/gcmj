import pandas as pd
import geopandas as gpd
from sodapy import Socrata
import json
from datetime import datetime
import numpy as np
import config

today = datetime.today()
current_year = today.year

client = Socrata("data.colorado.gov", None)


# initial data fetch
mj_results = client.get("j7a3-jgd3", limit=6000)
pop_results = client.get("q5vp-adf3", limit=381504)

# revenue data
df_rev = pd.DataFrame.from_records(mj_results)
df_rev['county'] = df_rev['county'].str.upper()
df_rev.fillna(0, inplace=True)
df_rev['med_sales'] = df_rev['med_sales'].astype(int)
df_rev['rec_sales'] = df_rev['rec_sales'].astype(int)
df_rev['tot_sales'] = df_rev['med_sales'] + df_rev['rec_sales']
df_rev['month'] = df_rev['month'].astype(int)
# print(df_rev.head())
# df_cnty_rev = df_rev.groupby(['county', 'year'])
# crat = df_cnty_rev.sum()
# print(crat)
df_revenue = df_rev.groupby(['year', 'county']).agg({'tot_sales': 'sum'})
df_revenue = df_revenue.reset_index()
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'
df_revenue['year'] = df_revenue['year'].astype(int)
# print(df_revenue)

counties = gpd.read_file('./data/Colorado_County_Boundaries.geojson')
# print(counties)
df_lat_lon = counties[['COUNTY', 'CENT_LAT', 'CENT_LONG']]
# merge revenue and county boundaries 
df_revenue = pd.merge(df_revenue, df_lat_lon, how='left', left_on=['county'], right_on=['COUNTY'])

with open('./data/Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)

sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})


#Population data ##################################################
df_pop = pd.DataFrame.from_records(pop_results)
df_pop['totalpopulation'] = df_pop['totalpopulation'].astype(int)
df_pop = df_pop.drop(['age', 'malepopulation', 'femalepopulation'], axis=1)
df_pop = df_pop.groupby(['year', 'county'], as_index=False)['totalpopulation'].sum()
df_pop['county'] = df_pop['county'].str.upper()
df_pop['year'] = df_pop['year'].astype(int)
df_pop_pc = df_pop[(df_pop['year'] >= 2014) & (df_pop['year'] < current_year)]

#Per capita data ##################################################
df_rev_pc = df_revenue[(df_revenue['year'] >= 2014) & (df_revenue['year'] < current_year)]
# print(df_rev_pc)
df_pc = pd.merge(df_rev_pc, df_pop, how='left', left_on=['county', 'year'], right_on=['county', 'year'])

df_pc['pc_rev'] = df_pc['tot_sales'] / df_pc['totalpopulation']

df_pc.loc[df_pc['tot_sales'] > 0, 'color'] = 'red'
df_pc.loc[df_pc['tot_sales'] == 0, 'color'] = 'blue'

#Business Data ###############################################
# df_biz = gpd.read_file('./Data/cannabis_business.geojson')
df_biz = pd.read_csv('./Data/CO_mj_biz_loc.csv')

df_biz['County'] = df_biz['County'].str.upper()
# export_csv = df_biz.to_csv(r'./New_Products.csv', index = None, header=True)
# print(df_biz)
color_list = ['purple', 'darkblue', 'dodgerblue', 'darkgreen','black','lightgreen','yellow','orange', 'darkorange','red','darkred','violet']

text=[]
i=0
while i < len(df_biz):
    text.append(df_biz['Licensee'][i])
    i += 1

conditions = [
    df_biz['Category'] == 'MED Licensed Transporters',
    df_biz['Category'] == 'MED Licensed Center',
    df_biz['Category'] == 'MED Licensed Cultivator',
    df_biz['Category'] == 'MED Licensed Infused Product Manufacturer',
    df_biz['Category'] == 'MED Licensed R&D Cultivation',
    df_biz['Category'] == 'MED Licensed Retail Operator',
    df_biz['Category'] == 'MED Licensed Testing Facility',
    df_biz['Category'] == 'MED Licensed Retail Marijuana Product Manufacturer',
    df_biz['Category'] == 'MED Licensed Retail Cultivator',
    df_biz['Category'] == 'MED Licensed Retail Testing Facility',
    df_biz['Category'] == 'MED Licensed Retail Transporter',
    df_biz['Category'] == 'MED Licensed Retail Marijuana Store',
]

df_biz['color'] = np.select(conditions, color_list)

categories = []
for i in df_biz['Category'].unique():
    categories.append(i)

categories_table = pd.DataFrame({'Category':df_biz['Category'].unique()})

df_bidness = pd.read_csv('https://data.colorado.gov/resource/sqs8-2un5.csv?$select=Category,Licensee,License_No,Month,Year&$limit=400000&$$app_token='+ config.state_data_token)
# print(df_bidness)