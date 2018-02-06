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

def Get_AURN_data(site_names, years):

    filename = 'dataplot/InfoFiles/DEFRA_AURN_sites_info.csv'
    sites = pd.read_csv(filename)
    site_code = sites['Site Code'].loc[sites['Site Name'] == site_names]
    site_code = site_code.values[0]

    all_dataframes = []

    if years[0] == years[1]:
        year_range = range(int(years[0]), int(years[1]) +1)
    else:
        year_range = range(int(years[0]), int(years[1]) )

    for year in year_range:

        url = "http://www.airquality.co.uk/archive/data_files/site_data/%s_%s.csv" % (site_code, year)

        df = pd.read_csv(url, skiprows = 4, dtype = str)

        # Get all the column names
        column_names = df.columns

        # Rename the columns with the units added in to the names
        col_vars = []
        for x in column_names:
            if x.split('.')[0] not in ['Date', 'time', 'status','unit']:
                col_vars.append(x)

        column_name_change = {}
        for n,v in enumerate(col_vars):
            if n == 0 :
                unit_name = 'unit'
            else:
                unit_name = 'unit.' + str(n)

            # Need to find the unit of the variable -> make sure its not a 'nan'
            var_unit_col = df[unit_name]
            units_in_col = list(var_unit_col.unique())

            for us in units_in_col:
                if type(us) == str:
                    var_unit = "(%s)" % us
            if not var_unit in locals():
                var_unit = ''

            column_name_change[v] = "%s %s" % (v, var_unit)

        df.rename(columns = column_name_change, inplace = True)

        # Get all the new column names
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
            if column == 'time':
                df[column].replace('24:00', '00:00', inplace = True)
            # Find if the column is a status column or date/time column, if it
            # is then go to next iteration, if its not then turn that value
            # from a string into a float
            if column.split('.')[0] in ['status', 'unit']:
                df.drop([column], axis = 1, inplace = True)
                continue
            elif column in ['Date', 'time']:
                continue
            else:
                df[column] = df[column].astype(float)

        # Add a new column using both date and time into a datetime format
        df['Date and Time'] = pd.to_datetime(df['Date'] + ' ' + df['time'], dayfirst = True)
        df['Date and Time'] = df['Date and Time'].apply(TidyData.add_day)
        df.set_index('Date and Time', inplace = True)

        all_dataframes.append(df)
    final_df = pd.concat(all_dataframes)
    return final_df

def AURN_environment_types():
    filename = 'dataplot/InfoFiles/DEFRA_AURN_sites_info.csv'
    sites = pd.read_csv(filename)
    env_types = list(sites['Environment Type'].unique())
    return env_types

def AURN_regions():
    filename = 'dataplot/InfoFiles/DEFRA_AURN_sites_info.csv'
    sites = pd.read_csv(filename)
    region_types = list(sites['Government Region'].unique())
    return region_types

def AURN_site_list(region, environment):
    filename = 'dataplot/InfoFiles/DEFRA_AURN_sites_info.csv'
    sites = pd.read_csv(filename)

    # If one value is submitted it will be a string not a list. Make it a Lists
    if type(region) == str:
        region = [region]
    if type(environment) == str:
        environment = [environment]

    if 'All' in region:
        regioned_sites = sites
    else:
        regioned_sites = sites.loc[sites['Government Region'].isin(region)]

    if 'All' in environment:
        env_sites = regioned_sites
    else:
        env_sites = regioned_sites.loc[sites['Environment Type'].isin(environment)]

    final_site_list = env_sites['Site Name']
    return final_site_list

def get_site_info(site_name):
    filename = 'dataplot/InfoFiles/DEFRA_AURN_sites_info.csv'
    all_sites = pd.read_csv(filename)
    site = all_sites.loc[all_sites['Site Name'] == site_name]

    site_dict = {}
    for c in all_sites.columns:
        site_dict[c] = site[c].values[0]

    return site_dict

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield/HFD_201301001_ch4-100m.csv'

    FromCSV(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
