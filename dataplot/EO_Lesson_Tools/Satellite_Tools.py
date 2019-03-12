import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go

def Satellite_Walkthrough():

    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Br(),
    html.Div(id = 'Satellite_Images', children =[
    dcc.RadioItems(
        id = 'Satellite_image_selector',
        options=[
            {'label': '4um Wavelength', 'value': 'T4'},
            {'label': '11um Wavelength', 'value': 'T11'},
            {'label': '12um Wavelength', 'value': 'T12'},
            {'label': '0.6um Wavelength', 'value': 'p65'},
            {'label': '0.8um Wavelength', 'value': 'p86'},
        ],
        value='T4'
        ),
    html.Div(id = 'satellite_image_holder')
    ])
    ])

    return page_layout

def render_image(wavelength):
    img_width = 1600
    img_height = 900
    scale_factor = 0.5

    layout = go.Layout(
        xaxis = go.layout.XAxis(
            visible = False,
            range = [0, img_width*scale_factor]),
        yaxis = go.layout.YAxis(
            visible=False,
            range = [0, img_height*scale_factor],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor = 'x'),
        width = img_width*scale_factor,
        height = img_height*scale_factor,
        margin = {'l': 0, 'r': 0, 't': 0, 'b': 0},
        images = [go.layout.Image(
            x=0,
            sizex=img_width*scale_factor,
            y=img_height*scale_factor,
            sizey=img_height*scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source='https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg')]
    )
    # we add a scatter trace with data points in opposite corners to give the Autoscale feature a reference point
    fig = go.Figure(data=[{
        'x': [0, img_width*scale_factor],
        'y': [0, img_height*scale_factor],
        'mode': 'markers',
        'marker': {'opacity': 0}}],layout = layout)


    return fig
