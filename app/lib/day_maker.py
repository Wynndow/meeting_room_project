from .booking import Booking
from datetime import datetime, timedelta

DATE_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S'
FREE_STATUS = 'Free'
BUSY_STATUS = 'Busy'
EXTRA_STRING_CHARACTERS = -6


def create_full_days(rooms, free_busy):
    output = {}
    for room in rooms:
        booking_object_list = _create_booking_object_list(free_busy.get(room.get('resourceEmail')).get('busy'))
        formatted_list = [{'times': b.times(), 'length': b.length(), 'status': b.status} for b in booking_object_list]
        output[room.get('resourceEmail')] = formatted_list
    return output


def _create_booking_object_list(bookings):
    output = []
    if not bookings:
        return [_create_full_day_free_booking()]

    for booking in bookings:
        if not output:
            _add_first_free_and_busy_bookings(booking, output)
            continue

        last_booking = output[-1]

        _add_current_booking_to_output(booking, output)

        current_booking = output[-1]

        if current_booking.is_right_after_(last_booking):
            continue
        else:
            _add_free_time_between_this_booking_and_the_previous(current_booking, last_booking, output)

    if _bookings_are_not_till_midnight(output):
        _add_free_time_between_last_meeting_and_midnight(output)

    return output


def _add_first_free_and_busy_bookings(booking, output):
    end = datetime.strptime(booking['start'][:EXTRA_STRING_CHARACTERS], DATE_FORMAT_STRING)
    start = end.replace(hour=0, minute=0, second=0)
    times = {
        'start': start,
        'end': end
    }
    output.append(Booking(times, FREE_STATUS))

    times = {
        'start': datetime.strptime(booking['start'][:EXTRA_STRING_CHARACTERS], DATE_FORMAT_STRING),
        'end': datetime.strptime(booking['end'][:EXTRA_STRING_CHARACTERS], DATE_FORMAT_STRING)
    }

    output.append(Booking(times, BUSY_STATUS))


def _create_full_day_free_booking():
    times = {
        'start': datetime.now().replace(hour=0, minute=0, second=0),
        'end': (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    }
    return Booking(times, FREE_STATUS)


def _add_free_time_between_this_booking_and_the_previous(current_booking, last_booking, output):
    times = {
        'start': last_booking.end,
        'end': current_booking.start
    }
    output.insert(-1, Booking(times, FREE_STATUS))


def _add_current_booking_to_output(booking, output):
    times = {
        'start': datetime.strptime(booking['start'][:EXTRA_STRING_CHARACTERS], DATE_FORMAT_STRING),
        'end': datetime.strptime(booking['end'][:EXTRA_STRING_CHARACTERS], DATE_FORMAT_STRING)
    }

    output.append(Booking(times, BUSY_STATUS))


def _bookings_are_not_till_midnight(output):
    return output[-1].end.hour != 0


def _add_free_time_between_last_meeting_and_midnight(output):
    times = {
        'start': output[-1].end,
        'end': (output[-1].end + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    }
    output.append(Booking(times, FREE_STATUS))
