import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL") or "http://localhost:5000/api/v1/"


def test_create_user():
    response = requests.post(
        API_URL + "user",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("displayName") == "testuser"
    assert response_json.get("email") == "testuser@example.com"


def test_create_user_without_username():
    response = requests.post(
        API_URL + "user",
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Insira um username maior que 3 caracteres.",
        "code": 400,
    }


def test_create_user_without_email():
    response = requests.post(
        API_URL + "user",
        json={
            "username": "testuser",
            "password": "testpassword",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Insira um email válido.",
        "code": 400,
    }


def test_create_user_without_password():
    response = requests.post(
        API_URL + "user",
        json={
            "username": "testuser",
            "email": "testuser2@example.com",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Insira uma senha maior que 6 caracteres.",
        "code": 400,
    }


def test_create_user_with_duplicated_email():
    response_1 = requests.post(
        API_URL + "user",
        json={
            "username": "testuser",
            "email": "in.use.email@example.com",
            "password": "testpassword",
        },
    )

    assert response_1.status_code == 200

    response_2 = requests.post(
        API_URL + "user",
        json={
            "username": "anotheruser",
            "email": "in.use.email@example.com",  # Using the same email
            "password": "testpassword",
        },
    )

    assert response_2.json() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "O email informado já está sendo utilizado.",
        "code": 400,
    }
