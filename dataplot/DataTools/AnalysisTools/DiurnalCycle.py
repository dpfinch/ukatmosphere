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
from plotly.subplots import make_subplots
#==============================================================================


'''
    Info about Dirunal cycle will go here
'''

def DiurnalCycle(df,**kwargs):

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
        if var.split(' ')[0][:2] == 'PM':
            var_name = var.split(' ')[0]
        else:
            var_name = var
    # Create dictionary with each month as a key containing all monthly data
        hourly_dict = {}
        for n,hour in enumerate(hour_names):
            hourly_dict[hour] = variable_dictionary[var].loc[variable_dictionary[var].index.hour == (n)]

        sample_type = kwargs['sample_type']
        if sample_type == 'Both':
            mean_data = []
            median_data = []

            for h in hour_names:
                mean_data.append(hourly_dict[h].mean())
                median_data.append(hourly_dict[h].median())

            all_plots.append( go.Scatter(
                y = mean_data,
                x = hour_names,
                name = 'Mean ' + var_name,
                mode = 'lines',
                ))
            all_plots.append( go.Scatter(
                y = median_data,
                x = hour_names,
                name = 'Median ' + var_name,
                mode = 'lines',
                line = {'dash' : 'dash'}
                ))

        else:
            plot_data = []
            for h in hour_names:
                if sample_type == 'Mean':
                    plot_data.append(hourly_dict[h].mean())
                if sample_type == 'Median':
                    plot_data.append(hourly_dict[h].median())

            all_plots.append( go.Scatter(
                y = plot_data,
                x = hour_names,
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
                for h in hour_names:

                    y_upper.append(hourly_dict[h].mean() + hourly_dict[h].std())
                    y_lower.append(hourly_dict[h].mean() - hourly_dict[h].std())
                    # Need to do some jiggery pokery to create a shaded area

                x = hour_names + hour_names[::-1]
                y = y_upper + y_lower[::-1]

                all_plots.append( go.Scatter(
                    y = y,
                    x = x,
                    fill = 'tozerox',
                    line = {'color':'rgba(0,100,80,0.2)'},
                    fillcolor='rgba(0,100,80,0.2)',
                    name = var_name,
                    showlegend = False,
                    ))
            elif error_type == '95% Confidence':
                for h in hour_names:

                    y_upper.append(hourly_dict[h].mean() + (1.96 * hourly_dict[h].std() / (len(hourly_dict[h]) ** 0.5)))
                    y_lower.append(hourly_dict[h].mean() - (1.96 * hourly_dict[h].std() / (len(hourly_dict[h]) ** 0.5)))
                    # Need to do some jiggery pokery to create a shaded area
                x = hour_names + hour_names[::-1]
                y = y_upper + y_lower[::-1]

                all_plots.append( go.Scatter(
                    y = y,
                    x = x,
                    fill = 'tozerox',
                    line = {'color':'rgba(0,100,80,0.2)'},
                    fillcolor='rgba(0,100,80,0.2)',
                    name = var_name,
                    showlegend = False,
                    ))

    ytitle = kwargs['ytitle']
    xtitle = kwargs['xtitle']
    plot_title = kwargs['title']

    layout = go.Layout(
        title = plot_title,
        xaxis = dict(title = xtitle, tickmode = 'array',tickvals=[0,3,6,9,12,15,18,21,24]),
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
    config = {"toImageButtonOptions": {"width": None, "height": None, "scale":2}}

    plot = dcc.Graph(
        id='DiurnalCyclePlot',
        figure={
            'data': all_plots,
            'layout': layout
        },
        config = config
    )
    return plot


def DiurnalCycleSplit(df, **kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']
    xtitle = kwargs['xtitle']
    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]

    # Get a list of hours
    hour_names = [x for x in range(24)]

    days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday')

    fig = make_subplots(rows = 1, cols = 7, shared_yaxes=True)
        # subplot_titles = days_of_week)

    for var_num, var in enumerate(variable_dictionary.keys()):
        day_names = [x for x in range(7)]

        daily_dict = {}
        for n,day in enumerate(day_names):
            daily_dict[day] = variable_dictionary[var].loc[variable_dictionary[var].index.dayofweek == (n)]

        # Create dictionary with each month as a key containing all monthly data
            hourly_dict = {}
            for i,hour in enumerate(hour_names):
                hourly_dict[hour] = daily_dict[day].loc[daily_dict[day].index.hour == (i)]

            sample_type = kwargs['sample_type']
            if sample_type == 'Both':
                mean_data = []
                median_data = []

                for h in hour_names:
                    mean_data.append(hourly_dict[h].mean())
                    median_data.append(hourly_dict[h].median())

                fig.add_trace(go.Scatter(
                    y = mean_data,
                    x = hour_names,
                    name = 'Mean ' + var,
                    mode = 'lines',
                    ),row = 1,col = n + 1)
                fig.add_trace(go.Scatter(
                    y = median_data,
                    x = hour_names,
                    name = 'Median ' + var,
                    mode = 'lines',
                    line = {'dash' : 'dash'}
                    ),row = 1,col = n + 1)
                fig.update_xaxes(title_text=days_of_week[n],row = 1,col = n+1)

            else:
                plot_data = []
                for h in hour_names:
                    if sample_type == 'Mean':
                        plot_data.append(hourly_dict[h].mean())
                    if sample_type == 'Median':
                        plot_data.append(hourly_dict[h].median())

                fig.add_trace(go.Scatter(
                    y = plot_data,
                    x = hour_names,
                    name = var,
                    mode = 'lines',
                    showlegend = False,
                    ),row = 1,col = n+1)

                fig.update_xaxes(title_text=days_of_week[n],row = 1,col = n+1)

            error_type = kwargs['errors']
            # Don't add error to just median
            if sample_type in ['Both', 'Mean']:
                error_bars = []
                y_upper = []
                y_lower = []

                if error_type == 'Std':
                    for h in hour_names:

                        y_upper.append(hourly_dict[h].mean() + hourly_dict[h].std())
                        y_lower.append(hourly_dict[h].mean() - hourly_dict[h].std())
                        # Need to do some jiggery pokery to create a shaded area
                    x = hour_names + hour_names[::-1]
                    y = y_upper + y_lower[::-1]
                    fig.add_trace(go.Scatter(
                        y = y,
                        x = x,
                        fill = 'tozerox',
                        line = {'color':'rgba(0,100,80,0.2)'},
                        fillcolor='rgba(0,100,80,0.2)',
                        name = var,
                        showlegend = False,
                        ),row = 1,col = n+1)
                elif error_type == '95% Confidence':
                    for h in hour_names:

                        y_upper.append(hourly_dict[h].mean() + (1.96 * hourly_dict[h].std() / (len(hourly_dict[h]) ** 0.5)))
                        y_lower.append(hourly_dict[h].mean() - (1.96 * hourly_dict[h].std() / (len(hourly_dict[h]) ** 0.5)))
                        # Need to do some jiggery pokery to create a shaded area
                    x = hour_names + hour_names[::-1]
                    y = y_upper + y_lower[::-1]

                    fig.add_trace(go.Scatter(
                        y = y,
                        x = x,
                        fill = 'tozerox',
                        line = {'color':'rgba(0,100,80,0.2)'},
                        fillcolor='rgba(0,100,80,0.2)',
                        name = var,
                        showlegend = False,
                        ),row = 1,col = n+1)

    ytitle = kwargs['ytitle']

    plot_title = kwargs['title']

    fig['layout']['yaxis1'].update(title = ytitle)
    fig['layout'].update(title = plot_title)
    # fig['layout']['xaxis4'].update(title = xtitle)
    fig['layout'].update(images=[dict(
        source="assets/all_logos.jpeg",
        xref="paper", yref="paper",
        x=1, y=1,
        sizex=0.42, sizey=0.42,
        xanchor="right", yanchor="bottom",
      )])
    for ax in range(1,8):
        ax_name = 'xaxis{}'.format(str(ax))
        fig['layout'][ax_name].update(tickmode = 'array',tickvals = [0,12,24])

    config = {"toImageButtonOptions": {"width": None, "height": None, "scale":2}}

    plot = dcc.Graph(
        id='DiurnalCyclePlot',
        figure = fig,
        # layout = layout,
        # figure={
        #     'data': fig,
        #     'layout': layout
        # },
        config = config
    )

    return plot
## ============================================================================
## END OF PROGRAM
## ============================================================================
