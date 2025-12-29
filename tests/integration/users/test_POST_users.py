import time


def test_create_user_with_valid_data(client):
    response = client.post(
        "/api/v1/users",
        json={
            "username": "valid.user",
            "email": "valid.user@orienta.com",
            "password": "validuser",
        },
    )

    assert response.status_code == 201

    response_body = response.get_json()

    assert response_body == {
        "message": "Usuário criado com sucesso.",
        "data": {
            "username": "valid.user",
            "email": "valid.user@orienta.com",
            "uid": response_body["data"]["uid"],
            "created_at": response_body["data"]["created_at"],
        },
    }

    assert int(response_body["data"]["created_at"]) < int(time.time() * 1000)


def test_create_user_without_username(client):
    response = client.post(
        "/api/v1/users",
        json={
            "email": "without.username@example.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O nome de usuário inserido não é válido.",
        "action": "Insira um nome de usuário maior que 3 caracteres.",
        "code": 400,
    }


def test_create_user_without_email(client):
    response = client.post(
        "/api/v1/users",
        json={
            "username": "without.email",
            "password": "testpassword",
        },
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Verifique o e-mail e tente novamente.",
        "code": 400,
    }


def test_create_user_without_password(client):
    response = client.post(
        "/api/v1/users",
        json={
            "username": "without.password",
            "email": "without.password@example.com",
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Insira uma senha maior que 6 caracteres.",
        "code": 400,
    }


def test_create_user_with_short_password(client):
    response = client.post(
        "/api/v1/users",
        json={
            "username": "short.password",
            "email": "short.password@example.com",
            "password": "123",  # deveria ter pelo menos 6 caracteres -> https://firebase.google.com/docs/auth/admin/manage-users?hl=pt-br#create_a_user
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "Ocorreu um erro de validação nos dados fornecidos.",
        "action": "Insira uma senha maior que 6 caracteres.",
        "code": 400,
    }


def test_create_user_with_duplicated_email(client):
    response_1 = client.post(
        "/api/v1/users",
        json={
            "username": "duplicated.email.1",
            "email": "duplicated.email@example.com",
            "password": "testpassword",
        },
    )

    assert response_1.status_code == 201

    response_2 = client.post(
        "/api/v1/users",
        json={
            "username": "duplicated.email.2",
            "email": "duplicated.email@example.com",  # usando o mesmo email
            "password": "testpassword",
        },
    )

    assert response_2.status_code == 409

    response_2_body = response_2.get_json()
    assert response_2_body == {
        "name": "ConflictError",
        "message": "O e-mail fornecido já está sendo utilizado.",
        "action": "Insira outro e-mail e tente novamente.",
        "code": 409,
    }


def test_create_user_with_duplicated_username(client):
    response_1 = client.post(
        "/api/v1/users",
        json={
            "username": "duplicated.user",
            "email": "duplicated.user.1@example.com",
            "password": "testpassword",
        },
    )

    assert response_1.status_code == 201

    response_2 = client.post(
        "/api/v1/users",
        json={
            "username": "duplicated.user",  # usando o mesmo username
            "email": "duplicated.user.2@example.com",
            "password": "testpassword",
        },
    )

    assert response_2.status_code == 409

    response_2_body = response_2.get_json()

    assert response_2_body == {
        "name": "ConflictError",
        "message": "O nome de usuário fornecido já está sendo utilizado.",
        "action": "Insira outro nome de usuário e tente novamente.",
        "code": 409,
    }
