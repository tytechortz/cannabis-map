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




app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

df = gpd.read_file('./cannabis_business.geojson')
print(df['Licensee'])

text = []
print(len(df))
text=[]
i=0
while i < len(df):
    text.append(df['Licensee'][i])
    i += 1
print(len(text))
#  Layouts
body = dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div(
                    className='app-header',
                    children=[
                        html.Div('COLORADO CANNABIS BUSINESSES', className="app-header--title"),
                    ]
                ),
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='map', 
                        figure={
                            'data': [{
                                
                                'lat': df['lat'],
                                'lon': df['long'],
                                'marker': {
                                    'color': 'blue',
                                    'size': 6,
                                    'opacity': 0.6
                                },
                                'text': text,
                                'hoverinfo': 'text',
                                'customdata': df['uid'],
                                'type': 'scattermapbox'
                            }],
                            'layout': {
                                'mapbox': {
                                    'accesstoken': 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw',
                                    'center': {
                                        'lat': 39,
                                        'lon':-105.5
                                    },
                                    'zoom': 6,
                                },
                                'hovermode': 'closest',
                                
                                'height': 550,
                                'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
                            }
                        }
                    ),
                ]),
                width={'size':10, 'offset':1 }
            ),
        ]),
        dbc.Row([
            html.Div(id='lic-name'),
        ]),
        dbc.Row([
            html.Div(id='biz-name'),
        ]),
        dbc.Row([
            html.Div(id='biz-type'),
        ]),
        dbc.Row([
            html.Div(id='city'),
        ]),
        dbc.Row([
            html.Div(id='address'),
        ]),
        dbc.Row([
            html.Div(id='lic-num'),
        ]),
        
])

@app.callback(
    dash.dependencies.Output('lic-name', 'children'),
    [dash.dependencies.Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Licensee Name: {}'.format(s.iloc[0]['Licensee'])

@app.callback(
    dash.dependencies.Output('biz-name', 'children'),
    [dash.dependencies.Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Business Name: {}'.format(s.iloc[0]['DBA'])

@app.callback(
    dash.dependencies.Output('biz-type', 'children'),
    [dash.dependencies.Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Business Type: {}'.format(s.iloc[0]['Category'])

@app.callback(
    dash.dependencies.Output('city', 'children'),
    [dash.dependencies.Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'City: {}'.format(s.iloc[0]['City'])

@app.callback(
    dash.dependencies.Output('address', 'children'),
    [dash.dependencies.Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Address: {}'.format(s.iloc[0]['Street_Address'])
        
@app.callback(
    dash.dependencies.Output('lic-num', 'children'),
    [dash.dependencies.Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'License Number: {}'.format(s.iloc[0]['License_No'])

app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8024, debug=True)
