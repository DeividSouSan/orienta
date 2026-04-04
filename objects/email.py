from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.value or "@" not in self.value:
            raise ValidationError(
                message="Formato de email inválido.",
                action="Forneça um email válido e tente novamente.",
            )
