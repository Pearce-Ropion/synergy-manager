import json
import schedule
from datetime import datetime, time

from .database.usages import store_usage
from .database.devices import initialize_device
from .mqtt_config import MQTT_PATH, MQTT_SERVER, MQTT_PORT
from .modeling.svm import pred_alert
from .database.database import connectDB, closeDB
from .reporter import reportError, isError
from .modeling.send_sms import reminder_msg

def get_reminders():
    try:
        conn, cursor = connectDB()
        query = ''' SELECT * FROM reminders GROUP BY channelID'''
        cursor.execute(query)
        results = cursor.fetchall()
        reminders = {}
        for result in results:
            reminders[result['channelID']] = result;
        
        flags = {}
        for chID in reminders:
            flags[chID] = {}
        for chID in reminders:
        	value = reminders[chID]
        	flags[chID][value['time']] = False
            
        return reminders, flags
    except Exception as error:
        reportError('SQL Error: Unable to retrieve reminders list', error)
        closeDB(conn, cursor)


rem_check = datetime.now()
reminders, flags = get_reminders()

def flag_schedule():
    schedule.every().day.at("03:00").do(reset_flags)

def reset_flags():
    global flags
    flags = {}

def set_flag(chID, time):
    global flags
    flags[chID][time] = True

def null_action(data):
    return

def switch_action(action_type):
    actions = {
        'usage': store_usage,
        'initialize': initialize_device,
    }
    return actions.get(action_type, null_action)
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT on ' + str(MQTT_SERVER) + ':' + str(MQTT_PORT))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode('utf-8')
        data = json.loads(message)
        # print(data)
    except Exception as error:
    	reportError('An error occured decoding the message', error)

    try:
        action_type = data.get('type', None)
        callback = switch_action(action_type)

        payload = data.get('payload', {})
        callback(payload)
    except Exception as error:
    	reportError('An error occured processing the callback', error)    
    
    try:
            # see if abnormal usage
        now = datetime.now()
        if action_type == 'usage':
            with open('started.txt', 'r') as f:
                started = f.read()

            try:
                startTime = datetime.strptime(started, '%Y-%m-%d %H:%M:%S.%f')
                time_between = now - startTime
                chID = payload['channelID']
                if time_between.days >= 7:
                    data = {
                        'amps': payload['amps'],
                        'time': payload['timestamp']
                    }
                    pred_alert(chID, data)
            except Exception as error:
    	        reportError('An error occurred processing the prediction', error)

            try:
                #see if need to issue a reminder for this usage
                global reminders
                global rem_check
                global flags

                time_between = now - rem_check
                if time_between.seconds >= 300:
                    reminders = get_reminders()
                    rem_check = now
                chID = payload['channelID']
                if chID in reminders:
                    value = reminders[chID]
                    rem_date = value['time']
                    if chID in flags:
                        if rem_date in flags[chID]:
                            if flags[chID][rem_date] is not True:
                                now_time = time(now.hour, now.minute, 0, 0)
                                rem_time = time(rem_date.hour, rem_date.minute, 0, 0)
                                if now_time == rem_time:
                                    reminder_msg(value['message'])
                                    # print(value['message'])
                                    set_flag(chID, rem_date)
            except Exception as error:
    	        reportError('An error occurred processing the reminders', error)   
    except Exception as error:
    	reportError('An error occurred processing the usage data', error)   

