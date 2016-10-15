from .context import fetch_latest
import vcr
import pytest


@vcr.use_cassette('testing/fixtures/chelsea.yml')
def test_chelsea():
    url = 'https://www.tripadvisor.co.uk/Hotel_Review-g155019-d183778-Reviews-Chelsea_Hotel_Toronto-Toronto_Ontario.html'
    expected = {
        'excellent': 873,
        'very_good': 1646,
        'average': 1275,
        'poor': 536,
        'terrible': 322,
    }

    assert fetch_latest.fetch_reviews(url, kind='hotel') == expected


@vcr.use_cassette('testing/fixtures/reversing_rapids.yml')
def test_reversing_rapids():
    url = 'https://www.tripadvisor.co.uk/Attraction_Review-g154960-d318433-Reviews-Reversing_Falls-Saint_John_New_Brunswick.html'
    expected = {
        'excellent': 251,
        'very_good': 222,
        'average': 216,
        'poor': 62,
        'terrible': 27,
    }

    assert fetch_latest.fetch_reviews(url, kind='attraction') == expected


def test_format_results():
    results = {
        'excellent': 251,
        'very_good': 222,
        'average': 216,
        'poor': 62,
        'terrible': 27,
    }

    expected = 'excellent:251,very good:222,average:216,poor:62,terrible:27'

    assert fetch_latest.format_results(results) == expected
