def test_get_status(client):
    response = client.get("/api/v1/status")

    assert response.status_code == 200

    response_body = response.get_json()

    assert response_body == {
        "message": "API está online.",
        "data": {"status": "Online"},
    }
