import os

from dotenv import load_dotenv

from src.models import guide

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_get_my_guides(mock_session):
    new_guide = guide.generate_with_metadata(
        owner="mock",
        inputs={
            "topic": "Eu quero estudar sobre docker. Como funciona e quais são seus principais comandos.",
            "knowledge": "zero",
            "focus_time": 45,
            "days": 3,
        },
    )

    new_guide_id = guide.save(new_guide)

    response = mock_session.get(f"{API_URL}/guides")

    assert response.status_code == 200

    response_body: dict = response.json()
    assert response_body["message"] == "Guias recuperados com sucesso."
    assert len(response_body["data"]) == 1
    assert response_body["data"][0] == {
        "created_at": response_body["data"][0]["created_at"],
        "daily_studies": response_body["data"][0]["daily_studies"],
        "days": 3,
        "id": new_guide_id,
        "status": "studying",
        "title": f"Guia: {new_guide_id}",
        "topic": response_body["data"][0]["topic"],
    }
