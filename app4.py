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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

counties = gpd.read_file('./Data/Colorado_County_Boundaries.geojson')
counties.sort_values(by=['US_FIPS'])
pop_rev = gpd.read_file('./per_cap_joined.geojson')
per_rev = pd.read_csv('./revenue_pop_data.csv',header=0, delim_whitespace=False)
rpd = pop_rev.set_index('COUNTY', drop=False)
df = gpd.read_file('./Data/cannabis_business.geojson')
df_revenue = pd.read_csv('https://data.colorado.gov/resource/j7a3-jgd3.csv?$limit=5000&$$app_token=Uwt19jYZWTc9a2UPr7tB6x2k1')
# df_taxes = pd.read_csv('https://data.colorado.gov/resource/3sm5-jtur.csv')
# df_biz = pd.read_csv('https://data.colorado.gov/resource/sqs8-2un5.csv')


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
            html.Div('Business Data',id='rev-title', style={'text-align':'right'})
        ),
        dbc.Col(
            html.Div([
                daq.BooleanSwitch(
                    id='rev-biz-switch',
                    on=True,
                    color='red'
                ),
            ]),
            width={'size':1}
        ),
        dbc.Col(
            html.Div('Revenue Data',id='biz-title')
        ),
    
    ]),

    html.Div(id='rev-stuff'),
    html.Div(id='biz-stuff'),
    html.Div(id='biz-stuff-2'),
    
    html.Div(id='rev-stuff-2'),
    html.Div(id='rev-stuff-3'),
                  
])


@app.callback(
            Output('rev-stuff', 'children'),
            [Input('rev-biz-switch', 'on')])
def display_rev_page(switch):
    print(switch)
    rev_page = []
    if switch == True:
        rev_page.append(
            dbc.Row([
                dbc.Col(
                    dcc.Slider(
                        id='year-selector',
                        min = 2014,
                        max = 2018,
                        marks={i: '{}'.format(i) for i in range(2014,2019)}, 
                        step = 1,
                        value = 2014,
                        vertical = True,
                        updatemode = 'drag'
                    ),
                    width = {'size':1},
                ),   
                dbc.Col(
                    dcc.Graph(id='rev-map',
                    config={
                        'scrollZoom': True
                    }),
                    width={'size':8},
                ),
                dbc.Col(
                    html.Div([
                            html.Table ([
                                html.Tr([html.Th('Revenue Stats')]),
                                html.Tr(html.Div(id='county-name', style={'height':30, 'text-align': 'left'})),
                                # html.Tr(html.Div(id='biz-name', style={'height':30, 'text-align': 'left'})),
                                # html.Tr(html.Div(id='biz-type', style={'height':30, 'text-align': 'left'})),
                                # html.Tr(html.Div(id='city', style={'height':30, 'text-align': 'left'})),
                                # html.Tr(html.Div(id='address', style={'height':30, 'text-align': 'left'})),
                                # html.Tr(html.Div(id='lic-num', style={'height':30, 'text-align': 'left'})),
                            ]),
                        ],
                        style = {'overflow-x':'scroll'}
                        ),   
                    width = {'size':3}
                ),
                
                  # style = {'height': 50}
            ])
        )
        return rev_page

@app.callback(
            Output('biz-stuff', 'children'),
            [Input('rev-biz-switch', 'on')])
