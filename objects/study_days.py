from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class StudyDays:
    value: int

    def __post_init__(self):
        if isinstance(self.value, str):
            try:
                object.__setattr__(self, "value", int(self.value.strip()))
            except ValueError:
                raise ValidationError("O número de dias precisa ser um número inteiro.")

        if not isinstance(self.value, int):
            raise ValidationError("O número de dias precisa ser um número inteiro.")

        if not 3 <= self.value <= 30:
            raise ValidationError(
                message="A duração do estudo precisa estar entre 3 e 30 dias.",
                action="Verifique se o campo 'duração' está preenchido e tente novamente.",
            )
