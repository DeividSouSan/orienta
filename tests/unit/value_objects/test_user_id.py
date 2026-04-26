import pytest

from errors import ValidationError
from objects.user_id import UserId


def test_user_id_valid():
    u = UserId("user123")
    assert u.value == "user123"


def test_user_id_empty():
    with pytest.raises(ValidationError) as error:
        UserId("")
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O ID do usuário não pode ser vazio.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_user_id_not_string():
    with pytest.raises(ValidationError) as error:
        UserId(123)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O ID do usuário precisa ser um texto.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
