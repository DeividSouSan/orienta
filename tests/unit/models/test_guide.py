import faker
import pytest

from dtos.guide_request import GuideRequest
from errors import ValidationError

fake = faker.Faker()


def test_with_title_below_min_chars():
    inputs = {
        "title": "Short",
        "topic": "A segunda guerra mundial",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O título do estudo precisa ter no mínimo 10 e no máximo 80 caracteres.",
        "action": "Verifique o número de caracteres do título e tente novamente.",
        "code": 400,
    }


def test_with_title_above_max_chars():
    inputs = {
        "title": "A" * 81,
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O título do estudo precisa ter no mínimo 10 e no máximo 80 caracteres.",
        "action": "Verifique o número de caracteres do título e tente novamente.",
        "code": 400,
    }


def test_with_knowledge_inexistent_value():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "blablabla",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
        "action": "Preencha o campo 'knowledge' corretamente e tente novamente.",
        "code": 400,
    }


def test_with_focus_time_below_min():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 15,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco precisa estar entre 30 minutos e 8 horas (480 minutos).",
        "action": "Verifique se o campo 'tempo de foco' está preenchido e tente novamente.",
        "code": 400,
    }


def test_with_focus_time_above_max():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 481,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco precisa estar entre 30 minutos e 8 horas (480 minutos).",
        "action": "Verifique se o campo 'tempo de foco' está preenchido e tente novamente.",
        "code": 400,
    }


def test_with_days_below_min():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 2,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A duração do estudo precisa estar entre 3 e 30 dias.",
        "action": "Verifique se o campo 'duração' está preenchido e tente novamente.",
        "code": 400,
    }


def test_with_days_above_max():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 31,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "A duração do estudo precisa estar entre 3 e 30 dias.",
        "action": "Verifique se o campo 'duração' está preenchido e tente novamente.",
        "code": 400,
    }
