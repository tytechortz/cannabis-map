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
# server = app.server

app.config['suppress_callback_exceptions']=True

mapbox_access_token = 'pk.eyJ1IjoidHl0ZWNob3J0eiIsImEiOiJjanN1emtuc2cwMXNhNDNuejdrMnN2aHYyIn0.kY0fOoozCTY-4IUzcLx22w'

df = gpd.read_file('./cannabis_business.geojson')
counties = gpd.read_file('./Colorado_County_Boundaries.geojson')



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
                dcc.Graph(id='map',
                config={
                    'scrollZoom': True
                }),
                width={'size':6, 'offset':1},
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
                    html.Tr(html.Div('Licensed Transporters', id='lics-num10', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Center', id='lics-num11', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Cultivator', id='lics-num12', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Infused Product Manufacturer', id='lics-num13', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed R&D Cultivation', id='lics-num1', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Retail Operator', id='lics-num2', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Testing Facility', id='lics-num3', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Retail Marijuana Product Manufacturer', id='lics-num4', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Retail Cultivator', id='lics-num5', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Retail Testing Facility', id='lics-num6', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Retail Transporter', id='lics-num7', style={'font-size':17.5})),
                    html.Tr(html.Div('Licensed Retail Marijuana Store', id='lics-num8', style={'font-size':17.5})),
                ]),
                width = {'size':4}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Table ([
                    html.Tr([html.Th('Business Info')]),
                    html.Tr(html.Div(id='lic-name', style={'height':30, 'text-align': 'center', 'font-size': '1em'})),
                    html.Tr(html.Div(id='biz-name', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='biz-type', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='city', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='address', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='lic-num', style={'height':30, 'text-align': 'center'})),
                ]),
                width = {'size':6, 'offset':1}
            ),
            dbc.Col(
                dcc.Graph(id='stats-bar',
                ),
                width = {'size':5},
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='map-2',
                config={
                    'scrollZoom': True
                }),
                width={'size':10},
            ),
        ]), 
])

@app.callback(
            Output('map', 'figure'),
            [Input('categories','value' )])         
def update_figure(selected_values):
    df1 = pd.DataFrame(df.loc[df['Category'] == selected_values])
    print(selected_values)
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
            zoom = 5.75,
            style = 'light'
        ),
        hovermode = 'closest',
        height = 400,
        margin = dict(r=0, l=0, t=0, b=0)
    )

    fig = dict(data=data, layout=layout)
    return fig

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


# @app.callback(
#     Output('map-2', 'figure'),
#     [Input('year', 'value')])
# def update_figure_a(year):
#     print(counties)
#     data = [dict(
#                 lat = counties['CENT_LAT'],
#                 lon = counties['CENT_LONG'],
#                 text = counties['COUNTY'],
#                 type = 'scattermapbox',
#                 hoverinfo = 'text',
#                 marker = dict(size=7,color=df['color'],opacity=.6)
#             )]
#     layout = dict(
#         mapbox = dict(
#             accesstoken = mapbox_access_token,
#             center = dict(lat=39, lon=-105.5),
#             zoom = 5.75,
#             style = 'light'
#         ),
#         hovermode = 'closest',
#         height = 400,
#         margin = dict(r=0, l=0, t=0, b=0)
#     )

#     fig = dict(data=data, layout=layout)
#     return fig

@app.callback(
            Output('map-2', 'figure'),
            [Input('categories','value' )])         
def update_figure(selected_values):
    df1 = pd.DataFrame(df.loc[df['Category'] == selected_values])
    print(selected_values)
    if selected_values == 'all':
        filtered_df = df
        data = [dict(
            lat = counties['CENT_LAT'],
            lon = counties['CENT_LONG'],
            text = counties['COUNTY'],
            hoverinfo = 'text',
            type = 'scattermapbox',
            # customdata = df['uid'],
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
            zoom = 5.75,
            style = 'light'
        ),
        hovermode = 'closest',
        height = 400,
        margin = dict(r=0, l=0, t=0, b=0)
    )

    fig = dict(data=data, layout=layout)
    return fig

app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8024, debug=True)
