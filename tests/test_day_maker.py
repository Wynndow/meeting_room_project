import pytest
from app.lib import day_maker

test_data = [{u'start': u'2016-06-03T09:30:00Z', u'end': u'2016-06-03T11:30:00Z'},
             {u'start': u'2016-06-03T13:30:00Z', u'end': u'2016-06-03T15:30:00Z'}]

test_data_2 = [{u'start': u'2016-06-03T08:30:00Z', u'end': u'2016-06-03T09:30:00Z'},
               {u'start': u'2016-06-03T10:30:00Z', u'end': u'2016-06-03T11:30:00Z'},
               {u'start': u'2016-06-03T11:30:00Z', u'end': u'2016-06-03T12:30:00Z'},
               {u'start': u'2016-06-03T12:30:00Z', u'end': u'2016-06-03T13:15:00Z'},
               {u'start': u'2016-06-03T13:30:00Z', u'end': u'2016-06-03T15:15:00Z'}]

class TestDayMaker():

    def test_create_full_day_json(self):
        output = day_maker.create_full_day_json(test_data)
        expected = [{'times': '00:00 to 09:30', 'length': 570, 'status': 'Free'},
                    {'times': '09:30 to 11:30', 'length': 120, 'status': 'Busy'},
                    {'times': '11:30 to 13:30', 'length': 120, 'status': 'Free'},
                    {'times': '13:30 to 15:30', 'length': 120, 'status': 'Busy'},
                    {'times': '15:30 to 00:00', 'length': 510, 'status': 'Free'}]
        assert output == expected

    def test_create_full_day_json_with_more_data(self):
        output = day_maker.create_full_day_json(test_data_2)
        expected = [{'times': '00:00 to 08:30', 'length': 510, 'status': 'Free'},
                    {'times': '08:30 to 09:30', 'length': 60, 'status': 'Busy'},
                    {'times': '09:30 to 10:30', 'length': 60, 'status': 'Free'},
                    {'times': '10:30 to 11:30', 'length': 60, 'status': 'Busy'},
                    {'times': '11:30 to 12:30', 'length': 60, 'status': 'Busy'},
                    {'times': '12:30 to 13:15', 'length': 45, 'status': 'Busy'},
                    {'times': '13:15 to 13:30', 'length': 15, 'status': 'Free'},
                    {'times': '13:30 to 15:15', 'length': 105, 'status': 'Busy'},
                    {'times': '15:15 to 00:00', 'length': 525, 'status': 'Free'}]
        assert output == expected

    def test_create_full_day_json_with_no_meetings_booked(self):
        output = day_maker.create_full_day_json([])
        expected = [{'times': '00:00 to 00:00', 'length': 1440, 'status': 'Free'}]
        assert output == expected


    def test_time_in_minutes(self):
        string = '2016-06-03T09:30:00Z'
        seconds = day_maker._time_in_minutes(string)
        assert seconds == 570

    def test_time_in_minutes_with_short_string(self):
        string = '09:30'
        seconds = day_maker._time_in_minutes(string)
        assert seconds == 570
