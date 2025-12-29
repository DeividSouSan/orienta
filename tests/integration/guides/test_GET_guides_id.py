import pytest
from tests import orchestrator


@pytest.mark.vcr
def test_get_guide(auth_client):
    new_guide = orchestrator.create_guide()

    response = auth_client.get(f"/api/v1/guides/{new_guide['id']}")

    assert response.status_code == 200

    response_body = response.get_json()

    assert response_body == {
        "message": "Guia recuperado com sucesso.",
        "data": {
            "title": new_guide["title"],
            "model": new_guide["model"],
            "is_public": False,
            "owner": response_body["data"]["owner"],
            "status": "studying",
            "temperature": 2.0,
            "created_at": response_body["data"][
                "created_at"
            ],  # ? Seria melhor usar `new_guide["created_at"]` ?
            "generation_time_seconds": new_guide["generation_time_seconds"],
            "inputs": {
                "topic": new_guide["inputs"]["topic"],
                "knowledge": new_guide["inputs"]["knowledge"],
                "focus_time": new_guide["inputs"]["focus_time"],
                "days": new_guide["inputs"]["days"],
            },
            "daily_study": new_guide["daily_study"],
        },
    }


def test_get_nonexistent_guide(auth_client):
    response = auth_client.get("/api/v1/guides/a32fdsa5")

    assert response.status_code == 404

    response_body = response.get_json()

    assert response_body == {
        "name": "NotFoundError",
        "message": "O guia não foi encontrado.",
        "action": "Verifique que o guia existe e tente novamente.",
        "code": 404,
    }
