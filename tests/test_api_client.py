import pytest
from app import create_app
from app.lib import api_client
from httplib2 import Http

room_data = [{
                u'kind': u'admin#directory#resources#calendars#CalendarResource',
                u'resourceType': u'Meeting Room',
                u'resourceId': u'-9717392-651',
                u'resourceEmail': u'digital.cabinet-office.gov.uk_2d393731373339322d363531@resource.calendar.google.com',
                u'etags': u'"XRsypGOPUmlmxokHB51cC07Vb3s/gJruQjs8s_aR200IlqqDePeE-zA"',
                u'resourceDescription': u'3rd Floor Meeting room with capacity of 12',
                u'resourceName': u'Meeting Room 305 (12)'
            }]

class TestApiClient():

    def test_get_room_list(self):
        rooms = api_client.get_room_list()
        room_names = map(lambda room: room['resourceName'], rooms)
        assert 'GDS Boardroom' in room_names
        assert not 'Device Lab - Fire HD7' in room_names

    def test_get_busy_free_returns_json(self):
        response = api_client.get_busy_free(room_data)
        assert response.get('kind') == 'calendar#freeBusy'
