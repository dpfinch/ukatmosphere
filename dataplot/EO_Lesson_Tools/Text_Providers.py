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
    is plotted like a bar chart. This will be updated as the map is updated.
    """),
    html.P("""
    Can you determine what the most common temperature is?"""),
    html.P("""
    Is there only one peak or are there more? Can you tell which peak might be the
    temperature of the ocean and which might be the temperature of the land?
    """),

    ], className = 'text_holder')
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

def Spotting_Fires_Text():
    s = html.Div([
    html.P("""
        Using satellites like Sentinel-2 means we can spot fires from space.
        Below is a scan taken by the Sentinel-2 satellite on the 1st of November
        2017 over the east of Australia. November is the beginning of summer for the southern hemisphere and
        sees a lot of fires in regions without much rainfall. This is real data
        but has been transfored to a lower resolution to make it easier to analyse.
    """),
    html.P("""
        By following the steps below, we can go from a satellite scan to a count of
        how many pixels are on fire. This is a simple process of using the 'brightness temperature'
        data as well the reflectivitiy data from the satellite.
        """)
    ], className = 'text_holder')
    return s

def Sentinel_Text():
    s = html.Div([
    html.P("""
        The satellite data comes in a value of 'Brightness Temperature'. This is
        similar but not quite the same surface temperature. The brightness temperature
        can be defined as what the temperature would be of a black body that was emitting
        the same amount of radiation as a 'target body' (in our case - the surface of
        the Earth) at a specific wavelength.
    """),
    html.A(href = 'https://www.sciencedirect.com/topics/earth-and-planetary-sciences/brightness-temperature',
        children = [html.P('More information on black bodies can be found here.')]),
    html.P("""
        We can use this to highlight different things in our satellite scan. If different
        surfaces (land, ocean, clouds, tarmac, grass, etc) have a different brightness temperature
        at different wavelengths we can start to mathmatically pick out features
    """),
    html.P('Look at the different wavelengths - what do they highlight?'),
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

def cloud_step_1():
    s = html.Div([ html.P("""
        The first step is to remove the clouds from image. To do this there
        are three rules we have to follow.
    """),
    html.P("""
        Rule 1: Clouds are cold - any area in the image below 265 K at the 12\265m wavelength
        is going to be a cloud (or ice which won't be on fire!).
    """),
    ])
    return s

def cloud_step_2():
    s = html.Div([ html.P("""
        Rule 2: Clouds are white and therefore reflective. Pixels in the image
         that are above 0.9 (90%) relectance when the 0.6\265m and 0.8\265m wavelengths
         are added together is going to be a cloud.
    """),
    ])
    return s

def cloud_step_3():
    s = html.Div([ html.P("""
        Rule 3: Some clouds are greyer and warmer than others. But they will still
        be cooler than 300 K and have a reflectance higher than 0.7 (70%). We can
        remove pixels that meet both of these characteristics.
    """),
    ])
    return s

def land_mask_1():
        s = html.Div([ html.P("""
            There are two more steps to find where is on fire.
        """),
        html.P("""
        As we know fires are hot, we can remove anything the satellite sees that is
        going to be too cool to be on fire. We can remove anything below 310 K on
        the 4\265m wavelength.
        """),
        ])
        return s


def land_mask_2():
    s = html.Div([ html.P("""
        Finally, we can use a special property of the wavelengths of light emitted
        by fire. If a pixel is on fire, the 4\265m and 11\265m wavelengths will
        show a very similar temperature. The difference between the two wavelengths
        must be within 10 K for it to be fire, otherwise it'll just hot land.
    """),
    ])
    return s

def Fire_Count():
    s = html.Div([ html.P("""
        This analysis revealed that there are 105 pixels in this image that are
        on fire when the Sentinel satellite took this scan.
    """),
    html.P("""
        That may seem like a lot of fires for one day but this is a big
        under-estimate. The image above is very low resolution. A higer resolution
        image will show even more fires. Read below about how many fires the full
        resolution image can pick up.
    """)
    ])
    return s

def Resolution():
    s = html.Div(className = 'text_holder', children = [ html.P("""
        The satellite image aboves has 308 x 320 pixels, thats a total of
        93,016 pixels it has to process. That may seem like a lot but this is
        lower resolution version of the orignal image. The original scan from the
        satellite had 3072 x 3200 pixels - a total of over 9.8 million pixels. Which is
        100 times more than this image. The more pixels in a scan the higher
        the resolution and therefore the more detail you can see. The problem with
        this is oridinary computers start to struggle to compute all of this. This
        website can only process so much data before it crashes meaning for this
        example we're using a lower resolution scan.
    """),
    html.P("""
        As a higher resolution scan would show more detail, we could see more smaller
        fires that the lower resolution wouldn't pick up. If we did the same processing
        as above but for the highest resolution there would be over 10,000 pixels
        highlighted as on fire. Thats over 100x as many as we found!
    """),
    html.P("""
        It is important to remeber that this might not mean 10,000 individual fires.
        Some of these pixels may be next to each other and are scanning huge fires that
        cover a large area. If two or more pixels next to each other are both showing
        the characteristics of fire - they its likely they are one bigger fire.
    """),
    ])
    return s


def More_Fire_Count_Info():
    s = html.Div(className = 'text_holder', children = [
    html.P("""
        This is one snapshot taken on the 1st of November 2017. This satellite can
        revisit a location over and over again for weeks,months and years and each
        time it makes a scan it can count the number of fires over a period of time.
        By doing this we can see if there are more or less fires year to year, or
        where is particularly prone to fires.
    """),
    html.P("""
        To find out how large a fire is - or the area of land that has been burnt
         we simply
        need to know how much land is covered by one pixel then multiply that by
        the number of pixels on fire.
    """),
    html.P([
        'For example - if each pixel covers 1 km x 1 km of the Earth surface and',
        'we counted 105 fires in our scan then the burned area in this image is',
        '105 km squared.']
    ),
    ])
    return s

def More_Analysis_text():
    s = html.Div(children = [
    html.P("""
        Satellites are incredible tools to have at our disposal to observe the
        natural world. We've looked at fires here but satellites look at a huge
        range of things such as forests, oceans, population spread, snow cover,
        air pollution - the list goes on and on!
    """),
    html.P("""
        If you'd like to explore more satellite data or thermal data then below
        are some links to follow that can be the next steps.
    """),
    ])
    return s

def jupyter_text():
    s = html.Div(children = [
    html.Img(id = 'jupyter_logo', src='https://jupyter.org/assets/nav_logo.svg',
    ),
    html.Br(),
    html.P("""
        A great way to learn how to process data like the data shown here using
        computer code is the Jupter Notbooks.
    """),
    html.P("""
        Using these requires some knowledge of coding but not a lot - its a great
        learning tool and really useful for showing your working in code as well
        as sharing.
    """),
    html.A(href ='https://jupyter.org/', children = [html.P('Information about Jupyter can be found here.')]),
    html.P("If you'd like to download a Jupyter Notebook to process some data similar to whats shown on this website, click below."),
    html.A(href ='https://drive.google.com/file/d/10M1wbs_mgxrjWF4Yc56bEYfAejQ2ay3Z/view', children = [html.P('Jupyter Notebook')]),
    ])
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
