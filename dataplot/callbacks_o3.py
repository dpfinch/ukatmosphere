###### CALLBACKS FOR OZONE PAGE
from .server import app, cache
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
from dataplot.DataTools import AnalysisDriver
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData
import pandas as pd
import time

@app.callback(Output('o3_minimum_year', 'options'),
    [Input('o3_env_choice','value'),
    Input('o3_region_choice','value')])
def get_site_minimum_year(environment,region):
    species = 'Ozone'
    start_year, end_year = LoadData.get_species_year_range(species, environment, region)

    options = [{'label': i, 'value': i} for i in range(start_year,end_year + 1)]
    return options

@app.callback(Output('o3_maximum_year', 'options'),
    [Input('o3_minimum_year','options'),
    Input('o3_minimum_year','value')])
def get_site_maximum_year(year_options, year_choice):
    if year_choice:
        year_range = [x['value'] for x in year_options if x['value'] >= year_choice]
        year_options = [{'label': i, 'value': i} for i in year_range]
    return year_options

@cache.memoize()
def get_o3_data(species, environment, region, year_start, year_end):
    if year_start and year_end:
        df = LoadData.get_all_species_obvs(species, environment, region,year_start, year_end)
    else:
        df = 0
    return df

### Callback to load the data into the page
@app.callback(Output('o3_dataframe-holder', 'children'),
    [Input('o3_go_button', 'n_clicks')],
    [State('o3_env_choice', 'value'),
    State('o3_region_choice','value'),
    State('o3_minimum_year', 'value'),
    State('o3_maximum_year', 'value'),
    ])
def load_o3_data(button_clicked,environment,region, year_start, year_end):
    species = 'Ozone'
    get_o3_data(species, environment, region,year_start,year_end )
    info_string = 'DEFRA AURN,{},{},{},{},{}'.format(species,environment, region, year_start, year_end)
    return info_string


### Callback for the TimeSeries plot
@app.callback(Output('O3_TimeSeries', 'children'),
    [Input('o3_dataframe-holder', 'children'),
    Input('O3_TimeSeriesTitle','value'),
    Input('O3_TimeSeriesXTitle', 'value'),
    Input('O3_TimeSeriesYTitle', 'value'),
    Input('O3_TimeSeriesRollingMean', 'values'),
    Input('O3_TimeSeriesLineOrScatter', 'value'),
    Input('O3_TimeSeriesLabelFormat', 'value')
    ])
def change_o3_timeseries(data,title, xtitle, ytitle, rollingMean, lineorscatter, label_format):
    if not data:
        return ''
    data = data.split(',')
    df  = get_o3_data(data[1],data[2],data[3],int(data[4]), int(data[5]))
    if not isinstance(df, pd.DataFrame):
        return ''
    # variable_options = data[4:]
    from dataplot.DataTools.AnalysisTools import TimeSeries

    return 'The mininmum value is {}'.format(str(df.min().min()))
    # return TimeSeries.TimeSeries(df,variable_options =variable_options,
    #     site_choice = site_choice, combine_choice = combine_choice,
    #     DataResample = DataResample, date_range = date_range, title = title,
    #     rollingMean = rollingMean, xtitle = xtitle, ytitle = ytitle,
    #     lineorscatter = lineorscatter, label_format = label_format )

@app.callback(Output("loading-output-1", "children"), [Input("input-1", "value")])
def input_triggers_spinner(value):
    time.sleep(1)
    return value
