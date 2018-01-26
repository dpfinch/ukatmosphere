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

def HourlyBoxplots(df,variable_options,site_choice,
        combine_choice, DataResample, date_range):

    if type(variable_options) == str:
        df_col = df[variable_options]
    else:
        df_col = df[variable_options[0]]

    # Get a list of hours
    hour_names = [x for x in range(24)]

    # Create dictionary with each month as a key containing all monthly data
    hourly_dict = {}
    for n,hour in enumerate(hour_names):
        hourly_dict[hour] = df_col.loc[df_col.index.hour == (n)]

    # Create list to put in the plot.ly traces and combine them
    # to send to plot.ly
    box_data = []
    for x, hour in enumerate(hour_names):
        box_data.append( go.Box(
            y = hourly_dict[hour].values,
            name = str(hour).zfill(2)))

    layout = go.Layout(
        yaxis = dict( title = variable_options[0]),
        xaxis = dict( title = 'Hour of the Day'),
        showlegend = False,
        title = 'Hourly Stats for '+ variable_options[0]
        )

    plot = dcc.Graph(
        id='HourlyBoxplotsPlot',
        figure={
            'data': box_data,
            'layout': layout
        }
    )
    return plot
## ============================================================================
## END OF PROGAM
## ============================================================================
