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


'''
    Info about TimeSeries will go here
'''

def TimeSeries(df,variable_options,site_choice,
        combine_choice, DataResample, date_range, rollingMean):

    if type(variable_options) == str:
        df_col = df[variable_options]
    else:
        df_col = df[variable_options[0]]
    resample_rate = DataResample[0]

    if resample_rate == 'R':
        resampled_df = df_col
    else:
        resampled_df = df_col.resample(resample_rate).apply('mean')

    # Apply time range
    resampled_df = resampled_df[date_range[0]:date_range[1]]

    x = resampled_df.index
    y = resampled_df
    all_plots = [go.Scatter(
        x = x,
        y = y,
        mode = 'markers'
    )]

    if rollingMean:
        if rollingMean == '8-Hourly Rolling Mean':
            roll_num = 8
        else:
            # This works out because every other option the data is resampled to
            # the value anyway (ie daily sampled)
            roll_num = 1
        rolling = resampled_df.rolling(roll_num, min_periods = int(roll_num*0.75))

        rollingMean = None

        all_plots.append(go.Scatter(
            y = rolling.mean(),
            x = rolling.mean().index
            ))
    plot = dcc.Graph(
        id='TimeSeriesPlot',
        figure={
            'data': all_plots,
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
    return plot
## ============================================================================
## END OF PROGAM
## ============================================================================
