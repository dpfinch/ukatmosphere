import os
from datetime import datetime as dt
import pandas as pd
from dataplot.models import site_info, pollutants_details, measurement_info,measurement_data
from dataplot.DataTools import LoadData
from django.utils import timezone
import pickle

### Need to put measurement data into database
def DEFRA_AURN_data_to_db(df,site_code):

    pollutant_cols = []
    status_cols = []
    unit_cols = []

    for c in df.columns:
        if c.split('.')[0].lower() == 'status':
            status_cols.append(c)
        elif c.split('.')[0].lower() == 'unit':
            unit_cols.append(c)
        else:
            pollutant_cols.append(c)

    for i, col in enumerate(pollutant_cols):
        # Check to see if I've got info on the variable.
        # Only have info on standard AURN variables so far
        try:
            chemical_formula = Get_Chemical_Formula(col)
        except IndexError:
            continue
        # Get the unit for the column variable
        # The corresponding unit column is:
        unit_col = df[unit_cols[i]]
        unit_col.dropna(inplace = True)
        unit = unit_col.unique()[0] # This assume there is only one unit - why wouldn't there be?!
        # Remove PM extra bit
        unit = unit.replace('(TEOM FDMS)', '').strip()

        # Get the relevant status for the measurement
        status_col = df[status_cols[i]]
        status_col.replace('R','V', inplace = True)
        # Fill the nan values with 'U' for unknown - although this will rarely be
        # a problem as all nan status have a matching nan measurement
        status_col.dropna(inplace = True)
        status_col.fillna('U', inplace = True)

        measurement_name = 'DEFRA_AURN_%s' % chemical_formula
        temp_col = df[col]
        temp_col.dropna(inplace = True)
        for n in range(len(temp_col)):

            x = temp_col[n]
            entry = measurement_data(
                date_and_time = temp_col.index[n],
                value = x,
                verified = status_col[n],
            )

            if site_info.objects.filter(site_code = site_code).exists():
                entry.site_id = site_info.objects.filter(site_code = site_code)[0]
                # Need an else....
            if measurement_info.objects.filter(measurement_name = measurement_name).exists():
                entry.measurement_id = measurement_info.objects.filter(measurement_name = measurement_name)[0]
            else:
                meas_info = measurement_info(
                    variable_name = col,
                    unit = unit,
                    chemical_formula = chemical_formula,
                    measurement_name = measurement_name
                )
                meas_info.save()
                entry.measurement_id = meas_info
            entry.save()

def Get_Latest_AURN_Data(site_name, year):
    # Just add the latest data to the database. This relies on all variables
    # in a site being updated at the same time. Which I think is correct.

    df = LoadData.Get_AURN_data(site_name, [year,year], drop_status_and_units = False)

    # Get the site code - I need a cleaner way of doing this...
    filename = 'dataplot/InfoFiles/DEFRA_AURN_sites_info.csv'
    sites = pd.read_csv(filename)
    site_code = sites['Site Code'].loc[sites['Site Name'] == site_name]
    site_code = site_code.values[0]

    # Query the site info based on the site code
    site_id = site_info.objects.filter(side_code = site_code)
    # Get the latest date and time in the database for a given site
    most_recent_date = measurement_info.objects.latest('date_and_time').date_and_time

    trimmed_df = df.loc[df.index > most_recent_date]

    DEFRA_AURN_data_to_db(trimmed_df,site_code)

