# get the database table for the user
import pandas as pd
import numpy as np
from invoice.dbmod import dbfunctions as db

# NOTE: the Path for the report and invoice templates will be the same
# only the name will change


def set_report_data(report_name: str, data_list: dict, template_name: str, sheet_name: str, user_id):
    # map the report_name , datalist and the templateName to a json store
    data_dict = []
    data_dict["datalist"] = data_list
    data_dict["temp_name"] = template_name
    data_dict["sheet_name"] = sheet_name
    data_dict["report_name"] = report_name
    table = db.set_data("report", data_dict, user_id)
    return table


def get_template(report_name: str, user_id: str):
    # TODO: check if the template exists in the server filesystem
    data = db.get_data("report", user_id, report_name)
    template = data.table_data.template_name
    sheet_name = data.table_data.sheet_name
    sheet = pd.read_excel(template, sheet_name=sheet_name, header=None)
    return sheet

def get_data(tag: str, user_id: str):
    data = db.get_data("report", user_id, tag)
def process_report(report_name: str, user_id: str):
    sheet = get_template(report_name, user_id)
    
    for tag, data in data_list:
        results = (sheet == "{{"+tag+"}}")
        location = list(zip(*results.to_numpy().nonzero()))
        for row, column in location:
            packing.at[row, column] = data
    # use the list to match and replace with user data retrieved from TableData
    # copy modified dataframe and make excel sheet
