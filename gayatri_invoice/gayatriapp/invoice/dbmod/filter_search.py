from ..models import *
import logging
from .dbfunctions import get_company_inst

logger = logging.getLogger(__name__)


def search_data(table_name: str, user_id: str, search_term: str, search_column: str = None, company_id: int = None):
    '''
        this function is to search for the row which is searched for in the search field 
    '''
    try:
        if company_id:
            company = Company.objects.get(id=company_id)
        else:
            company = get_company_inst(user_id)
        table = TableName.objects.get(
            table_name=table_name, company=company.id)
        metadata = TableMetaData.objects.filter(
            table_name=table).values("table_metadata")
        if search_column and search_column in metadata.keys():
            raise ValueError("search coulmn not found")
        queryset = TableData.objects.filter(table_name=table, company=company).filter(
            table_data__icontains=search_term)
        data = queryset.values().order_by("id")
        return data

    except TableName.DoesNotExist:
        logger.error("Table does not exists")


def filter_by(table_name: str, *args, **kwargs):
    """
    this function will be used to filter the table with the columns of the 
    table including the date and time. according to the provided metadata for the particular table.
    this means the template will send a request involving the name of the columns and will have the wasy to sort it 
    and in cases where the user will be  able to multiselect the unique values in a columns

    :param table_name: name of the table to be filtered
    """
    # get the tablename
    # name = TableName.objects.get(table_name=table_name)
    # TableData.objects.filter()
