import pytest
from src.errors import UnauthorizedError
from src.models import auth


class TestAuthentication:
    def test_with_correct_email_and_correct_password(self):
        user_data = auth.authenticate(email="mock@orienta.com", password="123456")

        assert user_data["idToken"] is not None
        assert isinstance(user_data["idToken"], str)
        assert user_data["email"] == "mock@orienta.com"
        assert user_data["registered"] is True
        assert user_data["displayName"] == "mock"

    def test_with_wrong_email_and_correct_password(self):
        with pytest.raises(UnauthorizedError) as error:
            auth.authenticate(email="wrong-mock@orienta.com", password="123456")

        assert error.value.name == "UnauthorizedError"
        assert (
            error.value.message
            == "Dados de autenticação não conferem, email ou senha errados."
        )

    def test_with_correct_email_and_wrong_password(self):
        with pytest.raises(UnauthorizedError) as error:
            auth.authenticate(email="mock@orienta.com", password="wrong-password")

        assert error.value.name == "UnauthorizedError"
        assert (
            error.value.message
            == "Dados de autenticação não conferem, email ou senha errados."
        )

    def test_with_empty_email_and_correct_password(self):
        with pytest.raises(UnauthorizedError) as error:
            auth.authenticate(email="", password="123456")

        assert error.value.name == "UnauthorizedError"
        assert (
            error.value.message
            == "Dados de autenticação não conferem, email ou senha errados."
        )

    def test_with_correct_email_and_empty_password(self):
        with pytest.raises(UnauthorizedError) as error:
            auth.authenticate(email="mock@orienta.com", password="")

        assert error.value.name == "UnauthorizedError"
        assert (
            error.value.message
            == "Dados de autenticação não conferem, email ou senha errados."
        )

    def test_with_invalid_email(self):
        with pytest.raises(UnauthorizedError) as error:
            auth.authenticate(email="mock", password="123456")

        assert error.value.name == "UnauthorizedError"
        assert (
            error.value.message
            == "Dados de autenticação não conferem, email ou senha errados."
        )
