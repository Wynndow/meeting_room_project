import json
from datetime import datetime
from ..exceptions import InvalidUsage
from flask import current_app
from ..lib.room_list import RoomList


def get_room_list(room_group):
    resources = _fetch_resources()
    filtered = _filter_rooms(resources, room_group)
    return RoomList(filtered)


def _fetch_resources():
    directory = current_app.config['DIRECTORY']
    return directory.resources().calendars().list(customer='my_customer').execute().get('items', [])


def _filter_rooms(resources, room_group):
    room_ids = [room for room in ROOM_IDS if room_group in room['lists']]

    if not room_ids:
        raise InvalidUsage("You've submitted an invalid floor or room type!")

    output = []
    for room_id in room_ids:
        for resource in resources:
            if resource.get('resourceEmail') == room_id['resourceEmail']:
                resource['customName'] = room_id['resourceName']
                output.append(resource)

    return output


def _load_room_ids():
    with open('./app/data/room_ids.json') as file:
        return json.load(file)

ROOM_IDS = _load_room_ids()
