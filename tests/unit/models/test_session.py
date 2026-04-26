from datetime import timedelta
from unittest.mock import patch

import pytest
from firebase_admin import auth, exceptions

from dtos.session_create import SessionCreateDTO
from errors import ValidationError
from models import session


def test_create_session_success():
    session_data = SessionCreateDTO(id_token="fake-token")
    with patch("models.session.auth.create_session_cookie") as mock_create:
        mock_create.return_value = "fake-session-cookie"

        cookie = session.create(session_data)

        assert cookie == "fake-session-cookie"
        mock_create.assert_called_once_with(
            id_token="fake-token",
            expires_in=timedelta(seconds=session.DURATION_IN_SECONDS),
        )


def test_verify_cookie_success():
    with patch("models.session.auth.verify_session_cookie") as mock_verify:
        mock_verify.return_value = {"uid": "user123", "email": "test@test.com"}

        decoded = session.verify_cookie("valid-cookie")

        assert decoded.uid == "user123"
        assert decoded.email == "test@test.com"
        mock_verify.assert_called_once_with("valid-cookie", check_revoked=True)


def test_create_session_empty_token():
    session_data = SessionCreateDTO(id_token="")
    with pytest.raises(ValidationError) as exc:
        session.create(session_data)
    assert exc.value.toDict() == {
        "name": "ValidationError",
        "message": "O idToken não pode ser vazio.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_create_session_invalid_duration():
    too_long = timedelta(days=15)
    session_data = SessionCreateDTO(id_token="token")
    with pytest.raises(ValidationError) as exc:
        session.create(session_data, duration=too_long)
    assert exc.value.toDict() == {
        "name": "ValidationError",
        "message": "Duração da sessão é tem que ser menor que 14 dias.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_verify_cookie_empty():
    with pytest.raises(ValidationError) as exc:
        session.verify_cookie("")
    assert exc.value.toDict() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro ao validar o cookie: o cookie não pode ser vázio.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


@pytest.mark.parametrize(
    "firebase_exc, expected_err_dict",
    [
        (
            auth.InvalidIdTokenError("Invalid"),
            {
                "name": "UnauthorizedError",
                "message": "Não foi possível criar a sessão. O ID token não é um token de código do Firebase válido.",
                "action": "Verifique os dados e tente novamente.",
                "code": 401,
            },
        ),
        (
            auth.ExpiredIdTokenError("Expired", {}),
            {
                "name": "UnauthorizedError",
                "message": "Não foi possível criar a sessão. O ID token não é um token de código do Firebase válido.",
                "action": "Verifique os dados e tente novamente.",
                "code": 401,
            },
        ),
        (
            auth.RevokedIdTokenError("Revoked"),
            {
                "name": "UnauthorizedError",
                "message": "Não foi possível criar a sessão. O ID token não é um token de código do Firebase válido.",
                "action": "Verifique os dados e tente novamente.",
                "code": 401,
            },
        ),
        (
            ValueError("Value error"),
            {
                "name": "ServiceError",
                "message": "Ocorreu um erro ao processar a solicitação de sessão.",
                "action": "Entre em contado com o suporte.",
                "code": 503,
            },
        ),
        (
            exceptions.FirebaseError("Code", "Msg"),
            {
                "name": "ServiceError",
                "message": "Ocorreu um erro ao se comunicar com o serviço de autenticação.",
                "action": "Entre em contado com o suporte.",
                "code": 503,
            },
        ),
    ],
)
def test_create_session_firebase_errors(firebase_exc, expected_err_dict):
    session_data = SessionCreateDTO(id_token="token")
    with patch("models.session.auth.create_session_cookie") as mock_create:
        mock_create.side_effect = firebase_exc
        with pytest.raises(Exception) as exc:
            session.create(session_data)
        assert exc.value.toDict() == expected_err_dict


@pytest.mark.parametrize(
    "firebase_exc, expected_err_dict",
    [
        (
            auth.ExpiredSessionCookieError("Expired", {}),
            {
                "name": "UnauthorizedError",
                "message": "Ocorreu um erro ao verificar a sessão: sessão expirada ou revogada.",
                "action": "Verifique os dados e tente novamente.",
                "code": 401,
            },
        ),
        (
            auth.RevokedSessionCookieError("Revoked"),
            {
                "name": "UnauthorizedError",
                "message": "Ocorreu um erro ao verificar a sessão: sessão expirada ou revogada.",
                "action": "Verifique os dados e tente novamente.",
                "code": 401,
            },
        ),
        (
            auth.InvalidSessionCookieError("Invalid"),
            {
                "name": "UnauthorizedError",
                "message": "Ocorreu um erro ao validar o cookie de sessão. O cookie não é um cookie de sessão do Firebase válido.",
                "action": "Verifique os dados e tente novamente.",
                "code": 401,
            },
        ),
        (
            auth.CertificateFetchError("Fetch error", Exception("cause")),
            {
                "name": "ServiceError",
                "message": "Ocorreu um erro ao verificar o cookie: serviço de autenticação indisponível.",
                "action": "Entre em contado com o suporte.",
                "code": 503,
            },
        ),
        (
            Exception("Generic"),
            {
                "name": "ServiceError",
                "message": "Ocorreu um erro de comunicação com o serviço de verificação.",
                "action": "Entre em contado com o suporte.",
                "code": 503,
            },
        ),
    ],
)
def test_verify_cookie_firebase_errors(firebase_exc, expected_err_dict):
    with patch("models.session.auth.verify_session_cookie") as mock_verify:
        mock_verify.side_effect = firebase_exc
        with pytest.raises(Exception) as exc:
            session.verify_cookie("some-cookie")
        assert exc.value.toDict() == expected_err_dict
