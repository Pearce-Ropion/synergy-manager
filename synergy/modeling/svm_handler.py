import json
import schedule
import time
import os
from datetime import datetime

from .utils import trim_time
from .svm import gen_alert_model
from ..database.database import connectDB, closeDB
from ..reporter import reportError, isError

def loopSVM():
    try:
        if os.path.isfile('svmrun.json'):
            with open('svmrun.json', 'r') as json_file:
                data = json.load(json_file)

            try:
                last = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
                time_between = datetime.now() - last
            except Exception as error:
                reportError('An error occurred gathering the last run date', error)

            if time_between.days >= 7:
                try:
                    conn, cursor = connectDB()
                    query = ''' SELECT channelID from channels '''
                    cursor.execute(query)
                    channels = cursor.fetchall()
                except Exception as error:
                    reportError('SQL Error: Unable to retrieve channel IDs', error)
                    closeDB(conn, cursor)

                for chID in channels:
                    try:
                        query = ''' SELECT time, amps FROM usages WHERE channelID = %s '''
                        cursor.execute(query, chID)
                        results = cursor.fetchall()
                    except Exception as error:
                        reportError('SQL Error: Unable to insert channel usage', error)
                        closeDB(conn, cursor)
                
                    closeDB(conn, cursor)
                    data = trim_time(results)
                    gen_alert_model(chID, data)

        data = {}
        data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('svmrun.json', 'w') as json_file:
            json.dump(data, json_file)
    except Exception as error:
	    reportError('An error occured within the SVM loop', error)

def start_svm():
    try:
        schedule.every().monday.at("03:00").do(loopSVM)
    except Exception as error:
        reportError('An error occurred scheduling the SVM', error)
