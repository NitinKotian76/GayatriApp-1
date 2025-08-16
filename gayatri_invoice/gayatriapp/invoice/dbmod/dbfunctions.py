from ..models import *
import logging

logger = logging.getLogger(__name__)


def get_company_inst(user_id: str) -> Company:
    user: CustomUser = CustomUser.objects.get(id=user_id)
    return Company.objects.get(id=user.company_id)


def get_choices(table_name: str, column: str, user_id: str) -> list:
    """
        can improve this function a bit
    """
    table: TableName = TableName.objects.get(
        table_name=table_name,
        company=get_company_inst(user_id)
    )
    dataquery = TableData.objects.filter(table_name=table).values("table_data")
    list_data = [item["table_data"][column] for item in dataquery]
    list_data = list(set(list_data))
    return [(item, item) for item in list_data]


<<<<<<< HEAD
def check_metadata(table_name: str, data: str) -> None:
    """
        this function check whether the data format conforms with metadata
    """


type_data: dict = {
    "str": str,
    "float": float,
    "int": int,
    "bool": bool,
}

 meta = TableMetaData.objects.filter(
      table_name=TableName.objects.get(table_name=table_name)).values("table_metadata")

  for key, value in data.items():
       if key not in meta:
            raise ValueError(f"unexpected key {key}")
        expected_value = type_data.get(meta[key])
        if not expected_value or not isinstance(value, expected_value):
            raise ValueError(
                f"data invalid expected data type {key}:{expected_value}")


def new_table(table_name: str, user_id: str, company_id: str = None, metadata: dict = {}, description: str = {}) -> None:
    """
        this def sets the table name and the metadata
    """
=======
def set_data(table_name: str, data: dict, user_id: str, company_id: int = None):

>>>>>>> ba7e3147723ca0c46d561d8f5ae0883af2410d4b
    if company_id:
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

        obj = TableName.objects.filter(
            table_name__contains=table_name,
            company=company)
        if obj.exists():
            table: TableName = TableName.objects.get(
                table_name=table_name,
                company=company)
            try:
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


def get_data(table_name: str, user_id: str, company_id: int = None, search_term: str = None) -> list:
    """
        this function is a general search function and returns rows of data
        but can be split in to 2 functions one for search and one for getting data 
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
        if search_term:
            queryset = queryset.filter(table_data__icontains=search_term)
        data = queryset.values().order_by("id")
        return data
    except TableName.DoesNotExist:
        logger.error("Table does not exists")
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")


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
