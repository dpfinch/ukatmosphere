from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData


def DEFRA_map_page():

    site_regions = LoadData.AURN_regions()
    region_choices = ['All'] + site_regions
    region_options = [{'label': i.strip(), 'value': i.strip()} for i in region_choices]

    site_envs = LoadData.AURN_environment_types()
    env_choices = ['All'] + site_envs
    env_options = [{'label': i.strip(), 'value': i.strip()} for i in env_choices]

    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'home-logo', href="/")]),
        html.Div(id = 'page-header-holder', children = [html.A('UK Atmosphere',id = "page-header-text", href = "/")]),
    ]),
    html.Div(className = 'page-body',children = [
    html.Div([
    html.H4('Select a region'),
    html.Div([dcc.Dropdown(
        id = 'map_region_choice',
        options = [{'label': i, 'value': i} for i in region_choices],
        value = 'All',
##        multi = True,
        )]),
    html.Br(),

    html.H4('Select an environment type'),
    html.Div([dcc.Dropdown(
        id = 'map_env_choice',
        options = [{'label': i, 'value': i} for i in env_choices],
        value = 'All',
##        multi = True,
        )]),
    html.Br(),

    # html.H4('Select a variable'),
    # html.Div([dcc.Dropdown(
    #     id = 'var_choice',
    #     options = [{'label': i, 'value': i} for i in avail_vars],
    #     value = 'Nitrogen dioxide ',
    #     )]),
    # html.Br(),

    html.Div([dcc.Slider(
        id = 'map_hour_slider',
        min = 0,
        max = 23,
        marks = {i: str(i).zfill(2)+':00' for i in range(24)},
        value = 12,
        )]),

    html.Br(),

    html.Div([dcc.Graph(id = 'main_graph_map')]),

    html.Br(),

##    html.Div([dcc.Graph(id = 'timeseries_plot')]),
    html.Div(id = 'timeseries_plot'),
    ], style = {'padding':40}),
    html.Br(),
    ])
    ]
    )




    return page_layout


### ===================================================================
### END OF PROGRAM
### ===================================================================
