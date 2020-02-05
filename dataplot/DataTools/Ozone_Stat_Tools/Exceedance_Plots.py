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
    Info about Exceedance plots will go here
'''

def total_exceedances(df,resample = 'year',**kwargs):

    if resample == 'year':
        resampled_df = df.resample('Y').sum()
        ytitle = 'Total Number of Exceedances'
        x=resampled_df.index.year
    if resample == 'month':
        resampled_df = df.groupby(df.index.month).sum()
        resampled_df = resampled_df/resampled_df.sum().sum() * 100
        ytitle = 'Percentage of Total Exceedances'
        x=resampled_df.index
    if resample == 'week day':
        resampled_df = df.groupby(df.index.dayofweek).sum()
        resampled_df = resampled_df/resampled_df.sum().sum() * 100
        ytitle = 'Percentage of Total Exceedances'
        x=resampled_df.index

    bars = []

    for env_type in resampled_df.columns:
        bars.append(go.Bar(name=env_type,
            x=x,
            y=resampled_df[env_type].values))


    layout = {
        'barmode':'stack',
        'title':kwargs['title'],
        'xaxis':{'title':resample.title()},
        'yaxis':{'title':ytitle}
    }
    fig = dcc.Graph(figure = {'data': bars,
        'layout':layout})

    return fig

def yearly_sites_exceeding(df, **kwargs):

    bars = []
    for env_type in df.columns:
        bars.append(go.Bar(name=env_type,
            x=df.index.year,
            y=df[env_type].values))


    layout = {
        'barmode':'stack',
        'title':kwargs['title'],
        'xaxis':{'title':'Year'},
        'yaxis':{'title':'Number of Sites Breaking Annual Ozone Limit'}
    }
    fig = dcc.Graph(figure = {'data': bars,
        'layout':layout})

    return fig
