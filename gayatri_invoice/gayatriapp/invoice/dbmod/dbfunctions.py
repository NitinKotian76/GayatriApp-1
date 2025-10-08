from ..models import *
import logging

logger = logging.getLogger(__name__)


TYPE_DATA = [
    ("str", "str"),
    ("float", "float"),
    ("int", "int"),
    ("bool", "bool"),
]


def get_company_inst(user_id: str) -> Company:
    user: CustomUser = CustomUser.objects.get(id=user_id)
    return Company.objects.get(id=user.company_id)


def get_choices(table_name: str, column: str, user_id: str) -> list:
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


def new_table(table_name: str, user_id: str, description: str, metadata: dict = {}, company_id: str = None):
    """
        this def sets the table name and the metadata
        Args:
            table_name: table name for the new table
            user_id: user id of for to get the company details and can add owner details to creation record
            description: description of the table for the user
            company_id: optional company id for the table 
            metadata: to define the dict structure and the datatype for the key value pairs 
        return:
           table
           metadata
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
            table_metadata=metadata
        )
        return table, metadata
    except Exception as e:
        logger.debug(f"new table error {e}")


def set_data(table_name: str, data: dict, user_id: str, company_id: int = None) -> None:
    """
         this function will set the initial data
    """
    try:
        if isinstance(data, dict) != True:
            logger.debug("data is not json compatible")
            raise Exception("data not compatible")

        if company_id:
            company = Company.objects.get(id=company_id)
        else:
            company = get_company_inst(user_id)

        tableobj = TableName.objects.filter(
            table_name=table_name,
            company=company)
        tablemeta = TableMetaData.objects.filter(
            table_name=table_name, company=company).values("table_metadata")

        if tableobj.exists():
            table: TableName = TableName.objects.get(
                table_name=table_name,
                company=company)
            try:
                for mkey in tablemeta:
                    # check if the data contains all the columns
                    if mkey not in data.keys():
                        raise ValueError(f"{mkey} doesnt exist")
                    if type(data[mkey]).__name__ not in tablemeta[mkey]:
                        raise ValueError(f"{mkey} datatype doesnt match")
                table_query: TableData = TableData.objects.create(
                    table_data=data, table_name=table, company=company)
                table_query.save()
            except Exception as e:
                logger.error("error storing data %s", e)
        else:
            logger.error("table does not exist")
        logger.info("data stored")

    except Exception as e:
        pass


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


def search_data(table_name: str, user_id: str, search_term: str, search_column: str = None, company_id: int = None):
    try:
        if company_id:
            company = Company.objects.get(id=company_id)
        else:
            company = get_company_inst(user_id)
        table = TableName.objects.get(
            table_name=table_name, company=company.id)
        metadata = TableMetaData.objects.filter(
            table_name=table, company=company).values("table_metadata")
        if search_column and search_column in metadata.keys():
            raise ValueError("search coulmn not found")
        queryset = TableData.objects.filter(table_name=table, company=company).filter(
            table_data__icontains=search_term)
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
    data = TableData.objects.filter(table_name=tableobj, company=Company.objects.get(
        company_id=company)).values("table_data")


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
