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
from dataplot.EO_Lesson_Tools import Text_Providers

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
    html.H1(children = ['Thermal Sensor Data Analysis'],style = {'textAlign':'center'}),
    Text_Providers.TIR_Info(),
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
    html.Div(children = [html.H3('OR'),
    html.Button('Use Example Data', id = 'Example_Data_button',
    style = {'width':'200px',
            'height':'50px',
        'borderRadius':'5px'}),
    html.Br(),
    daq.NumericInput(
      id='timesteps',
      min=1,
      max=350,
      value=10,
      label='Choose number of timesteps',
      size = 120
    ),
        ], style = {'textAlign':'center'}),
    html.Br(),
    html.Div(id='data-gatherer', children = [], style = {'textAlign':'center'}),
    html.Br(),
    html.Hr(),
    ###
    html.Div([
    html.P("If the data is loaded, then you can look at it by switching the toggle below."),
    html.P("This will show a table full of numbers - this isn't very useful unless we analyise this data with the tools below."),
    html.Div(id='output-data-upload'),], className = 'text_holder'),
    daq.BooleanSwitch(
        id = 'show_data',
        on=False,
        label="Show Data",
        labelPosition="bottom"
    ),
    html.Div(id='output-example-data', children = []),
    html.Br(),
    html.Hr(),
    html.H3('Data Description:', style = {'padding':'30px'}),
    html.Div([
    html.P('Here are some statistics which tell us a few things about the data.'),
    ], className = 'text_holder'),
    html.Div(id = 'data_desc_holder'),
    html.Hr(),
    html.Hr(),
    # Contour plot of the data
    html.H2(children = ['Contour Plot'], style = {'textAlign':'center'}),
    Text_Providers.ContourInfo(),
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
            html.P('Move the slider to see what each time step of the data looks like.'),
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
    Text_Providers.AfterContour(),
    html.Hr(),
    # Some plots
    html.H2(children = ['Histogram'], style = {'textAlign':'center'}),
    Text_Providers.HistInfo(),
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
            html.P("You can change the plot from 'frequency' to 'probability' - this is how likely it is that a certain temperature will occur."),
            dcc.Checklist( id = 'EOHistogramProbability',
                options = [{'label':'Probability', 'value': 'Probability'}],
                values = []),

        ]),
    ]),
    html.H4('What is the most common (modal) temperature?'),
    html.P('More information and questions'),
    html.Hr(),
    ## TimeSeries layout
    html.H2(children = ['Timeseries Plot'], style = {'textAlign':'center'}),
    Text_Providers.TimeseriesInfo(),
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
    html.Hr(),
    html.P(children = ['Any questions or issues? Email ', html.A('Doug Finch', href = 'mailto:d.finch@ed.ac.uk')]),
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
