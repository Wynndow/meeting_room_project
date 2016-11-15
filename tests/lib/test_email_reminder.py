import pytest
from app.lib.email_reminder import EmailReminder
import mock


class TestEmailReminder():
    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_send_reminders_correctly_calls_the_smtp_server(self, current_app, smtplib, load_room_ids, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        load_room_ids.return_value = {'all': ['roomID']}
        server_mock = mock.MagicMock()
        smtplib.SMTP.return_value = server_mock
        calendar_mock = mock.MagicMock()
        calendar_mock.events.return_value.list.return_value.execute.return_value = {
            'items': [
                {
                    u'end': {
                        u'dateTime': u'2016-10-21T16:30:00'
                    },
                    u'organizer': {
                        u'email': u'test@example.com',
                    },
                    u'start': {
                        u'dateTime': u'2016-10-21T14:30:00',
                    }
                }
            ]
        }
        current_app.config = {
            'CALENDAR': calendar_mock,
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }
        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert mock.call.sendmail('admin@example.com', ['admin@example.com'], 'Email message') in server_mock.mock_calls

    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_it_sends_the_correct_message(self, current_app, smtplib, load_room_ids):
        load_room_ids.return_value = {'all': ['roomID']}
        server_mock = mock.MagicMock()
        smtplib.SMTP.return_value = server_mock
        calendar_mock = mock.MagicMock()
        calendar_mock.events.return_value.list.return_value.execute.return_value = {
            'items': [
                {
                    u'end': {
                        u'dateTime': u'2016-10-21T16:30:00'
                    },
                    u'organizer': {
                        u'email': u'test@example.com',
                    },
                    u'start': {
                        u'dateTime': u'2016-10-21T14:30:00',
                    }
                }
            ]
        }
        current_app.config = {
            'CALENDAR': calendar_mock,
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        message = server_mock.mock_calls[-3][1][2]

        assert """Content-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n<p>Hello,</p>\n\n<p>Your meeting room booking details for tomorrow are:</p>\n\n\n  <ul>\n    <li>Room: None</li>\n    <li>Start: 14:30</li>\n    <li>End 16:30</li>\n  </ul>\n\n\n<p>\n  <strong>Delete your room booking if you don\'t need it</strong><br>\n  If you don\'t need the room booking anymore, please delete it so someone else can use the room.\n</p>\n<p>\n  You can delete a room booking in a series without affecting your future bookings.\n</p>\n<p>\n  Read how to delete a room booking using Google Calendar:<br>\n  <a href="https://support.google.com/calendar/answer/37113?hl=en&ref_topic=3417926" taget="_blank">https://support.google.com/calendar/answer/37113?hl=en&ref_topic=3417926</a>\n</p>\n<p>\n  <strong>Think about using a smaller room</strong><br>\n  If you\'ve got fewer people coming to the meeting than you first thought, it would be great if you could try moving to a smaller room.\n</p>\n\n<p>\n  Thanks,<br>\n  Your friendly meeting room app\n</p>\n""" in message  # NOQA

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_send_reminders_only_sends_one_email_for_multiple_bookings(
        self, current_app, smtplib, load_room_ids, MIMEMultipart
    ):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        load_room_ids.return_value = {'all': ['roomID']}
        server_mock = mock.MagicMock()
        smtplib.SMTP.return_value = server_mock
        calendar_mock = mock.MagicMock()
        calendar_mock.events.return_value.list.return_value.execute.return_value = {
            'items': [
                {
                    u'end': {
                        u'dateTime': u'2016-10-21T16:30:00'
                    },
                    u'organizer': {
                        u'email': u'test@example.com',
                    },
                    u'start': {
                        u'dateTime': u'2016-10-21T14:30:00',
                    }
                },
                {
                    u'end': {
                        u'dateTime': u'2016-10-21T11:30:00'
                    },
                    u'organizer': {
                        u'email': u'test@example.com',
                    },
                    u'start': {
                        u'dateTime': u'2016-10-21T10:30:00',
                    }
                }
            ]
        }
        current_app.config = {
            'CALENDAR': calendar_mock,
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }
        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert mock.call.sendmail('admin@example.com', ['admin@example.com'], 'Email message') in server_mock.mock_calls

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_send_reminders_sends_email_to_multiple_users(
        self, current_app, smtplib, load_room_ids, MIMEMultipart
    ):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        load_room_ids.return_value = {'all': ['roomID']}
        server_mock = mock.MagicMock()
        smtplib.SMTP.return_value = server_mock
        calendar_mock = mock.MagicMock()
        calendar_mock.events.return_value.list.return_value.execute.return_value = {
            'items': [
                {
                    u'end': {
                        u'dateTime': u'2016-10-21T16:30:00'
                    },
                    u'organizer': {
                        u'email': u'test@example.com',
                    },
                    u'start': {
                        u'dateTime': u'2016-10-21T14:30:00',
                    }
                },
                {
                    u'end': {
                        u'dateTime': u'2016-10-21T11:30:00'
                    },
                    u'organizer': {
                        u'email': u'anothertest@example.com',
                    },
                    u'start': {
                        u'dateTime': u'2016-10-21T10:30:00',
                    }
                }
            ]
        }
        current_app.config = {
            'CALENDAR': calendar_mock,
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }
        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert server_mock.sendmail.call_count == 3

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_send_reminders_sends_admin_confirmation(self, current_app, smtplib, load_room_ids, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        load_room_ids.return_value = {'all': ['roomID']}
        server_mock = mock.MagicMock()
        smtplib.SMTP.return_value = server_mock
        calendar_mock = mock.MagicMock()
        calendar_mock.events.return_value.list.return_value.execute.return_value = {
            'items': [
                {
                    u'end': {
                        u'dateTime': u'2016-10-21T16:30:00'
                    },
                    u'organizer': {
                        u'email': u'test@example.com',
                    },
                    u'start': {
                        u'dateTime': u'2016-10-21T14:30:00',
                    }
                }
            ]
        }
        current_app.config = {
            'CALENDAR': calendar_mock,
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }
        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        message = server_mock.mock_calls[-2][1][2]

        assert 'Subject: Reminder emails sent.' in message
