# get the database table for the user
import pandas as pd
import numpy as np
from invoice.dbmod import dbfunctions as db

# NOTE: the Path for the report and invoice templates will be the same
# only the name will change


def set_report_data(report_name: str, data_list: dict, template_name: str, user_id):
    # map the report_name , datalist and the templateName to a json store
    data_dict = []
    data_dict["datalist"] = data_list
    data_dict["temp_name"] = template_name
    data_dict["report_name"] = report_name
    table = db.set_data("report", data_dict, user_id)
    return table


def get_template(report_name: str):
    # TODO: check if the template exists in the server filesystem
    db.get_datarow_q("report", "")
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
