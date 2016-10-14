from .context import fetch_latest
import vcr
import pytest

@vcr.use_cassette('testing/cassettes/a.yml')
@pytest.mark.parametrize('url,expected', [
    ( 'https://www.tripadvisor.co.uk/Hotel_Review-g155019-d183778-Reviews-Chelsea_Hotel_Toronto-Toronto_Ontario.html', {
        'excellent': 873,
        'very good': 1646,
        'average': 1275,
        'poor': 536,
        'terrible': 322,
    }),
    ('https://www.tripadvisor.co.uk/Attraction_Review-g154960-d318433-Reviews-Reversing_Falls-Saint_John_New_Brunswick.html', {
        'excellent': 251,
        'very good': 222,
        'average': 216,
        'poor': 62,
        'terrible': 27,
    }),
])
def test_chelsea(url, expected):
    assert fetch_latest.fetch_reviews(url) == expected
