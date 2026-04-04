import pytest

from errors import ValidationError
from objects.password import Password


def test_with_valid_password():
    password = Password("senha123")

    assert password.value == "senha123"


def test_with_password_exactly_six_characters():
    password = Password("123456")

    assert password.value == "123456"


def test_with_long_password():
    password = Password("senhamuitolongacommuitos_caracteres123!@#")

    assert password.value == "senhamuitolongacommuitos_caracteres123!@#"


def test_with_empty_password():
    with pytest.raises(ValidationError) as error:
        Password("")

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A senha deve ter pelo menos 6 caracteres.",
        "action": "Forneça uma senha com no mínimo 6 caracteres e tente novamente.",
        "code": 400,
    }


def test_with_password_less_than_six_characters():
    with pytest.raises(ValidationError) as error:
        Password("12345")

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A senha deve ter pelo menos 6 caracteres.",
        "action": "Forneça uma senha com no mínimo 6 caracteres e tente novamente.",
        "code": 400,
    }


def test_with_password_one_character():
    with pytest.raises(ValidationError) as error:
        Password("a")

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A senha deve ter pelo menos 6 caracteres.",
        "action": "Forneça uma senha com no mínimo 6 caracteres e tente novamente.",
        "code": 400,
    }


def test_with_password_special_characters():
    password = Password("!@#$%^&*()")

    assert password.value == "!@#$%^&*()"


def test_with_five_characters():
    with pytest.raises(ValidationError) as error:
        Password("abcde")

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A senha deve ter pelo menos 6 caracteres.",
        "action": "Forneça uma senha com no mínimo 6 caracteres e tente novamente.",
        "code": 400,
    }


def test_with_whitespace_password():
    with pytest.raises(ValidationError) as error:
        Password("abc def")

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A senha não pode conter espaços.",
        "action": "Forneça uma senha sem espaços e tente novamente.",
        "code": 400,
    }
