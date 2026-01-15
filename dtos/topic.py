from dataclasses import dataclass

from infra.errors import ValidationError


@dataclass()
class Topic:
    text: str

    MIN_TOPIC_CHARS = 10
    MAX_TOPIC_CHARS = 150

    def __post_init__(self):
        self.text = self.text.strip()

        self._validate()

    @classmethod
    def from_dict(cls, data: dict) -> "Topic":
        return cls(
            text=data.get("text", ""),
        )

    def _validate(self) -> None:
        if not self.text:
            raise ValidationError(
                message="O tópico não pode ser vazio.",
                action="Preencha o tópico do guia e tente novamente.",
            )

        if not isinstance(self.text, str):
            raise ValidationError(
                message="O tópico de estudo precisa ser um texto.",
                action="Verifique se o tópico de estudo é um texto e tente novamente.",
            )

        chars_count = len(self.text)
        if not self.MIN_TOPIC_CHARS <= chars_count <= self.MAX_TOPIC_CHARS:
            raise ValidationError(
                message=f"O tópico de estudo precisa ter no mínimo {self.MIN_TOPIC_CHARS} e no máximo {self.MAX_TOPIC_CHARS} caracteres.",
                action="Verifique o número de caracteres e tente novamente.",
            )

    def check_feasebility():
        pass
