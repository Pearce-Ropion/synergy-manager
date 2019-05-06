from uuid import uuid4 as uuidv4

import mysql.connector as mariadb

from ..reporter import reportError, isError

config = {
    'user': 'synergy',
    'password': 'wonderland',
    'host': 'localhost',
    'port': 3306,
    'database': 'synergy',
    'raise_on_warnings': True
}

def connectDB():
    try:
        conn = mariadb.connect(**config)
        cursor = conn.cursor(dictionary=True)
        conn.autocommit = True

        return conn, cursor

    except Exception as error:
        reportError('SQL Error: Unable to connect to Synergy database', error)

    return None, None


def closeDB(conn, cursor):
    try:
        cursor.close()
        conn.close()

    except Exception as error:
        reportError('SQL Error: Unable to close database connection', error)

    return
