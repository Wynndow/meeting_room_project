import pytest
from app import create_app
from app.lib import credentials
from httplib2 import Http

class TestTheThings():
    def test_return_authorised_http(self):
        assert type(credentials.return_authorised_http()) is Http
