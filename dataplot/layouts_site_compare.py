import dash_core_components as dcc
import dash_html_components as html
import dash_table
from .server import app
from dash.dependencies import Output, Input
from dataplot.DataTools import LoadData
from dataplot.DataTools import TidyData
import pandas as pd


def Site_Comparison_Table():

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

    page_layout = html.Div(id = 'full_page_container', children =
    [html.Div(className = 'page-header', children = [
        html.Div(id = 'home-logo-holder', children = [html.A(id = 'home-logo', href="/")]),
        html.Div(id = 'page-header-holder', children = [html.A('UK Atmosphere',id = "page-header-text", href = "/")]),
    ]),
    html.Div(className = 'page-body',children = [
    html.Div(className = 'tool_explainer', children = [
    html.P('This is the development page for the site comparions table view.'),
    html.P('** Please Note **'),
    html.P('This page is still in the development stage.'),
    html.P('Currently only limited data is available and therefore the data shown is not up to date')
    ]), # End of the tool explainer brackets

    dash_table.DataTable(
    id = 'Table',
    columns = [{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    )

    ]), # End of the page body brackets

    ]) # End of the page layout brackets

    return page_layout
