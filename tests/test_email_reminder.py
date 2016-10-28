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
        expected_calls = [
            mock.call.ehlo(),
            mock.call.starttls(),
            mock.call.login('chris', 'password'),
            mock.call.sendmail('admin@example.com', ['admin@example.com'], 'Email message'),
            mock.call.quit()
        ]

        assert server_mock.mock_calls == expected_calls

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

        expected_calls = [
            mock.call.ehlo(),
            mock.call.starttls(),
            mock.call.login('chris', 'password'),
            mock.call.sendmail('admin@example.com', ['admin@example.com'], 'Email message'),
            mock.call.quit()
        ]

        message = server_mock.mock_calls[-2][1][2]

        assert """Content-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n<p>Hello,</p>\n\n<p>Your room bookings for tomorrow are:</p>\n\n<ul>\n  \n    <li>\n      Room: None <br>\n      Start: 14:30 <br>\n      End 16:30 <br>\n    </li>\n  \n</ul>\n\n<p>If you no longer require the room, please think about unbooking them.</p>\n\n<p>Thanks!</p>\n\n<p>Love from your friendly meeting room app.</p>\n\n<p>x</p>\n""" in message  # NOQA

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

        server_mock.sendmail.assert_called_once_with('admin@example.com', ['admin@example.com'], 'Email message')

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_send_reminders_only_sends_email_to_multiple_users(
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

        assert server_mock.sendmail.call_count == 2
