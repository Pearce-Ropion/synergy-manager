import random
from datetime import datetime
import json

data = []
unix = 1555226946
for i in range (0, 10000):
    unix += 60
    data.append({
        "amps": random.uniform(0.0, 3.0),
        "time": datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S.%f')
    })

with open('test.json', 'w') as json_file:
        json.dump(data, json_file)
