from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input



def main_page():
    page_layout = html.Div(children =
    ### The first items are for the common attributes (ie site)
    [dcc.RadioItems(
        id = 'site_choice',
        options = [{'label': i, 'value': i} for i in ['Edinburgh', 'Heathfield']],
        value = 'Edinburgh'
    ),
    html.Br(),

    dcc.Dropdown(id = 'variable_options',
    # multi = True,
    placeholder = 'Select variables'),
    html.Br(),

    dcc.RadioItems(id = 'combine_choice',
    options = [{'label': i, 'value': i} for i in ['Combine', 'Seperate']],
    value = 'Combine'),
    html.Br(),

    # Resample the data
    dcc.RadioItems(id = 'DataResample',
        options = [{'label': i, 'value': i} for i in ['Raw','Daily', 'Weekly','Monthly']],
        value = 'Daily'),
    html.Br(),

    dcc.RangeSlider( id = 'date-slider', min = 0),# updatemode = 'drag' ),
    html.Br(),

    html.Div( id = 'date-choice'),
    html.Hr(),
    ### Each placeholder for plots and their individual controls go below
    ### TimeSeries
    html.Div(id = 'TimeSeries'),
    html.Br(),
    dcc.Checklist(id = 'TimeSeriesRollingMean',
        values = [],
        labelStyle={'display': 'inline-block'}),
    html.Hr(),
    ### Histogram
    html.Div(id = 'Histogram'),
    html.Br(),
    html.Hr(),

    ### Hourly boxplots
    html.Div(id = 'HourlyBoxplots'),
    html.Br(),
    html.Hr(),

    ### Weekly boxplots
    html.Div(id = 'WeeklyBoxplots'),
    html.Br(),
    html.Hr(),

    ### Monthly boxplots
    # html.Div(id = 'MonthlyBoxplots'),
    # html.Br(),
    # html.Hr(),

    ])
    return page_layout

def TimeSeries():

    page_layout = html.Div(children = [
    html.Div(children = 'Time Series Plot'),
    # dcc.Dropdown(
    #     id='app-1-dropdown',
    #     options=[
    #         {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
    #             'NYC', 'MTL', 'LA'
    #         ]
    #     ]
    # ),
    html.Div(id = 'main-graph')])

    return page_layout


### ===================================================================
### END OF PROGRAM
### ===================================================================
