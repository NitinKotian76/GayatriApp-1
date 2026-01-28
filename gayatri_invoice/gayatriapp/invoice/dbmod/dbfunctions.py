###############
# PHASE 2
###############
import logging

from ..models import *

logger = logging.getLogger(__name__)


TYPE_DATA = [
    ("str", "str"),
    ("float", "float"),
    ("int", "int"),
    ("bool", "bool"),
    ("date", "date")
]


def get_company_inst(user_id: str) -> Company:
    user: CustomUser = CustomUser.objects.get(id=user_id)
    return Company.objects.get(id=user.company_id)


def get_choices(table_name: str, column: str, user_id: int) -> list:
    """
    this function is to get list of choices in a table
    """
    table: TableName = TableName.objects.get(
        table_name=table_name,
        company=get_company_inst(user_id)
    )
    dataquery = TableData.objects.filter(table_name=table).values("table_data")
    list_data = [item["table_data"][column] for item in dataquery]
    list_data = list(set(list_data))
    return [(item, item) for item in list_data]


def check_metadata(table_name: str, data: str) -> bool:
    # NOTE:the data coming has to be of the same structure or ValueError is raised
    """
        this function check whether the data format conforms with metadata
        Args:
            table_name = table name of the table whose schema has to be checked 
            data = the incoming dict data that has to be checked 
        return:
            False:
            ValueError
                if the dict structure is different
                if the value is not the expected data type 
            True:
            if datatype is accurate in each key value pair.
    """
    type_data = TYPE_DATA  # this is predefined above
    meta = TableMetaData.objects.filter(
        table_name=TableName.objects.get(table_name=table_name)).values("table_metadata")
    logger.debug(meta)
    for key, value in data.items():
        if key not in meta:
            raise ValueError(f"unexpected key {key}")
            return False

        expected_value = type_data.get(meta[key])
        if not expected_value or not isinstance(value, expected_value):
            raise ValueError(
                f"data invalid expected data type {key}:{expected_value}")
            return False
    return True


def new_table(table_name: str, user_id: int, description: str, duplicates_allowed: bool, metadata: dict = {}, company_id: str = None):
    """
    this def sets the table name and the metadata

    :param table_name: table_name
    :param user_id: user id of the current user
    :param description: description of the new table
    :param metadata: metadata list 
    :param company_id: optional company_id
    """
    if company_id is not None:
        company = Company.objects.get(id=company_id)
    else:
        company = get_company_inst(user_id)

    try:
        table = TableName.objects.create(
            table_name=table_name,
            description=description,
            company=company
        )
        metadata = TableMetaData.objects.create(
            table_name=table,
            table_unique=duplicates_allowed,
            table_metadata=metadata
        )
        return table, metadata
    except Exception as e:
        logger.debug(f"new table error {e}")


def set_data(table_name: str, data: dict, user_id: str, company_id: int = None) -> None:
    """
    this function sets the nested data base rows by checking the metadata of the nested table

    :param table_name: table name of the nested table
    :param data: data dict for the row data
    :param user_id: user id 
    :param company_id: company id 
    :raises Exception: raises exception if data is not type dict 
    :raises ValueError: if the table dosent contain the column name 
    :raises ValueError: if the data is not the data type of the column
    """
    logger.debug("set_data started")
    if isinstance(data, dict) != True:
        logger.debug("data is not json compatible")
        raise Exception("data not compatible")

    if company_id:
        company = Company.objects.get(id=company_id)

    else:
        company = get_company_inst(user_id)

    tableobj = TableName.objects.get(table_name=table_name, company=company)

    tablemeta = TableMetaData.objects.filter(
        table_name=tableobj).values("table_metadata")

    try:
        for mkey in tablemeta[0]["table_metadata"].keys():
            # check if the data contains all the columns
            if mkey not in data.keys():
                raise ValueError(f"{mkey} doesnt exist")
            if type(data[mkey]).__name__ != tablemeta[0]["table_metadata"][mkey]:
                logger.debug(type(data[mkey]).__name__)
                logger.debug(tablemeta[0]["table_metadata"][mkey])
                raise ValueError(f"{mkey} datatype doesnt match")

        table_query = TableData.objects.create(
            table_data=data, table_name=tableobj, company=company)
        table_query.save()

        logger.info("data stored")
    except Exception as e:
        logger.error("error storing data %s", e)


def get_data(table_name: str, user_id: str, company_id: int = None) -> list:
    """
        this function is a general search function and returns rows of data
        but can be split in to 2 functions one for search and one for getting data 
        Args: 
            table_name = table name
            user_id = user id for company_id
            company_id = specifically mention company_id
            search_term = for search term in the table in TableData
    """
    try:
        if company_id:
            company = Company.objects.get(id=company_id)
        else:
            company = get_company_inst(user_id)
        table = TableName.objects.get(
            table_name=table_name, company=company.id)
        queryset = TableData.objects.filter(
            table_name=table, company=company)
        data = queryset.values().order_by("id")
        return data
    except TableName.DoesNotExist:
        logger.error("Table does not exists")


def get_data_column(table_name: str, user_id: str, column_name: str, company_id: str = None) -> list:
    """
         this function is meant for extracting columnar data from the json strings
    """
    if company_id:
        company: Company = Company.objects.get(id=company_id)
    else:
        company: Company = get_company_inst(user_id)

    tableobj = TableName.objects.get(table_name=table_name)
    data = TableData.objects.filter(
        table_name=tableobj, company=company).values("table_data")
    return data


def update_data(table_name: str, data: dict, user_id: str, search_term: str = None, company_id: int = None) -> None:
    """
        this function will only update the data not the metadata
    """
    # initial checks

    if isinstance(data, dict) != True:
        logger.error("data is not json compatible")
        raise Exception("data not compatible")
    if company_id:
        company: Company = Company.objects.get(id=company_id)
    else:
        company: Company = get_company_inst(user_id)

    obj = TableName.objects.filter(
        table_name__contains=table_name, company=company)
    # check the data with metadata format
    try:
        check_metadata(table_name, data)
    except Exception as e:
        pass

    if obj.exists():
        table = TableName.objects.get(table_name=table_name, company=company)
        try:
            query = get_data(table_name, user_id, search_term)
            if data:
                table_query = TableData.objects.update(
                    table_data=data, table_name=table, company=company)
                table_query.save()
            else:
                logger.error("data not found")
        except Exception as e:
            logger.error("error storing data %s", e)
    else:
        logger.error("table does not exist")
    logger.error("data stored")
