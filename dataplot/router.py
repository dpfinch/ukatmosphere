from dash.dependencies import Output, Input
from .server import app#, server
from . import layouts_defra_sites, layouts_defra_map, layouts_data_upload
from . import layouts_EO_lessons, layouts_site_compare, layouts_uk_o3



pages = (
    ('DEFRA_sites', layouts_defra_sites.DEFRA_individual_sites),
    ('DEFRA_map', layouts_defra_map.DEFRA_map_page),
    ('Data_Upload', layouts_data_upload.data_upload_page),
    ('UK_Ozone', layouts_uk_o3.uk_ozone),
    ('EO_Lessons', layouts_EO_lessons.EO_Lessons),
    ('EO_lessons',layouts_EO_lessons.EO_Lessons),
    ('Site_Comparison', layouts_site_compare.Site_Comparison_Table),
    )

routes = {f"{app.url_base_pathname}{path}": layout for path, layout in pages}

@app.callback(Output('content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    ''' '''

    if pathname is None:
        return ''

    page = routes.get(pathname, 'Unknown link')

    if callable(page):
        # can add arguments to layout functions if needed etc
        layout = page()
    else:
        layout = page

    return layout
