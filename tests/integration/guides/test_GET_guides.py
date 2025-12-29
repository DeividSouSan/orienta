import pytest
from tests import orchestrator


@pytest.mark.vcr
def test_get_my_guides(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user["username"])

    response = auth_client.get("/api/v1/guides")

    assert response.status_code == 200

    response_body = response.get_json()

    assert len(response_body["data"]) == 1
    assert response_body == {
        "message": "Guias recuperados com sucesso.",
        "data": [
            {
                "id": new_guide["id"],
                "title": new_guide["title"],
                "topic": new_guide["inputs"]["topic"],
                "days": new_guide["inputs"]["days"],
                "daily_studies": new_guide["daily_study"],
                "created_at": response_body["data"][0]["created_at"],
                "status": "studying",
            }
        ],
    }
