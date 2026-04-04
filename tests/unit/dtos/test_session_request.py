import pytest

from dtos.session_request import SessionRequest
from errors import ValidationError


def test_with_valid_data():
    inputs = {
        "email": "usuario@exemplo.com",
        "password": "senha123",
    }

    session_request = SessionRequest.from_dict(inputs)

    assert session_request.email.value == inputs["email"]
    assert session_request.password.value == inputs["password"]


def test_with_valid_data_minimum_password():
    inputs = {
        "email": "test@test.com",
        "password": "123456",
    }

    session_request = SessionRequest.from_dict(inputs)

    assert session_request.email.value == inputs["email"]
    assert session_request.password.value == inputs["password"]


def test_with_invalid_email_no_at_symbol():
    inputs = {
        "email": "usuario.exemplo.com",
        "password": "senha123",
    }

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_invalid_password_too_short():
    inputs = {
        "email": "usuario@exemplo.com",
        "password": "12345",
    }

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_empty_email():
    inputs = {
        "email": "",
        "password": "senha123",
    }

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_empty_password():
    inputs = {
        "email": "usuario@exemplo.com",
        "password": "",
    }

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_both_fields_empty():
    inputs = {
        "email": "",
        "password": "",
    }

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_missing_email_field():
    inputs = {
        "password": "senha123",
    }

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_missing_password_field():
    inputs = {
        "email": "usuario@exemplo.com",
    }

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_no_fields():
    inputs = {}

    with pytest.raises(ValidationError) as error:
        SessionRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
