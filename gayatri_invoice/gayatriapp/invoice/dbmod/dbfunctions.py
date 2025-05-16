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
    user = CustomUser.objects.get(id=user_id)
    company = Company.objects.get(id=user.company_id)
    data_list = []

    try:
        logger.debug(type(data))
        json.loads(json.dumps(data))
        obj = Table.objects.filter(table_name__contains=table_name)
        data_list.append(data)
        # NOTE: can improve performance here
        if obj.exists():
            logger.debug("table_name exists")
            num = obj.count() - 1
            table_head = table_name + "_" + str(num)
            table_obj = Table.objects.filter(table_name__contains=table_head)
            if table_obj.exists():  # obj exists add data
                logger.debug("table num exists")
                table_query = Table.objects.get(
                    table_name=table_head)  # get table query for the no
                if len(table_query.table_data) < row_limit:  # add data if space is there
                    table_query.table_data.append(data)
                    table_query.save(update_fields=["table_data"])
                else:
                    logger.debug("storage full adding table num")
                    table_head = table_name + "_" + str(num+1)
                    table_query = Table.objects.create(
                        table_name=table_head, table_data=data_list, company=company)
            else:
                logger.debug(
                    "table num doesnt exist but the count shows it does")
                # table_query = Table.objects.create(table_name=table_head, table_data=data_list, company=company)

        else:  # create new table
            table_head = table_name + "_" + str(0)
            Table.objects.create(table_name=table_head,
                                 table_data=data_list, company=company)

    except ValueError:
        logger.debug("data is not json compatible")
        return 0


def get_data(table_name, search):
    table_head = table_name + "_" + str(num)
    table_query = Table.objects.get(table_name=table_head)
    return table_query.table_data


# helper functions

def hasher(data, table_name):
    # TODO: create hashes for each key and make a dict of arrays for each table num and make a search index
    node_dict = {}
    data_array = []
    dict
    hash_data = blake3.blake3(data).hexdigest()
    node_dict.
    data_array.append(hash_data)
    node_dict.update(data_array)

    Table.objects.create


# table_name +
    # | entryhash +
    #             | keyhash|#|...
    # |...
    # |...

def search():
    # TODO: search the hash in the search index and output related table num and entry no
