from flask import render_template, request
from . import main
from ..lib import api_client, day_maker
import pdb


@main.route('/')
def index():
    floor = request.args.get('floor') or 'third'
    rooms = api_client.get_room_list(floor)
    free_busy = api_client.get_free_busy(rooms).get('calendars')
    full_days = day_maker.create_full_days(rooms, free_busy)

    return render_template('index.html', rooms=rooms, full_days=full_days)
