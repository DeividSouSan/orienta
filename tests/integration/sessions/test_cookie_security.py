from unittest.mock import patch

import pytest

from tests import orchestrator


@pytest.fixture(scope="module")
def shared_user():
    return orchestrator.create_user()


@pytest.mark.vcr
def test_cookie_secure_flag_in_production(client, shared_user):
    # Patch ENV directly in the sessions module
    with patch("api.v1.sessions.ENV", "production"):
        response = client.post(
            "/api/v1/sessions",
            json={
                "email": shared_user.email,
                "password": "validpassword",
            },
        )

        assert response.status_code == 201
        set_cookie_header = response.headers.get("Set-Cookie")
        assert "Secure" in set_cookie_header


@pytest.mark.vcr
def test_cookie_secure_flag_not_in_development(client, shared_user):
    # Patch ENV directly in the sessions module
    with patch("api.v1.sessions.ENV", "development"):
        response = client.post(
            "/api/v1/sessions",
            json={
                "email": shared_user.email,
                "password": "validpassword",
            },
        )

        assert response.status_code == 201
        set_cookie_header = response.headers.get("Set-Cookie")
        assert "Secure" not in set_cookie_header
