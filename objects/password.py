from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 6:
            raise ValidationError(
                message="A senha deve ter pelo menos 6 caracteres.",
                action="Forneça uma senha com no mínimo 6 caracteres e tente novamente.",
            )
        if " " in self.value:
            raise ValidationError(
                message="A senha não pode conter espaços.",
                action="Forneça uma senha sem espaços e tente novamente.",
            )
