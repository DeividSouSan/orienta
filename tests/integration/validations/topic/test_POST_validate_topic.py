import requests

from tests import orchestrator


def test_validate_topic_with_valid_input():
    new_user = orchestrator.create_user()
    cookie_session = orchestrator.authenticate(new_user["email"], "validpassword")

    topic = "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn."

    response = requests.post(
        "http://localhost:5000/api/v1/validations/topic",
        json={"topic": topic},
        cookies={"session_id": cookie_session},
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body == {
        "message": "O tópico é válido.",
        "data": {
            "topic": topic,
            "info": {
                "is_valid": True,
                "motive": response_body["data"]["info"]["motive"],
            },
        },
    }


def test_validate_topic_with_invalid_topic():
    new_user = orchestrator.create_user()
    cookie_session = orchestrator.authenticate(new_user["email"], "validpassword")

    response = requests.post(
        "http://localhost:5000/api/v1/validations/topic",
        json={"topic": "aaaaaaaaaaaaa"},
        cookies={"session_id": cookie_session},
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": response_body["message"],
        "action": response_body["action"],
        "code": 400,
    }


def test_validate_topic_without_topic():
    new_user = orchestrator.create_user()
    cookie_session = orchestrator.authenticate(new_user["email"], "validpassword")

    response = requests.post(
        "http://localhost:5000/api/v1/validations/topic",
        json={},
        cookies={"session_id": cookie_session},
    )

    assert response.status_code == 400

    response_body = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter no mínimo 10 e no máximo 150 caracteres.",
        "action": "Verifique o número de caracteres e tente novamente.",
        "code": 400,
    }


def test_anonymous_user():
    new_user = orchestrator.create_user()
    cookie_session = orchestrator.authenticate(new_user["email"], "validpassword")

    response = requests.post(
        "http://localhost:5000/api/v1/validations/topic",
        json={},
    )

    assert response.status_code == 401

    response_body = response.json()
    assert response_body == {
        "name": "UnauthorizedError",
        "message": "Cookie de sessão não encontrado.",
        "action": "Faça login para continuar.",
        "code": 401,
    }
