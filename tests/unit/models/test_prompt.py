from unittest.mock import MagicMock, patch

import google.genai.errors as genai_errors
import pytest

from dtos.guide_request import GuideRequest
from errors import ServiceError, ValidationError
from models import prompt
from objects.topic import Topic


@patch("google.genai.Client")
def test_validate_relevance_success(mock_client_class):
    # Setup mock
    mock_client = mock_client_class.return_value
    mock_response = MagicMock()
    mock_response.parsed.is_valid = True
    mock_client.models.generate_content.return_value = mock_response

    # Execute — recebe um VO Topic
    result = prompt.validate_relevance(Topic("Aprendizado de Máquina com Python"))

    # Assert
    assert result.is_valid is True
    assert mock_client.models.generate_content.called


@patch("google.genai.Client")
def test_validate_relevance_invalid_topic(mock_client_class):
    mock_client = mock_client_class.return_value
    mock_response = MagicMock()
    mock_response.parsed.is_valid = False
    mock_response.parsed.motive = "Tópico irrelevante"
    mock_client.models.generate_content.return_value = mock_response

    with pytest.raises(ValidationError) as exc:
        prompt.validate_relevance(Topic("Blablabla é um tópico"))
    assert exc.value.toDict() == {
        "name": "ValidationError",
        "message": "Tópico irrelevante",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


@patch("google.genai.Client")
def test_validate_relevance_retry_on_429(mock_client_class):
    mock_client = mock_client_class.return_value

    # Simular 429 na primeira chamada e sucesso na segunda
    error_429 = genai_errors.ClientError("Quota exceeded", response_json={})
    error_429.code = 429
    mock_response = MagicMock()
    mock_response.parsed.is_valid = True

    mock_client.models.generate_content.side_effect = [error_429, mock_response]

    # Execute — recebe um VO Topic
    result = prompt.validate_relevance(Topic("Deep Learning avançado"))

    assert result.is_valid is True
    assert mock_client.models.generate_content.call_count == 2


@patch("google.genai.Client")
def test_validate_relevance_service_error_after_all_retries(mock_client_class):
    mock_client = mock_client_class.return_value
    error_503 = genai_errors.ServerError("Service unavailable", response_json={})
    error_503.code = 503

    # Falhar em todos os modelos
    mock_client.models.generate_content.side_effect = [error_503] * 10

    with pytest.raises(ServiceError) as exc:
        prompt.validate_relevance(Topic("Topic válido aqui"))
    assert exc.value.toDict() == {
        "name": "ServiceError",
        "message": "O modelo não consegiu gerar o conteúdo, a cota foi excedida ou seu acesso o modelo negado.",
        "action": "Entre em contado com o suporte.",
        "code": 503,
    }


@patch("models.prompt.validate_relevance")
def test_make_orchestration_success(mock_validate):
    mock_validate.return_value = MagicMock(is_valid=True)
    request = GuideRequest.from_dict(
        {
            "title": "Machine Learning Basics",
            "topic": "Machine Learning",
            "knowledge": "iniciante",
            "focus_time": 60,
            "days": 5,
        }
    )
    result = prompt.make(request)
    assert "<TOPIC>Machine Learning</TOPIC>" in result
    assert "<KNOWLEDGE>iniciante</KNOWLEDGE>" in result
    assert "<FOCUS_TIME>60 minutes</FOCUS_TIME>" in result
    assert "<DURATION_IN_DAYS>5 days</DURATION_IN_DAYS>" in result


def test_make_with_invalid_topic():
    with pytest.raises(ValidationError) as exc:
        GuideRequest.from_dict(
            {
                "title": "Título válido aqui",
                "topic": "Short",  # < 10 chars
                "knowledge": "iniciante",
                "focus_time": 60,
                "days": 5,
            }
        )
    assert exc.value.toDict() == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter entre 10 e 150 caracteres.",
        "action": "Forneça um tópico válido e tente novamente.",
        "code": 400,
    }
