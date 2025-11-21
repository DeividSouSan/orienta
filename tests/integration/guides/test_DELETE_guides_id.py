from dotenv import load_dotenv
import os

from src.models import guide

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_delete_guide_with_valid_id(mock_session):
    guide_data = guide.generate_with_metadata(
        title="Test DELETE Method",
        owner="mock",
        inputs={
            "topic": "Eu gostaria de estudar sobe o Brasil colônia. Gostaria de entender o básico do que aconteceu.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 5,
        },
    )

    guide_id = guide.save(guide_data)

    response = mock_session.delete(f"{API_URL}/guides/{guide_id}")

    assert response.status_code == 200

    assert response.json() == {"message": "Guia de estudo deletado com sucesso."}


def test_delete_guide_with_invalid_id(mock_session):
    response = mock_session.delete(f"{API_URL}/guides/123456")

    assert response.status_code == 404

    assert response.json() == {
        "name": "NotFoundError",
        "message": "Guia não encontrado.",
        "action": "Verifique o ID e tente novamente.",
        "code": 404,
    }
