import pytest

from tests import orchestrator


@pytest.fixture(scope="module")
def shared_user():
    return orchestrator.create_user()


@pytest.mark.vcr
def test_with_valid_data(client, shared_user):
    response = client.post(
        "/api/v1/sessions",
        json={
            "email": shared_user["email"],
            "password": "validpassword",
        },
    )

    assert response.status_code == 201
    assert "session_id" in response.headers.get("Set-Cookie")

    body = response.get_json()

    assert body == {
        "message": "Sessão criada com sucesso.",
    }


def test_with_wrong_email(client):
    response = client.post(
        "/api/v1/sessions",
        json={
            "email": "wrong.email@orienta.com",
            "password": "123456",
        },
    )

    assert response.status_code == 401

    assert response.get_json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha errados.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_with_correct_email_and_wrong_password(client, shared_user):
    response = client.post(
        "/api/v1/sessions",
        json={
            "email": shared_user["email"],
            "password": "wrong.password",
        },
    )

    assert response.status_code == 401

    assert response.get_json() == {
        "name": "UnauthorizedError",
        "message": "Email ou senha errados.",
        "action": "Verifique os dados e tente novamente.",
        "code": 401,
    }


def test_session_cookie_has_correct_max_age(client, shared_user):
    response = client.post(
        "/api/v1/sessions",
        json={
            "email": shared_user["email"],
            "password": "validpassword",
        },
    )

    assert response.status_code == 201

    # Verificar que o cookie tem max_age de 14 dias (1209600 segundos)
    set_cookie_header = response.headers.get("Set-Cookie")
    assert "Max-Age=1209600" in set_cookie_header


def test_session_cookie_has_httponly_flag(client, shared_user):
    response = client.post(
        "/api/v1/sessions",
        json={
            "email": shared_user["email"],
            "password": "validpassword",
        },
    )

    assert response.status_code == 201

    # Verificar que o cookie tem flag HttpOnly para segurança
    set_cookie_header = response.headers.get("Set-Cookie")
    assert "HttpOnly" in set_cookie_header


def test_session_cookie_path_is_root(client, shared_user):
    response = client.post(
        "/api/v1/sessions",
        json={
            "email": shared_user["email"],
            "password": "validpassword",
        },
    )

    assert response.status_code == 201

    # Verificar que o cookie está disponível em todo o domínio (Path=/)
    set_cookie_header = response.headers.get("Set-Cookie")
    assert "Path=/" in set_cookie_header
