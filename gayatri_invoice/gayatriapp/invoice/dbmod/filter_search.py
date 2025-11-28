from ..models import *
import logging

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
            table_name=table, company=company).values("table_metadata")
        if search_column and search_column in metadata.keys():
            raise ValueError("search coulmn not found")
        queryset = TableData.objects.filter(table_name=table, company=company).filter(
            table_data__icontains=search_term)
        data = queryset.values().order_by("id")
        return data

    except TableName.DoesNotExist:
        logger.error("Table does not exists")
