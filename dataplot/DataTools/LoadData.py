#==============================================================================
# A number of functions to load in the data from various sources
#
#==============================================================================
# Uses modules:
# pandas, os
import pandas as pd
import os,os.path
from dataplot.DataTools import TidyData
import numpy as np
import pickle
from dataplot.models import *
from datetime import datetime as dt
from datetime import timedelta
from django.db.models import Q, Count
from rq import get_current_job
from scipy.stats import gamma
import wget
import pyreadr
from urllib.error import HTTPError,URLError
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

def Get_AURN_data(site_names, years, drop_status_and_units = True):

    filename = 'dataplot/InfoFiles/DEFRA_AURN_all_sites_info.csv'
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

        df = pd.read_csv(url, skiprows = 4, dtype = str).rename(columns=lambda x: x.strip())

        # Get all the column names
        column_names = df.columns

        # Rename the columns with the units added in to the names
        col_vars = []
        for x in column_names:
            if x.split('.')[0] not in ['Date', 'time', 'status','unit']:
                col_vars.append(x)

        # column_name_change = {}
        # for n,v in enumerate(col_vars):
        #     if n == 0 :
        #         unit_name = 'unit'
        #     else:
        #         unit_name = 'unit.' + str(n)
        #
        #     # Need to find the unit of the variable -> make sure its not a 'nan'
        #     var_unit_col = df[unit_name]
        #     units_in_col = list(var_unit_col.unique())
        #
        #     for us in units_in_col:
        #         if type(us) == str:
        #             var_unit = "(%s)" % us
        #     if not var_unit in locals():
        #         var_unit = ''
        #
        #     column_name_change[v] = "%s %s" % (v, var_unit)
        #
        # df.rename(columns = column_name_change, inplace = True)

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
                if drop_status_and_units:
                    df.drop([column], axis = 1, inplace = True)
                continue
            elif column in ['Date', 'time']:
                continue
            else:
                df[column] = df[column].astype(float)

        # Add a new column using both date and time into a datetime format
        df['Date and Time'] = pd.to_datetime(df['Date'] + ' ' + df['time'], dayfirst = True)
        df['Date and Time'] = df['Date and Time'].apply(TidyData.add_day)
        ## Remove an hour from each time stamp to take measurement from the
        ## end of the hour to the beginning of the hour. I.E. if a measurement
        ## is labeled 01:00 that will be changed to 00:00 to indicate it is for
        ## the hour 00:00 - 01:00 as DEFRA provide the time stamp indicating
        ## the end of the hour the measurement was taken.
        df['Date and Time'] = df['Date and Time'].apply(TidyData.subtract_hour)
        df.set_index('Date and Time', inplace = True)

        df.drop(['Date', 'time'], axis = 1, inplace = True)

        all_dataframes.append(df)
    final_df = pd.concat(all_dataframes)
    return final_df

def Get_AURN_Met_Data(site_code, year):
    base_url = 'https://uk-air.defra.gov.uk/openair/R_data/'
    outdir = 'temp_Rdata/'

    site_data_url = '{}_{}.RData'.format(site_code,year)
    in_url = base_url + site_data_url
    out_url = outdir + site_data_url

    try:
        wget.download(in_url,out_url)
        open_rdata = pyreadr.read_r(out_url)
        site_df = open_rdata[site_data_url.split('.')[0]]
        site_df.index = site_df.date
        site_df.drop('date',axis = 1, inplace = True)
        try:
            met_df = site_df[['wd','ws','temp']]
        except KeyError:
            os.remove(out_url)
            return None
        os.remove(out_url)
    except (HTTPError, URLError) as e:
        return None
    return met_df

