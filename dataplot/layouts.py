from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input



def main_page():
    page_layout = html.Div(id = 'full_page_container', children =
    ### The first items are for the common attributes (ie site)
    [
    html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'home-logo', href="/")]),
        html.Div(id = 'page-header-holder', children = [html.A('UK Atmosphere',id = "page-header-text", href = "/")]),
    ]),
    html.Div(className = 'page-body',children = [
    html.Div(className = 'DataSelectionArea', children = [
    #### **** THIS IS WHERE THE DATA SELECTION STARTS *****

    html.H3('Select a type of site:'),
    dcc.RadioItems(
        id = 'site_type_choice',
        options = [{'label': i, 'value': i} for i in ['DEFRA AURN', 'GAUGE']],
        value = 'DEFRA AURN'
    ),
    html.Br(),

    html.Label('Select a region:'),
    dcc.Dropdown(id = 'site_region_choice',
        multi = True,
        value = 'All'),
    html.Br(),

    html.Label('Select an environment type:'),
    dcc.Checklist(id = 'site_env_choice',
        values = ['All']),
    html.Br(),

    html.Label('Select a site:'),
    dcc.Dropdown(
        id = 'site_choice',
        placeholder = 'Select sites...'
    ),
    html.Br(),

    html.Label('Select a range of years:'),
    dcc.Dropdown(
        id = 'minimum_year',
        placeholder = 'Select start year...',
        options = [{'label': i, 'value': i} for i in range(2010,2019)]
    ),
    html.P('To'),
    dcc.Dropdown(
        id = 'maximum_year',
        placeholder = 'Select end year...',
    ),
    html.Br(),
    ### Have a submit button to load in the choices and then load the relevant
    ### data

    html.Button('Submit', id = 'site_choice_button'),
    html.Br(),
    html.Br(),

    html.Div(id = 'user_criteria'),

    html.Hr(),
    ###  Create a div to place the dataframe while its being used but not
    ### viewable by the user. Make data Json - very slow when being read
    html.Div(id = 'dataframe-holder', style = {'display': 'none'}),

    html.Label('Select a variable:'),
    dcc.Dropdown(id = 'variable_options',
    multi = True,
    placeholder = 'Select variables'),
    html.Br(),

    html.Label('Combine or seperate the variables?'),
    dcc.RadioItems(id = 'combine_choice',
    options = [{'label': i, 'value': i} for i in ['Combine', 'Seperate']],
    value = 'Combine'),
    html.Br(),

    # Resample the data
    html.Label('How do you want the data resampled?'),
    dcc.RadioItems(id = 'DataResample',
        options = [{'label': i, 'value': i} for i in ['Raw','Daily', 'Weekly','Monthly']],
        value = 'Daily'),
    html.Br(),

    html.Label('Select a date range of the data:'),
    dcc.RangeSlider( id = 'date-slider', min = 0, allowCross = False),# updatemode = 'drag' ),
    html.Br(),

    html.Div( id = 'date-choice'),
    ]),
    html.Hr(),
    html.Hr(),

    ### Each placeholder for plots and their individual controls go below
    ### **************************  TimeSeries  ***************************
    html.Div(id = 'TimeSeriesHolder', className = 'plot_holder', children = [
        html.Div(id = 'TimeSeries', className = 'main_plot'),
        html.Div(id = 'TimeSeriesTools', className = 'plot_tools', children = [
            html.H3('Time Series Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'TimeSeriesTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            html.Label('X Axis Label'),
            dcc.Input( id = 'TimeSeriesXTitle',
                placeholder = 'Enter X axis label',
                value = 'Date'),
            html.Br(),
            html.Label('Y Axis Label'),
            dcc.Input( id = 'TimeSeriesYTitle',
                placeholder = 'Enter Y axis label',
                value = ''),
            html.Br(),
            html.Label('Add a rolling mean'),
            dcc.Checklist(id = 'TimeSeriesRollingMean',
                values = [],
            ),
            html.Br(),
            dcc.RadioItems(id = 'TimeSeriesLineOrScatter',
            options = [{'label': i, 'value': i} for i in ['Scatter', 'Line', 'Line & Scatter']],
            value = 'Scatter',
            ),
        ])
    ]),
    html.Hr(),
    ### *********************  Histogram  *********************************
    html.Div(id = 'HistogramHolder', className = 'plot_holder', children = [
        html.Div(id = 'Histogram', className = 'main_plot'),
        html.Div(id = 'HistogramTools', className = 'plot_tools', children = [
            html.H3('Histogram Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'HistogramTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            html.Label('X Axis Label'),
            dcc.Input( id = 'HistogramXTitle',
                placeholder = 'Enter X axis label',
                value = ''),
            html.Br(),
            html.Label('Choose the maximum number of histogram bins'),
            dcc.Input( id = 'HistogramBins',
                placeholder = 'Number of bins...',
                value = '25'), #TODO this needs to change depending on input
        ]),
    ]),
    html.Hr(),

    ### *********************  Correlation  *********************************
    html.Div(id = 'CorrelationHolder', className = 'plot_holder', children = [
        html.Div(id = 'Correlation', className = 'main_plot'),
        html.Div(id = 'CorrelationTools', className = 'plot_tools', children = [
            html.H3('Correlation Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'CorrelationTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),

            html.Label('X Axis Label'),
            dcc.Input( id = 'CorrelationXTitle',
                placeholder = 'Enter X axis label',
                value = ''),
            html.Br(),

            html.Label('Y Axis Label'),
            dcc.Input( id = 'CorrelationYTitle',
                placeholder = 'Enter Y axis label',
                value = ''),
            html.Br(),

            html.Label('Swap Axes'),
            html.Button('Swap X & Y', id = 'CorrelationSwapButton', n_clicks = 0),
            html.Br(),

            html.Label('Colour scatter by:'),
            dcc.Dropdown(id = 'correlation_colourby',
            placeholder = 'Select variable'),
            #TODO Need to make a 'clear' option if user wants to get rid of colourbar
            html.Br(),

        ]),
    ]),
    html.Hr(),


    ### *******************  Hourly boxplots  ***************************
    html.Div(id = 'HourlyBoxHolder', className = 'plot_holder', children = [
        html.Div(id = 'HourlyBoxplots', className = 'main_plot'),
        html.Div(id = 'HourlyBoxTools', className = 'plot_tools', children = [
            html.H3('Hourly Box Plot Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'HourlyBoxTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),

            html.Label('Y Axis Label'),
            dcc.Input( id = 'HourlyBoxYTitle',
                placeholder = 'Enter Y axis label',
                value = ''),
            html.Br(),

            dcc.Checklist(id = 'HourlyBoxMean',
                options = [{'label': 'Show Mean', 'value': True}],
                    values = [])
        ]),
    ]),
    html.Br(),
    html.Hr(),

    ### *******************  Weekly boxplots  ***************************
    html.Div(id = 'WeeklyBoxHolder', className = 'plot_holder', children = [
        html.Div(id = 'WeeklyBoxplots', className = 'main_plot'),
        html.Div(id = 'WeeklyBoxTools', className = 'plot_tools', children = [
            html.H3('Weekly Box Plot Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'WeeklyBoxTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),

            html.Label('Y Axis Label'),
            dcc.Input( id = 'WeeklyBoxYTitle',
                placeholder = 'Enter Y axis label',
                value = ''),
            html.Br(),

            dcc.Checklist(id = 'WeeklyBoxMean',
                options = [{'label': 'Show Mean', 'value': True}],
                    values = [])
        ]),
    ]),
    html.Br(),
    html.Hr(),

    ### Monthly boxplots
    # html.Div(id = 'MonthlyBoxplots'),
    # html.Br(),
    # html.Hr(),

    ### Date and Day heatmaps
    html.Div( id = 'DateDayHeatmapHolder', className = 'plot_holder', children =[
        html.Div(id = 'DateDayHeatmap', className = 'main_plot'),
        html.Div(id = 'DateDayHeatmapTools', className = 'plot_tools', children = [
        html.H3('Date & Day Heatmap Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'DateDayHeatmapTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            # html.Label('Sample Type'),
            # dcc.RadioItems( id = 'DateDayHeatmapSampleType',
            #     options = [{'label': i, 'value': i} for i in ['Mean', 'Median', 'Maximum', 'Minimum']],
            #     value = ''),
            # html.Br(),
        ])
    ]),

    html.Br(),
    html.Hr(),

    ])])
    return page_layout


### ===================================================================
### END OF PROGRAM
### ===================================================================
