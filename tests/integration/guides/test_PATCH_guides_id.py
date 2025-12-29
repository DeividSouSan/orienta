import pytest

from models import guide
from tests import orchestrator


@pytest.mark.vcr
def test_update_studies_on_valid_guide(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user["username"], days=3)

    assert new_guide["status"] == "studying"
    assert new_guide["daily_study"][0]["completed"] is False
    assert new_guide["daily_study"][1]["completed"] is False
    assert new_guide["daily_study"][2]["completed"] is False

    response = auth_client.patch(
        f"/api/v1/guides/{new_guide['id']}",
        headers={"Content-Type": "application/json"},
        json={
            "new_studies_list": [
                {
                    "day": 1,
                    **new_guide["daily_study"][0],
                    "completed": True,
                },
                {
                    "day": 2,
                    **new_guide["daily_study"][1],
                    "completed": True,
                },
                {
                    "day": 3,
                    **new_guide["daily_study"][2],
                    "completed": False,
                },
            ]
        },
    )

    assert response.status_code == 200

    response_body = response.get_json()

    assert response_body == {
        "message": "O estado da Studies List foi alterado com sucesso!",
        "data": [
            {
                "day": 1,
                **response_body["data"][0],
                "completed": True,
            },
            {
                "day": 2,
                **new_guide["daily_study"][1],
                "completed": True,
            },
            {
                "day": 3,
                **new_guide["daily_study"][2],
                "completed": False,
            },
        ],
    }


@pytest.mark.vcr("test_PATCH_guides_id/test_update_studies_on_valid_guide.yaml")
def test_update_studies_with_unauthorized_user(auth_client):
    new_guide = orchestrator.create_guide()  # Random owner

    response = auth_client.patch(
        f"/api/v1/guides/{new_guide['id']}",
        headers={"Content-Type": "application/json"},
        json={
            "new_studies_list": [
                {
                    "day": 1,
                    **new_guide["daily_study"][0],
                    "completed": True,
                },
                {
                    "day": 2,
                    **new_guide["daily_study"][1],
                    "completed": True,
                },
                {
                    "day": 3,
                    **new_guide["daily_study"][2],
                    "completed": True,
                },
            ]
        },
    )

    assert response.status_code == 401

    response_body = response.get_json()

    assert response_body == {
        "name": "UnauthorizedError",
        "message": "Você não tem acesso à esse guia.",
        "action": "Acesse um guia de sua autoria e tente novamente.",
        "code": 401,
    }


@pytest.mark.vcr("test_PATCH_guides_id/test_update_studies_on_valid_guide.yaml")
def test_update_studies_with_completed_guide(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user["username"])

    assert new_guide["status"] == "studying"

    response = auth_client.patch(
        f"/api/v1/guides/{new_guide['id']}",
        headers={"Content-Type": "application/json"},
        json={
            "new_studies_list": [
                {
                    "day": 1,
                    **new_guide["daily_study"][0],
                    "completed": True,
                },
                {
                    "day": 2,
                    **new_guide["daily_study"][1],
                    "completed": True,
                },
                {
                    "day": 3,
                    **new_guide["daily_study"][2],
                    "completed": True,
                },
            ]
        },
    )

    assert response.status_code == 200

    response_body: dict[str, str] = response.get_json()
    assert response_body == {
        "message": "O estado da Studies List foi alterado com sucesso!",
        "data": [
            {
                "day": 1,
                **new_guide["daily_study"][0],
                "completed": True,
            },
            {
                "day": 2,
                **new_guide["daily_study"][1],
                "completed": True,
            },
            {
                "day": 3,
                **new_guide["daily_study"][2],
                "completed": True,
            },
        ],
    }

    completed_guide = guide.find_guide_by_id(new_guide["id"])
    assert completed_guide["status"] == "completed"
    assert completed_guide["completed_at"]
