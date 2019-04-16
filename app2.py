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
# from plotly import graph_objs as go
# from plotly.graph_objs import *



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

counties = gpd.read_file('./Colorado_County_Boundaries.geojson')
pop_rev = gpd.read_file('./per_cap_joined.geojson')
df = gpd.read_file('./cannabis_business.geojson')
df_revenue = pd.read_csv('https://data.colorado.gov/resource/j7a3-jgd3.csv?$limit=4000&$$app_token=Uwt19jYZWTc9a2UPr7tB6x2k1')
df_taxes = pd.read_csv('https://data.colorado.gov/resource/3sm5-jtur.csv')
df_biz = pd.read_csv('https://data.colorado.gov/resource/sqs8-2un5.csv')
print(df_revenue)
# df_revenue = pd.read_csv('./weed_stats.csv')

# df_revenue1 = pd.read_csv('./weed_stats.csv')
df_revenue['county'] = df_revenue['county'].str.upper()

df_revenue['tot_sales'] = df_revenue['med_sales'] + df_revenue['rec_sales']
# print(df_revenue)
# pop_rev.set_index('RId2', drop=False)
# print(pop_rev.loc[0]['Rrev_med_14'])

with open('./Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)

sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})
# print(sources[63]['features'][0]['properties']['US_FIPS'])
county_revenue_df = df_revenue.groupby(['county', 'year'])
crat = county_revenue_df.sum()
crat.reset_index(inplace=True)

layers=[dict(sourcetype = 'geojson',
             source =sources[k],
             below="water", 
             type = 'fill',
             color = sources[k]['features'][0]['properties']['COLOR'],
             opacity = 0.2
            ) for k in range(len(sources))]


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

# def license_count():

