import sys
from random import randint

import dash
import dash_core_components as dcc
import dash_html_components as html

def dispatcher(request):
    '''
    Main Function
    '''

    app = _create_app()
    params = {
        'data':request.body,
        'method': request.method,
        'content_type':request.content_type
        }
    with app.server.test_request_context(request.path, **params):
        app.server.preprocess_request()
        try:
            response = app.server.full_dispatch_request()
        except Exception as e:
            response = app.server.make_response(app.server.handle_exception(e))
        return response.get_data()

def _create_app():
    '''
    Creates the dash application
    '''
    app = dash.Dash(csrf_protect = False)
    app.layout = html.Div(children = [
        dcc.Location(id = 'url', refresh = False),
        dcc.Link('Index', href = '/dash-index'),
        dcc.Link('Figure 1', href = '/dash-fig1'), ', ',
        dcc.Link('Figure 2', href = '/dash-fig2'), ', ',
        html.Br(),
        html.Br(),
        html.Div(id = 'content')
    ])

    @app.callback(
        dash.dependencies.Output('content', 'children'),
        [dash.dependencies.Input('url', 'pathname')]
    )
    def display_page(pathname):
        if not pathname:
            return ''
        if pathname == '/':
            return dash_index()
        method = pathname[1:].replace('-','_')
        func = getattr(sys.modules[__name__], method, None)
        if func:
            return func()
        return 'Unknown Link'
    return app

def dash_index():
    return "Welcome to the index page"

def dash_fig1():
    ''' '''
    return dcc.Graph(
        id='main-graph',
        figure={
            'data': [{
                'name': 'Some name',
                'mode': 'line',
                'line': {
                    'color': 'rgb(0, 0, 0)',
                    'opacity': 1
                },
                'type': 'scatter',
                'x': [randint(1, 100) for x in range(0, 20)],
                'y': [randint(1, 100) for x in range(0, 20)]
            }],
            'layout': {
                'autosize': True,
                'scene': {
                    'bgcolor': 'rgb(255, 255, 255)',
                    'xaxis': {
                        'titlefont': {'color': 'rgb(0, 0, 0)'},
                        'title': 'X-AXIS',
                        'color': 'rgb(0, 0, 0)'
                    },
                    'yaxis': {
                        'titlefont': {'color': 'rgb(0, 0, 0)'},
                        'title': 'Y-AXIS',
                        'color': 'rgb(0, 0, 0)'
                    }
                }
            }
        }
    )


def dash_fig2():
    ''' '''
    return dcc.Graph(
        id='main-graph',
        figure={
            'data': [{
                'name': 'Some name',
                'mode': 'line',
                'line': {
                    'color': 'rgb(0, 0, 0)',
                    'opacity': 1
                },
                'type': 'scatter',
                'x': [randint(1, 100) for x in range(0, 20)],
                'y': [randint(1, 100) for x in range(0, 20)]
            }],
            'layout': {
                'autosize': True,
                'scene': {
                    'bgcolor': 'rgb(255, 255, 255)',
                    'xaxis': {
                        'titlefont': {'color': 'rgb(0, 0, 0)'},
                        'title': 'X-AXIS',
                        'color': 'rgb(0, 0, 0)'
                    },
                    'yaxis': {
                        'titlefont': {'color': 'rgb(0, 0, 0)'},
                        'title': 'Y-AXIS',
                        'color': 'rgb(0, 0, 0)'
                    }
                }
            }
        }
    )