def Get_One_Site_Data(site,years, variables):

    if type(variables) == str:
        variables = [variables]

    queried_measurements = measurement_data.objects.filter(
        site_id__site_name = site)

    queried_variables = queried_measurements.filter(measurement_id__in = measurement_info.objects.filter(
        variable_name__in = variables))

    # Get the range of years chosen
    year_range = range(years[0],years[1] + 1)
    selected_years = queried_measurements.filter(date_and_time__year__in = year_range)

    all_var_dfs = []
    for var in variables:

        var_info = measurement_info.objects.get(variable_name = var)

        temp_df = pd.DataFrame(list(selected_years.filter(measurement_id = var_info.id).values(
            'date_and_time', 'value', 'verified'
        )))

        temp_df.set_index('date_and_time', inplace = True)

        temp_df.rename(columns = {'value': var, 'verified':'Verified_'+var}, inplace = True)

        all_var_dfs.append(temp_df)

    final_df = pd.concat(all_var_dfs,axis = 0)
    return final_df

def o3_exceedence_count(df):
    # Maybe shouldn't be in LoadData module...
    roll8_mean = df.rolling(8).mean()
    day_exceed = roll8_mean.resample('D').max()
    day_exceed= day_exceed > 100
    # year_count = day_exceed.groupby(day_exceed.index.year).sum()
    return day_exceed

def multi_site_loop(site_list,year_start,year_end,species):
    start_date = dt(year_start, 1, 1)
    end_date = dt(year_end, 12,31)

    job = get_current_job()
    job.meta['progress'] = 0
    job.meta['current_site'] = ''
    job.save_meta()

    result_dict = {}
    env_dict = {}
    yearly_exceed_dict = {}
    env_gamma = {}
    site_dfs = []
    for i,site_name in enumerate(site_list):
        job.meta['current_site'] = site_name
        job.save_meta()
        site_data = measurement_data.objects.filter(
            site_id__site_name = site_name).filter(
                measurement_id__variable_name = species).filter(
                    date_and_time__range = (start_date, end_date)
                )

        if site_data.count() == 0:
            job.meta['progress'] = i
            job.save_meta()
            continue
        temp_df = pd.DataFrame(site_data.values_list('date_and_time','value'),
        columns = ['date_and_time',site_name])
        temp_df.set_index('date_and_time', inplace = True)
        resampled = temp_df.resample('Y').mean()
        exceedance_df = o3_exceedence_count(temp_df)
        yearly_exceed = exceedance_df.resample('Y').sum()
        above_limit = yearly_exceed > 10
        env_type = site_info.objects.get(site_name = site_name).environment_type
        if env_type not in env_dict.keys():
            env_dict[env_type] = []
            yearly_exceed_dict[env_type] = []
            env_gamma[env_type] = []
        env_dict[env_type].append(exceedance_df)
        yearly_exceed_dict[env_type].append(above_limit)
        site_dfs.append(resampled)
        job.meta['progress'] = i
        job.save_meta()

    final_exceed_dfs = {}
    yearly_sites_above = {}
    for env_type in env_dict.keys():
        env_exceed_df = pd.concat(env_dict[env_type], axis = 1)
        # gamma_df = gamma_df = pd.DataFrame(columns = ['Alpha','Beta'])
        # for year in env_exceed_df.index.year.unique():
        #     year_df = env_exceed_df[env_exceed_df.index.year == year]
        #     year_list = year_df.values.flatten()
        #     print(year_list[:10])
        #     year_list = year_list[~np.isnan(year_list)]
        #     alpha,fit, beta = gamma.fit(year_list, floc = 0)
        #     gamma_df.loc[year] = [alpha,beta]
        # env_gamma[env_type] = gamma_df
        total_env_exceed = env_exceed_df.sum(axis = 1)
        total_env_exceed.name = env_type
        final_exceed_dfs[env_type] = total_env_exceed
        env_above_limit = pd.concat(yearly_exceed_dict[env_type], axis = 1)
        total_above_limit = env_above_limit.sum(axis = 1)
        total_above_limit.name = env_type
        yearly_sites_above[env_type]  = total_above_limit
    final_exceed_df = pd.DataFrame.from_dict(final_exceed_dfs)
    final_df = pd.concat(site_dfs,axis = 1)
    final_above_limit_df = pd.DataFrame.from_dict(yearly_sites_above)
    result_dict = {'conc':final_df, 'exceedance':final_exceed_df,
    'sitesabove':final_above_limit_df, 'gamma': env_gamma}
    return result_dict


