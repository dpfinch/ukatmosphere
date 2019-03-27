from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData

def EO_Lessons():

    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'eo-pi-logo', href="https://sites.google.com/view/eoscience/home")]),
        html.Div(id = 'page-header-holder', children = [html.A('Earth Observation',id = "page-header-text", href = "/dataplot/EO_Lessons")]),
    ]),
    html.Div(className = 'page-body',children = [
        html.H1(id = 'UploadHolder', children = ['The World On Fire'], style = {'textAlign':'center'}),
        html.H3(id = 'EO_subheader', children =['Thermal Data Analysis'], style = {'textAlign':'center'}),
        html.Hr(),
        html.Br(),
        html.H4(id = 'EO_lessons_intro', children = [
        'Choose to either analyse some data from a thermal sensor or look at some satellite data.']),
    ]),

    html.Div([
    ### Create a hidden div to store the users data
    html.Div(id='stored_data', children = [], style={'display': 'none'}),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Thermal Sensor Analysis', value='tab-1'),
        dcc.Tab(label='Satellite Fire Detection', value='tab-2'),
        dcc.Tab(label='More Information & Lessons', value='tab-3'),
    ]),
    html.Div(id='tabs-content'),
    ]),

])
    return page_layout
