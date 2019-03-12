import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import math
import string

def Get_Example_Data():
    points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
    grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

    pixels = np.random.randint(18,34,64)

    output = griddata(points, pixels, (grid_x, grid_y), method='cubic')
    labels = list(string.ascii_letters)[:32]
    output = pd.DataFrame(data = output, index = labels,
        columns = labels)
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
    # Some plots
    html.Div(id = 'EOHistogramHolder', className = 'plot_holder', children = [
        html.Div(id = 'EOHistogram', className = 'main_plot'),
        html.Div(id = 'EOHistogramTools', className = 'plot_tools', children = [
            html.H3('Histogram Tools:'),
            html.Br(),
            html.Label('Plot Title'),
            dcc.Input( id = 'EOHistogramTitle',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            html.Label('Choose the maximum number of histogram bins'),
            dcc.Input( id = 'EOHistogramBins',
                placeholder = 'Number of bins...',
                value = '25'),
            html.Br(),
            html.Br(),
            dcc.Checklist( id = 'EOHistogramProbability',
                options = [{'label':'Probability', 'value': 'Probability'}],
                values = []),

        ]),
    ]),
    html.Hr(),

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
