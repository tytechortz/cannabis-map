import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import geopandas as gpd 
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import json
import numpy as np
from dash.dependencies import Input, Output, State
import dash_daq as daq
import os
import config

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

counties = gpd.read_file('./Data/Colorado_County_Boundaries.geojson')
counties.sort_values(by=['US_FIPS'])
pop_rev = gpd.read_file('./Data/per_cap_joined.geojson')
per_rev = pd.read_csv('./Data/revenue_pop_data.csv',header=0, delim_whitespace=False)
rpd = pop_rev.set_index('COUNTY', drop=False)
# print(rpd)
df = gpd.read_file('./Data/cannabis_business.geojson')
df_revenue = pd.read_csv('https://data.colorado.gov/resource/j7a3-jgd3.csv?$limit=5000&$$app_token='+ config.state_data_token)
df_biz = pd.read_csv('https://data.colorado.gov/resource/sqs8-2un5.csv?$select=Category,License_No,Month,Year&$limit=166000&$$app_token='+ config.state_data_token)

# print(df_biz)
df_revenue['county'] = df_revenue['county'].str.upper()

df_revenue.fillna(0, inplace=True)
df_revenue['tot_sales'] = df_revenue['med_sales'] + df_revenue['rec_sales']
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'

# print(df_revenue)

with open('./Data/Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)
    
sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})

# dfinal = df_revenue.merge(counties, how='inner', left_on='county', right_on='COUNTY')

county_revenue_df = df_revenue.groupby(['county', 'year'])
crat = county_revenue_df.sum()
crat.reset_index(inplace=True)

color_list = ['purple', 'darkblue', 'dodgerblue', 'darkgreen','black','lightgreen','yellow','orange', 'darkorange','red','darkred','violet']

text=[]
i=0
while i < len(df):
    text.append(df['Licensee'][i])
    i += 1

conditions = [
    df['Category'] == 'MED Licensed Transporters',
    df['Category'] == 'MED Licensed Center',
    df['Category'] == 'MED Licensed Cultivator',
    df['Category'] == 'MED Licensed Infused Product Manufacturer',
    df['Category'] == 'MED Licensed R&D Cultivation',
    df['Category'] == 'MED Licensed Retail Operator',
    df['Category'] == 'MED Licensed Testing Facility',
    df['Category'] == 'MED Licensed Retail Marijuana Product Manufacturer',
    df['Category'] == 'MED Licensed Retail Cultivator',
    df['Category'] == 'MED Licensed Retail Testing Facility',
    df['Category'] == 'MED Licensed Retail Transporter',
    df['Category'] == 'MED Licensed Retail Marijuana Store',
]

df['color'] = np.select(conditions, color_list)

categories = []
for i in df['Category'].unique():
    categories.append(i)

categories_table = pd.DataFrame({'Category':df['Category'].unique()})

colors = dict(zip(categories, color_list))

def get_layout():
    return html.Div(
        [
            html.Div([
                html.H2(
                    'COLORADO CANNABIS',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.H6('Business Data',style={'text-align':'right'})
                ],
                    className='five columns'
                ),
                html.Div([
                    daq.ToggleSwitch(
                        id='rev-biz-switch',
                        value=True
                    )
                ],
                    className='two columns'
                ),
                html.Div([
                    html.H6('Revenue Data', style={'text-align':'left'})
                ],
                    className='five columns'
                ),
            ],
                className='row'
            ),
            html.Div(id='revenue'),
            html.Div(id='biz')
        ]
    )

@app.callback(
    Output('revenue', 'children'),
    [Input('rev-biz-switch', 'value')])
def revenue_layout(value):
    if value == True:
        return html.Div([
            html.Div([
                html.Div([
                    html.Div('hello world', style={'text-align':'center'})
                ],
                    className='seven columns'
                ),
                
            ],
                className='row'
            ),
        ])

@app.callback(
    Output('biz', 'children'),
    [Input('rev-biz-switch', 'value')])
def revenue_layout(value):
    if value == False:
        return html.Div([
            html.Div([
                html.Div([
                    html.Div('goodbye world', style={'text-align':'center'})
                ],
                    className='seven columns'
                ),
                
            ],
                className='row'
            ),
        ])




app.layout = get_layout
if __name__ == "__main__":
    app.run_server(port=8050, debug=False)
