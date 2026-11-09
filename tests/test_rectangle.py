import pytest
import source.shapes as s

# test with fixtures
# @pytest.fixture
# def my_rectangle():
#     return s.Rectangle(20, 40)


# @pytest.fixture
# def weird_rectangle():
#     return s.Rectangle(5, 6)


def test_area(my_rectangle):
    assert my_rectangle.area() == 20 * 40


def test_peremeter(my_rectangle):
    assert my_rectangle.perimeter() == (20 * 2) + (40 * 2)


def test_not_equal(my_rectangle, weird_rectangle):
    assert my_rectangle != weird_rectangle
