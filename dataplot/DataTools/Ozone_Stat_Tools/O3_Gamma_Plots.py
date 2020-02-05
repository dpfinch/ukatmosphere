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
from plotly.subplots import make_subplots
#==============================================================================


'''
    Info about Gamme plots will go here
'''


def GammaPlot(gamma_dict,**kwargs):
    fig = make_subplots(rows =2, cols = 3, shared_xaxis = True, shared_yaxis = True)
    all_plots = []
    for n,env in enumerate(gamma_dict.keys):
        x = gamma_dict[env].alpha.values
        y = gamma_dict[env].beta.values
        all_plots.append(go.Scatter(
        x = x,
        y = x,
        name = env,
        mode = 'markers'
        ),row = n%2,
        col = n%3)

    plot_layout = {'title':kwargs['title'],
        }

    plot = dcc.Graph(figure = {
        'data':all_plots,
        'layout':plot_layout
    })

    return plot
