# get the database table for the user
import pandas as pd
import numpy as np
from invoice.models import TableData, TableName


def set_report_format():

    # TODO: store the received dict in tableData with the report name
    # and template name added in
    # store template in the server filesystem
    pass


def get_template():
    # TODO: check if the template exists in the server filesystem
    sheet = pd.read_excel(
        template, sheet_name=sheet_name, header=None)


class get_data():

    # TODO: get the data from the database as a queryset and filter the elements needed
    # or use the n no of querysets as a table
    # tag_list = TableData.objects.get(table_name=report_name).values("table_data")

    def get_oneItem(column_name, identifier):
        pass

    def get_queryset():
        pass


def process_report(template: str, sheet_name: str, data_list: list):
    for tag, data in data_list:
        results = (sheet == "{{"+tag+"}}")
        location = list(zip(*results.to_numpy().nonzero()))
        for row, column in location:
            packing.at[row, column] = data
    # use the list to match and replace with user data retrieved from TableData
    # copy modified dataframe and make excel sheet
