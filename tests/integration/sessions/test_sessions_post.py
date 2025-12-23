from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_create_session_with_valid_data():
    response = requests.post(
        f"{API_URL}/sessions",
        json={"email": "mock@orienta.com", "password": "123456"},
    )

    assert response.status_code == 201

    assert response.headers.get("Set-Cookie")
    assert "session_id" in response.cookies

    body = response.json()

    assert body == {
        "message": "Sessão criada com sucesso.",
        "data": {
            "userId": body["data"]["userId"],
            "username": "mock",
            "email": "mock@orienta.com",
            "sessionCookie": body["data"]["sessionCookie"],
            "sessionExpiresIn": 1209600,
        },
    }


def test_create_session_with_wrong_email():
    response = requests.post(
        f"{API_URL}/sessions",
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
        f"{API_URL}/sessions",
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
        f"{API_URL}/sessions",
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
        f"{API_URL}/sessions",
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
        f"{API_URL}/sessions",
        json={},
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 400,
    }
