import requests

def trigger_reminder_emails():
    requests.post('http://localhost:5000/send_emails')
