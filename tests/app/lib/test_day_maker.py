import pytest
from app.lib import day_maker

rooms = [
    {
        'resourceEmail': 'test@example.com'
    }
]

test_data = {
    'test@example.com': {
        'busy': [
            {u'start': u'2016-01-01T09:30:00Z', u'end': u'2016-01-01T11:30:00Z'},
            {u'start': u'2016-01-01T13:30:00Z', u'end': u'2016-01-01T15:30:00Z'}
        ]
    }
}


test_data_2 = {
    'test@example.com': {
        'busy': [
            {u'start': u'2016-01-01T08:30:00Z', u'end': u'2016-01-01T09:30:00Z'},
            {u'start': u'2016-01-01T10:30:00Z', u'end': u'2016-01-01T11:30:00Z'},
            {u'start': u'2016-01-01T11:30:00Z', u'end': u'2016-01-01T12:30:00Z'},
            {u'start': u'2016-01-01T12:30:00Z', u'end': u'2016-01-01T13:15:00Z'},
            {u'start': u'2016-01-01T13:30:00Z', u'end': u'2016-01-01T15:15:00Z'}
        ]
    }
}

test_data_3 = {
    'test@example.com': {
        'busy': []
    }
}


class TestDayMaker():

    def test_create_full_days(self):
        output = day_maker.create_full_days(rooms, test_data)
        expected = {
            'test@example.com': [
                {'times': '00:00 to 09:30', 'length': 570, 'status': 'Free', 'from_to': '20160101T000000Z/20160101T093000Z'},
                {'times': '09:30 to 11:30', 'length': 120, 'status': 'Busy', 'from_to': '20160101T093000Z/20160101T113000Z'},
                {'times': '11:30 to 13:30', 'length': 120, 'status': 'Free', 'from_to': '20160101T113000Z/20160101T133000Z'},
                {'times': '13:30 to 15:30', 'length': 120, 'status': 'Busy', 'from_to': '20160101T133000Z/20160101T153000Z'},
                {'times': '15:30 to 00:00', 'length': 510, 'status': 'Free', 'from_to': '20160101T153000Z/20160102T000000Z'}
            ]
        }
        assert output == expected

    def test_create_full_days_with_more_data(self):
        output = day_maker.create_full_days(rooms, test_data_2)
        expected = {
            'test@example.com': [
                {'times': '00:00 to 08:30', 'length': 510, 'status': 'Free', 'from_to': '20160101T000000Z/20160101T083000Z'},
                {'times': '08:30 to 09:30', 'length': 60, 'status': 'Busy', 'from_to': '20160101T083000Z/20160101T093000Z'},
                {'times': '09:30 to 10:30', 'length': 60, 'status': 'Free', 'from_to': '20160101T093000Z/20160101T103000Z'},
                {'times': '10:30 to 11:30', 'length': 60, 'status': 'Busy', 'from_to': '20160101T103000Z/20160101T113000Z'},
                {'times': '11:30 to 12:30', 'length': 60, 'status': 'Busy', 'from_to': '20160101T113000Z/20160101T123000Z'},
                {'times': '12:30 to 13:15', 'length': 45, 'status': 'Busy', 'from_to': '20160101T123000Z/20160101T131500Z'},
                {'times': '13:15 to 13:30', 'length': 15, 'status': 'Free', 'from_to': '20160101T131500Z/20160101T133000Z'},
                {'times': '13:30 to 15:15', 'length': 105, 'status': 'Busy', 'from_to': '20160101T133000Z/20160101T151500Z'},
                {'times': '15:15 to 00:00', 'length': 525, 'status': 'Free', 'from_to': '20160101T151500Z/20160102T000000Z'}
            ]
        }
        assert output == expected

    def test_create_full_days_with_no_meetings_booked(self):
        output = day_maker.create_full_days(rooms, test_data_3)
        expected = {
            'test@example.com': [
                {'times': '00:00 to 00:00', 'length': 1440, 'status': 'Free', 'from_to': '20191127T000000Z/20191128T000000Z'}
            ]
        }
        assert output == expected
