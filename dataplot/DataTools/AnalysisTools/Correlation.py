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

def Correlation(df,**kwargs):
    """
        Description of function here
        Function IN:
            argin (REQUIRED, DTYPE):
                Description of the argument in, wheter its REQUIRED, OPTIONAL,
                and what is DEFAULT
        Fucntion OUT:
            argout:
                Description of what the fuction returns if any
    """

    variable_dictionary = {}
    variable_options = kwargs['variable_options']

    if type(variable_options) == str:
        variable_dictionary[variable_options] = df[variable_options]
    else:
        for var in variable_options:
            variable_dictionary[var] = df[var]

    if len(variable_dictionary.keys()) != 2:
        #TODO Maybe return a faded picture to show.
        return html.P('Choose two variables for a correlation plot.')

    else:
        # Need to check this - might have the mixed up
        x = variable_dictionary[variable_options[1]]
        y = variable_dictionary[variable_options[0]]

        resample_rate = kwargs['DataResample'][0]
        if resample_rate == 'R':
            resampled_x = x
            resampled_y = y
        else:
            resampled_x = x.resample(resample_rate).apply('mean')
            resampled_y = y.resample(resample_rate).apply('mean')
        # Apply time range
        date_range = kwargs['date_range']
        resampled_x = resampled_x[date_range[0]:date_range[1]]
        resampled_y = resampled_y[date_range[0]:date_range[1]]

        swap_axis_button_clicks = kwargs['swap_button']
        if swap_axis_button_clicks % 2 == 1:
            xaxis = resampled_y
            yaxis = resampled_x
        else:
            xaxis = resampled_x
            yaxis = resampled_y

        if kwargs['colourby']:
            c = df[kwargs['colourby']]
            if resample_rate == 'R':
                resampled_c = c
            else:
                resampled_c = c.resample(resample_rate).apply('mean')
            resampled_c = resampled_c[date_range[0]:date_range[1]]
            markers = {'color': resampled_c,
                'colorscale':'Viridis',
                'showscale':True,
                'colorbar': {'title': kwargs['clabel'],
                            'titleside': 'right'}}
        else:
            markers = {}

        plot_list = [go.Scatter(
            x = xaxis,
            y = yaxis,
            mode = 'markers',
            marker = markers,
        )]

        if swap_axis_button_clicks % 2 == 1:
            xtitle = kwargs['xtitle']
            ytitle = kwargs['ytitle']
        else:
            ytitle = kwargs['xtitle']
            xtitle = kwargs['ytitle']

        plot_title = kwargs['title']

        # plot_layout = {'title':plot_title,
        #     'xaxis' : {'title':xtitle},
        #     'yaxis' : {'title':ytitle},
        #     }

        plot_layout = go.Layout(
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
        config = {"toImageButtonOptions": {"width": None, "height": None, "scale":2}}

        figure = dcc.Graph(
            id='CorrelationMainPlot',
            figure={
                'data': plot_list,
                'layout': plot_layout
            },
            config = config
        )

    return figure

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield' \
                    + 'GAUGE-CRDS_HFD_20130101_ch4-100m.nc'
    FuncName(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
