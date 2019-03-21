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
from plotly import tools
#==============================================================================


'''
    Info about Weekly cycle will go here
'''

def WeeklyCycle(df,**kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]


    # Get a list of days
    day_names = [x for x in range(7)]
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']

    all_plots = []

    colours = ['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)',
        'rgb(255, 65, 54)', 'rgb(207, 114, 255)', 'rgb(127, 96, 0)']

    for var_num, var in enumerate(variable_dictionary.keys()):

    # Create dictionary with each month as a key containing all monthly data
        daily_dict = {}
        for n,day in enumerate(day_names):
            daily_dict[day] = variable_dictionary[var].loc[variable_dictionary[var].index.dayofweek == (n)]

        sample_type = kwargs['sample_type']
        if sample_type == 'Both':
            mean_data = []
            median_data = []

            for d in day_names:
                mean_data.append(daily_dict[d].mean())
                median_data.append(daily_dict[d].median())

            all_plots.append( go.Scatter(
                y = mean_data,
                x = days_of_week,
                name = 'Mean ' + var,
                mode = 'lines',
                ))
            all_plots.append( go.Scatter(
                y = median_data,
                x = days_of_week,
                name = 'Median ' + var,
                mode = 'lines',
                line = {'dash' : 'dash'}
                ))

        else:
            plot_data = []
            for d in day_names:
                if sample_type == 'Mean':
                    plot_data.append(daily_dict[d].mean())
                if sample_type == 'Median':
                    plot_data.append(daily_dict[d].median())

            all_plots.append( go.Scatter(
                y = plot_data,
                x = days_of_week,
                name = var,
                mode = 'lines',
                ))

        error_type = kwargs['errors']
        # Don't add error to just median
        if sample_type in ['Both', 'Mean']:
            error_bars = []
            y_upper = []
            y_lower = []

            if error_type == 'Std':
                for d in day_names:

                    y_upper.append(daily_dict[d].mean() + daily_dict[d].std())
                    y_lower.append(daily_dict[d].mean() - daily_dict[d].std())
                    # Need to do some jiggery pokery to create a shaded area
                x = days_of_week + days_of_week[::-1]
                y = y_upper + y_lower[::-1]
                all_plots.append( go.Scatter(
                    y = y,
                    x = x,
                    fill = 'tozerox',
                    line = {'color':'rgba(0,100,80,0.2)'},
                    fillcolor='rgba(0,100,80,0.2)',
                    name = var,
                    showlegend = False,
                    ))
            elif error_type == '95% Confidence':
                for d in day_names:

                    y_upper.append(daily_dict[d].mean() + (1.96 * daily_dict[d].std() / (len(daily_dict[d]) ** 0.5)))
                    y_lower.append(daily_dict[d].mean() - (1.96 * daily_dict[d].std() / (len(daily_dict[d]) ** 0.5)))
                    # Need to do some jiggery pokery to create a shaded area
                x = days_of_week + days_of_week[::-1]
                y = y_upper + y_lower[::-1]

                all_plots.append( go.Scatter(
                    y = y,
                    x = x,
                    fill = 'tozerox',
                    line = {'color':'rgba(0,100,80,0.2)'},
                    fillcolor='rgba(0,100,80,0.2)',
                    name = var,
                    showlegend = False,
                    ))

    ytitle = kwargs['ytitle']
    xtitle = kwargs['xtitle']
    plot_title = kwargs['title']

    layout = go.Layout(
        xaxis = dict( title = xtitle),
        yaxis = dict( title = ytitle),
        title = plot_title,
        )

    plot = dcc.Graph(
        id='WeeklyCyclePlot',
        figure={
            'data': all_plots,
            'layout': layout
        }
    )
    return plot

## ============================================================================
## END OF PROGRAM
## ============================================================================
