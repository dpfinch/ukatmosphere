from flask import Flask, request, send_from_directory
from dash import Dash
import os
import redis
from flask_caching import Cache
from rq import Queue

# from flask.helpers import get_root_path
# print('Helllllooo')
# print(get_root_path(__name__))

# should start and end with a '/'
URL_BASE_PATHNAME = '/dataplot/'

server = Flask(__name__)#, static_folder = "static")

# external CSS stylesheets
external_stylesheets = [
    # 'http://127.0.0.1:8000/static/css/dataplot.css',
    # 'http://www.ukatmosphere.org/static/css/dataplot.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

external_scripts = [
    'https://www.googletagmanager.com/gtag/js?id=UA-142478083-1',
    'http://www.ukatmosphere.org/static/js/gtag.js'
    ]

app = Dash(
    __name__,
    server=server,
    url_base_pathname=URL_BASE_PATHNAME,
    # assets_folder = 'assets',
    # static_folder = 'static',
    external_stylesheets=external_stylesheets,
    external_scripts = external_scripts
)

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

app.config['suppress_callback_exceptions'] = True

app.title = "UK Atmosphere"
# app.config.update({
#     'routes_pathname_prefix': URL_BASE_PATHNAME
# })
# r = redis.from_url(os.environ.get("REDIS_URL"))
# print(r)
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379')
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)
conn = redis.from_url(CACHE_CONFIG['CACHE_REDIS_URL'])
queue = Queue(connection = conn)
# @server.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(server.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#my_css_url = "http://127.0.0.1:8000/static/css/dataplot.css"
# my_css_url = "http://www.ukatmosphere.org/static/css/dataplot.css"
#
# app.css.append_css({"external_url": my_css_url})
