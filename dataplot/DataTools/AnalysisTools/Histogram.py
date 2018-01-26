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
"""
    Histogram info here
"""
def Histogram(df, variable_options,site_choice, combine_choice,
    DataResample, date_range):

    if type(variable_options) == str:
        df_col = df[variable_options]
    else:
        df_col = df[variable_options[0]]
    resample_rate = DataResample[0]

    if resample_rate == 'R':
        resampled_df = df_col
    else:
        resampled_df = df_col.resample(resample_rate).apply('mean')

    resampled_df = resampled_df[date_range[0]:date_range[1]]
    y = resampled_df
    figure = dcc.Graph(
        id='HistogramPlot',
        figure={
            'data': [go.Histogram(
                x = y
            )],
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

## ============================================================================
## END OF PROGAM
## ============================================================================
