import pytest
import mock
from app import create_app
from app.lib import api_client
from httplib2 import Http
from datetime import datetime


data = [{
  u'etags': u'"MuWcgcolLPkKr8QHxQ1YIz3aV0o/AVxr01F5j0vGifNKyV2LwmVrkcs"',
  u'generatedResourceName': u'WCB-6-612 Meeting Room (8)',
  u'kind': u'admin#directory#resources#calendars#CalendarResource',
  u'resourceDescription': u'Meeting Room (8)',
  u'resourceEmail': u'digital.cabinet-office.gov.uk_57432d362d3630372d4d522d38@resource.calendar.google.com',
  u'resourceId': u'WC-6-607-MR-8',
  u'resourceName': u'612 Meeting Room',
  u'resourceType': u'MR'}]


class TestApiClient():

    @mock.patch('app.lib.api_client._fetch_resources')
    def test_get_room_list(self, _fetch_resources):
        _fetch_resources.return_value = data
        floor = 'wc-sixth'
        rooms = api_client.get_room_list(floor).rooms
        room_names = list(map(lambda room: room['resourceName'], rooms))
        assert '612 Meeting Room' in room_names
