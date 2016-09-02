from datetime import datetime


class Booking():
    def __init__(self, times, status):
        self.start = times['start']
        self.end = times['end']
        self.status = status

    def times(self):
        return '{} to {}'.format(self.start.strftime('%H:%M'), self.end.strftime('%H:%M'))

    def length(self):
        seconds = (self.end - self.start).total_seconds()
        return int(seconds / 60)
