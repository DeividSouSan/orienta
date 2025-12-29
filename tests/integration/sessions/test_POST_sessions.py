from models import session
from tests import orchestrator


def test_create_session_with_valid_data(client):
    new_user = orchestrator.create_user()

    response = client.post(
        "/api/v1/sessions",
        json={"email": new_user["email"], "password": "validpassword"},
    )

    assert response.status_code == 201

    assert "session_id" in response.headers.get("Set-Cookie")

    body = response.get_json()

    assert body == {
        "message": "Sessão criada com sucesso.",
        "data": {
            "userId": body["data"]["userId"],
            "username": new_user["username"],
            "email": new_user["email"],
            "sessionCookie": body["data"]["sessionCookie"],
            "sessionExpiresIn": session.DURATION_IN_SECONDS,
        },
    }


def test_create_session_with_wrong_email(client):
    response = client.post(
        "/api/v1/sessions",
        json={"email": "wrong.email@orienta.com", "password": "123456"},
    )

    assert response.status_code == 401

    assert response.get_json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha errados.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_create_session_with_wrong_password(client):
    response = client.post(
        "/api/v1/sessions",
        json={"email": "mock@orienta.com", "password": "wrong.password"},
    )

    assert response.status_code == 401

    assert response.get_json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha errados.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_create_session_without_email(client):
    response = client.post(
        "/api/v1/sessions",
        json={"passowrd": "123456"},
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_create_session_without_password(client):
    response = client.post(
        "/api/v1/sessions",
        json={"email": "mock@orienta.com"},
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_create_session_without_data(client):
    response = client.post(
        "/api/v1/sessions",
        json={},
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
