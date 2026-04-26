import faker
import pytest

from dtos.guide_request import GuideRequest
from errors import ValidationError

fake = faker.Faker()


def test_with_valid_data():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }

    guide_request = GuideRequest.from_dict(inputs)

    assert guide_request.title.value == inputs["title"]
    assert guide_request.topic.value == inputs["topic"]
    assert guide_request.knowledge.value == inputs["knowledge"]
    assert guide_request.focus_time.value == inputs["focus_time"]
    assert guide_request.days.value == inputs["days"]


def test_with_one_field_missing():
    inputs = {
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


def test_with_all_fields_missing():
    inputs = {}

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O título do estudo precisa ter no mínimo 10 e no máximo 80 caracteres.",
        "action": "Verifique o número de caracteres do título e tente novamente.",
        "code": 400,
    }


def test_with_str_fields_as_int():
    inputs = {
        "title": 90,
        "topic": 1000,
        "knowledge": 0,
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O título do estudo precisa ser um texto.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_with_int_fields_as_str():
    # '30' e '5' são convertidos automaticamente nos VOs atuais
    # Para testar erro de tipo, usamos algo que não pode ser convertido
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": "trinta",
        "days": "cinco",
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco (minutos) deve ser um número inteiro.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
