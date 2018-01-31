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
    Info about TimeSeries will go here
'''

# def TimeSeries(df,variable_options,site_choice,
#         combine_choice, DataResample, date_range, title, rollingMean):

def TimeSeries(df, **kwargs):
    # Keywords are:
        # variable_options
        # site_choice
        # combine_choice
        # DataResample
        # date_range
        # title
        # rollingMean

    colours = ColourPicker.GetQualitative()

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]

    all_plots = []

    for n,var in enumerate(variable_dictionary.keys()):
        df_col = variable_dictionary[var]

        resample_rate = kwargs['DataResample'][0]
        if resample_rate == 'R':
            resampled_df = df_col
        else:
            resampled_df = df_col.resample(resample_rate).apply('mean')

        # Apply time range
        date_range = kwargs['date_range']
        resampled_df = resampled_df[date_range[0]:date_range[1]]

        # Colour choice
        colour_choice = colours[n]

        x = resampled_df.index
        y = resampled_df
        all_plots.append(go.Scatter(
            x = x,
            y = y,
            mode = 'markers',
            # marker = {'size': 5,
            #     'color':colour_choice},
            name = var
        ))

        rollingMean = kwargs['rollingMean']
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

    xtitle = kwargs['xtitle']
    ytitle = kwargs['ytitle']
    plot_title = kwargs['title']

    plot_layout = {'title':plot_title,
        'xaxis' : {'title':xtitle},
        'yaxis' : {'title':ytitle},
        }

    plot = dcc.Graph(
        id='TimeSeriesPlot',
        figure={
            'data': all_plots,
            'layout': plot_layout
        }
    )
    return plot
## ============================================================================
## END OF PROGAM
## ============================================================================
