import pytest

from errors import ValidationError
from objects.topic import Topic


def test_topic_valid():
    t = Topic("Aprendizado de Python")
    assert t.value == "Aprendizado de Python"


def test_topic_invalid_length_short():
    with pytest.raises(ValidationError) as error:
        Topic("Curto")
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter entre 10 e 150 caracteres.",
        "action": "Forneça um tópico válido e tente novamente.",
        "code": 400,
    }


def test_topic_invalid_length_long():
    with pytest.raises(ValidationError) as error:
        Topic("a" * 151)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter entre 10 e 150 caracteres.",
        "action": "Forneça um tópico válido e tente novamente.",
        "code": 400,
    }


def test_topic_not_string():
    with pytest.raises(ValidationError) as error:
        Topic(123)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ser um texto.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
