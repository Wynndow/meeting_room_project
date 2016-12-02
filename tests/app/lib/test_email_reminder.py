from datetime import datetime
import mock
import pytest
from freezegun import freeze_time
from app.lib.email_reminder import EmailReminder


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

        assert mock.call.sendmail('admin@example.com', ['test@example.com'], 'Email message') in server_mock.mock_calls

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
                    },
                    u'location': u'Room 101',
                    u'summary': u'Stuff about stuff'
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

        assert """Title: Stuff about stuff\n  Room: Room 101\n  Start: 14:30\n  End: 16:30""" in message

    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_it_sends_the_correct_message_if_no_location_set(self, current_app, smtplib, load_room_ids):
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
                    },
                    u'summary': u'Stuff about stuff'
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

        assert """Title: Stuff about stuff\n  Room: Check your calendar\n  Start: 14:30\n  End: 16:30""" in message

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

        assert mock.call.sendmail('admin@example.com', ['test@example.com'], 'Email message') in server_mock.mock_calls

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

    @freeze_time('2016-11-24 16:09:00')
    @mock.patch('app.lib.email_reminder.EmailReminder._get_all_days_events')
    @mock.patch('app.lib.email_reminder.current_app')
    @mock.patch('app.lib.email_reminder.smtplib')
    def test_if_its_not_friday_it_retrieves_nextday_events(self, smtplib, current_app, _get_all_days_events):
        current_app.config = {
            'CALENDAR': 'calendar',
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }
        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        _get_all_days_events.assert_called_once_with(mock.ANY, mock.ANY, datetime(2016, 11, 25, 16, 9, 0))

    @freeze_time('2016-11-25 16:09:00')
    @mock.patch('app.lib.email_reminder.EmailReminder._get_all_days_events')
    @mock.patch('app.lib.email_reminder.current_app')
    @mock.patch('app.lib.email_reminder.smtplib')
    def test_if_its_friday_it_retrieves_monday_events(self, smtplib, current_app, _get_all_days_events):
        current_app.config = {
            'CALENDAR': 'calendar',
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }
        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        _get_all_days_events.assert_called_once_with(mock.ANY, mock.ANY, datetime(2016, 11, 28, 16, 9, 0))

    @freeze_time('2016-11-25 16:09:00')
    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_subject_is_correct_if_friday(
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

        assert MIMEMultipart.mock_calls[1][1][1] == 'Your meeting room bookings on Monday'

    @freeze_time('2016-11-24 16:09:00')
    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    @mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
    @mock.patch('app.lib.email_reminder.smtplib')
    @mock.patch('app.lib.email_reminder.current_app')
    def test_subject_is_correct_if_not_friday(
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

        assert MIMEMultipart.mock_calls[1][1][1] == 'Your meeting room bookings tomorrow'
