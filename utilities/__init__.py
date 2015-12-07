import datetime
import threading
import time

import serial

import local_config
from models import Bike
from vtk_bike import app, mongo


def action():
    app.bikes = {1: Bike("bike1"), 2: Bike("bike2")}
    ser = serial.Serial(local_config.address, local_config.baud)
    while True:
        line = ser.readline().strip()
        print('received line', line)
        res = line.split(':')
        current_speed = float(res[1])
        current_bike = int(res[0].split())

        app.bikes[current_bike].speed_received(current_speed)


def start_new_session():
    session_id = mongo.db.sessions.insert({"timestamp": time.time()})
    app.bikes[1].start_new_session(session_id)
    app.bikes[2].start_new_session(session_id)
    app.current_session_id = session_id


def start_thread():
    try:
        app.thread = threading.Thread(name="serial", target=action)
        app.thread.start()
    except Exception:
        print("an error occurred while trying to connect to the serial device")


def get_overall_distance():
    total_distance = mongo.db.sessions.aggregate(
        [{"$group": {"_id": 1, "total_distance_bike_1": {"$sum": "$bike1"},
                     "total_distance_bike_2": {"$sum": "$bike2"}}}])
    if total_distance.count() == 0:
        return 0
    res = total_distance.next()
    total_distance = res['total_distance_bike_1'] + res['total_distance_bike_2']
    return total_distance


def get_today_distance():
    today_start_timestamp = time.mktime(
        datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y").timetuple())
    today_end_timestamp = today_start_timestamp + 3600 * 24
    today_distance = mongo.db.sessions.aggregate(
        [{"$match": {"timestamp": {"$gte": today_start_timestamp, "$lt": today_end_timestamp}}},
         {"$group": {"_id": 1, "total_distance_bike_1": {"$sum": "$bike1"},
                     "total_distance_bike_2": {"$sum": "$bike2"}}}])
    if today_distance.count() == 0:
        return 0
    res = today_distance.next()
    today_distance = res['total_distance_bike_1'] + res['total_distance_bike_2']

    return today_distance


def get_current_session_distance():
    return app.bikes[1].get_total_distance() + app.bikes[2].get_total_distance()
