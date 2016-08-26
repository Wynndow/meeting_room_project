from .booking import Booking
from datetime import datetime, timedelta

def create_booking_object_list(data):
    output = []
    if not data:
        return output

    for booking in data:
        if not output:
            _add_first_free_and_busy_blocks(booking, output)
            continue

        last_booking = output[-1]

        times = {
            'start': datetime.strptime(booking['start'][:-6], '%Y-%m-%dT%H:%M:%S'),
            'end': datetime.strptime(booking['end'][:-6], '%Y-%m-%dT%H:%M:%S')
        }
        output.append(Booking(times, 'Busy'))
        current_booking = output[-1]

        if last_booking.end == current_booking.start:
            continue

        times = {
            'start': last_booking.end,
            'end': current_booking.start
        }
        output.insert(-1, Booking(times, 'Free'))

    if output[-1].end.hour != 0:
        times = {
            'start': output[-1].end,
            'end': (output[-1].end + timedelta(days=1)).replace(hour=0, minute=0, second=0)
        }
        output.append(Booking(times, 'Free'))
        
    return output

# def parse_api_data_to_objects(data):
#     output = [ Booking(busy_data) for busy_data in data ]
#     return output
#
# def fill_in_free_data(busy_bookings):
#     if not busy_bookings:
#         all_day = {
#             'start': '',
#             'end': ''
#         }
#         return [Booking()]



def create_full_days(rooms, free_busy):
    output = {}
    for room in rooms:
        output[room.get('resourceEmail')] = create_booking_object_list(free_busy.get(room.get('resourceEmail')).get('busy'))
    return output


def _add_last_block_if_end_of_day_is_free(output):
    length = 1440 - _time_in_minutes(output[-1].get('times')[-5:])
    times = '{} to {}'.format(output[-1].get('times')[-5:], '00:00')
    _add_block_to_day(output, times, length, 'Free')


def _add_first_free_and_busy_blocks(booking, output):

    end = datetime.strptime(booking['start'][:-6], '%Y-%m-%dT%H:%M:%S')
    start = end.replace(hour=0, minute=0, second=0)
    times = {
        'start': start,
        'end': end
    }
    output.append(Booking(times, 'Free'))

    times = {
        'start': datetime.strptime(booking['start'][:-6], '%Y-%m-%dT%H:%M:%S'),
        'end': datetime.strptime(booking['end'][:-6], '%Y-%m-%dT%H:%M:%S')
    }

    output.append(Booking(times, 'Busy'))

def _length_and_times_for_busy_block(booking):
    length = _time_in_minutes(booking.get('end')) - _time_in_minutes(booking.get('start'))
    times = '{} to {}'.format(booking.get('start')[11:16], booking.get('end')[11:16])
    return length, times


def _add_block_to_day(output, times, length, status):
    output.append({'times': times, 'length': length, 'status': status})


def _time_in_minutes(time_string):
    if len(time_string) > 5:
        components = time_string[11:16].split(':')
    else:
        components = time_string.split(':')

    int_components = map(lambda time_comp: int(time_comp), components)
    int_components[0] = int_components[0] * 60
    return sum(int_components)
