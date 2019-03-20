
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np


def satellite_scatter(value, removed_310K, cloud_mask, fires_on):
    mapbox_access_token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'
    data_dirc = 'https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/{}_wavelenght.csv'

    brightness = pd.read_csv(data_dirc.format(value),
        header = None)[0]

    lats = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/lats.csv', header = None)[0]
    lons = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/lons.csv', header = None)[0]

    if removed_310K:
        t4 = pd.read_csv(data_dirc.format('T4'),
        header = None)
        lats = lats[t4[0]>310]
        lons = lons[t4[0]>310]
        brightness = brightness[t4[0]>310]

    if cloud_mask:
        t12 = pd.read_csv(data_dirc.format('T12'), header = None)[0]
        p65 = pd.read_csv(data_dirc.format('p65'), header = None)[0]
        p86 = pd.read_csv(data_dirc.format('p86'), header = None)[0]
        cloud_mask1 = p65 + p86 > 0.9
        cloud_mask2 = t12 < 265
        cloud_mask3 =(p65+p86 >0.7) & (t12<300)
        brightness[cloud_mask1+cloud_mask2+cloud_mask3] = np.nan
        lats[cloud_mask1+cloud_mask2+cloud_mask3] = np.nan
        lons[cloud_mask1+cloud_mask2+cloud_mask3] = np.nan

    data = [
    go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5,
            color=brightness,
            cmax = brightness.max(),
            colorbar=dict(title = 'Temperature',
                titleside = 'right')
            ),
        text = brightness
        ),
    ]

    if fires_on:
        fire_locs = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/fire_locs.csv')
        data.append(
            go.Scattermapbox(
            lat = fire_locs.Fire_Lats,
            lon = fire_locs.Fire_Lons,
            mode = 'markers',
            marker = go.scattermapbox.Marker(
                symbol = 'circle-stroked'
            )
            )
        )


    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,

            center=go.layout.mapbox.Center(
                lat=-24,
                lon=143
            ),
            pitch=0,
            zoom=3.7,
        ),
        height = 700,
        width = 700
    )

    fig = dcc.Graph(id = 'fire_mapbox',
        figure = {'data':data, 'layout':layout},
                config={
                'scrollZoom': True
            })

    return fig


def simple_map(value, removed_310K, cloud_mask, fires_on, coastline_data):
    data_dirc = 'https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/{}_wavelenght.csv'
    coastline = pd.read_json(coastline_data, orient = 'split')

    brightness = pd.read_csv(data_dirc.format(value),
        header = None)[0]

    lats = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/lats.csv', header = None)[0]
    lons = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/lons.csv', header = None)[0]

    if removed_310K:
        t4 = pd.read_csv(data_dirc.format('T4'),
        header = None)
        lats = lats[t4[0]>310]
        lons = lons[t4[0]>310]
        brightness = brightness[t4[0]>310]

    if cloud_mask:
        t12 = pd.read_csv(data_dirc.format('T12'), header = None)[0]
        p65 = pd.read_csv(data_dirc.format('p65'), header = None)[0]
        p86 = pd.read_csv(data_dirc.format('p86'), header = None)[0]
        cloud_mask1 = p65 + p86 > 0.9
        cloud_mask2 = t12 < 265
        cloud_mask3 =(p65+p86 >0.7) & (t12<300)
        brightness[cloud_mask1+cloud_mask2+cloud_mask3] = np.nan
        lats[cloud_mask1+cloud_mask2+cloud_mask3] = np.nan
        lons[cloud_mask1+cloud_mask2+cloud_mask3] = np.nan

    data = []

    data.append(
        go.Scattergl(
        x = lons,
        y = lats,
        mode='markers',
        marker = {'color':brightness,
            'showscale':True,
        },
        name = value
        ))

    if fires_on:
        fire_locs = pd.read_csv('https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/fire_locs.csv')
        data.append(
            go.Scattergl(
            y = fire_locs.Fire_Lats,
            x = fire_locs.Fire_Lons,
            mode = 'markers',
            marker = {'symbol':'hexagon-open'}
            )
            )

    data.append(
        go.Scattergl(
        x = coastline.Lon,
        y = coastline.Lat,
        mode = 'lines',
        line = {'color':'black',
            'width':1},
        name = 'Coastline'
        )
    )

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        height = 700,
        width = 800,
        showlegend = False,
    )

    fig = dcc.Graph(id = 'simple_sat_map',
        figure = {'data':data, 'layout':layout},
            config={
            'scrollZoom': True
            })


    return fig
