from flask import render_template, request
from . import main
from ..lib import api_client, day_maker, number_padder
from datetime import datetime


@main.route('/')
def index():
    floor = request.args.get('floor', 'third')
    date = request.args.get('date', str(datetime.utcnow())[0:10])
    rooms = api_client.get_room_list(floor)
    free_busy = api_client.get_free_busy(rooms, date).get('calendars')
    full_days = day_maker.create_full_days(rooms, free_busy)
    times = number_padder.add_zero(24)

    return render_template('index.html', rooms=rooms, full_days=full_days, times=times)
