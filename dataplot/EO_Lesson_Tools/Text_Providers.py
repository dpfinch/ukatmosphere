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
])
    return s


def Hist_Text():
    s = html.Div([
    html.P("""
    Below is a histogram of the different temperatures seen by the satellite at
    a this wavelength. How often a certain temperature occurs (known as the frequency)
    is plotted like a bar chart.
    """),
    html.P("""
    Can you spot the most common temperature?"""),
    html.P("""
    Is there only one peak or are there more? Can you tell which peak might be the
    temperature of the ocean and which might be the temperature of the land?
    """),

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
