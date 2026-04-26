from dataclasses import dataclass

from dtos.auth_response import AuthResponseDTO


@dataclass(frozen=True)
class SessionCreateDTO:
    id_token: str

    @classmethod
    def from_dict(cls, data: dict) -> "SessionCreateDTO":
        return cls(id_token=data.get("idToken", ""))

    @classmethod
    def from_auth_response(cls, auth_res: AuthResponseDTO) -> "SessionCreateDTO":
        return cls(id_token=auth_res.id_token)
