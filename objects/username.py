from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("O nome de usuário inserido não é válido.")

        value = self.value.strip()
        object.__setattr__(self, "value", value)

        if not (3 <= len(value)):
            raise ValidationError(
                message="O nome de usuário inserido não é válido.",
                action="Insira um nome de usuário maior que 3 caracteres.",
            )
