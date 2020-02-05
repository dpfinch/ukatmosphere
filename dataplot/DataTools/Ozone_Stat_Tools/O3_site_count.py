#==============================================================================
# Description of module here
#
#==============================================================================
# Uses modules:
# modulename
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
#==============================================================================


'''
    Info about O3 site count will go here
'''

def site_count_timeseries(site_count_df, **kwargs):
    all_plots = []

    for col in site_count_df.columns:
        all_plots.append(go.Scatter(
            x = site_count_df.index,
            y = site_count_df[col],
            mode = 'lines',
            name = col
        ))
    plot_layout = {
        'title':kwargs['plot_title'],
        'xaxis':{'title': 'Year'},
        'yaxis':{'title': 'Number of open AURN sites'}
    }
    plot = dcc.Graph(
        id = 'site_count_plot',
        figure = {'data':all_plots,
                'layout':plot_layout}
    )
    return plot
