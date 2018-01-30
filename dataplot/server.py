from flask import Flask, request, send_from_directory
from dash import Dash
import os

# should start and end with a '/'
URL_BASE_PATHNAME = '/dataplot/'

server = Flask(__name__, static_folder = "static")

app = Dash(
    __name__,
    server=server,
    url_base_pathname=URL_BASE_PATHNAME
)

app.config['suppress_callback_exceptions'] = True

app.title = "UK Atmosphere"

# @server.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(server.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
my_css_url = "http://127.0.0.1:8000/static/css/dataplot.css"

app.css.append_css({"external_url": my_css_url})
