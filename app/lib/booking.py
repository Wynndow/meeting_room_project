from datetime import datetime

class Booking():
    def __init__(self, times, status):
        self.start = times['start']
        self.end = times['end']
        self.status = status
