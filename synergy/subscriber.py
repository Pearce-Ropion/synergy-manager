import json

from .database.usages import store_usage
from .mqtt_config import MQTT_PATH
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	message = msg.payload.decode('utf-8')
	data = json.loads(message)
	store_usage(data)
    # more callbacks, etc