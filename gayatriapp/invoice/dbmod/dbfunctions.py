# TODO: create a function for storing the data in lists
# divide the list by the field limit and store the data in
# numbered unique keys.
from django.core.paginator import Paginator
from ..models import *
import json
import logging

logger = logging.getLogger(__name__)
# TODO: get company instance from a global constant


def set_data(table_name, data, user_id):
    # NOTE: get the table data as a row of values in json
    # expect json values as data
    row_limit = 1000
    # user = CustomUser.objects.get(user_emp_code=user_id)
    company = Company.objects.get(id=user_id.company_id)

    try:
        json.loads(data)
        obj = Table.objects.filter(table_name__contains=table_name)
        # NOTE: can improve performance here
        if obj.exists():
            num = obj.count() - 1
            table_head = table_name + "_" + str(num)
            table_obj = Table.objects.filter(table_name__contains=table_head)
            if table_obj.exists():
                logger.debug("object exists")
                table_query = Table.objects.get(table_name=table_head)
            else:
                table_query = Table.objects.create(
                    table_name=table_head, table_data=data, company=company)

            if len(table_query.table_data) < row_limit:
                table_query.table_data.append(data)
                table_query.save(update_fields=["table_data"])
        else:  # create new table
            Table.objects.create(table_name=table_name,
                                 table_data=data, company=company)

    except ValueError:
        logger.debug("data is not json compatible")
        return 0


def get_data(table_name):
    table_query = Table.objects.get(table_name=table_name)
    return table_query.table_data
