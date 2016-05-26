import os
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

scopes = ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
          'https://www.googleapis.com/auth/calendar']

def get_room_list():
    resources = _fetch_resources(_build_directory())
    return _filter_rooms(resources)

def _fetch_resources(directory):
    return directory.resources().calendars().list(customer='my_customer').execute().get('items', [])

def _filter_rooms(resources):
    room_types = ['Meeting Room', 'Meeting Space', 'Meeting space', 'Boardroom']
    return [resource for resource in resources if resource.get('resourceType') in room_types]

def _build_directory():
     http_auth = _return_authorised_http()
     return build('admin', 'directory_v1', http=http_auth)

def _return_authorised_http():
    credentials = _create_delegated_credentials(scopes)
    return credentials.authorize(Http())

def _create_delegated_credentials(scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scopes=scopes)
    return credentials.create_delegated(os.environ['MRP_DELEGATED_ACCOUNT'])
