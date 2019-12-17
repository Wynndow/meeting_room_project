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

    def is_right_after_(self, booking):
        return self.start == booking.end

    def from_to_for_calendar_link(self):
        return f"{self.start.strftime('%Y%m%dT%H%M%SZ')}/{self.end.strftime('%Y%m%dT%H%M%SZ')}"
