from datetime import timedelta

from firebase_admin import auth, exceptions

from infra.errors import ServiceError, UnauthorizedError, ValidationError

DURATION_IN_SECONDS = 14 * 24 * 60 * 60  # 14 dias


def create(
    token: str,
    duration=timedelta(seconds=DURATION_IN_SECONDS),
) -> str:
    """Cria um novo cookie de sessão.

    Args:
        token (str): Firebase ID token do usuário.
        duration (timedelta): duração do cookie de sessão (default é 14 dias)

    Returns:
        str: cookie de sessão com JWT.

    Raises:
        ValidationError: se o token estiver vazio ou a duração for maior que o permitido.
        UnauthorizedError: se o ID token não for um token do Firebase válido.
        ServiceError: se ocorreu um erro com o Firebase Authentication.
    """
    if not token:
        raise ValidationError("O idToken não pode ser vazio.")

    if duration > timedelta(seconds=DURATION_IN_SECONDS):
        raise ValidationError("Duração da sessão é tem que ser menor que 14 dias.")

    try:
        return auth.create_session_cookie(id_token=token, expires_in=duration)
    except (
        auth.InvalidIdTokenError,
        auth.ExpiredIdTokenError,
        auth.RevokedIdTokenError,
    ) as error:
        raise UnauthorizedError(
            "Não foi possível criar a sessão. O ID token não é um token de código do Firebase válido."
        ) from error
    except ValueError as error:
        raise ServiceError(
            "Ocorreu um erro ao processar a solicitação de sessão."
        ) from error
    except exceptions.FirebaseError as error:
        raise ServiceError(
            "Ocorreu um erro ao se comunicar com o serviço de autenticação."
        ) from error


def verify_cookie(
    cookie: str,
) -> dict:
    """Verifica se o cookie de sessão é válido.

    Args:
        cookie (str): o cookie de sessão que se quer verificar.

    Returns:
        dict: um dicionário com informações sobre o cookie.

    Raises:
        ValidationError: se o cookie estiver vazio.
        UnauthorizedError: se o cookie de sessão estiver expirado ou revogado.
        ServiceError: se ocorrer um erro de comunicação com o Firebase.
    """
    if not cookie:
        raise ValidationError(
            "Ocorreu um erro ao validar o cookie: o cookie não pode ser vázio."
        )

    try:
        return auth.verify_session_cookie(cookie, check_revoked=True)
    except (auth.ExpiredSessionCookieError, auth.RevokedSessionCookieError) as error:
        raise UnauthorizedError(
            "Ocorreu um erro ao verificar a sessão: sessão expirada ou revogada."
        ) from error
    except auth.InvalidSessionCookieError as error:
        raise UnauthorizedError(
            "Ocorreu um erro ao validar o cookie de sessão. O cookie não é um cookie de sessão do Firebase válido."
        ) from error
    except auth.CertificateFetchError as error:
        raise ServiceError(
            "Ocorreu um erro ao verificar o cookie: serviço de autenticação indisponível."
        ) from error
    except Exception as error:
        raise ServiceError(
            "Ocorreu um erro de comunicação com o serviço de verificação."
        ) from error
