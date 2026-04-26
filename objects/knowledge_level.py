from dataclasses import dataclass

from errors import ValidationError

KNOWLEDGE_STATES = ("zero", "iniciante", "intermediario")


@dataclass(frozen=True)
class KnowledgeLevel:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("O conhecimento deve ser um texto.")

        value = self.value.strip().lower()
        object.__setattr__(self, "value", value)

        if value not in KNOWLEDGE_STATES:
            raise ValidationError(
                message="O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
                action="Preencha o campo 'knowledge' corretamente e tente novamente.",
            )
