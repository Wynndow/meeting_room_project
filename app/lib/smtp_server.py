import smtplib
from flask import current_app


class LoggedInServer():
    def __init__(self):
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.ehlo()
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        self.server = server

    def sendmail(self, sender, reciever, message):
        self.server.sendmail(sender, reciever, message)
