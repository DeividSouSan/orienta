from dataclasses import dataclass

from errors import ValidationError
from objects.email import Email
from objects.password import Password
from objects.username import Username


@dataclass(frozen=True)
class UserCreateRequest:
    username: Username
    email: Email
    password: Password

    @classmethod
    def from_dict(cls, data: dict) -> "UserCreateRequest":
        try:
            return cls(
                username=Username(data.get("username", "")),
                email=Email(data.get("email", "")),
                password=Password(data.get("password", "")),
            )
        except ValidationError as error:
            raise error
