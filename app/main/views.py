from flask import render_template
from . import main
from ..lib import api_client

@main.route('/')
def index():
    rooms = api_client.get_room_list()
    free_busy = api_client.get_busy_free(rooms)
    return render_template('index.html', rooms=rooms, free_busy=free_busy)
