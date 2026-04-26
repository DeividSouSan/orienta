from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class FocusTime:
    value: int

    def __post_init__(self):
        # Handle string input if coming from raw dict
        if isinstance(self.value, str):
            try:
                object.__setattr__(self, "value", int(self.value.strip()))
            except ValueError:
                raise ValidationError(
                    "O tempo de foco (minutos) deve ser um número inteiro."
                )

        if not isinstance(self.value, int):
            raise ValidationError(
                "O tempo de foco (minutos) deve ser um número inteiro."
            )

        if not 30 <= self.value <= 480:
            raise ValidationError(
                message="O tempo de foco precisa estar entre 30 minutos e 8 horas (480 minutos).",
                action="Verifique se o campo 'tempo de foco' está preenchido e tente novamente.",
            )
