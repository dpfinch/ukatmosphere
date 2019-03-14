from .server import app, cache
from random import randint
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
from dataplot.DataTools import AnalysisDriver
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData
import pandas as pd
from dataplot.EO_Lesson_Tools import Satellite_Tools
from dataplot.EO_Lesson_Tools import TIR_Tools
from dataplot.EO_Lesson_Tools import TIR_Data_Process

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
    sites = list(sites)
    sites.sort()
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

#
# @app.callback(Output('submit_counter', 'children'),
#     [Input('site_choice_button', 'n_clicks')],
#     )
# def submit_button_counter(data):
#     # print(data)
#     return str(data)


### ===========================================================
### AFTER SUBMIT BUTTON
### ===========================================================


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

@app.callback(Output('TimeSeriesYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('TimeSeriesLabelFormat', 'value')])
def get_timeseries_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

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
    Input('TimeSeriesLineOrScatter', 'value'),
    Input('TimeSeriesLabelFormat', 'value')
    ])
def change_timeseries(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, xtitle, ytitle, rollingMean, lineorscatter, label_format):
    if not data:
        return ''
    data = data.split(',')

    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''
    variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import TimeSeries
    return TimeSeries.TimeSeries(df,variable_options =variable_options,
        site_choice = site_choice, combine_choice = combine_choice,
        DataResample = DataResample, date_range = date_range, title = title,
        rollingMean = rollingMean, xtitle = xtitle, ytitle = ytitle,
        lineorscatter = lineorscatter, label_format = label_format )

#### *********** HISTOGRAM PLOT *******************
### Callback for the Histogram interaction
@app.callback(Output('HistogramXTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('HistogramLabelFormat', 'value')])
def get_histo_xtitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True

    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]

    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

#### Callback for the Histogram plot
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
    Input('HistogramProbability','values'),
    Input('HistogramLabelFormat', 'value')
    ])
def change_histogram(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, xtitle, histbins, probability, label_format):

    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import Histogram
    return Histogram.Histogram(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, histbins = histbins,
    title = title, xtitle = xtitle, probability = probability, label_format = label_format )

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

