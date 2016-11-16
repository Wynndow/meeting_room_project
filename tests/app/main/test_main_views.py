import pytest
from app import create_app


class TestMainView():
    def setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_home_page(self):
        res = self.client.get('/')

        assert res.status_code == 200
        assert 'GDS Meeting Room Availablity' in res.get_data(as_text=True)

    def test_error_page_rendered_for_incorrect_date(self):
        res = self.client.get('/?date=2016-50-17', follow_redirects=True)

        assert res.status_code == 400
        assert "You&#39;ve submitted an invalid date!" in res.get_data(as_text=True)

    def test_error_page_rendered_for_incorrect_floor(self):
        res = self.client.get('?floor=not_a_floor', follow_redirects=True)

        assert res.status_code == 400
        assert "You&#39;ve submitted an invalid floor!" in res.get_data(as_text=True)
