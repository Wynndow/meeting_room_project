import mock
from app.lib.smtp_server import LoggedInServer

class TestSmtpServer():

    @mock.patch('app.lib.smtp_server.smtplib')
    @mock.patch('app.lib.smtp_server.current_app')
    def test_logged_in_server_gets_created_with_correct_creds(self, current_app, smtplib):
        current_app.config = {
            'MAIL_SERVER': 'server',
            'MAIL_PORT': '101',
            'MAIL_USERNAME': 'Mr. User',
            'MAIL_PASSWORD': 'dead secret'
        }
        smtplib_server_mock = mock.MagicMock()
        smtplib.SMTP.return_value = smtplib_server_mock

        logged_in_server = LoggedInServer()
        mock_calls = smtplib_server_mock.mock_calls

        assert smtplib.SMTP.called_with('server', '101')
        expected_calls = [mock.call.ehlo(), mock.call.starttls(), mock.call.login('Mr. User', 'dead secret')]
        assert expected_calls == mock_calls

    @mock.patch('app.lib.smtp_server.smtplib')
    @mock.patch('app.lib.smtp_server.current_app')
    def test_sendmail_correctly_calls_the_smtp_library(self, current_app, smtplib):
        current_app = mock.MagicMock()
        smtplib_server_mock = mock.MagicMock()
        smtplib.SMTP.return_value = smtplib_server_mock
        logged_in_server = LoggedInServer()
        logged_in_server.sendmail('sender', 'receiver', 'message')

        smtplib_server_mock.sendmail.assert_called_once_with('sender', 'receiver', 'message')
