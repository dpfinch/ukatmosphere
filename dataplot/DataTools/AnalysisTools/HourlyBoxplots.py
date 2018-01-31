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

    for var in variable_dictionary.keys():

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
                marker = {'color':'rgb(8, 81, 156)'},
                boxmean = showmean))

    ytitle = kwargs['ytitle']
    plot_title = kwargs['title']

    layout = go.Layout(
        yaxis = dict( title = ytitle),
        xaxis = dict( title = 'Hour of the Day'),
        showlegend = False,
        title = plot_title,
        boxmode='group'
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
