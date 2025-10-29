import requests
from dotenv import load_dotenv
import os

from src.models import auth, guide, session

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_delete_guide_with_valid_id():
    user_data = auth.authenticate("mock@orienta.com", "123456")

    s = requests.Session()
    session_cookie = session.create(user_data["idToken"])

    s.cookies.set("session_id", session_cookie)

    inputs = {
        "topic": "Mov. Ret. Uniforme",
        "objective": "Eu quero entender o que é o MRU (Movimento Reilíneo Uniforme) e como ele se aplica no dia-a-dia.",
        "study_time": "60",
        "duration_time": "3",
        "knowledge": "Eu estudei isso no ensino fundamental e médio e agora gostaria de revisar.",
    }

    guide_data = guide.generate_with_metadata(
        owner=user_data["displayName"], inputs=inputs, validation_type="det"
    )

    guide_id = guide.save(guide_data)

    response = s.delete(f"{API_URL}/guides/{guide_id}")

    assert response.status_code == 200

    assert response.json() == {"message": "Guia de estudo deletado com sucesso."}


def test_delete_guide_with_invalid_id():
    user_data = auth.authenticate("mock@orienta.com", "123456")

    s = requests.Session()
    session_cookie = session.create(user_data["idToken"])

    s.cookies.set("session_id", session_cookie)

    response = s.delete(f"{API_URL}/guides/123456")

    assert response.status_code == 404

    assert response.json() == {
        "name": "NotFoundError",
        "message": "Guia não encontrado.",
        "action": "Verifique o ID e tente novamente.",
        "code": 404,
    }
