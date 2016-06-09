import os
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
from datetime import datetime

scopes = ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
          'https://www.googleapis.com/auth/calendar']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scopes=scopes).create_delegated(os.environ['MRP_DELEGATED_ACCOUNT'])
http = credentials.authorize(Http())
directory = build('admin', 'directory_v1', http=http)
calendar = build('calendar', 'v3', http=http)


def get_room_list():
    resources = _fetch_resources()
    return _filter_rooms(resources)


def get_free_busy(room_list):
    times = _set_times()
    calendar_ids = _extract_calendar_ids(room_list)
    body = _build_free_busy_body(times, calendar_ids)
    return calendar.freebusy().query(body=body).execute()


def _set_times():
    today = datetime.utcnow()
    start = today.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    end = today.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
    return {
        'start': start,
        'end': end
    }


def _build_free_busy_body(times, calendar_ids):
    return {
        "timeMin": times['start'],
        "timeMax": times['end'],
        "timeZone": 'GMT+01:00',
        "items": calendar_ids
    }


def _extract_calendar_ids(room_list):
    calendars = []
    for room in room_list:
        calendars.append({"id": room.get('resourceEmail')})
    return calendars


def _fetch_resources():
    return directory.resources().calendars().list(customer='my_customer').execute().get('items', [])


def _filter_rooms(resources):
    room_types = ['Meeting Room', 'Meeting Space', 'Meeting space', 'Boardroom']
    return [resource for resource in resources if resource.get('resourceType') in room_types]
