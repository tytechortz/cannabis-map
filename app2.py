import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import geopandas as gpd 
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import json
from dash.dependencies import Input, Output, State



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
pop_rev = gpd.read_file('./per_cap_joined.geojson')
df = gpd.read_file('./cannabis_business.geojson')
print(counties)
# pop_rev.set_index('RId2', drop=False)
print(pop_rev.loc[0])

with open('./Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)

sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})
print(sources[63]['features'][0]['properties']['US_FIPS'])


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
])

@app.callback(
            Output('map', 'figure'),
            [Input('year-selector','value' )])         
def update_figure(year):
    year = str(year)
    counties_s = counties.sort_values(by=['US_FIPS'])
  
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




app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(debug=True)

