import os

import requests
from dotenv import load_dotenv

from errors import ServiceError, UnauthorizedError
from objects.email import Email
from objects.password import Password

load_dotenv()

API_KEY = os.getenv("FIREBASE_API_KEY")
KNOWN_ERRORS = {"INVALID_LOGIN_CREDENTIALS", "MISSING_PASSWORD", "INVALID_EMAIL"}


def authenticate(email: Email, password: Password) -> dict[str, str]:
    payload = {
        "email": email.value,
        "password": password.value,
        "returnSecureToken": True,
    }

    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        response = requests.post(url=url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as error:
        error_data = error.response.json()
        error_code = error_data.get("error", {}).get("message")

        if error_code in KNOWN_ERRORS:
            raise UnauthorizedError(
                "Email ou senha errados.",
                "Verifique os dados e tente novamente.",
            ) from error

        raise
    except requests.RequestException as error:
        raise ServiceError(
            "Ocorreu um erro ao se comunicar com o serviço de autenticação."
        ) from error
