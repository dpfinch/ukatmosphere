from dataplot.models import *
import pickle
from datetime import datetime as dt
import pandas as pd
from dataplot.DataTools import LoadData
from urllib.error import HTTPError,URLError

# def add_met_meta_to_database():
add_met_meta_to_database = False
if add_met_meta_to_database:
    variables = ['Modelled Wind Speed','Modelled Wind Direction','Modelled Temperature']
    var_units = ['m/s','deg','C']
    chem_forms = ['ws','wd','T']
    all_meas = measurement_info.objects.all()
    for n,variable in enumerate(variables):
        meas_info = measurement_info(
            variable_name = variable,
            unit = var_units[n],
            chemical_formula = chem_forms[n],
            measurement_name = 'Modelled_AURN_{}'.format(chem_forms[n].upper())
        )
        meas_info.save()

update_met_data = True
if update_met_data:
    print('Adding all modelled met data to database')

    all_avail_sites = site_info.objects.filter(site_type = 'DEFRA AURN')

    var_ids = {'wd':measurement_info.objects.get(measurement_name ='Modelled_AURN_WD'),
        'ws':measurement_info.objects.get(measurement_name ='Modelled_AURN_WS'),
        'temp':measurement_info.objects.get(measurement_name ='Modelled_AURN_T')}

    for site in all_avail_sites[:]:
        if site.site_name.split()[-1] in ['PM10','PM2.5','PM25']:
            continue

        print('Updating {}'.format(site))
        site_year_open = site.date_open.year
        site_year_closed = site.date_closed

        if site_year_open < 2010:
            site_year_open = 2010 # This is when modelled met started

        site_year_open = 2020

        if site_year_closed:
            site_year_closed = site_year_closed.year
        else:
            site_year_closed = dt.now().year
        for year in range(site_year_open,site_year_closed + 1):
            # print(year)
            site_code  = site.site_code
            # try:
            df = LoadData.Get_AURN_Met_Data(site_code, year)
            # except (HTTPError, URLError, KeyError) as e:
            #     continue
            if type(df) != pd.core.frame.DataFrame:
                continue
            all_entries = []
            for var in df.columns:

                filters = {'site_id':site,
                            'date_and_time__year': year,
                            'measurement_id':var_ids[var]}
                avail_data = measurement_data.objects.filter(
                    **filters)

                if len(avail_data):
                    earliest_meas = avail_data.earliest('date_and_time')
                    latest_meas = avail_data.latest('date_and_time')
                    if df.index[-1].to_pydatetime() == latest_meas.date_and_time:
                        continue
                    else:
                        df = df[df.index > pd.to_datetime(
                            latest_meas.date_and_time)]

                var_df = df[var]
                for n,row in enumerate(var_df):
                    entry = measurement_data(
                        date_and_time = var_df.index[n].to_pydatetime(),
                        value = row,
                        verified = 'V',
                        site_id = site,
                        measurement_id = var_ids[var]
                    )
                    all_entries.append(entry)
            print('')
            print('Adding {} met entries for {} at {} to the database...'.format(len(all_entries), year,site.site_name))
            measurement_data.objects.bulk_create(all_entries)
