from ..reporter import reportError, isError
from .database import connectDB, closeDB

from .channels import insert_channels


def store_usage(data):
    conn, cursor = connectDB()

    insert_variables = []
    channels = [None] * 12

    try:
        deviceID = data.get('uuid', '0')

        insert_channels(deviceID)

        timestamp = data.get('epoch', 0)
        currents = data.get('channels', [])

        col_list = ['deviceID', 'time', 'ch1', 'ch2', 'ch3', 'ch4',
                    'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']

        insert_variables.append(deviceID)
        insert_variables.append(timestamp)

        for i in range(len(currents)):
            channels[i] = currents[i]

        for channel in channels:
            insert_variables.append(channel)

        query_placeholders = ', '.join(['%s'] * len(insert_variables))
        query_columns = ', '.join(col_list)

        try:
            query = ''' INSERT INTO usages (%s) VALUES (%s) ''' % (
                query_columns, query_placeholders)

            cursor.execute(query, insert_variables)
            closeDB(conn, cursor)

        except Exception as error:
            reportError('SQL Error: Unable to insert channel usage data for the device with the specified ID: {}'.format(deviceID), error)
            closeDB(conn, cursor)

    except Exception as error:
        reportError('An error occured inserting channel usage data for the device with the specified ID: {}'.format(deviceID), error)
        closeDB(conn, cursor)
