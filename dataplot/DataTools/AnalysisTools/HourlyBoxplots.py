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
    Info about Boxplots will go here
'''

def HourlyBoxplots(df,**kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]


    # Get a list of hours
    hour_names = [x for x in range(24)]

    all_plots = []

    colours = ['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)',
        'rgb(255, 65, 54)', 'rgb(207, 114, 255)', 'rgb(127, 96, 0)']

    for var_num, var in enumerate(variable_dictionary.keys()):

    # Create dictionary with each month as a key containing all monthly data
        hourly_dict = {}
        for n,hour in enumerate(hour_names):
            hourly_dict[hour] = variable_dictionary[var].loc[variable_dictionary[var].index.hour == (n)]

        # Create list to put in the plot.ly traces and combine them
        # to send to plot.ly

        if kwargs['showmean']:# == True:
            showmean = True
        else:
            showmean = False

        for x, hour in enumerate(hour_names):
            all_plots.append( go.Box(
                y = hourly_dict[hour].values,
                name = str(hour).zfill(2)+':00',
                marker = {'color':colours[var_num]},
                boxmean = showmean))

    ytitle = kwargs['ytitle']
    plot_title = kwargs['title']

    layout = go.Layout(
        title = plot_title,
        xaxis = dict(title = 'Hour of the Day'),
        yaxis = dict(title = ytitle),
        showlegend = False,
        boxmode = 'group',
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
        id='HourlyBoxplotsPlot',
        figure={
            'data': all_plots,
            'layout': layout
        }
    )
    return plot
## ============================================================================
## END OF PROGRAM
## ============================================================================
