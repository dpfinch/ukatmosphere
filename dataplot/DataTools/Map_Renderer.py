import plotly.graph_objs as go
import pandas as pd
from dataplot.DataTools import LoadData
import numpy as np
from datetime import datetime

def main_site_map(environment, region, species):
    mapbox_access_token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'
    # site_df = LoadData.get_all_site_info(environment, region)

    # random_sizes = np.random.randint(20, size = len(site_df))
    # For the time being lets just set variable and time
    date= datetime(2017,12,14,12)
    variable = species

    vals_df = LoadData.all_sites_one_var_data(date, variable, region, environment)
    unit = LoadData.Get_Unit('AURN', species)

    size_scale = 1
    variable_vals = vals_df.value * size_scale

    hover_text = ['%s: %.3f %s' % (vals_df.index.tolist()[x],variable_vals[x], unit) for x in range(len(variable_vals))]

    data = [go.Scattermapbox(
        lat=vals_df.latitude.tolist(),
        lon=vals_df.longitude.tolist(),
        mode='markers',
        # customdata = final_df.index.tolist(),
        marker=go.scattermapbox.Marker(
            color=variable_vals.tolist(),
            colorscale='Viridis',
            showscale=True,
            size = 14,
            colorbar=dict(
                title= species + ' ' + unit,
                titleside = 'right'
            ),
            # opacity = 0.85,
            # color = chosen_hour,
            # cmax = last_day.max(axis = 1).max(),
            # colorbar = {'title':var_choice}
        ),
        text=hover_text,
        )]

    layout = go.Layout(
        showlegend = False,
        autosize=True,
        # showlegend = True,
        height = 750,
        hovermode='closest',
        margin = {'l':0.2,'r':0.2, 't':0.2, 'b':0.2},
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=55,
                lon=-3.2
            ),
            pitch=0,
            zoom=4.5
        ),
    )


    fig = dict(data=data, layout=layout)

    return len(vals_df),fig
