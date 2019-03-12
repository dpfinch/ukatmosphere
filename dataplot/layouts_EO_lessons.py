from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData

def EO_Lessons():

    EO_lesson_list = ['Thermal Camera Analysis', 'Satellite Fire Detection']
    lesson_options  = [{'label': i.strip(), 'value': i.strip()} for i in EO_lesson_list]

    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'eo-pi-logo', href="/dataplot/EO_Lessons")]),
        html.Div(id = 'page-header-holder', children = [html.A('Earth Observation',id = "page-header-text", href = "/dataplot/EO_Lessons")]),
    ]),
    html.Div(className = 'page-body',children = [
        html.H1(id = 'UploadHolder', children = 'Learn about observing the Earth from space'),
        html.Br(),
        html.P(id = 'EO_lessons_intro', children = [
        'Earth observation info here.']),
    ]),

    html.Div([
    ### Create a hidden div to store the users data
    html.Div(id='stored_data', children = [], style={'display': 'none'}),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Thermal Sensor Analysis', value='tab-1'),
        dcc.Tab(label='Satellite Fire Detection', value='tab-2'),
        dcc.Tab(label='More Information', value='tab-3'),
    ]),
    html.Div(id='tabs-content'),
    ]),

])
    return page_layout
