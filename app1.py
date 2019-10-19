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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True

counties = gpd.read_file('./Data/Colorado_County_Boundaries.geojson')
counties.sort_values(by=['US_FIPS'])
pop_rev = gpd.read_file('./Data/per_cap_joined.geojson')
per_rev = pd.read_csv('./Data/revenue_pop_data.csv',header=0, delim_whitespace=False)
rpd = pop_rev.set_index('COUNTY', drop=False)
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
                    html.H6('Revenue Data',id='rev-title', style={'text-align':'right'})
                ],
                    className='five columns'
                ),
                html.Div([
                    daq.ToggleSwitch(
                        id='rev-biz-switch',
                        value=True, 
                    ),
                ],
                    className='two columns'
                ),
                html.Div([
                    html.H6('Business Data',id='biz-title', style={'text-align':'left'})
                ],
                    className='five columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(
                        id='map'
                    ),
                ],
                    className='eight columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div(id='rev-map-year-slider')
            ],
                className='row'
            ),
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(
    Output('map', 'children'),
    [Input('rev-biz-switch', 'value')])
def display_graph(value):
    print(value)
    if value == True:
        return dcc.Graph(id='rev-map')
    elif value == False:
        return dcc.Graph(id='biz-map')

@app.callback(
            Output('rev-map-year-slider', 'children'),
            [Input('rev-biz-switch', 'value')])         
def update_figure(value):
    if value == True:
        return dcc.Slider(
                    id='year-selector',
                        min = 2014,
                        max = 2018,
                        marks={i: '{}'.format(i) for i in range(2014,2019)}, 
                        step = 1,
                        value = 2014,
                        vertical = False,
                        updatemode = 'drag'
                    )

@app.callback(
            Output('rev-map', 'figure'),
            [Input('rev-biz-switch', 'value'),
            Input('year-selector', 'value')])         
def update_figure(value,year):
    
    year1 = str(year)
    year2 = year1[-2:]
    rpd_s = rpd.sort_values(by=['RId2'])
  
    rpd_s = rpd_s.apply(pd.to_numeric, errors='ignore')
    rpd_s = rpd_s.fillna(0)

    counties_s = counties.sort_values(by=['US_FIPS'])
  
    selected_med_rev = rpd_s.loc[ : ,'Rper_cap_med_'+year2+'']
    selected_rec_rev = rpd_s.loc[ : ,'Rper_cap_rec_'+year2+'']
  
    df_smr = pd.DataFrame({'name': selected_med_rev.index, 'med_rev': selected_med_rev.values, 'rec_rev': 
            selected_rec_rev.values, 'tot_rev': selected_med_rev.values + selected_rec_rev.values,'CENT_LAT':counties_s['CENT_LAT'],
                'CENT_LON':counties_s['CENT_LONG'], 'marker_size':(selected_med_rev.values + selected_rec_rev.values)*(.3**3)})

    df_year = df_revenue.loc[df_revenue['year'] == year]
 
    df_year_filtered = df_year.loc[df_year['color'] == 'red']

    color_counties = df_year_filtered['county'].unique().tolist()

    
   
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
        text = df_smr['name'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        customdata = df['uid'],
        marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
        )]
    layout = dict(
            mapbox = dict(
                accesstoken = config.mapbox_token,
                center = dict(lat=39, lon=-105.5),
                zoom = 6.25,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 575,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
            Output('biz-map', 'figure'),
            [Input('rev-biz-switch', 'value'),
            Input('categories', 'value')])
def update_figure_a(value,selected_values):
    
    rpd_s = rpd.sort_values(by=['RId2'])
  
    rpd_s = rpd_s.apply(pd.to_numeric, errors='ignore')
    rpd_s = rpd_s.fillna(0)

    data = [dict(
            type = 'scattermapbox',
        )]

    df1 = pd.DataFrame(df.loc[df['Category'] == selected_values])
    if selected_values == 'all':
            filtered_df = df
            data = [dict(
                lat = df['lat'],
                lon = df['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df['color'],opacity=.6)
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
    
    layout = dict(
            mapbox = dict(
                accesstoken = config.mapbox_token,
                center = dict(lat=39, lon=-105.5),
                zoom = 6.5,
                style = 'light'
            ),
            hovermode = 'closest',
            height = 700,
            margin = dict(r=0, l=0, t=0, b=0),
            clickmode = 'event+select'
        )  
  
    fig = dict(data=data, layout=layout)
    return fig


if __name__ == "__main__":
    app.run_server(port=8050, debug=False)