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

    colours = ['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)',
        'rgb(255, 65, 54)', 'rgb(207, 114, 255)', 'rgb(127, 96, 0)']

    for var_num, var in enumerate(variable_dictionary.keys()):

        # Create dictionary with each month as a key containing all monthly data
        daily_dict = {}
        for n,day in enumerate(day_names):
            daily_dict[day] = variable_dictionary[var].loc[variable_dictionary[var].index.dayofweek == (n)]

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
                y = daily_dict[day].values,
                name = days_of_week[x],
                marker = {'color':colours[var_num],
                    'size':5},
                boxmean = showmean
            ))

    ytitle = kwargs['ytitle']
    plot_title = kwargs['title']

    layout = go.Layout(
        title = plot_title,
        xaxis = dict(title = 'Day of the Week'),
        yaxis = dict(title = ytitle),
        showlegend = False,
        boxmode = 'group',
        boxgap = 0.1,
        boxgroupgap = 0,
        images=[dict(
            source="assets/all_logos.jpeg",
            xref="paper", yref="paper",
            x=1, y=1,
            sizex=0.42, sizey=0.42,
            xanchor="right", yanchor="bottom"
          ),
            ],
        )
    config = {"toImageButtonOptions": {"width": None, "height": None, "scale":2}}

    plot = dcc.Graph(
        id='WeeklyBoxplotsPlot',
        figure={
            'data': all_plots,
            'layout': layout
        },
        config = config
    )
    return plot
## ============================================================================
## END OF PROGAM
## ============================================================================
