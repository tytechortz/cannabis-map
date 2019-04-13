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
from plotly import graph_objs as go
from plotly.graph_objs import *



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
pop_rev = gpd.read_file('./per_cap_joined.geojson')
df = gpd.read_file('./cannabis_business.geojson')
df_revenue = pd.read_csv('./weed_stats.csv')
df_revenue['County'] = df_revenue['County'].str.upper()
# pop_rev.set_index('RId2', drop=False)
print(pop_rev.loc[0]['Rrev_med_14'])

with open('./Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)

sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})
print(sources[63]['features'][0]['properties']['US_FIPS'])

county_revenue_df = df_revenue.groupby(['County', 'Year'])
crat = county_revenue_df.sum()
crat.reset_index(inplace=True)

# def color_maker():
#     for i in pop_rev:
#         if pop_rev.loc[i]['Rrev_med_14'] is not None:
#             print(true)
#         else: print(false)

# color_maker()

layers=[dict(sourcetype = 'geojson',
            source =sources[k],
            below="water", 
            type = 'fill',
            #  color = sources[k]['features'][0]['properties']['COLOR'],
            color = 'white',
            opacity = 0.2
            ) for k in range(len(sources))]

body = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div(
                className='app-header',
                children=[
                    html.Div('COLORADO CANNABIS BUSINESSES', className="app-header--title"),
                ]
            ),
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='map',
            config={
                'scrollZoom': True
            }),
            width={'size':12},
        ),       
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Slider(
                    id='year-selector',
                    min = 2014,
                    max = 2018,
                    marks={i: '{}'.format(i) for i in range(2014,2019)}, 
                    step = 1,
                    value = 2014
                ),
            ),
            width = {'size':4, 'offset':4},
            style = {'height': 50}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='rev-bar',
            ),
            width = {'size': 10}
        ),
        dbc.Col(
            html.Div(
                className='rev-radio',
                children=[ 
                    dcc.RadioItems(id='sales', options=[
                        {'label':'Total Sales', 'value':'tot'},
                        {'label':'Rec Sales','value':'rec'},
                        {'label':'Med Sales','value':'med'},
                    ],
                labelStyle={'display':'block', 'margin': 0, 'padding': 1}
                    ),
                ]
            ),
            width = {'size': 2}
        ),
    ]), 
])

@app.callback(
            Output('map', 'figure'),
            [Input('year-selector','value' )])         
def update_figure(year):
    year = str(year)
    year = year[-2:]
   
    counties_s = counties.sort_values(by=['US_FIPS'])

    selected_med_rev = pop_rev.loc[ : ,'Rrev_med_'+year+'']
    selected_rec_rev = pop_rev.loc[ : ,'Rrev_rec_'+year+'']
    
  
    data = [dict(
        lat = counties_s['CENT_LAT'],
        lon = counties_s['CENT_LONG'],
        text = counties_s['COUNTY'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        customdata = df['uid'],
        marker = dict(size=5,color='red',opacity=.5),
        )]
    layout = dict(
        mapbox = dict(
            accesstoken = mapbox_access_token,
            center = dict(lat=39, lon=-105.5),
            zoom = 6.5,
            style = 'light',
            layers = layers
        ),
        hovermode = 'closest',
        height = 800,
        margin = dict(r=0, l=0, t=0, b=0)
    )

    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
            Output('rev-bar', 'figure'),
            [Input('sales', 'value'),
            Input('map', 'hoverData')])
def create_rev_bar_a(selected_values,hoverData):
    filtered_county = crat['County'] ==  hoverData['points'][-1]['text']
    # filtered_county = crat['County'] == 'ADAMS'
    selected_county = crat[filtered_county]
    # print(selected_county)
    traces = []
    trace1 = [
        {'x': selected_county['Year'], 'y': selected_county['Med_Sales'], 'type': 'bar', 'name': 'Med Sales' },
        {'x': selected_county['Year'], 'y': selected_county['Rec_Sales'], 'type': 'bar', 'name': 'Rec Sales' },
        {'x': selected_county['Year'], 'y': selected_county['Tot_Sales'], 'type': 'bar', 'name': 'Tot Sales' },
    ]
    traces.append(trace1)
  
    return {
        'data': trace1,
        'layout': go.Layout(
            title = '{} County Revenue By Year'.format(hoverData['points'][-1]['text'])
        ),
    }


app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(port=8024, debug=True)

