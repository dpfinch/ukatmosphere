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
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
from calendar import monthrange
#==============================================================================


'''
    Info about Comparison plots will go here
'''
def CompareWeeks(df, **kwargs):

    if type(kwargs['variable_options']) == str:
        df_col = df[kwargs['variable_options']]
    else:
        df_col = df[kwargs['variable_options'][0]]

    if df_col.name.split(' ')[0][:2] == 'PM':
        df_col.name = df_col.name.split(' ')[0]

    start_date = dt.strptime(kwargs['start_date'],'%Y-%m-%d')
    end_date = dt.strptime(kwargs['end_date'],'%Y-%m-%d')
    if start_date.year != end_date.year:
        return 'Comparison dates cannot stradle different years'
    comp_year = start_date.year

    if df_col.index.year.min() + 6 > dt.now().year:
        return "Not enough data at this site to make a comparison"
    if start_date.year < df_col.index.year.min() + 6:
        return "Not enough data with this date selection to make a comparison"

    df_col = df_col[(df_col.index.year > start_date.year - 6) & (df_col.index.year <= end_date.year)]
    df_col = df_col.resample('H').mean()
    df_col = df_col[~((df_col.index.month == 2) & (df_col.index.day == 29))]
    start_doy = start_date.timetuple().tm_yday
    end_doy = end_date.timetuple().tm_yday

    current_year = df_col[df_col.index.year == comp_year]
    other_years = df_col[df_col.index.year != comp_year]

    date_range = pd.date_range('2020-1-1','2020-12-31 23:00:00', freq = 'H')
    date_range = date_range[~((date_range.month == 2) & (date_range.day == 29))]

    clim = []
    for year in other_years.index.year.unique():
        clim.append(other_years[other_years.index.year == year].reset_index(drop = True))
    clim = pd.concat(clim,axis = 1)
    clim.index = date_range
    clim = clim[(clim.index >= start_date) & (clim.index <= end_date)]
    mean_weeks = clim.mean(axis = 1)
    median_weeks = clim.median(axis = 1)

    # comp_dates = df_col[(df_col.index.dayofyear >= start_doy) & (df_col.index.dayofyear < end_doy)]
    # comp_dates = df_col[(df_col.index.dayofyear >= start_doy) & (df_col.index.day >= start_date.day)]
    # comp_dates = comp_dates_temp[(comp_dates_temp.index.month <= end_date.month) & (comp_dates_temp.index.day <= end_date.day)]

    current_week = current_year[(current_year.index >= start_date) & (current_year.index <= end_date)]

    # mean_weeks = clim_mean[(clim_mean.index >= start_date) & (clim_mean.index <= end_date)]
    # median_weeks = clim_median[(clim_median.index >= start_date) & (clim_median.index <= end_date)]

    median_weeks.loc[current_week.index]
    median_weeks.loc[current_week.index]

    if pd.Timestamp(current_week.index.year[0],2,29) in current_week.index:
        return "We can't currently process weeks with leap days in them - we're working on it!"

    # other_year_weeks = []
    # for year in other_weeks.index.year.unique():
    #     other_year_weeks.append(
    #         other_weeks[other_weeks.index.year == year].reset_index(drop = True))
    #
    # transformed_weeks = pd.concat(other_year_weeks, axis = 1)
    # current_week = current_week.resample('H').mean()
    # # print(current_week.shape)
    # # print(transformed_weeks.shape)
    #
    # mean_weeks = transformed_weeks.mean(axis = 1)
    # median_weeks = transformed_weeks.median(axis = 1)
    # mean_weeks.index = current_week.index
    # median_weeks.index = current_week.index
    min_weeks = clim.min(axis = 1)#.rolling(24,min_periods = 1).mean()
    max_weeks = clim.max(axis = 1)#.rolling(24,min_periods = 1).mean()

    all_plots = []
    # y_upper = mean_weeks.values + std_weeks.values
    # y_lower = mean_weeks.values - std_weeks.values

    x = mean_weeks.index.append(mean_weeks.index[::-1])
    y = np.concatenate([min_weeks.values,max_weeks.values[::-1]])

    all_plots.append(go.Scatter(
        y = y,
        x = x,
        fill = 'tozerox',
        line = {'color':'rgba(0,100,80,0.2)'},
        fillcolor='rgba(0,100,80,0.15)',
        name = '5 Year Range',
        # mode = 'lines',
    ))
    all_plots.append(go.Scatter(
        y = mean_weeks.values,
        x = mean_weeks.index,
        name = '5 Year Mean',
        mode = 'lines',
        line = {'color':'rgba(0,100,80,1)'},
    ))

    if kwargs['show_median']:
        all_plots.append(go.Scatter(
            y = median_weeks.values,
            x = median_weeks.index,
            name = 'Previous 5 year median',
            mode = 'lines',
            line = {'color':'rgba(0,100,80,1)','dash' : 'dash'},
        ))

    actual_end = end_date - timedelta(days = 1)
    date_labels = '{} to {}'.format(start_date.strftime('%d/%m/%y'),actual_end.strftime('%d/%m/%y') )

    all_plots.append(go.Scatter(
        y = current_week.values,
        x = current_week.index,
        # name = date_labels,
        name = 'This Year',
        mode = 'lines',
        line = {'color':'rgba(214,108,43,1)'},
    ))

    xtitle = kwargs['xtitle']
    ytitle = kwargs['ytitle']
    plot_title = kwargs['title']

    plot_layout = go.Layout(
    title = dict(text = plot_title, x = 0.1, y = 0.9),
    xaxis = dict(title = xtitle, range = [current_week.index[0],current_week.index[-1]]),
    yaxis = dict(title = ytitle),
    # legend_orientation="h",
    # legend = dict(x = 1, y = 1,bordercolor="Black", borderwidth=2),
    images=[dict(
        source="assets/all_logos.jpeg",
        xref="paper", yref="paper",
        x=1, y=1,
        sizex=0.42, sizey=0.42,
        xanchor="right", yanchor="bottom"
      ),])

    config = {"toImageButtonOptions": {"width": None, "height": None, "scale":4}}

    plot = dcc.Graph(
        id ='WeekComparePlot',
        figure = {
            'data':all_plots,
            'layout':plot_layout
            },
        config = config
    )

    return plot

