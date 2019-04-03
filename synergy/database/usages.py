from ..reporter import reportError, isError
from .database import connectDB, closeDB

def store_usage(data):
    conn, cursor = connectDB()

    insert_variables = []

    try:
        deviceID = data.get('deviceID', None)
        channelID = data.get('channelID', None)
        if (deviceID is None or channelID is None):
            return

        timestamp = datetime(1970, 1, 1) + timedelta(milliseconds = data.get('timestamp', 0))
        amperage = data.get('amps', 0)

        col_list = ['deviceID', 'channelID', 'time', 'amps']

        insert_variables.append(deviceID)
        insert_variables.append(channelID)
        insert_variables.append(timestamp)
        insert_variables.append(amperage)

        query_placeholders = ', '.join(['%s'] * len(insert_variables))
        query_columns = ', '.join(col_list)

        try:
            query = ''' INSERT INTO usages (%s) VALUES (%s) ''' % (
                query_columns, query_placeholders)

            cursor.execute(query, insert_variables)
            closeDB(conn, cursor)

        except Exception as error:
            reportError('SQL Error: Unable to insert channel usage', error)
            closeDB(conn, cursor)

    except Exception as error:
        reportError('An error occured inserting channel usage data', error)
        closeDB(conn, cursor)
