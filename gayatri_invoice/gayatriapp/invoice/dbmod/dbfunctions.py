"""
Database functions for managing table data and operations.

This module provides functions for creating, updating, and retrieving data from
custom tables in the database. It handles JSON data storage and retrieval,
with company-specific data isolation.
"""

from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchQuery
from ..models import *
import logging
import pandas as pd
import json
from django.db import IntegrityError

logger = logging.getLogger(__name__)


def set_data(table_name: str, data, user_id):
    """
    Store data in an existing table.

    Args:
        table_name (str): Name of the table to store data in
        data: JSON-compatible data to store
        user_id: ID of the user performing the operation

    Returns:
        int: 0 on success, 1 on failure
    """
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
            return 1
    else:
        logger.debug("table does not exist")
        return 1
    return 0


def new_table(table_name: str, user_id, data={}):
    """
    Create a new table and store initial data.

    Args:
        table_name (str): Name for the new table
        user_id: ID of the user creating the table
        data (dict, optional): Initial data to store in the table

    Returns:
        int: 0 on success
    """
    user = CustomUser.objects.get(id=user_id)
    company = Company.objects.get(id=user.company_id)
    obj = TableName.objects.create(
        table_name=table_name, company=company)
    TableData.objects.create(table_data=data, table_name=obj, company=company)
    return 0


def get_datarow_q(table_name: str, user_id: str):
    """
    Retrieve all data rows from a specific table.

    Args:
        table_name (str): Name of the table to query
        user_id (str): ID of the user requesting the data

    Returns:
        list: List of dictionaries containing table data, or 0 on error
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        logger.debug(user)
        company_id = Company.objects.get(id=user.company_id).id
        logger.debug(company_id)
        table = TableName.objects.get(table_name=table_name).id
        logger.debug(table)
        data = TableData.objects.filter(
            table_name=table, company=company_id).values("table_data")

        return list(data)
    except TableName.DoesNotExist:
        logger.debug("Table does not exists")
        return 1
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return 1


def get_datacolumn(table_name: str, column_name: str, user_id: str):
    """
    Retrieve a specific column of data from a table.

    Args:
        table_name (str): Name of the table to query
        column_name (str): Name of the column to retrieve
        user_id (str): ID of the user requesting the data

    Returns:
        pandas.Series: Column data, or 0 on error
    """
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
        return 1


def search(data, user_id, table_name=None):
    """
    Search for data in TableData based on search term and optional table name.

    Args:
        data (str): Search term to look for in table_data
        user_id (int): ID of the user performing the search
        table_name (str, optional): Name of table to search in. If None, searches all tables.

    Returns:
        dict: Contains count of results, primary keys, and queryset
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        company_id = Company.objects.get(id=user.company_id).id

        # Build base query
        if table_name:
            namequery = TableName.objects.filter(
                table_name__icontains=table_name,
                company_id=company_id
            )
            if not namequery.exists():
                return {"count": 0, "pk": [], "queryset": []}

            dataquery = TableData.objects.filter(
                table_data__icontains=data,
                table_name=namequery,
                company_id=company_id
            ).values_list()
        else:
            dataquery = TableData.objects.filter(
                table_data__icontains=data,
                company_id=company_id
            ).values_list()

        if not dataquery.exists():
            return {"count": 0, "pk": [], "queryset": []}

        # Convert queryset to lists
        results = list(dataquery)
        pks = [row[0] for row in results]
        queryset = [row[1] for row in results]

        return {
            "count": len(results),
            "pk": pks,
            "queryset": queryset
        }

    except CustomUser.DoesNotExist:
        logger.error(f"User with ID {user_id} not found")
        return {"count": 0, "pk": [], "queryset": []}
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        return {"count": 0, "pk": [], "queryset": []}
