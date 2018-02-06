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

def WeeklyBoxplots(df,**kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]

    # Get a list of hours
    day_names = [x for x in range(7)]

    all_plots = []

    for var in variable_dictionary.keys():

        # Create dictionary with each month as a key containing all monthly data
        dayly_dict = {}
        for n,day in enumerate(day_names):
            dayly_dict[day] = variable_dictionary[var].loc[variable_dictionary[var].index.dayofweek == (n)]

        # Create list to put in the plot.ly traces and combine them
        # to send to plot.ly
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']

        if kwargs['showmean']:# == True:
            showmean = True
        else:
            showmean = False

        for x, day in enumerate(day_names):
            all_plots.append( go.Box(
                y = dayly_dict[day].values,
                name = days_of_week[x],
                marker = {'color':'rgb(8, 81, 156)'},
                boxmean = showmean
            ))

    ytitle = kwargs['ytitle']
    plot_title = kwargs['title']

    layout = go.Layout(
        yaxis = dict( title = ytitle),
        xaxis = dict( title = 'Day of the Week'),
        showlegend = False,
        title = plot_title,
        boxmode = 'group'
        )

    plot = dcc.Graph(
        id='WeeklyBoxplotsPlot',
        figure={
            'data': all_plots,
            'layout': layout
        }
    )
    return plot
## ============================================================================
## END OF PROGAM
## ============================================================================
