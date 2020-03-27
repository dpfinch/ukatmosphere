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
    Info about Annual cycle will go here
'''

def AnnualCycle(df,**kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]


    # Get a list of days
    month_nums = [x for x in range(12)]
    months = ['January', 'Febuary', 'March', 'April', 'May', 'June','July',
        'August', 'September', 'October', 'November', 'December']

    all_plots = []

    colours = ['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)',
        'rgb(255, 65, 54)', 'rgb(207, 114, 255)', 'rgb(127, 96, 0)']

    for var_num, var in enumerate(variable_dictionary.keys()):
        if var.split(' ')[0][:2] == 'PM':
            var_name = var.split(' ')[0]
        else:
            var_name = var
    # Create dictionary with each month as a key containing all monthly data
        monthly_dict = {}
        for n,mon in enumerate(months):
            monthly_dict[mon] = variable_dictionary[var].loc[variable_dictionary[var].index.month == (n + 1)]

        sample_type = kwargs['sample_type']
        if sample_type == 'Both':
            mean_data = []
            median_data = []

            for mon in months:
                mean_data.append(monthly_dict[mon].mean())
                median_data.append(monthly_dict[mon].median())

            all_plots.append( go.Scatter(
                y = mean_data,
                x = months,
                name = 'Mean ' + var_name,
                mode = 'lines',
                ))
            all_plots.append( go.Scatter(
                y = median_data,
                x = months,
                name = 'Median ' + var_name,
                mode = 'lines',
                line = {'dash' : 'dash'}
                ))

        else:
            plot_data = []
            for mon in months:
                if sample_type == 'Mean':
                    plot_data.append(monthly_dict[mon].mean())
                if sample_type == 'Median':
                    plot_data.append(monthly_dict[mon].median())

            all_plots.append( go.Scatter(
                y = plot_data,
                x = months,
                name = var_name,
                mode = 'lines',
                ))

        error_type = kwargs['errors']
        # Don't add error to just median
        if sample_type in ['Both', 'Mean']:
            error_bars = []
            y_upper = []
            y_lower = []

            if error_type == 'Std':
                for mon in months:

                    y_upper.append(monthly_dict[mon].mean() + monthly_dict[mon].std())
                    y_lower.append(monthly_dict[mon].mean() - monthly_dict[mon].std())
                    # Need to do some jiggery pokery to create a shaded area
                x = months + months[::-1]
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
                for mon in months:

                    y_upper.append(monthly_dict[mon].mean() + (1.96 * monthly_dict[mon].std() / (len(monthly_dict[mon]) ** 0.5)))
                    y_lower.append(monthly_dict[mon].mean() - (1.96 * monthly_dict[mon].std() / (len(monthly_dict[mon]) ** 0.5)))
                    # Need to do some jiggery pokery to create a shaded area
                x = months + months[::-1]
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
        title = plot_title,
        xaxis = dict(title = xtitle),
        yaxis = dict(title = ytitle),
        images=[dict(
            source="assets/all_logos.jpeg",
            xref="paper", yref="paper",
            x=1, y=1,
            sizex=0.42, sizey=0.42,
            xanchor="right", yanchor="bottom"
          ),
            ],
        )

    plot = dcc.Graph(
        id='AnuualCyclePlot',
        figure={
            'data': all_plots,
            'layout': layout
        }
    )
    return plot

## ============================================================================
## END OF PROGRAM
## ============================================================================
