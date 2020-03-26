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
from dataplot.models import measurement_info
import numpy as np
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

        if kwargs['lineorscatter'] == 'Line':
            line_mode = 'lines'
        elif kwargs['lineorscatter'] == 'Line & Scatter':
            line_mode = 'lines+markers'
        else:
            line_mode = 'markers'

        x = resampled_df.index
        y = resampled_df
        all_plots.append(go.Scatter(
            x = x,
            y = y,
            mode = line_mode,
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

    # plot_layout = {'title':plot_title,
    #     'xaxis' : {'title':xtitle,
    #         # 'rangeslider':{},
    #         # 'type':'date'
    #         },
    #     'yaxis' : {'title':ytitle},
    #     'images':{
    #         'source':'https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png',
    #         'xref':'paper',
    #         'yref':'paper',
    #         'x':1,'y':1.05,
    #         'sizex':0.2,'sizey':0.2,
    #         'xanchor':'right','yanchor':'bottom'
    #     }
    #     }

    plot_layout = go.Layout(
    title = plot_title,
    xaxis = dict(title = xtitle),
    yaxis = dict(title = ytitle),
    images=[dict(
        source="assets/UoE_Geosciences_2_colour.jpg",
        xref="paper", yref="paper",
        x=.66, y=0.95,
        sizex=0.25, sizey=0.25,
        xanchor="right", yanchor="bottom"
      ),
      dict(
          source="assets/ukri-nerc-logo-600x160.png",
          xref="paper", yref="paper",
          x=0.88, y=0.95,
          sizex=0.2, sizey=0.2,
          xanchor="right", yanchor="bottom"
        ),
        dict(
            source="assets/DEFRA-logo.png",
            xref="paper", yref="paper",
            x=1, y=0.95,
            sizex=0.18, sizey=0.18,
            xanchor="right", yanchor="bottom"
          ),
        ],
    )

    plot = dcc.Graph(
        id='TimeSeriesPlot',
        figure={
            'data': all_plots,
            'layout': plot_layout
        }
    )
    return plot


def EO_Lessons_TimeSeries(indata, **kwargs):

    mean = indata.mean(axis = (1,2))
    std = indata.std(axis = (1,2))
    mini = indata.min(axis = (1,2))
    maxi = indata.max(axis = (1,2))

    all_plots = []

    if kwargs['linemode'] == 'Line':
        line_mode = 'lines'
    elif kwargs['linemode'] == 'Line & Scatter':
        line_mode = 'lines+markers'
    else:
        line_mode = 'markers'

    if 'Mean' in kwargs['stattype']:
        all_plots.append(
            go.Scatter(
            x = np.arange(len(mean))+1,
            y = mean,
            mode = line_mode,
            name = 'Mean'
            )
        )
    if 'Minimum' in kwargs['stattype']:
        all_plots.append(
            go.Scatter(
                x = np.arange(len(mean))+1,
                y = mini,
                mode = line_mode,
                name = 'Minimum'
            )
        )
    if 'Maximum' in kwargs['stattype']:
        all_plots.append(
            go.Scatter(
                x = np.arange(len(mean))+1,
                y = maxi,
                mode = line_mode,
                name = 'Maximum'
            )
        )

    plot_layout = {'title':kwargs['title'],
        'xaxis' : {'title':'Timestep'},
        'yaxis' : {'title':'Temperature \260C'},
        }

    plot = dcc.Graph(
    id = 'EOTimeseriesPlot',
    figure = {
        'data':all_plots,
        'layout':plot_layout
    }
    )

    return plot
## ============================================================================
## END OF PROGAM
## ============================================================================
