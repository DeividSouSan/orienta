import pytest
from tests import orchestrator


@pytest.mark.vcr
def test_delete_guide_with_valid_id(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user["username"])

    response = auth_client.delete(f"/api/v1/guides/{new_guide['id']}")

    assert response.status_code == 200

    response_body = response.get_json()

    assert response_body == {"message": "Guia de estudo deletado com sucesso."}


def test_delete_guide_with_invalid_id(auth_client):
    response = auth_client.delete("/api/v1/guides/123456")

    assert response.status_code == 404

    response_body = response.get_json()

    assert response_body == {
        "name": "NotFoundError",
        "message": "Guia não encontrado.",
        "action": "Verifique o ID e tente novamente.",
        "code": 404,
    }
