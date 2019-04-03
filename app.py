import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd 
import json
import numpy as np
import dash_colorscales


from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State




app = dash.Dash(__name__)
server = app.server

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'


# df = pd.read_csv(
#     'https://raw.githubusercontent.com/'
#     'plotly/datasets/master/'
#     '1962_2006_walmart_store_openings.csv')

df = gpd.read_file('./cannabis_business.geojson')
print(df)

#  Layouts
body = dbc.Container([
    dbc.Row([
        html.H1('Colorado Cannabis Businesses'),  
    ]),
    dbc.Row([
         html.Div(id='text-content'),
    ]),
    dbc.Row([
        dcc.Graph(id='map', figure={
        'data': [{
            'lat': df['lat'],
            'lon': df['long'],
            'marker': {
                'color': 'blue',
                'size': 8,
                'opacity': 0.6
            },
            # 'customdata': df['storenum'],
            'type': 'scattermapbox'
        }],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
            },
            'hovermode': 'closest',
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
        }
    })
    ])
])



app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(debug=True)
