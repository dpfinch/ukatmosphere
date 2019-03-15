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
#==============================================================================

def EO_Lesson_Contour(inarray,**kwargs):

    timestep = kwargs['timestep']

    data = [go.Contour(
    z = inarray[timestep - 1],
    line = {'smoothing':1},
    contours = {'coloring':'fill', 'showlines':False},
    colorbar = {'title':'Temperature \260C', 'titleside':'right'}
    )]

    plot_layout = {
    'title':kwargs['title'],
    'width' : 600,
    'height': 600
    }

    figure = dcc.Graph(
    id = 'ContourPlot',
    figure = {
        'data':data,
        'layout':plot_layout
        }
        )

    return figure
