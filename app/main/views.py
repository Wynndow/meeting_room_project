from flask import render_template
from . import main
from ..lib import api_client

@main.route('/')
def index():
    rooms = api_client.get_room_list()
    return render_template('index.html', rooms=rooms)
