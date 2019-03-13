import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import math
import string
from dataplot.EO_Lesson_Tools import TIR_Data_Process

def Get_Example_Data(timesteps):

    points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
    grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

    pixels = np.random.randint(18,34,[timesteps,64])

    full_arr = []

    for n in range(pixels.shape[0]):
        snapshot = griddata(points, pixels[n], (grid_x, grid_y), method='cubic')
        full_arr.append(snapshot)

    output = TIR_Data_Process.from_3d_numpy_to_pd(np.stack(full_arr))
    return output

def TIR_Walkthrough():
    page_layout = html.Div(id ='full_page_container', children =
    [html.Br(),
    dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files from the Thermal Sensor')
            ]),
            style={
                'width': '98%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '12px'
            },
            # Allow multiple files to be uploaded
            multiple=False),
    html.Div(children = [html.H2('OR'),
    html.Button('Use Example Data', id = 'Example_Data_button',
    style = {'width':'200px',
            'height':'50px',
        'borderRadius':'5px'}),
    html.Br(),
    daq.NumericInput(
      id='timesteps',
      min=1,
      max=1000,
      value=1,
      label='Choose number of timesteps',
      size = 120
    ),
        ], style = {'textAlign':'center'}),
    html.Br(),
    html.Div(id='data-gatherer', children = [], style = {'textAlign':'center'}),
    html.Br(),
    html.Hr(),
    ###
    html.Div(id='output-data-upload'),
    daq.BooleanSwitch(
        id = 'show_data',
        on=False,
        label="Show Data",
        labelPosition="bottom"
    ),
    html.Div(id='output-example-data', children = []),
    html.Br(),
    html.Hr(),
    html.H3('Data Description:'),
    html.Div(id = 'data_desc_holder'),
    html.Hr(),
    html.Hr(),
    # Contour plot of the data
    html.Div(id = 'EOContourHolder', className = 'plot_holder', children = [
        html.Div(id = 'EOContour', className = 'main_plot'),
        html.Div(id = 'EOContourTools', className = 'plot_tools', children = [
            html.H3('Contour Tools:'),
            html.Br(),
            html.Label('Plot Title '),
            dcc.Input( id = 'EOContourTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            html.P('Timestep:'),
            daq.Slider(
            id = 'ContourSlider',
            min = 1,
            step = 1,
            value = 1
            ),
            html.Br(),
            html.P(id='timestep_label'),
        ]),
    ]),
    html.P('Questions and information could go here'),
    html.H3('What features can you see in the contour plot?'),
    html.H3('What is the maximum and minimum tempearture?'),
    html.Hr(),
    # Some plots
    html.Div(id = 'EOHistogramHolder', className = 'plot_holder', children = [
        html.Div(id = 'EOHistogram', className = 'main_plot'),
        html.Div(id = 'EOHistogramTools', className = 'plot_tools', children = [
            html.H3('Histogram Tools:'),
            html.Br(),
            html.Label('Plot Title '),
            dcc.Input( id = 'EOHistogramTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            html.Label('Choose the maximum number of histogram bins'),
            daq.Slider(
            id = 'HistBinSlider',
            min = 1,
            max = 100,
            step = 1,
            value = 25,
            ),
            html.Br(),
            html.Br(),
            dcc.Checklist( id = 'EOHistogramProbability',
                options = [{'label':'Probability', 'value': 'Probability'}],
                values = []),

        ]),
    ]),
    html.H3('What is the most common (modal) tempearture?'),
    html.P('More information and questions'),
    html.Hr(),
    ## TimeSeries layout
    html.Div(id = 'EOTimeSeriesHolder', className = 'plot_holder', children = [
        html.Div(id = 'EOTimeSeries', className = 'main_plot'),
        html.Div(id = 'EOTimeSeriesTools', className = 'plot_tools', children = [
            html.H3('Timeseries Tools:'),
            html.Br(),
            html.Label('Plot Title '),
            dcc.Input( id = 'EOTimeSeriesTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            dcc.RadioItems(id = 'EOTimeSeriesLine',
            options = [{'label': i, 'value': i} for i in ['Scatter', 'Line', 'Line & Scatter']],
            value = 'Scatter',
            ),
            html.P('Choose which analysis to plot:'),
            dcc.Checklist(id = 'EOTimeSeriesMeanMinMax',
            options = [{'label': i, 'value': i} for i in ['Mean', 'Minimum', 'Maximum']],
            values = ['Mean'],
            )

        ]),
    ]),
    ## Put a buffer on the bottom of the page so it looks nicer
    html.Br(),
    html.Br(),
    html.Br(),
    ])
    return page_layout

def StatsTable(df):
    dims = df.shape
    mean = df.mean().mean()
    std = df.std().std()

    desc_layout = html.Div(children = [
    html.P('The data is a {}D array with the dimensions of {}'.format(len(dims), dims)),
    html.P('The mean of the data is: {}'.format(mean)),
    html.P('The standard deviation of the data is: {}'.format(std))
    ])

    return desc_layout