def Update_DEFRA_Data(site_name):
    ## Find where the database still has unverified data in and see
    ## if the DEFRA site has been updated.
    site_id = site_info.objects.filter(side_code = site_code)
    site_data = measurement_info.objects.filter(site_id = site_id)

    # Only get data that hasn't been verified but isn't unknown
    queried_data = site_data.exclude(verified = 'V').exclude(verified = 'U')

    # Into a dataframe for ease of use
    current_data = pd.DataFrame.from_records(queried_data.values('date_and_time', 'value','verified'),
        index = 'date_and_time')

    # Get the years that still have unverified data
    years = current_data.index.year.unique().values
    # If the range of years is more than two then its unlikely it'll
    # ever be verifed so ignore it
    if len(years) > 2:
        years[years[0],years[1]]

    if max(years) < dt.now().year - 1:
        # If the maximum year is more than a year ago then don't bother doing anything
        pass

    if min(years) < dt.now().year - 1:
        # If the minimum year is more than a year ago then only use recent year
        years = [years[0]]

    # Load in the data again
    new_df = LoadData.Get_AURN_data(site_name, [years[0],years[-1]],
        drop_status_and_units = False)

    pollutant_cols = []
    status_cols = []
    unit_cols = []

    for c in df.columns:
        if c.split('.')[0].lower() == 'status':
            status_cols.append(c)
        elif c.split('.')[0].lower() == 'unit':
            unit_cols.append(c)
        else:
            pollutant_cols.append(c)
    # Need to now update the database
    for i,col in enumerate(pollutant_cols):
        # Get the relevant status for the measurement
        status_col = df[status_cols[i]]
        status_col.replace('R','V', inplace = True)
        # Fill the nan values with 'U' for unknown - although this will rarely be
        # a problem as all nan status have a matching nan measurement
        status_col.dropna(inplace = True)
        status_col.fillna('U')

        chemical_formula = Get_Chemical_Formula(col)
        measurement_name = 'DEFRA_AURN_%s' % chemical_formula

        temp_col = new_df[col]
        temp_col.dropna(inplace = True)

        for x in range(len(temp_col)):
            # Filter the data by measurement_id, site and time
            # There should only be one data entry for each of these
            data_entry = measurement_data.objects.filter(
                measurement_id = measurement_name).filter(
                site_id = site_id).filter(
                date_and_time = temp_col.index[x])[0]

            if data_entry.verified == 'V':
                continue
            elif status_col[x] in ['U','N']:
                continue
            elif status_col[x] == data_entry.verified:
                continue
            else:
                data_entry.verified = status_col[x]
                data_entry.value = temp_col[x]
                data_entry.save()


def Delete_all_DEFRA_data():
    ## A module to clear all the measurement data from the database
    ## Hopefully will never be needed!
    measurement_info.objects.all().delete()

def Fill_DEFRA_AURN_DB():
    ## This will be a module to fill up the db with the past values
    ## Likely/hopefully only need this the once.
    all_sites_query = site_info.objects.all()

    ## Need to prioritise input as this takes and absolute age.


    for site in all_sites_query:
        site_name = site.site_name
        site_code = site.site_code
        site_open = site.site_open
        date_open = site.date_open
        date_closed = site.date_closed

        # This skips sites that have already been added to the database
        ### THIS IS NOT A SMART WAY OF DOING THIS BUT IS A TEMP BODGE
        if measurement_data.objects.filter(site_id = site_info.objects.filter(site_name = site_name)).exists():
            continue

        # Don't include sites that are just a quick PM10 site
        # Only inlcudes Brighton Roadside PM10 & Northampton PM10
        if 'PM10' in site_name:
            continue

        # Load in dataframe - could be a memory issue here with the
        # site open the longest
        if site_open:
            date_closed = dt.now()

        # For the time being only get 2018 data
        if site_open:

            print('Getting data for %s: %d - %d (%s)' % (site_name, date_open.year, date_closed.year, site_code))
            df = LoadData.Get_AURN_data(site_name, [2018,2018],
                drop_status_and_units = False)

            DEFRA_AURN_data_to_db(df,site_code)
            print('Submitted to database')


def Get_Chemical_Formula(chemical_name):
    chems = pd.read_csv('dataplot/InfoFiles/Chemical_Formula.csv', dtype = str).rename(columns=lambda x: x.strip())
    for col in chems.columns:
        chems[col] = chems[col].str.strip()

    # Take out any sub html commands
    chemical_name = chemical_name.replace('<sub>', '')
    chemical_name = chemical_name.replace('</sub>', '')

    chemical = chems.loc[chems['Variable Name'].str.lower() == chemical_name.strip().lower()]


    return chemical['Variable Formula'].values[0]
