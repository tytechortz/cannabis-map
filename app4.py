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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
counties.sort_values(by=['US_FIPS'])
pop_rev = gpd.read_file('./per_cap_joined.geojson')
# per_rev = pd.read_csv('./revenue_pop_data.csv',header=0, delim_whitespace=False)
rpd = pop_rev.set_index('COUNTY', drop=False)
df = gpd.read_file('./cannabis_business.geojson')
df_revenue = pd.read_csv('https://data.colorado.gov/resource/j7a3-jgd3.csv?$limit=5000&$$app_token=Uwt19jYZWTc9a2UPr7tB6x2k1')
df_taxes = pd.read_csv('https://data.colorado.gov/resource/3sm5-jtur.csv')
df_biz = pd.read_csv('https://data.colorado.gov/resource/sqs8-2un5.csv')


df_revenue['county'] = df_revenue['county'].str.upper()


df_revenue.fillna(0, inplace=True)
df_revenue['tot_sales'] = df_revenue['med_sales'] + df_revenue['rec_sales']
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'

with open('./Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)
    
sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})

# counties_s = counties.sort_values(by=['US_FIPS'])
dfinal = df_revenue.merge(counties, how='inner', left_on='county', right_on='COUNTY')

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

body = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div(
                className='app-header',
                children=[
                    html.Div('COLORADO CANNABIS', className="app-header--title"),
                ]
            ),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                className='map-radio',
                children=[ 
                    dcc.RadioItems(id='map-radio', options=[
                        {'label':'Revenue Map', 'value':'rev-map'},
                        {'label':'Business Map','value':'biz-map'},
                    ],
                labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1},
                value = 'rev-map'
                    ),
                ]
            ),
            width = {'size': 4, 'offset':5}
        ),
    ]),
    html.Div(id='biz-stuff'),
    html.Div(id='rev-stuff'),
        # html.Div(id='output-biz-data')              
])

@app.callback(
            Output('biz-stuff', 'children'),
            [Input('map-radio', 'value')])
def display_biz_page(selected_values):
    biz_page = []
    if selected_values == 'biz-map':
        biz_page.append(
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Div(html.Button('All License Types',id='button-all', n_clicks=0)),
                        html.Div(html.Button('Transporters', id='button-transporters', n_clicks=0)),
                        html.Div(html.Button('Center', id='button-center', n_clicks=0)),
                        html.Div(html.Button('Cultivator', id='button-cultivator', n_clicks=0)),
                        html.Div(html.Button('Infused Product Manufacturer', id='button-ipm', n_clicks=0)),
                        html.Div(html.Button('R&D Cultivation', id='button-rdc', n_clicks=0)),
                        html.Div(html.Button('Retail Operator', id='button-operator', n_clicks=0)),
                        html.Div(html.Button('Testing Facility', id='button-testing', n_clicks=0)),
                        html.Div(html.Button('Retail Marijuana Product Manufacturer', id='button-rmpm', n_clicks=0)),
                        html.Div(html.Button('Retail Cultivator', id='button-ret-cult', n_clicks=0)),
                        html.Div(html.Button('Retail Testing Facility', id='button-ret-test', n_clicks=0)),
                        html.Div(html.Button('Retail Transporter', id='button-ret-trans', n_clicks=0)),
                        html.Div(html.Button('Retail Marijuana Store', id='button-ret-store', n_clicks=0)),
                    ]),
                    width = {'size':2}
                ),
                dbc.Col(
                    dcc.Graph(id='map',
                    config={
                        'scrollZoom': True
                    }),
                    width={'size':6},
                ),
                dbc.Col(
                        html.Div([
                            html.Table ([
                                html.Tr([html.Th('Business Info')]),
                                html.Tr(html.Div(id='lic-name', style={'height':30, 'text-align': 'left'})),
                                html.Tr(html.Div(id='biz-name', style={'height':30, 'text-align': 'left'})),
                                html.Tr(html.Div(id='biz-type', style={'height':30, 'text-align': 'left'})),
                                html.Tr(html.Div(id='city', style={'height':30, 'text-align': 'left'})),
                                html.Tr(html.Div(id='address', style={'height':30, 'text-align': 'left'})),
                                html.Tr(html.Div(id='lic-num', style={'height':30, 'text-align': 'left'})),
                            ]),
                        ],
                        style = {'overflow-x':'scroll'}
                        ),   
                    width = {'size':4}
                ),
            ]),
        )  
        return biz_page

@app.callback(
            Output('rev-stuff', 'children'),
            [Input('map-radio', 'value')])
def display_rev_page(selected_values):
    rev_page = []
    if selected_values == 'rev-map':
        rev_page.append(
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='rev-map',
                    config={
                        'scrollZoom': True
                    }),
                    width={'size':8, 'offset':2},
                ),
            ]),
        )  
        return rev_page













app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(port=8024, debug=True)