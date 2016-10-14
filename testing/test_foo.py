from .context import fetch_latest
import vcr
import requests

@vcr.use_cassette('testing/cassettes/a.yml')
def test_ratings():
    url = 'https://www.tripadvisor.co.uk/Hotel_Review-g155019-d183778-Reviews-Chelsea_Hotel_Toronto-Toronto_Ontario.html'
    assert fetch_latest.fetch_reviews(url) == {
        'excellent': 873,
        'very good': 1646,
        'average': 1275,
        'poor': 536,
        'terrible': 322,
    }
