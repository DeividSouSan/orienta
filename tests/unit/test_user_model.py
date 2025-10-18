from datetime import datetime, timezone
import pytest

from src.errors import ValidationError
from src.models import user


class TestUserCreation:
    def test_with_valid_data(self):
        created_user = user.create(
            username="valid.user", email="valid.user@orienta.com", password="123456"
        )

        assert created_user["displayName"] == "valid.user"
        assert created_user["email"] == "valid.user@orienta.com"
        assert created_user["createdAt"] is not None

        created_at_dt = datetime.fromtimestamp(
            int(created_user["createdAt"]) / 1000, timezone.utc
        )
        assert created_at_dt < datetime.now(timezone.utc)

    def test_with_empty_username_(self):
        with pytest.raises(ValidationError) as error:
            user.create(
                username="",
                email="empty.username@orienta.com",
                password="123456",
            )

        assert (
            error.value.message == "O nome de usuario deve ser maior que 3 caracteres."
        )

    def test_with_empty_email(self):
        with pytest.raises(ValidationError) as error:
            user.create(
                username="empty.email",
                email="",
                password="123456",
            )

        assert error.value.message == "O email fornecido é inválido."

    def test_with_empty_password_(self):
        with pytest.raises(ValidationError) as error:
            user.create(
                username="empty.password",
                email="empty.password@orienta.com",
                password="",
            )

        assert error.value.message == "A senha informada é muito curta."

    def test_with_duplicated_email(self):
        user.create(
            username="valid.email", email="valid.email@orienta.com", password="123456"
        )

        with pytest.raises(ValidationError) as error:
            user.create(
                username="in.use.email",
                email="valid.email@orienta.com",
                password="123456",
            )

        assert error.value.message == "O email informado já está sendo utilizado."

    def test_with_invalid_email(self):
        with pytest.raises(ValidationError) as error:
            user.create(username="valid.email", email="email", password="123456")

        assert error.value.message == "O email fornecido é inválido."

    def test_with_short_password_(self):
        with pytest.raises(ValidationError) as error:
            user.create(
                username="short.password",
                email="short.password@orienta.com",
                password="12345",
            )

        assert error.value.message == "A senha informada é muito curta."
