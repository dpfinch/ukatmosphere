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
from dataplot.DataTools import Map_Plots_Renderer
import pandas as pd
from dataplot.EO_Lesson_Tools import Satellite_Tools
from dataplot.EO_Lesson_Tools import TIR_Tools
from dataplot.EO_Lesson_Tools import TIR_Data_Process
from dataplot.EO_Lesson_Tools import Scatter_map
from dataplot.EO_Lesson_Tools import More_Info_Page
from dataplot.EO_Lesson_Tools import Text_Providers


### ===================================================================
### The first callbacks are for the choices effecting every plot
### These outputs are to be included in every other callback.
### ===================================================================

### Callback to list the available sites with above selection
@app.callback(Output('site_choice', 'options'),
    [Input('site_region_choice', 'value'),
    Input('site_env_choice', 'value'),])
def list_available_sites(site_region, env_choice, open_sites_only = True):
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
@app.callback([Output('variable_options', 'options'),
    Output('site_choice_button','disabled')],
    [Input('site_choice', 'value')],
    )
def varaible_list(site):
    site_vars = LoadData.get_site_variables_db(site)
    var_options = [{'label': i.replace('<sub>','').replace('</sub>',''), 'value': i} for i in site_vars]

    return var_options, False

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
        return html.H4(TidyData.site_info_message(data_info))

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
    Input('TimeSeriesRollingMean', 'value'),
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

#### *********** COMPARISON PLOT *******************
### Callback for the COMPARISON interaction

@app.callback(Output('ComparisonYTitle', 'value'),
    [Input('dataframe-holder', 'children'),
    Input('ComparisonLabelFormat', 'value')])
def get_comparison_ytitle(data_info, format):
    if format == 'Variable Name':
        chemical_formula = False
    else:
        chemical_formula = True
    if not data_info:
        return ''
    variable_options = data_info.split(',')[4:]
    ytitle = TidyData.Axis_Title(variable_options, chemical_formula)
    return ytitle

@app.callback(Output('Comparisons', 'children'),
        [Input('dataframe-holder', 'children'),
        Input('variable_options','value'),
        Input('site_choice', 'value'),
        Input('DataResample', 'value'),
        Input('date-picker-range','start_date'),
        Input('date-picker-range','end_date'),
        Input('medianswitch','on'),
        Input('ComparisonTitle','value'),
        Input('ComparisonXTitle', 'value'),
        Input('ComparisonYTitle', 'value'),
        Input('ComparisonLabelFormat', 'value')])
def comparison_plot_renderer(data, variable_options,site_choice, DataResample,
    start_date,end_date,medianswitch, title, xtitle, ytitle,
    label_format):

    if not data:
        return ''
    data = data.split(',')

    # Find min year for site
    start_year, end_year = LoadData.get_site_year_range_db(data[1])

    df  = load_station_data(data[0],data[1],[start_year,int(data[3])], data[4:])
    if not isinstance(df, pd.DataFrame):
        return ''
    variable_options = data[4:]

    from dataplot.DataTools.AnalysisTools import ComparisonPlots
    # if comparison_tabs == 'week_comp':
    return ComparisonPlots.CompareWeeks(df,variable_options = variable_options,
        site_choice = site_choice, DataResample = DataResample,
        start_date = start_date, end_date = end_date, show_median = medianswitch,
        title = title,xtitle = xtitle, ytitle = ytitle, label_format = label_format)
    # if comparison_tabs == 'month_comp':
    #     return ComparisonPlots.CompareMonths(df,variable_options = variable_options,
    #         site_choice = site_choice, DataResample = DataResample, title = title,
    #         xtitle = xtitle, ytitle = ytitle, label_format = label_format,
    #         comp_month = comp_month,comp_year = comp_year)
    # if comparison_tabs == 'yearly_comp':
    #     return ComparisonPlots.CompareYears(df,variable_options = variable_options,
    #         site_choice = site_choice, DataResample = DataResample, title = title,
    #         xtitle = xtitle, ytitle = ytitle, label_format = label_format,
    #         comp_year = comp_year)


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
    Input('HistogramProbability','value'),
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

    variable_list = LoadData.get_site_variables_db(data[1])
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
    if ytitle.split(' ')[0][:2] == 'PM':
        ytitle = ytitle.split(' ')[0]
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
    Input('HourlyBoxMean', 'value'),
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
    Input('WeeklyBoxMean', 'value'),
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
@app.callback([Output('main_map','figure'),
                Output('site_counter_output', 'children')],
              [Input('map_env_choice','value'),
              Input('map_region_choice', 'value'),
              Input('map_species_choice','value')]
              # [State('main_map', 'relayoutData')]
              )
def create_map(environment, region, species):
    from dataplot.DataTools import Map_Renderer
    num_sites, map_fig  = Map_Renderer.main_site_map(environment, region, species)

    if environment != 'All' and environment[0] in ['A','E','I','O','U']:
        prefix = 'an'
    else:
        prefix = 'a'

    if num_sites == 0:
        site_count_message = 'There are no sites measuring {} {} environment in the {} region.'.format(prefix, environment.lower(), region)
    else:
        if environment == 'All' and region != 'All':
            site_count_message = 'Showing {} sites in the {} region for all environment types.'.format(num_sites, region)
        elif environment != 'All' and region == 'All':
            site_count_message = 'Showing {} sites measuring {} {} environment across the country.'.format(num_sites, prefix, environment.lower())
        elif environment == 'All' and region == 'All':
            site_count_message = 'Showing all {} sites across the country measuring all environment types.'.format(num_sites)
        else:
            site_count_message = 'Showing {} sites measuring {} {} environment in the {} region.'.format(num_sites, prefix,  environment.lower(), region)

    return map_fig, html.P(site_count_message)

# A call back to inteact with the map
@app.callback(Output('site_name_from_map','children'),
            [Input('main_map', 'clickData')])
def Get_point_info(clickData):
    if clickData:
        # print(clickData['points'][0]['text'])
        return clickData['points'][0]['text'].split(':')[0]
    else:
        return 'Edinburgh St Leonards'

# A callback to register the site chosen and the type of
#  data wanted and return a div with the data/info
@app.callback(Output('map_site_info', 'children'),
        [Input('main_map','clickData'),
        Input('map_tabs', 'value'),
        Input('map_species_choice','value')])
def site_information_from_map(clickData, tab_val, species):

    if not clickData:
        site_name = 'Edinburgh St Leonards'
    else:
        site_name = clickData['points'][0]['text'].split(':')[0]

    if tab_val == 'site_sum':
        return Map_Plots_Renderer.Site_Summary(site_name,species)
    elif tab_val == 'site_week':
        return Map_Plots_Renderer.Site_Week_Summary(site_name,species)
    else:
        return Map_Plots_Renderer.Site_Year_Summary(site_name, species)


### ===================================================================
### END OF PROGRAM
### ===================================================================
