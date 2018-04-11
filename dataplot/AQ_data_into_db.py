import os
from datetime import datetime as dt
import pandas as pd
from dataplot.models import site_info, pollutants_details, measurement_info,measurement_data
from dataplot.DataTools import LoadData
from django.utils import timezone
import pickle

### Need to put measurement data into database
def DEFRA_AURN_data_to_db():
    ## Trial database first - with a small amount of test data.

    ## TEST DATA:
    df = LoadData.Get_AURN_data('Aberdeen', [2018,2018])
    ignore_list = ['Date', 'Time', 'time', 'Status']
    site_code = 'ABD'

    for col in df.columns:
        if col in ignore_list:
            continue
        else:
            chemical_formula = Get_Chemical_Formula(col)
            measurement_name = 'DEFRA_AURN_%s' % chemical_formula
            for n in range(100):
                x = df[col][n]
                entry = measurement_data(
                    date_and_time = df.index[n],
                    value = x,
                    verified = 'U', # Need to get this sorted
                )

                if site_info.objects.filter(site_code = site_code).exists():
                    entry.site_id = site_info.objects.filter(site_code = site_code)[0]
                    # Need an else....
                if measurement_info.objects.filter(measurement_name = measurement_name).exists():
                    entry.measurement_id = measurement_info.objects.filter(measurement_name = measurement_name)[0]
                else:
                    meas_info = measurement_info(
                        variable_name = col,
                        unit = 'ugm-3', # TODO make sure these units are corrected
                        chemical_formula = chemical_formula,
                        measurement_name = measurement_name
                    )
                    meas_info.save()
                    entry.measurement_id = meas_info
                entry.save()

def Get_Chemical_Formula(chemical_name):
    chems = pd.read_csv('dataplot/InfoFiles/Chemical_Formula.csv', dtype = str).rename(columns=lambda x: x.strip())
    for col in chems.columns:
        chems[col] = chems[col].str.strip()

    # Take out any sub html commands
    chemical_name = chemical_name.replace('<sub>', '')
    chemical_name = chemical_name.replace('</sub>', '')

    chemical = chems.loc[chems['Variable Name'].str.lower() == chemical_name.strip().lower()]


    return chemical['Variable Formula'].values[0]
