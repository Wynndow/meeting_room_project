import pytest
from app.lib.booking import Booking
from datetime import datetime


class TestBooking():

    def test_times(self, booking_fixture):
        assert booking_fixture.times() == '16:00 to 17:30'

    def test_length(self, booking_fixture):
        assert booking_fixture.length() == 90

    def test_length_for_entirely_free_day(self, full_day_free_booking_fixture):
        assert full_day_free_booking_fixture.length() == 1440

    def test_status(self, booking_fixture):
        assert booking_fixture.status == 'Free'

    def test_is_right_after_returns_true_for_back_to_back_bookings(self):
        booking_1 = Booking(
            {
                'start': datetime(2016, 9, 28, 16, 0, 0),
                'end': datetime(2016, 9, 28, 17, 30, 0)
            },
            'Busy'
        )

        booking_2 = Booking(
            {
                'start': datetime(2016, 9, 28, 17, 30, 0),
                'end': datetime(2016, 9, 28, 18, 30, 0)
            },
            'Busy'
        )

        assert booking_2.is_right_after_(booking_1)

    def test_is_right_after_returns_false_for_separate_bookings(self):
        booking_1 = Booking(
            {
                'start': datetime(2016, 9, 28, 16, 0, 0),
                'end': datetime(2016, 9, 28, 17, 0, 0)
            },
            'Busy'
        )

        booking_2 = Booking(
            {
                'start': datetime(2016, 9, 28, 17, 30, 0),
                'end': datetime(2016, 9, 28, 18, 30, 0)
            },
            'Busy'
        )

        assert not booking_2.is_right_after_(booking_1)
