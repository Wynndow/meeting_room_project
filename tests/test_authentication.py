import mock
import pytest
from app.authentication import requires_authentication, token_is_valid, get_token_from_headers


class TestGetTokenFromHeaders():
    def test_it_returns_token_from_correct_header(self):
        assert get_token_from_headers({'Authorization': 'Bearer iAmTheToken'}) == 'iAmTheToken'

    def test_it_returns_none_if_header_value_incorrect(self):
        assert not get_token_from_headers({'Authorization': 'Wrong! iAmTheToken'})

    def test_it_returns_none_if_header_key_incorrect(self):
        assert not get_token_from_headers({'Authorisation': 'Bearer iAmTheToken'})


@mock.patch('app.authentication.current_app')
class TestTokenIsValid():
    def test_it_returns_true_if_token_matches_config(self, current_app):
        current_app.config = {'AUTH_TOKEN': 'iAmTheToken'}
        assert token_is_valid('iAmTheToken')

    def test_it_returns_false_if_token_does_not_match_config(self, current_app):
        current_app.config = {'AUTH_TOKEN': 'iAmNotTheToken'}
        assert not token_is_valid('iAmTheToken')


@mock.patch('app.authentication.current_app')
class TestRequiresAuthentication():
    @mock.patch('app.authentication.request')
    def test_it_does_not_abort_if_all_is_well(self, request, current_app):
        current_app.config = {
            'AUTH_REQUIRED': True,
            'AUTH_TOKEN': 'iAmTheToken'
        }
        request.headers = {
            'Authorization': 'Bearer iAmTheToken'
        }

        assert not requires_authentication()

    @mock.patch('app.authentication.request')
    @mock.patch('app.authentication.abort')
    def test_it_aborts_if_no_token(self, abort, request, current_app):
        current_app.config = {
            'AUTH_REQUIRED': True,
            'AUTH_TOKEN': 'iAmTheToken'
        }
        request.headers = {
            'Authorization': 'iAmNotTheToken'
        }

        requires_authentication()
        abort.assert_any_call(401, "Unauthorized; bearer token must be provided")

    @mock.patch('app.authentication.request')
    @mock.patch('app.authentication.abort')
    def test_it_aborts_if_incorrect_token(self, abort, request, current_app):
        current_app.config = {
            'AUTH_REQUIRED': True,
            'AUTH_TOKEN': 'iAmTheToken'
        }
        request.headers = {
            'Authorization': 'Bearer iAmNotTheToken'
        }

        requires_authentication()
        abort.assert_any_call(403, "Forbidden; invalid bearer token provided iAmNotTheToken")
