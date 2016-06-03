import json

def create_full_day_json(data):
    output = []
    if len(data) == 0:
        return [{'times': '00:00 to 00:00', 'length': 1440, 'status': 'Free'}]
    for booking in data:
        if len(output) == 0:
            length = _time_in_minutes(booking.get('start'))
            times = '00:00 to {}'.format(booking.get('start')[-9:-4])
            _add_block_to_day(output, times, length, 'Free')

            start = length
            end = _time_in_minutes(booking.get('end'))
            length = end - start
            times = '{} to {}'.format(booking.get('start')[-9:-4], booking.get('end')[-9:-4])

            _add_block_to_day(output, times, length, 'Busy')

            continue

        length = _time_in_minutes(booking.get('start')) - _time_in_minutes(output[-1].get('times')[-5:])
        if length == 0:
            length = _time_in_minutes(booking.get('end')) - _time_in_minutes(booking.get('start'))
            times = '{} to {}'.format(booking.get('start')[-9:-4], booking.get('end')[-9:-4])

            _add_block_to_day(output, times, length, 'Busy')
            continue

        times = '{} to {}'.format(output[-1].get('times')[-5:], booking.get('start')[-9:-4])
        _add_block_to_day(output, times, length, 'Free')

        length = _time_in_minutes(booking.get('end')) - _time_in_minutes(booking.get('start'))
        times = '{} to {}'.format(booking.get('start')[-9:-4], booking.get('end')[-9:-4])

        _add_block_to_day(output, times, length, 'Busy')

    if not output[-1].get('times')[-5:] == '00:00' and not len(data) == 0:
        length = 1440 - _time_in_minutes(output[-1].get('times')[-5:])
        times = '{} to {}'.format(output[-1].get('times')[-5:], '00:00')
        _add_block_to_day(output, times, length, 'Free')

    return output

def _add_block_to_day(output, times, length, status):
    output.append({'times': times, 'length': length, 'status': status})


def _time_in_minutes(time_string):
    if len(time_string) > 5:
        components = time_string[-9:-4].split(':')
    else:
        components = time_string.split(':')
    int_components = map(lambda time_comp: int(time_comp), components)
    int_components[0] = int_components[0] * 60
    return sum(int_components)
