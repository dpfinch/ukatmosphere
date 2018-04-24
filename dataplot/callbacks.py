from .server import app, cache
from random import randint
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
from dataplot.DataTools import AnalysisDriver
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData
import pandas as pd

### ===================================================================
### Load the data in at set up. By no means a clever way of doing this
### but hopefully it'll do the job for now.
### ===================================================================

# all_df = {'Edinburgh': AnalysisDriver.GetData(['Edinburgh']),
#     'Heathfield': AnalysisDriver.GetData(['Heathfield'])}
# print('Read in data')
### ===================================================================
### The first callbacks are for the choices effecting every plot
### These outputs are to be included in every other callback.
### ===================================================================

### Callback to list the available sites with above selection
@app.callback(Output('site_choice', 'options'),
    [Input('site_region_choice', 'value'),
    Input('site_env_choice', 'values'),])
def list_available_sites(site_region, env_choice):
    sites = LoadData.AURN_site_list_db(site_region, env_choice)
    options = [{'label': i, 'value': i} for i in sites]
    return options

### Callback to set the limit on the range of years. So can choose a site
### and not go beyond when it was active
@app.callback(Output('minimum_year','value'),
    [Input('site_choice','value')])
def fill_maximum_year(site):
    start_year, end_year = LoadData.get_site_year_range_db(site)
    return start_year

@app.callback(Output('minimum_year', 'options'),
    [Input('site_choice','value')])
def get_site_minimum_year(site):
    start_year, end_year = LoadData.get_site_year_range_db(site)

    options = [{'label': i, 'value': i} for i in range(start_year,end_year + 1)]
    return options

@app.callback(Output('maximum_year','value'),
    [Input('site_choice','value')])
def fill_maximum_year(site):
    start_year, end_year = LoadData.get_site_year_range_db(site)
    return end_year

### Callback to list the variable options
@app.callback(Output('variable_options', 'options'),
    [Input('site_choice', 'value')],
    )
def varaible_list(site):
    site_vars = LoadData.Get_Site_Variables_db(site)

    var_options = [{'label': i, 'value': i} for i in site_vars]
    return var_options

### Callback to prevent the end year being before the start year
@app.callback(Output('maximum_year', 'options'),
    [Input('minimum_year', 'value'),
    Input('site_choice', 'value')
    ])
def get_correct_year_range(min_year,site):
    start_year, end_year = LoadData.get_site_year_range_db(site)
    options = [{'label': i, 'value': i} for i in range(min_year,end_year + 1)]
    return options
### Cache the loaded dataframe so we don't have to load it each time
@cache.memoize()
def load_station_data(site_type, sites, years, variables):
    if sites:
        if site_type == 'DEFRA AURN':
            # df = LoadData.Get_AURN_data( sites, years, variables)
            df = LoadData.Get_One_Site_Data(sites,years, variables)
        else:
            print("Don't have any other data yet")
    else:
        df = 0
    return df

### Callback to load the data into the page
@app.callback(Output('dataframe-holder', 'children'),
    [Input('site_choice_button', 'n_clicks')],
    [State('site_choice', 'value'),
    State('minimum_year', 'value'),
    State('maximum_year', 'value'),
    State('variable_options','value'),
    ])
def load_data(button_clicked,sites, min_year, max_year, variables):
    years = [min_year, max_year]
    load_station_data('DEFRA AURN', sites, years, variables)
    info_string = 'DEFRA AURN' + ',' + sites + ',' + str(min_year) + ',' + str(max_year) + ',' + ','.join(variables)
    return info_string

@app.callback(Output('user_criteria', 'children'),
    [Input('dataframe-holder','children')
    ])
def return_user_choice_info(data_info):
    if not data_info:
        return ''
    else:
        return html.P(TidyData.site_info_message(data_info))




### ===========================================================
### AFTER SUBMIT BUTTON
### ===========================================================


# ### Callback for the variables choices (dropdown menu)
# @app.callback(Output('variable_options','value'),
#     [Input('dataframe-holder', 'children'),
#     Input('variable_options','options')])
# def variable_user_choices(data,options):
#     if not data:
#         return ''
#     data = data.split(',')
#     df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
#     if not isinstance(df, pd.DataFrame):
#         return ''
#     #Currently only return the first option the page can't handle more yet
#     return options[0]['value']


### Callback for the year range slider - will set values for date range
### Currently need a seperate callback for each property of the slider
### First range callback to set the maximum bound
@app.callback(Output('date-slider','max'),
    [Input('DataResample','value'),
    Input('dataframe-holder', 'children')])
def get_range_min(resample_value, data):
    if not data:
        return ''
    data = data.split(',')
    variable_list = data[4:]

    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], variable_list)

    if not isinstance(df, pd.DataFrame):
        return ''
    resample_rate = resample_value[0]
    if resample_rate != 'R':
        df = df.resample(resample_rate).apply('mean')

    year_max = len(df)
    return year_max
