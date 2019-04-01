import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd 
import json
import numpy as np
# import dash_colorscales


from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State




app = dash.Dash(__name__)
server = app.server

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

# Read data
with open('./Colorado_County_Boundaries.geojson') as f:
    counties = json.load(f)
weed_stats = pd.read_csv('./weed_stats.csv')
county_df = pd.read_csv('./counties.csv')

new_cty_df = pd.DataFrame(counties.items())


stats_2017 = weed_stats.loc[weed_stats['Year'] == 2017]
values = stats_2017['Tot_Sales'].tolist()
endpts = list(np.mgrid[min(values):max(values):4j])

BINS = ['0-17872757','17872757.1-35745515','35745515.1-53618273', '>53618273']
print(BINS)
DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c"]

DEFAULT_OPACITY = 0.8

YEARS = [2014, 2015, 2016, 2017, 2018]

names=[]
i = 0
while i < len(county_df['COUNTY']):
    names.append(county_df['COUNTY'][i])
    i += 1




#  Layouts
body = dbc.Container([
    dbc.Row([
        html.Div([
				html.H4(children='Cannabis Sales'),
				html.P('Drag the slider to change the year:'),
			]),
        html.Div([
				dcc.Slider(
					id='years-slider',
					min=min(YEARS),
					max=max(YEARS),
					value=min(YEARS),
					marks={str(year): str(year) for year in YEARS},
			    ),
		], style={'width':400, 'margin':25}),
        # html.Div(id='text-content'),
        # html.Div(
        #     [
        #         dcc.Graph(id='map', figure={
        #             'data': [{
        #                 'hoverinfo': 'text',
        #                 'lat': county_df['CENT_LAT'],
        #                 'lon': county_df['CENT_LONG'],
        #                 'marker': {
        #                     'color': 'blue',
        #                     'size': 4,
        #                     'opacity': 0.6,
        #                 },
        #                 'text': names,
        #                 'type': 'scattermapbox',
        #             }],
        #             'layout': {
        #                 'mapbox': {
        #                     'accesstoken': mapbox_access_token,
        #                     'center': {'lon':-105.5, 'lat':39},
        #                     'zoom':6,
        #                     'style': 'light',
        #                     'layers': [
        #                         {
        #                             'sourcetype': 'geojson',
        #                             'source': counties,
        #                             'type': 'fill',
        #                             'color': 'blue',
                                    
        #                         } 
        #                     ]
        #                 },
        #                 'hovermode': 'closest',
        #                 'height': 1000
        #                 # 'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
        #             }
        #         }),
        #     ], 
        # ),    
    ])
])




app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(debug=True)
