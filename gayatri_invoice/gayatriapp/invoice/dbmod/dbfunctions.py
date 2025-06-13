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


def set_data(table_name: str, data, user_id):
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
        logger.debug("table does not exist")
        return 0
    return 1


def new_table(table_name: str, user_id, data=None):
    user = CustomUser.objects.get(id=user_id)
    company = Company.objects.get(id=user.company_id)
    obj = TableName.objects.create(
        table_name=table_name, company=company)
    TableData.objects.create(table_data=data, table_name=obj)
    return 1


def get_datarow_q(table_name: str, user_id: str):
    # NOTE: this is only being used for getting TableData json column
    try:
        user = CustomUser.objects.get(id=user_id)
        logger.debug(user)
        company_id = Company.objects.get(id=user.company_id).id
        logger.debug(company_id)
        table = TableName.objects.get(table_name=table_name).id
        logger.debug(table)
        data = TableData.objects.filter(
            table_name=table, company=company_id).values("table_data")

        return data
    except:
        logger.debug("Table does not exists")
        return 0


def get_datacolumn(table_name: str, column_name: str, user_id: str):
    try:
        user = CustomUser.objects.get(id=user_id)
        company_id = Company.objects.get(id=user.company_id).id
        table = TableName.objects.get(table_name=table_name)
        query = TableData.objects.filter(
            table_name=table, company=company_id).values("table_data")
        data = pd.json_normalize(query)[column_name]

        return data
    except:
        logger.debug("Table does not exists")
        return 0


def search(data, table_name: str):
    # TODO: search the hash in the search index and output related table num and entry no
    namequery = TableName.objects.filter(table_name__contains=table_name)
    if namequery.exists():
        dataquery = TableData.objects.filter(
            table_data__contains=data, table_name=namequery)
