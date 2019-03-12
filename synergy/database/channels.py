from uuid import uuid4 as uuidv4

from ..reporter import reportError, isError
from .database import connectDB, closeDB

def insert_channels(deviceID, channel_count):
    conn, cursor = connectDB()

    # Check if the device has already been added to the database
    try:
        query = ''' SELECT id FROM devices WHERE deviceID = %s '''
        cursor.execute(query, (deviceID,))
        data = cursor.fetchall()
        if data:
            closeDB(conn, cursor)
            return

    except Exception as error:
        reportError('SQL Error: Unable to get channels for the device with the specified ID: {}'.format(deviceID), error)
        closeDB(conn, cursor)
        return


    # If not add it and its channels
    try:
        device_insert_variables = [deviceID, channel_count]
        device_col_list = ['deviceID', 'channels', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5',
                    'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']

        for i in range(channel_count):
            channelID = str(uuidv4())
            device_insert_variables.append(channelID)

            try:
                channel_insert_variables = [deviceID, channelID, i + 1]
                channel_col_list = ['deviceID', 'channelID', 'position']
                
                channel_query_placeholders = ', '.join(['%s'] * len(channel_insert_variables))
                channel_query_columns = ', '.join(channel_col_list)

                try:
                    channel_query = ''' INSERT INTO channels (%s) VALUES (%s) ''' % (
                        channel_query_columns, channel_query_placeholders)
                    cursor.execute(channel_query, channel_insert_variables)

                except Exception as error:
                    reportError('SQL Error: Unable to insert new channel into channels table with ID: {}'.format(channelID), error)
                    closeDB(conn, cursor)
                    return

            except Exception as error:
                reportError('An error occured inserting a new channel into channels table with ID: {}'.format(channelID), error)
                closeDB(conn, cursor)
                return

        for _ in range(12 - channel_count):
            device_insert_variables.append(None)

        device_query_placeholders = ', '.join(['%s'] * len(device_insert_variables))
        device_query_columns = ', '.join(device_col_list)

        try:
            device_query = ''' INSERT INTO devices (%s) VALUES (%s) ''' % (
                device_query_columns, device_query_placeholders)
            cursor.execute(device_query, device_insert_variables)

        except Exception as error:
            reportError('SQL Error: Unable to insert channel IDs for the device with the specified ID: {}'.format(deviceID), error)
            closeDB(conn, cursor)
            return

    except Exception as error:
        reportError('An error occured inserting the channels for the device with the specified ID: {}'.format(deviceID), error)
        closeDB(conn, cursor)
        return

    closeDB(conn, cursor)
    return
