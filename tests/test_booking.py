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
