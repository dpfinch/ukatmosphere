#==============================================================================
# A number of functions to load in the data from various sources
#
#==============================================================================
# Uses modules:
# pandas, os
import pandas as pd
import os.path
from dataplot.DataTools import TidyData
import numpy as np
#==============================================================================

def FromCSV(filename = None, parameters = []):
    """
        Read in data from a CSV file in the website directory
        Function IN:
            filename (OPTIONAL, STRING):
                The filename to be read. If this is not provided it will use data
                from Heathfield measure CH4 at 100m since 2013
            paramters (OPTIONAL, LIST):
                Any parameters, eg. time range, specific variables
        Fucntion OUT:
            df:
                A pandas DataFrame with all the variables specified. Time will be
                the index although not formatted.
    """

    # Set filename to Heathfield data is there isn't a filename provided
    if not filename:
        filename = 'RawData/Heathfield/HFD_20130101_ch4-100m.csv'

    # Check if the given filename is a file
    if not os.path.isfile(filename):
        error_msg = 'File either does not exists or is not a file'
        print(filename)
        return error_msg

    # Get the headers of the csv file to set the index and columns in DataFrame
    f = open(filename)
    headers = f.readline()
    f.close()

    headers = headers.split(',')
    first_col = headers[0]

    # Import the file into a dataframe and set the index and the first column
    # from the file. This should be time in most cases.
    df = pd.read_csv(filename, index_col = first_col)

    # Return the dataframe
    return df


def Edinburgh_Data():
    """
        This will open the sample Edinburgh data we've currently got.
        This is only a temporay measure before we know more about
        data input.
    """

    filename = 'RawData/Edinburgh/edinburgh_st_leonards_2015_2017.csv'

    # Read straight into pandas data frame
    # Skipping first four lines
    # Needs datatype (dtype) as string since columns mix datatypes
    skip_num_rows = 4
    df =  pd.read_csv(filename, skiprows = int(skip_num_rows), dtype = str)
    # Get all the column names
    column_names = df.columns
    # Loop through each column and repace 'No data' with NaNs
    # - easier to process into numbers not strings
    for column in column_names:
        df[column].replace('No data', np.nan, inplace = True)
        # In the time column replace the hour 24 with zero
        # This is needed for pandas to convert to a datetime type
        # This creates an error in the data as the value for 00:00:00 in then
        # placed at the beginning of the day instead of the end. ie. It should
        # changed to 00:00:00 and the date moved forward one day. This is
        # recitifed later.
        if column == 'Time':
            df[column].replace('24:00:00', '00:00:00', inplace = True)
        # Find if the column is a status column or date/time column, if it
        # is then go to next iteration, if its not then turn that value
        # from a string into a float
        if column.split('.')[0] == 'Status':
            continue
        elif column in ['Date', 'Time']:
            continue
        else:
            df[column] = df[column].astype(float)

    # Add a new column using both date and time into a datetime format
    df['Date and Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Date and Time'] = df['Date and Time'].apply(TidyData.add_day)
    return df

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield/HFD_201301001_ch4-100m.csv'

    FromCSV(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
