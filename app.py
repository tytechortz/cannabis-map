import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd 
import json

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State




app = dash.Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions']=True
mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'


with open('./Colorado_County_Boundaries.geojson') as f:
    counties = json.load(f)
# with open('./solar.geojson') as f:
#     red_data = json.load(f)    
# sources=[{"type": "FeatureCollection", 'features': [feat]} for feat in red_data['features']]
dec_2017 = []


weed_stats = pd.read_csv('./weed_stats.csv')
county_df = pd.read_csv('./counties.csv')


i = 0
print(len(weed_stats['Tot_Sales']))



# i = 0
# print(len(solar['dni']))
# while i < len(solar['dni']):
#     text.append(str(solar['dni'][i]))
#     i += 1
# print(type(text[0]))
names=[]
i = 0
print(len(county_df['COUNTY']))
while i < len(county_df['COUNTY']):
    names.append(county_df['COUNTY'][i])
    i += 1
print(names)


#  Layouts
body = dbc.Container([
    dbc.Row([
        html.Div(id='text-content'),
        html.Div(
            [
                dcc.Graph(id='map', figure={
                    'data': [{
                        'hoverinfo': 'text',
                        'lat': county_df['CENT_LAT'],
                        'lon': county_df['CENT_LONG'],
                        'marker': {
                            # 'color': county_df[''],
                            'size': 4,
                            'opacity': 0.6,
                        },
                        'text': ['LARIMER', 'LAS ANIMAS', 'FREMONT', 'GUNNISON', 'CONEJOS', 'EAGLE', 'OTERO', 'LA PLATA', 'SUMMIT', 'CUSTER', 'PITKIN', 'CROWLEY', 'CHEYENNE', 'BENT', 'ADAMS', 'ELBERT', 'YUMA', 'LAKE', 'DELTA', 'COSTILLA', 'GARFIELD', 'MORGAN', 'PROWERS', 'MONTEZUMA', 'MINERAL', 'LINCOLN', 'JEFFERSON', 'RIO BLANCO', 'SEDGWICK', 'SAN MIGUEL', 'ALAMOSA', 'PHILLIPS', 'OURAY', 'MESA', 'SAGUACHE', 'DOUGLAS', 'DOLORES', 'RIO GRANDE', 'PUEBLO', 'KIT CARSON', 'BACA', 'GRAND', 'LOGAN', 'CLEAR CREEK', 'MOFFAT', 'TELLER', 'BOULDER', 'KIOWA', 'CHAFFEE', 'HINSDALE', 'JACKSON', 'WELD', 'SAN JUAN', 'MONTROSE', 'BROOMFIELD', 'WASHINGTON', 'ROUTT', 'ARCHULETA', 'GILPIN', 'DENVER', 'PARK', 'EL PASO', 'ARAPAHOE', 'HUERFANO'],
                        'type': 'scattermapbox'
                    }],
                    'layout': {
                        'mapbox': {
                            'accesstoken': mapbox_access_token,
                            'center': {'lon':-105.5, 'lat':39},
                            'zoom':6,
                            'style': 'light',
                            'layers': [
                                {
                                    'sourcetype': 'geojson',
                                    'source': counties,
                                    'type': 'fill',

                                    'color': 'rgba(255, 255, 255, .05)'
                                },
                            ]
                        },
                        'hovermode': 'closest',
                        'height': 1000
                        # 'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
                    }
                }),
            ], 
        ),    
    ])
])




app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(debug=True)
