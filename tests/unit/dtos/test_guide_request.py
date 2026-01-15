import faker
import pytest

from dtos.guide_request import GuideRequest
from errors import SchemaError

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
    assert guide_request.topic == inputs["topic"]
    assert guide_request.knowledge == inputs["knowledge"]
    assert guide_request.focus_time == inputs["focus_time"]
    assert guide_request.days == inputs["days"]


def test_with_one_field_missing():
    missing = ["title"]

    inputs = {
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": 30,
        "days": 5,
    }
    with pytest.raises(SchemaError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "SchemaError",
        "message": f"Os campos {missing} estão faltando.",
        "action": "Preencha os campos faltantes e tente novamente.",
        "code": 400,
    }


def test_with_all_fields_missing():
    missing = ["title", "topic", "knowledge", "focus_time", "days"]

    inputs = {}

    with pytest.raises(SchemaError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "SchemaError",
        "message": f"Os campos {missing} estão faltando.",
        "action": "Preencha os campos faltantes e tente novamente.",
        "code": 400,
    }


def test_with_str_fields_as_int():
    wrong_type = ["title", "topic", "knowledge"]

    inputs = {
        "title": 90,
        "topic": 1000,
        "knowledge": 0,
        "focus_time": 30,
        "days": 5,
    }

    with pytest.raises(SchemaError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "SchemaError",
        "message": f"Erro de tipo nos campos: {wrong_type}.",
        "action": "Preencha os campos com os dados do tipo certo e tente novamente.",
        "code": 400,
    }


def test_with_int_fields_as_str():
    wrong_type = ["focus_time", "days"]

    inputs = {
        "title": "A segunda guerra mundial.",
        "topic": "A segunda guerra mundial.",
        "knowledge": "iniciante",
        "focus_time": "30",
        "days": "5",
    }

    with pytest.raises(SchemaError) as error:
        GuideRequest.from_dict(inputs)

    assert error.value.toDict() == {
        "name": "SchemaError",
        "message": f"Erro de tipo nos campos: {wrong_type}.",
        "action": "Preencha os campos com os dados do tipo certo e tente novamente.",
        "code": 400,
    }
