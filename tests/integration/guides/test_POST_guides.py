from datetime import datetime, timezone

import faker
import pytest

from models import guide

fake = faker.Faker()


@pytest.mark.vcr
def test_with_valid_input(auth_client, new_user):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Generate Valid Guide",
            "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 3,
        },
    )

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "message": "Guia de estudos gerado com sucesso.",
        "data": {
            "owner": new_user["username"],
            "inputs": {
                "title": "Generate Valid Guide",
                "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
                "knowledge": "zero",
                "focus_time": 60,
                "days": 3,
            },
            "is_public": False,
            **response_body["data"],
        },
    }

    assert response_body["data"]["model"] in guide.GEN_MODELS
    assert response_body["data"]["temperature"] == 2.0
    assert isinstance(response_body["data"]["generation_time_seconds"], int)
    assert len(response_body["data"]["daily_study"]) == 3

    created_at = datetime.strptime(
        response_body["data"]["created_at"], "%a, %d %b %Y %H:%M:%S %Z"
    )
    created_at = created_at.replace(tzinfo=timezone.utc)

    assert created_at < datetime.now(tz=timezone.utc)


def test_with_anonymous_user(client):
    response = client.post(
        "/api/v1/guides",
        json={
            "title": "Test with anonymous",
            "topic": "Quero estudar sobre a revolução russa e como e por que ela aconteceu.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 5,
        },
    )

    response_body = response.get_json()

    assert response.status_code == 401
    assert response_body == {
        "name": "UnauthorizedError",
        "message": "Cookie de sessão não encontrado.",
        "action": "Faça login para continuar.",
        "code": 401,
    }
