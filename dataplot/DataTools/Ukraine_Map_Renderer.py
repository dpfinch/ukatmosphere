import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd
import numpy as np
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html

def load_fire_data(app):
    modis_df = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_7d.csv')

    viirs_snpp = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_7d.csv')
    viirs_noaa = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_7d.csv')

    firms_df = pd.concat([modis_df,viirs_snpp,viirs_noaa])
    firms_gdf = gpd.GeoDataFrame(firms_df, geometry = gpd.points_from_xy(firms_df.longitude, firms_df.latitude))

    shapefile = app.get_asset_url('ne_10m_admin_0_countries.shp')

    world_gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    ukraine_poly = world_gdf[world_gdf.ADMIN == 'Ukraine']

    ukr_fires = firms_gdf[firms_gdf.geometry.within(ukraine_poly.geometry.iloc[0])]
    return  ukr_fires.longitude, ukr_fires.latitude


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


    fig.update_layout(mapbox = {'style': "stamen-terrain", 'center': {'lon': 30.577133, 'lat': 50.414894}, 'zoom': 12})
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
