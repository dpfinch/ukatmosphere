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

def GetData(parameters = []):
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
    df = LoadData.FromCSV()

    # Use the DateClean function to make the date into a datetime format
    df = TidyData.DateClean(df)

    return df

def PerformAnalysis(df):
    """
        This function will send off for types of analysis to be performed
        from a chosen list.
        It will perform preprocessing analysis first (eg. resampling, date ranges)
        and then call on functions to process the data into something the plot
        functions can understand.
        Function IN:
            df (REQUIRED, PD.DATAFRAME):
                A pandas dataframe containing the data to be processed
    """

    tool_dictionary = AnalysisMods()

    chosen_analyses = ['TimeSeries', 'Histogram']

    for analysis_type in chosen_analyses:
        if analysis_type == 'TimeSeries':
            tool_dictionary[analysis_type].TimeSeries(df, errors = False)

    pass


def MainDriver(tool_type = 'TimeSeries'):
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
    df = GetData()

    if tool_type == 'TimeSeries':
        figure = tool_dictionary[tool_type].TimeSeries(df)
    elif tool_type == 'Histogram':
        figure = tool_dictionary[tool_type].Histogram(df)

        # If the type of analysis isn't availble then return an 'unknown'
    else:
        figure = "Figure type '%s' unknown." % str(tool_type)

    return figure



if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters

    pass
## ============================================================================
## END OF PROGAM
## ============================================================================
