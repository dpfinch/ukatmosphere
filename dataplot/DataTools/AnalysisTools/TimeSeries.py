#==============================================================================
# Description of module here
#
#==============================================================================
# Uses modules:
# modulename
import dash
import dash_core_components as dcc
import dash_html_components as html
#==============================================================================

def TimeSeries(df, errors = False):
    """
        Create x and y axes for a simple time series plot. With possble errors
        Function IN:
            df (REQUIRED, PD.DATAFRAME):
                A pandas dataframe containing the data to be processed
            errors (OPTIONAL, BOOLEAN):
                Whether there are errors to be processed and included in the plots
        Fucntion OUT:
            argout:
                Description of what the fuction returns if any
    """

    variable_chosen = 'ch4 (1e-9)'
    
    # Do the preprocessing here. Any resampling etc.
    chosen_preprocess = ['dailymean']

    # If there are any chosen process to maniuplate data
    if chosen_preprocess:
        # Loop through the processes
        for process in chosen_preprocess:
            # IF statements determaning what to do
            if process == 'dailymean':
                # Create a daily mean for the plot
                daily_mean = df[variable_chosen].resample('D')


    final_plot_option = daily_mean.mean()


    xdata = final_plot_option.index
    ydata = final_plot_option

    figure = dcc.Graph(
        id='main-graph',
        figure={
            'data': [{
                'name': 'Some name',
                'mode': 'line',
                'line': {
                    'color': 'rgb(0, 0, 0)',
                    'opacity': 1
                },
                'type': 'scatter',
                'x': xdata,
                'y': ydata
            }],
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

    return figure

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield' \
                    + 'GAUGE-CRDS_HFD_20130101_ch4-100m.nc'
    TimeSeries(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
