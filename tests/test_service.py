import pytest
import source.service as service
import unittest.mock as mock
import requests


# Mocking database
@mock.patch("source.service.get_user")
def test_get_user_from_db(mock_get_user):
    mock_get_user.return_value = "mocked Alice"
    user_name = service.get_user(1)

    assert user_name == "mocked Alice"


# Mocking actual API
@mock.patch("requests.get")
def test_get_users(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Leanne Graham"}
    mock_get.return_value = mock_response
    data = service.get_user_api()

    assert data == {"id": 1, "name": "Leanne Graham"}


# Mocking httperror
@mock.patch("requests.get")
def test_get_users_error(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 400
    mock_get.return_value = mock_response
    with pytest.raises(requests.HTTPError):
        service.get_user_api()
