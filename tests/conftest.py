import pytest
from datetime import datetime
from app.lib.booking import Booking


@pytest.fixture()
def booking_fixture():
    times = {
        'start': datetime(2016, 9, 28, 16, 0, 0),
        'end': datetime(2016, 9, 28, 17, 30, 0)
    }

    return Booking(times, 'Free')


@pytest.fixture()
def full_day_free_booking_fixture():
    times = {
        'start': datetime(2016, 9, 28, 0, 0, 0),
        'end': datetime(2016, 9, 29, 0, 0, 0)
    }

    return Booking(times, 'Free')
