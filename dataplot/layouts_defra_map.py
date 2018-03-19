from random import randint
import dash_core_components as dcc
import dash_html_components as html
from .server import app
from dash.dependencies import Output, Input



def DEFRA_map_page():

    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'home-logo', href="/")]),
        html.Div(id = 'page-header-holder', children = [html.A('UK Atmosphere',id = "page-header-text", href = "/")]),
    ]),
    html.Div(className = 'page-body',children = [
    html.H1(id = 'Holder', children = 'This is where a map will go '),
    html.Br(),
    ])
    ]
    )
    return page_layout


### ===================================================================
### END OF PROGRAM
### ===================================================================
