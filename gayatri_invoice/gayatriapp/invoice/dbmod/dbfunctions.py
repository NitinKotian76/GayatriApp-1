# TODO: create a function for storing the data in lists
# divide the list by the field limit and store the data in
# numbered unique keys.
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchQuery
from ..models import *
import logging
import pandas as pd
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
        return 1
    obj = TableName.objects.filter(table_name__contains=table_name)
    if obj.exists():
        logger.debug("table_name exists")
        table = TableName.objects.get(table_name=table_name)
        try:
            table_query = TableData.objects.create(
                table_data=data, table_name=table, company=company)
            table_query.save()
        except Exception as e:
            logger.debug("data duplicate %s", e)
            # NOTE: have to choose either the data be similar in json level or the model level
            return 1
    else:  # create new table
        logger.debug("table does not exist")
        return 1
    return 0


def new_table(table_name: str, user_id, data={}):
    user = CustomUser.objects.get(id=user_id)
    company = Company.objects.get(id=user.company_id)
    obj = TableName.objects.create(
        table_name=table_name, company=company)
    TableData.objects.create(table_data=data, table_name=obj, company=company)
    return 1


def get_datarow_q(table_name: str, user_id: str):
    # NOTE: this is only being used for getting TableData json column
    # all data stored in the application is stored in TableData
    try:
        user = CustomUser.objects.get(id=user_id)
        logger.debug(user)
        company_id = Company.objects.get(id=user.company_id).id
        logger.debug(company_id)
        table = TableName.objects.get(table_name=table_name).id
        logger.debug(table)
        data = TableData.objects.filter(
            table_name=table, company=company_id).values("table_data")

        # Convert QuerySet to list of dictionaries
        return list(data)
    except TableName.DoesNotExist:
        logger.debug("Table does not exists")
        return 0
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
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


def search(data, user_id, table_name=None):
    # TODO: search the hash in the search index and output related table num and entry no
    pk = []
    data_dict = {}
    queryset = []
    count = None
    user = CustomUser.objects.get(id=user_id)
    company_id = Company.objects.get(id=user.company_id).id
    if table_name:
        namequery = TableName.objects.filter(
            table_name__icontains=table_name, company_id=company_id)
        if namequery.exists():
            dataquery = TableData.objects.filter(
                table_data__icontains=data, table_name=namequery, company_id=company_id).values_list()
    else:
        dataquery = TableData.objects.filter(
            table_data__icontains=data, company_id=company_id).values_list()

    if dataquery.exists():
        count = len(dataquery)
        for i in 0, count:
            pk.append(dataquery[i][0])

        for i in 0, count:
            queryset.append(dataquery[i][1])

    data_dict["count"] = count
    data_dict["pk"] = pk
    data_dict["queryset"] = queryset
    return data_dict
