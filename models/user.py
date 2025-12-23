from typing import cast
import traceback
from firebase_admin import auth, exceptions, firestore
from firebase_admin.auth import UserRecord
from google.cloud.firestore_v1.base_query import FieldFilter
from errors import ConflictError, NotFoundError, ServiceError, ValidationError


def find_by_username(username: str):
    """Busca os dados de um usuário no banco de dados.

    Args:
        username (str): o nome do usuário que se quer os dados.

    Returns:
        dict[str, str]: os dados do usuário consultado.

    Raises:
        NotFoundError: se o usuário procurado não for encontrado.
    """

    validate_username(username)

    db = firestore.client()

    results = (
        db.collection("users")
        .where(filter=FieldFilter("username", "==", username))
        .limit(1)
        .get()
    )

    if results and results[0].exists:
        user = results[0]

        return {
            "username": user.get("username"),
            "uid": user.get("uid"),
            "email": user.get("username"),
            "created_at": user.get("created_at"),
        }
    else:
        raise NotFoundError(
            "O usuário não foi encontrado.",
            "Verifique se o nome foi digitado corretamente e tente de novo.",
        )


def find_by_email(username: str):
    """Busca os dados de um usuário no banco de dados.

    Args:
        username (str): o nome do usuário que se quer os dados.

    Returns:
        dict[str, str]: os dados do usuário consultado.
    """

    pass


def validate_username(username: str) -> None:
    """Valida se o nome de usuário está formatado corretamente.

    Args:
        username (str): o nome de usuário que se quer validar.

    Returns:
        None (sucesso): se o nome de usuário é válido.

    Raises:
        ValidationError: se o nome de usuário não é válido.
    """
    if not (3 <= len(username) <= 20):
        raise ValidationError(
            "O nome de usuário inserido não é válido.",
            "Insira um nome de usuário maior que 3 caracteres e menor que 20 caracteres.",
        )


def create(*, username: str, email: str, password: str) -> dict[str, str]:
    """Cria um novo usuário no sistema.

    Args:
        username (str): nome de usuário.
        email (str): email do usuário.
        password (str): senha do usuário.

    Returns:
        dict[str, str]: dicionário com as informações do usuário que foi criado.

    Raises:
        ValidationError: se as entradas (username, email ou password) forem inválidas.
        ServiceError: se o serviço do Firebase Auth não estiver disponível.
    """

    def validate_password(password: str) -> None:
        if len(password) < 6:
            raise ValidationError(
                action="Insira uma senha maior que 6 caracteres.",
            )

    def validate_email(email: str) -> None:
        if not email:
            raise ValidationError(
                action="Verifique o e-mail e tente novamente.",
            )

    validate_username(username)
    validate_password(password)
    validate_email(email)

    try:
        db = firestore.client()

        if (
            db.collection("users")
            .where(filter=FieldFilter("username", "==", username))
            .get()
        ):
            raise ConflictError(
                "O nome de usuário fornecido já está sendo utilizado.",
                "Insira outro nome de usuário e tente novamente.",
            )

        created_user: UserRecord = auth.create_user(
            email=email,
            password=password,
            display_name=username,
        )

        created_user_data = {
            "username": cast(str, created_user.display_name),
            "email": cast(str, created_user.email),
            "uid": cast(str, created_user.uid),
            "created_at": str(created_user.user_metadata.creation_timestamp),
        }

        db.collection("users").document().set(created_user_data)
    except auth.EmailAlreadyExistsError as error:
        raise ConflictError(
            "O e-mail fornecido já está sendo utilizado.",
            "Insira outro e-mail e tente novamente.",
        ) from error
    except ValueError as error:
        raise ValidationError(
            "A entrada (email, password ou username) fornecida é inválida."
        ) from error
    except exceptions.FirebaseError as error:
        traceback.print_exc()
        raise ServiceError("Não foi possível criar o usuário.") from error

    return created_user_data
