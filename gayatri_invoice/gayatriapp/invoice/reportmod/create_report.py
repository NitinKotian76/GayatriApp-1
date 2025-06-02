# get the database table for the user
import pandas as pd
import numpy as np
from invoice.models import TableData, TableName


def set_report_format():
    # TODO: store the received dict in tableData with the report name
    # and template name added in
    # store template in the server filesystem


def get_template():
    # TODO: check if the template exists in the server filesystem


def get_data():
    tag_list = TableData.objects.get(table_name=).values("table_data")


def process_report(template: str, sheet_name: str, data_list: list):
    sheet = pd.read_excel(
        template, sheet_name=sheet_name, header=None)
    for tag, data in data_list:
        results = (sheet == "{{"+tag+"}}")
        location = list(zip(*results.to_numpy().nonzero()))
        for row, column in location:
            packing.at[row, column] = data
    # use the list to match and replace with user data retrieved from TableData
    # copy modified dataframe and make excel sheet
