import traceback
from typing import cast

from firebase_admin import auth, exceptions, firestore
from firebase_admin.auth import UserRecord
from google.cloud.firestore_v1.base_query import FieldFilter

from dtos.user import UserDTO
from dtos.user_create_request import UserCreateRequest
from errors import ConflictError, NotFoundError, ServiceError, ValidationError
from objects.username import Username


def find_by_username(username: Username) -> UserDTO:
    """Busca os dados de um usuário no banco de dados.

    Args:
        username (Username): o VO do nome do usuário que se quer os dados.

    Returns:
        UserDTO: os dados do usuário consultado.

    Raises:
        NotFoundError: se o usuário procurado não for encontrado.
    """

    db = firestore.client()

    results = (
        db.collection("users")
        .where(filter=FieldFilter("username", "==", username.value))
        .limit(1)
        .get()
    )

    if results and results[0].exists:
        user = results[0]

        return UserDTO(
            username=user.get("username"),
            uid=user.get("uid"),
            email=user.get("email"),
            created_at=user.get("created_at"),
        )
    else:
        raise NotFoundError(
            "O usuário não foi encontrado.",
            "Verifique se o nome foi digitado corretamente e tente de novo.",
        )


def find_by_email(username: str):
    """Busca os dados de um usuário no banco de dados."""
    pass


def create(request: UserCreateRequest) -> UserDTO:
    """Cria um novo usuário no sistema.

    Args:
        request (UserCreateRequest): DTO com username, email e password já validados.

    Returns:
        UserDTO: objeto com as informações do usuário que foi criado.

    Raises:
        ValidationError: se as entradas (username, email ou password) forem inválidas.
        ServiceError: se o serviço do Firebase Auth não estiver disponível.
    """

    try:
        db = firestore.client()

        if (
            db.collection("users")
            .where(filter=FieldFilter("username", "==", request.username.value))
            .get()
        ):
            raise ConflictError(
                "O nome de usuário fornecido já está sendo utilizado.",
                "Insira outro nome de usuário e tente novamente.",
            )

        created_user: UserRecord = auth.create_user(
            email=request.email.value,
            password=request.password.value,
            display_name=request.username.value,
        )

        user_data = UserDTO(
            username=cast(str, created_user.display_name),
            email=cast(str, created_user.email),
            uid=cast(str, created_user.uid),
            created_at=str(created_user.user_metadata.creation_timestamp),
        )

        db.collection("users").document().set(
            {
                "username": user_data.username,
                "email": user_data.email,
                "uid": user_data.uid,
                "created_at": user_data.created_at,
            }
        )

        return user_data

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
