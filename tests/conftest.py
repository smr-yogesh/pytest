import pytest
import source.shapes as s

# test with fixtures
# conftest is global variable file for fixtures


@pytest.fixture
def my_rectangle():
    return s.Rectangle(20, 40)


@pytest.fixture
def weird_rectangle():
    return s.Rectangle(5, 6)
