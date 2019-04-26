from uuid import uuid4 as uuidv4
from datetime import datetime, timedelta

from ..reporter import reportError, isError
from .database import connectDB, closeDB

epoch = datetime(1970,1,1)

def initialize_device(data):
    deviceID = data.get('deviceID', None)
    if deviceID is None:
        reportError('An error occurred getting the deviceID from the monitoring device')
        return

    conn, cursor = connectDB()

    # Check if the device has already been added to the database
    try:
        query = ''' SELECT id FROM devices WHERE deviceID = %s '''
        cursor.execute(query, (deviceID,))
        result = cursor.fetchall()
        if result:
            print("EXISTS")
            closeDB(conn, cursor)
            return

    except Exception as error:
        reportError('SQL Error: Unable to check for device existance', error)
        closeDB(conn, cursor)
        return


    # If not add it and its channels
    try:
        channels = data.get('channels', [])

        # see https://stackoverflow.com/a/25722275
        now = datetime.now()
        timestamp_micros = (now - epoch) // timedelta(microseconds=1)
        timestamp_millis = timestamp_micros // 1000
        timestamp = epoch + timedelta(milliseconds=timestamp_millis)

        device_insert_variables = [deviceID, len(channels), timestamp, timestamp]
        device_col_list = ['deviceID', 'channels', 'created', 'updated']

        position = 1
        for channelID in channels:
            
            try:
                name = 'Channel {}'.format(position)
                channel_col_list = ['deviceID', 'channelID', 'position', 'name', 'created', 'updated']
                channel_insert_variables = [deviceID, channelID, position, name, timestamp, timestamp]
                
                channel_query_placeholders = ', '.join(['%s'] * len(channel_insert_variables))
                channel_query_columns = ', '.join(channel_col_list)

                try:
                    channel_query = ''' INSERT INTO channels (%s) VALUES (%s) ''' % (
                        channel_query_columns, channel_query_placeholders)
                    cursor.execute(channel_query, channel_insert_variables)

                except Exception as error:
                    reportError('SQL Error: Unable to insert new channel', error)
                    closeDB(conn, cursor)
                    return

                position += 1

            except Exception as error:
                reportError('An error occured inserting a new channel', error)
                closeDB(conn, cursor)
                return

        device_query_placeholders = ', '.join(['%s'] * len(device_insert_variables))
        device_query_columns = ', '.join(device_col_list)

        try:
            device_query = ''' INSERT INTO devices (%s) VALUES (%s) ''' % (
                device_query_columns, device_query_placeholders)
            print(device_query)
            cursor.execute(device_query, device_insert_variables)

        except Exception as error:
            reportError('SQL Error: Unable to insert new device', error)
            closeDB(conn, cursor)
            return

    except Exception as error:
        reportError('An error occured inserting a new device', error)
        closeDB(conn, cursor)
        return

    closeDB(conn, cursor)
    return
