import os
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

def return_authorised_http():
    scopes = ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
        'https://www.googleapis.com/auth/calendar']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scopes=scopes)
    delegated_credentials = credentials.create_delegated(os.environ['MRP_DELEGATED_ACCOUNT'])
    return delegated_credentials.authorize(Http())