colors = dict(zip(categories, color_list))
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
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='map',
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
                    labelStyle={'display':'block', 'margin': 0, 'padding': 1}
                    ),
                ]),
                width = {'size':.1}
            ),
            dbc.Col(
                html.Table ([
                    html.Tr(html.Div('All License Types', id='lics-num9', style={'font-size':17.5})),
                    html.Tr(html.Div('Transporters', id='lics-num10', style={'font-size':17.5})),
                    html.Tr(html.Div('Center', id='lics-num11', style={'font-size':17.5})),
                    html.Tr(html.Div('Cultivator', id='lics-num12', style={'font-size':17.5})),
                    html.Tr(html.Div('Infused Product Mfg.', id='lics-num13', style={'font-size':17.5})),
                    html.Tr(html.Div('R&D Cultivation', id='lics-num1', style={'font-size':17.5})),
                    html.Tr(html.Div('Retail Operator', id='lics-num2', style={'font-size':17.5})),
                    html.Tr(html.Div('Testing Facility', id='lics-num3', style={'font-size':17.5})),
                    html.Tr(html.Div('Retail Marijuana Product Mfg.', id='lics-num4', style={'font-size':17.5})),
                    html.Tr(html.Div('Retail Cultivator', id='lics-num5', style={'font-size':17.5})),
                    html.Tr(html.Div('Retail Testing Facility', id='lics-num6', style={'font-size':17.5})),
                    html.Tr(html.Div('Retail Transporter', id='lics-num7', style={'font-size':17.5})),
                    html.Tr(html.Div('Retail Marijuana Store', id='lics-num8', style={'font-size':17.5})),
                    html.Tr([html.Th('Business Info')]),
                    html.Tr(html.Div(id='lic-name', style={'height':30, 'text-align': 'left', 'font-size': '1em'})),
                    html.Tr(html.Div(id='biz-name', style={'height':30, 'text-align': 'left'})),
                    html.Tr(html.Div(id='biz-type', style={'height':30, 'text-align': 'left'})),
                    html.Tr(html.Div(id='city', style={'height':30, 'text-align': 'left'})),
                    html.Tr(html.Div(id='address', style={'height':30, 'text-align': 'left'})),
                    html.Tr(html.Div(id='lic-num', style={'height':30, 'text-align': 'left'})),
                ]),
                width = {'size':3}
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
            width = {'size':4, 'offset':2},
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
                labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1}
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
                labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1}
                    ),
                ]
            ),
            width = {'size': 4}
        ),
    ]),
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
    # dbc.Row([
    #         dbc.Col(
    #             html.Div(
    #                 className='radio',
    #                 children=[ 
    #                 dcc.RadioItems(id='categories', options=[
    #                     {'label':'', 'value':'all'},
    #                     {'label':'','value':'MED Licensed Transporters'},
    #                     {'label':'','value':'MED Licensed Center'},
    #                     {'label':'','value':'MED Licensed Cultivator'},
    #                     {'label':'','value':'MED Licensed Infused Product Manufacturer'},
    #                     {'label':'','value':'MED Licensed R&D Cultivation'},
    #                     {'label':'','value':'MED Licensed Retail Operator'},
    #                     {'label':'','value':'MED Licensed Testing Facility'},
    #                     {'label':'','value':'MED Licensed Retail Marijuana Product Manufacturer'},
    #                     {'label':'','value':'MED Licensed Retail Cultivator'},
    #                     {'label':'','value':'MED Licensed Retail Testing Facility'},
    #                     {'label':'','value':'MED Licensed Retail Transporter'},
    #                     {'label':'','value':'MED Licensed Retail Marijuana Store'},
    #                 ],
    #                 labelStyle={'display':'block', 'margin': 0, 'padding': 1}
    #                 ),
    #             ]),
    #             width = {'size':.1}
    #         ),
    #         dbc.Col(
    #             html.Table ([
    #                 html.Tr(html.Div('All License Types', id='lics-num9', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Transporters', id='lics-num10', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Center', id='lics-num11', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Cultivator', id='lics-num12', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Infused Product Manufacturer', id='lics-num13', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed R&D Cultivation', id='lics-num1', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Retail Operator', id='lics-num2', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Testing Facility', id='lics-num3', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Retail Marijuana Product Manufacturer', id='lics-num4', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Retail Cultivator', id='lics-num5', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Retail Testing Facility', id='lics-num6', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Retail Transporter', id='lics-num7', style={'font-size':17.5})),
    #                 html.Tr(html.Div('Licensed Retail Marijuana Store', id='lics-num8', style={'font-size':17.5})),
    #             ]),
    #             width = {'size':4}
    #         ),
    #     ]),
        dbc.Row([
            # dbc.Col(
            #     html.Table ([
            #         html.Tr([html.Th('Business Info')]),
            #         html.Tr(html.Div(id='lic-name', style={'height':30, 'text-align': 'center', 'font-size': '1em'})),
            #         html.Tr(html.Div(id='biz-name', style={'height':30, 'text-align': 'center'})),
            #         html.Tr(html.Div(id='biz-type', style={'height':30, 'text-align': 'center'})),
            #         html.Tr(html.Div(id='city', style={'height':30, 'text-align': 'center'})),
            #         html.Tr(html.Div(id='address', style={'height':30, 'text-align': 'center'})),
            #         html.Tr(html.Div(id='lic-num', style={'height':30, 'text-align': 'center'})),
            #     ]),
            #     width = {'size':4, 'offset':1}
            # ),
            dbc.Col(
                dcc.Graph(id='stats-bar',
                ),
                width = {'size':5},
                style = {'height': 200}
            ),
        ]), 
])

@app.callback(
            Output('map', 'figure'),
            [Input('year-selector','value' ),
            Input('map-radio', 'value'),
            Input('categories', 'value')])         
def update_figure(year,map,selected_values):
    year = str(year)
    year = year[-2:]
    print(map)
    counties_s = counties.sort_values(by=['US_FIPS'])

    selected_med_rev = pop_rev.loc[ : ,'Rrev_med_'+year+'']
    selected_rec_rev = pop_rev.loc[ : ,'Rrev_rec_'+year+'']
    
    if map == 'rev-map':
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
                zoom = 6,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 600,
            margin = dict(r=0, l=0, t=0, b=0)
        )
    elif map == 'biz-map':
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
                marker = dict(size=7,color=df['color'],opacity=.6)
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
                zoom = 6,
                style = 'light'
            ),
            hovermode = 'closest',
            height = 600,
            margin = dict(r=0, l=0, t=0, b=0)
        )    
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
            Output('rev-bar', 'figure'),
            [Input('rev', 'value'),
            Input('map', 'clickData')])
