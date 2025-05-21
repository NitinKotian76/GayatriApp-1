# get the database table for the user
import pandas as pd
import numpy as np

# get the report template
packing = pd.read_excel("ExportInvoiceB.xls", sheet_name='PCK')
results = (packing == "{{data}}")
location = list(zip(*results.to_numpy().nonzero()))
for row, column in location:
    packing.at[row, column] = "data added"
