# TODO: create a function for storing the data in lists
# divide the list by the field limit and store the data in
# numbered unique keys.
from django.core.paginator import Paginator
from ..models import *
import json
import logging

logger = logging.getLogger(__name__)


def set_data(table_name, data):
    # NOTE: get the table data as a row of values in json
    # expect json values as data
    try:
        json.loads(data)
        row_limit = 1000
        obj = Table.objects.filter(table_name__contains=table_name)
        if obj.exists():

            table_query = Table.objects.get(table_name=table_name)

            if len(table_query.table_data) < 1000:
                table_query.table_data.append(data)
                table_query.save()
            else:
                try:
                    Table.objects.get(table_name=table_name)
                except:
                    # do something else
                Table.objects.create_or_update(table_name=table_name, table_data=data, company)

    except ValueError:
        logger.debug("data is not json compatible")
        return 0


def get_data(table_name):
    table_query = Table.objects.get(table_name=table_name)
    return table_query.table_data
