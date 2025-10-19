from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1/")


def test_create_session():
    response = requests.post(
        f"{API_URL}sessions",
        json={"email": "mock@orienta.com", "password": "123456"},
    )

    assert response.status_code == 201

    assert response.headers.get("Set-Cookie")
    assert "session_id" in response.cookies

    assert response.json() == {
        "userId": response.json().get("userId"),
        "username": "mock",
        "email": "mock@orienta.com",
        "sessionCookie": response.json().get("sessionCookie"),
        "sessionExpiresIn": 1209600,
    }


def test_create_session_wrong_email():
    response = requests.post(
        f"{API_URL}sessions",
        json={"email": "not_mock@orienta.com", "password": "123456"},
    )

    assert response.status_code == 401

    assert response.json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_create_session_wrong_password():
    response = requests.post(
        f"{API_URL}sessions",
        json={"email": "mock@orienta.com", "password": "wrong_password"},
    )

    assert response.status_code == 401

    assert response.json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_create_session_missing_fields():
    response = requests.post(
        f"{API_URL}sessions",
        json={},
    )

    assert response.status_code == 401

    assert response.json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha inválidos.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }
