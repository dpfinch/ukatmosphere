from random import randint
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html

from .server import app
from . import router
from . import callbacks
from . import callbacks_o3
from . import callbacks_EO_Lessons

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='content')
])
