import pytest
from app import create_app
from app.lib import api_client
from httplib2 import Http

class TestApiClient():
    def test_return_authorised_http(self):
        assert type(api_client.return_authorised_http()) is Http

    def test_get_room_list(self):
        rooms = api_client.get_room_list()
        room_names = map(lambda room: room['resourceName'], rooms)
        assert 'GDS Boardroom' in room_names
        assert not 'Device Lab - Fire HD7' in room_names
