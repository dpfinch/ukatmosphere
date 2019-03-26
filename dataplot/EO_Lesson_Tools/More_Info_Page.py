import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import dash_table
import dash_daq as daq
from dataplot.EO_Lesson_Tools import Text_Providers

def more_info_holder():
    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Br(),
    html.H2('More Analysis'),
    html.H3('Jupyter Notebooks'),
    html.Br(),
    html.H2('More Information'),
    html.Br(),
    html.A(html.Button('Return to EO-Pi Site'), href = 'https://sites.google.com/view/eoscience/home'),
    html.Br(),
    html.Hr(),
    html.P(children = ['Any questions or issues? Email ', html.A('Doug Finch', href = 'mailto:d.finch@ed.ac.uk')]),
    ])

    return page_layout
