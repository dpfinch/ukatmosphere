from flask import Flask, request
from dash import Dash

# should start and end with a '/'
URL_BASE_PATHNAME = '/dataplot/'

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    url_base_pathname=URL_BASE_PATHNAME
)

app.config['suppress_callback_exceptions'] = True

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
