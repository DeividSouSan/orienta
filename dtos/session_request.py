from dataclasses import dataclass

from errors import ValidationError
from objects.email import Email
from objects.password import Password


@dataclass(frozen=True)
class SessionRequest:
    email: Email
    password: Password

    @classmethod
    def from_dict(cls, data: dict) -> "SessionRequest":
        try:
            return cls(
                email=Email(data.get("email", "")),
                password=Password(data.get("password", "")),
            )
        except ValidationError:
            raise ValidationError(
                message="Email ou senha inválidos.",
                action="Verifique os dados e tente novamente.",
            )
