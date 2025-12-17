import requests
from dotenv import load_dotenv
import os

from models import auth, session, user

load_dotenv()

API_URL = os.getenv("API_URL") or "http://localhost:5000/api/v1"


def test_get_current_user():
    user_data = user.find_by_username("mock")

    auth_user = auth.authenticate("mock@orienta.com", "123456")

    s = requests.Session()
    s.cookies.set("session_id", session.create(token=auth_user["idToken"]))

    response = s.get(API_URL + "/user")

    assert response.status_code == 200
    assert response.json() == {
        "uid": user_data["uid"],
        "email": user_data["email"],
        "username": user_data["username"],
        "created_at": user_data["created_at"],
    }
