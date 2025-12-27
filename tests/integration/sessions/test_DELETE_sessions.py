from datetime import datetime, timezone
from http.cookies import SimpleCookie
import requests


def test_delete_session():
    response = requests.delete("http://localhost:5000/api/v1/sessions")

    assert response.status_code == 200

    cookie = SimpleCookie()
    cookie.load(response.headers.get("Set-Cookie"))

    session_id = cookie["session_id"]
    assert session_id.value == ""
    assert session_id["max-age"] == "0"

    expires = datetime.strptime(
        session_id["expires"], "%a, %d %b %Y %H:%M:%S GMT"
    ).replace(tzinfo=timezone.utc)  # adiciona um offset ao expires que era naive

    assert expires < datetime.now(timezone.utc)
