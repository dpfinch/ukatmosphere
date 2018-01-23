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

# def TimeSeries(df=None, variables=None, combined = False):
# """
#     Create x and y axes for a simple time series plot. With possble errors
#     Function IN:
#         df (REQUIRED, PD.DATAFRAME):
#             A pandas dataframe containing the data to be processed
#         errors (OPTIONAL, BOOLEAN):
#             Whether there are errors to be processed and included in the plots
#     Fucntion OUT:
#         argout:
#             Description of what the fuction returns if any
# """
# def app_time():
#     app = dash.Dash()
#
#     app.config.suppress_callback_exceptions = True

page_layout = html.Div([
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
    ])
def display_plot(value):
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
            plot_list.append(go.Scatter(
                x = df[vars_dictionary[k]].index,
                y = df[vars_dictionary[k]],
                mode = 'markers')
                )

    else:

        plot_list = [go.Scatter(
            x = df[variables].index,
            y = df[variables],
            mode = 'markers'
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
    })

    return plot_holder

    # return app
    # return page_layout

## ============================================================================
## END OF PROGAM
## ============================================================================
