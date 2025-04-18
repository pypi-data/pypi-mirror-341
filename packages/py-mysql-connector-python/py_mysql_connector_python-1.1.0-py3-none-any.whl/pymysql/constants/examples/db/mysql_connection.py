import logging
from typing import Union, Dict, List

import pymysql
from pymysql.cursors import DictCursor

from settings import settings

# Подключение к БД
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database=settings.db_name,
    port=3306,
    cursorclass=DictCursor
)
print("Подключение к MySQL успешно")

def select(query, args=None) -> List[Dict[str, Union[str, int]]]:
    cursor = connection.cursor()
    try:
        print(query, args or "")
        print('-'*20)
        cursor.execute(query, args)
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        raise e
    finally:
        cursor.close()

def update(query, args=None) -> int:
    cursor = connection.cursor()
    try:
        print(query, args)
        print('-'*20)
        cursor.execute(query, args)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        connection.rollback()
        raise e
    finally:
        cursor.close()