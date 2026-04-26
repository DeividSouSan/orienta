from dataclasses import dataclass

from errors import SchemaError, ValidationError
from objects.focus_time import FocusTime
from objects.knowledge_level import KnowledgeLevel
from objects.study_days import StudyDays
from objects.title import Title
from objects.topic import Topic


@dataclass(frozen=True)
class GuideRequest:
    title: Title
    topic: Topic
    knowledge: KnowledgeLevel
    focus_time: FocusTime
    days: StudyDays

    @classmethod
    def from_dict(cls, data: dict) -> "GuideRequest":
        try:
            return cls(
                title=Title(data.get("title", "")),
                topic=Topic(data.get("topic", "")),
                knowledge=KnowledgeLevel(data.get("knowledge", "")),
                focus_time=FocusTime(data.get("focus_time", 0)),
                days=StudyDays(data.get("days", 0)),
            )
        except ValidationError as error:
            # Re-raise with same info but could wrap if needed.
            # In this project, VOs already have specific messages.
            raise error
        except Exception as error:
            raise SchemaError(
                message="Dados inválidos para criação do guia.",
                action="Verifique todos os campos e tente novamente.",
            ) from error

    def to_dict(self) -> dict:
        return {
            "title": self.title.value,
            "topic": self.topic.value,
            "knowledge": self.knowledge.value,
            "focus_time": self.focus_time.value,
            "days": self.days.value,
        }
