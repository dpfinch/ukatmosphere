#==============================================================================
# Description of module here
#
#==============================================================================
# Uses modules:
# modulename
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dataplot.DataTools import ColourPicker
#==============================================================================


'''
    Info about DateDayHeatmap will go here
'''
def DateDayHeatmap(df, **kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    # Will only be able to handle on variable
    if type(variable_options) == str:
        var = df[variable_options]
    else:
        if len(variable_options == 0):
            return ''
        var = df[variable_options[0]]

    date_range = kwargs['date_range']

    # var = var[date_range[0]:date_range[1]]

    hours_in_day = [x for x in range(24)]
    z_dim = []

    for h in hours_in_day:
        z_dim.append(list(var.loc[var.index.hour == h]))


    plot = [go.Heatmap(
        z = z_dim,
        x = var.index,
        y = hours_in_day,
        colorscale = 'Viridis',
    )]

    xtitle = 'Date'
    ytitle = 'Hour of the Day'
    plot_title = kwargs['title']

    plot_layout = {'title':plot_title,
        'xaxis' : {'title':xtitle},
        'yaxis' : {'title':ytitle},
        }

    figure = dcc.Graph(
        id='DateDayHeatmapPlot',
        figure={
            'data': plot,
            'layout': plot_layout
    })

    return figure
## ============================================================================
## END OF PROGAM
## ============================================================================
