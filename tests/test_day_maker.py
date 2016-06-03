import pytest
from app.lib import day_maker

test_data = [{u'start': u'2016-06-03T09:30:00Z', u'end': u'2016-06-03T11:30:00Z'}, {u'start': u'2016-06-03T13:30:00Z', u'end': u'2016-06-03T15:30:00Z'}]

class TestDayMaker():

    def test_create_full_day_json(self):
        output = day_maker.create_full_day_json(test_data)
        expected = [{'times': '00:00 to 09:30', 'length': 570, 'status': 'Free'},
                    {'times': '09:30 to 11:30', 'length': 120, 'status': 'Busy'},
                    {'times': '11:30 to 13:30', 'length': 120, 'status': 'Free'},
                    {'times': '13:30 to 15:30', 'length': 120, 'status': 'Busy'},
                    {'times': '15:30 to 00:00', 'length': 510, 'status': 'Free'}]
        assert output == expected

    def test_time_in_minutes(self):
        string = '2016-06-03T09:30:00Z'
        seconds = day_maker._time_in_minutes(string)
        assert seconds == 570

    def test_time_in_minutes_with_short_string(self):
        string = '09:30'
        seconds = day_maker._time_in_minutes(string)
        assert seconds == 570
