import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html

def load_plume_data():

    plume_vertexs = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/plume_assets/plume_vertex_list_merged.csv')
    # plume_vertexs = plume_vertexs.replace({np.nan:None})
    plume_lons = plume_vertexs.Lons.values
    plume_lats = plume_vertexs.Lats.values
    return plume_lons,plume_lats

def load_ps_data():

    pwr_f = 'https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/plume_assets/global_power_plant_database.csv'

    ps_df = pd.read_csv(pwr_f, usecols = ['longitude','latitude','primary_fuel'])
    ps_df = ps_df[ps_df.primary_fuel.isin(['Gas','Oil','Coal'])]

    ps_lons = ps_df.longitude.values
    ps_lats = ps_df.latitude.values

    return ps_lons, ps_lats

def load_flare_data():

    flare_df = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/plume_assets/flare_list_merged.csv')
    # flare_df = flare_df.replace({np.nan:None})
    flare_lons = flare_df.Lons.values
    flare_lats = flare_df.Lats.values

    return flare_lons,flare_lats

def render_map(map_style = 'satellite-streets'):
    token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'

    plume_lons,plume_lats = load_plume_data()
    ps_lons,ps_lats = load_ps_data()
    flare_lons,flare_lats = load_flare_data()

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        mode = "markers",
        name = 'Power Stations',
        lon = ps_lons,
        lat = ps_lats,
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
        lon = plume_lons,
        lat = plume_lats,
        hoverinfo = 'none',
        marker = {'color':'#006391'}))


    fig.update_layout(mapbox = {'style': "stamen-terrain", 'center': {'lon': 0, 'lat': 30}, 'zoom': 2})
    fig.update_layout(mapbox_style=map_style,mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, autosize = True)
    fig.update_layout(legend=dict(
        title = 'Click to show/hide',
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig
