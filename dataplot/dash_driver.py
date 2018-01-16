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

    app = _create_app(request)
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

def _create_app(request):
    '''
    Creates the dash application
    '''
    app = dash.Dash(csrf_protect = False)
    app.layout = html.Div([
        html.Div([dcc.RadioItems(
                id='resampling',
                options=[{'label': i, 'value': i} for i in ['Daily', 'Weekly','Monthly']],
                value='Daily',
                labelStyle={'display': 'inline-block'}
            )]),
        html.Div(children = [
        dcc.Location(id = 'url', refresh = False),
        html.Div(id = 'content')
    ])
    ])

    @app.callback(
        dash.dependencies.Output('content', 'children'),
        [dash.dependencies.Input('url', 'pathname'),
        dash.dependencies.Input('resampling','value')]
    )
    def display_page(pathname, resample_type):
        if not pathname:
            return ''


        sites = request.session['sites']
        vars_chosen = request.session['variables']
        if request.session['combine'][0] == 'combined':
            var_combined = True
        else:
            var_combined = False

        # Get the second part of the path name (dash-toolname)
        tool_type = request.session['plot_paths'][pathname]

        method = 'MainDriver'
        #method = pathname[1:].replace('-','_')
        func = getattr(sys.modules[__name__], method, None)

        if func:
            return func(tool_type = tool_type, sites = sites,
                variables_chosen = vars_chosen, vars_combined = var_combined,
                resampling = resample_type)
        return 'Plot Driver Unavailable'
    return app
