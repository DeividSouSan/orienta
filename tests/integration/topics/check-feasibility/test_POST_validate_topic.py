import faker
import pytest

fake = faker.Faker()


def test_with_anonymous_user(client):
    response = client.post(
        "/api/v1/topisc/check-feasibility",
    )

    response_body = response.get_json()

    assert response.status_code == 401
    assert response_body == {
        "name": "UnauthorizedError",
        "message": "Cookie de sessão não encontrado.",
        "action": "Faça login para continuar.",
        "code": 401,
    }


@pytest.mark.vcr
def test_with_valid_input(auth_client):
    text = "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn."

    response = auth_client.post(
        "/api/v1/topics/check-feasibility",
        json={"text": text},
    )

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "message": "O tópico foi validado.",
        "data": {
            "topic": text,
            "info": {
                "is_valid": True,
                "motive": "N/A",
            },
        },
    }


@pytest.mark.vcr
def test_with_invalid_topic(auth_client):
    text = "Pastel TV Python Javascript Computador Faculdade Dinheiro"

    response = auth_client.post(
        "/api/v1/topics/check-feasibility",
        json={"topic": text},
    )

    response_body = response.get_json()

    assert response_body == {
        "message": "O tópico foi validado.",
        "data": {
            "topic": text,
            "info": {
                "is_valid": True,
                "motive": "N/A",
            },
        },
    }
