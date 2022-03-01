import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np
import plotly.graph_objects as go
from .server import app, queue


def fire_map():

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    page_layout = html.Div(id ='full_page_container', children = [
        html.Div([
        html.Div(className = 'plume-header', children = [
        ],style={'width':'100%', 'height':'70px', 'justify-content': 'center', 'positon':'relative'}),]),
        html.Div(className = 'page-body',children = [
        html.H2('Fires Spotted over Ukraine', style={'textAlign': 'center'}),
        dcc.Markdown('''
         Fires spotted within the last seven days over Ukraine from the [FIMRS satellite products](https://firms.modaps.eosdis.nasa.gov).
         These fires could be related to recent military activity in the area.
        ''',dangerously_allow_html = True),
        dcc.Markdown('''
         It is important to note that this satellite product does not capture all fires and will have some false detections. Also many of these fires will not be related to military activity.
        ''',dangerously_allow_html = True),
        html.Hr(),
        dcc.Loading(id='loading_plume_map',children=[
        html.Div(id = 'fire_map_holder',style={'width': '90%', 'height': '90vh'})],
        type="graph"),
        html.Br(),
        daq.ToggleSwitch(id = 'fire_map_toggle', value = True,
            label='Switch to map view',labelPosition='bottom'),
        html.Hr(),
        # html.Button('Map View',id = 'map_view'),
    ],style={'display': 'inline-block','padding':'8px','width': '100%', 'height': '100hv'})
    ])

    return page_layout
