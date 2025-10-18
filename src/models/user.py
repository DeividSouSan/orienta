from firebase_admin import auth, exceptions
from firebase_admin.auth import UserRecord, UserNotFoundError
from src.errors import ValidationError, ServiceError


def find(email: str) -> dict[str, any] | None:
    try:
        storedUser: UserRecord = auth.get_user_by_email(email)
        return storedUser.__dict__["_data"]
    except UserNotFoundError:
        return None
    except ValueError as error:
        raise ValidationError("O email fornecido é inválido.") from error
    except exceptions.FirebaseError as error:
        raise ServiceError(
            "Houve um erro ao buscar o usuáro com o email fornecido."
        ) from error


def create(*, username, email, password) -> dict[str, any]:
    def validate_username(username: str) -> None:
        if len(username) < 3:
            raise ValidationError(
                "O nome de usuario deve ser maior que 3 caracteres.",
            )

    def validate_email(email: str) -> None:
        if find(email):
            raise ValidationError(
                "O email informado já está sendo utilizado.",
            )

    def validate_password(password: str) -> None:
        if len(password) < 6:
            raise ValidationError(
                "A senha informada é muito curta.",
            )

    validate_username(username)
    validate_email(email)
    validate_password(password)

    try:
        createdUser: UserRecord = auth.create_user(
            email=email,
            password=password,
            display_name=username,
        )
    except ValueError as error:
        raise ValidationError(
            "A entrada (email, password ou username) fornecida é inválida."
        ) from error
    except exceptions.FirebaseError as error:
        raise ServiceError("Houve um erro ao criar o usuário") from error

    return createdUser.__dict__["_data"]