def get_recent_site_data(site_name, species, days_ago = 7):
    #  Will do last week or something simmilar
    #  currently (Since we don't have up to date data)
    #  we'll just show the last 7 days of what we've got.

    # Get latest date
    latest_date = measurement_data.objects.filter(
        site_id__site_name = site_name).filter(
            measurement_id__variable_name = species).latest('date_and_time').date_and_time

    first_date = latest_date - timedelta(days = days_ago)

    site_obs = measurement_data.objects.filter(site_id__site_name = site_name).filter(
        measurement_id__variable_name = species).filter(
            date_and_time__range = (first_date, latest_date)
        )

    site_df = pd.DataFrame(site_obs.values_list('date_and_time', 'value'),
        columns = ['Date and Time', 'Concentration'])
    site_df.set_index('Date and Time', inplace = True)
    return site_df

def get_all_species_obvs(species, environment, region, year_start, year_end):
    start_date = dt(year_start, 1, 1)
    end_date = dt(year_end, 12,31)

    filters = {}
    filters['date_and_time__range'] = (start_date, end_date)
    filters['measurement_id__variable_name'] = species
    if region != 'All':
        filters['site_id__region'] = region
    if environment != 'All':
        filters['site_id__environment_type'] = environment

    obvs = measurement_data.objects.filter(**filters)
    site_series = []
    for site in obvs.values('site_id__site_name').distinct():
        site_obvs = obvs.filter(**site)
        temp_series = pd.Series(site_obvs.values_list('value', flat = True), index=
            site_obvs.values_list('date_and_time'))
        temp_series.name = site['site_id__site_name']
        site_series.append(temp_series)

    final_df = pd.concat(site_series, axis = 1)

    return final_df

def Get_Data_Count(region,environment, year_start,year_end, species):
    start_date = dt(year_start, 1, 1)
    end_date = dt(year_end, 12,31)

    filters = {}
    filters['date_and_time__range'] = (start_date, end_date)
    filters['measurement_id__variable_name'] = species
    if region != 'All':
        filters['site_id__region'] = region
    if environment != 'All':
        filters['site_id__environment_type'] = environment

    obvs = measurement_data.objects.filter(**filters)
    return obvs.count()

def Get_Species_Sites(species, environment,region, currently_open,year_start,year_end):
    start_date = dt(year_start, 1, 1)
    end_date = dt(year_end, 12,31)

    filters = {}
    if currently_open:
        filters['relevant_site__site_open'] = True
    if region != 'All':
        filters['relevant_site__region'] = region
    if environment != 'All':
        filters['relevant_site__environment_type'] = environment

    site_query = pollutants_details.objects.filter(pollutant_name = species).filter(
        **filters)

    date_query = site_query.filter(Q(end_date__gte = start_date)|Q(
        relevant_site__site_open = True)).filter(start_date__lte = end_date)

    species_sites = pd.DataFrame(date_query.values_list('relevant_site__site_name', 'relevant_site__region', 'relevant_site__environment_type'),
        columns = ['Site Name', 'Region', 'Environment'])

    # HUUUUUUGE BODGE - Need to address
    # For some reason London Cromwell Road is in the database but has no data
    if 'London Cromwell Road' in species_sites['Site Name'].values:
        species_sites = species_sites[species_sites['Site Name'] != 'London Cromwell Road']

    return species_sites

def Estimate_data_count(species, sites_df, year_min, year_max):
    end_date = dt(year_max,12,31).date()
    start_date = dt(year_min,1,1).date()

    count_estimate = 0
    for site in sites_df['Site Name']:
        site_obj = site_info.objects.get(site_name = site)
        if site_obj.site_open:
            if site_obj.date_open > start_date:
                day_diff = end_date - site_obj.date_open
            else:
                day_diff =  end_date - start_date
        else:
            if site_obj.date_open > start_date:
                day_diff = site_obj.date_closed - site_obj.date_open
            else:
                day_diff =  site_obj.date_closed - start_date

        count_estimate += day_diff.days * 24
    return count_estimate

