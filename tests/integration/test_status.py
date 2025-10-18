import requests


class TestStatusPage:
    def test_status_online(self):
        """Testa se o status retorna 'online' quando o banco está conectado"""
        response = requests.get("http://localhost:5000/status")

        assert response.status_code == 200
        assert "Online" in response.text
