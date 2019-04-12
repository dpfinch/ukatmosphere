import plotly.graph_objs as go
import pandas as pd
from dataplot.DataTools import LoadData

def main_site_map(environment, region):
    mapbox_access_token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'
    site_df = LoadData.get_all_site_info(environment, region)

    data = [go.Scattermapbox(
        lat=site_df.latitude.tolist(),
        lon=site_df.longitude.tolist(),
        mode='markers',
        # customdata = final_df.index.tolist(),
        marker=go.scattermapbox.Marker(
            size=9,
            # opacity = 0.85,
            # color = chosen_hour,
            # cmax = last_day.max(axis = 1).max(),
            # colorbar = {'title':var_choice}
        ),
        text=site_df.index.tolist(),
        )]

    layout = go.Layout(
        autosize=True,
        height = 750,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=54,
                lon=-3
            ),
            pitch=0,
            zoom=4
        ),
    )


    fig = dict(data=data, layout=layout)

    return len(site_df),fig

def test_map():
    mapbox_access_token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'
    data = [
    go.Scattermapbox(
        lat=['38.91427','38.91538','38.91458',
             '38.92239','38.93222','38.90842',
             '38.91931','38.93260','38.91368',
             '38.88516','38.921894','38.93206',
             '38.91275'],
        lon=['-77.02827','-77.02013','-77.03155',
             '-77.04227','-77.02854','-77.02419',
             '-77.02518','-77.03304','-77.04509',
             '-76.99656','-77.042438','-77.02821',
             '-77.01239'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=["The coffee bar","Bistro Bohem","Black Cat",
             "Snap","Columbia Heights Coffee","Azi's Cafe",
             "Blind Dog Cafe","Le Caprice","Filter",
             "Peregrine","Tryst","The Coupe",
             "Big Bear Cafe"],
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38.92,
                lon=-77.07
            ),
            pitch=0,
            zoom=10
        ),
    )

    fig =  dict(data=data, layout=layout)
    return fig
