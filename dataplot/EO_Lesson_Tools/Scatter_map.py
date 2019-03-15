
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd


def satellite_scatter():
    mapbox_access_token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'
    brightness = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/T4_wavelenght.csv', header = None)
    lats = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/lats.csv', header = None)
    lons = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/lons.csv', header = None)

    data = [
    go.Scattermapbox(
        lat=lats[0],
        lon=lons[0],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=3,
            symbol = 'square',
            color=brightness[0]
        ),
    )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=-15,
                lon=142
            ),
            pitch=0,
            zoom=3
        ),
    )

    fig = dcc.Graph(id = 'fire_mapbox',
        figure = {'data':data, 'layout':layout})
        
    return fig

def fire_loc_map():


    mapbox_access_token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'
    fire_locs = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/fire_locs.csv', header = None)

    data = [
    go.Scattermapbox(
        lat=fire_locs.Lats,
        lon=fire_locs.Lons,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=3,
            color='red'
        ),
    )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=-15,
                lon=142
            ),
            pitch=0,
            zoom=3
        ),
    )

    fig = dcc.Graph(id = 'fire_mapbox',
        figure = {'data':data, 'layout':layout})
    print(fig)
    return fig
