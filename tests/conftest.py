import pytest
import source.shapes as s
import source.Vault as v


# test with fixtures
# conftest is global variable file for fixtures
@pytest.fixture
def my_rectangle():
    return s.Rectangle(20, 40)


@pytest.fixture
def weird_rectangle():
    return s.Rectangle(5, 6)


@pytest.fixture
def my_item():
    return v.VaultItem("1", "gold", 3)


@pytest.fixture
def cursed_item():
    return v.VaultItem("2", "gold", 3, True)


@pytest.fixture
def magical_vault():
    return v.MagicalVault("1", 3)
