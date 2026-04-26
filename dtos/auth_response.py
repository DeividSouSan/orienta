from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthResponseDTO:
    local_id: str
    email: str
    display_name: Optional[str]
    id_token: str
    registered: bool
    refresh_token: str
    expires_in: str

    @classmethod
    def from_dict(cls, data: dict) -> "AuthResponseDTO":
        return cls(
            local_id=data.get("localId", ""),
            email=data.get("email", ""),
            display_name=data.get("displayName"),
            id_token=data.get("idToken", ""),
            registered=data.get("registered", False),
            refresh_token=data.get("refreshToken", ""),
            expires_in=data.get("expiresIn", ""),
        )
