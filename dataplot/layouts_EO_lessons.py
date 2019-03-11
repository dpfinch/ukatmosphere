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


    html.Label('Select a lesson:'),
    dcc.Dropdown(id = 'EO_lesson_choice',
        multi = False,
        options = lesson_options,
        value = 'All'),
    html.Br(),

    # html.Div([
    #
    # html.Div(className='EO_Home_Page', children = [
    # html.Div(className='Link_Box', children = [
    #     html.Div(className='LinkTIR', children = [
    # dcc.Link('Thermal Camera Analysis', href='/app1', className='Link_Text'),
    # ])]),
    #
    #
    # html.Div(className='Link_Box', children = [
    #     html.Div(className='LinkLessons',children = [
    # dcc.Link('Satellite Fire Detection', href='/app2', className='Link_Text'),
    # ])]),
    #
    # ])])
])
    return page_layout
