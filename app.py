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

# def generate_table_categories(categories_table, max_rows=12):
#     return html.Table (
#         [html.Tr([html.Th(col) for col in categories_table.columns])] +
#         [html.Tr([
#             html.Td(categories_table.iloc[i][col]) for col in categories_table.columns
#             ]) for i in range(min(len(categories_table), max_rows))]
#     )




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
        # dbc.Row([
        #     dbc.Col(
        #         html.Div([
        #             dcc.Graph(id='map', 
        #                 figure={
        #                     'data': [{
        #                         'lat': df['lat'],
        #                         'lon': df['long'],
        #                         'marker': {
        #                             'color': df['color'],
        #                             'size': 6,
        #                             'opacity': 0.6
        #                         },
        #                         'text': text,
        #                         'hoverinfo': 'text',
        #                         'customdata': df['uid'],
        #                         'type': 'scattermapbox'
        #                     }],
        #                     'layout': {
        #                         'mapbox': {
        #                             'accesstoken': mapbox_access_token,
        #                             'center': {
        #                                 'lat': 39,
        #                                 'lon':-105.5
        #                             },
        #                             'zoom': 6,
        #                         },
        #                         'hovermode': 'closest',
                                
        #                         'height': 550,
        #                         'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
        #                     }
        #                 }
        #             ),
        #         ]),
        #         width={'size':10, 'offset':1 }
        #     ),
        # ]),
        # dbc.Row([
        #     dbc.Col(
        #         dcc.RadioItems(id='types', options=[
        #             {'label':'MED Licensed Transporters','value':'MED Licensed Transporters'},
        #             {'label':'MED Licensed Center','value':'MED Licensed Center'},
        #             {'label':'MED Licensed Cultivator','value':'MED Licensed Cultivator'},
        #             {'label':'MED Licensed Infused Product Manufacturer','value':'MED Licensed Infused Product Manufacturer'},
        #             {'label':'MED Licensed R&D Cultivation','value':'MED Licensed R&D Cultivation'},
        #             {'label':'MED Licensed Retail Operator','value':'MED Licensed Retail Operator'},
        #             {'label':'MED Licensed Testing Facility','value':'MED Licensed Testing Facility'},
        #             {'label':'MED Licensed Retail Marijuana Product Manufacturer','value':'MED Licensed Retail Marijuana Product Manufacturer'},
        #             {'label':'MED Licensed Retail Cultivator','value':'MED Licensed Retail Cultivator'},
        #             {'label':'MED Licensed Retail Testing Facility','value':'MED Licensed Retail Testing Facility'},
        #             {'label':'MED Licensed Retail Transporter','value':'MED Licensed Retail Transporter'},
        #             {'label':'MED Licensed Retail Marijuana Store','value':'MED Licensed Retail Marijuana Store'}
        #             ]),
        #         width = {'size': 10}),        
        # ],
        # justify='around',
        # ),
        # dbc.Row([
        #     dbc.Col(
        #         html.Div(id='table-container'),
        #     ),
        #     dbc.Col(
        #         dcc.Graph(id='map-2'),
        #     ),
        # ]),


        # dbc.Row([
        #     html.Div(id='none'),
        #         html.H1("")
        # ]),
        # dbc.Row([
        #     dbc.Col(
        #         html.Div(id='lic-name', style={'height':20, 'text-align': 'center'}),
        #     ),
        # ]),
        # dbc.Row([
        #     dbc.Col(
        #          html.Div(id='biz-name', style={'height':20, 'text-align': 'center'}),
        #     ),
        # ]),
        # dbc.Row([
        #     dbc.Col(
        #         html.Div(id='biz-type', style={'height':20, 'text-align': 'center'}),
        #     ),
        # ]),
        # dbc.Row([
        #     dbc.Col(
        #         html.Div(id='city', style={'height':20, 'text-align': 'center'}),
        #     ),
        # ]),
        # dbc.Row([
        #     dbc.Col(
        #         html.Div(id='address', style={'height':20, 'text-align': 'center'}),
        #     ),
        # ]),
        # dbc.Row([
        #     dbc.Col(
        #         html.Div(id='lic-num', style={'height':20, 'text-align': 'center'}),
        #     ),
        # ]),
        dbc.Row([
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
            dbc.Col(
                dcc.Graph(id='map',
                config={
                    'scrollZoom': True
                }),
                width={'size':7},
                
            ),
        ]),
        # dbc.Row([
            # dbc.Col(
            #     generate_table_categories(categories_table, max_rows=12),
            #     width = {'size':4, 'offset': 1}
            # ),
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
                width = {'size':5}
            ),
            dbc.Col(
                html.Table ([
                    html.Tr([html.Th('Stats')]),
                    html.Tr(html.Div(id='lics1-name', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='bizs-name', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='bizs1-type', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='citys', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='addresss', style={'height':30, 'text-align': 'center'})),
                    html.Tr(html.Div(id='lics-num', style={'height':30, 'text-align': 'center'})),
                ]),
                width = {'size':2}
            ),
        ]),
            
    
    #     def generate_table_categories(categories_table, max_rows=12):
    # return html.Table (
    #     [html.Tr([html.Th(col) for col in categories_table.columns])] +
    #     [html.Tr([
    #         html.Td(categories_table.iloc[i][col]) for col in categories_table.columns
    #         ]) for i in range(min(len(categories_table), max_rows))]
    # )
   
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
            zoom = 6.25,
            style = 'light'
        ),
        hovermode = 'closest',
        height = 550,
        margin = dict(r=0, l=0, t=0, b=0)
    )

    fig = dict(data=data, layout=layout)
    return fig

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
