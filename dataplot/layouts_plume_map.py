import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from .server import app

def plume_map():

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'

    plume_vertexs = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/plume_assets/plume_vertex_list_merged.csv')
    plume_vertexs = plume_vertexs.replace({np.nan:None})
    lons = plume_vertexs.Lons.values
    lats = plume_vertexs.Lats.values

    pwr_f = 'https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/plume_assets/global_power_plant_database.csv'

    ps_df = pd.read_csv(pwr_f)
    ps_df = ps_df[ps_df.primary_fuel.isin(['Gas','Oil','Coal'])]

    flare_df = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/plume_assets/flare_list_merged.csv')
    flare_df = flare_df.replace({np.nan:None})
    flare_lons = flare_df.Lons.values
    flare_lats = flare_df.Lats.values

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        mode = "markers",
        name = 'Power Stations',
        lon = ps_df.longitude,
        lat = ps_df.latitude,
        hoverinfo = 'none',
        marker = {'color':'red', 'opacity':0.8,
            'size':5}))

    fig.add_trace(go.Scattermapbox(
        mode = "lines", fill = "toself",
        name = 'Nighttime Flaring',
        lon = flare_lons,
        lat = flare_lats,
        hoverinfo = 'none',
        marker = {'color':'#e07509'}))

    fig.add_trace(go.Scattermapbox(
        mode = "lines", fill = "toself",
        name = 'NO<sub>2</sub> Plumes',
        lon = lons,
        lat = lats,
        hoverinfo = 'none',
        marker = {'color':'#006391'}))


    fig.update_layout(mapbox = {'style': "stamen-terrain", 'center': {'lon': 0, 'lat': 30}, 'zoom': 2})
    fig.update_layout(mapbox_style="satellite-streets",mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, autosize = True)
    fig.update_layout(legend=dict(
        title = 'Click to show/hide',
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    page_layout = html.Div(id ='full_page_container', children = [
        html.Div([
        html.Div(className = 'plume-header', children = [
            html.Div(id = 'home-logo-holder', children = [html.A(id = 'home-logo', href="/")]),

        html.Div(id = 'imgs',children = [
        html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/plume_assets/plume_0008.png?raw=true', style={'height':'60px', 'width':'60px','padding':'1px','display': 'inline-block'}),
        html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/plume_assets/plume_0141.png?raw=true', style={'height':'60px', 'width':'60px','padding':'1px','display': 'inline-block'}),
        html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/plume_assets/plume_0165.png?raw=true', style={'height':'60px', 'width':'60px','padding':'1px','display': 'inline-block'}),
        html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/plume_assets/plume_0299.png?raw=true', style={'height':'60px', 'width':'60px','padding':'1px','display': 'inline-block'}),
        html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/plume_assets/plume_0330.png?raw=true', style={'height':'60px', 'width':'60px','padding':'1px','display': 'inline-block'}),
        html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/plume_assets/plume_0367.png?raw=true', style={'height':'60px', 'width':'60px','padding':'1px','display': 'inline-block'}),
        ], style={'margin-left': '33%', 'width':'372px','display': 'inline-block'}),

        html.Div(id = 'logos',children = [
        html.A(href = 'https://nerc.ukri.org', children = [
            html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/nerc_logo.png?raw=true', style={'height':'40px','margin':'10px',})]),
        html.A(href = 'https://www.nceo.ac.uk', children = [
        html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/nceo_logo.png?raw=true', style={'height':'40px','margin':'10px'})]),
        ], style={'float': 'right','margin-right':'5px','display': 'inline-block'}),

        ],style={'width':'100%', 'height':'70px', 'justify-content': 'center', 'positon':'relative'}),

        html.H2('Satellites reveal anthropogenic combustion hotspots across the globe', style={'textAlign': 'center'}),
        dcc.Markdown('''
        The map shows the location of nitrogen dioxide (NO<sub>2</sub>) plumes that have been detected automatically
         by a deep learning model from observations collected by the [TROPOMI](http://www.tropomi.eu)
         instrument on board the Sentinel 5P satellite.
         Nitrogen dioxide is a proxy for combustion so the location of the plumes tell us about combustion hotspots,
         e.g. urban centres, power stations, biomass burning.
        ''',dangerously_allow_html = True),
        dcc.Markdown('''
        We are showing the results from analysing two years of satellite observations. We have attempted
        to remove the influence of biomass burning using thermal anomaly data collected by the
        [VIIRS](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/viirs-i-band-active-fire-data) satellite,
        although some fires may have slipped through the filter. The remaining plumes we attribute
        to specific combustion sources using other information: locations of power stations are also
        shown in red (data from [Global Power Plant Database](https://datasets.wri.org/dataset/globalpowerplantdatabase))
         and areas of nighttime oil and gas flaring are
        shown in orange (data from [SkyTruth](https://skytruth.org/flaring/)). Check out the ship tracks,
        especially around Spain, across the
        Mediterranean, and along the Suez Canal.
        '''),
        dcc.Markdown('''
        As you scroll inwards you’ll see the plumes have difference shapes - this is a result of overlapping plumes.
        '''),
        dcc.Markdown('''
         It is also important to note that the NO<sub>2</sub> data are sensitive to cloud cover and therefore the
         cloudier a place is (e.g. tropical regions) the less likely there it is for there to be clear
         observations and therefore the fewer plumes can be observed. Nevertheless, there is no shortage
         of plumes over the tropics.
        ''',dangerously_allow_html = True),
        dcc.Markdown('''
        More information, including methods and analysis can be found in our paper (link coming soon).
        '''),
        html.Hr(),
        dcc.Graph(figure=fig, style={'width': '100%', 'height': '90vh'}),
        html.Hr(),
        # html.Button('Map View',id = 'map_view'),
    ],style={'display': 'inline-block','padding':'8px','width': '100%', 'height': '100hv'})
    ])

    return page_layout