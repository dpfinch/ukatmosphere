from flask import Flask, request, send_from_directory
from dash import Dash
import os
import redis
from flask_caching import Cache

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

# r = redis.from_url(os.environ.get("REDIS_URL"))
# print(r)
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'localhost:6379')
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)
# @server.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(server.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#my_css_url = "http://127.0.0.1:8000/static/css/dataplot.css"
my_css_url = "http://www.ukatmosphere.org/static/css/dataplot.css"

app.css.append_css({"external_url": my_css_url})
