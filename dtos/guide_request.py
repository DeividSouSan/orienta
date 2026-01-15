from dataclasses import dataclass

from dtos.topic import Topic
from infra.errors import ValidationError


@dataclass
class GuideRequest:
    title: str
    topic: Topic
    knowledge: str
    focus_time: int
    days: int

    MIN_TITLE_CHARS = 10
    MAX_TITLE_CHARS = 80
    KNOWLEDGE_STATES = ("zero", "iniciante", "intermediario")
    MIN_FOCUS_TIME = 30
    MAX_FOCUS_TIME = 480
    MIN_DAYS = 3
    MAX_DAYS = 30

    def __post_init__(self):
        self.title = self.title.strip()
        self.knowledge = self.knowledge.strip()

        self._validate_title()
        self._validate_knowledge()
        self._validate_focus_time()
        self._validate_days()

    @classmethod
    def from_dict(cls, data: dict) -> "GuideRequest":
        return cls(
            title=data.get("title", ""),
            topic=Topic(data.get("topic", "")),
            knowledge=data.get("knowledge", ""),
            focus_time=data.get("focus_time", ""),
            days=data.get("days", ""),
        )

    def _validate_title(self) -> None:
        self.title = self.title.strip()

        if not self.title:
            raise ValidationError(
                message="O título não pode ser vazio.",
                action="Preencha o título do guia e tente novamente.",
            )

        if not isinstance(self.title, str):
            raise ValidationError(
                message="O título precisa ser um texto.",
                action="Verifique se o título é um texto e tente novamente.",
            )

        chars_count = len(self.title)
        if not self.MIN_TITLE_CHARS <= chars_count <= self.MAX_TITLE_CHARS:
            raise ValidationError(
                message=f"O título do estudo precisa ter no mínimo {self.MIN_TITLE_CHARS} e no máximo {self.MAX_TITLE_CHARS} caracteres.",
                action="Verifique o número de caracteres do título e tente novamente.",
            )

    def _validate_topic(self) -> None:
        self.topic = self.topic.strip()

        if not self.topic:
            raise ValidationError(
                message="O tópico não pode ser vazio.",
                action="Preencha o tópico do guia e tente novamente.",
            )

        if not isinstance(self.topic, str):
            raise ValidationError(
                message="O tópico de estudo precisa ser um texto.",
                action="Verifique se o tópico de estudo é um texto e tente novamente.",
            )

        chars_count = len(self.topic)
        if not self.MIN_TOPIC_CHARS <= chars_count <= self.MAX_TOPIC_CHARS:
            raise ValidationError(
                message=f"O tópico de estudo precisa ter no mínimo {self.MIN_TOPIC_CHARS} e no máximo {self.MAX_TOPIC_CHARS} caracteres.",
                action="Verifique o número de caracteres e tente novamente.",
            )

    def _validate_focus_time(self) -> None:
        if not self.focus_time:
            raise ValidationError(
                message="O tempo de foco não pode ser vazio.",
                action="Preencha o tempo de foco e tente novamente.",
            )

        if not isinstance(self.focus_time, int):
            raise ValidationError(
                message="O tempo de foco (minutos) deve ser um número inteiro.",
                action="Verifique se o tempo de foco é um número inteiro e tente novamente.",
            )

        if not self.MIN_FOCUS_TIME <= self.focus_time <= self.MAX_FOCUS_TIME:
            raise ValidationError(
                message=f"O tempo de foco precisa estar entre {self.MIN_FOCUS_TIME} minutos e {self.MAX_FOCUS_TIME}.",
                action="Verifique se o campo 'tempo de foco' está preenchido corretamente e tente novamente.",
            )

    def _validate_days(self) -> None:
        if not self.days:
            raise ValidationError(
                message="O número de dias não pode ser vazio.",
                action="Preencha o número de dias e tente novamente.",
            )

        if not isinstance(self.days, int):
            raise ValidationError(
                message="O número de dias precisa ser um número inteiro.",
                action="Verifique o número de dias fornecido e tente novamente.",
            )

        if not self.MIN_DAYS <= self.days <= self.MAX_DAYS:
            raise ValidationError(
                message=f"A número de dias precisa estar entre {self.MIN_DAYS} e {self.MAX_DAYS} dias.",
                action="Verifique se o campo 'dias' está preenchido corretamente e tente novamente.",
            )

    def _validate_knowledge(self) -> None:
        if not self.knowledge:
            raise ValidationError(
                message="O conhecimento prévio não pode ser vazio.",
                action="Preencha o conhecimento prévio e tente novamente.",
            )

        if not isinstance(self.knowledge, str):
            raise ValidationError(
                message="O conhecimento prévio deve ser um texto.",
                action="Verifique se o conhecimento prévio fornecido é um texto e tente novamente.",
            )

        if self.knowledge not in self.KNOWLEDGE_STATES:
            raise ValidationError(
                message="O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
                action="Preencha o campo 'knowledge' corretamente e tente novamente.",
            )
