import time

from vtk_bike import mongo, app


class Bike:
    last_time_received = None
    last_speed_received = 0
    total_distance = 0
    session_id = None

    def __init__(self, bike_id):
        self.bike_id = bike_id

    def speed_received(self, speed):
        with app.app_context():
            current_time = time.time()
            if self.last_time_received is not None:
                distance = speed / 3600.* (current_time - self.last_time_received)
                self.total_distance += distance
                res = mongo.db.sessions.update({"_id": self.session_id}, {"$set": {self.bike_id: self.total_distance}})
            self.last_speed_received = speed
            self.last_time_received = current_time

    def get_total_distance(self):
        return self.total_distance

    def start_new_session(self, session_id):
        self.total_distance = 0
        self.session_id = session_id