### Second range callback to set the value range
@app.callback(Output('date-slider','value'),
    [Input('dataframe-holder', 'children'),
    Input('site_choice','value'),
    Input('DataResample','value')])
def get_range_min(data, site_value, resample_value):
    if not data:
        return ''
    data = data.split(',')
    variable_list = data[4:]
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], variable_list)
    if not isinstance(df, pd.DataFrame):
        return ''

    resample_rate = resample_value[0]
    if resample_rate != 'R':
        df = df.resample(resample_rate).apply('mean')
    value_range = [1,len(df)]
    return value_range
### third range callback to set the slider marks
@app.callback(Output('date-slider','marks'),
    [Input('dataframe-holder', 'children'),
    Input('site_choice','value'),
    Input('DataResample','value')])
def get_range_marks(data, site_value, resample_value):
    if not data:
        return ''
    data = data.split(',')
    variable_list = data[4:]
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], variable_list)
    if not isinstance(df, pd.DataFrame):
        return ''

    resample_rate = resample_value[0]
    if resample_rate != 'R':
        df = df.resample(resample_rate).apply('mean')

    marks = {
        0:{'label':str(df.index[0].date())},
        len(df):{'label':str(df.index[-1].date())}
    }
    return marks


### Callback to print the dates chosen
@app.callback(Output('date-choice','children'),
    [Input('dataframe-holder', 'children'),
    Input('site_choice','value'),
    Input('DataResample','value'),
    Input('date-slider','value')
    ])
def print_date_choices(data, site_value, resample_value,
    date_values):
    if not data:
        return ''
    data = data.split(',')
    variable_list = data[4:]
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], variable_list)
    if not isinstance(df, pd.DataFrame):
        return ''

    resample_rate = resample_value[0]

    if resample_rate != 'R':
        df = df.resample(resample_rate).apply('mean')

    begin_date = str(df.index[date_values[0] -1].date())
    end_date = str(df.index[date_values[1] - 1].date())

    out_string = "Date range: %s to %s " % (begin_date, end_date)

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

# @app.callback(Output('TimeSeriesYTitle', 'value'),
#     [Input('variable_options', 'value')])
# def get_timeseries_ytitle(variable_options):
#     ytitle = variable_options
#     return ytitle

### Callback for the TimeSeries plot
@app.callback(Output('TimeSeries', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('TimeSeriesTitle','value'),
    Input('TimeSeriesXTitle', 'value'),
    Input('TimeSeriesYTitle', 'value'),
    Input('TimeSeriesRollingMean', 'values'),
    Input('TimeSeriesLineOrScatter', 'value')
    ])
def change_timeseries(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, xtitle, ytitle, rollingMean, lineorscatter):
    if not data:
        return ''
    data = data.split(',')

    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import TimeSeries
    return TimeSeries.TimeSeries(df,variable_options = variable_options,
        site_choice = site_choice, combine_choice = combine_choice,
        DataResample = DataResample, date_range = date_range, title = title,
        rollingMean = rollingMean, xtitle = xtitle, ytitle = ytitle,
        lineorscatter = lineorscatter )

# ### *********** HISTOGRAM PLOT *******************
# ### Callback for the Histogram interaction
#
# ### Callback for the Histogram plot
@app.callback(Output('Histogram', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('HistogramTitle', 'value'),
    Input('HistogramXTitle', 'value'),
    Input('HistogramBins','value'),
    Input('HistogramProbability','values')
    ])
def change_histogram(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, xtitle, histbins, probability):

    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import Histogram
    return Histogram.Histogram(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, histbins = histbins,
    title = title, xtitle = xtitle, probability = probability)

### *********** CORRELATION PLOT *******************
### Callback for the Correlation interaction

@app.callback(Output('correlation_colourby', 'options'),
    [Input('dataframe-holder', 'children'),
    Input('site_choice','value')])
def get_colourbychoices(data,value):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    variable_list = LoadData.Get_Site_Variables_db(data[1])
    var_options = [{'label': i, 'value': i} for i in variable_list]
    return var_options


# @app.callback(Output('CorrelationYTitle', 'value'),
#     [Input('variable_options', 'value')])
# def get_correlation_ytitle(variable_options):
#     ytitle = variable_options[1]
#     return ytitle
#
# @app.callback(Output('CorrelationXTitle', 'value'),
#     [Input('variable_options', 'value')])
# def get_correlation_xtitle(variable_options):
#     xtitle = variable_options[0]
#     return xtitle

# ### Callback for the Correlation plot
@app.callback(Output('Correlation', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('CorrelationTitle', 'value'),
    Input('CorrelationXTitle', 'value'),
    Input('CorrelationYTitle','value'),
    Input('CorrelationSwapButton', 'n_clicks'),
    Input('correlation_colourby','value'),
    Input('CorrelationCLabel', 'value')
    ])