def CompareMonths(df, **kwargs):
    if type(kwargs['variable_options']) == str:
        df_col = df[kwargs['variable_options']]
    else:
        df_col = df[kwargs['variable_options'][0]]

    if df_col.name.split(' ')[0][:2] == 'PM':
        df_col.name = df_col.name.split(' ')[0]

    # Processing month comparison starts here:
    try:
        month_to_compare = int(kwargs['comp_month'])
    except ValueError:
        return 'Month not a valid number'
    if month_to_compare > 12 or month_to_compare < 1:
        return "{} isn't a valid month number (it should be between 1 - 12)".format(month_to_compare)

    df_col = df_col.resample('D').mean()
    month_df = df_col[df_col.index.month == month_to_compare]

    try:
        year_to_compare = int(kwargs['comp_year'])
    except ValueError:
        return 'Year not a valid number'
    if year_to_compare > max(month_df.index.year):
        return "No data for that date yet."
    if year_to_compare < min(month_df.index.year):
        return "This site doesn't have data going back that far"

    days_in_month = monthrange(year_to_compare,month_to_compare)[1]
    all_month_days = pd.date_range(pd.Timestamp(year_to_compare, month_to_compare,1),
        pd.Timestamp(year_to_compare,month_to_compare,days_in_month), freq = 'D')

    # Need a lot of crap to fill in any days that havent happened yet!
    full_month = pd.DataFrame(np.zeros(len(all_month_days)),index = all_month_days)
    current_month = month_df[month_df.index.year == year_to_compare]

    current_month = pd.concat([full_month, current_month], axis = 1)
    current_month = current_month[df_col.name]


    other_months = month_df[month_df.index.year != year_to_compare]
    mean_months = other_months.groupby(other_months.index.day).mean()
    std_months = other_months.groupby(other_months.index.day).std()

    all_plots = []

    year_name = str(year_to_compare)

    all_plots.append(go.Scatter(
        y = mean_months.values,
        x = current_month.index,
        name = 'All Years',
        mode = 'lines',
    ))
    y_upper = mean_months.values + std_months.values
    y_lower = mean_months.values - std_months.values

    x = current_month.index.append(current_month.index[::-1])
    y = np.concatenate([y_upper,y_lower[::-1]])

    all_plots.append(go.Scatter(
        y = y,
        x = x,
        fill = 'tozerox',
        name = year_name + 'std',
        # mode = 'lines',
    ))

    all_plots.append(go.Scatter(
        y = current_month.values,
        x = current_month.index,
        name = year_name,
        mode = 'lines',
    ))

    xtitle = kwargs['xtitle']
    ytitle = kwargs['ytitle']
    plot_title = kwargs['title']

    plot_layout = go.Layout(
    title = plot_title,
    xaxis = dict(title = xtitle),
    yaxis = dict(title = ytitle),
    images=[dict(
        source="assets/all_logos.jpeg",
        xref="paper", yref="paper",
        x=1, y=1,
        sizex=0.42, sizey=0.42,
        xanchor="right", yanchor="bottom"
      ),])

    config = {"toImageButtonOptions": {"width": None, "height": None, "scale":2}}

    plot = dcc.Graph(
        id ='WeekComparePlot',
        figure = {
            'data':all_plots,
            'layout':plot_layout
            },
        config = config
    )
    return plot

def CompareYears(df, **kwargs):
    # if type(kwargs['variable_options']) == str:
    #     df_col = df[kwargs['variable_options']]
    # else:
    #     df_col = df[kwargs['variable_options'][0]]
    #
    # if df_col.name.split(' ')[0][:2] == 'PM':
    #     df_col.name = df_col.name.split(' ')[0]
    #
    # # Processing year comparison starts here:
    # try:
    #     year_to_compare = int(kwargs['comp_year'])
    # except ValueError:
    #     return 'Year not a valid number'
    # if year_to_compare > dt.now().year:
    #     return "That year hasn't happened yet"
    # if year_to_compare < min(df_col.index.year):
    #     return "This site doesn't have data going back that far"
    #
    # xtitle = kwargs['xtitle']
    # ytitle = kwargs['ytitle']
    # plot_title = kwargs['title']
    #
    # plot_layout = go.Layout(
    # title = plot_title,
    # xaxis = dict(title = xtitle),
    # yaxis = dict(title = ytitle),
    # images=[dict(
    #     source="assets/all_logos.jpeg",
    #     xref="paper", yref="paper",
    #     x=1, y=1,
    #     sizex=0.42, sizey=0.42,
    #     xanchor="right", yanchor="bottom"
    #   ),])
    #
    # config = {"toImageButtonOptions": {"width": None, "height": None, "scale":2}}
    #
    # plot = dcc.Graph(
    #     id ='WeekComparePlot',
    #     figure = {
    #         'data':all_plots,
    #         'layout':plot_layout
    #         },
    #     config = config
    # )
    return 'Year Plots being developed'
## ============================================================================
## END OF PROGAM
## ============================================================================
