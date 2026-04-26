from unittest.mock import MagicMock, patch

import pytest

from dtos.user import UserDTO
from dtos.user_create_request import UserCreateRequest
from errors import ConflictError, NotFoundError, ValidationError
from models import user
from objects.email import Email
from objects.password import Password
from objects.username import Username


@patch("models.user.firestore.client")
def test_find_by_username_success(mock_firestore):
    mock_db = mock_firestore.return_value
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.get.side_effect = lambda field: {
        "username": "testuser",
        "uid": "123",
        "email": "test@test.com",
        "created_at": "2024-01-01",
    }[field]

    mock_db.collection.return_value.where.return_value.limit.return_value.get.return_value = [
        mock_doc
    ]

    res = user.find_by_username(Username("testuser"))

    assert isinstance(res, UserDTO)
    assert res.username == "testuser"
    assert res.uid == "123"


def test_find_by_username_invalid():
    with pytest.raises(ValidationError) as exc:
        user.find_by_username(Username("ab"))
    assert exc.value.toDict()["name"] == "ValidationError"


@patch("models.user.firestore.client")
def test_find_by_username_not_found(mock_firestore):
    mock_db = mock_firestore.return_value
    mock_db.collection.return_value.where.return_value.limit.return_value.get.return_value = []

    with pytest.raises(NotFoundError) as exc:
        user.find_by_username(Username("nonexistent"))
    assert exc.value.toDict()["name"] == "NotFoundError"


@patch("models.user.auth.create_user")
@patch("models.user.firestore.client")
def test_create_user_success(mock_firestore, mock_create_user):
    mock_db = mock_firestore.return_value
    mock_db.collection.return_value.where.return_value.get.return_value = []

    mock_firebase_user = MagicMock()
    mock_firebase_user.display_name = "newuser"
    mock_firebase_user.email = "new@test.com"
    mock_firebase_user.uid = "uid123"
    mock_firebase_user.user_metadata.creation_timestamp = 123456789
    mock_create_user.return_value = mock_firebase_user

    request = UserCreateRequest(
        username=Username("newuser"),
        email=Email("new@test.com"),
        password=Password("password123"),
    )

    res = user.create(request)

    assert res.username == "newuser"
    assert mock_create_user.called


@patch("models.user.firestore.client")
def test_create_user_conflict(mock_firestore):
    mock_db = mock_firestore.return_value
    mock_db.collection.return_value.where.return_value.get.return_value = [MagicMock()]

    request = UserCreateRequest(
        username=Username("existing"),
        email=Email("new@test.com"),
        password=Password("password123"),
    )

    with pytest.raises(ConflictError) as exc:
        user.create(request)
    assert exc.value.toDict()["name"] == "ConflictError"
