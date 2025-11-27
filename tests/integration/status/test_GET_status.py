import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_get_status():
    """
    Testa se a rota /status retorna o status da API.
    Essa é uma requisição anônima que não requer autenticação.
    """
    response = requests.get(f"{API_URL}/status")

    assert response.status_code in [200, 503]

    response_body = response.json()

    assert "status" in response_body
    assert response_body["status"] in ["Online", "Offline"]

    assert "message" in response_body
    assert isinstance(response_body["message"], str)

    # Verifica se o status code corresponde ao status retornado
    if response_body["status"] == "Online":
        assert response.status_code == 200
        assert response_body["message"] == "API está online"
    else:
        assert response.status_code == 503
        assert response_body["message"] == "API está offline"
