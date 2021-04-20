import pytest

import echo
from error import InputError


def test_echo():
    '''
    Test echo function, from starter code
    A pytest example
    '''
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    '''
    Test echo function, from starter code
    A pytest example
    '''
    with pytest.raises(InputError):
        assert echo.echo("echo")
