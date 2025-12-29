def test_get_current_user(auth_client, new_user):
    response = auth_client.get("/api/v1/user")

    assert response.status_code == 200

    response_body = response.get_json()

    assert response_body == {
        "message": "Usuário atual recuperado com sucesso.",
        "data": {
            "uid": response_body["data"]["uid"],
            "username": new_user["username"],
            "email": new_user["email"],
            "created_at": response_body["data"]["created_at"],
        },
    }
