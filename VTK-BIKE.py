import os
import threading
import time

import serial
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.name = "VTK_BIKE"
app.config.from_object(os.environ['APP_SETTINGS'])

Bootstrap(app)
address = "/dev/arduino1"
baud = 115200


@app.route('/')
def hello_world():
    return render_template('distance.html')


@app.route('/distance')
def get_distance():
    return app.distance


def action():
    ser = serial.Serial(address, baud)
    last_time_received = None
    previous_rpm = 0.0
    perimeter = 2.3
    while True:
        line = ser.readline().strip()
        print('received line', line)
        res = line.split(';')
        current_rpm = float(res[0])
        current_time = time.time()
        if last_time_received is not None:
            app.distance += (previous_rpm + current_rpm) / 2. * (current_time - last_time_received) * 60 * perimeter
        print('distance is now: ', app.distance)
        last_time_received = current_time
        previous_rpm = current_rpm


def start_thread():
    try:
        app.thread = threading.Thread(name="serial", target=action)
    except Exception:
        print("an error occurred while trying to connect to the serial device")


if __name__ == '__main__':
    app.distance = 0.
    start_thread()
    app.run()
