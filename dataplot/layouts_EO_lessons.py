from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData
import os

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
        html.P(os.uname())
    ]),
    html.Div([
        html.Div(className='Normal_Page', children = [
        html.H3('Thermal Camera (Fake output)'),

        html.Div(className = 'Buttons_Box', children = [
        html.Button('TIR Video Feed', id = 'TIR_Button'),
        html.Div(id='Button_container')]),
        html.Div(className = 'Buttons_Box', children = [
        html.Button('Take Snapshot', id = 'Snapshot_Button'),
        ]),
        html.Div(id='Snapshot_Contianer'),

        html.Div(id='app-1-display-value'),
        dcc.Link('Go to EO Lessons', href='/app2'),
        html.Br(),
        dcc.Link('Home', href='/')])
    ]),])
    return page_layout
