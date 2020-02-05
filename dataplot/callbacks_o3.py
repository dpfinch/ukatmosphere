###### CALLBACKS FOR OZONE PAGE
from .server import app, cache, conn, queue
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
from dataplot.DataTools import AnalysisDriver
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData
import pandas as pd
from rq import get_current_job
from rq.exceptions import NoSuchJobError
from rq.job import Job
import time
import uuid

@app.callback(Output('o3_minimum_year', 'options'),
    [Input('o3_env_choice','value'),
    Input('o3_region_choice','value')])
def get_site_minimum_year(environment,region):
    species = 'Ozone'
    # start_year, end_year = LoadData.get_species_year_range(species, environment, region)
    start_year = 1979
    end_year = 2019
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

@app.callback(Output('o3_meta_data_text', 'children'),
    [Input('o3_go_button', 'n_clicks')],
    [State('o3_site_open','on'),
    State('o3_env_choice','value'),
    State('o3_region_choice','value'),
    State('o3_minimum_year','value'),
    State('o3_maximum_year','value')])
def meta_data_text(clicked,sites_open,environment, region, year_min, year_max):
    species = 'Ozone'
    if year_min and year_max:
        sites_df = LoadData.Get_Species_Sites(species,environment,region,sites_open,
            year_min,year_max)

        table = dash_table.DataTable(
            id = 'o3_site_table',
            columns = [{"name": i, "id": i} for i in sites_df.columns],
            data= sites_df.to_dict('records'),
            sort_action = 'native',
            style_table={'maxHeight':288,
                'overflowX': 'scroll'},
            style_header={
            'textAlign': 'center',
            'backgroundColor': 'white',
            'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'},
            style_as_list_view=True,
            # row_selectable="multi",
        )
        count_estimate = str(LoadData.Estimate_data_count(species, sites_df,year_min, year_max))
        if len(count_estimate) > 6:
            message = 'There are approximately {} million data points. This will take a while to load and process.'.format(count_estimate[:-6])
        elif len(count_estimate) <= 6 and len(count_estimate) > 4:
            message = 'Approximately {} data points found'.format(int(count_estimate) - int(count_estimate)%1000)
        else:
            message = 'Approximately {} data points found'.format(count_estimate)

        output = html.Div(children = [html.P(message, style = {'color':'red'}),
            html.Br(),table])
    else:
        output = html.P('Select years to analyse')
    return output

@cache.memoize()
def get_o3_meta_data(species, environment, region, year_start, year_end):
    if year_start and year_end:
        df = LoadData.get_all_species_obvs(species, environment, region,year_start, year_end)
    else:
        df = 0
    return df

### Callback to load the data into the page
@app.callback(Output('o3_metadata-holder', 'children'),
    [Input('o3_go_button', 'n_clicks')],
    [State('o3_env_choice', 'value'),
    State('o3_region_choice','value'),
    State('o3_minimum_year', 'value'),
    State('o3_maximum_year', 'value'),
    ])
def load_o3_meta_data(button_clicked,environment,region, year_start, year_end):
    species = 'Ozone'
    get_o3_meta_data(species, environment, region,year_start,year_end )
    info_string = 'DEFRA AURN,{},{},{},{},{}'.format(species,environment, region, year_start, year_end)
    return info_string



@app.callback([Output('load_id_store','data'),
    Output('o3_load_bar','max')],
    [Input('o3_load_button','n_clicks')],
    [State('o3_meta_data_text', 'children'),
    State('o3_minimum_year','value'),
    State('o3_maximum_year','value')])
def load_data_via_worker(n_clicks,o3_table_text,year_start,year_end):
    if n_clicks and o3_table_text:
        table_data = o3_table_text['props']['children'][2]['props']['data']
        sites = []
        for row in table_data:
            sites.append(row['Site Name'])

        id_ = uuid.uuid4()
        species = 'Ozone'
        queue.enqueue(LoadData.multi_site_loop,sites,year_start,year_end,species,
            job_id = str(id_), timeout=500)
        return {"id": str(id_),'site_list':sites},len(sites)
    else:
        return {},100

