from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData


def DEFRA_individual_sites():
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
    html.Div(className = 'tool_explainer', children = [
    html.P('This is the development page for the data plotting tool. Choose a DEFRA site and a variable or two to plot and click the submit button to produce a number of plots for the given data.'),
    html.P('** Please Note **'),
    html.P('This page is still in the development stage.'),
    html.P('Currently only limited data is available and therefore the data shown is not up to date')
    ]),
    html.Div(className = 'DataSelectionArea', children = [
    #### **** THIS IS WHERE THE DATA SELECTION STARTS *****

    html.H3('Analysis for individual DEFRA sites.'),
    # dcc.RadioItems(
    #     id = 'site_type_choice',
    #     options = [{'label': i, 'value': i} for i in ['DEFRA AURN', 'GAUGE (Currenlty Unavailable)']],
    #     value = 'DEFRA AURN'
    # ),
    html.Br(),

    html.Label('Select a region:'),
    dcc.Dropdown(id = 'site_region_choice',
        multi = True,
        options = region_options,
        value = 'All'),
    html.Br(),

    html.Label('Select an environment type:'),
    dcc.Checklist(id = 'site_env_choice',
        options = env_options,
        values = ['All']),
    html.Br(),

    html.Label('Select a site:'),
    dcc.Dropdown(
        id = 'site_choice',
        placeholder = 'Select sites...',
        # value = 'Aberdeen'
    ),
    html.Br(),

    html.Label('Select a range of years:'),
    dcc.Dropdown(
        id = 'minimum_year',
        placeholder = 'Select start year...',
    ),
    html.P('To'),
    dcc.Dropdown(
        id = 'maximum_year',
        placeholder = 'Select end year...',
    ),
    html.Br(),
    ### Have a submit button to load in the choices and then load the relevant
    ### data
    dcc.Loading(id="loading-variables", children=[
    html.Label('Select a variable:'),
    dcc.Dropdown(id = 'variable_options',
    multi = True,
    placeholder = 'Select variables'),
    ],type="dot"),
    html.Br(),

    html.Div(children = [
    html.Label('Combine or separate the variables?'),
    dcc.RadioItems(id = 'combine_choice',
    options = [{'label': i, 'value': i} for i in ['Combine', 'Separate']],
    value = 'Combine'),
    html.Br(),], style = {'display': 'none'}),

    html.Button('Submit', id = 'site_choice_button'),
    dcc.Loading(id="loading-main", children=[html.Div(id = 'dataframe-holder', style = {'display': 'none'})],
        type="graph", fullscreen = True),
    html.Br(),
    html.Br(),
    html.Div(id = 'submit_counter', style= {'display':'none'}),
    html.Div(id = 'user_criteria'),

    html.Hr(),
    ###  Create a div to place the dataframe while its being used but not
    ### viewable by the user. Make data Json - very slow when being read
    # html.Div(id = 'dataframe-holder', style = {'display': 'none'}),



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
        dcc.Loading(id="loading-timeseries", children=[html.Div(id = 'TimeSeries')],
            type="dot", className = 'main_plot'),
        # html.Div(id = 'TimeSeries', className = 'main_plot'),
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
            dcc.RadioItems(id = 'TimeSeriesLabelFormat',
                options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
                value = 'Variable Name'),
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
    dcc.Loading(id="loading-histogram", children=[html.Div(id = 'Histogram')],
        type="dot", className = 'main_plot'),
        # html.Div(id = 'Histogram', className = 'main_plot'),
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
            dcc.RadioItems(id = 'HistogramLabelFormat',
                options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
                value = 'Variable Name'),
            html.Br(),
            html.Label('Choose the maximum number of histogram bins'),
            dcc.Input( id = 'HistogramBins',
                placeholder = 'Number of bins...',
                value = '25'),
            html.Br(),
            html.Br(),
            dcc.Checklist( id = 'HistogramProbability',
                options = [{'label':'Probability', 'value': 'Probability'}],
                values = []),

        ]),
    ]),
    html.Hr(),

    ### *********************  Correlation  *********************************
    html.Div(id = 'CorrelationHolder', className = 'plot_holder', children = [
    dcc.Loading(id="loading-correlation", children=[html.Div(id = 'Correlation')],
        type="dot", className = 'main_plot'),
        # html.Div(id = 'Correlation', className = 'main_plot'),
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
            dcc.RadioItems(id = 'CorrelationLabelFormat',
                options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
                value = 'Variable Name'),
            html.Br(),
            html.Label('Swap Axes'),
            html.Button('Swap X & Y', id = 'CorrelationSwapButton', n_clicks = 0),
            html.Br(),

            html.Label('Colour scatter by:'),
            dcc.Dropdown(id = 'correlation_colourby',
            placeholder = 'Select variable'),
            html.Br(),

            html.Label('Colour Bar Label:'),
            dcc.Input(id = 'CorrelationCLabel',
            placeholder = 'Enter Colourbar label'),
            html.Br(),


        ]),
    ]),
    html.Hr(),

