import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

def quick_test():

    df_mean = 'dint work'
    output = html.Div([
            html.H3('Mean temp: '  + df_mean)
        ])

    return output

def TIR_Walkthrough():
    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Br(),
    html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files from the Thermal Sensor')
        ]),
        style={
            'width': '98%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '12px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    ]),
    html.Div([
        html.H2('OR')], style={'textAlign':'center'}),
    html.Div([
        html.Button('Use Example Data', id = 'Example_Data_button',
        style = {'width':'200px',
                'height':'50px',
            'borderRadius':'5px'})],
        style={'textAlign':'center'}),
    html.Br(),
    html.Div(id='output-data-upload'),
    html.Div(id='output-example-data'),
    ])
    return page_layout
