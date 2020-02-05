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
from dataplot.models import measurement_info
import numpy as np
import pandas as pd
#==============================================================================


'''
    Info about TimeSeries will go here
'''

def TimeSeries(df, site_info,**kwargs):
    table_data = site_info['props']['children'][2]['props']['data']
    sites = []
    env_type = []
    region = []
    for row in table_data:
        sites.append(row['Site Name'])
        env_type.append(row['Environment'])
        region.append(row['Region'])

    sites_df = pd.DataFrame({'Region':region,'Environment':env_type},
        index = sites)

    if kwargs['env_or_region'] == 'Environment Type':
        iterator = sites_df.Environment.unique()
    if kwargs['env_or_region'] == 'Region':
        iterator = sites_df.Region.unique()

    if kwargs['lineorscatter'] == 'Line':
        line_mode = 'lines'
    elif kwargs['lineorscatter'] == 'Line & Scatter':
        line_mode = 'lines+markers'
    else:
        line_mode = 'markers'

    all_plots = []

    for i in iterator:

        if kwargs['env_or_region'] == 'Environment Type':
            sites_subset = sites_df[sites_df.Environment == i]
        if kwargs['env_or_region'] == 'Region':
            sites_subset = sites_df[sites_df.Region == i]

        df_subset = df[sites_subset.index]

        if kwargs['value_type'] == 'Annual Minimum':
            df_stats = df_subset.min(axis = 1)
        elif kwargs['value_type'] == 'Annual Maximum':
            df_stats = df_subset.max(axis = 1)
        else:
            df_stats = df_subset.mean(axis = 1)

        x = df_stats.index
        all_plots.append(go.Scatter(
        x = x,
        y = df_stats.values,
        mode = line_mode,
        name = i
        ))

    xtitle = kwargs['xtitle']
    ytitle = kwargs['ytitle']

    plot_title = kwargs['title']

    plot_layout = {'title':plot_title,
        'xaxis' : {'title':xtitle,
            # 'rangeslider':{},
            # 'type':'date'
            },
        'yaxis' : {'title':ytitle},
        }

    plot = dcc.Graph(
        id='O3_TimeSeriesPlot',
        figure={
            'data': all_plots,
            'layout': plot_layout
        }
    )
    return plot
