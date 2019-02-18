import mysql.connector as mariadb
import config
from uuid import uuid4 as uuidv4

def connectDB():
    try:
        conn = mariadb.connect(
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = conn.cursor
        conn.autocommit = True

        return conn, cursor

    except Exception as error:
        print('SQL Error: Unable to connect to MySQL database')
        print(error)
        return None


def closeDB(conn, cursor):
    try:
        cursor.close()
        conn.close()

    except Exception as error:
        print('SQL Error: Unable to close connection to MySQL database')
        print(error)


def store_usage(data):
    conn, cursor = connectDB()

    insert_variables = []
    channels = [None] * 12

    try:
        device_id = data.get('uuid', '0')

        channel_uuids(device_id)

        timestamp = data.get('epoch', 0)
        currents = data.get('channels', [])

        col_list = ['deviceID', 'time', 'ch1', 'ch2', 'ch3', 'ch4',
            'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']

        insert_variables.append(device_id)
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
            conn.commit()

            closeDB(conn, cursor)

        except Exception as error:
            print('SQL Error: Unable to insert channel usage data')
            print(error)
            closeDB(conn, cursor)
            return None

    except Exception as error:
        print('Error generating SQL query for channel usage insertion')
        print(error)
        closeDB(conn, cursor)
        return None


def channel_uuids(deviceID):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT id FROM devices WHERE deviceID = %s '''
        cursor.execute(query, (deviceID,))
        data = cursor.fetchall()
        if data:
            closeDB(conn, cursor)
            return

    except Exception as error:
            print(''' SQL Error: Unable to fetch channels for deviceID = %s ''' % (deviceID))
            print(error)
            closeDB(conn, cursor)
            return

    try:
        insert_variables = []
        col_list = ['deviceID', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5',
            'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']

        insert_variables.append(deviceID)
        for _ in range(12):
            channelID = str(uuidv4())
            insert_variables.append(channelID)

        query_placeholders = ', '.join(['%s'] * len(insert_variables))
        query_columns = ', '.join(col_list)

        try:
            query = ''' INSERT INTO devices (%s) VALUES (%s) ''' % (
                query_columns, query_placeholders)
            cursor.execute(query, insert_variables)

        except Exception as error:
            print(''' SQL Error: Unable to add channel IDs for deviceID = %s ''' % (deviceID))
            print(error)
            closeDB(conn, cursor)

    except Exception as error:
        print('Error generating SQL query for channel ID insertion')
        print(error)
        closeDB(conn, cursor)

    closeDB(conn, cursor)