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
            dcc.Graph(id='map',
            config={
                'scrollZoom': True
            }),
            width={'size':7},
        ),
        dbc.Col(
            html.Div([
                html.Table([
                    html.Tr(html.Div(html.Button('All License Types', id='button-all', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Transporters', id='button-transporters', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Center', id='button-center', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Cultivator', id='button-cultivator', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Infused Product Manufacturer', id='button-ipm', n_clicks=0))),
                    html.Tr(html.Div(html.Button('R&D Cultivation', id='button-rdc', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Retail Operator', id='button-operator', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Testing Facility', id='button-testing', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Retail Marijuana Product Manufacturer', id='button-rmpm', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Retail Cultivator', id='button-ret-cult', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Retail Testing Facility', id='button-ret-test', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Retail Transporter', id='button-ret-trans', n_clicks=0))),
                    html.Tr(html.Div(html.Button('Retail Marijuana Store', id='button-ret-store', n_clicks=0))),
                ])
            ])
        )       
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
            width = {'size':4, 'offset':1},
            style = {'height': 50}
        ),
        dbc.Col(
            html.Div(
                className='map-radio',
                children=[ 
                    dcc.RadioItems(id='map-radio', options=[
                        {'label':'Rev Map', 'value':'rev-map'},
                        {'label':'Biz Map','value':'biz-map'},
                    ],
                labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1},
                value = 'rev-map'
                    ),
                ]
            ),
            width = {'size': 2}
        ),
        dbc.Col(
            html.Div(
                className='rev-radio',
                children=[ 
                    dcc.RadioItems(id='rev', options=[
                        {'label':'Total Sales', 'value':'TOTAL'},
                        {'label':'Rec Sales','value':'REC'},
                        {'label':'Med Sales','value':'MED'},
                    ],
                labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1},
                value = 'TOTAL'
                    ),
                ]
            ),
            width = {'size': 4}
        ), 
    ]),
])

@app.callback(
            Output('map', 'figure'),
            [Input('map-radio', 'value'),
            Input('year-selector', 'value'),
            Input('button-all', 'n_clicks'),
            Input('button-transporters','n_clicks'),
            Input('button-center','n_clicks'),
            Input('button-cultivator','n_clicks'),
            Input('button-ipm','n_clicks'),
            Input('button-rdc','n_clicks'),
            Input('button-operator','n_clicks'),
            Input('button-testing','n_clicks'),
            Input('button-rmpm','n_clicks'),
            Input('button-ret-cult','n_clicks'),
            Input('button-ret-test','n_clicks'),
            Input('button-ret-trans','n_clicks'),
            Input('button-ret-store','n_clicks'),
            ])         
def update_figure(map,year,all_clicks,trans_clicks,center_clicks,cultivator_clicks,
ipm_clicks,rdc_clicks,operator_clicks,testing_clicks,rmpm_clicks,ret_cult_clicks,ret_test_clicks,ret_trans_clicks,ret_store_clicks):
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


    if map == 'rev-map':
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
                accesstoken = mapbox_access_token,
                center = dict(lat=39, lon=-105.5),
                zoom = 6,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 600,
            margin = dict(r=0, l=0, t=0, b=0)
        )
    elif map == 'biz-map':
       
        
        print(all_clicks)
        # all_clicks = None
        data = [dict(
            type = 'scattermapbox',
        )]
        if all_clicks % 2 == 0:
            data = [dict(
                lat = df['lat'],
                lon = df['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df['color'],opacity=.6)
            )]
           
        elif trans_clicks % 2 == 1:
            df1 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Transporters'])
            data = [dict(
                lat = df1['lat'],
                lon = df1['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df1['color'],opacity=.6)
            )]
        elif center_clicks % 2 == 1:
            df2 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Center'])
            data = [dict(
                lat = df2['lat'],
                lon = df2['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df2['color'],opacity=.6)
            )]
        elif cultivator_clicks % 2 == 1:
            df3 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Cultivator'])
            data = [dict(
                lat = df3['lat'],
                lon = df3['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df3['color'],opacity=.6)
            )]
        elif ipm_clicks % 2 == 1:
            df4 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Infused Product Manufacturer'])
            data = [dict(
                lat = df4['lat'],
                lon = df4['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df4['color'],opacity=.6)
            )]
        elif rdc_clicks % 2 == 1:
            df5 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed R&D Cultivation'])
            data = [dict(
                lat = df5['lat'],
                lon = df5['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df5['color'],opacity=.6)
            )]
        elif operator_clicks % 2 == 1:
            df6 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Retail Operator'])
            data = [dict(
                lat = df6['lat'],
                lon = df6['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df6['color'],opacity=.6)
            )]
        elif testing_clicks % 2 == 1:
            df7 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Testing Facility'])
            data = [dict(
                lat = df7['lat'],
                lon = df7['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df7['color'],opacity=.6)
            )]
        elif rmpm_clicks % 2 == 1:
            df8 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Retail Marijuana Product Manufacturer'])
            data = [dict(
                lat = df8['lat'],
                lon = df8['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df8['color'],opacity=.6)
            )]
        elif ret_cult_clicks % 2 == 1:
            df9 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Retail Cultivator'])
            data = [dict(
                lat = df9['lat'],
                lon = df9['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df9['color'],opacity=.6)
            )]
        elif ret_test_clicks % 2 == 1:
            df10 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Retail Testing Facility'])
            data = [dict(
                lat = df10['lat'],
                lon = df10['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df10['color'],opacity=.6)
            )]
        elif ret_trans_clicks % 2 == 1:
            df11 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Retail Transporter'])
            data = [dict(
                lat = df11['lat'],
                lon = df11['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df11['color'],opacity=.6)
            )]
        elif ret_store_clicks % 2 == 1:
            df12 = pd.DataFrame(df.loc[df['Category'] == 'MED Licensed Retail Marijuana Store'])
            data = [dict(
                lat = df12['lat'],
                lon = df12['long'],
                text = text,
                hoverinfo = 'text',
                type = 'scattermapbox',
                customdata = df['uid'],
                marker = dict(size=10,color=df12['color'],opacity=.6)
            )]
        layout = dict(
            mapbox = dict(
                accesstoken = mapbox_access_token,
                center = dict(lat=39, lon=-105.5),
                zoom = 6,
                style = 'light'
            ),
            hovermode = 'closest',
            height = 600,
            margin = dict(r=0, l=0, t=0, b=0),
            clickmode = 'event+select'
        )    
  
        
    fig = dict(data=data, layout=layout)
    return fig
    
app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(port=8024, debug=True)