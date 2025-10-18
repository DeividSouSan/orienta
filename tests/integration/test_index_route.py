import requests

from src.models import auth, session


class TestIndexRoute:
    def test_not_authenticated_user_navigation_to_index(self):
        """Test NOT AUTHENTICATED USER to navigate to '/' with GET / request"""

        response = requests.get("http://localhost:5000/")

        assert response.status_code == 200
        assert response.url == "http://localhost:5000/"
        assert "text/html" in response.headers["content-type"]
        assert "utf-8" in response.headers["content-type"]

        HTML = response.text
        assert '<header id="public-header"' in HTML
        assert "<footer" in HTML

    def test_user_with_invalid_cookie_navigation_to_index(self):
        """Test USER with not valid session_cookie to navigate to '/' with GET / request"""

        s = requests.Session()
        s.cookies.set(
            name="session_id",
            value="12345",
        )

        response = s.get("http://localhost:5000/")

        assert response.status_code == 200
        assert response.url == "http://localhost:5000/"
        assert "text/html" in response.headers["content-type"]
        assert "utf-8" in response.headers["content-type"]

        HTML = response.text
        assert '<header id="public-header"' in HTML
        assert "<footer" in HTML

    def test_authenticated_user_navigation_to_index(self):
        """Test AUTHENTICATED USER to navigate to '/' with GET / request"""

        user_data = auth.authenticate("mock@orienta.com", "123456")
        cookie_value = session.create(user_data["idToken"])

        s = requests.Session()
        s.cookies.set(
            name="session_id",
            value=cookie_value,
        )

        response = s.get("http://localhost:5000/")

        assert response.history[0].status_code == 302
        assert response.history[0].url == "http://localhost:5000/"

        assert response.status_code == 200
        assert response.url == "http://localhost:5000/plan"

        assert "text/html" in response.headers["content-type"]
        assert "utf-8" in response.headers["content-type"]

        HTML = response.text
        assert '<header id="private-header"' in HTML
        assert '<a href="/generate"' in HTML
        assert '<a href="/guides"' in HTML
        assert "<footer" in HTML
