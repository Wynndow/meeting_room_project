import json
import jinja2
from datetime import datetime, timedelta
from collections import defaultdict
from dateutil.parser import parse
from flask import current_app

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from smtp_server import LoggedInServer


class EmailReminder():

    def __init__(self):
        self.day_of_the_week = datetime.now().weekday()
        self.day_in_question = 'Monday' if self.day_of_the_week == 4 else 'tomorrow'
        self.logged_in_server = LoggedInServer()
        self.admin = current_app.config['ADMIN_EMAIL']

    def send_reminders(self):
        calendar = current_app.config['CALENDAR']
        rooms = self._load_room_ids()['wc-all']
        days_until_next_working_day = 3 if self.day_of_the_week == 4 else 1
        next_working_day_events = self._get_all_days_events(
            calendar,
            rooms,
            datetime.now() + timedelta(days=days_until_next_working_day)
        )
        user_events = self._parse_events(next_working_day_events)
        self._send_the_emails(user_events)

    def _load_room_ids(self):
        with open('./app/data/room_ids.json') as file:
            return json.load(file)

    def _get_all_days_events(self, calendar, rooms, date):
        start = date.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        end = date.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        all_events = []
        for room_id in rooms:
            page_token = None
            while True:
                room_events = calendar.events().list(calendarId=room_id,
                                                     timeMin=start,
                                                     timeMax=end,
                                                     pageToken=page_token,
                                                     showDeleted=False,
                                                     singleEvents=True).execute()
                all_events = all_events + room_events['items']
                page_token = room_events.get('nextPageToken')
                if not page_token:
                    break

        return all_events

    def _parse_events(self, events):
        output = defaultdict(list)
        for event in events:
            organizer = event['organizer']['email']

            if organizer[0:29] == 'digital.cabinet-office.gov.uk':
                continue

            output[organizer].append(
                {
                    'summary': event.get('summary'),
                    'location': event.get('location', 'Check your calendar'),
                    'start': parse(event.get('start').get('dateTime')).strftime('%H:%M'),
                    'end': parse(event.get('end').get('dateTime')).strftime('%H:%M')
                }
            )

        for email, event_list in output.items():
            output[email] = sorted(event_list, key=lambda k: k['start'])

        return output

    def _send_the_emails(self, all_events):
        for email_address, events in all_events.items():
            sender = self.admin
            receiver = current_app.config['TEST_MAIL_ADDRESS'] if current_app.config.get('TESTING') \
                else email_address
            subject = 'Your meeting room booking{} for {}'.format('s' if len(events) > 1 else '', self.day_in_question)
            message = self._create_message(sender, receiver, subject)

            part1, part2 = self._render_content(events)

            message.attach(part1)
            message.attach(part2)
            if not current_app.config.get('TESTING'):
                try:
                    self.logged_in_server.sendmail(sender, [receiver], message.as_string())
                except Exception as e:
                    subject = 'Error sending email to {}'.format(receiver)
                    message = 'A wild error appeared! $$$ {}'.format(e)
                    self._email_admin(subject, message)

        self._email_admin(
            'Reminder emails sent.',
            '{} emails sent at {}'.format(
                len(all_events.items()),
                datetime.now().strftime('%d/%m/%y @ %H:%M')
            )
        )

    def _email_admin(self, subject, content):
        message = MIMEText(content.encode('utf-8'))
        message['Subject'] = subject
        message['From'] = self.admin
        message['To'] = self.admin
        self.logged_in_server.sendmail(self.admin, [self.admin], message.as_string())

    def _create_message(self, sender, receiver, subject):
        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        return msg

    def _render_content(self, events):
        env = jinja2.Environment(
            loader=jinja2.PackageLoader('app', 'templates')
        )
        text_body = env.get_template('reminder.txt')
        html_body = env.get_template('reminder.html')

        text = text_body.render(events=events, day=self.day_in_question)
        html = html_body.render(events=events, day=self.day_in_question)

        part1 = MIMEText(text.encode('utf-8'), 'plain')
        part2 = MIMEText(html.encode('utf-8'), 'html')

        return part1, part2
