from datetime import datetime, timezone
from http.cookies import SimpleCookie
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1/")


def test_delete_session():
    s = requests.Session()

    response1 = s.post(
        API_URL + "sessions", json={"email": "mock@orienta.com", "password": "123456"}
    )

    assert response1.status_code == 201
    assert response1.headers.get("Set-Cookie") is not None

    response2 = s.delete(API_URL + "sessions")

    cookie = SimpleCookie()
    cookie.load(response2.headers.get("Set-Cookie"))

    sid = cookie["session_id"]
    assert sid.value == ""
    assert sid["max-age"] == "0"

    exp = datetime.strptime(sid["expires"], "%a, %d %b %Y %H:%M:%S GMT").replace(
        tzinfo=timezone.utc
    )  # adiciona um offset ao expires que era naive
    assert exp < datetime.now(timezone.utc)
