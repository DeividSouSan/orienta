def test_with_authenticated_user(auth_client, new_user):
    response = auth_client.get("/api/v1/user")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "message": "Usuário atual recuperado com sucesso.",
        "data": {
            "uid": response_body["data"]["uid"],
            "username": new_user["username"],
            "email": new_user["email"],
            "created_at": response_body["data"]["created_at"],
        },
    }


def test_with_unauthorized_user(client):
    response = client.get("/api/v1/user")
    response_body = response.get_json()

    assert response.status_code == 401
    assert response_body == {
        "name": "UnauthorizedError",
        "message": "Cookie de sessão não encontrado.",
        "action": "Faça login para continuar.",
        "code": 401,
    }