@app.callback(Output('CorrelationXTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('CorrelationLabelFormat', 'value')])
def get_correlation_xtitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True

    if not data_info:
        return ''

    if len(data_info.split(',')[4:]) > 1:
        variable_options = data_info.split(',')[4:][0]
    else:
        return ''

    ytitle = TidyData.Axis_Title([variable_options],
        chemical_formula)
    return ytitle

@app.callback(Output('CorrelationYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('CorrelationLabelFormat', 'value')])
def get_correlation_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True

    if not data_info:
        return ''
    if len(data_info.split(',')[4:]) > 1:
        variable_options = data_info.split(',')[4:][1]
    else:
        return ''

    ytitle = TidyData.Axis_Title([variable_options], chemical_formula)
    return ytitle


@app.callback(Output('CorrelationCLabel', 'value'),
    [Input('correlation_colourby', 'value'),
    Input('CorrelationLabelFormat', 'value')])
def get_correlation_clabel(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True

    if not data_info:
        return ''

    ytitle = TidyData.Axis_Title([data_info], chemical_formula)
    return ytitle

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
    Input('CorrelationCLabel', 'value'),
    ])
def change_correlation(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, xtitle, ytitle, swap_button, colourby, clabel):
    if not data:
        return ''
    data = data.split(',')
    variable_options = data[4:]
    if colourby:
        data.append(colourby)
        variable_options = data[4:-1]
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
@app.callback(Output('DiurnalCycleYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('DiurnalCycleLabelFormat', 'value')])
def get_dirunal_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

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
    Input('DiurnalCycleLabelFormat', 'value'),
    ])
def change_dirunalplot(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, xtitle, weekdaysplit, sample_type, errors, label_format):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.AnalysisTools import DiurnalCycle

    variable_options = data[4:]
    if weekdaysplit == 'Yes':
        return DiurnalCycle.DiurnalCycleSplit(df,variable_options = variable_options,
        site_choice = site_choice, combine_choice = combine_choice,
        DataResample = DataResample, date_range = date_range, title = title,
        ytitle = ytitle, xtitle = xtitle, weekdaysplit = weekdaysplit, sample_type = sample_type,
        errors = errors, label_format = label_format )
    else:
        return DiurnalCycle.DiurnalCycle(df,variable_options = variable_options,
        site_choice = site_choice, combine_choice = combine_choice,
        DataResample = DataResample, date_range = date_range, title = title,
        ytitle = ytitle, xtitle = xtitle, weekdaysplit = weekdaysplit, sample_type = sample_type,
        errors = errors, label_format = label_format )

### *********** HOURLY BOXPLOT *******************
### Callback for the Hourly boxplot interaction
@app.callback(Output('HourlyBoxYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('HourlyBoxLabelFormat', 'value')])
def get_hourly_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

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
    Input('HourlyBoxMean', 'values'),
    Input('HourlyBoxLabelFormat', 'value'),
    ])
def change_hourlybox(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, showmean, label_format):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import HourlyBoxplots
    return HourlyBoxplots.HourlyBoxplots(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, showmean = showmean, label_format = label_format )

### *********** Weekly Cycle *******************
### Callback for the Weekly cycle interaction
@app.callback(Output('WeeklyCycleYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('WeeklyCycleLabelFormat', 'value')])
def get_weeklycycle_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

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
    Input('WeeklyCycleLabelFormat', 'value'),
    ])
def change_Weeklyplot(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, xtitle, sample_type, errors, label_format):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import WeeklyCycle
    return WeeklyCycle.WeeklyCycle(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, xtitle = xtitle, sample_type = sample_type,
    errors = errors, label_format = label_format )


### *********** WEEKLY BOXPLOT *******************
### Callback for the Weekly boxplot interaction
@app.callback(Output('WeeklyBoxYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('WeeklyBoxLabelFormat', 'value')])
def get_weeklybox_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

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
    Input('WeeklyBoxMean', 'values'),
    Input('WeeklyBoxLabelFormat', 'value'),
    ])
def change_weeklybox(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, showmean, label_format):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''
    variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import WeeklyBoxplots
    return WeeklyBoxplots.WeeklyBoxplots(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, showmean = showmean, label_format = label_format )

### *********** Annual Cycle *******************
### Callback for the annual cycle interaction
@app.callback(Output('AnnualCycleYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('AnnualCycleLabelFormat', 'value')])
def get_annaualcycle_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

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
    Input('AnnualCycleLabelFormat', 'value'),
    ])
def change_Annualplot(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, ytitle, xtitle, sample_type, errors, label_format):
    if not data:
        return ''
    data = data.split(',')
    if (int(data[3]) - int(data[2])) < 2:
        return html.H3('Annual mean needs more than one year of data.')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''
    variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import AnnualCycle
    return AnnualCycle.AnnualCycle(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    ytitle = ytitle, xtitle = xtitle, sample_type = sample_type,
    errors = errors, label_format = label_format )


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

@app.callback(Output('DateDayHeatmapCLabel', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('DateDayHeatmapLabelFormat', 'value')])
def get_heatmap_Ctitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''

    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

@app.callback(Output('DateDayHeatmap', 'children'),
    [Input('dataframe-holder', 'children'),
    Input('variable_options','value'),
    Input('site_choice', 'value'),
    Input('combine_choice','value'),
    Input('DataResample', 'value'),
    Input('date-slider', 'value'),
    Input('DateDayHeatmapTitle', 'value'),
    Input('DateDayHeatmapCLabel','value'),
    ])
def change_datedayheatmap(data, variable_options,site_choice, combine_choice, DataResample,
    date_range, title, clabel):
    if not data:
        return ''
    data = data.split(',')
    df  = load_station_data(data[0],data[1],[int(data[2]),int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''

    variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import DateDayHeatmap
    return DateDayHeatmap.DateDayHeatmap(df,variable_options = variable_options,
    site_choice = site_choice, combine_choice = combine_choice,
    DataResample = DataResample, date_range = date_range, title = title,
    clabel=clabel
    )

### ===================================================================
### Callbacks for the map section
### ===================================================================

## Create the map
@app.callback(Output('main_graph_map','figure'),
              [Input('map_region_choice','value'),
               Input('map_env_choice', 'value'),
            #    Input('var_choice', 'value'),
               Input('map_hour_slider', 'value')],
              [State('main_graph_map', 'relayoutData')],
              )
def create_map(region, environ, hour_choice, main_graph_layout):

    aurn_df = pd.DataFrame(list(site_info.objects.filter(
    site_type = 'DEFRA AURN').filter(site_open = True).values()))

    if type(region) == str:
        region = [region]
    if type(environment) == str:
        environment = [environment]

    if 'All' in region:
        regioned_sites = aurn_df
    else:
        regioned_sites = aurn_df.loc[aurn_df['region'].isin(region)]

    if 'All' in environment:
        env_sites = regioned_sites
    else:
        env_sites = regioned_sites.loc[regioned_sites['environment_type'].isin(environment)]


    var_data = all_recent_data[var_choice]
    last_day = var_data.loc[var_data.index[-24:][0]:var_data.index[-24:][-1]]

    # This need to be protected somehow... maybe import from elsewhere
    mapbox_access_token = 'pk.eyJ1IjoiZG91Z2ZpbmNoIiwiYSI6ImNqZHhjYnpqeDBteDAyd3FsZXM4ZGdqdTAifQ.xLS22vmqzVYR0SAEDWdLpQ'

    chosen_hour = last_day.iloc[hour_choice].values.tolist()

    # values =

    final_df = final_df.loc[last_day.columns]
    marker_text = [x +': '+str(y) for x, y, in zip(env_sites.site_names.tolist(),
        chosen_hour)]

    data = Data([
    Scattermapbox(
        lat=env_sites.latitudes.tolist(),
        lon=env_sites.longitudes.tolist(),
        mode='markers',
        customdata = final_df.index.tolist(),
        marker=Marker(
            size=9,
            opacity = 0.85,
            color = chosen_hour,
            cmax = last_day.max(axis = 1).max(),
            colorbar = {'title':var_choice}
        ),
        text=marker_text,
        )
    ])

    layout = Layout(
        autosize=True,
        height = 750,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=54,
                lon=-3
            ),
            pitch=0,
            zoom=4
        ),
    )


    fig = dict(data=data, layout=layout)

    return fig
### ===================================================================
### ===================================================================
### ALL EO LESSON PLANS GO HERE
### ===================================================================
### ===================================================================

### ===================================================================
### Tabs for main page
### ===================================================================


### Callback for EO lesson tabs
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        output = TIR_Tools.TIR_Walkthrough()

    elif tab == 'tab-2':
        output = Satellite_Tools.Satellite_Walkthrough()

    elif tab == 'tab-3':
        output = html.Div(children = [
            html.H3('More info & links'),
            html.H3('Links to jupyter notebooks')

        ])

    return output

### ===================================================================
### File uploader callback
### ===================================================================

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(contents, filename, dates):
    if contents is not None:

        return filename


### ===================================================================
### Load example data
### ===================================================================
# Intermediate step to store data in secret div
@app.callback(Output('stored_data', 'children'),
              [Input('Example_Data_button', 'n_clicks')],
              [State('timesteps','value')])
def load_content(n_clicks,timesteps):
    if n_clicks:
        example_data = TIR_Tools.Get_Example_Data(timesteps)
        # from sys import getsizeof
        # print(getsizeof(example_data.to_json(orient = 'split')))
        return example_data.to_json(orient = 'split')


## Callback for TIR Use example data
@app.callback(Output('output-example-data', 'children'),
              [Input('show_data', 'on'),
              Input('stored_data', 'children')])
def create_data_table(on,data_store):
    if on:
        try:
            data = pd.read_json(data_store,orient = 'split')
            data_table = html.Div(id = 'table_container', children = [
                html.H3('Thermal Data:'),
                dash_table.DataTable(id = 'Example_Data_Table',
                    columns = [{"name": i, "id": i} for i in data.columns],
                    data=data.to_dict('rows'),
                    style_table = {'maxHeight':300,
                            'overflowY':'scroll'}),
                html.Br(),
                html.Br(),
                html.Hr(),
            ])
        except (ValueError) as e:
            data_table = html.Div(html.H3('No data loaded'), style = {'textAlign':'center'})
    else:
        try:
            data = TIR_Data_Process.from_stored_json(data_store)
            data_table = html.Div(html.H3('Data Hidden'), style = {'textAlign':'center'})
        except (ValueError, AttributeError) as e:
            data_table = html.Div(html.H3('No data loaded'), style = {'textAlign':'center'})
    return data_table

## Callback to describe the data
@app.callback(Output('data_desc_holder', 'children'),
              [Input('stored_data', 'children')])
def data_desciber(data_store):
    try:
        data = TIR_Data_Process.from_stored_json(data_store)

        stats_table = TIR_Tools.StatsTable(data)
    except (ValueError, AttributeError) as e:
        stats_table = html.Div(html.H3('Load in some data to see descriptive statistics'))
    return stats_table

#### *********** EO Lessons HISTOGRAM PLOT *******************

# Callback for the time slider with the contour plot
@app.callback(Output('ContourSlider', 'max'),
    [Input('timesteps','value')])
def define_slider(max_val):
    return max_val

# Label for the timesteps
@app.callback(Output('timestep_label', 'children'),
    [Input('timesteps','value'),
    Input('ContourSlider', 'value')])
def timestep_label(max_val, slide_val):
    s = 'Showing timestep {} out of {}.'.format(slide_val, max_val)
    return s

#### Callback for the contour plot
@app.callback(Output('EOContour', 'children'),
    [Input('stored_data', 'children'),
    Input('EOContourTitle', 'value'),
    Input('ContourSlider','value')
    ])
def change_contour(data_store, title, slider_val):
    try:
        data = TIR_Data_Process.from_stored_json(data_store)
        from dataplot.DataTools.AnalysisTools import ContourPlot

        return ContourPlot.EO_Lesson_Contour(data,title = title,
        timestep = slider_val)
    except (ValueError, AttributeError) as e:
        return ''



#### Callback for the Histogram plot
@app.callback(Output('EOHistogram', 'children'),
    [Input('stored_data', 'children'),
    Input('EOHistogramTitle', 'value'),
    Input('HistBinSlider','value'),
    Input('EOHistogramProbability','values')
    ])
def change_histogram(data_store, title, histbins, probability):
    try:
        data = TIR_Data_Process.from_stored_json(data_store)
        from dataplot.DataTools.AnalysisTools import Histogram

        return Histogram.EO_Lesson_Hist(data, histbins = histbins,
        title = title, probability = probability )
    except (ValueError, AttributeError) as e:
        return ''


#### Callback for the tiemseries plot
@app.callback(Output('EOTimeSeries', 'children'),
    [Input('stored_data', 'children'),
    Input('EOTimeSeriesTitle', 'value'),
    Input('EOTimeSeriesLine', 'value'),
    Input('EOTimeSeriesMeanMinMax', 'values')])
def Change_Timeseries(data_store, title, linemode, linetype):
    try:
        data = TIR_Data_Process.from_stored_json(data_store)
        if data.shape[0] < 2:
            return html.P('Need more than one timestep to create a timeseries')
        else:
            from dataplot.DataTools.AnalysisTools import TimeSeries

            return TimeSeries.EO_Lessons_TimeSeries(data, title = title,
            linemode = linemode, stattype = linetype )
    except (ValueError, AttributeError) as e:
        return ''


#### *********** EO Lessons Satellite Imagery *******************

### Callback to select different wavelengths

@app.callback(Output('satellite_image_holder', 'children'),
    [Input('img_tabs', 'value')])
def Satellite_Image_renderer(value):
    img = Satellite_Tools.render_image(value)
    # img = html.Img(src='https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/fire_count.png')
    return img


### Callback to show fire locations on map

@app.callback(Output('FireMapHolder', 'children'),
    [Input('show_fire_button', 'n_clicks')])
def Satellite_Image_renderer(clicked):
    if clicked:
        from dataplot.EO_Lesson_Tools import Scatter_map
        f_map = Scatter_map.fire_loc_map()
        return f_map


### ===================================================================
### END OF PROGRAM
### ===================================================================
