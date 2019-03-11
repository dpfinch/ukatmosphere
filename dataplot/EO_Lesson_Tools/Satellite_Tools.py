import dash_core_components as dcc
import dash_html_components as html

def quick_test():
    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Div([
            html.H3('Tab content 1')
        ])
    ])
    return page_layout