def display_biz_page(switch):
    print(switch)
    biz_page = []
    if switch == False:
        biz_page.append(
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='biz-map',
                    config={
                        'scrollZoom': True
                    }),
                    width={'size':8},
                ),
                dbc.Col(
                html.Div(
                    className='radio',
                    children=[ 
                    dcc.RadioItems(id='categories', options=[
                        {'label':'', 'value':'all'},
                        {'label':'','value':'MED Licensed Transporters'},
                        {'label':'','value':'MED Licensed Center'},
                        {'label':'','value':'MED Licensed Cultivator'},
                        {'label':'','value':'MED Licensed Infused Product Manufacturer'},
                        {'label':'','value':'MED Licensed R&D Cultivation'},
                        {'label':'','value':'MED Licensed Retail Operator'},
                        {'label':'','value':'MED Licensed Testing Facility'},
                        {'label':'','value':'MED Licensed Retail Marijuana Product Manufacturer'},
                        {'label':'','value':'MED Licensed Retail Cultivator'},
                        {'label':'','value':'MED Licensed Retail Testing Facility'},
                        {'label':'','value':'MED Licensed Retail Transporter'},
                        {'label':'','value':'MED Licensed Retail Marijuana Store'},
                    ],
                    labelStyle={'display':'block', 'margin': 0, 'padding': 1},
                    value = 'all'
                    ),
                ]),
                width = {'size':.1}
                ),
                dbc.Col(
                html.Div([
                    html.Table ([
                        html.Tr(html.Div('All License Types', id='lics-num9', style={'font-size':17.5})),
                        html.Tr(html.Div('Transporters', id='lics-num10', style={'font-size':17.5})),
                        html.Tr(html.Div('Center', id='lics-num11', style={'font-size':17.5})),
                        html.Tr(html.Div('Cultivator', id='lics-num12', style={'font-size':17.5})),
                        html.Tr(html.Div('Infused Product Mfg.', id='lics-num13', style={'font-size':17.5})),
                        html.Tr(html.Div('R&D Cultivation', id='lics-num1', style={'height':26,'font-size':17.5})),
                        html.Tr(html.Div('Retail Operator', id='lics-num2', style={'height':26,'font-size':17.5})),
                        html.Tr(html.Div('Testing Facility', id='lics-num3', style={'height':26,'font-size':17.5})),
                        html.Tr(html.Div('Retail Marijuana Product Mfg.', id='lics-num4', style={'height':26,'font-size':17.5})),
                        html.Tr(html.Div('Retail Cultivator', id='lics-num5', style={'height':26,'font-size':17.5})),
                        html.Tr(html.Div('Retail Testing Facility', id='lics-num6', style={'height':26,'font-size':17.5})),
                        html.Tr(html.Div('Retail Transporter', id='lics-num7', style={'height':26,'font-size':17.5})),
                        html.Tr(html.Div('Retail Marijuana Store', id='lics-num8', style={'font-size':17.5})),
                        html.Tr([html.Th('Business Info',style={'height':50, 'text-align': 'center'})]),
                        html.Tr(html.Div(id='lic-name', style={'height':50, 'text-align': 'left'})),
                        html.Tr(html.Div(id='biz-name', style={'height':50, 'text-align': 'left'})),
                        html.Tr(html.Div(id='biz-type', style={'height':30, 'text-align': 'left'})),
                        html.Tr(html.Div(id='city', style={'height':30, 'text-align': 'left'})),
                        html.Tr(html.Div(id='address', style={'height':30, 'text-align': 'left'})),
                        html.Tr(html.Div(id='lic-num', style={'height':30, 'text-align': 'left'})),
                    ]),
                ],
                style = {'overflow-x':'scroll'}
                ),
                width = {'size':3}
                ),
            ]),
        ) 
       
        return biz_page


@app.callback(
            Output('rev-stuff-2', 'children'),
            [Input('rev-biz-switch', 'on')])
def display_rev_page_a(switch):
    rev_page_selectors = []
    if switch == True:
        rev_page_selectors.append(
            dbc.Row([
                
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
                    width = {'size': 4, 'offset':8}
                ), 
            ]),
        )
        return rev_page_selectors

@app.callback(
            Output('rev-stuff-3', 'children'),
            [Input('rev-biz-switch', 'on')])
def display_rev_page_b(switch):
    rev_page_graphs = []
    if switch == True:
        rev_page_graphs.append(
           dbc.Row([
                dbc.Col(
                    dcc.Graph(id='rev-bar',
                    ),
                    width = {'size': 6}
                ),
                dbc.Col(
                    dcc.Graph(id='rev-scatter',
                    ),
                    width = {'size': 6}
                ),
            ]), 
        )
        return rev_page_graphs  
        


@app.callback(
            Output('rev-map', 'figure'),
            [Input('rev-biz-switch', 'on'),
            Input('year-selector', 'value')])         
def update_figure(switch,year):
    
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
                accesstoken = mapbox_access_token,
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
            Output('rev-scatter', 'figure'),
            [Input('rev', 'value'),
            Input('rev-map', 'clickData'),
            Input('year-selector','value'),
            Input('rev-biz-switch', 'on')])
