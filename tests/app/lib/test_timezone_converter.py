from app.lib.timezone_converter import TimeZoneConverter


class TestTimeZoneConverter():
    def test_it_converts_utc_times_to_london_times_out_of_BST(self):
        google_api_utc_time_string = u'2016-01-01T09:30:00Z'
        converted_time_string = TimeZoneConverter.utc_to_london(google_api_utc_time_string)

        assert converted_time_string == u'2016-01-01T09:30:00'

    def test_it_converts_utc_times_to_london_times_during_BST(self):
        google_api_utc_time_string = u'2016-10-28T09:30:00Z'
        converted_time_string = TimeZoneConverter.utc_to_london(google_api_utc_time_string)

        assert converted_time_string == u'2016-10-28T10:30:00'

    def test_it_converts_correctly_on_the_day_the_clocks_go_forward_pre_change(self):
        google_api_utc_time_string = u'2017-03-26T00:59:59Z'
        converted_time_string = TimeZoneConverter.utc_to_london(google_api_utc_time_string)

        assert converted_time_string == u'2017-03-26T00:59:59'

    def test_it_converts_correctly_on_the_day_the_clocks_go_forward_post_change(self):
        google_api_utc_time_string = u'2017-03-26T01:00:00Z'
        converted_time_string = TimeZoneConverter.utc_to_london(google_api_utc_time_string)

        assert converted_time_string == u'2017-03-26T02:00:00'

    def test_it_converts_correctly_on_the_day_the_clocks_go_back_pre_change(self):
        google_api_utc_time_string = u'2016-10-30T00:59:59Z'
        converted_time_string = TimeZoneConverter.utc_to_london(google_api_utc_time_string)

        assert converted_time_string == u'2016-10-30T01:59:59'

    def test_it_converts_correctly_on_the_day_the_clocks_go_back_post_change(self):
        google_api_utc_time_string = u'2016-10-30T01:00:00Z'
        converted_time_string = TimeZoneConverter.utc_to_london(google_api_utc_time_string)

        assert converted_time_string == u'2016-10-30T01:00:00'
