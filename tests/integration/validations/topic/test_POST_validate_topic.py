import pytest


def test_anonymous_user(client):
    response = client.post(
        "/api/v1/validations/topic",
    )

    assert response.status_code == 401

    response_body = response.get_json()

    assert response_body == {
        "name": "UnauthorizedError",
        "message": "Cookie de sessão não encontrado.",
        "action": "Faça login para continuar.",
        "code": 401,
    }


@pytest.mark.vcr
def test_validate_topic_with_valid_input(auth_client):
    topic = "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn."

    response = auth_client.post(
        "/api/v1/validations/topic",
        json={"topic": topic},
    )

    assert response.status_code == 200

    response_body = response.get_json()

    assert response_body == {
        "message": "O tópico é válido.",
        "data": {
            "topic": topic,
            "info": {
                "is_valid": True,
                "motive": "N/A",
            },
        },
    }


@pytest.mark.vcr
def test_validate_topic_with_invalid_topic(auth_client):
    response = auth_client.post(
        "/api/v1/validations/topic",
        json={"topic": "aaaaaaaaaaaaa"},
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": response_body["message"],
        "action": response_body["action"],
        "code": 400,
    }


def test_validate_topic_without_topic(auth_client):
    response = auth_client.post(
        "/api/v1/validations/topic",
        json={},
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter no mínimo 10 e no máximo 150 caracteres.",
        "action": "Verifique o número de caracteres e tente novamente.",
        "code": 400,
    }
