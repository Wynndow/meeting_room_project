from flask import current_app
from datetime import datetime
from dateutil.tz import tzlocal


class RoomList():

    def __init__(self, rooms):
        self.rooms = rooms

    def get_free_busy(self, date):
        times = self._set_times(date)
        calendar_ids = self._extract_calendar_ids(self.rooms)
        body = self._build_free_busy_body(times, calendar_ids)
        calendar = current_app.config['CALENDAR']
        return calendar.freebusy().query(body=body).execute()

    def _set_times(self, date):
        try:
            today = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise InvalidUsage("You've submitted an invalid date!")

        start = today.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        end = today.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        return {
            'start': start,
            'end': end
        }

    def _extract_calendar_ids(self, rooms):
        calendars = []
        for room in rooms:
            calendars.append({"id": room.get('resourceEmail')})
        return calendars

    def _build_free_busy_body(self, times, calendar_ids):
        return {
            "timeMin": times['start'],
            "timeMax": times['end'],
            "timeZone": 'GMT+0{}:00'.format('1' if datetime.now(tzlocal()).tzname() == 'BST' else '0'),
            "items": calendar_ids
        }