### *********************  Dirunal Cycle  *********************************
html.Div(id = 'DiurnalCycleHolder', className = 'plot_holder', children = [
dcc.Loading(id="loading-diurnalcycle", children=[html.Div(id = 'DiurnalCycle')],
    type="dot", className = 'main_plot'),
    # html.Div(id = 'DiurnalCycle', className = 'main_plot'),
    html.Div(id = 'DiurnalCycleTools', className = 'plot_tools', children = [
        html.H3('Diurnal Cycle Tools:'),
        html.Br(),
        html.Label('Plot Title'),
        dcc.Input( id = 'DiurnalCycleTitle',
            placeholder = 'Enter Title',
            value = ''),
        html.Br(),

        html.Label('X Axis Label'),
        dcc.Input( id = 'DiurnalCycleXTitle',
            placeholder = 'Enter X axis label',
            value = 'Hour of the Day'),
        html.Br(),

        html.Label('Y Axis Label'),
        dcc.Input( id = 'DiurnalCycleYTitle',
            placeholder = 'Enter Y axis label',
            value = ''),
        html.Br(),
        dcc.RadioItems(id = 'DiurnalCycleLabelFormat',
            options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
            value = 'Variable Name'),
        html.Br(),
        html.Label('Split into Weekdays'),
        dcc.RadioItems( id = 'DiurnalCycleWeekdaySplit',
            options = [{'label': i, 'value': i} for i in ['Yes', 'No']],
            value = 'No'),
        html.Br(),

        html.Label('Sample Type'),
        dcc.RadioItems( id = 'DiurnalCycleSampleType',
            options = [{'label': i, 'value': i} for i in ['Mean', 'Median', 'Both']],
            value = 'Mean'),
        html.Br(),

        html.Label('Error Shading'),
        dcc.RadioItems( id = 'DiurnalCycleErrors',
            options = [{'label': i, 'value': i} for i in ['Std', '95% Confidence', 'None']],
            value = '95% Confidence'),
        html.Br(),

        ]),
    ]),
    html.Hr(),


    ### *******************  Hourly boxplots  ***************************
    html.Div(id = 'HourlyBoxHolder', className = 'plot_holder', children = [
    dcc.Loading(id="loading-hourlybox", children=[html.Div(id = 'HourlyBoxplots')],
        type="dot", className = 'main_plot'),
        # html.Div(id = 'HourlyBoxplots', className = 'main_plot'),
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
            dcc.RadioItems(id = 'HourlyBoxLabelFormat',
                options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
                value = 'Variable Name'),
            html.Br(),
            dcc.Checklist(id = 'HourlyBoxMean',
                options = [{'label': 'Show Mean', 'value': True}],
                    values = [])
        ]),
    ]),
    html.Br(),
    html.Hr(),

