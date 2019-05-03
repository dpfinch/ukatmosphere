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

    all_species = LoadData.get_all_aurn_species()
    species_options = [{'label': i.strip(), 'value': i.strip()} for i in all_species]

    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'home-logo', href="/")]),
        html.Div(id = 'page-header-holder', children = [html.A('UK Atmosphere',id = "page-header-text", href = "/")]),
    ]),
    html.Div(className = 'page-body',children = [
    html.Div(className = 'map_data_selection', children = [
    html.Label('Select an environment:'),
    dcc.Dropdown(id = 'map_env_choice',
        multi = False,
        options = env_options,
        value = 'All'),
    html.Br(),
    html.Label('Select a region:'),
    dcc.Dropdown(id = 'map_region_choice',
        multi = False,
        options = region_options,
        value = 'All'),
    html.Br(),
    html.Label('Select a species:'),
    dcc.Dropdown(id = 'map_species_choice',
        multi = False,
        options = species_options,
        value = 'Ozone'),
    html.Br(),
    ]),
    # Map layout will go here
    html.Div(id = 'map_output_holder', children = [
    html.Div(id = 'main_map_holder', children = [
        html.Div(id = 'site_counter_output'),
        dcc.Graph(id = 'main_map', config = {'scrollZoom': True},
        )
    ]),
    html.Div(id = 'site_plot_from_map', children = [
    html.H4(id = 'site_name_from_map'),
    dcc.Tabs(id="map_tabs", value='site_sum', children=[
        dcc.Tab(label='Site Summary', value='site_sum'),
        dcc.Tab(label='Last 7 Days', value='site_week'),
        dcc.Tab(label='Yearly Stats', value='yearly_stats'),
    ]),
    html.Div(id = 'map_site_info'),
    ]),
    ])
    ])
    ])

    return page_layout


### ===================================================================
### END OF PROGRAM
### ===================================================================
