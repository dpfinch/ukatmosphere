import schedule
from dataplot.models import *
from dataplot import AQ_data_into_db as db
from datetime import datetime as dt
from dataplot.DataTools import LoadData
import pandas as pd
from urllib.error import HTTPError,URLError

#### THIS IS A BRUTE FORCE UPLOAD ALL THE DEFRA DATA ####

def latest_AURN_station_data():
    all_avail_sites = site_info.objects.filter(site_type = 'DEFRA AURN').filter(
        site_open = True).values_list('site_name')
    sites = [x[0] for x in all_avail_sites]
    sites.sort()
    year = dt.now().year

    ## Catch if its a new year and get the previous year
    if dt.now().month == 1 and dt.now().day == 1:
        year = year - 1

    for site in sites:
        print(site)
        db.Get_Latest_AURN_Data(site,year)

def update_AURN_verified():
    all_avail_sites = site_info.objects.filter(site_type = 'DEFRA AURN').values_list('site_name')
    sites = [x[0] for x in all_avail_sites]

    for site in sites:
        db.Update_DEFRA_Data(site)


### TO RUN AS A SCRIPT
print("Committing stuff to database")

all_avail_sites = site_info.objects.filter(site_type = 'DEFRA AURN')
# For speeds sake lets bodge what I know has already completed
for site in all_avail_sites[:]:
    if site.site_name.split()[-1] in ['PM10','PM2.5','PM25']:
        continue

    site_year_open = site.date_open.year
    site_year_closed = site.date_closed

    if site_year_closed:
        site_year_closed = site_year_closed.year
    else:
        site_year_closed = dt.now().year


    for year in range(site_year_open,site_year_closed + 1):
        print('Processing {} data for site {}'.format(year, site.site_name))
        try:
            df = LoadData.Get_AURN_data(site.site_name,[year,year], drop_status_and_units = False)
        except (HTTPError, URLError) as e:
            print('No web data for {} {}'.format(site.site_name,year))
            continue
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


            all_entries = []
            # Check to see if I've got info on the variable.
            # Only have info on standard AURN variables so far
            try:
                chemical_formula = db.Get_Chemical_Formula(col)
            except IndexError:
                continue

            # Check this is actually data in the dataframe (ignores nans)
            if df[col].count() == 0:
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

            measurement_name = 'DEFRA_AURN_{}'.format(chemical_formula)
            if not measurement_info.objects.filter(measurement_name = measurement_name).exists():
                meas_info = measurement_info(
                    variable_name = col,
                    unit = unit,
                    chemical_formula = chemical_formula,
                    measurement_name = measurement_name
                )
                meas_info.save()

            meas_name_id = measurement_info.objects.get(measurement_name = measurement_name)

            temp_col = df[col]
            temp_col.dropna(inplace = True)

            filters = {'site_id':site,
                        'date_and_time__year': year,
                        'measurement_id':meas_name_id}
            avail_data = measurement_data.objects.filter(
                **filters)

            if len(avail_data):
                earliest_meas = avail_data.earliest('date_and_time')
                latest_meas = avail_data.latest('date_and_time')
                if temp_col.index[-1].to_pydatetime() == latest_meas.date_and_time:
                    continue
                else:
                    temp_col = temp_col[temp_col.index > pd.to_datetime(
                        latest_meas.date_and_time)]

            if len(temp_col) == 0:
                continue
            for n,x in enumerate(temp_col):
                if status_col[n] == 'P*':
                    status_val = 'P'
                else:
                    status_val = status_col[n]

                entry = measurement_data(
                    date_and_time = temp_col.index[n],
                    value = x,
                    verified = status_val,
                    site_id = site,
                    measurement_id = meas_name_id
                )

                all_entries.append(entry)
            print('Adding {} entries of {} for {} at {} to the database...'.format(len(all_entries), col,year,site.site_name))
            measurement_data.objects.bulk_create(all_entries)
            print('Entries entered')
