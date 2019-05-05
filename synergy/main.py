import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime

from .mqtt_config import MQTT_SERVER, MQTT_PORT
from .subscriber import on_connect, on_message
from .reporter import reportError
from .modeling.svm_handler import start_svm
from .subscriber import flag_schedule


def main():

    try:

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(MQTT_SERVER, MQTT_PORT, 60)

        start_svm()
        flag_schedule()

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()
    except Exception as error:
        reportError('An error occured started that MQTT Hub Server', error)

    exists = os.path.isfile('started.txt')
    if not exists:
        f = open('started.txt', 'w')
        f.write(datetime.now())
        f.close()

if __name__ == "__main__":
    main()
