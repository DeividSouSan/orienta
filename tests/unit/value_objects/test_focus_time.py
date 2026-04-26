import pytest

from errors import ValidationError
from objects.focus_time import FocusTime


def test_focus_time_valid_int():
    f = FocusTime(60)
    assert f.value == 60


def test_focus_time_valid_str():
    f = FocusTime(" 120 ")
    assert f.value == 120


def test_focus_time_too_short():
    with pytest.raises(ValidationError) as error:
        FocusTime(15)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco precisa estar entre 30 minutos e 8 horas (480 minutos).",
        "action": "Verifique se o campo 'tempo de foco' está preenchido e tente novamente.",
        "code": 400,
    }


def test_focus_time_too_long():
    with pytest.raises(ValidationError) as error:
        FocusTime(481)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco precisa estar entre 30 minutos e 8 horas (480 minutos).",
        "action": "Verifique se o campo 'tempo de foco' está preenchido e tente novamente.",
        "code": 400,
    }


def test_focus_time_invalid_str():
    with pytest.raises(ValidationError) as error:
        FocusTime("abc")
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco (minutos) deve ser um número inteiro.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
