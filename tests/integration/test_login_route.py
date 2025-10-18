from datetime import datetime
import requests
from http.cookies import SimpleCookie

from src.models import auth, session


class TestLoginRoute:
    def test_not_authenticated_user_to_navigate_to_login_route(self):
        """Test NOT AUTHENTICATED USER to navigate to '/login' with GET request"""

        response = requests.get("http://localhost:5000/login")

        assert response.status_code == 200
        assert response.url == "http://localhost:5000/login"
        assert "text/html" in response.headers["content-type"]
        assert "utf-8" in response.headers["content-type"]

        HTML = response.text
        assert "<form" in HTML
        assert 'name="email"' in HTML
        assert 'name="password"' in HTML
        assert "<button" in HTML or 'type="submit"' in HTML

    def test_authenticated_user_to_navigate_to_login_route(self):
        """Test AUTHENTICATED USER to navigate to '/login' with GET request"""

        user_data = auth.authenticate("mock@orienta.com", "123456")
        cookie_value = session.create(user_data["idToken"])

        s = requests.Session()
        s.cookies.set(
            name="session_id",
            value=cookie_value,
        )

        response = s.get("http://localhost:5000/login")
        assert "text/html" in response.headers["content-type"]
        assert "utf-8" in response.headers["content-type"]

        assert response.history[0].status_code == 302
        assert response.history[0].url == "http://localhost:5000/login"

        assert response.status_code == 200
        assert response.url == "http://localhost:5000/plan"

    def test_authentication_set_cookie_data(self):
        """Test Set-Cookie data is correct"""

        response = requests.post(
            "http://localhost:5000/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "email": "mock@orienta.com",
                "password": "123456",
            },
            allow_redirects=False,
        )

        assert response.status_code == 302
        assert response.url == "http://localhost:5000/login"
        assert "text/html" in response.headers["Content-Type"]
        assert "utf-8" in response.headers["Content-Type"]

        cookie = SimpleCookie()
        cookie.load(response.headers.get("Set-Cookie"))
        sess = cookie["session_id"]
        assert sess["max-age"] == str(session.DURATION_IN_SECONDS)
        assert sess["httponly"] is True
        assert "/" in sess["path"]

        EXPIRES = datetime.strptime(sess["expires"], "%a, %d %b %Y %H:%M:%S GMT")
        NOW = datetime.now()

        assert EXPIRES > NOW

    def test_authentication_with_correct_email_and_correct_password(self):
        """Test authentication process"""

        response = requests.post(
            "http://localhost:5000/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "email": "mock@orienta.com",
                "password": "123456",
            },
            allow_redirects=True,
        )

        assert "text/html" in response.headers["Content-Type"]
        assert "utf-8" in response.headers["Content-Type"]

        assert response.history[0].status_code == 302
        assert response.history[0].url == "http://localhost:5000/login"

        assert response.status_code == 200
        assert response.url == "http://localhost:5000/plan"

        cookie = SimpleCookie()
        cookie.load(response.request.headers.get("Cookie"))
        assert cookie["session_id"]
