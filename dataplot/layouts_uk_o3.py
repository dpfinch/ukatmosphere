from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData


def uk_ozone():
    ## Get the sites availble from the DEFRA AURN network
    site_regions = LoadData.AURN_regions()
    region_choices = ['All'] + site_regions
    region_options = [{'label': i.strip(), 'value': i.strip()} for i in region_choices]

    site_envs = LoadData.AURN_environment_types()
    env_choices = ['All'] + site_envs
    env_options = [{'label': i.strip(), 'value': i.strip()} for i in env_choices]

    #### Start the page layout
    page_layout = html.Div(id = 'full_page_container', children =
    ### The first items are for the common attributes (ie site)
    [
    html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'home-logo', href="/")]),
        html.Div(id = 'page-header-holder', children = [html.A('UK Atmosphere',id = "page-header-text", href = "/")]),
    ]),
    html.Div(className = 'page-body',children = [
    html.H3('Analysis for UK ozone from DEFRA AURN sites.'),
    html.Br(),

    html.Label('Select a region:'),
    dcc.Dropdown(id = 'o3_region_choice',
        multi = True,
        options = region_options,
        value = 'All'),
    html.Br(),

    html.Label('Select an environment type:'),
    dcc.Dropdown(id = 'o3_env_choice',
        multi = True,
        options = env_options,
        value = 'All'),
    html.Br(),

        html.Label('Select a range of years:'),
        dcc.Dropdown(
            id = 'o3_minimum_year',
            placeholder = 'Select start year...',
        ),
        html.P('To'),
        dcc.Dropdown(
            id = 'o3_maximum_year',
            placeholder = 'Select end year...',
        ),
        html.Br(),
        html.Button('GO', id = 'o3_go_button'),
        html.Br(),
        html.Br(),

        ###  Create a div to place the dataframe while its being used but not
        ### viewable by the user. Make data Json - very slow when being read
        html.Div(id = 'o3_dataframe-holder', style = {'display': 'none'}),

        ### Each placeholder for plots and their individual controls go below
        ### **************************  TimeSeries  ***************************
        html.Div(id = 'O3_TimeSeriesHolder', className = 'plot_holder', children = [
            html.Div(id = 'O3_TimeSeries', className = 'main_plot'),
            html.Div(id = 'TimeSeriesTools', className = 'plot_tools', children = [
                html.H3('Time Series Tools:'),
                html.Br(),
                html.Label('Plot Title'),
                dcc.Input( id = 'O3_TimeSeriesTitle',
                    placeholder = 'Enter Title',
                    value = ''),
                html.Br(),
                html.Label('X Axis Label'),
                dcc.Input( id = 'O3_TimeSeriesXTitle',
                    placeholder = 'Enter X axis label',
                    value = 'Date'),
                html.Br(),
                html.Label('Y Axis Label'),
                dcc.Input( id = 'O3_TimeSeriesYTitle',
                    placeholder = 'Enter Y axis label',
                    value = ''),
                html.Br(),
                dcc.RadioItems(id = 'O3_TimeSeriesLabelFormat',
                    options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
                    value = 'Variable Name'),
                html.Br(),
                html.Label('Add a rolling mean'),
                dcc.Checklist(id = 'O3_TimeSeriesRollingMean',
                    values = [],
                ),
                html.Br(),
                dcc.RadioItems(id = 'O3_TimeSeriesLineOrScatter',
                options = [{'label': i, 'value': i} for i in ['Scatter', 'Line', 'Line & Scatter']],
                value = 'Scatter',
                ),
            ])
        ]),
        html.Hr(),
        html.Div(
    children=[
        html.H3("Edit text input to see loading state"),
        dcc.Input(id="input-1", value='Input triggers local spinner'),
        dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="graph")#, fullscreen = True)
        ])
    ])])
    return page_layout


### ===================================================================
### END OF PROGRAM
### ===================================================================
