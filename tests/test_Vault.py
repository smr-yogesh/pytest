import pytest
import source.Vault as v
import logging
import unittest.mock as mock

logger = logging.getLogger(__name__)


def test_magical_vault_initialization(magical_vault):

    assert magical_vault.security_clearance_limit == 3


def test_item_initialization(my_item):

    assert my_item.name == "gold"
    assert my_item.clearance_level == 3


# Deposit test
def test_deposit_item(my_item, magical_vault, caplog):
    caplog.set_level(logging.INFO)
    v.MagicalVault.deposit_item(magical_vault, my_item, 3)
    assert f"Successfully vaulted item: {my_item.name}" in caplog.text


# test if it fails
def test_deposit_item_fail(my_item, magical_vault, caplog):
    with pytest.raises(v.VaultSecurityError):
        v.MagicalVault.deposit_item(magical_vault, my_item, 1)


@pytest.mark.parametrize(
    "item_data",
    [
        ("1", "gold", 3),
        ("1", "gold", 3),
    ],
)
def test_deposit_same_item(item_data, magical_vault):
    item = v.VaultItem(*item_data)

    magical_vault.deposit_item(item, 3)

    with pytest.raises(ValueError):
        magical_vault.deposit_item(item, 3)


# test checkout item
def test_check_out_item(my_item, magical_vault):
    v.MagicalVault.deposit_item(magical_vault, my_item, 3)
    item = v.MagicalVault.check_out_item(magical_vault, my_item.item_id, "jack", 4)
    assert item.item_id == my_item.item_id


# Test check out item not found
def test_check_out_item_not_found(my_item, magical_vault):
    with pytest.raises(v.ArtifactNotFoundError):
        v.MagicalVault.check_out_item(magical_vault, my_item.item_id, "jack", 4)


# test if already checked out
def test_already_checkd_out_(my_item, magical_vault):
    v.MagicalVault.deposit_item(magical_vault, my_item, 3)
    v.MagicalVault.check_out_item(magical_vault, my_item.item_id, "jack", 4)
    with pytest.raises(RuntimeError):
        v.MagicalVault.check_out_item(magical_vault, my_item.item_id, "jack", 4)


# Insufficient borrower clearance (VaultSecurityError)
def test_Insufficient_borrower_clearance(my_item, magical_vault):
    v.MagicalVault.deposit_item(magical_vault, my_item, 3)
    with pytest.raises(v.VaultSecurityError):
        v.MagicalVault.check_out_item(magical_vault, my_item.item_id, "jack", 1)


# requires master vault clearance
def test_requires_master_vault_clearance(cursed_item, magical_vault):
    v.MagicalVault.deposit_item(magical_vault, cursed_item, 3)
    with pytest.raises(v.VaultSecurityError):
        v.MagicalVault.check_out_item(magical_vault, cursed_item.item_id, "jack", 1)


# get_audit_trail
def test_get_audit_trail(magical_vault, my_item, cursed_item):
    v.MagicalVault.deposit_item(magical_vault, my_item, 3)
    v.MagicalVault.get_audit_trail(magical_vault)
    assert v.MagicalVault.get_audit_trail(magical_vault) == ["DEPOSIT: gold (1)"]


@mock.patch("requests.post")
def test_mock_request_cursed(mock_post, magical_vault, cursed_item):

    mock_post.return_value.status_code = 200

    # 2. Run the methods under test (with "jack" as a string)
    v.MagicalVault.deposit_item(magical_vault, cursed_item, 3)
    v.MagicalVault.check_out_item(magical_vault, cursed_item.item_id, "jack", 3)

    mock_post.assert_called_once()


@mock.patch("requests.post")
def test_mock_request_not_cursed(mock_post, magical_vault, my_item):

    mock_post.return_value.status_code = 200

    # 2. Run the methods under test (with "jack" as a string)
    v.MagicalVault.deposit_item(magical_vault, my_item, 3)
    v.MagicalVault.check_out_item(magical_vault, my_item.item_id, "jack", 3)

    with pytest.raises(AssertionError):
        mock_post.assert_called_once()
