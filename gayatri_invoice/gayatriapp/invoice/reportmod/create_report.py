# get the database table for the user
import pandas as pd
import numpy as np
from invoice.dbmod import dbfunctions as db
from django.db.models import F, Value
import os

# NOTE: the Path for the report and invoice templates will be the same
# only the name will change

# tag_data = {
#         "demo_table": [column1, column2, column3],
#         "orderby": [column1, column2],
#         "groupby": [column1],
#         "formula": {
#             "row1": 'sum',
#             "row2": 'average',
#             },
#         "filter": {
#             'fil1': {
#                 'greaterthan': {
#                     'column': {
#                         'column1': value,
#                         'column2': value,
#                         }
#                 }
#                 'lessthan': {},
#                 'equalto': {},
#             }
#         }
# }
# this dict will contain all the information related to the tags.


def set_report_data(report_name: str, tag_data: dict, template_name: str, sheet_name: str, user_id: str):
    # map the report_name , datalist and the templateName to a json store
    data_dict = {}
    data_dict["tagdata"] = tag_data
    data_dict["temp_name"] = template_name
    data_dict["sheet_name"] = sheet_name
    data_dict["report_name"] = report_name
    table = db.set_data("report", data_dict, user_id)
    return table


class templateops():
    '''
        this function is used to process excel templates and add data in the format specified 
    '''

    def __init__(self, report_name, user_id):
        self.templatepath = os.path.join(
            BASE_DIR, 'invoice', 'ReportTemplates', 'template.xlsx')
        self.data = db.get_data("report", user_id, search_term=report_name)

    def get_template(self):
        try:
            filepath = self.templatepath + report_name
            os.path.exists(filepath)

            sheet_name = data.table_data.sheet_name
            sheet = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
            return sheet
        except Exception as e:
            logger.debug("template issue %s", e)

        # use the list to match and replace with user data retrieved from TableData
        # copy modified dataframe and make excel sheet

    def render_template(self):
        # get the data list and find the key tags in the template
        # and render the value tags
        # make different functions for redering table and single values.
        data_list = self.data.objects.annotate(
            tagdata=F("table_data__tagdata")
        ).values("tagdata")
        df = get_template()
        loc_dict = {}
        # find the loc of the tags in the template
        for tag in data_list[0]["tagdata"].keys():
            for i in df.len()-1:
                a = df[i].filter("{{"+tag+"}}").dropna().to_dict()
                if a.values():
                    loc_dict["tag"] = [i, a.keys()]

        # prepare the type of data to be rendered
        for tag in loc_dict:
            match data_list[0]["tagdata"][tag].values():
                case single:
                    data
                case table:
