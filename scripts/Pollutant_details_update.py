# Update the start and end dates of the pollutant details
# Database had wrong entry into due to small type years ago...

from dataplot.models import *
import pickle
from datetime import datetime as dt
print('Update Pollutant Details Script')
print('Updating Pollutant Details...')

all_pollutants = pollutants_details.objects.all()

var_file ='dataplot/InfoFiles/All_AURN_site_variables.p'
d = pickle.load(open(var_file,'rb'))

for poll in all_pollutants:
    if poll.pollutant_name.split()[0] == 'Modelled':
        continue
    if poll.pollutant_name.split()[-1] in ['Temperature','measured','Preasure','Speed','Direction']:
        continue

    if poll.start_date != poll.end_date:
        continue

    # Have already processed Auchencorth Moss but should skip still checking it
    if poll.relevant_site.site_name[0].lower() < 'y' :
        continue
    # in ['Brighton Roadside PM10','Auchencorth Moss',
    #     'Bournemouth', 'Brighton Preston Park','Chilbolton Observatory']:
    #     continue
    print('Updating {} for {}'.format(poll.pollutant_name,poll.relevant_site.site_name))

    filters = {}
    if poll.pollutant_name.split()[0] in ['PM10','PM2.5','Volatile','Non-volatile']:
        old_name = poll.pollutant_name
        for name_part in old_name.split():
            if name_part == 'PM2.5':
                new_name = old_name.replace('PM2.5','PM<sub>2.5</sub>')
            if name_part == 'PM10':
                new_name = old_name.replace('PM10','PM<sub>10</sub>')
        filters['measurement_id__variable_name'] = new_name
    else:
        filters['measurement_id__variable_name'] = poll.pollutant_name
    filters['site_id'] = poll.relevant_site

    pollutant_call = measurement_data.objects.filter(**filters)
    try:
        first_occurance = pollutant_call.first().date_and_time
    except AttributeError:
        continue

    site_pollutants = d[poll.relevant_site.site_name]['Pollutants']
    specific_pollutant = site_pollutants[poll.pollutant_name]

    end_date_raw = specific_pollutant['end_date']
    if end_date_raw == '-':
        end_date = None
    else:
        end_date = dt.strptime(end_date_raw, '%d/%m/%Y').date()

    poll.start_date = first_occurance.date()
    poll.end_date = end_date

    poll.save()
