import pytest
from app import create_app


class TestMainView():
    def setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_whitechapel_page(self):
        res = self.client.get('/')

        assert res.status_code == 200
        assert 'Whitechapel - go to <a href="/aviation">Aviation House</a>' in res.get_data(as_text=True)
        assert 'GDS Meeting Room Availablity' in res.get_data(as_text=True)

    def test_aviation_house_page(self):
        res = self.client.get('/aviation')

        assert res.status_code == 200
        assert 'Aviation House - go to <a href="/">Whitechapel</a>' in res.get_data(as_text=True)
        assert 'GDS Meeting Room Availablity' in res.get_data(as_text=True)

    def test_error_page_rendered_for_incorrect_date(self):
        res = self.client.get('/?date=2016-50-17', follow_redirects=True)

        assert res.status_code == 400
        assert "You&#39;ve submitted an invalid date!" in res.get_data(as_text=True)

    def test_error_page_rendered_for_incorrect_floor(self):
        res = self.client.get('/?room_group=not_a_floor', follow_redirects=True)

        assert res.status_code == 400
        assert "You&#39;ve submitted an invalid floor or room type!" in res.get_data(as_text=True)
