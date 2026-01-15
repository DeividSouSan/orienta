from random import randint

import faker
import pytest

from dtos.guide_request import GuideRequest
from errors import ValidationError
from models import guide

fake = faker.Faker()


def test_with_title_below_min_chars():
    inputs = {
        "title": fake.pystr(
            min_chars=1,
            max_chars=guide.MIN_TITLE_CHARS - 1,
        ),
        "topic": "A segunda guerra mundia",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        guide_request = GuideRequest.from_dict(inputs)
        guide._validate_inputs(guide_request)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O título do estudo precisa ter no mínimo {guide.MIN_TITLE_CHARS} e no máximo {guide.MAX_TITLE_CHARS} caracteres.",
        "action": "Verifique o número de caracteres do título e tente novamente.",
        "code": 400,
    }


def test_with_title_above_max_chars():
    inputs = {
        "title": fake.pystr(
            min_chars=guide.MAX_TITLE_CHARS + 1,
            max_chars=guide.MAX_TITLE_CHARS + 10,
        ),
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        guide_request = GuideRequest.from_dict(inputs)
        guide._validate_inputs(guide_request)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O título do estudo precisa ter no mínimo {guide.MIN_TITLE_CHARS} e no máximo {guide.MAX_TITLE_CHARS} caracteres.",
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
        guide_request = GuideRequest.from_dict(inputs)
        guide._validate_inputs(guide_request)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
        "action": "Preencha o campo 'knowledge' corretamente e tente novamente.",
        "code": 400,
    }


def test_with_focus_time_below_min_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": randint(0, guide.MIN_FOCUS_TIME - 1),
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        guide_request = GuideRequest.from_dict(inputs)
        guide._validate_inputs(guide_request)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O tempo de foco precisa estar entre {guide.MIN_FOCUS_TIME} minutos e {guide.MAX_FOCUS_TIME}.",
        "action": "Verifique se o campo 'tempo de foco' está preenchido corretamente e tente novamente.",
        "code": 400,
    }


def test_with_focus_time_above_max_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": randint(guide.MAX_FOCUS_TIME + 1, guide.MAX_FOCUS_TIME + 10),
        "days": 5,
    }

    with pytest.raises(ValidationError) as error:
        guide_request = GuideRequest.from_dict(inputs)
        guide._validate_inputs(guide_request)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O tempo de foco precisa estar entre {guide.MIN_FOCUS_TIME} minutos e {guide.MAX_FOCUS_TIME}.",
        "action": "Verifique se o campo 'tempo de foco' está preenchido corretamente e tente novamente.",
        "code": 400,
    }


def test_with_days_below_min_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": randint(0, guide.MIN_DAYS - 1),
    }

    with pytest.raises(ValidationError) as error:
        guide_request = GuideRequest.from_dict(inputs)
        guide._validate_inputs(guide_request)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"A número de dias precisa estar entre {guide.MIN_DAYS} e {guide.MAX_DAYS} dias.",
        "action": "Verifique se o campo 'dias' está preenchido corretamente e tente novamente.",
        "code": 400,
    }


def test_with_days_above_max_chars():
    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": randint(guide.MAX_DAYS + 1, guide.MAX_DAYS + 10),
    }

    with pytest.raises(ValidationError) as error:
        guide_request = GuideRequest.from_dict(inputs)
        guide._validate_inputs(guide_request)

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"A número de dias precisa estar entre {guide.MIN_DAYS} e {guide.MAX_DAYS} dias.",
        "action": "Verifique se o campo 'dias' está preenchido corretamente e tente novamente.",
        "code": 400,
    }
