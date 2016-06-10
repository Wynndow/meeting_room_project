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
        rooms = api_client.get_room_list(floor)
        room_names = map(lambda room: room['resourceName'], rooms)
        assert 'Meeting Room 305 (12)' in room_names

    @mock.patch('app.lib.api_client.calendar.freebusy')
    def test_get_free_busy_calls_api_with_data(self, freebusy):

        query_return = mock.MagicMock()
        query_return.execute.return_value = None
        freebusy_return = mock.MagicMock()
        freebusy_return.query.return_value = query_return
        freebusy.return_value = freebusy_return

        response = api_client.get_free_busy(data)

        freebusy_return.query.assert_called_once_with(body={
            'timeMax': mock.ANY,
            'timeZone': 'GMT+01:00',
            'timeMin': mock.ANY,
            'items': [{
                'id': u'digital.cabinet-office.gov.uk_2d393731373339322d363531@resource.calendar.google.com'
            }]
        })
