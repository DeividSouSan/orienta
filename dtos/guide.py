from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional

from dtos.guide_request import GuideRequest
from objects.username import Username


@dataclass(frozen=True)
class GuideDTO:
    owner: Username
    inputs: GuideRequest
    model: str
    temperature: float
    generation_time_seconds: int
    daily_study: List[dict]  # Podemos evoluir para um DTO de DailyStudy depois
    created_at: datetime
    is_public: bool
    status: str = "studying"
    completed_at: Optional[datetime] = None
    id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "GuideDTO":
        # Note: data might have 'id' from Firestore document ID
        return cls(
            id=data.get("id"),
            owner=Username(data.get("owner")),
            inputs=GuideRequest.from_dict(data.get("inputs", {})),
            model=data.get("model", "unknown"),
            temperature=data.get("temperature", 2.0),
            generation_time_seconds=data.get("generation_time_seconds", 0),
            daily_study=data.get("daily_study", []),
            created_at=data.get("created_at")
            if isinstance(data.get("created_at"), datetime)
            else datetime.now(),
            is_public=data.get("is_public", False),
            status=data.get("status", "studying"),
            completed_at=data.get("completed_at"),
        )

    def to_dict(self) -> dict:
        result = asdict(self)
        # Convert VOs to primitives
        result["owner"] = self.owner.value
        result["inputs"] = self.inputs.to_dict()

        # Clean up None values (like id or completed_at when not set)
        return {k: v for k, v in result.items() if v is not None}
