from dataclasses import dataclass


@dataclass(frozen=True)
class SessionRequest:
    email: str
    password: str

    @classmethod
    def from_dict(cls, data: dict) -> "SessionRequest":
        return cls(email=data.get("email", ""), password=data.get("password", ""))
