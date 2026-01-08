import pytest
from tests import orchestrator


@pytest.mark.vcr
def test_with_valid_id(auth_client, new_user):
    new_guide = orchestrator.create_guide(owner=new_user["username"])

    response1 = auth_client.delete(f"/api/v1/guides/{new_guide['id']}")
    response1_body = response1.get_json()

    assert response1.status_code == 200
    assert response1_body == {"message": "Guia de estudo deletado com sucesso."}

    response2 = auth_client.get(f"/api/v1/guides/{new_guide['id']}")
    response2_body = response2.get_json()

    assert response2_body == {
        "message": response2_body["message"],
        "data": {
            **response2_body["data"],
            "status": "deleted",
        },
    }


def test_with_just_spaces(auth_client):
    response = auth_client.delete("/api/v1/guides/                   ")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "name": "ValidationError",
        "message": "ID do Guia não é válido.",
        "action": "Verifique o ID e tente novamente.",
        "code": 400,
    }


def test_with_blank_spaces(auth_client):
    response = auth_client.delete("/api/v1/guides/                   muitos espaços")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "name": "NotFoundError",
        "message": "Guia não encontrado.",
        "action": "Verifique o ID e tente novamente.",
        "code": 404,
    }


def test_with_invalid_id(auth_client):
    response = auth_client.delete("/api/v1/guides/pasteldequeijo")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "name": "NotFoundError",
        "message": "Guia não encontrado.",
        "action": "Verifique o ID e tente novamente.",
        "code": 404,
    }


def test_with_valid_but_inexistant_id(auth_client):
    response = auth_client.delete("/api/v1/guides/3vT2Ot6aVi9glNMcIzW1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "name": "NotFoundError",
        "message": "Guia não encontrado.",
        "action": "Verifique o ID e tente novamente.",
        "code": 404,
    }


@pytest.mark.vcr
def test_with_someone_else_guide(auth_client):
    new_guide = orchestrator.create_guide(owner="mock")

    response = auth_client.delete(f"/api/v1/guides/{new_guide['id']}")
    response_body = response.get_json()

    assert response.status_code == 403
    assert response_body == {
        "name": "ForbiddenError",
        "message": "Você não tem permissão para deletar esse guia.",
        "action": "Verifique se o guia é de sua autoria e tente novamente.",
        "code": 403,
    }


def test_with_unauthorized_user(client):
    response = client.delete("/api/v1/guides/3vT2Ot6aVi9glNMcIzW1")
    response_body = response.get_json()

    assert response.status_code == 401
    assert response_body == {
        "name": "UnauthorizedError",
        "message": "Cookie de sessão não encontrado.",
        "action": "Faça login para continuar.",
        "code": 401,
    }
