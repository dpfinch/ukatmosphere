import sys
from random import randint

import dash
import dash_core_components as dcc
import dash_html_components as html
from dataplot.DataTools.AnalysisDriver import MainDriver

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
        html.Div(id = 'content')
    ])

    @app.callback(
        dash.dependencies.Output('content', 'children'),
        [dash.dependencies.Input('url', 'pathname')]
    )
    def display_page(pathname):
        if not pathname:
            return ''
            
        # For random pathnames (eg /dash-abcd123) need a reference
        # list or dictionary - do we even need a random pathname?

        # Get the second part of the path name (dash-toolname)
        tool_type = pathname.split('-')[-1]

        method = 'MainDriver'
        #method = pathname[1:].replace('-','_')
        func = getattr(sys.modules[__name__], method, None)

        if func:
            return func(tool_type = tool_type)
        return 'Plot Driver Unavailable'
    return app
