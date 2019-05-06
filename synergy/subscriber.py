import json
import schedule
from datetime import datetime
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
        reminders = dict(cursor.fetchall())
        return reminders
    except Exception as error:
        reportError('SQL Error: Unable to retrieve channel name', error)
        closeDB(conn, cursor)


with open('started.txt', 'r') as f:
    started = f.read()

rem_check = datetime.now()
reminders = get_reminders()
flags = {}

def flag_schedule():
    schedule.every().week.at("03:00").do(reset_flags)

def reset_flags():
    global flags
    flags = {}

def set_flag(chID, time):
    global flags
    flags['chID']['time'] = True

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
    message = msg.payload.decode('utf-8')
    data = json.loads(message)
    # print(data)

    action_type = data.get('type', None)
    callback = switch_action(action_type)

    payload = data.get('payload', {})
    callback(payload)

    # see if abnormal usage
    now = datetime.now()
    if action_type == 'usage':
        first = datetime.strptime(started, '%Y-%m-%d %H:%M:%S')
        time_between = now - first
        chID = payload['channelID']
        if time_between.days >= 7:
            data = {
                'amps': payload['amps'],
                'time': payload['timestamp']
            }
            pred_alert(chID, data)

        #see if need to issue a reminder for this usage
        time_between = now - rem_check
        if time_between.minute >= 5:
            reminders = get_reminders()
        if chID in reminders:
            value = reminders[chID]
            time = datetime.strptime(value['time'], '%Y-%m-%d %H:%M:%S')
            if flags['chID']['time'] is not True:
                if now.time(second=0) == time.time(second=0):
                    #reminder_msg(value['message'])
                    print(value['message'])
                    set_flag(chID, time)

