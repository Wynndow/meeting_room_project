import pytest
import mock
from datetime import datetime
from app.lib.room_list import RoomList


class TestRoomList():
    def test_it_takes_a_list_of_rooms_as_an_argument(self):
        rooms = ['Big One', 'Little One', 'Cardboard One']
        room_list = RoomList(rooms)
        assert room_list.rooms == rooms

    @mock.patch('app.lib.room_list.current_app')
    def test_get_free_busy_calls_to_api_with_correct_data(self, current_app):
        rooms = [
            {
                'resourceEmail': 'Big One'
            },
            {
                'resourceEmail': 'Little One'
            },
            {
                'resourceEmail': 'Cardboard One'
            }
        ]
        room_list = RoomList(rooms)
        date = str(datetime(2016, 8, 19, 16, 0, 0))[0:10]
        calendar = mock.MagicMock()
        freebusy_return = mock.MagicMock()
        query_return = mock.MagicMock()

        query_return.execute.return_value = {
            'rooms': rooms,
            'date': date
        }
        freebusy_return.query.return_value = query_return
        calendar.freebusy.return_value = freebusy_return
        current_app.config = {'CALENDAR': calendar}

        free_busy_info = room_list.get_free_busy(date)

        assert free_busy_info == {
            'rooms': rooms,
            'date': date
        }
