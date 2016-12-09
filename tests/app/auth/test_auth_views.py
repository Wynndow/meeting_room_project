import pytest
import mock
from app import create_app
from flask import current_app


class TestAuthViews():
    def setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    @mock.patch('app.lib.email_reminder.EmailReminder._get_all_days_events')
    @mock.patch('app.lib.email_reminder.LoggedInServer')
    def test_send_mails_returns_204(self, LoggedInServer, _get_all_days_events):
        server_mock = mock.MagicMock()
        LoggedInServer.SMTP.return_value = server_mock
        _get_all_days_events.return_value = []

        with self.app.app_context():
            res = self.client.post(
                '/send_emails',
                headers={
                    'Authorization': 'Bearer {}'.format(current_app.config['AUTH_TOKEN'])
                }
            )

        assert res.status_code == 204
