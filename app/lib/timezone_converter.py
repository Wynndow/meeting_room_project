from datetime import datetime, timedelta
from dateutil import tz


class TimeZoneConverter():
    def __init__(self):
        pass

    @staticmethod
    def utc_to_london(time_string):
        utc_tz = tz.gettz('UTC')
        london_tz = tz.gettz('Europe/London')
        naive_time_object = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
        utc_time_object = naive_time_object.replace(tzinfo=utc_tz)
        london_time_object = utc_time_object.astimezone(london_tz)
        return london_time_object.strftime('%Y-%m-%dT%H:%M:%S')
