import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import dash_table
import dash_daq as daq
from dataplot.EO_Lesson_Tools import Text_Providers

def more_info_holder():
    page_layout = html.Div(id = 'full_page_container', children =
    [
        html.Br(),
        html.Div(className = 'text_holder', children = [
        html.H2('More Analysis'),
        Text_Providers.More_Analysis_text(),
        html.H3('Lessons and Jupyter Notebooks'),
        Text_Providers.jupyter_text(),
        html.Br(),
        html.H2('More Information'),
        html.P('For more information, check out these other websites:'),
        html.A('UK Space Agency', href = 'https://www.gov.uk/government/organisations/uk-space-agency',target="_blank" ),
        html.P(''),
        html.A('ESA School Atlas', href = 'https://earth.esa.int/web/guest/eo-education-and-trainingweb/eo-edu/esa-school-atlas',target="_blank" ),
        html.P(''),
        html.A('NASA EOSDIS Worldview', href = 'https://worldview.earthdata.nasa.gov/',target="_blank" ),
        html.P(''),
        html.A('Global Fire Emission Database', href = 'https://www.globalfiredata.org/index.html',target="_blank" ),
        html.Br(),
        html.Br(),
        html.Div(id = 'return_button_holder', children = [
        html.A(html.Button(children = ['Return to EO-Pi Site'],id = 'EO_PI_link' ),
            href = 'https://sites.google.com/view/eoscience/home'),]),
        html.Br(),
        html.Hr(),
        html.P(children = ['Any questions or issues? Email ', html.A('Doug Finch', href = 'mailto:d.finch@ed.ac.uk')]),
    ]),
    ])

    return page_layout
