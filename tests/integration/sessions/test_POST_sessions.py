import requests

from models import session
from tests import orchestrator


def test_create_session_with_valid_data():
    new_user = orchestrator.create_user()

    response = requests.post(
        "http://localhost:5000/api/v1/sessions",
        json={"email": new_user["email"], "password": "validpassword"},
    )

    assert response.status_code == 201

    assert "session_id" in response.headers.get("Set-Cookie")

    body = response.json()

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


def test_create_session_with_wrong_email():
    response = requests.post(
        "http://localhost:5000/api/v1/sessions",
        json={"email": "wrong.email@orienta.com", "password": "123456"},
    )

    assert response.status_code == 401

    assert response.json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha errados.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_create_session_with_wrong_password():
    response = requests.post(
        "http://localhost:5000/api/v1/sessions",
        json={"email": "mock@orienta.com", "password": "wrong.password"},
    )

    assert response.status_code == 401

    assert response.json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha errados.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_create_session_without_email():
    response = requests.post(
        "http://localhost:5000/api/v1/sessions",
        json={"passowrd": "123456"},
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_create_session_without_password():
    response = requests.post(
        "http://localhost:5000/api/v1/sessions",
        json={"email": "mock@orienta.com"},
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }


def test_create_session_without_data():
    response = requests.post(
        "http://localhost:5000/api/v1/sessions",
        json={},
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
