# get the database table for the user
import pandas as pd
import numpy as np

# get the report template


def get_template():
    pass
    # return dataframe


def get_data():
    pass


def tag_search():
    results = (packing == "{{data}}")
    location = list(zip(*results.to_numpy().nonzero()))
    for row, column in location:
        packing.at[row, column] = "data added"
    # search tags for dataframe


def process_data():
    packing = pd.read_excel("ExportInvoiceB.xls", sheet_name='PCK')
    # copy modified dataframe and make excel sheet
