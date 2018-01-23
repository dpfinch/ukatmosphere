from random import randint
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html

from .server import app
from . import router
from . import callbacks

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    dcc.Link('Index', href=app.url_base_pathname),
    ', ',
    dcc.Link('Figure 1', href=f'{app.url_base_pathname}fig1'),
    ', ',
    dcc.Link('Figure 2', href=f'{app.url_base_pathname}fig2'),
    html.Br(),
    html.Br(),
    html.Div(id='content')
])
