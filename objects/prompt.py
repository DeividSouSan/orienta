from dataclasses import dataclass

from objects.focus_time import FocusTime
from objects.knowledge_level import KnowledgeLevel
from objects.study_days import StudyDays
from objects.topic import Topic


@dataclass(frozen=True)
class Prompt:
    topic: Topic
    knowledge: KnowledgeLevel
    focus_time: FocusTime
    days: StudyDays

    def to_xml(self) -> str:
        return f"""
    <INPUTS>
        <TOPIC>{self.topic.value}</TOPIC>
        <KNOWLEDGE>{self.knowledge.value}</KNOWLEDGE>
        <FOCUS_TIME>{self.focus_time.value} minutes</FOCUS_TIME>
        <DURATION_IN_DAYS>{self.days.value} days</DURATION_IN_DAYS>
    </INPUTS>
    """
