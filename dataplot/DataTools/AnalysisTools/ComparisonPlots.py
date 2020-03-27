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

    # Processing week comparison starts here:
    try:
        week_to_compare = int(kwargs['comp_week'])
    except ValueError:
        return 'Week not a valid number'
    if week_to_compare > 53 or week_to_compare < 1:
        return "{} is not valid week number (it should be between 1-52)".format(week_to_compare)

    df_week = df_col[df_col.index.weekofyear == week_to_compare]

    try:
        year_to_compare = int(kwargs['comp_year'])
    except ValueError:
        return 'Year not a valid number'
    if year_to_compare > max(df_week.index.year):
        return "No data for that date yet."
    if year_to_compare < min(df_week.index.year):
        return "This site doesn't have data going back that far"

    current_week = df_week[df_week.index.year == year_to_compare]
    other_weeks = df_week[df_week.index.year != year_to_compare]

    if pd.Timestamp(current_week.index.year[0],2,29) in current_week.index:
        return "We can't currently process weeks with leap days in them - we're working on it!"

    other_year_weeks = []
    for year in other_weeks.index.year.unique():
        other_year_weeks.append(
            other_weeks[other_weeks.index.year == year].reset_index(drop = True))

    transformed_weeks = pd.concat(other_year_weeks, axis = 1)
    current_week = current_week.resample('H').mean()

    mean_weeks = transformed_weeks.mean(axis = 1)
    mean_weeks.index = current_week.index
    std_weeks = transformed_weeks.std(axis = 1)
    std_weeks.index = current_week.index

    week_name = 'Weeks' # Need to address this

    all_plots = []
    all_plots.append(go.Scatter(
        y = mean_weeks.values,
        x = mean_weeks.index,
        name = week_name,
        mode = 'lines',
    ))
    y_upper = mean_weeks.values + std_weeks.values
    y_lower = mean_weeks.values - std_weeks.values

    x = mean_weeks.index.append(mean_weeks.index[::-1])
    y = np.concatenate([y_upper,y_lower[::-1]])

    all_plots.append(go.Scatter(
        y = y,
        x = x,
        fill = 'tozerox',
        name = week_name + 'std',
        # mode = 'lines',
    ))

    all_plots.append(go.Scatter(
        y = current_week.values,
        x = current_week.index,
        name = week_name,
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
