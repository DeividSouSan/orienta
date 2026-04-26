import pytest

from errors import ValidationError
from objects.study_days import StudyDays


def test_study_days_valid_int():
    d = StudyDays(5)
    assert d.value == 5


def test_study_days_valid_str():
    d = StudyDays(" 10 ")
    assert d.value == 10


def test_study_days_too_short():
    with pytest.raises(ValidationError) as error:
        StudyDays(2)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A duração do estudo precisa estar entre 3 e 30 dias.",
        "action": "Verifique se o campo 'duração' está preenchido e tente novamente.",
        "code": 400,
    }


def test_study_days_too_long():
    with pytest.raises(ValidationError) as error:
        StudyDays(31)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A duração do estudo precisa estar entre 3 e 30 dias.",
        "action": "Verifique se o campo 'duração' está preenchido e tente novamente.",
        "code": 400,
    }


def test_study_days_invalid_str():
    with pytest.raises(ValidationError) as error:
        StudyDays("abc")
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O número de dias precisa ser um número inteiro.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
