import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np
import plotly.graph_objects as go
from .server import app, queue


def plume_map():

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
        html.A(href = 'http://www.tropomi.eu', children = [
            html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/TROPOMI_logo.jpg?raw=true', style={'height':'50px','margin':'10px',})]),
        html.A(href = 'https://nerc.ukri.org', children = [
            html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/nerc_logo.png?raw=true', style={'height':'40px','margin':'10px',})]),
        html.A(href = 'https://www.nceo.ac.uk', children = [
            html.Img(src = 'https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/nceo_logo.png?raw=true', style={'height':'40px','margin':'10px'})]),
        ], style={'float': 'right','margin-right':'5px','display': 'inline-block'}),

        ],style={'width':'100%', 'height':'70px', 'justify-content': 'center', 'positon':'relative'}),]),
        html.Div(className = 'page-body',children = [
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
        dcc.Markdown('''
        Contact: Doug Finch [email](mailto:d.finch@ed.ac.uk) & [Twitter](https://twitter.com/douglasfinch)
        [<img src="https://github.com/dpfinch/ukatmosphere/blob/master/dataplot/assets/twitter_logo.png?raw=true" width="20px"/>](https://twitter.com/douglasfinch)''',
        dangerously_allow_html = True),
        html.Hr(),
        dcc.Loading(id='loading_plume_map',children=[
        html.Div(id = 'plume_map_holder',style={'width': '100%', 'height': '90vh'})],
        type="graph"),
        html.Br(),
        daq.ToggleSwitch(id = 'map_toggle', value = True,
            label='Switch to map view',labelPosition='bottom'),
        html.Hr(),
        # html.Button('Map View',id = 'map_view'),
    ],style={'display': 'inline-block','padding':'8px','width': '100%', 'height': '100hv'})
    ])

    return page_layout
