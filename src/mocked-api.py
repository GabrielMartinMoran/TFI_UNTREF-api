from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import time
import random
from datetime import datetime
from werkzeug.serving import WSGIRequestHandler


class Device:

    def __init__(self, name: str, ble_id: str, active=True, turned_on=True):
        self.name = name
        self.ble_id = ble_id
        self.active = active
        self.turned_on = turned_on
        self.measures = []

    def to_dict(self):
        return {
            'name': self.name,
            'ble_id': self.ble_id,
            'measures': [measure.to_dict() for measure in self.measures],
            'active': self.active,
            'turned_on': self.turned_on
        }


class Measure:

    def __init__(self, voltage: float, current: float, timestamp: int):
        self.voltage = voltage
        self.current = current
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'voltage': self.voltage,
            'current': self.current,
            'power': self.current * self.voltage
        }


app = Flask(__name__)
CORS(app)

APP_PORT = 5000

REF_VOLTAGE = 220

data = [
    Device('Heladera', 'b3240d32-9ee9-11eb-a8b3-0242ac130003', active=True, turned_on=True),
    Device('Lavarropas', 'bbe4137c-9ee9-11eb-a8b3-0242ac130003', active=True, turned_on=True),
    Device('Cafetera', 'c331ee60-9ee9-11eb-a8b3-0242ac130003', active=False, turned_on=True),
    Device('Computadora', 'c80fbd68-9ee9-11eb-a8b3-0242ac130003', active=True, turned_on=False),
]


def data_generating_thread():
    global data
    loop = True
    while (loop):
        for device in data:
            device.measures.append(
                Measure(
                    REF_VOLTAGE + random.uniform(-10, 10),
                    random.uniform(0, 1),
                    int(datetime.now().timestamp())  # * 1000)
                )
            )
        time.sleep(5)
        loop = True


@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify([device.to_dict() for device in data])


if __name__ == '__main__':
    thread = Thread(target=data_generating_thread)
    thread.start()
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(port=APP_PORT)
