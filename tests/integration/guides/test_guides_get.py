from dotenv import load_dotenv
import os

from src.models import user
from src.models import guide

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_get_public_guides_with_existent_username(mock_session):
    user.create(username="ava", email="ava@orienta.com", password="123456")
    guide1 = guide.generate_with_metadata(
        owner="ava",
        inputs={
            "topic": "Eu quero estudar sobre docker. Como funciona e quais são seus principais comandos.",
            "knowledge": "zero",
            "focus_time": 45,
            "days": 3,
        },
        is_public=True,
    )

    guide.save(guide1)

    response = mock_session.get(f"{API_URL}/guides/ava")
    assert response.status_code == 200

    response_body = response.json()
    assert response_body["message"] == "Guias recuperados com sucesso."
    assert len(response_body["data"]) == 1


def test_get_public_guides_with_nonexistent_username(mock_session):
    response = mock_session.get(f"{API_URL}/guides/nonexistent_user")

    assert response.status_code == 404

    response_body: dict = response.json()
    assert response_body == {
        "name": "NotFoundError",
        "message": "O usuário não foi encontrado.",
        "action": "Verifique se o nome foi digitado corretamente e tente de novo.",
        "code": 404,
    }


def test_get_public_guides_with_too_short_username(mock_session):
    response = mock_session.get(f"{API_URL}/guides/12")

    assert response.status_code == 400

    response_body: dict = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O nome de usuário inserido não é válido.",
        "action": "Insira um nome de usuário maior que 3 caracteres e menor que 20 caracteres.",
        "code": 400,
    }


def test_get_public_guides_with_too_long_username(mock_session):
    response = mock_session.get(f"{API_URL}/guides/123456789101112131415")

    assert response.status_code == 400

    response_body: dict = response.json()
    assert response_body == {
        "name": "ValidationError",
        "message": "O nome de usuário inserido não é válido.",
        "action": "Insira um nome de usuário maior que 3 caracteres e menor que 20 caracteres.",
        "code": 400,
    }


def test_get_my_guides(mock_session):
    guide1 = guide.generate_with_metadata(
        owner="mock",
        inputs={
            "topic": "Eu quero estudar sobre docker. Como funciona e quais são seus principais comandos.",
            "knowledge": "zero",
            "focus_time": 45,
            "days": 3,
        },
    )

    guide.save(guide1)

    response = mock_session.get(f"{API_URL}/my-guides")

    assert response.status_code == 200

    response_body: dict = response.json()
    assert response_body["message"] == "Guias recuperados com sucesso."
    assert len(response_body["data"]) == 1
