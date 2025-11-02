from dotenv import load_dotenv
import os


load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_generate_guide_with_valid_input(mock_session):
    response = mock_session.post(
        f"{API_URL}/guides",
        json={
            "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 3,
        },
    )

    response_body = response.json()
    assert response_body == {
        "message": "Guia de estudos gerado com sucesso.",
        "data": {
            "owner": "mock",
            "inputs": {
                "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
                "knowledge": "zero",
                "focus_time": 60,
                "days": 3,
            },
            "model": response_body["data"]["model"],
            "temperature": 2,
            "generation_time_seconds": response_body["data"]["generation_time_seconds"],
            "daily_study": response_body["data"]["daily_study"],
            "created_at": response_body["data"]["created_at"],
            "is_public": False,
        },
    }


def test_generate_guide_with_specific_model(mock_session):
    response = mock_session.post(
        f"{API_URL}/guides",
        json={
            "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
            "knowledge": "iniciante",
            "focus_time": 60,
            "days": 3,
            "model": "gemini-2.5-flash-lite",
            "temperature": 0,
        },
    )

    response_body = response.json()
    assert response_body == {
        "message": "Guia de estudos gerado com sucesso.",
        "data": {
            "owner": "mock",
            "inputs": {
                "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
                "knowledge": "iniciante",
                "focus_time": 60,
                "days": 3,
            },
            "model": "gemini-2.5-flash-lite",
            "temperature": 0,
            "generation_time_seconds": response_body["data"]["generation_time_seconds"],
            "daily_study": response_body["data"]["daily_study"],
            "created_at": response_body["data"]["created_at"],
            "is_public": False,
        },
    }


def test_generate_guide_with_str_focus_time_and_days(mock_session):
    response = mock_session.post(
        f"{API_URL}/guides",
        json={
            "topic": "Eu quero estudar sobre neurociência.",
            "knowledge": "iniciante",
            "focus_time": "60",
            "days": "3",
        },
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O tempo de foco (minutos) deve ser um número inteiro.",
        "action": response_body["action"],
        "code": 400,
    }


def test_generate_guide_without_topic(mock_session):
    response = mock_session.post(
        f"{API_URL}/guides",
        json={
            "knowledge": "iniciante",
            "focus_time": 60,
            "days": 3,
        },
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter no mínimo 10 e no máximo 150 caracteres.",
        "action": "Verifique o número de caracteres e tente novamente.",
        "code": 400,
    }


def test_generate_guide_without_knowledge(mock_session):
    response = mock_session.post(
        f"{API_URL}/guides",
        json={
            "topic": "Eu quero estudar sobre a segunda guerra mundial.",
            "focus_time": 60,
            "days": 3,
        },
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
        "action": "Preencha o campo 'knowledge' corretamente e tente novamente.",
        "code": 400,
    }


def test_generate_guide_without_focus_time(mock_session):
    response = mock_session.post(
        f"{API_URL}/guides",
        json={
            "topic": "Eu quero estudar sobre Git e quais seus principais comandos.",
            "knowledge": "zero",
            "days": 3,
        },
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O tempo de foco (minutos) deve ser um número inteiro.",
        "action": response_body["action"],
        "code": 400,
    }


def test_generate_guide_without_days(mock_session):
    response = mock_session.post(
        f"{API_URL}/guides",
        json={
            "topic": "Quero estudar sobre a revolução russa e como e por que ela aconteceu.",
            "knowledge": "zero",
            "focus_time": 60,
        },
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O número de dias precisa ser um número inteiro.",
        "action": response_body["action"],
        "code": 400,
    }
