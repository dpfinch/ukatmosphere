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

def TimeSeries(df, variables, combined = False):
    """
        Create x and y axes for a simple time series plot. With possble errors
        Function IN:
            df (REQUIRED, PD.DATAFRAME):
                A pandas dataframe containing the data to be processed
            errors (OPTIONAL, BOOLEAN):
                Whether there are errors to be processed and included in the plots
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
            plot_list.append(go.Scatter(
                x = df[vars_dictionary[k]].index,
                y = df[vars_dictionary[k]],
                mode = 'markers')
                )

    else:

        plot_list = [go.Scatter(
            x = df[variables].index,
            y = df[variables],
            mode = 'markers'
            )]

    figure = [
        # html.Div([dcc.RadioItems(
        # id='resampling',
        # options=[{'label': i, 'value': i} for i in ['Daily', 'Weekly','Monthly']],
        # value='Daily',
        # labelStyle={'display': 'inline-block'}
        # )]),
        dcc.Graph(
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
    )]



    return figure

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield' \
                    + 'GAUGE-CRDS_HFD_20130101_ch4-100m.nc'
    TimeSeries(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
