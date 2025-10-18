from datetime import timedelta
from firebase_admin import auth, exceptions

from src.errors import UnauthorizedError, ValidationError, ServiceError

DURATION_IN_SECONDS = 14 * 24 * 60 * 60  # 14 dias


def create(
    token: str,
    duration=timedelta(seconds=DURATION_IN_SECONDS),
) -> str:
    if not isinstance(token, str):
        raise ValidationError("O idToken deve ser um texto.")

    if not token:
        raise ValidationError("O idToken não pode ser vazio.")

    if duration > timedelta(seconds=DURATION_IN_SECONDS):
        raise ValidationError("Duração da sessão é tem que ser menor que 14 dias.")

    try:
        return auth.create_session_cookie(id_token=token, expires_in=duration)
    except auth.InvalidIdTokenError as error:
        raise UnauthorizedError("O idToken fornecido é inválido.") from error
    except ValueError as error:
        raise ValidationError(
            "O idToken não pode ser vazio e a duração da sessão tem que ser maior que 14 dias."
        ) from error
    except exceptions.FirebaseError as error:
        raise ServiceError("Ocorreu um erro ao criar o cookie de sessão.") from error


def verify(
    cookie: str,
) -> dict:
    if not cookie:
        raise UnauthorizedError("O cookie de sessão não pode ser vazio.")

    try:
        return auth.verify_session_cookie(cookie, check_revoked=True)
    except (auth.InvalidSessionCookieError, auth.RevokedSessionCookieError) as error:
        raise UnauthorizedError("Sessão inválida ou expirada.") from error
    except auth.CertificateFetchError as error:
        raise UnauthorizedError("Serviço de autenticação indisponível.") from error
    except Exception as error:
        raise UnauthorizedError(
            "Ocorreu um erro inesperado durante a autenticação."
        ) from error
