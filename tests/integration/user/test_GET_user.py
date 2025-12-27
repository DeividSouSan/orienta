import requests
from tests import orchestrator


def test_get_current_user():
    orchestrator.create_user(username="mock", email="mock@orienta.com")
    session_cookie = orchestrator.authenticate("mock@orienta.com", "validpassword")

    response = requests.get(
        "http://localhost:5000/api/v1/user", cookies={"session_id": session_cookie}
    )

    assert response.status_code == 200

    response_body = response.json()
    print(response_body)
    assert response_body == {
        "message": "Usuário atual recuperado com sucesso.",
        "data": {
            "uid": response_body["data"]["uid"],
            "username": "mock",
            "email": "mock@orienta.com",
            "created_at": response_body["data"]["created_at"],
        },
    }
