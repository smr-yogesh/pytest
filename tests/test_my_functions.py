import pytest
import source.my_functions as function
import time


def test_add():
    result = function.add(2, 3)
    assert result == 5


def test_divide():
    result = function.divide(10, 2)
    assert result == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        function.divide(10, 0)


@pytest.mark.slow
def test_very_slow():
    time.sleep(5)
    result = function.divide(10, 2)
    assert result == 5


@pytest.mark.skip(reason="this feature is currently broken")
def test_add_2():
    assert function.add(1, 2) == 3


@pytest.mark.xfail(reason="we know we cannot divide by zero")
def test_divide_zero_broken():
    function.divide(4, 0)
