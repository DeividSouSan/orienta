import pytest

from errors import ValidationError
from objects.email import Email


def test_with_valid_email():
    email = Email("usuario@exemplo.com")

    assert email.value == "usuario@exemplo.com"


def test_with_valid_email_multiple_domains():
    email = Email("usuario@mail.exemplo.com.br")

    assert email.value == "usuario@mail.exemplo.com.br"


def test_with_empty_email():
    with pytest.raises(ValidationError) as error:
        Email("")

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Formato de email inválido.",
        "action": "Forneça um email válido e tente novamente.",
        "code": 400,
    }


def test_with_email_without_at_symbol():
    with pytest.raises(ValidationError) as error:
        Email("usuario.exemplo.com")

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "Formato de email inválido.",
        "action": "Forneça um email válido e tente novamente.",
        "code": 400,
    }


def test_with_email_only_at_symbol():
    email = Email("@")

    # Email básico permite apenas @ (validação simplificada verifica apenas presença de @)
    assert email.value == "@"


def test_with_email_starting_with_at():
    email = Email("@exemplo.com")

    # Email básico permite @ no início (validação simplificada)
    assert email.value == "@exemplo.com"


def test_with_email_ending_with_at():
    email = Email("usuario@")

    # Email básico permite @ no final (validação simplificada)
    assert email.value == "usuario@"


def test_with_multiple_at_symbols():
    email = Email("usuario@@exemplo.com")

    # Email básico permite múltiplos @ (validação simplificada)
    assert email.value == "usuario@@exemplo.com"


def test_with_spaces_in_email():
    email = Email("usuario @exemplo.com")

    # Email básico permite espaços (validação simplificada)
    assert email.value == "usuario @exemplo.com"
