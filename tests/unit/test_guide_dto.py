from random import randint

import faker
import pytest

from dtos.guide_request import GuideRequest
from dtos.topic import Topic
from infra.errors import ValidationError

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

    assert guide_request.title == inputs["title"]
    assert guide_request.topic.text == inputs["topic"]
    assert isinstance(guide_request.topic, Topic)
    assert guide_request.knowledge == inputs["knowledge"]
    assert guide_request.focus_time == inputs["focus_time"]
    assert guide_request.days == inputs["days"]


def test_without_title():
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
        "message": "O título não pode ser vazio.",
        "action": "Preencha o título do guia e tente novamente.",
        "code": 400,
    }


def test_with_title_below_min_chars():
    inputs = {
        "title": fake.pystr(min_chars=1, max_chars=9),
        "topic": "A segunda guerra mundia",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O título do estudo precisa ter no mínimo {GuideRequest.MIN_TITLE_CHARS} e no máximo {GuideRequest.MAX_TITLE_CHARS} caracteres.",
        "action": "Verifique o número de caracteres do título e tente novamente.",
        "code": 400,
    }


def test_with_title_above_max_chars():
    inputs = {
        "title": fake.pystr(min_chars=81, max_chars=90),
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O título do estudo precisa ter no mínimo {GuideRequest.MIN_TITLE_CHARS} e no máximo {GuideRequest.MAX_TITLE_CHARS} caracteres.",
        "action": "Verifique o número de caracteres do título e tente novamente.",
        "code": 400,
    }


def test_without_knowledge():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O conhecimento prévio não pode ser vazio.",
        "action": "Preencha o conhecimento prévio e tente novamente.",
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


def test_without_focus_time():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco não pode ser vazio.",
        "action": "Preencha o tempo de foco e tente novamente.",
        "code": 400,
    }


def test_with_focus_time_below_min_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": randint(1, 29),
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O tempo de foco precisa estar entre {GuideRequest.MIN_FOCUS_TIME} minutos e {GuideRequest.MAX_FOCUS_TIME}.",
        "action": "Verifique se o campo 'tempo de foco' está preenchido corretamente e tente novamente.",
        "code": 400,
    }


def test_with_focus_time_above_max_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": randint(481, 500),
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O tempo de foco precisa estar entre {GuideRequest.MIN_FOCUS_TIME} minutos e {GuideRequest.MAX_FOCUS_TIME}.",
        "action": "Verifique se o campo 'tempo de foco' está preenchido corretamente e tente novamente.",
        "code": 400,
    }


def test_with_focus_time_as_str():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": str(randint(30, 480)),
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tempo de foco (minutos) deve ser um número inteiro.",
        "action": "Verifique se o tempo de foco é um número inteiro e tente novamente.",
        "code": 400,
    }


def test_without_days():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O número de dias não pode ser vazio.",
        "action": "Preencha o número de dias e tente novamente.",
        "code": 400,
    }


def test_with_days_below_min_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": randint(0, 2),
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"A número de dias precisa estar entre {GuideRequest.MIN_DAYS} e {GuideRequest.MAX_DAYS} dias.",
        "action": "Verifique se o campo 'dias' está preenchido corretamente e tente novamente.",
        "code": 400,
    }


def test_with_days_above_max_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": randint(31, 40),
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"A número de dias precisa estar entre {GuideRequest.MIN_DAYS} e {GuideRequest.MAX_DAYS} dias.",
        "action": "Verifique se o campo 'dias' está preenchido corretamente e tente novamente.",
        "code": 400,
    }


def test_with_days_as_str():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": str(randint(3, 30)),
    }

    with pytest.raises(ValidationError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O número de dias precisa ser um número inteiro.",
        "action": "Verifique o número de dias fornecido e tente novamente.",
        "code": 400,
    }
