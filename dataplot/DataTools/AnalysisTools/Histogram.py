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
def Histogram(df, **kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']
    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]


    all_plots = []

    for var in variable_dictionary.keys():
        df_column = variable_dictionary[var]

        resample_rate = kwargs['DataResample'][0]
        if resample_rate == 'R':
            resampled_df = df_column
        else:
            resampled_df = df_column.resample(resample_rate).apply('mean')

        # Apply time range
        date_range = kwargs['date_range']
        resampled_df = resampled_df[date_range[0]:date_range[1]]

        try:
            num_bins = int(kwargs['histbins'])
        except ValueError:
            num_bins = 20 ## Maybe need to set this to None or something?

        bin_start = resampled_df.min()
        bin_end = resampled_df.max()
        bin_size = (resampled_df.max() -resampled_df.min()) / num_bins
        bin_size = 5
        x = resampled_df

        if kwargs['probability'] == ['Probability']:

            all_plots.append(go.Histogram(
                x = x,
                histnorm = 'probability',
                nbinsx = num_bins,
                name = var
            ))
            yaxisTitle = 'Probability'
        else:
            all_plots.append(go.Histogram(
                x = x,
                # xbins = {'start': bin_start,
                #         'end': bin_end,
                #         'size': bin_size},
                nbinsx = num_bins,
                name = var
                ))

            yaxisTitle = 'Frequency'

    plot_layout = {
        'bargap': 0.2,
        'bargroupgap': 0.1,
        'yaxis': {'title': yaxisTitle},
        'xaxis': {'title': kwargs['xtitle']},
        'title': kwargs['title'],
        }

    figure = dcc.Graph(
        id='HistogramPlot',
        figure={
            'data': all_plots,
            'layout': plot_layout
        }
    )


    return figure

def EO_Lesson_Hist(df, **kwargs):

    all_plots = []

    vals = df.values.flatten()

    try:
        num_bins = int(kwargs['histbins'])
    except ValueError:
        num_bins = 20 ## Maybe need to set this to None or something?

    bin_start = vals.min()
    bin_end = vals.max()
    bin_size = (vals.max() -vals.min()) / num_bins
    bin_size = 5
    x = vals

    if kwargs['probability'] == ['Probability']:

        all_plots.append(go.Histogram(
            x = x,
            histnorm = 'probability',
            nbinsx = num_bins,
        ))
        yaxisTitle = 'Probability'
    else:
        all_plots.append(go.Histogram(
            x = x,
            # xbins = {'start': bin_start,
            #         'end': bin_end,
            #         'size': bin_size},
            nbinsx = num_bins,
            ))

        yaxisTitle = 'Frequency'

    plot_layout = {
        'bargap': 0.2,
        'bargroupgap': 0.1,
        'yaxis': {'title': yaxisTitle},
        'xaxis': {'title': 'Temperature'},
        'title': kwargs['title'],
        }

    figure = dcc.Graph(
        id='HistogramPlot',
        figure={
            'data': all_plots,
            'layout': plot_layout
        }
        )


    return figure
## ============================================================================
## END OF PROGRAM
## ============================================================================
