from dotenv import load_dotenv
import os
from time import sleep
from src.models import user
from src.models import guide

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_get_guide(mock_session):
    user.create(username="ava", email="ava@orienta.com", password="123456")
    new_guide = guide.generate_with_metadata(
        owner="ava",
        inputs={
            "topic": "Eu quero estudar sobre docker. Como funciona e quais são seus principais comandos.",
            "knowledge": "zero",
            "focus_time": 45,
            "days": 3,
        },
    )

    guide.save(new_guide)

    sleep(10)

    print("Até aqui foi o guia foi salvo.")
    guide_from_db = guide.find_by_username("ava")
    assert len(guide_from_db) == 1

    new_guide_id = guide_from_db[0].get("id", None)
    assert new_guide_id is not None

    response = mock_session.get(f"{API_URL}/guides/{new_guide_id}")
    assert response.status_code == 200

    response_body: dict[str, str] = response.json()
    assert response_body == {
        "message": "Guia recuperado com sucesso.",
        "data": {
            "title": f"Guia: {new_guide_id}",
            "model": response_body["data"].get("model", ""),
            "is_public": False,
            "owner": "ava",
            "status": "studying",
            "temperature": 2,
            "completed_days": 0,
            "created_at": response_body["data"].get("created_at", ""),
            "generation_time_seconds": response_body["data"].get(
                "generation_time_seconds", ""
            ),
            "inputs": {
                "topic": "Eu quero estudar sobre docker. Como funciona e quais são seus principais comandos.",
                "knowledge": "zero",
                "focus_time": 45,
                "days": 3,
            },
            "daily_study": response_body["data"].get("daily_study", ""),
        },
    }


def test_get_nonexistent_guide(mock_session):
    response = mock_session.get(f"{API_URL}/guides/123")

    assert response.status_code == 404

    assert response.json() == {
        "name": "NotFoundError",
        "message": "O guia não foi encontrado.",
        "action": "Verifique que o guia existe e tente novamente.",
        "code": 404,
    }