@cache.memoize()
def get_final_loaded_data(load_id):
    job = Job.fetch(load_id['id'],connection = conn)
    total_df = job.result
    return total_df

@app.callback([Output('o3_load_bar','value'),
    Output('loaded_sites2','children'),
    Output('Interval','disabled')],
    [Input('Interval','n_intervals')],
    [State('load_id_store','data')])
def progress_getter(n_intervals,load_id):
    if n_intervals and load_id:
        try:
            sites = load_id['site_list']
            job = Job.fetch(load_id['id'],connection = conn)

            if job.get_status() == 'finished':
                total_df = get_final_loaded_data(load_id)
                return len(sites),'All Sites Processed',True
            else:
                return job.meta.get('progress') + 1, 'Loading: {}'.format(job.meta.get('current_site')), False
        except NoSuchJobError:
            return 0,'', False
    else:
        return 0,'',False


@cache.memoize()
def site_count_data(species,split_by):
    site_count_df = LoadData.Yearly_Site_Count(species,split_by = split_by)
    return site_count_df

### Callback for the TimeSeries plot
@app.callback(Output('O3_SiteCountPlot','children'),
    [Input('O3_SiteCountTitle','value'),
    Input('Site_Count_Split','value')])
def change_site_count_plot(plot_title,site_split):
    species = 'Ozone'
    if site_split == 'Region':
        split_by = 'region'
    elif site_split == 'Environment Type':
        split_by = 'environment'
    else:
        split_by = None

    site_count_df = site_count_data(species, split_by = split_by)

    from dataplot.DataTools.Ozone_Stat_Tools import O3_site_count
    return O3_site_count.site_count_timeseries(
        site_count_df, plot_title = plot_title)


## Callback for the TimeSeries plot
@app.callback(Output('O3_TimeSeries', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_TimeSeriesTitle','value'),
    Input('O3_TimeSeriesXTitle', 'value'),
    Input('O3_TimeSeriesYTitle', 'value'),
    Input('O3_ValueType', 'value'),
    Input('O3_Env_or_Regions','value'),
    Input('O3_TimeSeriesLineOrScatter', 'value'),
    Input('O3_TimeSeriesLabelFormat', 'value')],
    [State('o3_meta_data_text', 'children')])
def change_o3_timeseries(load_id,sites_loaded,title, xtitle, ytitle, value_type,
    env_or_region, lineorscatter, label_format, o3_table_text):
    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    df = df_dict['conc']
    if not isinstance(df, pd.DataFrame):
        return ''

    from dataplot.DataTools.Ozone_Stat_Tools import O3_Timeseries

    return O3_Timeseries.TimeSeries(df, o3_table_text,
        title = title, value_type = value_type, xtitle = xtitle, ytitle = ytitle,
        env_or_region = env_or_region,lineorscatter = lineorscatter,
        label_format = label_format )


