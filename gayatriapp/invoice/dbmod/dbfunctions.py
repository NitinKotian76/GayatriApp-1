# TODO: create a function for storing the data in lists
# divide the list by the field limit and store the data in
# numbered unique keys.
from django.core.paginator import Paginator
from ..models import *


def set_data(table_name, data):
    # get the data as a list and append to already existing json
    # or add new add_data
    row_limit = 1000
    table_query = Table.objects.get(table_name=table_name)

    if len(table_query.table_data) < 1000:
        table_query.table_data.append(data)
        table_query.save()
    else:
        tab
        Table.objects.create_or_update()


def get_data(table_name):
    table_query = Table.objects.get(table_name=table_name)
    return table_query.table_data
