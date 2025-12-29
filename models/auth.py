import os
from dotenv import load_dotenv
import requests
from errors import UnauthorizedError, ServiceError, ValidationError

load_dotenv()

API_KEY = os.getenv("FIREBASE_API_KEY")
FB_REST_API = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
KNOWN_ERRORS = {"INVALID_LOGIN_CREDENTIALS", "MISSING_PASSWORD", "INVALID_EMAIL"}


def authenticate(email: str, password: str) -> dict[str, str]:
    if not email or not password:
        raise ValidationError(
            "Email ou senha inválidos.", "Verifique os dados e tente novamente."
        )

    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(url=FB_REST_API, json=payload, timeout=10)
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
