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
                    html.Div([
                        dcc.Graph(id='revenue-map')
                    ],
                        className='six columns'
                    ),
                    html.Div([
                        dcc.Graph(id='rev-bar')
                    ],
                        className='five columns'
                    ),
                    html.Div([
                        html.Div(id='instructions')
                    ],
                        className='five columns'
                    ),
                ],
                    className='twelve columns'
                ),
                    
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(id='year-slider')
                ],
                    className='six columns'
                ),
                html.Div([
                    html.Div(id='rev-radio')
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
        ]),
        
@app.callback(
    Output('rev-radio', 'children'),
    [Input('rev-biz-switch', 'value')])
def display_graph(value):
    if value == True:
        return html.Div([
            dcc.RadioItems(id='rev', options=[
                {'label':'Total Sales', 'value':'TOTAL'},
                {'label':'Rec Sales','value':'REC'},
                {'label':'Med Sales','value':'MED'},
            ],
            labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1},
            value = 'TOTAL',
            style = {'text-align': 'center'}
            ),
        ],
            # className='round1'
        ),

@app.callback(
    Output('instructions', 'children'),
    [Input('rev-biz-switch', 'value')])
def instructions(value):
    if value == True:
        return html.Div([
            dcc.Markdown('''
            Click on counties and use year slider to see annual county
            revenue data displayed in graphs.  Green counties have at
            least one form of legalized cannabis, green circles show 
            relative per capita cannabis revenue for selected year. 
            Select sales radio buttons to display revenue graphically below.''')
        ])

@app.callback(
    Output('biz', 'children'),
    [Input('rev-biz-switch', 'value')])
def biz_layout(value):
    if value == False:
        return html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='biz-map')
                ],
                    className='seven columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(id='year-slider')
                ],
                    className='seven columns'
                ),
            ],
                className='row'
            ),
        ])

@app.callback(
            Output('rev-bar', 'figure'),
            [Input('revenue-map', 'clickData'),
            Input('rev-biz-switch', 'value')])         
def create_rev_bar_a(clickData,value):
    print(clickData)
    filtered_county = crat['county'] ==  clickData['points'][-1]['text']
    # print(filtered_county)
    selected_county = crat[filtered_county]
    # denver_county = crat['county'] == 'DENVER'
    # county1 = crat[denver_county]
    # print(county1)
    # print(selected_county)

    traces = []
    # trace = [
    #     {'x': county1['year'], 'y': county1['med_sales'], 'type': 'bar', 'name': 'Med Sales' },
    #     {'x': county1['year'], 'y': county1['rec_sales'], 'type': 'bar', 'name': 'Rec Sales' },
    #     {'x': county1['year'], 'y': county1['tot_sales'], 'type': 'bar', 'name': 'Tot Sales' },
    # ]
    trace1 = [
        {'x': selected_county['year'], 'y': selected_county['med_sales'], 'type': 'bar', 'name': 'Med Sales' },
        {'x': selected_county['year'], 'y': selected_county['rec_sales'], 'type': 'bar', 'name': 'Rec Sales' },
        {'x': selected_county['year'], 'y': selected_county['tot_sales'], 'type': 'bar', 'name': 'Tot Sales' },
    ]

    
    if value == True:
        return {
            'data': trace1,
            'layout': go.Layout(
                height = 350,
                title = '{} COUNTY REVENUE BY YEAR'.format(clickData['points'][-1]['text'])
            ),
        }

@app.callback(
    Output('year-slider', 'children'),
    [Input('rev-biz-switch', 'value')])
def display_rev_map_year(value): 
    # if value == True:
        return html.Div([
                dcc.Slider(
                    id='year',
                        min = 2014,
                        max = 2018,
                        marks={i: '{}'.format(i) for i in range(2014,2019)}, 
                        step = 1,
                        value = 2014,
                        # vertical = False,
                        updatemode = 'drag'
                    )   
            ]) 

@app.callback(
    Output('revenue-map', 'figure'),
    [Input('year', 'value')])         
def update_rev_map(year):
    print(year)
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
                center = dict(lat=39.05, lon=-105.5),
                zoom = 5.85,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 450,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
            Output('biz-map', 'figure'),
            [Input('rev-biz-switch', 'value'),
            Input('categories', 'value')])
def update_figure_a(value, selected_values):
    
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
            height = 400,
            margin = dict(r=0, l=0, t=0, b=0),
            clickmode = 'event+select'
        )  
  
    fig = dict(data=data, layout=layout)
    return fig


app.layout = get_layout
if __name__ == "__main__":
    app.run_server(port=8050, debug=False)
