from dash.dependencies import Output, Input

from .server import app#, server
from . import layouts



pages = (
    ('main_page', layouts.main_page),
    # ('fig2', layouts.fig2),
    )

routes = {f"{app.url_base_pathname}{path}": layout for path, layout in pages}

@app.callback(Output('content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    ''' '''

    if pathname is None:
        return ''

    page = routes.get(pathname, 'Unknown link')

    if callable(page):
        # can add arguments to layout functions if needed etc
        layout = page()
    else:
        layout = page

    return layout
