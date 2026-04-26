import pytest

from errors import ValidationError
from objects.knowledge_level import KnowledgeLevel


def test_knowledge_level_valid():
    k = KnowledgeLevel("Iniciante ")
    assert k.value == "iniciante"


def test_knowledge_level_invalid():
    with pytest.raises(ValidationError) as error:
        KnowledgeLevel("expert")
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
        "action": "Preencha o campo 'knowledge' corretamente e tente novamente.",
        "code": 400,
    }


def test_knowledge_level_not_string():
    with pytest.raises(ValidationError) as error:
        KnowledgeLevel(123)
    assert error.value.toDict() == {
        "name": "ValidationError",
        "message": "O conhecimento deve ser um texto.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
