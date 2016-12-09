from datetime import datetime
from copy import deepcopy
import mock
from freezegun import freeze_time
from app.lib.email_reminder import EmailReminder

GENERIC_EVENT = {
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


class TestEmailReminder():

    def setup(self):
        self._load_room_ids_patch = mock.patch('app.lib.email_reminder.EmailReminder._load_room_ids')
        self.logged_in_server_patch = mock.patch('app.lib.email_reminder.LoggedInServer')
        self.current_app_patch = mock.patch('app.lib.email_reminder.current_app')

        self._load_room_ids = self._load_room_ids_patch.start()
        self.logged_in_server = self.logged_in_server_patch.start()
        self.current_app = self.current_app_patch.start()

        self.server_mock = mock.MagicMock()
        self.calendar_mock = mock.MagicMock()

        self._load_room_ids.return_value = {'all': ['roomID']}
        self.logged_in_server.return_value = self.server_mock

        self.current_app.config = {
            'CALENDAR': self.calendar_mock,
            'MAIL_SERVER': 'server',
            'MAIL_PORT': 25,
            'MAIL_USERNAME': 'chris',
            'MAIL_PASSWORD': 'password',
            'ADMIN_EMAIL': 'admin@example.com'
        }
        self.events = deepcopy(GENERIC_EVENT)

    def teardown(self):
        self._load_room_ids_patch.stop()
        self.logged_in_server_patch.stop()
        self.current_app_patch.stop()

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    def test_send_reminders_correctly_calls_the_logged_in_server(self, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = GENERIC_EVENT

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert mock.call.sendmail(
            'admin@example.com',
            ['test@example.com'],
            'Email message'
        ) in self.server_mock.mock_calls

    def test_it_sends_the_correct_message(self):
        self.events['items'][0].update({
            u'location': u'Room 101',
            u'summary': u'Stuff about stuff'
        })
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        message = self.server_mock.mock_calls[0][1][2]

        assert """Title: Stuff about stuff\n  Room: Room 101\n  Start: 14:30\n  End: 16:30""" in message

    def test_it_sends_the_correct_message_if_no_location_set(self):
        self.events['items'][0].update({
            u'summary': u'Stuff about stuff'
        })
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        message = self.server_mock.mock_calls[0][1][2]

        assert """Title: Stuff about stuff\n  Room: Check your calendar\n  Start: 14:30\n  End: 16:30""" in message

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    def test_send_reminders_only_sends_one_email_for_multiple_bookings(self, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        event_two = self.events['items'][0].copy()
        event_two.update({
            u'start': {
                u'dateTime': u'2016-10-21T10:30:00',
            },
            u'end': {
                u'dateTime': u'2016-10-21T11:30:00'
            },
        })
        self.events['items'].append(event_two)
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert mock.call.sendmail(
            'admin@example.com',
            ['test@example.com'],
            'Email message'
        ) in self.server_mock.mock_calls

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    def test_send_reminders_sends_email_to_multiple_users(self, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        event_two = self.events['items'][0].copy()
        event_two.update({
            u'organizer': {
                u'email': u'anothertest@example.com',
            },
        })
        self.events['items'].append(event_two)
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert len(self.server_mock.mock_calls) == 3

    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    def test_send_reminders_sends_admin_confirmation(self, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        message = self.server_mock.mock_calls[-1][1][2]

        assert 'Subject: Reminder emails sent.' in message

    @freeze_time('2016-11-24 16:09:00')
    @mock.patch('app.lib.email_reminder.EmailReminder._get_all_days_events')
    def test_if_its_not_friday_it_retrieves_nextday_events(self, _get_all_days_events):

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        _get_all_days_events.assert_called_once_with(mock.ANY, mock.ANY, datetime(2016, 11, 25, 16, 9, 0))

    @freeze_time('2016-11-25 16:09:00')
    @mock.patch('app.lib.email_reminder.EmailReminder._get_all_days_events')
    def test_if_its_friday_it_retrieves_monday_events(self, _get_all_days_events):

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        _get_all_days_events.assert_called_once_with(mock.ANY, mock.ANY, datetime(2016, 11, 28, 16, 9, 0))

    @freeze_time('2016-11-25 16:09:00')
    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    def test_subject_is_correct_if_friday(self, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert MIMEMultipart.mock_calls[3][1][1] == 'Your meeting room booking for Monday'

    @freeze_time('2016-11-24 16:09:00')
    @mock.patch('app.lib.email_reminder.MIMEMultipart')
    def test_subject_is_correct_if_not_friday(self, MIMEMultipart):
        MIMEMultipart.return_value.as_string.return_value = 'Email message'
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert MIMEMultipart.mock_calls[3][1][1] == 'Your meeting room booking for tomorrow'

    def test_resource_email_addresses_are_ignored(self):
        self.events['items'][0].update({
            u'organizer': {
                u'email': u'digital.cabinet-office.gov.uk@example.com',
            },
        })
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert len(self.server_mock.mock_calls) == 1
        assert self.server_mock.mock_calls[0][1][1][0] != 'digital.cabinet-office.gov.uk@example.com'

    def test_error_sending_email_sends_email_to_admin(self):
        self.server_mock.sendmail.side_effect = [Exception('Something went wrong'), True, True]
        self.calendar_mock.events.return_value.list.return_value.execute.return_value = self.events

        email_reminder = EmailReminder()
        email_reminder.send_reminders()

        assert self.server_mock.mock_calls[1][1][1][0] == 'admin@example.com'
        assert 'Subject: Error sending email to test@example.com' in self.server_mock.mock_calls[1][1][2]
        assert 'A wild error appeared! $$$ Something went wrong' in self.server_mock.mock_calls[1][1][2]
