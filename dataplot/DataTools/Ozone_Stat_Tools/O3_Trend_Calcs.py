#==============================================================================
# Description of module here
#
#==============================================================================
# Uses modules:
# modulename
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dataplot.models import measurement_info
import numpy as np
import pandas as pd
from scipy import stats
#==============================================================================


'''
    Info about trend calculations will go here
'''

def GetTrends(df,site_info,**kwargs):
    table_data = site_info['props']['children'][2]['props']['data']
    sites = []
    env_type = []
    region = []
    for row in table_data:
        sites.append(row['Site Name'])
        env_type.append(row['Environment'])
        region.append(row['Region'])

    sites_df = pd.DataFrame({'Region':region,'Environment':env_type},
        index = sites)

    if kwargs['env_or_region'] == 'Environment Type':
        iterator = sites_df.Environment.unique()
    if kwargs['env_or_region'] == 'Region':
        iterator = sites_df.Region.unique()

    mean_r2s = []
    mean_ps = []
    std_errs = []

    for i in iterator:

        if kwargs['env_or_region'] == 'Environment Type':
            sites_subset = sites_df[sites_df.Environment == i]
        if kwargs['env_or_region'] == 'Region':
            sites_subset = sites_df[sites_df.Region == i]

        df_subset = df[sites_subset.index]
        annual_mean = df_subset.mean(axis = 1)
        annual_mean.dropna(inplace = True)

        mean_slope, intercept, r_value, mean_p_value, mean_std_err = stats.linregress(range(len(annual_mean)),
                                                                   annual_mean.values)
        mean_r2s.append(r_value ** 2)
        mean_ps.append(mean_p_value)
        std_errs.append(mean_std_err)

    trends = pd.DataFrame({kwargs['env_or_region']:iterator,'Mean Ozone Trend':mean_r2s,
        'P Value': mean_ps,'Std Error': std_errs})

    mean_slope, intercept, r_value, mean_p_value, mean_std_err = stats.linregress(range(len(df)),
                                                                df.mean(axis =1).values)
    trends.loc[len(iterator)] = ['All',r_value**2,mean_p_value,mean_std_err]

    for col in ['Mean Ozone Trend','P Value','Std Error']:
        trends[col] = trends[col].map('{:,.2f}'.format)

    return trends
