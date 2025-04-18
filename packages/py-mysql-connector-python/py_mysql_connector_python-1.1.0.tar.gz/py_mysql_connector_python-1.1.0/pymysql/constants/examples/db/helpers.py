from db.mysql_connection import select

from settings import settings


def get_columns(table_name):
    query = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS \n"
             "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s \n"
             "ORDER BY ORDINAL_POSITION;")
    result_dict = select(query, (settings.db_name, table_name))

    return [row["COLUMN_NAME"] for row in result_dict]