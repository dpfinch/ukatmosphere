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
    Info about DateDayHeatmap will go here
'''
def DateDayHeatmap(df, **kwargs):

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    # Will only be able to handle on variable
    if type(variable_options) == str:
        var = df[variable_options]
    else:
        if len(variable_options) == 0:
            return ''
        var = df[variable_options[0]]

    date_range = kwargs['date_range']

    # var = var[date_range[0]:date_range[1]]

    hours_in_day = [x for x in range(24)]
    z_dim = []

    for h in hours_in_day:
        z_dim.append(list(var.loc[var.index.hour == h]))


    plot = [go.Heatmap(
        z = z_dim,
        x = var.index,
        y = hours_in_day,
        colorscale = 'Viridis',
        colorbar = {'title': kwargs['clabel'],
                    'titleside': 'right'}
    )]

    xtitle = 'Date'
    ytitle = 'Hour of the Day'
    plot_title = kwargs['title']

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

    figure = dcc.Graph(
        id='DateDayHeatmapPlot',
        figure={
            'data': plot,
            'layout': plot_layout
    })

    return figure
## ============================================================================
## END OF PROGAM
## ============================================================================
