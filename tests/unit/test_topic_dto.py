import faker
import pytest

from dtos.topic import Topic
from infra.errors import ValidationError

fake = faker.Faker()


def test_with_valid_data():
    text = "A segunda guerra mundial."

    topic = Topic.from_dict({"text": text})

    assert topic.text == text


def test_without_text():
    with pytest.raises(ValidationError) as error:
        Topic.from_dict({})

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tópico não pode ser vazio.",
        "action": "Preencha o tópico do guia e tente novamente.",
        "code": 400,
    }


def test_with_below_min_chars_text():
    with pytest.raises(ValidationError) as error:
        Topic.from_dict({"text": fake.text(max_nb_chars=5)})

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O tópico de estudo precisa ter no mínimo {Topic.MIN_TOPIC_CHARS} e no máximo {Topic.MAX_TOPIC_CHARS} caracteres.",
        "action": "Verifique o número de caracteres e tente novamente.",
        "code": 400,
    }


def test_with_above_max_chars_text():
    with pytest.raises(ValidationError) as error:
        Topic.from_dict({"text": fake.text(max_nb_chars=300)})

    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": f"O tópico de estudo precisa ter no mínimo {Topic.MIN_TOPIC_CHARS} e no máximo {Topic.MAX_TOPIC_CHARS} caracteres.",
        "action": "Verifique o número de caracteres e tente novamente.",
        "code": 400,
    }
