
from .server import app, cache
from random import randint
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import pandas as pd
from dataplot.EO_Lesson_Tools import Satellite_Tools
from dataplot.EO_Lesson_Tools import TIR_Tools
from dataplot.EO_Lesson_Tools import TIR_Data_Process
from dataplot.EO_Lesson_Tools import Scatter_map
from dataplot.EO_Lesson_Tools import More_Info_Page
from dataplot.EO_Lesson_Tools import Text_Providers

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
        output = More_Info_Page.more_info_holder()

    return output

### ===================================================================
### File uploader callback
### ===================================================================

# @app.callback(Output('stored_data_actual', 'children'),
#               [Input('upload-data', 'contents')],
#               [State('upload-data', 'filename'),
#                State('upload-data', 'last_modified')])
# def update_output(contents, filename, dates):
#     if filename is not None:
#         passed = True
#         if filename.split('_')[0] != 'Thermal':
#             passed = False
#         if contents is None:
#             passed = False
#         if not 'csv' in filename:
#             passed = False
#
#         if passed:
#             json_txt = TIR_Tools.parse_data(contents, filename)
#             return json_txt
#         else:
#             return "This doesn't seem like a file from the Raspberry Pi"
#     # else:
#     #     return filename
#

### ===================================================================
### Load example data
### ===================================================================

# Intermediate step to store data in secret div
@app.callback(Output('stored_data', 'children'),
              [Input('upload-data', 'contents'),
              Input('Example_Data_button', 'n_clicks')],
              [State('timesteps','value'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              State('example_switch', 'on')
              ])
def load_content(contents,n_clicks, timesteps, filename, modified, example_on):
    if n_clicks:
        if example_on:
            out_data = TIR_Tools.Get_Example_Data(timesteps)
            out_data = out_data.to_json(orient = 'split')
        # elif filename is not None:
        else:
            out_data = TIR_Tools.parse_data(contents, filename)
        return out_data


@app.callback(Output('Example_button_holder', 'children'),
            [Input('example_switch', 'on')])
def turn_on_example_data(on):
    if on:
        return html.Div(children = [html.Br(),
            daq.NumericInput(
              id='timesteps',
              min=1,
              max=350,
              value=10,
              label='Choose number of timesteps',
              size = 120
            ),])

@app.callback(Output('upload-data', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(contents, filename, dates):
    if filename is not None:
        return filename
    else:
        return html.Div([
            'Drag and Drop or ',
            html.A('Select Files from the Thermal Sensor')
        ])


## Callback for TIR Use example data
@app.callback(Output('output-example-data', 'children'),
              [Input('show_data', 'on'),
              Input('stored_data', 'children'),
              ])
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
            data = pd.read_json(data_store,orient = 'split')
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
        stats_table = html.Div(html.H4('Load in some data to see descriptive statistics'),
        style = {'textAlign':'center'})
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

@app.callback(Output('coastline_data', 'children'),
    [Input('img_tabs', 'value'),])
def load_coastline_data(value):
    import os
    cwd = os.getcwd()
    coastline = pd.read_csv(cwd + '/dataplot/static/coastline.csv')
    return coastline.to_json(orient = 'split')
### Callback to select different wavelengths

@app.callback(Output('Satellite_Image', 'children'),
    [Input('img_tabs', 'value'),
    Input('cloud_1', 'on'),
    Input('cloud_2', 'on'),
    Input('cloud_3', 'on'),
    Input('land_1', 'on'),
    Input('land_2', 'on'),
    Input('reveal_fires', 'n_clicks'),
    Input('coastline_data', 'children')])
def Satellite_Image_renderer(value, cloud_1, cloud_2,
    cloud_3, land_1, land_2, show_fires, coastline_data):
    # If removing 310 K is clicked
    if not coastline_data:
        return [html.Br(),html.H3('Satellite data may take a few seconds to load...'),]

    masks = {'cloud_1':cloud_1, 'cloud_2':cloud_2, 'cloud_3':cloud_3, 'land_1':land_1, 'land_2':land_2}

    if show_fires:
        if show_fires%2:
            fires_on = True
        else:
            fires_on = False
    else:
        fires_on = False

    f_map = Scatter_map.simple_map(value, masks, fires_on, coastline_data)
    from dataplot.DataTools.AnalysisTools import Histogram
    f_hist = Histogram.Satellite_Hist(value, masks)

    hist_text = Text_Providers.Hist_Text()
    return [f_map, hist_text, f_hist]

@app.callback([Output('TempSlider', 'min'),
    Output('TempSlider', 'max'),
    Output('TempSlider', 'value'),
    Output('TempSlider', 'step')],
    [Input('img_tabs', 'value')])
def update_slider_limits(value):
    if value in ['T4','T11','T12']:
        new_min = 200
        new_max = 400
        outvalue = 200
        outstep = 1
    else:
        new_min = 0
        new_max = 1.5
        outvalue = 0
        outstep = 0.1
    return new_min, new_max, outvalue, outstep

@app.callback(Output('cloud_mask', 'label'),
    [Input('TempSlider', 'value'),
    Input('img_tabs','value')])
def update_mask_value(value, tab_val):
    if tab_val in ['T4','T11','T12']:
        unit = '\260K'
    else:
        unit = ''
    outlabel = 'Mask below {}{}'.format(value, unit)
    return outlabel


@app.callback([Output('reveal_fires', 'children'),
    Output('Fire_count_text', 'children')],
    [Input('reveal_fires','n_clicks')])
def fire_button_label(n_clicks):
    if n_clicks:
        if n_clicks%2:
            label  = 'Hide Fires'
            fire_count_text = Text_Providers.Fire_Count()
        else:
            label = 'Count Fires'
            fire_count_text = html.P('')
    else:
        label = 'Count Fires'
        fire_count_text = html.P('')

    return label, fire_count_text
