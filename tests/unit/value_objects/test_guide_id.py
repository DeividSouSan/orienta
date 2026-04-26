import pytest

from errors import ValidationError
from objects.guide_id import GuideId


def test_guide_id_valid():
    g = GuideId("guide456")
    assert g.value == "guide456"


def test_guide_id_empty():
    with pytest.raises(ValidationError) as error:
        GuideId("")
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O ID do guia não pode ser vazio.",
        "action": "Verifique se o ID foi enviado corretamente e tente novamente.",
        "code": 400,
    }


def test_guide_id_not_string():
    with pytest.raises(ValidationError) as error:
        GuideId(123)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O ID do guia precisa ser um texto.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
