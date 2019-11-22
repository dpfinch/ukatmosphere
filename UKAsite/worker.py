import schedule
from dataplot.models import *
from dataplot import AQ_data_into_db as db
from datetime import datetime as dt
#### Need to schedule jobs to load new data into database.
#### Start it at once per day. Possible to do more frequent later.

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

if __name__ == '__main__':
    ## Get the latest data - set this to 18:00 - for no particular reason
    # schedule.every().day.at("18:00").do(latest_AURN_station_data)
    #
    # ## Check the verified data every monday at 01:00 - again no particular reason
    # schedule.every().monday.at("01:00").do(latest_AURN_station_data)
    #
    #
    # while True:
    #
    #     schedule.run_pending()
    print('Nothing happening yet')
