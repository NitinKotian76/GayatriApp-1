from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchQuery
from ..models import *
import logging
import pandas as pd
import json
from django.db import IntegrityError

logger = logging.getLogger(__name__)


def get_company_inst(user_id: str) -> Company:
    user = CustomUser.objects.get(id=user_id)
    return Company.objects.get(id=user.company_id)


def get_choices(table_name:str, column:str, user_id:str):
    table = TableName.objects.get(table_name=table_name, company= get_company_inst(user_id))
    dataquery = TableData.objects.filter(table_name=table).values("table_data")
    list_data = [item["table_data"][column] for item in dataquery]
    list_data = list(set(list_data))
    choices = [(item, item) for item in list_data]
    return choices

def set_data(table_name: str, data:dict, user_id:str, company_id:int=None):
    if company_id:
        company = Company.objects.get(id=company_id)
    else:
        company = get_company_inst(user_id)
    try:
        json.loads(json.dumps(data))
    except ValueError:
        logger.debug("data is not json compatible")
        return 1
    obj = TableName.objects.filter(table_name__contains=table_name, company=company.id)
    if obj.exists():
        logger.debug("table_name exists")
        table = TableName.objects.get(table_name=table_name, company=company.id)
        try:
            table_query = TableData.objects.create(
                table_data=data, table_name=table, company=company.id)
            table_query.save()
        except Exception as e:
            logger.debug("error storing data %s", e)
            return 1
    else:
        logger.debug("table does not exist")
        return 1
    logger.debug("data stored")
    return 0

def update_data(table_name: str, data:dict, user_id:str,search_term:str=None, company_id:int=None):
    if company_id:
        company = Company.objects.get(id=company_id)
    else:
        company = get_company_inst(user_id)
    try:
        json.loads(json.dumps(data))
    except ValueError:
        logger.debug("data is not json compatible")
        return 1
    obj = TableName.objects.filter(table_name__contains=table_name, company=company.id)
    if obj.exists():
        logger.debug("table_name exists")
        table = TableName.objects.get(table_name=table_name, company=company.id)
        try:
            query = get_data(table_name,user_id,search_term)
            query[0]
            if data:
                table_query = TableData.objects.update(
                    table_data=data, table_name=table, company=company.id)
                table_query.save()
            else:
                logger.debug("data not found")
                return 1
        except Exception as e:
            logger.debug("error storing data %s", e)
            return 1
    else:
        logger.debug("table does not exist")
        return 1
    logger.debug("data stored")
    return 0



def new_table(table_name: str, user_id: str, data: dict = {}) -> int:
    company = get_company_inst(user_id)
    try:
        obj = TableName.objects.create(
            table_name=table_name, company=company.id)
        TableData.objects.create(
            table_data=data, table_name=obj, company=company.id)
    except Exception as e:
        logger.debug("issue with table creation %s " % e)
        return 1
    return 0


def get_data(table_name: str, user_id: str, search_term: str = None, company_id:int=None) -> list:
    try:
        if company_id:
            company = Company.objects.get(id=company_id)
        else:
            company = get_company_inst(user_id)
        table = TableName.objects.get(table_name=table_name, company=company.id).id
        queryset = TableData.objects.filter(
            table_name=table, company=company)
        if search_term:
            queryset = queryset.filter(table_data__icontains=search_term)
        data = queryset.values().order_by("id")
        return list(data)
    except TableName.DoesNotExist:
        logger.debug("Table does not exists")
        return 1
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return 1