from app.lib.user_events import UserEvents


class TestUserEvents():
    def test_it_has_the_correct_attributes(self):
        event = UserEvents('Test Event', 'test@example.com', ['A booking object', 'Another booking object'])

        assert event.name == 'Test Event'
        assert event.email == 'test@example.com'
        assert event.bookings == ['A booking object', 'Another booking object']
