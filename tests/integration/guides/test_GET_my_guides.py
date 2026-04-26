import pytest

from tests import orchestrator


@pytest.fixture(autouse=True)
def clear_database():
    yield
    orchestrator.clear_database()


@pytest.mark.vcr
def test_with_direct_access(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user.username)

    response = auth_client.get("/api/v1/my-guides")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body["data"]) == 1
    assert response_body == {
        "message": "Guias recuperados com sucesso.",
        "data": [
            {
                "id": new_guide.id,
                "owner": new_guide.owner.value,
                "model": new_guide.model,
                "temperature": 2.0,
                "generation_time_seconds": new_guide.generation_time_seconds,
                "inputs": {
                    "title": new_guide.inputs.title.value,
                    "topic": new_guide.inputs.topic.value,
                    "knowledge": new_guide.inputs.knowledge.value,
                    "focus_time": new_guide.inputs.focus_time.value,
                    "days": new_guide.inputs.days.value,
                },
                "daily_study": new_guide.daily_study,
                "created_at": response_body["data"][0]["created_at"],
                "status": "studying",
                "is_public": False,
            }
        ],
    }


@pytest.mark.vcr("test_with_direct_access.yaml")
def test_with_deleted_guides(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user.username)
    orchestrator.delete_guide(new_guide.id, new_user.username)

    response = auth_client.get("/api/v1/my-guides")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body["data"]) == 0
    assert response_body == {
        "message": "Guias recuperados com sucesso.",
        "data": [],
    }


@pytest.mark.vcr("test_with_direct_access.yaml")
def test_with_someone_else_guides(auth_client):
    orchestrator.create_guide(owner="mock")

    response = auth_client.get("/api/v1/my-guides")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body["data"]) == 0
    assert response_body == {
        "message": "Guias recuperados com sucesso.",
        "data": [],
    }
