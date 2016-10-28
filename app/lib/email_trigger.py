import requests


class EmailTrigger():

    @staticmethod
    def call():
        requests.post('http://localhost:5000/send_emails')
