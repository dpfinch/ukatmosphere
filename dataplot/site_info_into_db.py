import os
from datetime import datetime as dt
import pandas as pd
from dataplot.models import site_info, pollutants_details
from dataplot.DataTools import LoadData
from django.utils import timezone
import pickle

def DEFRA_AURN_sites_to_db(site_code):
    sites_filename = 'dataplot/InfoFiles/DEFRA_AURN_all_sites_info.csv'
    all_sites = pd.read_csv(sites_filename)

    site = all_sites.loc[all_sites['Site Code'] == site_code]

    print(site_code, site['Site Name'].values[0].strip())
    try:
        start_year, end_year = LoadData.get_site_year_range(site['Site Name'].values[0])

        current_year = timezone.now().year
        if end_year == current_year:
            open_site = True
            date_closed = None
        else:
            open_site = False
            try:
                date_closed = dt(end_year, 1,1)
            except TypeError:
                date_closed = None

        try:
            date_open = dt(start_year, 1,1)
        except TypeError:
            date_open = None

    except KeyError:
        start_year = None
        end_year = None
        open_site = None

    entry = site_info(
        site_type = 'DEFRA AURN',
        site_code = site_code,
        site_name = site['Site Name'].values[0].strip(),
        latitude = site['Latitude'].values[0],
        longitude = site['Longitude'].values[0],
        country = 'United Kingdom',
        address = site['Site Address'].values[0].strip(),
        region = site['Government Region'].values[0].strip(),
        environment_type = site['Environment Type'].values[0].strip(),
        EU_site_ID = site['EU Site ID'].values[0].strip(),
        UK_AIR_ID = site['UK-AIR ID'].values[0].strip(),
        site_open = open_site,
        date_open = date_open,
        date_closed = date_closed
    )

    entry.save()

    # Can loop through pollutants and add them
    all_site_obvs = Get_Site_Variables(site['Site Name'].values[0].strip())
    for obvs in all_site_obvs.keys():
        start_date_raw = all_site_obvs[obvs]['start_date']
        start_date = dt.strptime(start_date_raw, '%d/%m/%Y').date()
        end_date_raw = all_site_obvs[obvs]['start_date']
        if end_date_raw == '-':
            end_date = None
        else:
            end_date = dt.strptime(end_date_raw, '%d/%m/%Y').date()

        # new_pollutant = pollutants_details(
        #     pollutant_name = obvs,
        #     start_date = start_date,
        #     end_date = end_date
        # )
        # new_pollutant.save()
        entry.pollutants_details_set.create(
            pollutant_name = obvs,
            start_date = start_date,
            end_date = end_date)
        # entry.save()


def Get_Site_Variables(site_name):
    var_file ='dataplot/InfoFiles/All_AURN_site_variables.p'
    d = pickle.load(open(var_file,'rb'))

    pollutants = d[site_name]['Pollutants']

    return pollutants

if __name__ == '__main__':
    sites_filename = 'dataplot/InfoFiles/DEFRA_AURN_all_sites_info.csv'
    all_sites = pd.read_csv(sites_filename)

    for s in all_sites['Site Code']:
        DEFRA_AURN_sites_to_db(s)
