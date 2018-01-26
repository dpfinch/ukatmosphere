from .server import app
from random import randint
from .test_random_gen import random_numbers
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from dataplot.DataTools import AnalysisDriver
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData


### ===================================================================
### Load the data in at set up. By no means a clever way of doing this
### but hopefully it'll do the job for now.
### ===================================================================

all_df = {'Edinburgh': AnalysisDriver.GetData(['Edinburgh']),
    'Heathfield': AnalysisDriver.GetData(['Heathfield'])}
# print('Read in data')
### ===================================================================
### The first callbacks are for the choices effecting every plot
### These outputs are to be included in every other callback.
### ===================================================================

### Callback for the initial_form site choice
@app.callback(Output('variable_options', 'options'),
    [Input('site_choice', 'value')])
def site_user_choices(value):
    variable_list = AnalysisDriver.GetSiteVariables([value])
    var_options = [{'label': i, 'value': i} for i in variable_list]

    return var_options

### Callback for the variables choices (dropdown menu)
@app.callback(Output('variable_options','value'),
    [Input('variable_options','options')])
def variable_user_choices(options):
    #Currently only return the first option the page can't handle more yet
    return options[0]['value']


### Callback for the year range slider - will set values for date range
### Currently need a seperate callback for each property of the slider
### First range callback to set the maximum bound
@app.callback(Output('date-slider','max'),
    [Input('site_choice','value'),
    Input('DataResample','value')])
def get_range_min(site_value, resample_value):
    site_df = all_df[site_value][:]

    resample_rate = resample_value[0]
    if resample_rate != 'R':
        site_df = site_df.resample(resample_rate).apply('mean')

    year_max = len(site_df)
    return year_max
### Second range callback to set the value range
@app.callback(Output('date-slider','value'),
    [Input('site_choice','value'),
    Input('DataResample','value')])
def get_range_min(site_value, resample_value):
    site_df = all_df[site_value][:]

    resample_rate = resample_value[0]
    if resample_rate != 'R':
        site_df = site_df.resample(resample_rate).apply('mean')
    value_range = [1,len(site_df)]
    return value_range
### third range callback to set the slider marks
@app.callback(Output('date-slider','marks'),
    [Input('site_choice','value'),
    Input('DataResample','value')])
def get_range_min(site_value, resample_value):
    site_df = all_df[site_value][:]

    resample_rate = resample_value[0]
    if resample_rate != 'R':
        site_df = site_df.resample(resample_rate).apply('mean')

    marks = {
        0:{'label':str(site_df.index[0].date())},
        len(site_df):{'label':str(site_df.index[-1].date())}
    }
    return marks


### Callback to print the dates chosen
@app.callback(Output('date-choice','children'),
    [
    Input('site_choice','value'),
    Input('DataResample','value'),
    Input('date-slider','value')
    ])
def print_date_choices(site_value, resample_value, date_values):

    site_df = all_df[site_value][:]

    resample_rate = resample_value[0]

    if resample_rate != 'R':
        site_df = site_df.resample(resample_rate).apply('mean')

    begin_date = str(site_df.index[date_values[0] -1])
    end_date = str(site_df.index[date_values[1] - 1])

    out_string = "Date range: %s -> %s " % (begin_date, end_date)

    return out_string
## ===================================================================
### Each of the following callbacks are for each plot. They need to be
### named uniquely.
### Each callback Output must match the placeholder in the main layout.
### ===================================================================

### *********** TIMESERIES PLOT *******************
### Callback for the TimeSeries interaction
### Rolling mean callback
@app.callback(Output('TimeSeriesRollingMean','options'),
    [Input('DataResample','value')])
def rolling_mean_options(value):
    if value[0] == 'R':
        rmean_options = [{'label': i, 'value': i} for i in ['Hourly Rolling Mean', '8-Hourly Rolling Mean']]
    if value[0] == 'D':
        rmean_options = [{'label': i, 'value': i} for i in ['Daily Rolling Mean']]
    if value[0] == 'W':
        rmean_options = [{'label': i, 'value': i} for i in ['Weekly Rolling Mean ']]
    if value[0] == 'M':
        rmean_options = [{'label': i, 'value': i} for i in ['Monthly Rolling Mean']]

    return rmean_options
### Callback for the TimeSeries plot
@app.callback(Output('TimeSeries', 'children'),
    [Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('TimeSeriesRollingMean', 'values')
    ])
def change_timeseries(variable_options,site_choice, combine_choice, DataResample,
    date_range, rollingMean):

    df = all_df[site_choice]

    from dataplot.DataTools.AnalysisTools import TimeSeries
    return TimeSeries.TimeSeries(df,variable_options,site_choice,
        combine_choice, DataResample, date_range, rollingMean)

# ### *********** HISTOGRAM PLOT *******************
# ### Callback for the Histogram interaction
#
# ### Callback for the Histogram plot
@app.callback(Output('Histogram', 'children'),
    [Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    ])
def change_histogram(variable_options,site_choice, combine_choice, DataResample,
    date_range):
    df = all_df[site_choice]

    from dataplot.DataTools.AnalysisTools import Histogram
    return Histogram.Histogram(df,variable_options,site_choice,
        combine_choice, DataResample, date_range)

### *********** HOURLY BOXPLOT *******************
### Callback for the Hourly boxplot interaction

### Callback for the hourly box plot
@app.callback(Output('HourlyBoxplots', 'children'),
    [Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    ])
def change_hourlybox(variable_options,site_choice, combine_choice, DataResample,
    date_range):
    df = all_df[site_choice]

    from dataplot.DataTools.AnalysisTools import HourlyBoxplots
    return HourlyBoxplots.HourlyBoxplots(df,variable_options,site_choice,
        combine_choice, DataResample, date_range)

### *********** WEEKLY BOXPLOT *******************
### Callback for the Weekly boxplot interaction

### Callback for the weekly box plot
@app.callback(Output('WeeklyBoxplots', 'children'),
    [Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    ])
def change_weeklybox(variable_options,site_choice, combine_choice, DataResample,
    date_range):
    df = all_df[site_choice]

    from dataplot.DataTools.AnalysisTools import WeeklyBoxplots
    return WeeklyBoxplots.WeeklyBoxplots(df,variable_options,site_choice,
        combine_choice, DataResample, date_range)

### *********** MONTHLY BOXPLOT *******************
### Callback for the Monthyl boxplot interaction

### Callback for the monthly box plot
# @app.callback(Output('MonthlyBoxplots', 'children'),
#     [Input('variable_options','value'),
#     Input('site_choice', 'value'),
#     Input('combine_choice','value'),
#     Input('DataResample', 'value'),
#     Input('date-slider', 'value'),
#     ])
# def change_monthlybox(variable_options,site_choice, combine_choice, DataResample,
#     date_range):
#     df = all_df[site_choice]
#
#     from dataplot.DataTools.AnalysisTools import MonthlyBoxplots
#     return MonthlyBoxplots.MonthlyBoxplots(df,variable_options,site_choice,
#         combine_choice, DataResample, date_range)

### ===================================================================
### END OF PROGRAM
### ===================================================================
