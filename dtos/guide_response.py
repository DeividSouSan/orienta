from dataclasses import dataclass
from datetime import datetime

from dtos.guide_request import GuideRequest
from infra.response_schema import StudyDaySchema


@dataclass
class GuideResponse:
    owner: str
    inputs: GuideRequest
    model: str
    temperature: float
    study_days: list[StudyDaySchema]
    created_at: datetime
    is_public: bool
