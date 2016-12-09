import json
import jinja2
from datetime import datetime, timedelta
from collections import defaultdict
from dateutil.parser import parse
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailReminder():

    def __init__(self):
        self.day_of_the_week = datetime.now().weekday()
        self.day_in_question = 'Monday' if self.day_of_the_week == 4 else 'tomorrow'

    def send_reminders(self):
        calendar = current_app.config['CALENDAR']
        rooms = self._load_room_ids()['all']
        days_until_next_working_day = 3 if self.day_of_the_week == 4 else 1
        next_working_day_events = self._get_all_days_events(
            calendar,
            rooms,
            datetime.now() + timedelta(days=days_until_next_working_day)
        )
        user_events = self._parse_events(next_working_day_events)
        self._send_the_emails(user_events)

    def _load_room_ids(self):
        with open('./app/data/room_ids_by_floor.json') as file:
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
        smtp_server = self._create_smtp_server()

        for email_address, events in all_events.items():
            sender = current_app.config['ADMIN_EMAIL']
            receiver = current_app.config['TEST_MAIL_ADDRESS'] if current_app.config.get('TESTING') \
                else email_address
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Your meeting room booking{} for {}'.format(
                's' if len(events) > 1 else '',
                self.day_in_question
            )
            msg['From'] = sender
            msg['To'] = receiver

            env = jinja2.Environment(
                loader=jinja2.PackageLoader('app', 'templates')
            )
            text_body = env.get_template('reminder.txt')
            html_body = env.get_template('reminder.html')

            text = text_body.render(events=events, day=self.day_in_question)
            html = html_body.render(events=events, day=self.day_in_question)

            part1 = MIMEText(text.encode('utf-8'), 'plain')
            part2 = MIMEText(html.encode('utf-8'), 'html')

            msg.attach(part1)
            msg.attach(part2)

            if not current_app.config.get('TESTING'):
                try:
                    smtp_server.sendmail(sender, [receiver], msg.as_string())
                except Exception as e:
                    print('A wild error appeared! $$$ {}'.format(e))
                    break

        if not current_app.config.get('TESTING'):
            try:
                admin_address = current_app.config['ADMIN_EMAIL']
                admin_msg = MIMEText(
                    '{} emails sent at {}'.format(
                        len(all_events.items()),
                        datetime.now().strftime('%d/%m/%y @ %H:%M')
                    )
                )
                admin_msg['Subject'] = 'Reminder emails sent.'
                admin_msg['From'] = admin_address
                admin_msg['To'] = admin_address
                smtp_server.sendmail(admin_address, [admin_address], admin_msg.as_string())
            except Exception as e:
                print('An error occured sending admin email! $$$ {}'.format(e))

        smtp_server.quit()

    def _create_smtp_server(self):
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.ehlo()
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        return server
