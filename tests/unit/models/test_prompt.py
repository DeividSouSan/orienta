from unittest.mock import MagicMock, patch

import google.genai.errors as genai_errors
import pytest

from errors import ServiceError, ValidationError
from models import prompt


def test_process_strips_whitespace():
    user_input = {
        "topic": "  Deep Learning  ",
        "knowledge": " iniciante ",
        "focus_time": " 60 ",
        "days": " 10 ",
    }
    processed = prompt.process(user_input)
    assert processed["topic"] == "Deep Learning"
    assert processed["knowledge"] == "iniciante"
    assert processed["focus_time"] == "60"
    assert processed["days"] == "10"


def test_process_with_empty_input():
    with pytest.raises(ValidationError) as exc:
        prompt.process({})
    assert "As entradas do usuário não podem ser um dicionário vazio." in str(exc.value)


def test_format_xml_structure():
    user_input = {"topic": "Python", "knowledge": "zero", "focus_time": 45, "days": 7}
    formatted = prompt.format(user_input)
    assert "<TOPIC>Python</TOPIC>" in formatted
    assert "<KNOWLEDGE>zero</KNOWLEDGE>" in formatted
    assert "<FOCUS_TIME>45 minutes</FOCUSC_TIME>" in formatted
    assert "<DURATION_IN_DAYS>7 days</DURATION_IN_DAYS>" in formatted


def test_format_with_empty_input():
    with pytest.raises(ValidationError) as exc:
        prompt.format({})
    assert "As entradas do usuário não podem ser um dicionário vazio." in str(exc.value)


@pytest.mark.parametrize(
    "topic, expected_msg",
    [
        ("A" * 9, "O tópico de estudo precisa ter no mínimo 10"),
        (
            "A" * 151,
            "O tópico de estudo precisa ter no mínimo 10 e no máximo 150 caracteres.",
        ),
        (123, "O tópico de estudo precisa ser um texto."),
    ],
    ids=["too-short", "too-long", "invalid-type"],
)
def test_validate_topic_failures(topic, expected_msg):
    with pytest.raises(ValidationError) as exc:
        prompt.validate_topic(topic)
    assert expected_msg in str(exc.value)


def test_validate_topic_success():
    # Deve passar sem exceção
    prompt.validate_topic("Aprendizado de Máquina")


@pytest.mark.parametrize(
    "knowledge, expected_msg",
    [
        ("expert", "O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'"),
        (None, "O conhecimento deve ser um texto."),
        (1, "O conhecimento deve ser um texto."),
    ],
    ids=["invalid-value", "none-value", "int-value"],
)
def test_validate_knowledge_failures(knowledge, expected_msg):
    with pytest.raises(ValidationError) as exc:
        prompt.validate_knowledge(knowledge)
    assert expected_msg in str(exc.value)


@pytest.mark.parametrize("val", ["zero", "iniciante", "intermediario"])
def test_validate_knowledge_success(val):
    prompt.validate_knowledge(val)


@pytest.mark.parametrize(
    "focus_time, expected_msg",
    [
        (29, "O tempo de foco precisa estar entre 30 minutos e 8 horas"),
        (481, "O tempo de foco precisa estar entre 30 minutos e 8 horas"),
        ("60", "O tempo de foco (minutos) deve ser um número inteiro."),
    ],
    ids=["too-low", "too-high", "str-type"],
)
def test_validate_focus_time_failures(focus_time, expected_msg):
    with pytest.raises(ValidationError) as exc:
        prompt.validate_focus_time(focus_time)
    assert expected_msg in str(exc.value)


def test_validate_focus_time_success():
    prompt.validate_focus_time(60)


@pytest.mark.parametrize(
    "days, expected_msg",
    [
        (2, "A duração do estudo precisa estar entre 3 e 30 dias."),
        (31, "A duração do estudo precisa estar entre 3 e 30 dias."),
        ("5", "O número de dias precisa ser um número inteiro."),
    ],
    ids=["too-low", "too-high", "str-type"],
)
def test_validate_days_failures(days, expected_msg):
    with pytest.raises(ValidationError) as exc:
        prompt.validate_days(days)
    assert expected_msg in str(exc.value)


def test_validate_days_success():
    prompt.validate_days(10)


@patch("google.genai.Client")
def test_validate_relevance_success(mock_client_class):
    # Setup mock
    mock_client = mock_client_class.return_value
    mock_response = MagicMock()
    mock_response.parsed.is_valid = True
    mock_client.models.generate_content.return_value = mock_response

    # Execute
    result = prompt.validate_relevance("Arendizado de Máquina com Python")

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
        prompt.validate_relevance("Blablabla")
    assert "Tópico irrelevante" in str(exc.value)


@patch("google.genai.Client")
def test_validate_relevance_retry_on_429(mock_client_class):
    mock_client = mock_client_class.return_value

    # Simular 429 na primeira chamada e sucesso na segunda
    error_429 = genai_errors.ClientError("Quota exceeded", response_json={})
    error_429.code = 429
    mock_response = MagicMock()
    mock_response.parsed.is_valid = True

    mock_client.models.generate_content.side_effect = [error_429, mock_response]

    # Execute
    result = prompt.validate_relevance("Deep Learning")

    assert result.is_valid is True
    assert mock_client.models.generate_content.call_count == 2


@patch("google.genai.Client")
def test_validate_relevance_service_error_after_all_retries(mock_client_class):
    mock_client = mock_client_class.return_value
    error_503 = genai_errors.ServerError("Service unavailable", response_json={})
    error_503.code = 503

    # Falhar em todos os modelos (o número de modelos vem do .env, geralmente 2 ou mais)
    mock_client.models.generate_content.side_effect = [error_503] * 10

    with pytest.raises(ServiceError) as exc:
        prompt.validate_relevance("Topic")
    assert "O modelo não consegiu gerar o conteúdo" in str(exc.value)


@patch("models.prompt.validate_relevance")
def test_make_orchestration_success(mock_validate):
    mock_validate.return_value = MagicMock(is_valid=True)
    user_input = {
        "topic": "Machine Learning",
        "knowledge": "iniciante",
        "focus_time": 60,
        "days": 5,
    }
    result = prompt.make(user_input)
    assert "<TOPIC>Machine Learning</TOPIC>" in result


def test_make_validation_failure():
    user_input = {
        "topic": "Short",  # < 10 chars
        "knowledge": "iniciante",
        "focus_time": 60,
        "days": 5,
    }
    with pytest.raises(ValidationError):
        prompt.make(user_input)
