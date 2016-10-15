from .context import fetch_latest
import pytest

@pytest.mark.parametrize('label,expected', [
    ('Excellent', 'excellent'),
    ('Very good', 'very_good'),
])
def test_format_label(label, expected):
    assert fetch_latest.format_label(label) == expected


@pytest.mark.parametrize('value,expected', [
    ('253', 253),
    ('1,534', 1534),
    ('   1,534', 1534),
])
def test_format_value(value, expected):
    assert fetch_latest.format_value(value) == expected

