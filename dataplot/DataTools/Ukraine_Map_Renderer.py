import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html

def load_fire_data(app):
    modis_df = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_7d.csv')

    viirs_snpp = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_7d.csv')
    viirs_noaa = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_7d.csv')

    firms_df = pd.concat([modis_df,viirs_snpp,viirs_noaa])

    firms_df = firms_df[(firms_df.latitude > 44) & (firms_df.latitude < 52.5) & (firms_df.longitude > 21.5) & (firms_df.longitude < 40.5)]
    firms_df.index = = pd.to_datetime(ukr_fires.acq_date,format = '%Y-%m-%d')
    firms_df = firms_df.loc['2022-02-24':]

    return  firms_df.longitude, firms_df.latitude


def render_map(app, map_style = 'satellite-streets'):
    token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'

    fire_lons,fire_lats = load_fire_data(app)

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        mode = "markers",
        name = 'Fires Detected',
        lon = fire_lons,
        lat = fire_lats,
        hoverinfo = 'none',
        marker = {'color':'red', 'opacity':0.8,
            'size':10}))


    fig.update_layout(mapbox = {'style': "stamen-terrain", 'center': {'lon': 30.577133, 'lat': 50.414894}, 'zoom': 6})
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
