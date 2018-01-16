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

def Histogram(df, variables, combined = False):
    """
        Description of function here
        Function IN:
            argin (REQUIRED, DTYPE):
                Description of the argument in, wheter its REQUIRED, OPTIONAL,
                and what is DEFAULT
        Fucntion OUT:
            argout:
                Description of what the fuction returns if any
    """

    vars_dictionary = {}
    if combined:
        for n, var in enumerate(variables):
            vars_dictionary['var_'+str(n+1)] = var

        plot_list = []

        for k in vars_dictionary.keys():
            plot_list.append(go.Histogram(
                x = df[vars_dictionary[k]])
                )

    else:

        plot_list = [go.Histogram(
            x = df[variables]
            )]

    figure = dcc.Graph(
        id='main-graph',
        figure={
            'data': plot_list,
            'layout': {
                'autosize': True,
                'scene': {
                    'bgcolor': 'rgb(255, 255, 255)',
                    'xaxis': {
                        'titlefont': {'color': 'rgb(0, 0, 0)'},
                        'title': 'X-AXIS',
                        'color': 'rgb(0, 0, 0)'
                    },
                    'yaxis': {
                        'titlefont': {'color': 'rgb(0, 0, 0)'},
                        'title': 'Y-AXIS',
                        'color': 'rgb(0, 0, 0)'
                    }
                }
            }
        }
    )



    return figure

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # paramters
    filename  = 'RawData/Heathfield' \
                    + 'GAUGE-CRDS_HFD_20130101_ch4-100m.nc'
    Histogram(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
