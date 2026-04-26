from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("O título do estudo precisa ser um texto.")

        value = self.value.strip()
        object.__setattr__(self, "value", value)

        chars_count = len(value)
        if not 10 <= chars_count <= 80:
            raise ValidationError(
                message="O título do estudo precisa ter no mínimo 10 e no máximo 80 caracteres.",
                action="Verifique o número de caracteres do título e tente novamente.",
            )
