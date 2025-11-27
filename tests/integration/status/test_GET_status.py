import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_get_status():
    response = requests.get(f"{API_URL}/status")

    assert response.status_code in [200, 503]

    response_body = response.json()
    print(response_body)

    assert "status" in response_body["data"]
    assert response_body["data"]["status"] in ["Online", "Offline"]

    assert "message" in response_body
    assert isinstance(response_body["message"], str)

    # Verifica se o status code corresponde ao status retornado
    if response_body["data"]["status"] == "Online":
        assert response.status_code == 200
        assert response_body["message"] == "API está online"
    else:
        assert response.status_code == 503
        assert response_body["message"] == "API está offline"
