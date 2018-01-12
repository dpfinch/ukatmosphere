#==============================================================================
# A number of functions to load in the data from various sources
#
#==============================================================================
# Uses modules:
# pandas, os
import pandas as pd
import os.path
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
        filename = './RawData/Heathfield/HFD_20130101_ch4-100m.csv'

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

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield/HFD_201301001_ch4-100m.csv'

    FromCSV(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
