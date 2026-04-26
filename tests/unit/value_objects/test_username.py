import pytest

from errors import ValidationError
from objects.username import Username


def test_username_valid():
    u = Username("deivid")
    assert u.value == "deivid"


def test_username_too_short():
    with pytest.raises(ValidationError) as error:
        Username("ab")
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O nome de usuário inserido não é válido.",
        "action": "Insira um nome de usuário maior que 3 caracteres.",
        "code": 400,
    }


def test_username_not_string():
    with pytest.raises(ValidationError) as error:
        Username(123)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O nome de usuário inserido não é válido.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