def create_rev_scat(rev,clickData,year,switch):
  
    year_df = df_revenue[df_revenue['year'] == year]
    filtered_df = year_df[year_df['county'] == clickData['points'][-1]['text']]

    # if selected_values == 'rev-map':

    traces = []

    if rev == 'TOTAL':
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['tot_sales'],
            name = rev,
            line = {'color':'red'} 
            ))
    elif rev == 'REC':  
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['rec_sales'],
            name = rev,
            line = {'color':'dodgerblue'}
            ))
    elif rev == 'MED':  
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['med_sales'],
            name = rev,
            line = {'color':'black'}
            ))
    return {
            'data': traces,
            'layout': go.Layout(
                xaxis = {'title': 'Month'},
                yaxis = {'title': 'Revenue'},
                hovermode = 'closest',
                title = '{} COUNTY {} REVENUE - {}'.format(clickData['points'][-1]['text'],rev,year),
                height = 400,
            )
        }

@app.callback(
            Output('rev-bar', 'figure'),
            [Input('rev-map', 'clickData'),
            Input('rev-biz-switch', 'on')])
def create_rev_bar(clickData,switch):
    filtered_county = crat['county'] ==  clickData['points'][-1]['text']
    selected_county = crat[filtered_county]

    traces = []
    trace1 = [
        {'x': selected_county['year'], 'y': selected_county['med_sales'], 'type': 'bar', 'name': 'Med Sales' },
        {'x': selected_county['year'], 'y': selected_county['rec_sales'], 'type': 'bar', 'name': 'Rec Sales' },
        {'x': selected_county['year'], 'y': selected_county['tot_sales'], 'type': 'bar', 'name': 'Tot Sales' },
    ]
    traces.append(trace1)
    if switch == True:
        return {
            'data': trace1,
            'layout': go.Layout(
                height = 400,
                title = '{} COUNTY REVENUE BY YEAR'.format(clickData['points'][-1]['text'])
            ),
        }


@app.callback(
            Output('biz-map', 'figure'),
            [Input('rev-biz-switch', 'on'),
            Input('categories', 'value')])
def update_figure_a(switch,selected_values):
    
    rpd_s = rpd.sort_values(by=['RId2'])
  
    rpd_s = rpd_s.apply(pd.to_numeric, errors='ignore')
    rpd_s = rpd_s.fillna(0)

    # counties_s = counties.sort_values(by=['US_FIPS'])
  

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
                accesstoken = mapbox_access_token,
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

@app.callback(
    Output('lic-name', 'children'),
    [Input('biz-map', 'hoverData'),
    Input('rev-biz-switch', 'on')])
def update_text_a(hoverData,switch):
    if switch == False:
        s = df[df['uid'] == hoverData['points'][0]['customdata']]
        return  'Licensee: {}'.format(s.iloc[0]['Licensee'])

@app.callback(
    Output('biz-name', 'children'),
    [Input('biz-map', 'hoverData'),
    Input('rev-biz-switch', 'on')])
def update_text_b(hoverData,switch):
    if switch == False:
        s = df[df['uid'] == hoverData['points'][0]['customdata']]
        return  'Business: {}'.format(s.iloc[0]['DBA'])

@app.callback(
    Output('biz-type', 'children'),
    [Input('biz-map', 'hoverData'),
    Input('rev-biz-switch', 'on')])
def update_text_c(hoverData,switch):
    if switch == False:
        s = df[df['uid'] == hoverData['points'][0]['customdata']]
        return  'Business Type: {}'.format(s.iloc[0]['Category'][13:])

@app.callback(
    Output('city', 'children'),
    [Input('biz-map', 'hoverData'),
    Input('rev-biz-switch', 'on')])
def update_text_d(hoverData,switch):
    if switch == False:
        s = df[df['uid'] == hoverData['points'][0]['customdata']]
        return  'City: {}'.format(s.iloc[0]['City'])

@app.callback(
    Output('address', 'children'),
    [Input('biz-map', 'hoverData'),
    Input('rev-biz-switch', 'on')])
def update_text_e(hoverData,switch):
    if switch == False:
        s = df[df['uid'] == hoverData['points'][0]['customdata']]
        return  'Address: {}'.format(s.iloc[0]['Street_Address'])
        
@app.callback(
    Output('lic-num', 'children'),
    [Input('biz-map', 'hoverData'),
    Input('rev-biz-switch', 'on')])
def update_text_f(hoverData,switch):
    if switch == False:
        s = df[df['uid'] == hoverData['points'][0]['customdata']]
        return  'License Number: {}'.format(s.iloc[0]['License_No'])








app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(port=8050, debug=True)