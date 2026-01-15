import pytest

from tests import orchestrator


@pytest.mark.vcr
def test_with_valid_id(auth_client):
    new_guide = orchestrator.create_guide()

    response = auth_client.get(f"/api/v1/guides/{new_guide['id']}")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "message": "Guia recuperado com sucesso.",
        "data": {
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
                "title": new_guide["inputs"]["title"],
                "topic": new_guide["inputs"]["topic"],
                "knowledge": new_guide["inputs"]["knowledge"],
                "focus_time": new_guide["inputs"]["focus_time"],
                "days": new_guide["inputs"]["days"],
            },
            "daily_study": new_guide["daily_study"],
        },
    }


def test_with_nonexistent_guide(auth_client):
    response = auth_client.get("/api/v1/guides/3vT2Ot6aVi9glNMcIzW1")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "name": "NotFoundError",
        "message": "O guia não foi encontrado.",
        "action": "Verifique que o guia existe e tente novamente.",
        "code": 404,
    }


@pytest.mark.vcr("test_with_valid_id.yaml")
def test_with_deleted_guide(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user["username"])
    orchestrator.delete_guide(new_guide["id"], new_user["username"])

    response = auth_client.get(f"/api/v1/guides/{new_guide['id']}")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "name": "NotFoundError",
        "message": "O guia não foi encontrado.",
        "action": "Verifique que o guia existe e tente novamente.",
        "code": 404,
    }
