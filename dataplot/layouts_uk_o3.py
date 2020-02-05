from random import randint
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
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
            value = 2000
        ),
        html.P('To'),
        dcc.Dropdown(
            id = 'o3_maximum_year',
            placeholder = 'Select end year...',
        ),
    html.Br(),
    daq.BooleanSwitch(id = 'o3_site_open', on = False,
        label = 'Only use sites currently open',
        labelPosition = 'top'),
    html.Br(),
    html.Button('Find Ozone Data', id = 'o3_go_button'),
    html.Br(),
    html.Br(),

    dcc.Loading(id="o3_meta_data_load", children=[
    html.Div(id = 'o3_meta_data_text')],type="dot"),

    html.Hr(),
    html.Button('Load Ozone Data', id = 'o3_load_button'),# disabled = True),
    html.Hr(),
    html.Div(id = 'o3_data_values_holder',children = [
    daq.GraduatedBar(id = 'o3_load_bar',
        size = 500,
        # max = 100,
        value = 0,
        showCurrentValue=True),
    html.Div(id = 'o3_dataframe-holder'),
    dcc.Interval(id = 'Interval',interval = 500),
    dcc.Store(id = 'load_id_store'),
    html.Div(id = 'loaded_sites2'),
    html.Div(id = 'tester_output')]),
    ###  Create a div to place the dataframe while its being used but not
    ### viewable by the user. Make data Json - very slow when being read
    html.Div(id = 'o3_metadata-holder', style = {'display': 'none'}),

    ### **************************  Site Count  ***************************
    html.Div(id = 'O3_SiteCountHolder', className = 'plot_holder', children = [
        dcc.Loading(id="loading-sitecount", children=[
            html.Div(id = 'O3_SiteCountPlot')],type="dot", className = 'main_plot'),
        html.Div(id = 'O3_SiteCountTools', className = 'plot_tools', children = [
        html.H3('Site Count Plot Tools:'),
        html.Br(),
        html.Label('Plot Title'),
        dcc.Input( id = 'O3_SiteCountTitle',
            placeholder = 'Enter Title',
            value = ''),
        html.Br(),
        html.Br(),
        html.Label('Spliy by:'),
        dcc.RadioItems(id = 'Site_Count_Split',
            options = [{'label': i, 'value': i} for i in ['Total', 'Environment Type','Region',]],
            value = 'Total'),
        html.Br(),
        ]),
    ]),
    html.Hr(),
    html.Br(),
    html.Label(),
    dcc.RadioItems(id = 'O3_Env_or_Regions',
    options = [{'label': i, 'value': i} for i in ['Environment Type', 'Region']],
    value = 'Environment Type',
    labelStyle={'display': 'inline-block'}),
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
                value = 'Year'),
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
            html.Label('Value Type'),
            dcc.RadioItems(id = 'O3_ValueType',
                options = [{'label': i, 'value': i} for i in ['Annual Mean', 'Annual Maximum','Annual Minimum']],
                value = 'Annual Mean'),
            html.Br(),
            html.Label('Line Type'),
            dcc.RadioItems(id = 'O3_TimeSeriesLineOrScatter',
            options = [{'label': i, 'value': i} for i in ['Scatter', 'Line', 'Line & Scatter']],
            value = 'Line & Scatter',
            ),
        ])
    ]),
    html.Hr(),
    ### *********************  Trend Table  *********************************
    html.Div(id = 'o3_trend_table'),
    html.Hr(),
    ### *********************  Gamma plot  *********************************
    html.Div(id = 'O3_Gamma_Plot_Holder', className = 'plot_holder', children = [
    html.Div(id = 'O3_Gamma_Plot', className = 'main_plot'),
        html.Div(id = 'O3_GammaTools', className = 'plot_tools', children = [
            html.H3('Gamma Plot Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'O3_GammaTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
        ]),
    ]),
    html.Hr(),

    ### *********************  YearlyExceed  *********************************
    html.Div(id = 'O3_YearlyExceedHolder', className = 'plot_holder', children = [
    html.Div(id = 'O3_YearlyExceed',className = 'main_plot'),
        # html.Div(id = 'Correlation', className = 'main_plot'),
        html.Div(id = 'O3_YearlyExceedTools', className = 'plot_tools', children = [
            html.H3('Yearly Exceedance Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'O3_YearlyExceedTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
        ]),
    ]),
    html.Hr(),

    ### *********************  Yearly siteExceed  *********************************
    html.Div(id = 'O3_YearlySiteExceedHolder', className = 'plot_holder', children = [
    html.Div(id = 'O3_YearlySiteExceed',className = 'main_plot'),
        # html.Div(id = 'Correlation', className = 'main_plot'),
        html.Div(id = 'O3_YearlySiteExceedTools', className = 'plot_tools', children = [
            html.H3('Yearly Site Exceedance Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'O3_YearlySiteExceedTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
        ]),
    ]),
    html.Hr(),

### *********************  MonthlyExceed *********************************
html.Div(id = 'O3_MonthlyExceedHolder', className = 'plot_holder', children = [
html.Div(id = 'O3_MonthlyExceed', className = 'main_plot'),
    # html.Div(id = 'DiurnalCycle', className = 'main_plot'),
    html.Div(id = 'O3_MonthlyExceedTools', className = 'plot_tools', children = [
        html.H3('Monthly Exceedance Tools:'),
        html.Br(),
        html.Label('Plot Title'),
        dcc.Input( id = 'O3_MonthlyExceedTitle',
            placeholder = 'Enter Title',
            value = ''),
        html.Br(),
        ]),
    ]),
    html.Hr(),


    ### *******************  WeeklyExceed  ***************************
    html.Div(id = 'O3_WeeklyExceedHolder', className = 'plot_holder', children = [
    html.Div(id = 'O3_WeeklyExceed',className = 'main_plot'),
        # html.Div(id = 'HourlyBoxplots', className = 'main_plot'),
        html.Div(id = 'O3_WeeklyExceedTools', className = 'plot_tools', children = [
            html.H3('Weekly Exceedance Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'O3_WeeklyExceedTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
        ]),
    ]),
    html.Br(),
    html.Hr(),

### *********************  ExceedMap *********************************
html.Div(id = 'ExceedMapHolder', className = 'plot_holder', children = [
html.Div(id = 'O3_ExceedMap', className = 'main_plot'),
    # html.Div(id = 'WeeklyCycle', className = 'main_plot'),
    html.Div(id = 'O3_ExceedMapTools', className = 'plot_tools', children = [
        html.H3('Exceedance Map Tools:'),
        html.Br(),
        html.Label('Plot Title'),
        dcc.Input( id = 'O3_ExceedMapTitle',
            placeholder = 'Enter Title',
            value = ''),
        html.Br(),

        ]),
    ]),
    html.Hr(),


    ])])
    return page_layout


### ===================================================================
### END OF PROGRAM
### ===================================================================
