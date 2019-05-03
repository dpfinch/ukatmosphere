import plotly.graph_objs as go
import pandas as pd
from dataplot.DataTools import LoadData
import numpy as np
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html


def Site_Summary(site_name, species):
    site_object = LoadData.get_site_info_object(site_name)
    site_variables_list = LoadData.Get_Site_Variables(site_name)

    for v in site_variables_list:
        if 'modelled' in v.lower().split():
            site_variables_list.remove(v)
        if 'temperature' in v.lower().split():
            site_variables_list.remove(v)
        if 'pressure' in v.lower().split():
            site_variables_list.remove(v)

    if site_object.environment_type.lower()[0] in ['a','e','i','o','u']:
        prefix = 'an'
    else:
        prefix = 'a'

    summary = html.Div(id = 'site_summary', children = [
    html.Br(),
    html.P('%s is %s %s site in the %s region, opened in %s.' %(
        site_name, prefix, site_object.environment_type.lower(), site_object.region, site_object.date_open.year) ),
    html.Br(),
    html.P('This is a %s site measuring the following species:' % site_object.site_type),
    html.Ul([html.Li(x) for x in site_variables_list])
    ])

    return summary


def Site_Week_Summary(site_name, species):
    df= LoadData.get_recent_site_data(site_name, species, days_ago = 7)

    plot = [go.Scatter(
     x = df.index,
     y = df.Concentration.values,
     mode = 'lines',
     name = species
    )]

    plot_title = '%s at %s between %s and %s' %(species, site_name, df.index[0].date(), df.index[-1].date())
    #  Find the unit for the species

    unit = LoadData.Get_Unit('AURN', species)
    ytitle = '%s (%s)' % (species, unit)
    layout = {'title':plot_title,
        'xaxis':{'title': 'Date'},
        'yaxis':{'title':ytitle}}

    plot = dcc.Graph(
    id = 'map_site_timeseries',
    figure = {
        'data':plot,
        'layout':layout
            }
        )

    return plot


def Site_Year_Summary(site_name, species):
    return 'Year stats for %s' %site_name