## Callback for the TimeSeries plot
@app.callback(Output('o3_trend_table', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_Env_or_Regions','value')],
    [State('o3_meta_data_text', 'children')])
def make_trend_table(load_id,sites_loaded, env_or_region,o3_table_text):

    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    df = df_dict['conc']
    if not isinstance(df, pd.DataFrame):
        return ''
    from dataplot.DataTools.Ozone_Stat_Tools import O3_Trend_Calcs

    trends = O3_Trend_Calcs.GetTrends(df,o3_table_text,env_or_region = env_or_region)

    table = dash_table.DataTable(
        id = 'o3_trend_table',
        columns = [{"name": i, "id": i} for i in trends.columns],
        data= trends.to_dict('records'),
        sort_action = 'native',
        style_table={'maxHeight':288,
            'overflowX': 'scroll'},
        style_header={
        'textAlign': 'center',
        'backgroundColor': 'rgb(30, 30, 30)',
        'fontWeight': 'bold'},
        style_cell={'textAlign': 'left',
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'},
        # style_as_list_view=True,
        # row_selectable="multi",
    )

    return html.P(children = [html.H2('Mean Ozone Trends:'),html.Br(),table])


## Callback for the gamma plot
@app.callback(Output('O3_Gamma_Plot', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_GammaTitle','value')],
    [State('o3_meta_data_text', 'children')])
def Create_Gamma_plots(load_id,sites_loaded,title, o3_table_text):
    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    gamma_dict = df_dict['gamma']
    if not isinstance(gamma_dict, dict):
        return ''
    return html.P('Gamma plots currently unsupported')
    # from dataplot.DataTools.Ozone_Stat_Tools import O3_Gamma_Plots
    #
    # return O3_Gamma_Plots.GammaPlot(gamma_dict,title = title)

## Callback for the yearly exceedances plot
@app.callback(Output('O3_YearlyExceed', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_YearlyExceedTitle','value')],
    [State('o3_meta_data_text', 'children')])
def Yearly_Exceedance_plots(load_id,sites_loaded,title, o3_table_text):
    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    df = df_dict['exceedance']
    if not isinstance(df, pd.DataFrame):
        return ''
    from dataplot.DataTools.Ozone_Stat_Tools import Exceedance_Plots

    return Exceedance_Plots.total_exceedances(df, resample = 'year',
        title = title)

## Callback for the yearly exceedances plot
@app.callback(Output('O3_YearlySiteExceed', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_YearlySiteExceedTitle','value')],
    [State('o3_meta_data_text', 'children')])
def Yearly_Exceedance_plots(load_id,sites_loaded,title, o3_table_text):
    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    df = df_dict['sitesabove']
    if not isinstance(df, pd.DataFrame):
        return ''
    from dataplot.DataTools.Ozone_Stat_Tools import Exceedance_Plots

    return Exceedance_Plots.yearly_sites_exceeding(df,
        title = title)

## Callback for the monthly exceedances plot
@app.callback(Output('O3_MonthlyExceed', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_MonthlyExceedTitle','value')],
    [State('o3_meta_data_text', 'children')])
def Monthly_Exceedance_plots(load_id,sites_loaded,title, o3_table_text):
    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    df = df_dict['exceedance']
    if not isinstance(df, pd.DataFrame):
        return ''
    from dataplot.DataTools.Ozone_Stat_Tools import Exceedance_Plots

    return Exceedance_Plots.total_exceedances(df, resample = 'month',
        title = title)

## Callback for the weekly exceedances plot
@app.callback(Output('O3_WeeklyExceed', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_WeeklyExceedTitle','value')],
    [State('o3_meta_data_text', 'children')])
def Weekly_Exceedance_plots(load_id,sites_loaded,title, o3_table_text):
    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    df = df_dict['exceedance']
    if not isinstance(df, pd.DataFrame):
        return ''
    from dataplot.DataTools.Ozone_Stat_Tools import Exceedance_Plots

    return Exceedance_Plots.total_exceedances(df, resample = 'week day',
        title = title)

## Callback for the weekly exceedances plot
@app.callback(Output('O3_ExceedMap', 'children'),
    [Input('load_id_store', 'data'),
    Input('loaded_sites2','children'),
    Input('O3_ExceedMapTitle','value')],
    [State('o3_meta_data_text', 'children')])
def Weekly_Exceedance_plots(load_id,sites_loaded,title, o3_table_text):
    if not load_id:
        return ''
    df_dict = get_final_loaded_data(load_id)
    if not isinstance(df_dict, dict):
        return ''
    df = df_dict['exceedance']
    if not isinstance(df, pd.DataFrame):
        return ''
    # from dataplot.DataTools.Ozone_Stat_Tools import Exceedance_Plots
    #
    # return Exceedance_Plots.total_exceedances(df, resample = 'week day',
    #     title = title)
    return html.P('Exceedance mapping is currently unsupported')