def create_rev_bar(selected_values,clickData):
    filtered_county = crat['county'] ==  clickData['points'][-1]['text']
    # filtered_county = crat['County'] == 'ADAMS'
    selected_county = crat[filtered_county]
    # print(selected_county)
    traces = []
    trace1 = [
        {'x': selected_county['year'], 'y': selected_county['med_sales'], 'type': 'bar', 'name': 'Med Sales' },
        {'x': selected_county['year'], 'y': selected_county['rec_sales'], 'type': 'bar', 'name': 'Rec Sales' },
        {'x': selected_county['year'], 'y': selected_county['tot_sales'], 'type': 'bar', 'name': 'Tot Sales' },
    ]
    traces.append(trace1)
  
    return {
        'data': trace1,
        'layout': go.Layout(
            title = '{} COUNTY REVENUE BY YEAR'.format(clickData['points'][-1]['text'])
        ),
    }

@app.callback(
            Output('rev-scatter', 'figure'),
            [Input('rev', 'value'),
            Input('map', 'clickData'),
            Input('year-selector','value')])
def create_rev_scat(rev,clickData,year):
    # year = str(year)
    year_df = df_revenue[df_revenue['year'] == year]
    filtered_df = year_df[year_df['county'] == clickData['points'][-1]['text']]
    print(filtered_df)
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
            title = '{} COUNTY {} REVENUE'.format(clickData['points'][-1]['text'],rev),
            height = 450,
        )
    }

@app.callback(
    Output('lic-name', 'children'),
    [Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Licensee Name: {}'.format(s.iloc[0]['Licensee'])

@app.callback(
    Output('biz-name', 'children'),
    [Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Business Name: {}'.format(s.iloc[0]['DBA'])

@app.callback(
    Output('biz-type', 'children'),
    [Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Business Type: {}'.format(s.iloc[0]['Category'])

@app.callback(
    Output('city', 'children'),
    [Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'City: {}'.format(s.iloc[0]['City'])

@app.callback(
    Output('address', 'children'),
    [Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'Address: {}'.format(s.iloc[0]['Street_Address'])
        
@app.callback(
    Output('lic-num', 'children'),
    [Input('map', 'hoverData')])
def update_text(hoverData):
    s = df[df['uid'] == hoverData['points'][0]['customdata']]
    return  'License Number: {}'.format(s.iloc[0]['License_No'])

@app.callback(Output('stats-bar', 'figure'),
             [Input('categories', 'value')])
            #  Input('years', 'value')])
def update_figure_b(selected_values):
    df1 = pd.DataFrame(df.loc[df['Category'] == selected_values])
    if selected_values == 'all':
        type_count = df['Category'].count()
        count_year = []
        count_year.append(type_count)
        data = [
            go.Bar(
                x=df['Year'],
                y=count_year,
            )
        ]
        layout = go.Layout(
            xaxis={'title': 'Year', 'range':[2014,2019]},
            yaxis={'title': 'Count'},
            title='License Count By Year',
            plot_bgcolor = 'rgb(255,255,255,.5)',
            paper_bgcolor = 'rgb(255,255,255,.7)',
            height = 250  
        )
        return {'data': data, 'layout': layout}
    else: 
        
        type_count1 = df1['Category'].count()
        count_year1 = []
        count_year1.append(type_count1)
        data = [
            go.Bar(
                x=df1['Year'],
                y=count_year1,
            )
        ]
        layout = go.Layout(
            xaxis={'title': 'Year', 'range':[2014,2019]},
            yaxis={'title': 'Count'},
            title='License Count By Year',
            plot_bgcolor = 'rgb(255,255,255,.5)',
            paper_bgcolor = 'rgb(255,255,255,.7)',
            height = 250  
        )
        return {'data': data, 'layout': layout}

app.layout = html.Div(body)

if __name__ == '__main__':
    app.run_server(port=8024, debug=True)