def Yearly_Site_Count(species,split_by = None):
    years = []

    if split_by and split_by.lower() == 'region':
        regions = site_info.objects.all().values_list(
            'region', flat = True).distinct().order_by('region')
        out_df = pd.DataFrame(columns = regions)
    elif split_by and split_by.lower() == 'environment':
        envs = site_info.objects.all().values_list(
            'environment_type', flat = True).distinct().order_by('environment_type')
        out_df = pd.DataFrame(columns = envs)
    else:
        yearly_site_count = []

    for year in range(1979,dt.now().year + 1):
        years.append(year)
        opensites = pollutants_details.objects.filter(
            pollutant_name = species,relevant_site__date_open__year__lte = year)
        site_count = opensites.filter(
            Q(relevant_site__date_closed__year__gte = year)|Q(relevant_site__site_open = True))

        if split_by and split_by.lower() == 'region':
            region_count = site_count.values('relevant_site__region').annotate(
                total = Count('relevant_site__region')).order_by('relevant_site__region')
            out_df = out_df.append(pd.Series(name = year))

            for region in region_count:
                out_df.loc[year][region['relevant_site__region']] = region['total']


        elif split_by and split_by.lower() == 'environment':
            env_count = site_count.values('relevant_site__environment_type').annotate(
                total = Count('relevant_site__environment_type')).order_by('relevant_site__environment_type')
            out_df = out_df.append(pd.Series(name = year))
            for env in env_count:
                out_df.loc[year][env['relevant_site__environment_type']] = env['total']

        else:
            yearly_site_count.append(site_count.count())
    if not split_by:
        out_df = pd.DataFrame(yearly_site_count, index = years, columns = ['Site Count'])
    else:
        out_df['Total'] = out_df.sum(axis =1).astype(int)
    out_df.fillna(0,inplace = True)
    return out_df

def all_sites_one_var_data(date,variable, region, environment):

    filters = {}
    filters['date_and_time__year'] = date.year
    filters['date_and_time__month'] = date.month
    filters['date_and_time__day'] = date.day
    filters['date_and_time__hour'] = date.hour
    filters['measurement_id__variable_name'] = variable
    if region != 'All':
        filters['site_id__region'] = region
    if environment != 'All':
        filters['site_id__environment_type'] = environment

    vals = measurement_data.objects.filter(**filters)

    final_df = pd.DataFrame(vals.values_list('site_id__site_name','site_id__latitude', 'site_id__longitude','value'),
        columns = ['site_name','latitude','longitude','value'])

    final_df.set_index('site_name', inplace = True)

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

def AURN_site_list_db(region,environment, open_sites_only = True):
    # Get all the avaible sites in the databse (which are AURN related)
    # Get unique site codes primary keys
    # Old method - pretty slow
    # avail_sites_pks = list(measurement_data.objects.values_list('site_id', flat=True).distinct())

    # site_df = pd.DataFrame(list(site_info.objects.filter(id__in = avail_sites_pks).values()))
    # Now just list the open sites - runs the risk of a site being open but we don't have data for it
    #  but should be ok
    if open_sites_only:
        site_df = pd.DataFrame(list(site_info.objects.filter(site_open = True).values()))
    else:
        site_df = pd.DataFrame(list(site_info.objects.all().values()))
    aurn_df = site_df.loc[site_df.site_type.isin(['DEFRA AURN'])]
    # If one value is submitted it will be a string not a list. Make it a Lists
    if type(region) == str:
        region = [region]
    if type(environment) == str:
        environment = [environment]

    if 'All' in region:
        regioned_sites = aurn_df
    else:
        regioned_sites = aurn_df.loc[aurn_df['region'].isin(region)]

    if 'All' in environment:
        env_sites = regioned_sites
    else:
        env_sites = regioned_sites.loc[regioned_sites['environment_type'].isin(environment)]

    final_site_list = env_sites['site_name']
    return final_site_list

