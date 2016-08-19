import json
from datetime import datetime
from ..exceptions import InvalidUsage
from flask import current_app


def get_room_list(floor):
    resources = _fetch_resources()
    filtered = _filter_rooms(resources, floor)
    return _neaten_room_names(filtered)


def get_free_busy(room_list, date):
    times = _set_times(date)
    calendar_ids = _extract_calendar_ids(room_list)
    body = _build_free_busy_body(times, calendar_ids)
    calendar = current_app.config['CALENDAR']
    return calendar.freebusy().query(body=body).execute()


def _set_times(date):
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
    directory = current_app.config['DIRECTORY']
    return directory.resources().calendars().list(customer='my_customer').execute().get('items', [])


def _filter_rooms(resources, floor):
    with open('./app/data/room_ids_by_floor.json') as file:
        room_ids_by_floor = json.load(file)

    room_ids = room_ids_by_floor.get(floor)

    if room_ids is None:
        raise InvalidUsage("You've submitted an invalid floor!")

    output = []
    for room_id in room_ids:
        for resource in resources:
            if resource.get('resourceEmail') == room_id:
                output.append(resource)

    return output


def _neaten_room_names(rooms):
    for room in rooms:
        room['resourceName'] = room['resourceName'].replace('Meeting Room ', '')
    return rooms
