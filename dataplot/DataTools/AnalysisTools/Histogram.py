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
import pandas as pd
import numpy as np
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

def EO_Lesson_Hist(inarray, **kwargs):

    all_plots = []

    vals = inarray.flatten()

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
        'xaxis': {'title': 'Temperature \260K'},
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

def Satellite_Hist(value, masks):
    import os
    cwd = os.getcwd()
    data_dirc = cwd + '/dataplot/static/{}_wavelenght.csv'

    brightness = pd.read_csv(data_dirc.format(value),
        header = None)

    if masks['cloud_1']:
        t12 = pd.read_csv(data_dirc.format('T12'), header = None)[0]
        brightness[t12 < 265] = np.nan

    if masks['cloud_2']:
        p65 = pd.read_csv(data_dirc.format('p65'), header = None)[0]
        p86 = pd.read_csv(data_dirc.format('p86'), header = None)[0]

        brightness[p65 + p86 > 0.9] = np.nan

    if masks['cloud_3']:
        p65 = pd.read_csv(data_dirc.format('p65'), header = None)[0]
        p86 = pd.read_csv(data_dirc.format('p86'), header = None)[0]
        t12 = pd.read_csv(data_dirc.format('T12'), header = None)[0]

        brightness[(p65+p86 >0.7) & (t12<300)] = np.nan

    if masks['land_1']:
        t4 = pd.read_csv(data_dirc.format('T4'), header = None)[0]

        brightness[t4<310] = np.nan


    if masks['land_2']:
        t4 = pd.read_csv(data_dirc.format('T4'), header = None)[0]
        t11 = pd.read_csv(data_dirc.format('T11'), header = None)[0]

        brightness[t4 - t11 < 10] = np.nan


    plot = [go.Histogram(
    x = brightness.values.flatten()
    )]

    plot_layout = {
        'bargap': 0.2,
        'bargroupgap': 0.1,
        'yaxis': {'title': 'Frequency'},
        'xaxis': {'title': 'Temperature \260C'},
        'title' : 'Brightness Temperature Frequency'
        }

    figure = dcc.Graph(
        id='SatHistogramPlot',
        figure={
            'data': plot,
            'layout': plot_layout
        }
        )

    return figure
## ============================================================================
## END OF PROGRAM
## ============================================================================
