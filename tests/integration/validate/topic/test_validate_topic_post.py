from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_validate_topic_with_valid_input(mock_session):
    response = mock_session.post(
        f"{API_URL}/validate/topic",
        json={
            "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
        },
    )

    response.status_code == 201

    response_body = response.json()
    assert response_body == {"message": "O tópico é válido."}


def test_validate_topic_with_invalid_topic(mock_session):
    response = mock_session.post(
        f"{API_URL}/validate/topic",
        json={"topic": "aaaaaaaaaaaaa"},
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": response_body["message"],
        "action": response_body["action"],
        "code": 400,
    }


def test_validate_topic_without_topic(mock_session):
    response = mock_session.post(
        f"{API_URL}/validate/topic",
        json={},
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter no mínimo 10 e no máximo 150 caracteres.",
        "action": "Verifique o número de caracteres e tente novamente.",
        "code": 400,
    }