### *********************  Weekly Cycle  *********************************
html.Div(id = 'WeeklyCycleHolder', className = 'plot_holder', children = [
dcc.Loading(id="loading-weeklycycle", children=[html.Div(id = 'WeeklyCycle')],
    type="dot", className = 'main_plot'),
    # html.Div(id = 'WeeklyCycle', className = 'main_plot'),
    html.Div(id = 'WeeklyCycleTools', className = 'plot_tools', children = [
        html.H3('Weekly Cycle Tools:'),
        html.Br(),
        html.Label('Plot Title'),
        dcc.Input( id = 'WeeklyCycleTitle',
            placeholder = 'Enter Title',
            value = ''),
        html.Br(),

        html.Label('X Axis Label'),
        dcc.Input( id = 'WeeklyCycleXTitle',
            placeholder = 'Enter X axis label',
            value = 'Day of the Week'),
        html.Br(),

        html.Label('Y Axis Label'),
        dcc.Input( id = 'WeeklyCycleYTitle',
            placeholder = 'Enter Y axis label',
            value = ''),
        html.Br(),
        dcc.RadioItems(id = 'WeeklyCycleLabelFormat',
            options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
            value = 'Variable Name'),
        html.Br(),
        html.Label('Sample Type'),
        dcc.RadioItems( id = 'WeeklyCycleSampleType',
            options = [{'label': i, 'value': i} for i in ['Mean', 'Median', 'Both']],
            value = 'Mean'),
        html.Br(),

        html.Label('Error Shading'),
        dcc.RadioItems( id = 'WeeklyCycleErrors',
            options = [{'label': i, 'value': i} for i in ['Std', '95% Confidence', 'None']],
            value = '95% Confidence'),
        html.Br(),

        ]),
    ]),
    html.Hr(),


    ### *******************  Weekly boxplots  ***************************
    html.Div(id = 'WeeklyBoxHolder', className = 'plot_holder', children = [
    dcc.Loading(id="loading-weeklybox", children=[html.Div(id = 'WeeklyBoxplots')],
        type="dot", className = 'main_plot'),
        # html.Div(id = 'WeeklyBoxplots', className = 'main_plot'),
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
            dcc.RadioItems(id = 'WeeklyBoxLabelFormat',
                options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
                value = 'Variable Name'),
            html.Br(),
            dcc.Checklist(id = 'WeeklyBoxMean',
                options = [{'label': 'Show Mean', 'value': True}],
                    values = [])
        ]),
    ]),
    html.Br(),
    html.Hr(),


### *********************  Annual Cycle  *********************************
html.Div(id = 'AnnualCycleHolder', className = 'plot_holder', children = [
dcc.Loading(id="loading-annualcycle", children=[html.Div(id = 'AnnualCycle')],
    type="dot", className = 'main_plot'),
    # html.Div(id = 'AnnualCycle', className = 'main_plot'),
    html.Div(id = 'AnnualCycleTools', className = 'plot_tools', children = [
        html.H3('Annual Cycle Tools:'),
        html.Br(),
        html.Label('Plot Title'),
        dcc.Input( id = 'AnnualCycleTitle',
            placeholder = 'Enter Title',
            value = ''),
        html.Br(),

        html.Label('X Axis Label'),
        dcc.Input( id = 'AnnualCycleXTitle',
            placeholder = 'Enter X axis label',
            value = 'Month'),
        html.Br(),

        html.Label('Y Axis Label'),
        dcc.Input( id = 'AnnualCycleYTitle',
            placeholder = 'Enter Y axis label',
            value = ''),
        html.Br(),
        dcc.RadioItems(id = 'AnnualCycleLabelFormat',
            options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
            value = 'Variable Name'),
        html.Br(),
        html.Label('Sample Type'),
        dcc.RadioItems( id = 'AnnualCycleSampleType',
            options = [{'label': i, 'value': i} for i in ['Mean', 'Median', 'Both']],
            value = 'Mean'),
        html.Br(),

        html.Label('Error Shading'),
        dcc.RadioItems( id = 'AnnualCycleErrors',
            options = [{'label': i, 'value': i} for i in ['Std', '95% Confidence', 'None']],
            value = '95% Confidence'),
        html.Br(),

        ]),
    ]),
    html.Hr(),


    ### Monthly boxplots
    # html.Div(id = 'MonthlyBoxplots'),
    # html.Br(),
    # html.Hr(),

    ### Date and Day heatmaps
    html.Div( id = 'DateDayHeatmapHolder', className = 'plot_holder', children =[
    dcc.Loading(id="loading-datedatheat", children=[html.Div(id = 'DateDayHeatmap')],
        type="dot", className = 'main_plot'),
        # html.Div(id = 'DateDayHeatmap', className = 'main_plot'),
        html.Div(id = 'DateDayHeatmapTools', className = 'plot_tools', children = [
        html.H3('Date & Day Heatmap Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'DateDayHeatmapTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            html.Label('Colour Bar Title'),
            dcc.Input( id = 'DateDayHeatmapCLabel',
                placeholder = 'Enter Title',
                value = ''),
            dcc.RadioItems(id = 'DateDayHeatmapLabelFormat',
                options = [{'label': i, 'value': i} for i in ['Variable Name', 'Chemical Formula',]],
                value = 'Variable Name'),
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
