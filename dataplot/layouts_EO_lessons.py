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
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'eo-pi-logo', href="/dataplot/EO_Lessons")]),
        html.Div(id = 'page-header-holder', children = [html.A('Earth Observation',id = "page-header-text", href = "/dataplot/EO_Lessons")]),
    ]),
    html.Div(className = 'page-body',children = [
        html.H1(id = 'UploadHolder', children = 'Choose a lesson...'),
        html.Br(),
        html.P(id = 'EO_lessons_intro', children = [
        'Earth observation is good.']),
    ]),
    html.Div([

    html.Div(className='EO_Home_Page', children = [
    html.Div(className='Link_Box', children = [
        html.Div(className='LinkTIR', children = [
    dcc.Link('Thermal Camera Quick Play', href='/app1', className='Link_Text'),
    ])]),


    html.Div(className='Link_Box', children = [
        html.Div(className='LinkLessons',children = [
    dcc.Link('EO Lessons', href='/app2', className='Link_Text'),
    ])]),

    ])])
])
    return page_layout