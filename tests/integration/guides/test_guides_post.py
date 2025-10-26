from dotenv import load_dotenv
import os
import requests

from src.models import auth, session

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_generate_guide_with_minimal_inputs():
    s = requests.Session()

    user_data = auth.authenticate("mock@orienta.com", "123456")
    session_cookie = session.create(token=user_data["idToken"])

    s.cookies.set("session_id", session_cookie)

    response = s.post(
        f"{API_URL}/guides",
        json={
            "topic": "Workers",
            "objective": "Eu quero entender o que são os workers que eu tenho que configurar no gunicorn.",
            "study_time": "60",
            "duration_time": "3",
            "knowledge": "Eu sei um pouco sobre aplicações web, acabei de estudar sobre WSGI e entendi bem.",
        },
    )

    response_body = response.json()
    assert response_body == {
        "message": "Guia de estudos gerado com sucesso.",
        "data": {
            "owner": "mock",
            "inputs": {
                "duration_time": "3",
                "knowledge": "Eu sei um pouco sobre aplicações web, acabei de estudar sobre WSGI e entendi bem.",
                "objective": "Eu quero entender o que são os workers que eu tenho que configurar no gunicorn.",
                "study_time": "60",
                "topic": "Workers",
            },
            "model": "gemini-2.0-flash-lite",
            "temperature": 2,
            "generation_time_seconds": response_body["data"]["generation_time_seconds"],
            "daily_study": response_body["data"]["daily_study"],
            "created_at": response_body["data"]["created_at"],
            "is_public": False,
        },
    }


def test_generate_guide_with_full_inputs():
    s = requests.Session()

    user_data = auth.authenticate("mock@orienta.com", "123456")
    session_cookie = session.create(token=user_data["idToken"])

    s.cookies.set("session_id", session_cookie)

    response = s.post(
        f"{API_URL}/guides",
        json={
            "topic": "Workers",
            "objective": "Eu quero entender o que são os workers que eu tenho que configurar no gunicorn.",
            "study_time": "60",
            "duration_time": "3",
            "knowledge": "Eu sei um pouco sobre aplicações web, acabei de estudar sobre WSGI e entendi bem.",
            "temperature": 0.5,
            "validation": "det",
        },
    )
    response_body = response.json()
    assert response_body == {
        "message": "Guia de estudos gerado com sucesso.",
        "data": {
            "owner": "mock",
            "inputs": {
                "duration_time": "3",
                "knowledge": "Eu sei um pouco sobre aplicações web, acabei de estudar sobre WSGI e entendi bem.",
                "objective": "Eu quero entender o que são os workers que eu tenho que configurar no gunicorn.",
                "study_time": "60",
                "topic": "Workers",
            },
            "model": response_body["data"]["model"],
            "temperature": 0.5,
            "generation_time_seconds": response_body["data"]["generation_time_seconds"],
            "daily_study": response_body["data"]["daily_study"],
            "created_at": response_body["data"]["created_at"],
            "is_public": False,
        },
    }
