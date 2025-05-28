# TODO: create a function for storing the data in lists
# divide the list by the field limit and store the data in
# numbered unique keys.
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchQuery
from ..models import *
import logging
import json
from django.db import IntegrityError
logger = logging.getLogger(__name__)
# TODO: get company instance from a global constant


def set_data(table_name, data, user_id):
    # NOTE: the table name table and the table data table is different

    user = CustomUser.objects.get(id=user_id)
    company = Company.objects.get(id=user.company_id)
    try:
        json.loads(json.dumps(data))
    except ValueError:
        logger.debug("data is not json compatible")
        return 0
    obj = TableName.objects.filter(table_name__contains=table_name)
    if obj.exists():
        logger.debug("table_name exists")
        table = TableName.objects.get(table_name=table_name)
        try:
            table_query = TableData.objects.create(
                table_data=data, table_name=table)
            table_query.save()
        except IntegrityError as e:
            # TODO: send message to user the data is duplicate
            logger.debug("data duplicate")
            return 0
    else:  # create new table
        obj = TableName.objects.create(
            table_name=table_name, company=company)
        TableData.objects.create(table_data=data, table_name=obj)
    return 1


def get_data(table_name):  # TODO: need more granularity on the data sent
    obj = TableName.objects.get(table_name=table_name)
    return obj.table_data


def search(data, table_name):
    # TODO: search the hash in the search index and output related table num and entry no
    namequery = TableName.objects.filter(table_name__contains=table_name)
    if namequery.exists():
        dataquery = TableData.objects.filter(
            table_data__contains=data, table_name=namequery)
