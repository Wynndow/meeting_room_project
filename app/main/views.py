from flask import render_template, request
from . import main
from ..lib import api_client, day_maker, number_padder
from datetime import datetime


@main.route('/', methods=['GET'])
def whitechapel():
    room_group = request.args.get('room_group', 'wc-all')
    date = request.args.get('date', str(datetime.utcnow())[0:10])
    room_list = api_client.get_room_list(room_group)
    free_busy = room_list.get_free_busy(date).get('calendars')
    full_days = day_maker.create_full_days(room_list.rooms, free_busy)
    times = number_padder.add_zero(23)

    return render_template('index.html',
                           rooms=room_list.rooms,
                           full_days=full_days,
                           times=times,
                           date=date,
                           room_group=room_group,
                           building='whitechapel')
