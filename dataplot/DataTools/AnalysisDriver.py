#==============================================================================
# This is the main driving module to get the data and perform analysis
# on the data. This will be the 'control hub' of the analysis section
# of the website
#==============================================================================
# Uses modules:
# importlib, os, pkgutil, AnalysisTools
import importlib
import os
import pkgutil
from dataplot.DataTools import AnalysisTools
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData
#==============================================================================

def AnalysisMods():
    """
        Function to return list of available analysis packages that can be
        imported.
        Function IN:
            None
        Fucntion OUT:
            tool_dictionary:
                A dictionary of the available packages that can be imported from
                the AnalysisTools directory
    """

    # Path to modules that are Analysis Tools
    mod_path = os.path.dirname(AnalysisTools.__file__)
    # Get names of all usable modules in the directory
    packages = [name for _, name, _ in pkgutil.iter_modules([mod_path])]

    tool_dictionary = {}
    for mod in packages:
        tool_dictionary[mod] = importlib.import_module('dataplot.DataTools.AnalysisTools.'+ mod)

    return tool_dictionary

def GetData(sites):
    """
        This function loops gathers all the analysis modules needed and imports
        them.
        Function IN:
            parameters (OPTIONAL, LIST):

        Fucntion OUT:
            argout:
                Description of what the fuction returns if any
    """
    # Needs fucntion to specify the filenames and how the data should
    # be opened. For now lets just keep it simple with out Heathfield data

    # If there are no paramters given (and there should be)
    # then use some sample data

    # Get dataframe from LoadData.FromCSV. Leaving the input blank will get
    # the Heathfield data.

    if 'Heathfield' in sites:
        df = LoadData.FromCSV()
        df = TidyData.DateClean_Heathfeild(df)

    elif 'Edinburgh' in sites:
        df = LoadData.Edinburgh_Data()
        df.set_index('Date and Time', inplace = True)

    # Use the DateClean function to make the date into a datetime format

    # Drop last line as this is usually bogus data
    return df[:-1]

def MainDriver(app,tool_type = 'TimeSeries', sites = ['Edinburgh'],
    variables_chosen = [], vars_combined = False):
    """
        This function will send off for types of analysis to be performed
        from a chosen list.
        It will perform preprocessing analysis first (eg. resampling, date ranges)
        and then call on functions to process the data into something the plot
        functions can understand.
        Function IN:
            tool_type (REQUIRED, STRING):
                A string of the name of the analysis tool (eg. 'Histogram')
    """

    tool_dictionary = AnalysisMods()
    df = GetData(sites)


    # if resampling:
    #     # Resample by the capital letter of the option given
    #     # ie 'D' from 'Daily'
    #     df = df.resample(resampling[0]).apply('mean')

    if vars_combined:
        ##  Plot the variables together
        if tool_type == 'TimeSeries':
            return tool_dictionary[tool_type].TimeSeries(app,df, variables_chosen, combined = True)

        # if tool_type == 'Correlation':
        #     figure = tool_dictionary[tool_type].Correlation(df, variables_chosen)
        #
        # if tool_type == 'Histogram':
        #     figure = tool_dictionary[tool_type].Histogram(df,variables_chosen,combined = True)

    else:
        variables_chosen = variables_chosen[0]

        if tool_type == 'TimeSeries':
            figure = tool_dictionary[tool_type].TimeSeries(df, variables_chosen)
        elif tool_type == 'Histogram':
            figure = tool_dictionary[tool_type].Histogram(df)

            # If the type of analysis isn't availble then return an 'unknown'
        else:
            figure = "Figure type '%s' unknown." % str(tool_type)

    return figure

def GetSiteVariables(df):
    """
        Get the variables availble for a given site.
        The sitename should be a list (eg. ['Edinburgh'])
    """
    ignore_list = ['Date', 'Time', 'time', 'Date and Time', 'Status']

    variable_list = []
    for names in df.columns:
        if names.split('.')[0] in ignore_list:
            continue
        else:
            variable_list.append(names)


    return variable_list


if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters

    pass
## ============================================================================
## END OF PROGAM
## ============================================================================
