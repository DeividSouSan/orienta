import os
from dotenv import load_dotenv
import requests
from src.errors import UnauthorizedError, ServiceError

load_dotenv()

API_KEY = os.getenv("FIREBASE_API_KEY")
FB_REST_API = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
KNOWN_ERRORS = {"INVALID_LOGIN_CREDENTIALS", "MISSING_PASSWORD", "INVALID_EMAIL"}


def authenticate(email: str, password: str) -> dict[str, any]:
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
                "Dados de autenticação não conferem, email ou senha errados.",
            ) from error

        raise
    except requests.RequestException as error:
        raise ServiceError(
            "O serviço de autenticação falhou. Aguarde um momento e tente novamente."
        ) from error
