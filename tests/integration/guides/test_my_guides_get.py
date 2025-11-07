import os

from dotenv import load_dotenv

from src.models import guide

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_get_my_guides(mock_session):
    guide1 = guide.generate_with_metadata(
        "mock",
        inputs={
            "topic": "Eu gostaria de estudar sobre a teoria da evolução de darwin.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 5,
        },
    )
    guide.save(guide1)

    response = mock_session.get(f"{API_URL}/my-guides")

    assert response.status_code == 200
    response_body = response.json()

    assert response_body == {
        "message": "Guias recuperados com sucesso.",
        "data": [
            {
                "id": response_body["data"][0]["id"],
                "title": response_body["data"][0]["title"],
                "topic": "Eu gostaria de estudar sobre a teoria da evolução de darwin.",
                "days": 5,
                "completed_days": 0,
                "created_at": response_body["data"][0]["created_at"],
                "status": "studying",
            }
        ],
    }
