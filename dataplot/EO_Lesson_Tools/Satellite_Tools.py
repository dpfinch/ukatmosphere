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
    html.Div(id='satellite_head_title', children = [html.H1('Detecting Fires From Space'),],
    style = {'textAlign':'center'}),
    html.Div(id='Firepic', children = [
    html.Img(id = 'main_fire_pic', src='https://ktfnews.com/wp-content/uploads/2017/10/Black-Saturday.jpeg',
    )]),
    html.Div(id = 'Sentinenl_Info_holder', children = [
    Text_Providers.Sentinenl_Info()], style = {'textAlign':'left',
        'padding':'20px'}),
    html.Div(id = 'Satellite_Images', children =[
    html.Br(),
    html.H2(children = ['Spotting fires over Australia'], style = {'textAlign':'center'}),
    html.P('Below is some satellite data - explain about it'),
    html.H3(children = ['Sentinel 2 Brightness Temperature'], style = {'textAlign':'center'}),

    html.P('Explanation of what this actually means'),
    html.P('Look at the different wavelengths - what do they highlight?'),
    dcc.Tabs(id="img_tabs", value='T4', children=[
        dcc.Tab(label='4\265m Wavelength', value='T4'),
        dcc.Tab(label='11\265m Wavelength', value='T11'),
        dcc.Tab(label='12\265m Wavelength', value='T12'),
        dcc.Tab(label='0.6\265m Wavelength', value='p65'),
        dcc.Tab(label='0.8\265m Wavelength', value='p86'),
    ]),

    html.Div(id = 'Satellite_Image_Holder', className = 'plot_holder', children = [

        html.Br(),
        html.Div(id = 'Satellite_Image', className = 'satellite_plot',
                ),
        html.Div(id = 'Sat_Img_Tools', className = 'plot_tools', children = [
            html.H3('Finding Fires'),
            html.H4('Step one: Remove Clouds'),
            Text_Providers.cloud_step_1(),
            daq.BooleanSwitch(
              id='cloud_1',
              label = 'Remove pixels below 265 K',
              on=False
            ),

            Text_Providers.cloud_step_2(),
            daq.BooleanSwitch(
              id='cloud_2',
              label = 'Remove 0.9 reflectance',
              on=False
            ),
            Text_Providers.cloud_step_3(),
            daq.BooleanSwitch(
              id='cloud_3',
              label = 'Remove warmer duller clouds',
              on=False
            ),
            html.H4('Step two: Check the land Temperature'),
            Text_Providers.land_mask_1(),
            daq.BooleanSwitch(
              id='land_1',
              label = 'Remove colder land',
              on=False
            ),
            Text_Providers.land_mask_2(),
            daq.BooleanSwitch(
              id='land_2',
              label = 'Remove non-burning pixel',
              on=False
            ),
            html.Hr(),
            html.Div(id = 'fire_button_container', children = [
        html.Button(children = [], id = 'reveal_fires',
            style = {'width':'200px',
                    'height':'50px',
                'borderRadius':'5px'})], style = {'textAlign':'center'}),
        ], style ={'paddingRight':'20px'}),
    ]),
    html.Hr(),
    html.H2(children  = ['The effect of resoluton'], style = {'textAlign':'center'}),
    html.Br(),
    html.H2(children  = ['Fire Count'], style = {'textAlign':'center'}),
    Text_Providers.Fire_Count(),
    html.Br(),
    html.Hr(),
    html.P(children = ['Any questions or issues? Email ', html.A('Doug Finch', href = 'mailto:d.finch@ed.ac.uk')]),
    ])])


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
