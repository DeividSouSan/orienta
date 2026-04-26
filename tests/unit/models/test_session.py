from datetime import timedelta
from unittest.mock import patch

import pytest
from firebase_admin import auth, exceptions

from errors import ServiceError, UnauthorizedError, ValidationError
from models import session


def test_create_session_success():
    mock_user = {"idToken": "fake-token"}
    with patch("models.session.auth.create_session_cookie") as mock_create:
        mock_create.return_value = "fake-session-cookie"

        cookie = session.create(mock_user)

        assert cookie == "fake-session-cookie"
        mock_create.assert_called_once_with(
            id_token="fake-token",
            expires_in=timedelta(seconds=session.DURATION_IN_SECONDS),
        )


def test_verify_cookie_success():
    with patch("models.session.auth.verify_session_cookie") as mock_verify:
        mock_verify.return_value = {"uid": "user123"}

        decoded = session.verify_cookie("valid-cookie")

        assert decoded["uid"] == "user123"
        mock_verify.assert_called_once_with("valid-cookie", check_revoked=True)


def test_create_session_empty_token():
    with pytest.raises(ValidationError) as exc:
        session.create({"idToken": ""})
    assert "O idToken não pode ser vazio." in str(exc.value)


def test_create_session_invalid_duration():
    too_long = timedelta(days=15)
    with pytest.raises(ValidationError) as exc:
        session.create({"idToken": "token"}, duration=too_long)
    assert "Duração da sessão é tem que ser menor que 14 dias." in str(exc.value)


def test_verify_cookie_empty():
    with pytest.raises(ValidationError) as exc:
        session.verify_cookie("")
    assert "o cookie não pode ser vázio." in str(exc.value)


@pytest.mark.parametrize(
    "firebase_exc, expected_err",
    [
        (auth.InvalidIdTokenError("Invalid"), UnauthorizedError),
        (auth.ExpiredIdTokenError("Expired", {}), UnauthorizedError),
        (auth.RevokedIdTokenError("Revoked"), UnauthorizedError),
        (ValueError("Value error"), ServiceError),
        (exceptions.FirebaseError("Code", "Msg"), ServiceError),
    ],
)
def test_create_session_firebase_errors(firebase_exc, expected_err):
    with patch("models.session.auth.create_session_cookie") as mock_create:
        mock_create.side_effect = firebase_exc
        with pytest.raises(expected_err):
            session.create({"idToken": "token"})


@pytest.mark.parametrize(
    "firebase_exc, expected_err, expected_msg",
    [
        (
            auth.ExpiredSessionCookieError("Expired", {}),
            UnauthorizedError,
            "sessão expirada ou revogada",
        ),
        (
            auth.RevokedSessionCookieError("Revoked"),
            UnauthorizedError,
            "sessão expirada ou revogada",
        ),
        (
            auth.InvalidSessionCookieError("Invalid"),
            UnauthorizedError,
            "O cookie não é um cookie de sessão do Firebase válido",
        ),
        (
            auth.CertificateFetchError("Fetch error", Exception("cause")),
            ServiceError,
            "serviço de autenticação indisponível",
        ),
        (
            Exception("Generic"),
            ServiceError,
            "erro de comunicação com o serviço de verificação",
        ),
    ],
)
def test_verify_cookie_firebase_errors(firebase_exc, expected_err, expected_msg):
    with patch("models.session.auth.verify_session_cookie") as mock_verify:
        mock_verify.side_effect = firebase_exc
        with pytest.raises(expected_err) as exc:
            session.verify_cookie("some-cookie")
        assert expected_msg in str(exc.value)
