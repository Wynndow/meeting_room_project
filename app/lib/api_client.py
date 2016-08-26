import json
from datetime import datetime
from ..exceptions import InvalidUsage
from flask import current_app
from ..lib.room_list import RoomList


def get_room_list(floor):
    resources = _fetch_resources()
    filtered = _filter_rooms(resources, floor)
    return RoomList(_neaten_room_names(filtered))


def _fetch_resources():
    directory = current_app.config['DIRECTORY']
    return directory.resources().calendars().list(customer='my_customer').execute().get('items', [])


def _filter_rooms(resources, floor):
    room_ids = ROOM_IDS.get(floor)

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


def _load_room_ids():
    with open('./app/data/room_ids_by_floor.json') as file:
        return json.load(file)

ROOM_IDS = _load_room_ids()
