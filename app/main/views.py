from flask import render_template
from . import main
from ..lib import api_client, day_maker
import pdb

@main.route('/')
def index():
    rooms = api_client.get_room_list()
    free_busy = api_client.get_free_busy(rooms).get('calendars')
    full_days = {}
    for room in rooms:
        full_days[room.get('resourceEmail')] = day_maker.create_full_day_json(free_busy.get(room.get('resourceEmail')).get('busy'))
    return render_template('index.html', rooms=rooms, full_days=full_days)
