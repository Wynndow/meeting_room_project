import os
import requests


class EmailTrigger():

    @staticmethod
    def call():
        headers = {'Authorization': 'Bearer {}'.format(os.environ.get('MR_AUTH_TOKEN'))}
        requests.post('http://localhost:5000/send_emails', headers=headers)
