from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class FirebaseUserDTO:
    uid: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_claims(cls, claims: dict) -> "FirebaseUserDTO":
        return cls(
            uid=claims.get("uid") or claims.get("user_id"),
            email=claims.get("email"),
            name=claims.get("name"),
            picture=claims.get("picture"),
            username=claims.get("username"),
        )

    def to_dict(self) -> dict:
        return asdict(self)
