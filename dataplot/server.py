from flask import Flask
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
