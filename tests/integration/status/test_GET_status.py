import requests


def test_get_status():
    response = requests.get("http://localhost:5000/api/v1/status")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body == {
        "message": "API está online.",
        "data": {"status": "Online"},
    }
