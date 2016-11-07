import os
from datetime import datetime

import requests


class EmailTrigger():

    @staticmethod
    def call():
        headers = {'Authorization': 'Bearer {}'.format(os.environ.get('MR_AUTH_TOKEN'))}
        requests.post('https://meeting-rooms.cloudapps.digital/send_emails', headers=headers)
