from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class GuideId:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("O ID do guia precisa ser um texto.")

        value = self.value.strip()
        object.__setattr__(self, "value", value)

        if not value:
            raise ValidationError(
                message="O ID do guia não pode ser vazio.",
                action="Verifique se o ID foi enviado corretamente e tente novamente.",
            )
