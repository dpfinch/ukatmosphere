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

def WeeklyBoxplots(df,variable_options,site_choice,
        combine_choice, DataResample, date_range):

    if type(variable_options) == str:
        df_col = df[variable_options]
    else:
        df_col = df[variable_options[0]]

    # Get a list of hours
    day_names = [x for x in range(7)]

    # Create dictionary with each month as a key containing all monthly data
    dayly_dict = {}
    for n,day in enumerate(day_names):
        dayly_dict[day] = df_col.loc[df_col.index.dayofweek == (n)]

    # Create list to put in the plot.ly traces and combine them
    # to send to plot.ly
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday']
    box_data = []
    for x, day in enumerate(day_names):
        box_data.append( go.Box(
            y = dayly_dict[day].values,
            name = days_of_week[x]
        ))

    layout = go.Layout(
        yaxis = dict( title = variable_options[0]),
        xaxis = dict( title = 'Day of the Week'),
        showlegend = False,
        title = 'Weekly Stats for '+ variable_options[0]
        )

    plot = dcc.Graph(
        id='WeeklyBoxplotsPlot',
        figure={
            'data': box_data,
            'layout': layout
        }
    )
    return plot
## ============================================================================
## END OF PROGAM
## ============================================================================
