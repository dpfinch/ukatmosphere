import dash_html_components as html
import dash_core_components as dcc


def Sentinenl_Info():
    s = html.Div([
    html.P("""
    Sentinel-2 is an Earth observation mission from the EU Copernicus Programme
    that systematically acquires optical imagery over land and coastal waters.
    """),
    html.P("""
    The satellite as lauched by the European Space Agency in 2015 and orbits the
    Earth 14.3 times per day at an altitude of 768 km.
    """),
    html.P("""
    Multispectral imager (MSI) covering 13 spectral bands (443 nm–2190 nm) with
     a swath width of 290 km and spatial resolutions of 10 m (4 visible and
      near-infrared bands), 20 m (6 red-edge/shortwave-infrared bands) and 60 m
       (3 atmospheric correction bands).
    """
    ),
    html.P(""" These spectral bands can be used for a number of applications
    including monitoring agriculture, forests, land-use change, land-cover
    change; mapping
    biophysical variables such as leaf chlorophyll content, leaf water content,
    leaf area index; monitoring coastal and inland waters; risk mapping and
    disaster mapping
    """
    ),
    html.P(""" Below we can use some of the data gathered from the different
    wavelengths to detect fires from space.
    """
    ),
    html.P(""" More infomation about the Sentinel-2 satellite and the more
    satellite in the Sentinel mission can be found here:
    """
    ), html.A('Sentinel-2 Website', href='https://www.esa.int/Our_Activities/Observing_the_Earth/Copernicus/Sentinel-2', target="_blank")
], className = 'text_holder')
    return s


def Hist_Text():
    s = html.Div([
    html.P("""
    Below is a histogram of the different temperatures seen by the satellite at
    a this wavelength. How often a certain temperature occurs (known as the frequency)
    is plotted like a bar chart.
    """),
    html.P("""
    Can you determine what the most common temperature is?"""),
    html.P("""
    Is there only one peak or are there more? Can you tell which peak might be the
    temperature of the ocean and which might be the temperature of the land?
    """),

    ], className = 'text_holder')
    return s

def Fire_Count():
    s = html.Div([
    html.P("""
        Information about fire count over time goes here.
    """)
    ])
    return s

def TIR_Info():
    s = html.Div([
    html.P("""
        Below are some tools to help process data from the Raspberry Pi Thermal
        Sensor. If you've got your own data recorded from a Rapberry Pi sensor
        then find the file and drag it into the box below.
    """),
    html.P("""
        If you've not got a your own file then you can use some sample data we've
        got. You can pick the number of time steps you want to analyise (up to 350).
    """)
    ], className = 'text_holder')
    return s

def ContourInfo():
    s = html.Div([
    html.P("""
        A contour plot colours all the same values the same colour. This is useful
        if we want to see patterns in the data. """),
    html.P("""
        It creates an plot that is similar
        to a photograph - but coloured by temperature instead of light.
    """)
    ], className = 'text_holder')
    return s

def AfterContour():
    s = html.Div([
    html.H4('What features can you see in the contour plot?'),
    html.P("""
        The contour plot is slightly blured (this is only a small sensor after all),
        but can you determine any shapes in the data?
        """),

    html.H4('What is the maximum and minimum temperature?'),
    html.P("""
        What is the range of temperatures seen in the plot?
        """),
    ], className = 'text_holder')
    return s

def HistInfo():
    s = html.Div([
    html.P("""
        This histogram shows how often a particular temperature occurs - known
        as the frequency. The data is gathered into 'bins' (or groups) of
        temperatures.
    """)
    ], className = 'text_holder')
    return s

def TimeseriesInfo():
    s = html.Div([
    html.P("""
        If there is more than one time step in the data then a timeseries can
        show how the data changes over time. This time series plot takes the
        mean, minimum or maximum temperature for each timestep and plots it one
        after another. We can use this to see if the temperature is changing
        over time.
    """)
    ], className = 'text_holder')
    return s


def test_string2():
    s = html.Div([
    html.P("""
    Yet bed any for travelling assistance indulgence unpleasing.
     Not thoughts all exercise blessing. Indulgence way everything
     joy alteration boisterous the attachment. Party we years to order
     allow asked of. We so opinion friends me message as delight. Whole
     front do of plate heard oh ought. His defective nor convinced
     residence own. Connection has put impossible own apartments boisterous.
     At jointure ladyship an insisted so humanity he. Friendly bachelor
     entrance to on by."""),
     html.P("""
         Are own design entire former get should. Advantages boisterous day
    excellence boy. Out between our two waiting wishing. Pursuit he he
    garrets greater towards amiable so placing. Nothing off how norland
     delight. Abode shy shade she hours forth its use. Up whole of fancy ye quiet do.
     Justice fortune no to is if winding morning forming.
    Rooms oh fully taken by worse do. Points afraid but may end law lasted.
    Was out laughter raptures returned outweigh. Luckily cheered colonel me
      entrance to on by
        """)])

    return s
