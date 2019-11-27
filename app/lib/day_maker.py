from .booking import Booking
from .timezone_converter import TimeZoneConverter
from datetime import datetime, timedelta

DATE_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S'
FREE_STATUS = 'Free'
BUSY_STATUS = 'Busy'
EXTRA_STRING_CHARACTERS = -6


def create_full_days(rooms, free_busy):
    output = {}
    for room in rooms:
        booking_object_list = _create_booking_object_list(free_busy.get(room.get('resourceEmail')).get('busy'))
        formatted_list = [
            {'times': b.times(), 'length': b.length(), 'status': b.status, 'from_to': b.from_to_for_calendar_link()}
            for b in booking_object_list
        ]
        output[room.get('resourceEmail')] = formatted_list
    return output


def _create_booking_object_list(bookings):
    output = []
    if not bookings:
        return [_create_full_day_free_booking()]

    _convert_booking_times_to_local(bookings)

    for booking in bookings:
        if not output:
            free_booking, busy_booking = _create_first_free_and_busy_bookings(booking)
            output.append(free_booking)
            output.append(busy_booking)
            continue

        last_booking = output[-1]

        current_booking = _create_current_booking(booking)
        output.append(current_booking)

        if current_booking.is_right_after_(last_booking):
            continue
        else:
            between_bookings = _create_free_time_between_this_booking_and_the_previous(current_booking, last_booking)
            output.insert(-1, between_bookings)

    if _bookings_are_not_till_midnight(output):
        last_free_booking = _create_free_time_between_last_meeting_and_midnight(output)
        output.append(last_free_booking)

    return output


def _create_first_free_and_busy_bookings(booking):
    end = datetime.strptime(booking['start'], DATE_FORMAT_STRING)
    start = end.replace(hour=0, minute=0, second=0)
    times = {
        'start': start,
        'end': end
    }
    free_booking = Booking(times, FREE_STATUS)

    times = {
        'start': datetime.strptime(booking['start'], DATE_FORMAT_STRING),
        'end': datetime.strptime(booking['end'], DATE_FORMAT_STRING)
    }

    busy_booking = Booking(times, BUSY_STATUS)

    return free_booking, busy_booking


def _create_full_day_free_booking():
    times = {
        'start': datetime.now().replace(hour=0, minute=0, second=0),
        'end': (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    }
    return Booking(times, FREE_STATUS)


def _create_free_time_between_this_booking_and_the_previous(current_booking, last_booking):
    times = {
        'start': last_booking.end,
        'end': current_booking.start
    }
    return Booking(times, FREE_STATUS)


def _create_current_booking(booking):
    times = {
        'start': datetime.strptime(booking['start'], DATE_FORMAT_STRING),
        'end': datetime.strptime(booking['end'], DATE_FORMAT_STRING)
    }

    return Booking(times, BUSY_STATUS)


def _bookings_are_not_till_midnight(output):
    return output[-1].end.hour != 0


def _create_free_time_between_last_meeting_and_midnight(output):
    times = {
        'start': output[-1].end,
        'end': (output[-1].end + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    }
    return Booking(times, FREE_STATUS)


def _convert_booking_times_to_local(bookings):
    for booking in bookings:
        booking['start'] = TimeZoneConverter.utc_to_london(booking['start'])
        booking['end'] = TimeZoneConverter.utc_to_london(booking['end'])
