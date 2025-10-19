from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1/")


def test_retrieve_session_data():
    s = requests.Session()

    response1 = s.post(
        f"{API_URL}sessions",
        json={"email": "mock@orienta.com", "password": "123456"},
    )

    assert response1.status_code == 201
    assert response1.headers.get("Set-Cookie") is not None

    response2 = s.get(f"{API_URL}sessions")

    assert response2.status_code == 200
    assert response2.request.headers.get("Cookie") is not None
    assert response2.json() == {
        "userId": response1.json().get("userId"),
        "username": "mock",
        "email": "mock@orienta.com",
    }