def change_correlation(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, xtitle, ytitle, swap_button, colourby, clabel):
    if not data:
        return ''
    data = data.split(',')
    if colourby:
        data.append(colourby)
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import Correlation
    return Correlation.Correlation(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    xtitle = xtitle, ytitle = ytitle, swap_button = swap_button,
    colourby = colourby, clabel = clabel)


### *********** Diurnal Cycle *******************
### Callback for the diurnal cycle interaction


### Callback for the diurnal cycle plot
@app.callback(Output('DiurnalCycle', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('DiurnalCycleTitle', 'value'),
    Input('DiurnalCycleYTitle', 'value'),
    Input('DiurnalCycleXTitle', 'value'),
    Input('DiurnalCycleWeekdaySplit', 'value'),
    Input('DiurnalCycleSampleType', 'value'),
    Input('DiurnalCycleErrors', 'value'),
    ])
def change_dirunalplot(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, xtitle, weekdaysplit, sample_type, errors):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import DiurnalCycle

    if weekdaysplit == 'Yes':
        return DiurnalCycle.DiurnalCycleSplit(df,variable_options = variable_options,
        site_choice = site_choice, combine_choice = combine_choice,
        DataResample = DataResample, date_range = date_range, title = title,
        ytitle = ytitle, xtitle = xtitle, weekdaysplit = weekdaysplit, sample_type = sample_type,
        errors = errors)
    else:
        return DiurnalCycle.DiurnalCycle(df,variable_options = variable_options,
        site_choice = site_choice, combine_choice = combine_choice,
        DataResample = DataResample, date_range = date_range, title = title,
        ytitle = ytitle, xtitle = xtitle, weekdaysplit = weekdaysplit, sample_type = sample_type,
        errors = errors)

### *********** HOURLY BOXPLOT *******************
### Callback for the Hourly boxplot interaction

### Callback for the hourly box plot
@app.callback(Output('HourlyBoxplots', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('HourlyBoxTitle', 'value'),
    Input('HourlyBoxYTitle', 'value'),
    Input('HourlyBoxMean', 'values')
    ])
def change_hourlybox(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, showmean):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import HourlyBoxplots
    return HourlyBoxplots.HourlyBoxplots(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, showmean = showmean)

### *********** Weekly Cycle *******************
### Callback for the Weekly cycle interaction


### Callback for the Weekly cycle plot
@app.callback(Output('WeeklyCycle', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('WeeklyCycleTitle', 'value'),
    Input('WeeklyCycleYTitle', 'value'),
    Input('WeeklyCycleXTitle', 'value'),
    Input('WeeklyCycleSampleType', 'value'),
    Input('WeeklyCycleErrors', 'value'),
    ])
def change_Weeklyplot(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, xtitle, sample_type, errors):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import WeeklyCycle
    return WeeklyCycle.WeeklyCycle(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, xtitle = xtitle, sample_type = sample_type,
    errors = errors)


### *********** WEEKLY BOXPLOT *******************
### Callback for the Weekly boxplot interaction

### Callback for the weekly box plot
@app.callback(Output('WeeklyBoxplots', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('WeeklyBoxTitle', 'value'),
    Input('WeeklyBoxYTitle', 'value'),
    Input('WeeklyBoxMean', 'values')
    ])
def change_weeklybox(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, showmean):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import WeeklyBoxplots
    return WeeklyBoxplots.WeeklyBoxplots(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, showmean = showmean)

### *********** Annual Cycle *******************
### Callback for the annual cycle interaction


### Callback for the Annual cycle plot
@app.callback(Output('AnnualCycle', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('AnnualCycleTitle', 'value'),
    Input('AnnualCycleYTitle', 'value'),
    Input('AnnualCycleXTitle', 'value'),
    Input('AnnualCycleSampleType', 'value'),
    Input('AnnualCycleErrors', 'value'),
    ])
def change_Annualplot(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, xtitle, sample_type, errors):
    if not data:
        return ''
    data = data.split(',')
    if (int(data[3]) - int(data[2])) < 2:
        return html.H3('Annual mean needs more than one year of data.')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import AnnualCycle
    return AnnualCycle.AnnualCycle(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, xtitle = xtitle, sample_type = sample_type,
    errors = errors)


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

### *********** DATE AND DAY HEATMAP *******************
### Callback for the Date and Day Heatmap interaction

@app.callback(Output('DateDayHeatmap', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('DateDayHeatmapTitle', 'value'),
    ])
def change_datedayheatmap(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import DateDayHeatmap
    return DateDayHeatmap.DateDayHeatmap(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    )



### ===================================================================
### END OF PROGRAM
### ===================================================================
