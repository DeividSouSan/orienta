import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL") or "http://localhost:5000/api/v1"


def test_create_user_with_valid_data():
    response = requests.post(
        API_URL + "/users",
        json={
            "username": "valid.data",
            "email": "valid.data@example.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("username") == "valid.data"
    assert response_json.get("email") == "valid.data@example.com"


def test_create_user_without_username():
    response = requests.post(
        API_URL + "/users",
        json={
            "email": "without.username@example.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "O nome de usuário inserido não é válido.",
        "action": "Insira um nome de usuário maior que 3 caracteres e menor que 20 caracteres.",
        "code": 400,
    }


def test_create_user_without_email():
    response = requests.post(
        API_URL + "/users",
        json={
            "username": "without.email",
            "password": "testpassword",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Verifique o e-mail e tente novamente.",
        "code": 400,
    }


def test_create_user_without_password():
    response = requests.post(
        API_URL + "/users",
        json={
            "username": "without.password",
            "email": "without.password@example.com",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Insira uma senha maior que 6 caracteres.",
        "code": 400,
    }


def test_create_user_with_short_password():
    response = requests.post(
        API_URL + "/users",
        json={
            "username": "short.password",
            "email": "short.password@example.com",
            "password": "123",  # deveria ter pelo menos 6 caracteres -> https://firebase.google.com/docs/auth/admin/manage-users?hl=pt-br#create_a_user
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
        API_URL + "/users",
        json={
            "username": "duplicated.email.1",
            "email": "duplicated.email@example.com",
            "password": "testpassword",
        },
    )

    assert response_1.status_code == 200

    response_2 = requests.post(
        API_URL + "/users",
        json={
            "username": "duplicated.email.2",
            "email": "duplicated.email@example.com",  # Using the same email
            "password": "testpassword",
        },
    )

    assert response_2.status_code == 409

    assert response_2.json() == {
        "name": "ConflictError",
        "message": "O e-mail fornecido já está sendo utilizado.",
        "action": "Insira outro e-mail e tente novamente.",
        "code": 409,
    }


def test_create_user_with_duplicated_username():
    response_1 = requests.post(
        API_URL + "/users",
        json={
            "username": "duplicated.user",
            "email": "duplicated.user.1@example.com",
            "password": "testpassword",
        },
    )

    assert response_1.status_code == 200

    response_2 = requests.post(
        API_URL + "/users",
        json={
            "username": "duplicated.user",  # using the same username
            "email": "duplicated.user.2@example.com",
            "password": "testpassword",
        },
    )

    assert response_2.status_code == 409

    assert response_2.json() == {
        "name": "ConflictError",
        "message": "O nome de usuário fornecido já está sendo utilizado.",
        "action": "Insira outro nome de usuário e tente novamente.",
        "code": 409,
    }
