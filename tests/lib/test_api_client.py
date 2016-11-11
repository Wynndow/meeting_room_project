import pytest
import mock
from app import create_app
from app.lib import api_client
from httplib2 import Http
from datetime import datetime


data = [{
    u'kind': u'admin#directory#resources#calendars#CalendarResource',
    u'resourceType': u'Meeting Room',
    u'resourceId': u'-9717392-651',
    u'resourceEmail': u'digital.cabinet-office.gov.uk_2d393731373339322d363531@resource.calendar.google.com',
    u'etags': u'"XRsypGOPUmlmxokHB51cC07Vb3s/gJruQjs8s_aR200IlqqDePeE-zA"',
    u'resourceDescription': u'3rd Floor Meeting room with capacity of 12',
    u'resourceName': u'Meeting Room 305 (12)'
}]


class TestApiClient():

    @mock.patch('app.lib.api_client._fetch_resources')
    def test_get_room_list(self, _fetch_resources):
        _fetch_resources.return_value = data
        floor = 'third'
        rooms = api_client.get_room_list(floor).rooms
        room_names = list(map(lambda room: room['resourceName'], rooms))
        assert 'Meeting Room 305 (12)' not in room_names
        assert '305 (12)' in room_names
