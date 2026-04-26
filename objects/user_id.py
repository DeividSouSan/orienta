from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class UserId:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("O ID do usuário precisa ser um texto.")

        value = self.value.strip()
        object.__setattr__(self, "value", value)

        if not value:
            raise ValidationError("O ID do usuário não pode ser vazio.")
