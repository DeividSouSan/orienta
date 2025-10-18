from datetime import datetime, timedelta, timezone

import pytest
from src.errors import ValidationError, UnauthorizedError
from src.models import auth, session
import jwt


class TestSession:
    def test_create_with_valid_user(self):
        user_data = auth.authenticate(email="mock@orienta.com", password="123456")

        session_cookie = session.create(token=user_data["idToken"])

        assert session_cookie is not None
        assert isinstance(session_cookie, str)

    def test_create_with_empty_id_token(self):
        with pytest.raises(ValidationError) as error:
            session.create(token="")

        assert (error.value.message) == "O idToken não pode ser vazio."

    def test_create_with_not_string_token(self):
        with pytest.raises(ValidationError) as error:
            session.create(token=9)

        assert error.value.message == "O idToken deve ser um texto."

    def test_create_with_invalid_id_token(self):
        with pytest.raises(UnauthorizedError) as error:
            session.create(token="invalid_id_token")

        assert error.value.message == "O idToken fornecido é inválido."

    def test_create_with_invalid_duration(self):
        user_data = auth.authenticate(email="mock@orienta.com", password="123456")

        with pytest.raises(ValidationError) as error:
            session.create(
                token=user_data["idToken"], duration=timedelta(days=30)
            )  # too long duration

        assert (
            error.value.message == "Duração da sessão é tem que ser menor que 14 dias."
        )

    def test_session_cookie_basic_claims(self):
        user_data = auth.authenticate(email="mock@orienta.com", password="123456")

        session_cookie = session.create(token=user_data["idToken"])

        header = jwt.get_unverified_header(session_cookie)
        payload = jwt.decode(session_cookie, options={"verify_signature": False})

        assert session_cookie is not None
        assert header["alg"] == "RS256"
        assert payload["sub"] == user_data["localId"]
        assert payload["user_id"] == user_data["localId"]
        assert payload["email"] == user_data["email"]

        TIME_TOLERANCE = 10  # 10 SEGUNDOS
        current_timestamp = datetime.now(timezone.utc).timestamp()

        assert payload["iat"] <= current_timestamp + TIME_TOLERANCE
        assert payload["exp"] > current_timestamp
        assert payload["exp"] > payload["iat"]

    def test_verify_without_cookie(self):
        with pytest.raises(UnauthorizedError) as error:
            session.verify(cookie="")

        assert error.value.name == "UnauthorizedError"
        assert error.value.message == "O cookie de sessão não pode ser vazio."

    def test_verify_with_invalid_session_cookie(self):
        with pytest.raises(UnauthorizedError) as error:
            session.verify(cookie="1234")

        assert error.value.name == "UnauthorizedError"
        assert error.value.message == "Sessão inválida ou expirada."