def get_all_site_info(environment, region):
    filters = {}
    if region != 'All':
        filters['region'] = region
    if environment != 'All':
        filters['environment_type'] = environment

    # using filters like this means we can have no filter or many
    all_sites = site_info.objects.filter(**filters)

    if len(all_sites) == 0:
        final_site_df  = pd.DataFrame({'latitude':[], 'longitude': [], 'site_name':[]})
    else:
        final_site_df = pd.DataFrame(list(all_sites.values('site_name', 'latitude', 'longitude')))

    final_site_df.set_index('site_name', inplace = True)
    return final_site_df


def get_site_info_object(site_name):

    site = site_info.objects.get(site_name = site_name)

    return site

def get_site_year_range_db(site_name):
    site = site_info.objects.get(site_name = site_name)

    start_data = measurement_data.objects.filter(site_id = site).earliest('date_and_time')
    start_year = start_data.date_and_time.year
    end_data = measurement_data.objects.filter(site_id = site).latest('date_and_time')
    end_year = end_data.date_and_time.year

    # if site.date_closed:
    #     end_year = site.date_closed.year
    # else:
    #     end_year = dt.now().year
    return start_year, end_year

def get_site_year_range(site_name):
    sites = pickle.load(open('dataplot/InfoFiles/All_AURN_site_variables.p', 'rb'))
    site_info = sites[site_name]

    try:
        start_year = int(site_info['Start_Year'])
        end_year = int(site_info['End_Year'])
    except ValueError:
        start_year = None
        end_year = None

    return start_year, end_year

def get_species_year_range(species, environment, region):

    filters = {}
    filters['measurement_id__variable_name'] = species
    if region != 'All':
        filters['site_id__region'] = region
    if environment != 'All':
        filters['site_id__environment_type'] = environment


    obvs =  measurement_data.objects.filter(
        **filters)

    start_year = obvs.earliest('date_and_time').date_and_time.year
    end_year = obvs.latest('date_and_time').date_and_time.year
    return start_year,end_year

def Get_Site_Variables(site):
    site = site_info.objects.get(site_name = site)
    site_variables = list(pollutants_details.objects.filter(relevant_site = site).values_list('pollutant_name'))

    variable_list = [x[0] for x in site_variables]
    variable_list.sort()

    for v in variable_list:
        if 'modelled' in v.lower().split():
            variable_list.remove(v)

    return variable_list

def Get_Site_Variables_db(site):
    # Get the availble measured info from the site
    avail_measurements = measurement_data.objects.filter(site_id__site_name = site)
    measurement_ids = list(avail_measurements.values_list('measurement_id', flat = True).distinct())

    variable_list = list(measurement_info.objects.filter(
        id__in = measurement_ids).values_list('variable_name', flat = True))

    # for s in range(len(variable_list)):
    #     if '<sub>' in variable_list[s]:
    #         variable_list[s] = variable_list[s].replace('<sub>','').replace('</sub>','')

    # Don't get modelled data (yet)
    for v in variable_list:
        if 'modelled' in v.lower().split():
            variable_list.remove(v)

    return variable_list

def get_all_aurn_species():
    species_query = measurement_info.objects.filter(measurement_name__contains='AURN')
    species_list = list(species_query.values_list('variable_name', flat = True))

    # for s in range(len(species_list)):
    #     if '<sub>' in species_list[s]:
    #         species_list[s] = species_list[s].replace('<sub>','').replace('</sub>','')

    return species_list

def Get_Unit(site_type, species):
    unit = measurement_info.objects.filter(measurement_name__contains = site_type).get(
    variable_name = species).unit

    if unit[-2:] in ['-2', '-3']:
        unit =  unit[:-2] + '<sup>-%s</sup>' % unit[-1]

    return unit

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # parameters
    filename  = 'RawData/Heathfield/HFD_201301001_ch4-100m.csv'

    FromCSV(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
