import os
import ast
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build


class Config:
    @staticmethod
    def init_app(app):
        pass

    def create_credentials():
        scopes = ['https://www.googleapis.com/auth/admin.directory.resource.calendar',
                  'https://www.googleapis.com/auth/calendar']
        client_secret_dict = ast.literal_eval(os.environ['MR_CLIENT_SECRET_JSON'])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            client_secret_dict, scopes=scopes).create_delegated(os.environ['MR_DELEGATED_ACCOUNT'])
        http = credentials.authorize(Http())
        directory = build('admin', 'directory_v1', http=http)
        calendar = build('calendar', 'v3', http=http)
        return directory, calendar

    DIRECTORY, CALENDAR = create_credentials()


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
