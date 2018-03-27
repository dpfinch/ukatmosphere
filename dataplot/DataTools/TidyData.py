#==============================================================================
# Module with numerous functions to clean up the data, for example get all the
# dates the same format
#==============================================================================
# Uses modules:
# datetime.datetime, datetime.timedelta, pandas
from datetime import datetime, timedelta
import pandas as pd
from dataplot.DataTools import LoadData
#==============================================================================

def DateClean_Heathfeild(df):
    """
        Transform a list of dates or times into a standard python datetime object
        Function IN:
            df (REQUIRED, LIST or PD.DATAFRAME):
                Either a dataframe from pandas with the time/date as the index
                or a list with of datetimes to be converted
        Fucntion OUT:
            df:
                Will return the same dataframe or list but with the dates
                now in the standard format used here
    """

    # Check if its a list
    if isinstance(df, list):
        ##Do list stuff
        return df

    # If the object passed is a pandas dataframe:
    elif isinstance(df, pd.core.frame.DataFrame):
        # Use pandas function to convert seconds to date
        df.index = pd.to_datetime(df.index, unit='s',
            origin = pd.Timestamp('2013-01-01'))

        return df

    else:
        # If not a list of a dataframe then currently it'll be buggered
        error_msg = 'Cannot process type %s' % str(type(df))
        return df


def SecondsSince2013(indate):
    """
        As some date formats from the file are seconds since 2013, this
        function converts this into a datatime format.
        Function IN:
            A single string or integer of the number of seconds.
        Function OUT:
            A datetime object
    """

    # Set the first date as the first of Jan 2013 - as this is when other dates
    # are measured from in seconds.
    orig_date = datetime(2013,1,1,0,0)

    return outdate


def add_day(timestamp):
    """
        This functions fixes the errror in the timeseries where converting the
        the hour '24:00:00' to '00:00:00' put the time at the beginning of the
        day instead of the end. It basically just adds a day where the hour == 0
        Function IN:
            timestap(REQUIRED, DATETIME)
        Function OUT:
            timestap(DATETIME)
    """
    if timestamp.hour == 0:
        timestamp = timestamp + timedelta(days = 1 )
    return timestamp


def subtract_hour(timestamp):
    """
    Function to subtract an hour of the timestamp given
    """

    return timestamp - timedelta(hours = 1)

def site_info_message(site_info_string):
    ## Currently only works with one site chosen
    info = site_info_string.split(',')
    site_type, sites, min_year, max_year = info[0],info[1],str(info[2]), str(info[3])

    site_dict = LoadData.get_site_info(sites)

    env_type = site_dict['Environment Type']
    gov_region = site_dict['Government Region']

    message = "Plotting data for the %s site %s between %s and %s, which is a %s site in %s.\n" % (site_type, sites, min_year, max_year, env_type, gov_region)

    return message

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield' \
                    + 'GAUGE-CRDS_HFD_20130101_ch4-100m.nc'
    DateClean(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
