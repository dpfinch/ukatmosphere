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

# def Histogram(df, variables, combined = False):
#     """
#         Description of function here
#         Function IN:
#             argin (REQUIRED, DTYPE):
#                 Description of the argument in, wheter its REQUIRED, OPTIONAL,
#                 and what is DEFAULT
#         Fucntion OUT:
#             argout:
#                 Description of what the fuction returns if any
#     """
#
#     vars_dictionary = {}
#     if combined:
#         for n, var in enumerate(variables):
#             vars_dictionary['var_'+str(n+1)] = var
#
#         plot_list = []
#
#         for k in vars_dictionary.keys():
#             plot_list.append(go.Histogram(
#                 x = df[vars_dictionary[k]])
#                 )
#
#     else:
#
#         plot_list = [go.Histogram(
#             x = df[variables]
#             )]
#
#     figure = dcc.Graph(
#         id='main-graph',
#         figure={
#             'data': plot_list,
#             'layout': {
#                 'autosize': True,
#                 'scene': {
#                     'bgcolor': 'rgb(255, 255, 255)',
#                     'xaxis': {
#                         'titlefont': {'color': 'rgb(0, 0, 0)'},
#                         'title': 'X-AXIS',
#                         'color': 'rgb(0, 0, 0)'
#                     },
#                     'yaxis': {
#                         'titlefont': {'color': 'rgb(0, 0, 0)'},
#                         'title': 'Y-AXIS',
#                         'color': 'rgb(0, 0, 0)'
#                     }
#                 }
#             }
#         }
#     )
#
#
#
#     return figure

def app_time():
    app = dash.Dash()

    app.config.suppress_callback_exceptions = True

    app.layout = html.Div([
        dcc.Location(id = 'url', refresh = False ),
        html.Div([dcc.RadioItems(
                id='resampling',
                options=[{'label': i, 'value': i} for i in ['Daily', 'Weekly','Monthly']],
                value='Daily',
                labelStyle={'display': 'inline-block'}
            )]),
        html.Div(id = 'graph')
        ])

    @app.callback(
        dash.dependencies.Output('graph', 'children'),
        [dash.dependencies.Input('resampling','value'),
        dash.dependencies.Input('url','pathname')
        ])
    def display_plot(value,pathname):
        from dataplot.DataTools.AnalysisDriver import GetData
        df = GetData(['Edinburgh'])
        variables = ['Ozone', 'Nitric oxide']
        combined = True

        df = df.resample(value[0]).apply('mean')
        vars_dictionary = {}
        if combined:
            for n, var in enumerate(variables):
                vars_dictionary['var_'+str(n+1)] = var

            plot_list = []

            for k in vars_dictionary.keys():
                plot_list.append(go.Histogram(
                    x = df[vars_dictionary[k]],
                    )
                    )

        else:

            plot_list = [go.Histogram(
                x = df[variables],

                )]

        plot_holder = dcc.Graph(
            id='main-graph',
            figure={
                'data': plot_list,
                'layout': {
                    'autosize': True,
                    'scene': {
                        'bgcolor': 'rgb(255, 255, 255)',
                        'xaxis': {
                            'titlefont': {'color': 'rgb(0, 0, 0)'},
                            'title': 'X-AXIS',
                            'color': 'rgb(0, 0, 0)'
                        },
                        'yaxis': {
                            'titlefont': {'color': 'rgb(0, 0, 0)'},
                            'title': 'Y-AXIS',
                            'color': 'rgb(0, 0, 0)'
                        }
                    }
                }
            }
        )

        return plot_holder

    return app


if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # paramters
    filename  = 'RawData/Heathfield' \
                    + 'GAUGE-CRDS_HFD_20130101_ch4-100m.nc'
    Histogram(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
