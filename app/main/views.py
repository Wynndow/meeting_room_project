from flask import render_template, request
from . import main
from ..lib import api_client, day_maker, number_padder
from datetime import datetime


@main.route('/', methods=['GET'])
def index():
    floor = request.args.get('floor', 'all')
    date = request.args.get('date', str(datetime.utcnow())[0:10])
    room_list = api_client.get_room_list(floor)
    free_busy = room_list.get_free_busy(date).get('calendars')
    full_days = day_maker.create_full_days(room_list.rooms, free_busy)
    times = number_padder.add_zero(24)

    return render_template('index.html',
                           rooms=room_list.rooms,
                           full_days=full_days,
                           times=times,
                           date=date,
                           floor=floor)
