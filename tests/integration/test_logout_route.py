"""
Logout é complexo:
a) test_logout_happy_path() → cria usuário (ou seed), login, guarda cookie, GET protegido (200), POST /logout, GET protegido (401).
b) test_logout_sem_cookie() → POST /logout sem cookie (espera 401 ou 204 consistente).
c) test_logout_cookie_invalido() → Cookie: session_id=valor_aleatorio → POST /logout (espera mesmo comportamento de b ou 204).
d) test_logout_idempotente() → login → logout → logout novamente.
e) test_replay_cookie() → login → copia cookie → logout → tenta endpoint protegido com cookie copiado (401/403).
"""

from datetime import datetime, timezone
from http.cookies import SimpleCookie
import requests

from src.models import auth, session

# testar com GET


class TestLogoutRoute:
    def test_authenticated_user_logout_with_POST_request(self):
        user_data = auth.authenticate("mock@orienta.com", "123456")
        cookie_value = session.create(user_data["idToken"])

        s = requests.Session()
        s.cookies.set(
            name="session_id",
            value=cookie_value,
        )

        response = s.post("http://localhost:5000/logout", allow_redirects=False)

        cookie = SimpleCookie()
        cookie.load(response.headers.get("Set-Cookie"))

        sid = cookie["session_id"]
        assert sid.value == ""
        assert sid["max-age"] == "0"

        exp = datetime.strptime(sid["expires"], "%a, %d %b %Y %H:%M:%S GMT").replace(
            tzinfo=timezone.utc
        )  # adiciona um offset ao expires que era naive
        assert exp < datetime.now(timezone.utc)

    def test_authenticated_user_logout_with_GET_request(self):
        user_data = auth.authenticate("mock@orienta.com", "123456")
        cookie_value = session.create(user_data["idToken"])

        s = requests.Session()
        s.cookies.set(
            name="session_id",
            value=cookie_value,
        )

        response = s.get("http://localhost:5000/logout", allow_redirects=True)

        assert response.history[0].status_code == 302
        assert response.history[0].url == "http://localhost:5000/logout"

        assert response.status_code == 200
        assert response.url == "http://localhost:5000/plan"
