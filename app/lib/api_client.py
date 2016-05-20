import os
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

def return_authorised_http():
    scopes = ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
        'https://www.googleapis.com/auth/calendar']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scopes=scopes)
    delegated_credentials = credentials.create_delegated(os.environ['MRP_DELEGATED_ACCOUNT'])
    return delegated_credentials.authorize(Http())

def get_room_list():
    http_auth = return_authorised_http()
    directory = build('admin', 'directory_v1', http=http_auth)
    resources = _fetch_resources(directory)
    return _filter_rooms(resources)

def _fetch_resources(directory):
    return directory.resources().calendars().list(customer='my_customer').execute().get('items', [])

def _filter_rooms(resources):
    room_types = ['Meeting Room', 'Meeting Space', 'Meeting space', 'Boardroom']
    return [resource for resource in resources if resource.get('resourceType') in room_types]
