from dataclasses import dataclass

from errors import ValidationError


@dataclass(frozen=True)
class Topic:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("O tópico de estudo precisa ser um texto.")

        # Strip whitespace as per prompt.py logic
        value = self.value.strip()
        object.__setattr__(self, "value", value)

        chars_count = len(value)
        if not 10 <= chars_count <= 150:
            raise ValidationError(
                message="O tópico de estudo precisa ter entre 10 e 150 caracteres.",
                action="Forneça um tópico válido e tente novamente.",
            )
