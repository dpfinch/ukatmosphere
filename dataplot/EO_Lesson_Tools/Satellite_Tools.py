import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import dash_table
import dash_daq as daq
from dataplot.EO_Lesson_Tools import Text_Providers

def Satellite_Walkthrough():

    page_layout = html.Div(id ='full_page_container', children =
    [
    html.Br(),
    html.Div(id='coastline_data', children = [], style={'display': 'none'}),
    html.Div(),
    html.Div(id='Firepic', children = [
    html.Img(src='https://ktfnews.com/wp-content/uploads/2017/10/Black-Saturday.jpeg',
    style = {'height':'400px'}),
    html.Div(id = 'Satellite_Images', children =[
    html.Br(),
    html.H2('Sentinel 2 Brightness Temperature Over Australia'),
    html.Div(id = 'Sentinenl_Info_holder', children = [
    Text_Providers.Sentinenl_Info()], style = {'textAlign':'left',
        'padding':'20px'}),
    html.P('Look at the different wavelengths - what do they highlight?'),
    dcc.Tabs(id="img_tabs", value='T4', children=[
        dcc.Tab(label='4\265m Wavelength', value='T4'),
        dcc.Tab(label='11\265m Wavelength', value='T11'),
        dcc.Tab(label='12\265m Wavelength', value='T12'),
        dcc.Tab(label='0.6\265m Wavelength', value='p65'),
        dcc.Tab(label='0.8\265m Wavelength', value='p86'),
    ]),
    # dcc.RadioItems(
    #     id = 'Satellite_image_selector',
    #     options=[
    #         {'label': '4\265m Wavelength', 'value': 'T4'},
    #         {'label': '11\265m Wavelength', 'value': 'T11'},
    #         {'label': '12\265m Wavelength', 'value': 'T12'},
    #         {'label': '0.6\265m Wavelength', 'value': 'p65'},
    #         {'label': '0.8\265m Wavelength', 'value': 'p86'},
    #     ],
    #     value='T4'
    #     ),

    html.Div(id = 'Satellite_Image_Holder', className = 'plot_holder', children = [
        html.H3('Satellite data may take a few seconds to load...'),
        html.Br(),
        html.Div(id = 'Satellite_Image', className = 'satellite_plot',
                ),
        html.Div(id = 'Sat_Img_Tools', className = 'plot_tools', children = [
            html.H3('Image Tools:'),
            html.Br(),
            html.Label('Plot Title '),
            dcc.Input( id = 'Sat_Img_Title',
                placeholder = 'Enter Title',
                value = ''),
            html.Br(),
            html.Br(),
            html.Button(children = [], id = 'remove_310_K',
                style = {'width':'200px',
                        'height':'50px',
                    'borderRadius':'5px'}),
            html.Br(),
            html.Br(),
            daq.BooleanSwitch(
                id = 'cloud_mask',
                on=False,
                label="Mask Clouds",
                labelPosition="top"
            ),
            html.Br(),
        html.Button(children = [], id = 'reveal_fires',
            style = {'width':'200px',
                    'height':'50px',
                'borderRadius':'5px'}),
        ]),
    ]),
    html.Hr(),
    html.Br(),
    html.Br(),
    ])], style = {'textAlign':'center'}),
    html.Hr(),

    ])

    return page_layout

def render_image(wavelength):

    img_width = 1600
    img_height = 1400
    scale_factor = 0.5

    layout = dict(
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
            source='https://raw.githubusercontent.com/dpfinch/ukatmosphere/master/dataplot/assets/{}_Aus.png'.format(wavelength))]
    )
    # we add a scatter trace with data points in opposite corners to give the Autoscale feature a reference point
    data=[{
        'x': [0, img_width*scale_factor],
        'y': [0, img_height*scale_factor],
        'mode': 'markers',
        'marker': {'opacity': 0}}]


    img = html.Div(children = [
    html.H3('Brightness temperature at the {} wavelength band'.format(wavelength)),
    dcc.Graph(
        id = 'sat_image',
        figure = {
            'data':data,
            'layout':layout
        }
    )], style = {'margin':'auto'})

    return img
